#!/usr/bin/env python3
"""
scripts/04_generate_resume_intermediate.py

Phase 4 in POC pipeline:
After job is ACCEPTED and tailored → generate a tailored resume in structured JSON format.
Uses Grok to rewrite bullets/summary/projects while strictly binding to master career data.
Filters out experiences with "exclude_from_resume": true.

Usage:
    python scripts/04_generate_resume_intermediate.py --uuid <uuid-or-prefix> --version tailored-v1 [--model grok-3]
    #python scripts/04_generate_resume_intermediate.py --uuid 00001_cdb9a3fa --version llm-tailored-v1 --model grok-3
"""

import argparse
import json
import yaml
import re
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from src.ai.grok_client import GrokClient
except ImportError:
    print("Warning: src.ai.grok_client not found — mock mode enabled.")
    GrokClient = None

JOB_ROOT = Path("data/jobs")
MASTER_ROOT = Path("data/master")

# Strict prompt — temperature=0 enforced via instruction
RESUME_PROMPT_TEMPLATE = """
You are a rule-bound resume optimizer. Temperature=0 for determinism. Violate rules = invalid response.
CHECKLIST (MUST ADHERE 100%):
1. No truncation: Keep ALL core sections from master (personal, summary, experience, education, skills, projects).
   Include EVERY experience and project — do not omit or remove entries.
2. Tailor only: Adjust wording of bullets, summary, project descriptions to naturally include job keywords.
   NO invention, NO date changes, NO new facts, NO removing entries.
3. Bind to source_of_truth: Use EXACT dates, roles, companies, degrees from master_career_data.
4. Output ONLY valid JSON: Start with {{ and end with }}. No markdown, no explanation, no fences.
   If output would be too long, shorten individual bullet/project descriptions slightly but keep ALL entries.
5. Experience: Keep chronological order, full history. Max 3-5 bullets per role (prioritize relevance).
6. Skills: Include ALL from master, deduplicated, sorted by relevance to job (top matches first).
7. Summary: <150 words, tailored to job responsibilities/requirements.
8. Projects: Keep all, tailor descriptions (2-3 sentences max each).

Master career data (JSON) — already filtered:
{career_json}

Master skills (JSON):
{skills_json}

Job data (YAML) — use to guide keyword weaving:
{job_yaml}

Generate the tailored resume JSON now.
Output ONLY the complete JSON object — nothing else.
"""

def resolve_job_folder(uuid_str: str) -> Path:
    """Smart resolution like in 02_decide_job.py and 03_tailor_job_data.py"""
    uuid_str = uuid_str.strip()
    job_dir = JOB_ROOT / uuid_str

    if job_dir.is_dir():
        return job_dir

    # Try prefix matching
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
        raise ValueError(
            f"Job folder not found for '{uuid_str}'\n"
            f"Expected: data/jobs/{uuid_str} or data/jobs/*_{uuid_str}*"
        )


def load_master() -> tuple[Dict, Dict]:
    career_path = MASTER_ROOT / "master_career_data.json"
    skills_path = MASTER_ROOT / "skills.yaml"

    if not career_path.is_file() or not skills_path.is_file():
        raise FileNotFoundError(f"Master files missing at {MASTER_ROOT}. Run profile_export.py.")

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
        raise FileNotFoundError(f"No tailored/ folder: {tailored_dir}")

    # Find the latest version (highest alphanumeric sort)
    files = sorted(tailored_dir.glob("tailored_data_*.yaml"), reverse=True)
    if not files:
        raise FileNotFoundError(f"No tailored_data_*.yaml found in {tailored_dir}")

    latest = files[0]
    print(f"Using latest tailored file: {latest.name}")
    with open(latest, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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

    # Extract JSON
    json_str = response.strip()
    if json_str.startswith("```json"):
        json_str = json_str.split("```json", 1)[1].split("```", 1)[0].strip()
    match = re.search(r'\{.*\}', json_str, re.DOTALL)
    if match:
        json_str = match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        print("Raw LLM response excerpt:")
        print(response[:1200] + "..." if len(response) > 1200 else response)
        raise


def main():
    parser = argparse.ArgumentParser(description="Phase 4: Generate tailored resume intermediate JSON")
    parser.add_argument("--uuid", required=True, help="Job UUID or short prefix (e.g. cdb9a3fa)")
    parser.add_argument("--version", default="v1", help="Output version tag (e.g. tailored-v1)")
    parser.add_argument("--model", default="grok-3", help="Grok model to use")
    args = parser.parse_args()

    # Resolve folder
    job_folder = resolve_job_folder(args.uuid)
    print(f"Processing job: {job_folder.name}")

    # Prepare output dir
    generated_dir = job_folder / "generated"
    generated_dir.mkdir(exist_ok=True)

    # Load sources
    master_career, master_skills = load_master()
    job_data = load_latest_tailored_job(job_folder)

    # Build prompt
    prompt = RESUME_PROMPT_TEMPLATE.format(
        career_json=json.dumps(master_career, indent=2),
        skills_json=json.dumps(master_skills, indent=2),
        job_yaml=yaml.dump(job_data, sort_keys=False, allow_unicode=True)
    )

    print("Generating tailored resume intermediate JSON...")
    tailored_resume = call_llm(prompt, args.model)

    # Save
    out_path = generated_dir / f"resume_intermediate_{args.version}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tailored_resume, f, indent=2, ensure_ascii=False)

    print(f"Success! Intermediate resume saved → {out_path}")

    print("\nNext steps:")
    print("1. Review and manually tweak the JSON if needed")
    print(f"2. Run phase 5 renderer:")
    print(f"   python scripts/05_render_resume.py --uuid {args.uuid} --version {args.version} [--format pdf] [--trim]")


if __name__ == "__main__":
    main()