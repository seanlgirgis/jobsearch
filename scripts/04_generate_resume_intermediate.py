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
You are a resume optimizer. NEVER invent facts. NEVER change dates, titles, companies, or degrees.

MANDATORY RULES — violation = invalid output:

1. HEADER TITLE: Rewrite the professional subtitle under the candidate's name to mirror this job's level and
   domain keywords (e.g., "Staff Data Engineer | Cloud Lakehouse & Stream Processing"). Pull exact terms
   from job_title, must_have_skills, and ats_keywords. Never reuse the master profile subtitle verbatim.

2. EXPERIENCE — preserve all entries, but apply these bullet rules by era:
   - Roles ending 2010 or later: write 4–6 strong bullets each.
   - Roles ending 2005–2009: write 2–3 bullets max, focusing only on skills/tech that match this job.
   - Roles ending before 2005: keep company/title/dates but write AT MOST 2 bullets — or skip bullets
     entirely if nothing in that role matches the job's must_have_skills or extracted_skills.
   Keep original company, title, and dates exactly — do not modify them.

3. BULLET FORMAT (STAR-lite): Every bullet must follow: [Action verb] + [what was built/done] + [result or metric].
   Example: "Architected ETL pipelines ingesting telemetry from 6,000+ endpoints, replacing manual processes
   and cutting reporting lag by 40%."
   If master data has a specific number or percentage, include it exactly. Never drop metrics.

4. SUMMARY: 4–5 sentences. Open with the exact target job title level (e.g., "Staff Data Engineer" or "Lead
   Engineer"). Weave in 6–8 keywords from must_have_skills and ats_keywords. Close with one sentence about
   contributing to {company_name}.

5. SKILLS: Group into exactly these categories on one line each, pipe-separated within each group:
   "Languages: ..." | "Cloud & Data: ..." | "AI/ML: ..." | "Tools & Infra: ..." | "Legacy: ..."
   Put must_have_skills and nice_to_have_skills from the job first within each group.
   Include ALL skills from master skills — no omissions.

6. PROJECTS: Keep ALL. Max 3 sentences per project description. Rewrite to emphasize technologies matching
   this job's extracted_skills and ats_keywords.

7. Output ONLY valid JSON — nothing before {{ or after }}. No markdown, no explanations, no fences.

Master career data (use EXACTLY — do not alter facts):
{career_json}

Master skills (include all, prioritize job-relevant):
{skills_json}

Job data (keywords, must-haves, ATS terms — source of tailoring):
{job_yaml}

Generate the tailored resume JSON now. Output ONLY the JSON object.
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
    response = grok.chat([{"role": "user", "content": prompt}], max_tokens=4096, temperature=0.0)

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
        career_json=json.dumps(master_career, separators=(',', ':')),
        skills_json=json.dumps(master_skills, separators=(',', ':')),
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