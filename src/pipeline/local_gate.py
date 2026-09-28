"""Read-only local duplicate/eligibility checks. No providers or remote embeddings."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import yaml


def normalize_text(text: str) -> str:
    """Normalize intake whitespace without importing the legacy pipeline package."""
    return " ".join(text.strip().split())


def paid_job_text(text: str) -> str:
    """Collapse Unicode/whitespace for paid-cache identity without casefolding.

    Folder identity still uses job_hash() (casefold). Paid request identity must
    ignore whitespace-only edits without merging postings that differ only by case.
    """
    return normalize_text(unicodedata.normalize("NFKC", text.lstrip("\ufeff")))


GATE_VERSION = "local-v1"


def normalized(text):
    return normalize_text(unicodedata.normalize("NFKC", text.lstrip("\ufeff"))).casefold()


def job_hash(text):
    return hashlib.sha256(normalized(text).encode("utf-8")).hexdigest()


def legacy_exact_matches(root, text, own_folder):
    """Compare metadata hashes AND normalized raw text in both historical stores."""
    matches, errors = [], []
    candidate = normalized(text)
    for collection in ("jobs", "applied_jobs"):
        for folder in sorted((root / "data" / collection).glob("*")):
            if not folder.is_dir() or folder == own_folder:
                continue
            try:
                meta_path = folder / "metadata.yaml"
                meta = (
                    yaml.safe_load(meta_path.read_text(encoding="utf-8-sig"))
                    if meta_path.exists()
                    else {}
                )
                meta = meta or {}
                if not isinstance(meta, dict):
                    raise ValueError("Invalid metadata")
                if meta.get("index_exclude"):
                    continue
                paths = [
                    folder / "raw" / "job_description.md",
                    folder / "raw" / "raw_intake.md",
                    *sorted(folder.glob("*.md")),
                ]
                exact = meta.get("job_hash") == job_hash(text)
                near = False
                for path in paths:
                    if path.is_file():
                        prior = normalized(path.read_text(encoding="utf-8-sig"))
                        exact |= prior == candidate
                        # Supplements the existing FAISS index for newly created runner records.
                        if folder.name.startswith("runner_") and not exact:
                            near |= (
                                SequenceMatcher(None, candidate, prior, autojunk=False).ratio()
                                >= 0.94
                            )
                if exact or near:
                    matches.append(
                        {
                            "folder": folder.relative_to(root).as_posix(),
                            "kind": "exact" if exact else "runner_lexical",
                        }
                    )
            except (OSError, ValueError, yaml.YAMLError):
                errors.append(folder.relative_to(root).as_posix())
    return matches, errors


def semantic_worker(root, text, own_name):
    """Reuse the existing vector implementation, forced offline in an isolated process."""
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    from scripts.utils import vector_ops

    vector_ops.INDEX_PATH = root / "data/job_index/faiss_job_descriptions.index"
    vector_ops.METADATA_PATH = root / "data/job_index/jobs_metadata.yaml"
    vector_ops.LOCAL_ONLY = True
    local_model = root / "models/sentence-transformers/all-MiniLM-L6-v2"
    vector_ops.EMBEDDING_MODEL_NAME = (
        str(local_model) if local_model.exists() else "all-MiniLM-L6-v2"
    )
    vector_ops._MODEL = None
    index, metadata = vector_ops.load_index_and_metadata()
    if index is None or not metadata or not vector_ops.verify_integrity(index, metadata):
        return {
            "status": "BLOCKED",
            "reason": "FAISS index/metadata unavailable or inconsistent",
            "matches": [],
        }
    import faiss

    if index.metric_type != faiss.METRIC_INNER_PRODUCT:
        return {"status": "BLOCKED", "reason": "FAISS metric requires review", "matches": []}
    embedding = vector_ops.get_embedding(text)
    scores, indices = index.search(embedding, index.ntotal)
    matches = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or float(score) < 0.82:
            continue
        record = metadata[int(idx)]
        identifier = str(record.get("uuid", ""))
        if identifier == own_name:
            continue
        matches.append({"job": identifier, "similarity": round(float(score), 6)})
    return {
        "status": "DUPLICATE" if matches else "CLEAR",
        "matches": matches,
        "reason": "Existing FAISS cosine check (0.82 threshold; no age expiry)",
    }


def semantic_check(root, text, own_name):
    code = (
        "import sys,json; from pathlib import Path; "
        "from src.pipeline.local_gate import semantic_worker; "
        "a=json.load(sys.stdin); print('RUNNER_RESULT='+json.dumps(semantic_worker(Path(a['root']),a['text'],a['own'])))"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            input=json.dumps({"root": str(root), "text": text, "own": own_name}),
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=55,
        )
        lines = [line for line in result.stdout.splitlines() if line.startswith("RUNNER_RESULT=")]
        if result.returncode == 0 and len(lines) == 1:
            return json.loads(lines[0].split("=", 1)[1])
    except (OSError, ValueError, subprocess.TimeoutExpired):
        pass
    return {
        "status": "BLOCKED",
        "reason": "Offline FAISS check failed or timed out; no lexical-only clearance",
        "matches": [],
    }


def local_gate(root: Path, text: str, folder: Path, semantic=semantic_check):
    exact, errors = legacy_exact_matches(root, text, folder)
    if (folder / "metadata.yaml").is_file():
        meta = yaml.safe_load((folder / "metadata.yaml").read_text(encoding="utf-8")) or {}
        if meta.get("application", {}).get("applied"):
            exact.append({"folder": folder.relative_to(root).as_posix(), "kind": "already_applied"})
    eligibility = []
    if len(normalized(text)) < 80:
        eligibility.append("Intake too short; provide the complete description")
    if re.search(
        r"(?i)\b(?:no longer accepting applications|this job is closed|position has been filled)\b",
        text,
    ):
        eligibility.append("Posting explicitly says applications are closed")
    semantic_result = (
        {"status": "NOT_NEEDED", "matches": [], "reason": "Exact/lexical duplicate already blocks"}
        if exact
        else semantic(root, text, folder.name)
    )
    blocked = bool(errors) or semantic_result["status"] == "BLOCKED"
    duplicate = bool(exact) or semantic_result["status"] == "DUPLICATE"
    decision = "DUPLICATE" if duplicate else "BLOCKED" if blocked or eligibility else "CLEAR"
    return {
        "version": GATE_VERSION,
        "job_hash": job_hash(text),
        "tier0_decision": decision,
        "exact_matches": exact,
        "semantic": semantic_result,
        "read_errors": errors,
        "eligibility_blocks": eligibility,
        "duplicate_or_check_blocked": duplicate or blocked,
        "paid_calls": 0,
    }
