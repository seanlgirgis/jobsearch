"""Opt-in OpenAI-compatible chat client for OpenRouter, xAI and OpenAI.

Legacy GrokClient remains independent during the foundation step.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from jsonschema.validators import validator_for
from openai import APIConnectionError, APIStatusError, OpenAI

from .model_profiles import CONFIG_DIR, ROOT, ProfileError, get_profile, load_profiles

# Fixed endpoints keep credentials scoped to their provider, independently of ambient SDK defaults.
PROVIDERS = {
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "xai": ("https://api.x.ai/v1", "XAI_API_KEY"),
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
}
FALLBACK_STATUSES = {400, 404, 408, 409, 422, 429, 500, 502, 503, 504}
JSON_ONLY = (
    "Reply with a single JSON object that matches the requested schema. "
    "No markdown fences and no commentary."
)


class LLMError(RuntimeError):
    """Concise public failure; raw SDK errors and response bodies are never exposed."""


@dataclass(frozen=True)
class ChatRequest:
    """Inspectable request without headers or credentials."""

    provider: str
    model: str
    parameters: dict[str, Any]


def _field(value: Any, name: str) -> Any:
    if isinstance(value, Mapping):
        return value.get(name)
    direct = getattr(value, name, None)
    if direct is not None:
        return direct
    extra = getattr(value, "model_extra", None)
    if isinstance(extra, Mapping):
        return extra.get(name)
    return None


def _number(value: Any, kind: type[int] | type[float]) -> int | float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return kind(value)
    except (TypeError, ValueError):
        return None


def usage_summary(response: Any) -> dict[str, Any] | None:
    """Return safe provider-reported usage when available; never estimate costs."""
    usage = _field(response, "usage")
    if usage is None:
        return None
    completion_details = _field(usage, "completion_tokens_details")
    result = {
        "prompt_tokens": _number(_field(usage, "prompt_tokens"), int),
        "completion_tokens": _number(_field(usage, "completion_tokens"), int),
        "total_tokens": _number(_field(usage, "total_tokens"), int),
        "reasoning_tokens": _number(_field(completion_details, "reasoning_tokens"), int),
        "actual_usd": _number(_field(usage, "cost"), float),
    }
    return {key: value for key, value in result.items() if value is not None} or None


def _schema_validator(schema: dict[str, Any]) -> Any:
    """Check schema locally; allow only in-document references (never fetch a URL)."""

    def check_refs(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {"$ref", "$dynamicRef", "$recursiveRef"} and (
                    not isinstance(child, str) or not child.startswith("#")
                ):
                    raise ValueError("External schema reference")
                check_refs(child)
        elif isinstance(value, list):
            for child in value:
                check_refs(child)

    try:
        if not isinstance(schema, dict):
            raise ValueError("Schema must be an object")
        check_refs(schema)
        json.dumps(schema, allow_nan=False)
        validator = validator_for(schema)
        validator.check_schema(schema)
        return validator(schema)
    except Exception:
        raise ProfileError(
            "Invalid JSON schema; use a valid schema with local references only."
        ) from None


def _unwrap_result(value: Any) -> Any:
    if isinstance(value, dict) and "score" not in value:
        for key in ("analysis", "result", "data", "job_analysis"):
            inner = value.get(key)
            if isinstance(inner, dict):
                return inner
    return value


def _fill_required(value: Any, schema: dict[str, Any]) -> Any:
    if not isinstance(value, dict) or not isinstance(schema, dict):
        return value
    required = schema.get("required") or []
    properties = schema.get("properties") or {}
    filled = dict(value)
    for key in required:
        if key in filled and filled[key] is not None:
            continue
        spec = properties.get(key) or {}
        types = spec.get("type")
        allowed = {types} if isinstance(types, str) else set(types or ())
        if "null" in allowed:
            filled[key] = None
        elif spec.get("enum"):
            filled[key] = "REVIEW" if "REVIEW" in spec["enum"] else spec["enum"][0]
        elif "integer" in allowed:
            # Never invent a numerical result merely to make a model response valid.
            continue
        elif "array" in allowed:
            filled[key] = ["Requires manual review"] if spec.get("minItems", 0) else []
        elif "string" in allowed:
            filled[key] = "Requires manual review"
    return filled


def _coerce_for_schema(value: Any, schema: dict[str, Any]) -> Any:
    """Clip strings/arrays and drop unknown fields so cheap models can miss strict bounds."""
    if not isinstance(schema, dict):
        return value
    for option in schema.get("anyOf", []):
        if not isinstance(option, dict):
            continue
        option_type = option.get("type")
        option_types = {option_type} if isinstance(option_type, str) else set(option_type or ())
        if value is None and "null" in option_types:
            return _coerce_for_schema(value, option)
        if isinstance(value, dict) and "object" in option_types:
            return _coerce_for_schema(value, option)
        if isinstance(value, list) and "array" in option_types:
            return _coerce_for_schema(value, option)
    types = schema.get("type")
    allowed = {types} if isinstance(types, str) else set(types or ())
    if "object" in allowed and isinstance(value, dict):
        properties = schema.get("properties") or {}
        extra = schema.get("additionalProperties", True)
        coerced = {
            key: _coerce_for_schema(value[key], sub)
            for key, sub in properties.items()
            if key in value
        }
        if extra is not False:
            for key, child in value.items():
                if key not in coerced:
                    coerced[key] = child
        return coerced
    if "array" in allowed:
        item_schema = schema.get("items") or {}
        maximum = schema.get("maxItems")
        if isinstance(value, list):
            raw_items = value
        elif isinstance(value, str) and value.strip():
            raw_items = [value]
        else:
            raw_items = []
        items = [_coerce_for_schema(item, item_schema) for item in raw_items]
        if isinstance(maximum, int):
            items = items[:maximum]
        if not items and schema.get("minItems", 0):
            items = ["Requires manual review"]
        return items
    if "string" in allowed and value is not None and not isinstance(value, bool):
        text = value if isinstance(value, str) else str(value)
        maximum = schema.get("maxLength")
        if isinstance(maximum, int) and len(text) > maximum:
            text = text[:maximum]
        choices = schema.get("enum")
        if choices and text not in choices:
            text = "REVIEW" if "REVIEW" in choices else choices[0]
        return text
    if "integer" in allowed and not isinstance(value, bool):
        try:
            number = int(value)
        except (TypeError, ValueError):
            return value
        if "minimum" in schema:
            number = max(number, int(schema["minimum"]))
        if "maximum" in schema:
            number = min(number, int(schema["maximum"]))
        return number
    return value


def _extract_json_text(content: str) -> str:
    """Accept raw JSON or a fenced/prose wrapper; used after a plain chat completion."""
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, count=1, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text.strip()


class LLMClient:
    """Synchronous text chat with explicit profiles and bounded fallback attempts.

    `chat` always returns a stripped string, including validated JSON as a string.
    `build_requests` is a no-network preview. Instantiate again to load a changed profile.
    """

    def __init__(
        self,
        profile: str | None = None,
        *,
        config_dir: Path = CONFIG_DIR,
        env_file: Path = ROOT / ".env",
        environ: Mapping[str, str] | None = None,
        client_factory: Callable[..., Any] = OpenAI,
    ) -> None:
        config = load_profiles(config_dir)
        self.profile_name = config.active_profile if profile is None else profile
        self.profile = get_profile(config, profile)
        self._env_file = env_file
        self._environ = environ
        self._client_factory = client_factory
        self.last_usage: dict[str, Any] | None = None

    def build_requests(
        self,
        messages: list[dict[str, Any]],
        *,
        json_schema: dict[str, Any] | None = None,
        schema_name: str = "result",
    ) -> list[ChatRequest]:
        """Construct the primary and eligible fallbacks; never read keys or call an API."""
        if (
            not messages
            or not isinstance(messages, list)
            or any(
                not isinstance(message, dict)
                or message.get("role") not in {"system", "developer", "user", "assistant"}
                or not isinstance(message.get("content"), str)
                for message in messages
            )
        ):
            raise ProfileError("Chat requires a nonempty list of role/content text messages.")
        if self.profile.structured_output == "required" and json_schema is None:
            raise ProfileError(
                "This profile requires json_schema; plain-text fallback is disabled."
            )
        if json_schema is not None:
            if self.profile.structured_output == "off":
                raise ProfileError("Structured output is disabled for this profile.")
            if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", schema_name):
                raise ProfileError(
                    "Schema name must use 1-64 letters, digits, underscores or dashes."
                )
            _schema_validator(json_schema)
        requests = []
        seen: set[tuple[str, str]] = set()
        for target in self.profile.targets:
            if target.model is None:
                raise ProfileError(
                    "Set actual model IDs in config/model_profiles.local.json first."
                )
            if json_schema is not None and not target.supports_json_schema:
                continue
            identity = (target.provider, target.model)
            if identity in seen:
                continue
            seen.add(identity)
            token_key = target.token_parameter or (
                "max_completion_tokens" if target.provider == "openai" else "max_tokens"
            )
            outgoing = list(messages)
            if json_schema is not None and target.provider == "openrouter":
                outgoing = [*messages, {"role": "user", "content": JSON_ONLY}]
            parameters: dict[str, Any] = {
                "model": target.model,
                "messages": outgoing,
                token_key: self.profile.max_output_tokens,
            }
            if target.supports_temperature and self.profile.temperature is not None:
                parameters["temperature"] = self.profile.temperature
            if target.provider == "openrouter" and self.profile.reasoning_effort is not None:
                parameters["extra_body"] = {
                    "reasoning": {"effort": self.profile.reasoning_effort, "exclude": True}
                }
            # OpenRouter/DeepSeek (and similar) reject strict json_schema + require_parameters.
            # Keep native json_schema for OpenAI/xAI; OpenRouter uses plain chat + local validation.
            if json_schema is not None and target.provider != "openrouter":
                parameters["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": schema_name, "strict": True, "schema": json_schema},
                }
            requests.append(ChatRequest(target.provider, target.model, parameters))
        if not requests:
            raise ProfileError("No configured target supports the requested JSON-schema output.")
        return requests

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        json_schema: dict[str, Any] | None = None,
        schema_name: str = "result",
    ) -> str:
        requests = self.build_requests(messages, json_schema=json_schema, schema_name=schema_name)
        validator = _schema_validator(json_schema) if json_schema is not None else None
        if self._environ is None:
            load_dotenv(self._env_file, override=False, interpolate=False)
        env = os.environ if self._environ is None else self._environ
        failures: list[str] = []
        for request in requests:
            base_url, key_name = PROVIDERS[request.provider]
            key = env.get(key_name, "").strip()
            if not key or key.startswith("replace_with_"):
                failures.append(f"{request.provider}: {key_name} missing from .env")
                continue
            try:
                # No SDK retry loop: at most one request per configured eligible target.
                with self._client_factory(
                    api_key=key, base_url=base_url, timeout=45.0, max_retries=0
                ) as client:
                    response = client.chat.completions.create(**request.parameters)
            except APIStatusError as error:
                status = error.status_code
                if status not in FALLBACK_STATUSES:
                    raise LLMError(
                        f"{request.provider}: HTTP {status}; check credentials, billing or access."
                    ) from None
                failures.append(f"{request.provider}: HTTP {status}")
                continue
            except APIConnectionError:
                failures.append(f"{request.provider}: connection or timeout failure")
                continue
            except Exception:
                raise LLMError(
                    "LLM request failed; check local SDK and provider configuration."
                ) from None
            try:
                choice = response.choices[0]
                if choice.message.refusal or choice.finish_reason == "content_filter":
                    raise LLMError("Provider declined the request; fallback was not attempted.")
                content = choice.message.content
                if not isinstance(content, str) or not content.strip():
                    reasoning = getattr(choice.message, "reasoning", None)
                    content = reasoning if isinstance(reasoning, str) else ""
                if not isinstance(content, str) or not content.strip():
                    failures.append(
                        f"{request.provider}: incomplete or empty response"
                        f" (finish_reason={choice.finish_reason!s})"
                    )
                    continue
                if choice.finish_reason not in {None, "stop"}:
                    failures.append(
                        f"{request.provider}: incomplete or empty response"
                        f" (finish_reason={choice.finish_reason!s})"
                    )
                    continue
                if validator is not None:
                    extracted = _extract_json_text(content)
                    parsed = json.loads(extracted)
                    # Python accepts NaN/Infinity while JSON does not; reject both
                    # those literals and numeric overflow before validating schema.
                    json.dumps(parsed, allow_nan=False)
                    parsed = _unwrap_result(parsed)
                    try:
                        validator.validate(parsed)
                    except Exception:
                        parsed = _fill_required(
                            _coerce_for_schema(parsed, json_schema), json_schema
                        )
                        json.dumps(parsed, allow_nan=False)
                        validator.validate(parsed)
                    self.last_usage = usage_summary(response)
                    return json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
                self.last_usage = usage_summary(response)
                return content.strip()
            except LLMError:
                raise
            except Exception as error:
                detail = str(error).replace("\n", " ").strip()[:180]
                failures.append(
                    f"{request.provider}: invalid response or schema mismatch ({type(error).__name__}: {detail})"
                )
        raise LLMError("No configured model succeeded. " + "; ".join(failures)) from None
