"""Duplicate check helpers for the local gate step."""

import contextlib
from difflib import SequenceMatcher
import io
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


LEXICAL_THRESHOLD = 0.78


def _extract_field(text: str, field_name: str) -> str:
    match = re.search(rf"(?im)^{re.escape(field_name)}\s*:\s*(.+)$", text)
    return (match.group(1).strip() if match else "")


def _extract_intake_fingerprint(text: str) -> Dict[str, str]:
    return {
        "title": _extract_field(text, "Title").lower(),
        "company": _extract_field(text, "Company").lower(),
        "location": _extract_field(text, "Location").lower(),
    }


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _sim(a: str, b: str) -> float:
    a_n = _norm(a)
    b_n = _norm(b)
    if not a_n or not b_n:
        return 0.0
    return SequenceMatcher(None, a_n, b_n).ratio()


def _best_match_id(meta: Dict[str, Any]) -> Optional[str]:
    return meta.get("job_id") or meta.get("uuid")


def _semantic_check(
    normalized_text: str,
    threshold: float,
    top_k: int,
) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]], str]:
    """
    Returns:
    - result dict when semantic could run
    - metadata (for lexical fallback)
    - failure reason if semantic could not run
    """
    try:
        from scripts.utils.vector_ops import get_embedding, load_index_and_metadata
    except Exception as exc:
        return None, [], f"semantic imports unavailable: {exc}"

    index, metadata = load_index_and_metadata()
    if index is None:
        return None, metadata, "semantic index unavailable"

    try:
        # Keep local-gate CLI output clean even when model initialization is verbose.
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            emb = get_embedding(normalized_text)
        distances, indices = index.search(emb, top_k)
    except Exception as exc:
        return None, metadata, f"semantic query failed: {exc}"

    best_score = 0.0
    best_meta: Optional[Dict[str, Any]] = None

    for i in range(top_k):
        idx = int(indices[0][i])
        if idx == -1 or idx >= len(metadata):
            continue
        score = float(distances[0][i])
        if best_meta is None or score > best_score:
            best_score = score
            best_meta = metadata[idx]

    duplicate_found = best_score >= threshold
    matched_job_id = _best_match_id(best_meta) if best_meta else None

    reason = (
        "strong semantic match above threshold"
        if duplicate_found
        else "no strong duplicate found"
    )

    return {
        "mode": "semantic",
        "duplicate_found": duplicate_found,
        "score": best_score,
        "matched_job_id": matched_job_id,
        "reason": reason,
    }, metadata, ""


def _lexical_check(
    normalized_text: str,
    metadata: List[Dict[str, Any]],
    top_k: int,
) -> Optional[Dict[str, Any]]:
    if not metadata:
        return None

    fp = _extract_intake_fingerprint(normalized_text)
    if not (fp["title"] or fp["company"]):
        return None

    scored: List[Tuple[float, Dict[str, Any]]] = []
    for meta in metadata:
        company = str(meta.get("company", ""))
        role = str(meta.get("role", ""))
        location = str(meta.get("location", ""))

        company_sim = _sim(fp["company"], company)
        role_sim = _sim(fp["title"], role)
        loc_sim = _sim(fp["location"], location)
        score = (0.50 * role_sim) + (0.40 * company_sim) + (0.10 * loc_sim)
        scored.append((score, meta))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_matches = scored[: max(1, top_k)]
    best_score, best_meta = top_matches[0]

    duplicate_found = best_score >= LEXICAL_THRESHOLD
    matched_job_id = _best_match_id(best_meta)
    reason = (
        "strong lexical match above threshold"
        if duplicate_found
        else "no strong duplicate found"
    )

    return {
        "mode": "lexical",
        "duplicate_found": duplicate_found,
        "score": float(best_score),
        "matched_job_id": matched_job_id,
        "reason": reason,
    }


def run_duplicate_check(
    normalized_text: str,
    threshold: float = 0.82,
    top_k: int = 5,
) -> Dict[str, Any]:
    semantic_result, metadata, semantic_reason = _semantic_check(
        normalized_text=normalized_text,
        threshold=threshold,
        top_k=top_k,
    )
    if semantic_result is not None:
        return semantic_result

    lexical_result = _lexical_check(
        normalized_text=normalized_text,
        metadata=metadata,
        top_k=top_k,
    )
    if lexical_result is not None:
        return lexical_result

    return {
        "mode": "blocked",
        "duplicate_found": False,
        "score": 0.0,
        "matched_job_id": None,
        "reason": f"duplicate check unavailable: {semantic_reason}",
    }
