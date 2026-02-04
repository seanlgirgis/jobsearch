#!/usr/bin/env python3
"""
scripts/tailor_job_data.py

Phase 3 in POC pipeline:
After scoring & accepting a job → tailor / structure / enrich the job data
for better RAG retrieval, resume/cover matching, keyword optimization.

Loads from existing job folder (created by score_job.py)
Writes tailored artifacts into the same folder.

Usage:
    python scripts/tailor_job_data.py --uuid 96b16121-8608-405d-9553-af86fdbf939c
    # Optional: --version v2  (to create tailored_data_v2.yaml instead of overwriting)
"""

import argparse
import yaml
from pathlib import Path
import re
from typing import Dict, Any, Optional

# Reuse existing loaders/clients when possible
# (assuming src/ structure from decisions.md)
try:
    from src.loaders.master_profile import MasterProfileLoader  # for future LLM context if needed
    from src.ai.grok_client import GrokClient                   # for future LLM tailoring
except ImportError:
    print("Warning: src modules not found — running without LLM for now")

JOB_ROOT = Path("data/jobs")

# Naive section extractors (same as before — improve with LLM later)
SECTION_MARKERS = {
    "responsibilities": [r"(?i)(responsibilit(y|ies)|what you'll do|key duties|you will|day[- ]?to[- ]?day)"],
    "requirements": [r"(?i)(require(ments|d)|qualifications|must have|minimum)"],
    "preferred": [r"(?i)(preferred|nice to have|bonus|desired|plus)"],
    "benefits": [r"(?i)(benefit|perks|compensation|remote|hybrid)"],
}

SKILL_PATTERNS = [
    r"(?i)(python|java|javascript|typescript|go|rust|c\+\+|sql|aws|gcp|azure|docker|kubernetes|terraform|react|node\.js|django|flask|spring|kafka|spark|airflow|etl|data pipeline|machine learning|llm|generative ai)",
    # Expand based on your master skills / real jobs
]

def extract_section(text: str, key: str) -> Optional[str]:
    """Naive line-based section collector — replace with LLM chunking later."""
    lines = text.splitlines()
    in_section = False
    collected = []
    for line in lines:
        stripped = line.strip()
        if any(re.search(p, stripped) for p in SECTION_MARKERS.get(key, [])):
            in_section = True
            continue
        if in_section and stripped and not any(re.search(p, stripped) for pats in SECTION_MARKERS.values() for p in pats):
            collected.append(stripped)
        elif in_section and not stripped:
            break  # blank line ends section (heuristic)
    return "\n".join(collected).strip() if collected else None


def extract_skills(text: str) -> list[str]:
    found = set()
    for pat in SKILL_PATTERNS:
        found.update(m.group(0).lower() for m in re.finditer(pat, text))
    return sorted(found)


def clean_text(raw: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", raw.strip())
    text = re.sub(r"\s{2,}", " ", text)
    return text


def tailor_job(uuid_str: str, version: str = "v1"):
    job_dir = JOB_ROOT / uuid_str
    if not job_dir.is_dir():
        raise FileNotFoundError(f"Job folder not found: {job_dir}")

    raw_path = job_dir / "raw_intake.md"
    meta_path = job_dir / "metadata.yaml"

    if not raw_path.is_file() or not meta_path.is_file():
        raise FileNotFoundError(f"Missing raw_intake.md or metadata.yaml in {job_dir}")

    with open(raw_path, encoding="utf-8") as f:
        raw_text = f.read()

    with open(meta_path, encoding="utf-8") as f:
        metadata = yaml.safe_load(f) or {}

    cleaned = clean_text(raw_text)

    tailored_data: Dict[str, Any] = {
        "uuid": uuid_str,
        "version": version,
        "timestamp": "",  # can add datetime.now().isoformat()
        "clean_description": cleaned,
        "title": metadata.get("title", ""),
        "company": metadata.get("company", ""),
        "location": metadata.get("location", ""),
        "url": metadata.get("url", ""),
        "extracted_skills": extract_skills(cleaned),
        "sections": {
            "responsibilities": extract_section(cleaned, "responsibilities"),
            "requirements": extract_section(cleaned, "requirements"),
            "preferred": extract_section(cleaned, "preferred"),
            "benefits": extract_section(cleaned, "benefits"),
        },
        # Future LLM fields
        # "llm_summary": None,
        # "rephrased_bullets": [],
        # "keyword_boost_for_resume": [],
    }

    # Future: call GrokClient here to do real tailoring / rephrasing / skill prioritization

    tailored_dir = job_dir / "tailored"
    tailored_dir.mkdir(exist_ok=True)

    out_file = tailored_dir / f"tailored_data_{version}.yaml"
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(tailored_data, f, sort_keys=False, allow_unicode=True)

    print(f"Tailored data saved: {out_file}")
    print(f"Extracted skills ({len(tailored_data['extracted_skills'])}): {', '.join(tailored_data['extracted_skills'][:10])} ...")

    # Optional: update metadata.yaml with last_tailored_version or status
    # metadata["last_tailored"] = version
    # with open(meta_path, "w") as f:
    #     yaml.safe_dump(metadata, f)


def main():
    parser = argparse.ArgumentParser(description="Tailor job data for accepted jobs")
    parser.add_argument("--uuid", required=True, help="Job UUID (from score_job.py)")
    parser.add_argument("--version", default="v1", help="Tailored version tag (v1, v2-llm, etc.)")
    args = parser.parse_args()

    try:
        tailor_job(args.uuid, args.version)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()