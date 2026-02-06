#!/usr/bin/env python3
"""
scripts/04_generate_resume_intermediate.py

Phase 4 in POC pipeline:
After job is ACCEPTED and tailored → generate a tailored resume in structured JSON format.
Uses Grok to rewrite bullets/summary/projects while strictly binding to master career data.
Filters out experiences with "exclude_from_resume": true.

Improved version:
- More reliable JSON extraction
- Safer prompt (no conflicting rules)
- Company name/website guidance
- Overwrite protection
- Better error handling

Usage:
    python scripts/04_generate_resume_intermediate.py --uuid 402a89d6 --version v1-postscript [--model grok-3]
"""

import argparse
import json
import yaml
import re
import sys
from pathlib import Path
from typing import Dict, Any

try:
    from src.ai.grok_client import GrokClient
except ImportError:
    print("Warning: src.ai.grok_client not found — mock mode enabled.")
    GrokClient = None

JOB_ROOT = Path("data/jobs")
MASTER_ROOT = Path("data/master")

# Improved prompt — clearer rules, no contradictions
RESUME_PROMPT_TEMPLATE = """
You are a resume optimizer that NEVER invents facts, NEVER removes entries, NEVER changes dates, titles, companies, or degrees.

MANDATORY RULES — violation = invalid output:
1. Preserve EVERY experience entry and EVERY project from the master data exactly as provided.
   Do NOT omit, delete, or combine any entries.
2. For each experience: keep original company, title, dates. Rewrite up to 4–6 bullets per role.
   Prioritize relevance to this job but retain important non-matching bullets.
3. Summary: 4–6 sentences max, professional tone. Naturally weave in 5–8 key job keywords/responsibilities.
   If relevant, mention interest in contributing to {company_name}'s mission/platform.
4. Skills: Include ALL from master skills (deduplicated). Sort with job-relevant ones first
   (must_have_skills, nice_to_have_skills, extracted_skills from job data at the top).
5. Projects: Keep ALL. Shorten descriptions to 2–4 sentences max if needed for length.
6. Output ONLY valid JSON — nothing before {{ or after }}. No markdown, no explanations, no fences.

Master career data (already filtered — use EXACTLY):
{career_json}

Master skills (use all, sort by job relevance):
{skills_json}

This job (tailored data — source of keywords, responsibilities, must-haves):
{job_yaml}

Generate the tailored resume JSON now.
Output ONLY the complete JSON object.
"""

def resolve_job_folder(uuid_str: str) -> Path:
    uuid_str = uuid_str.strip()
    job_dir = JOB_ROOT / uuid_str

    if job_dir.is_dir():
        return job_dir

    candidates = list(JOB_ROOT.glob(f"*_{uuid_str}*"))
    if not candidates:
        short = uuid_str[:8]
        candidates = list(JOB_ROOT.glob(f"*_{short}*"))

    if len(candidates) == 1:
        print(f"Resolved UUID/prefix → using folder: {candidates[0].name}")
        return candidates[0]
    elif len(candidates) > 1:
        print("Ambiguous UUID — multiple matches:")
        for c in candidates:
            print(f"  - {c.name}")
        raise ValueError(f"Ambiguous UUID: {uuid_str}")
    else:
        raise ValueError(f"Job folder not found for '{uuid_str}'")


def load_master() -> tuple[Dict, Dict]:
    career_path = MASTER_ROOT / "master_career_data.json"
    skills_path = MASTER_ROOT / "skills.yaml"

    if not career_path.is_file() or not skills_path.is_file():
        raise FileNotFoundError(f"Master files missing at {MASTER_ROOT}. Run profile_export.py first.")

    with open(career_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    # Apply exclude filter
    if "experiences" in master:
        orig_len = len(master["experiences"])
        master["experiences"] = [
            exp for exp in master["experiences"]
            if not exp.get("exclude_from_resume", False)
        ]
        if len(master["experiences"]) < orig_len:
            print(f"Excluded {orig_len - len(master['experiences'])} experience entries (exclude_from_resume)")

    with open(skills_path, "r", encoding="utf-8") as f:
        skills = yaml.safe_load(f) or {}

    return master, skills


def load_latest_tailored_job(job_dir: Path) -> Dict[str, Any]:
    tailored_dir = job_dir / "tailored"
    if not tailored_dir.is_dir():
        raise FileNotFoundError(f"No tailored/ folder found: {tailored_dir}")

    files = sorted(tailored_dir.glob("tailored_data_*.yaml"), reverse=True)
    if not files:
        raise FileNotFoundError(f"No tailored_data_*.yaml files in {tailored_dir}")

    latest = files[0]
    print(f"Using latest tailored file: {latest.name}")
    with open(latest, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_json_from_response(response: str) -> Dict:
    """Robust JSON extraction with multiple strategies"""
    strategies = [
        response.strip(),                                   # raw
        re.sub(r'^.*?(\{.*\}).*$', r'\1', response, flags=re.DOTALL),  # greedy match
        re.sub(r'```(?:json)?\s*(.*?)\s*```', r'\1', response, flags=re.DOTALL | re.IGNORECASE),
    ]

    for candidate in strategies:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    print("\nJSON extraction failed. First 2000 chars of response:")
    print(response[:2000])
    if len(response) > 2000:
        print("...")
    raise ValueError("Could not extract valid JSON from LLM response")


def call_llm(prompt: str, model: str = "grok-3") -> Dict:
    if GrokClient is None:
        print("Mock mode: returning dummy resume JSON")
        return {
            "personal": {"full_name": "Sean Luka Girgis", "email": "seanlgirgis@gmail.com"},
            "summary": "Experienced data engineer specializing in scalable pipelines.",
            "experience": [{"company": "Example", "title": "Data Engineer", "bullets": ["Built ETL"]}],
            "education": [{"degree": "BS Computer Science"}],
            "skills": ["python", "sql"],
            "projects": [{"name": "Data Platform", "description": "Modern data stack"}]
        }

    grok = GrokClient(model=model)
    print(f"Calling Grok ({model}) for resume tailoring...")
    response = grok.chat([{"role": "user", "content": prompt}], max_tokens=8192, temperature=0.0)

    return extract_json_from_response(response)


def main():
    parser = argparse.ArgumentParser(description="Phase 4: Generate tailored resume intermediate JSON")
    parser.add_argument("--uuid", required=True, help="Job UUID or short prefix")
    parser.add_argument("--version", default="v1", help="Output version tag (e.g. v1-postscript)")
    parser.add_argument("--model", default="grok-3", help="Grok model to use")
    args = parser.parse_args()

    job_folder = resolve_job_folder(args.uuid)
    print(f"Processing job: {job_folder.name}")

    generated_dir = job_folder / "generated"
    generated_dir.mkdir(exist_ok=True)

    out_path = generated_dir / f"resume_intermediate_{args.version}.json"
    if out_path.exists():
        print(f"\nWarning: {out_path} already exists.")
        if input("Overwrite? [y/N] ").strip().lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    try:
        master_career, master_skills = load_master()
        job_data = load_latest_tailored_job(job_folder)
    except Exception as e:
        print(f"Error loading input data: {e}")
        sys.exit(1)

    company_name = job_data.get("company_name", "the company")

    prompt = RESUME_PROMPT_TEMPLATE.format(
        career_json=json.dumps(master_career, indent=2),
        skills_json=json.dumps(master_skills, indent=2),
        job_yaml=yaml.dump(job_data, sort_keys=False, allow_unicode=True),
        company_name=company_name
    )

    print("Generating tailored resume intermediate JSON...")
    try:
        tailored_resume = call_llm(prompt, args.model)
    except Exception as e:
        print(f"LLM / parsing failed: {e}")
        sys.exit(1)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tailored_resume, f, indent=2, ensure_ascii=False)

    print(f"\nSuccess! Intermediate resume saved → {out_path}")

    print("\nNext steps:")
    print("1. Review and manually tweak the JSON if needed")
    print("2. Proceed to rendering (when ready):")
    print(f"   python scripts/05_render_resume.py --uuid {args.uuid} --version {args.version} [--format pdf] [--trim]")


if __name__ == "__main__":
    main()