#!/usr/bin/env python3
"""
scripts/tailor_job_data.py

Phase 3 in POC pipeline:
After scoring & accepting a job → tailor / structure / enrich the job data
for better RAG retrieval, resume/cover matching, keyword optimization.

Loads from existing job folder (created by score_job.py)
Writes tailored artifacts into the same folder.

Usage:
    python scripts/tailor_job_data.py --uuid <uuid> [--version v1] [--raw-file path/to/raw_job.md]
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
    r"(?i)(python|java|javascript|typescript|go|rust|c\+\+|sql|aws|gcp|azure|docker|kubernetes|terraform|react|node\.js|django|flask|spring|kubernetes|ansible|jenkins|git|linux|windows|mysql|postgresql|mongodb|redis|elasticsearch|kafka|spark|hadoop|tableau|powerbi|excel|agile|scrum|devops|ci/cd|microservices|api|rest|graphql|machine learning|ai|data science|big data|cloud|security|networking|database|frontend|backend|fullstack|mobile|ios|android|flutter|react native|swift|kotlin|php|ruby|scala|perl|bash|shell|html|css|bootstrap|angular|vue|express|laravel|symfony|asp\.net|sql server|oracle|sap|salesforce|dynamics|erp|crm|blockchain|ethereum|bitcoin|nft|web3|vr|ar|unity|unreal|photoshop|illustrator|figma|sketch|invision|seo|sem|google analytics|adsense|adwords|content marketing|social media|email marketing|copywriting|ux|ui|product management|project management|leadership|team building|communication|problem solving|analytical|critical thinking)"
]  # Expanded list; add more as needed

def clean_text(text: str) -> str:
    """Basic cleaning: remove extra whitespace, HTML tags, etc."""
    text = re.sub(r'<[^>]+>', '', text)  # Strip HTML
    text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
    return text.strip()

def extract_section(text: str, section_key: str) -> str:
    """Extract content after a section marker using regex."""
    markers = SECTION_MARKERS.get(section_key, [])
    if not markers:
        return ""
    pattern = '|'.join(markers)
    match = re.search(pattern, text)
    if not match:
        return ""
    start = match.end()
    # Naive: take until next section or end (improve with better parsing)
    next_match = re.search(pattern, text[start:])
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()

def extract_skills(text: str) -> list[str]:
    """Find unique skills using patterns."""
    skills = set()
    for pattern in SKILL_PATTERNS:
        matches = re.findall(pattern, text)
        skills.update(m.lower() for m in matches)  # Lowercase for dedup
    return sorted(skills)

def tailor_job(uuid: str, version: str = "v1", raw_file: Optional[str] = None) -> None:
    job_dir = JOB_ROOT / uuid
    if not job_dir.is_dir():
        raise ValueError(f"Job folder not found: {job_dir}")

    # Raw path: use --raw-file if provided, else default
    if raw_file:
        raw_path = Path(raw_file)
    else:
        raw_path = job_dir / "raw" / "job_description.md"  # Default location

    if not raw_path.is_file():
        raise FileNotFoundError(f"Raw job file not found: {raw_path}")

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned = clean_text(raw_text)

    # Extract structured data
    tailored_data: Dict[str, Any] = {
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
    # meta_path = job_dir / "metadata.yaml"
    # if meta_path.is_file():
    #     with open(meta_path, "r") as f:
    #         metadata = yaml.safe_load(f)
    #     metadata["last_tailored"] = version
    #     with open(meta_path, "w") as f:
    #         yaml.safe_dump(metadata, f)


def main():
    parser = argparse.ArgumentParser(description="Tailor job data for accepted jobs")
    parser.add_argument("--uuid", required=True, help="Job UUID (from score_job.py)")
    parser.add_argument("--version", default="v1", help="Tailored version tag (v1, v2-llm, etc.)")
    parser.add_argument("--raw-file", default=None, help="Path to raw job description file (overrides default location)")
    args = parser.parse_args()

    try:
        tailor_job(args.uuid, args.version, args.raw_file)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()