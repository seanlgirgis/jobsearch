#!/usr/bin/env python3
"""
scripts/00_check_applied_before.py

Phase 0: Duplicate Check (semantic + lexical fallback)

Primary path:
- Semantic check using FAISS + sentence-transformers.

Fallback path:
- Lexical check against stored metadata when semantic resources are unavailable
  (network/model/cache/import/runtime issues).

Exit codes:
- 0: duplicate_check=clear
- 1: duplicate_check=flagged
- 2: duplicate_check=blocked
"""

import argparse
import re
import sys
from datetime import datetime, date
from pathlib import Path
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple

# ──────────────────────────────────────────────── Constants ─────
from scripts.utils.vector_ops import get_embedding, load_index_and_metadata

DEFAULT_THRESHOLD = 0.82
DEFAULT_TOP_K    = 5
DEFAULT_MAX_AGE_DAYS = 45


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _extract_apply_date(meta: Dict[str, Any]) -> str:
    """Best-effort extraction of applied date from indexed metadata shape(s)."""
    application = meta.get("application", {}) if isinstance(meta.get("application"), dict) else {}
    candidates = [
        meta.get("apply_date"),
        meta.get("applied_date"),
        application.get("applied_date"),
        application.get("date"),
        application.get("last_status_date"),
    ]
    for candidate in candidates:
        txt = _safe_text(candidate)
        if txt and txt.lower() not in {"n/a", "na", "none", "null", "unknown"}:
            return txt
    return "N/A"


def _parse_date(value: str) -> Optional[date]:
    txt = _safe_text(value)
    if not txt or txt == "N/A":
        return None
    # Common formats: YYYY-MM-DD and ISO timestamps.
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(txt[:10], fmt).date()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(txt.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _days_ago_label(value: str) -> str:
    d = _parse_date(value)
    if d is None:
        return "N/A"
    delta = (date.today() - d).days
    if delta < 0:
        return f"in {-delta}d"
    return f"{delta}d"


def _within_age_window(meta: Dict[str, Any], max_age_days: int) -> bool:
    """True if job is recent enough to be considered a blocking duplicate."""
    if max_age_days <= 0:
        return True
    applied = _extract_apply_date(meta)
    d = _parse_date(applied)
    if d is None:
        # Keep undated rows as candidates (safer default).
        return True
    age_days = (date.today() - d).days
    return age_days <= max_age_days


def load_intake_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)
    text = path.read_text(encoding="utf-8").strip()
    # MIN_TEXT_LEN was removed, so this check is also removed.
    # if len(text) < MIN_TEXT_LEN:
    #     print(f"⚠️ Warning: Input text is short ({len(text)} chars) – results may be unreliable.")
    return text


def check_duplicates_semantic(
    new_text: str,
    index: Any,
    metadata: List[Dict],
    threshold: float,
    top_k: int,
    max_age_days: int,
) -> bool:
    emb = get_embedding(new_text)
    distances, indices = index.search(emb, top_k)

    print(f"\n[INFO] Query against {index.ntotal} past jobs (threshold {threshold:.2f}, showing top {top_k}, age<= {max_age_days}d)")
    print(f"{'Sim':<8} | {'Applied':<12} | {'Age':<7} | {'Company':<20} | {'Role':<30} | {'UUID':<10} | {'Status':<10}")
    print("-" * 112)

    found_duplicate = False
    skipped_old = 0
    for i in range(top_k):
        score = distances[0][i]
        idx = indices[0][i]
        if idx == -1:
            continue

        meta = metadata[idx]
        if not _within_age_window(meta, max_age_days):
            skipped_old += 1
            continue

        is_dupe = score >= threshold
        flag = "DUPE" if is_dupe else ""

        if is_dupe:
            found_duplicate = True

        company = (meta.get("company", "Unknown"))[:18]
        role    = (meta.get("role",    "Unknown"))[:28]
        uuid    = meta.get("uuid",     "????")[:8]
        date_applied = _extract_apply_date(meta)
        age_days = _days_ago_label(date_applied)
        status  = meta.get("status",   "Unknown")[:8]

        print(f"{score:.4f} | {date_applied[:12]:<12} | {age_days:<7} | {company:<20} | {role:<30} | {uuid} | {status} {flag}")

    print("-" * 112)
    if skipped_old:
        print(f"[INFO] Skipped {skipped_old} old match(es) older than {max_age_days} days.")

    if found_duplicate:
        print(f"\n[FLAGGED] Semantic duplicate likely (>= {threshold:.2f})")
        return True
    else:
        print("\n[CLEAR] Semantic check found no strong duplicates.")
        return False


def _extract_field(text: str, field_name: str) -> str:
    match = re.search(rf"(?im)^{re.escape(field_name)}\s*:\s*(.+)$", text)
    return (match.group(1).strip() if match else "")


def extract_intake_fingerprint(text: str) -> Dict[str, str]:
    title = _extract_field(text, "Title")
    company = _extract_field(text, "Company")
    location = _extract_field(text, "Location")
    return {
        "title": title.lower(),
        "company": company.lower(),
        "location": location.lower(),
    }


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _sim(a: str, b: str) -> float:
    a_n = _norm(a)
    b_n = _norm(b)
    if not a_n or not b_n:
        return 0.0
    return SequenceMatcher(None, a_n, b_n).ratio()


def check_duplicates_lexical(new_text: str, metadata: List[Dict], top_k: int, max_age_days: int) -> Tuple[bool, str]:
    if not metadata:
        return False, "no metadata available for lexical fallback"

    fp = extract_intake_fingerprint(new_text)
    title_fp = fp["title"]
    company_fp = fp["company"]
    location_fp = fp["location"]

    if not (title_fp or company_fp):
        return False, "intake missing Title/Company fields for lexical comparison"

    scored: List[Tuple[float, Dict[str, Any]]] = []
    skipped_old = 0
    for meta in metadata:
        if not _within_age_window(meta, max_age_days):
            skipped_old += 1
            continue
        company = str(meta.get("company", ""))
        role = str(meta.get("role", ""))
        m_loc = str(meta.get("location", ""))

        company_sim = _sim(company_fp, company)
        role_sim = _sim(title_fp, role)
        loc_sim = _sim(location_fp, m_loc)

        score = (0.50 * role_sim) + (0.40 * company_sim) + (0.10 * loc_sim)
        scored.append((score, meta))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:max(1, top_k)]

    print(f"\n[INFO] Lexical fallback duplicate check (company/title/location similarity, age<= {max_age_days}d)")
    print(f"{'Score':<8} | {'Applied':<12} | {'Age':<7} | {'Company':<20} | {'Role':<30} | {'UUID':<10} | {'Status':<10}")
    print("-" * 112)
    if skipped_old:
        print(f"[INFO] Skipped {skipped_old} old candidate(s) older than {max_age_days} days.")

    flagged = False
    for score, meta in top:
        company = str(meta.get("company", "Unknown"))[:18]
        role = str(meta.get("role", "Unknown"))[:28]
        uuid = str(meta.get("uuid", "????"))[:8]
        status = str(meta.get("status", "Unknown"))[:8]
        date_applied = _extract_apply_date(meta)
        age_days = _days_ago_label(date_applied)
        is_dupe = score >= 0.78
        if is_dupe:
            flagged = True
        flag = "DUPE" if is_dupe else ""
        print(f"{score:.4f} | {date_applied[:12]:<12} | {age_days:<7} | {company:<20} | {role:<30} | {uuid} | {status:<10} {flag}")

    print("-" * 112)
    if flagged:
        return True, "lexical fallback flagged likely duplicate"
    return False, "lexical fallback found no likely duplicate"


def main():
    parser = argparse.ArgumentParser(description="Semantic duplicate check before pipeline")
    parser.add_argument("intake_file", help="Path to new job markdown file")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Similarity threshold (default: {DEFAULT_THRESHOLD})")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K,
                        help=f"Number of top matches to show (default: {DEFAULT_TOP_K})")
    parser.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS,
                        help=f"Ignore duplicate matches older than this many days (default: {DEFAULT_MAX_AGE_DAYS})")

    args = parser.parse_args()

    index, metadata = load_index_and_metadata()
    text = load_intake_text(args.intake_file)
    # 1) Try semantic check first when index is available.
    if index is not None:
        try:
            is_duplicate = check_duplicates_semantic(
                text,
                index,
                metadata,
                args.threshold,
                args.top_k,
                args.max_age_days,
            )
            if is_duplicate:
                print("duplicate_check: flagged (semantic)")
                sys.exit(1)
            print("duplicate_check: clear (semantic)")
            sys.exit(0)
        except Exception as e:
            print(f"[WARN] Semantic duplicate check unavailable: {e}")

    # 2) Fall back to lexical check if metadata exists.
    is_duplicate_lex, reason = check_duplicates_lexical(text, metadata, args.top_k, args.max_age_days)
    if is_duplicate_lex:
        print(f"duplicate_check: flagged (lexical) | reason: {reason}")
        sys.exit(1)
    if metadata:
        print(f"duplicate_check: clear (lexical) | reason: {reason}")
        sys.exit(0)

    # 3) Fully blocked (no semantic and no lexical inputs).
    print(f"duplicate_check: blocked | reason: {reason}")
    sys.exit(2)


if __name__ == "__main__":
    main()

