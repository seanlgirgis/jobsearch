#!/usr/bin/env python3
"""
scripts/06_generate_cover_intermediate.py

Phase 6 in POC pipeline:
Generate tailored cover letter intermediate JSON.
Classifies company (agency vs enterprise), fetches research if enterprise, tailors content accordingly.
Filters exclusions from master.

Usage:
    python scripts/06_generate_cover_intermediate.py --uuid <uuid-or-prefix> --version v1 [--model grok-3]
"""

import argparse
import json
import yaml
import re
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

try:
    from src.ai.grok_client import GrokClient
except ImportError:
    print("Warning: src.ai.grok_client not found — mock mode enabled.")
    GrokClient = None

JOB_ROOT = Path("data/jobs")
MASTER_ROOT = Path("data/master")

# Improved TEMPLATE - stronger anti-hallucination rules + current date injection
COVER_PROMPT_TEMPLATE = """
You are a rule-bound cover letter writer. Temperature=0. Violate rules = invalid response.
RULES:
1. Bind to master_data: Use ONLY facts/dates/achievements from master_career_json and master_skills_json. NO invention, NO new facts, NO changes to dates/roles/companies.
2. Tailor to job_data: Weave in keywords from responsibilities, requirements, must_have_skills, ats_keywords naturally — without altering facts.
3. Structure: Professional letter — header (contact info, date, employer address), salutation, intro para (1-2 sentences: role + excitement), 2-3 body paras (match experiences to job reqs, quantify from master), conclusion para (call to action), sign-off.
4. Length: 250-400 words. Formal, enthusiastic tone. NO hallucinations — stick to provided data.
5. Company type: If company_type='enterprise', incorporate company_research (values/history) in intro/body. If 'agency', keep generic — no research.
6. Date: ALWAYS use the exact current_date provided for header['date'] — do not use any other date.
7. Output ONLY JSON: {{ "header": {{...}}, "salutation": "Dear Hiring Manager,", "intro": "Para text", "body": ["Para1", "Para2"], "conclusion": "Para text", "sign_off": "Sincerely,\\nYour Name" }}. No other text.

Current date (use this EXACTLY for header['date']): {current_date}

Master career (JSON):
{master_career}

Master skills (JSON):
{master_skills}

Job data (YAML):
{job_data}

Company type: {company_type}
Company research (if enterprise): {company_research}

Generate JSON now.
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
        print(f"Resolved: {candidates[0].name}")
        return candidates[0]
    elif len(candidates) > 1:
        raise ValueError("Ambiguous UUID")
    else:
        raise ValueError("Job folder not found")

def load_master() -> tuple[Dict, Dict]:
    career_path = MASTER_ROOT / "master_career_data.json"
    skills_path = MASTER_ROOT / "skills.yaml"

    if not career_path.is_file():
        print(f"Warning: {career_path} missing — using minimal mock data")
        master = {
            "personal_info": {"full_name": "Sean Luka Girgis", "email": "seanlgirgis@gmail.com"},
            "experiences": [],
            "education": []
        }
    else:
        with open(career_path, "r", encoding="utf-8") as f:
            master = json.load(f)
        # Apply exclude filter
        if "experiences" in master:
            orig_len = len(master["experiences"])
            master["experiences"] = [exp for exp in master["experiences"] if not exp.get("exclude_from_resume", False)]
            if len(master["experiences"]) < orig_len:
                print(f"Excluded {orig_len - len(master['experiences'])} experiences")

    if not skills_path.is_file():
        print("Warning: skills.yaml missing — using empty skills")
        skills = {}
    else:
        with open(skills_path, "r", encoding="utf-8") as f:
            skills = yaml.safe_load(f) or {}

    return master, skills

def load_latest_tailored(job_dir: Path) -> Dict:
    tailored_dir = job_dir / "tailored"
    if not tailored_dir.is_dir():
        raise FileNotFoundError(f"No tailored/ folder: {tailored_dir}")
    files = sorted(tailored_dir.glob("tailored_data_*.yaml"), reverse=True)
    if not files:
        raise FileNotFoundError("No tailored_data_*.yaml found")
    print(f"Using tailored: {files[0].name}")
    with open(files[0], "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def classify_company(job_data: Dict) -> str:
    company = job_data.get("company", "").lower()
    agencies = ["teksystems", "randstad", "robert half", "adecco", "manpower"]
    enterprises = ["aetna", "southwest airlines", "microsoft", "citi", "at&t", "collective health"]
    if any(a in company for a in agencies):
        return "agency"
    if any(e in company for e in enterprises):
        return "enterprise"
    return "agency"

def fetch_company_research(company: str, model: str) -> str:
    if GrokClient is None:
        return "Mock research: Company values include innovation and customer focus."
    grok = GrokClient(model=model)
    query = f"Brief 1-2 paragraph summary of {company}'s history, mission, and core values."
    response = grok.chat([{"role": "user", "content": query}], temperature=0.0, max_tokens=300)
    return response.strip()

def call_llm(prompt: str, model: str) -> Dict:
    if GrokClient is None:
        return {
            "header": {"your_address": "Your Address", "date": "Date", "employer_address": "Employer Address"},
            "salutation": "Dear Hiring Manager,",
            "intro": "Mock intro paragraph.",
            "body": ["Mock body para 1.", "Mock body para 2."],
            "conclusion": "Mock conclusion.",
            "sign_off": "Sincerely,\nSean Luka Girgis"
        }
    grok = GrokClient(model=model)
    print(f"Calling Grok ({model}) for cover letter...")
    response = grok.chat([{"role": "user", "content": prompt}], temperature=0.0, max_tokens=1500)

    # Extract JSON
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        json_str = match.group(0)
    else:
        json_str = response
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        print("Raw response excerpt:", response[:500] + "..." if len(response) > 500 else response)
        raise ValueError("Invalid JSON from LLM")

def main():
    parser = argparse.ArgumentParser(description="Phase 6: Generate cover letter intermediate JSON")
    parser.add_argument("--uuid", required=True, help="Job UUID or short prefix (e.g. cdb9a3fa)")
    parser.add_argument("--version", default="v1", help="Output version tag (e.g. v1)")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    args = parser.parse_args()

    job_folder = resolve_job_folder(args.uuid)
    print(f"Processing job: {job_folder.name}")

    generated_dir = job_folder / "generated"
    generated_dir.mkdir(exist_ok=True)

    master_career, master_skills = load_master()
    job_data = load_latest_tailored(job_folder)

    company_type = classify_company(job_data)
    print(f"Classified company as: {company_type}")

    company_research = ""
    if company_type == "enterprise":
        company_research = fetch_company_research(job_data.get("company", "Unknown Company"), args.model)
        print("Fetched company research.")

    # Inject current date
    current_date = datetime.now().strftime("%B %Y")
    print(f"Using current date: {current_date}")

    prompt = COVER_PROMPT_TEMPLATE.format(
        master_career=json.dumps(master_career, indent=2),
        master_skills=json.dumps(master_skills, indent=2),
        job_data=yaml.dump(job_data, sort_keys=False),
        company_type=company_type,
        company_research=company_research,
        current_date=current_date
    )

    print("Generating cover letter intermediate JSON...")
    cover_json = call_llm(prompt, args.model)

    out_path = generated_dir / f"cover_intermediate_{args.version}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cover_json, f, indent=2, ensure_ascii=False)
    print(f"Success! Intermediate cover saved → {out_path}")

    print("\nNext steps:")
    print("1. Review and tweak the JSON if needed")
    print(f"2. Run phase 7 renderer:")
    print(f"   python scripts/07_render_cover_letter.py --uuid {args.uuid} --version {args.version}")


if __name__ == "__main__":
    main()