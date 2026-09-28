"""Atomic local records and a persistent, one-attempt-per-key request ledger."""

from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

from jsonschema import validate

from scripts.build_runtime_profile import canonical, digest
from src.ai.llm_client import LLMError
from src.ai.model_profiles import ProfileError


class PipelineError(ValueError):
    """Safe operator-facing error; never include raw model/SDK data."""


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=".runner-",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_json(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


@contextmanager
def workspace_lock(root):
    path = root / "data/pipeline_cache/runner.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = path.open("x", encoding="utf-8")
    except FileExistsError:
        raise PipelineError(
            "Runner is locked. If a prior process crashed, verify it has stopped before removing data/pipeline_cache/runner.lock."
        ) from None
    try:
        with handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        path.unlink(missing_ok=True)


def cached_call(root, identity, client, messages, schema, schema_name, validate_content):
    """COMPLETE hits reuse output. FAILED_OR_UNCERTAIN may be retried after a fix. ATTEMPTED stays locked."""
    key = digest(canonical(identity))
    path = root / "data/pipeline_cache" / f"{key}.json"
    if path.exists():
        record = read_json(path)
        if record.get("identity") != identity:
            raise PipelineError(
                "Cache identity mismatch; inspect local cache without retrying a paid call."
            )
        if record.get("status") == "FAILED_OR_UNCERTAIN":
            path.unlink()
        elif record.get("status") != "COMPLETE":
            raise PipelineError(
                f"Request {key} was already attempted or interrupted. No automatic paid retry; inspect the ledger."
            )
        else:
            result = record["result"]
            if digest(canonical(result)) != record.get("result_sha256"):
                raise PipelineError("Cached result failed its content hash; no paid retry.")
            validate(result, schema)
            validate_content(result)
            return result, {
                "key": key,
                "result": "HIT",
                "identity": identity,
                "model_used": record["model_used"],
                "usage": record.get("usage"),
            }
    # Request construction validates settings without credentials or network access.
    plans = client.build_requests(messages, json_schema=schema, schema_name=schema_name)
    if len(plans) != 1:
        raise PipelineError(
            "Canonical route requires exactly one primary request with no fallbacks."
        )
    model_used = {
        "profile": identity["model_profile"],
        "provider": plans[0].provider,
        "model": plans[0].model,
    }
    claim = {
        "identity": identity,
        "status": "ATTEMPTED",
        "max_provider_requests": 1,
        "model_used": model_used,
    }
    # Exclusive creation is a second protection even if a caller omitted the workspace lock.
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            json.dump(claim, handle)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        raise PipelineError("Cache key claimed by another run; no paid request made.") from None
    try:
        raw = client.chat(messages, json_schema=schema, schema_name=schema_name)
        result = json.loads(raw)
        validate(result, schema)
        validate_content(result)
        write_json(
            path,
            {
                **claim,
                "status": "COMPLETE",
                "result": result,
                "result_sha256": digest(canonical(result)),
                "usage": client.last_usage,
            },
        )
    except Exception as error:
        # Keep a fixed safe status, not the provider body or generated private text.
        write_json(path, {**claim, "status": "FAILED_OR_UNCERTAIN"})
        detail = ""
        if isinstance(error, (PipelineError, LLMError, ProfileError)):
            detail = " " + str(error).strip()
        raise PipelineError(
            f"Request {key} failed validation or provider execution.{detail} "
            "Fix the cause and rerun; a failed cache entry is retried."
        ) from None
    return result, {
        "key": key,
        "result": "MISS",
        "identity": identity,
        "model_used": model_used,
        "usage": client.last_usage,
    }
