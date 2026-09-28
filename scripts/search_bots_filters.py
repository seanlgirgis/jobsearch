"""Recency + denylist. Used before a paid eval."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

EXCLUSIONS = Path("config/search_bots_exclusions.json")
CONFIG = Path("config/search_bots.json")
INDEX = Path("data/search_bots/cache/index.json")


def load_exclusions(root: Path) -> dict[str, Any]:
    path = root / EXCLUSIONS
    if not path.is_file():
        return {"companies": [], "title_contains": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def is_excluded(
    *,
    company: str | None,
    title: str | None,
    root: Path,
) -> str | None:
    """Return the matching rule, or None if the job may proceed."""
    rules = load_exclusions(root)
    company_n = _norm(company)
    title_n = (title or "").lower()
    for name in rules.get("companies") or []:
        if _norm(name) and _norm(name) in company_n:
            return f"company:{name}"
        if _norm(name) and _norm(name) in _norm(title):
            return f"company_in_title:{name}"
    for fragment in rules.get("title_contains") or []:
        if fragment and fragment.lower() in title_n:
            return f"title:{fragment}"
    return None


def has_prior_dna(root: Path) -> bool:
    path = root / INDEX
    if not path.is_file():
        return False
    index = json.loads(path.read_text(encoding="utf-8"))
    return bool(index.get("by_alias") or index.get("by_dna"))


PART_TIME_HINTS = (
    "part time",
    "part-time",
    "parttime",
    "fractional",
    "flexible hours",
    "choose your own hours",
)


def is_part_time_or_flexible(
    *,
    title: str | None,
    salary_text: str | None,
    query: str | None,
    job_text: str | None = None,
) -> bool:
    # Search intent is not evidence about a listing. Only read posting fields and
    # explicit schedule lines; benefits prose often promises flexible work to FT staff.
    schedule = [
        line.strip()
        for line in (job_text or "").splitlines()
        if re.match(r"(?i)^\s*(?:schedule|employment type|job type|hours)\s*:", line)
        or re.fullmatch(r"(?i)\s*(?:full[ -]?time|part[ -]?time|fractional)\s*", line)
    ]
    blob = " ".join(x or "" for x in (title, salary_text, *schedule)).lower()
    if re.search(r"\bfull[ -]?time\b", blob):
        return False
    return any(hint in blob for hint in PART_TIME_HINTS)


def parse_pay_annual_max_usd(text: str | None) -> int | None:
    """Annualize an explicit USD pay range. Ambiguous units stay unknown."""
    if not text:
        return None
    blob = text.replace(",", "").lower()
    if re.search(
        r"\b(?:cad|aud|nzd|eur|gbp|inr)\b|[\u00a3\u20ac\u20b9]|\b(?:ca|au|nz|c|a)\$",
        blob,
    ):
        return None
    number = r"(\d+(?:\.\d+)?)\s*(k\b)?"
    match = re.search(
        rf"(?:\$|\busd\s*)\s*{number}(?:\s*(?:-|\u2013|\u2014|to)\s*(?:\$|usd)?\s*{number})?",
        blob,
    )
    if not match:
        return None
    lo, lo_k, hi, hi_k = match.groups()
    # A trailing K applies to both endpoints of a compact 120-160k range.
    amounts = [float(lo) * (1000 if lo_k or (hi_k and float(lo) < 1000) else 1)]
    if hi:
        amounts.append(float(hi) * (1000 if hi_k or (lo_k and float(hi) < 1000) else 1))
    # Ignore unrelated counts, bonuses, and benefits elsewhere in the snippet.
    suffix = blob[match.end() :].lstrip()
    period = re.match(
        r"(?:an?\s+|per\s+|/\s*)?(hours?|hrs?|hr|year|yr|annum|months?|weeks?|days?)\b",
        suffix,
    )
    if period:
        unit = period.group(1)
        if unit.startswith(("hour", "hr")):
            multiplier = 2080
        elif unit.startswith("month"):
            multiplier = 12
        elif unit.startswith("week"):
            multiplier = 52
        elif unit.startswith("day"):
            multiplier = 260
        else:
            multiplier = 1
    elif lo_k or hi_k or re.search(r"\b(?:annual|yearly)\b", blob):
        multiplier = 1
    else:
        return None
    return int(max(amounts) * multiplier)


def pay_skip_reason(
    *,
    title: str | None,
    salary_text: str | None,
    query: str | None,
    root: Path,
    job_text: str | None = None,
) -> str | None:
    cfg = json.loads((root / CONFIG).read_text(encoding="utf-8"))
    rules = cfg.get("pay_rules") or {}
    if is_part_time_or_flexible(
        title=title,
        salary_text=salary_text,
        query=query,
        job_text=job_text,
    ):
        return None
    posted = parse_pay_annual_max_usd(salary_text)
    if posted is None:
        if rules.get("skip_if_salary_unknown"):
            return "salary_unknown"
        return None
    floor = rules.get("full_time_skip_below_usd")
    if isinstance(floor, int) and posted < floor:
        return f"full_time_pay_{posted}_below_{floor}"
    return None


def indeed_fromage_days(root: Path) -> int:
    cfg = json.loads((root / CONFIG).read_text(encoding="utf-8"))
    recency = cfg.get("recency") or {}
    if has_prior_dna(root):
        return int(recency.get("later_run_days") or 1)
    return int(recency.get("first_run_days") or 1)
