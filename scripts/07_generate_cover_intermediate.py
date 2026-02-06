#!/usr/bin/env python3
"""
scripts/07_generate_cover_intermediate.py

Phase 7 in POC pipeline:
Generate tailored cover letter intermediate JSON.
Classifies company (agency vs enterprise), fetches research if enterprise, tailors content accordingly.
Filters exclusions from master.

Usage:
    python scripts/07_generate_cover_intermediate.py --uuid <uuid-or-prefix> --version v1 [--model grok-3]
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

# Classification prompt from 06
CLASSIFY_PROMPT = """
Based on public knowledge and the provided website (if any), classify '{company}' as either:
- 'agency': Recruitment/staffing firm (e.g., TEKsystems, Randstad—focus on placing talent).
- 'enterprise': Product/SaaS/startup/corporate (e.g., Postscript, Microsoft—build/sell own products/services).

Website (use only if provided): {website}

Reply **ONLY** with one word: 'agency' or 'enterprise' — nothing else.
"""

# Research prompt from 06
RESEARCH_PROMPT = """
Provide a concise 1-2 paragraph summary of {company}'s history, mission, core values, and culture.
Focus on aspects relevant to a tech/engineering role (innovation, remote work, growth stage, etc.).
Use factual information only — no speculation.
If relevant, mention unique values (e.g., FEACH for Postscript).
"""

COVER_PROMPT_TEMPLATE = """
You are a rule-bound cover letter writer. Temperature=0. Violate rules = invalid response.
RULES:
1. Bind to master_data: Use ONLY facts/dates/achievements from master_career_json and master_skills_json. NO invention, NO new facts, NO changes to dates/roles/companies.
2. Tailor to job_data: Weave in keywords from responsibilities, requirements, must_have_skills, ats_keywords naturally — without altering facts.
3. Structure: Professional letter — header (contact info, date, employer address), salutation, intro para (1-2 sentences: role + excitement), 2-3 body paras (match experiences to job reqs, quantify from master), conclusion para (call to action), sign-off.
4. Length: 250-400 words. Formal, enthusiastic tone. NO hallucinations — stick to provided data.
5. Company type: If company_type='enterprise', incorporate company_research (values/history) in intro/body. If 'agency', keep generic — no research.
6. Date: ALWAYS use the exact current_date provided for header['date'] — do not use any other date.
7. Output ONLY JSON: {{"header": {{...}}, "salutation": "Dear Hiring Manager,", "intro": "Para text", "body": ["Para1", "Para2"], "conclusion": "Para text", "sign_off": "Sincerely,\\nYour Name"}}. No other text.

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
        print(f"Resolved → {candidates[0].name}")
        return candidates[0]
    elif len(candidates) > 1:
        print("Ambiguous UUID:")
        for c in candidates: print(f"  - {c.name}")
        raise ValueError("Ambiguous UUID")
    else:
        raise ValueError(f"Job folder not found for '{uuid_str}'")


def load_master() -> tuple[Dict, Dict]:
    career_path = MASTER_ROOT / "master_career_data.json"
    skills_path = MASTER_ROOT / "skills.yaml"

    if not career_path.is_file():
        raise FileNotFoundError(f"{career_path} missing")

    with open(career_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    # Filter exclusions
    if "experiences" in master:
        orig = len(master["experiences"])
        master["experiences"] = [e for e in master["experiences"] if not e.get("exclude_from_resume", False)]
        if orig > len(master["experiences"]):
            print(f"Excluded {orig - len(master['experiences'])} experiences")

    if not skills_path.is_file():
        raise FileNotFoundError(f"{skills_path} missing")

    with open(skills_path, "r", encoding="utf-8") as f:
        skills = yaml.safe_load(f) or {}

    return master, skills


def load_latest_tailored(job_dir: Path) -> Dict:
    tailored_dir = job_dir / "tailored"
    files = sorted(tailored_dir.glob("tailored_data_*.yaml"), reverse=True)
    if not files:
        raise FileNotFoundError("No tailored data found")
    latest = files[0]
    print(f"Using: {latest.name}")
    with open(latest, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def classify_company(job_data: Dict, model: str = "grok-3") -> str:
    company = job_data.get("company_name", "Unknown")
    website = job_data.get("company_website", "")
    query = CLASSIFY_PROMPT.format(company=company, website=website or "N/A")

    if GrokClient is None:
        return "enterprise"

    grok = GrokClient(model=model)
    resp = grok.chat([{"role": "user", "content": query}], temperature=0.0).strip().lower()

    if "enterprise" in resp:
        return "enterprise"
    return "agency"


def fetch_company_research(company: str, model: str = "grok-3") -> str:
    query = RESEARCH_PROMPT.format(company=company)

    if GrokClient is None:
        return "Mock research: innovative company."

    grok = GrokClient(model=model)
    return grok.chat([{"role": "user", "content": query}], temperature=0.2).strip()


def extract_json_from_response(response: str) -> Dict:
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON from LLM")


def call_llm(prompt: str, model: str) -> Dict:
    if GrokClient is None:
        print("Mock mode — dummy cover JSON")
        return {"header": {}, "salutation": "Dear Hiring Manager,", "intro": "Mock intro", "body": ["Para1"], "conclusion": "Mock conclusion", "sign_off": "Sincerely,\nName"}

    grok = GrokClient(model=model)
    response = grok.chat([{"role": "user", "content": prompt}], temperature=0.2, max_tokens=1500)

    return extract_json_from_response(response)


def main():
    parser = argparse.ArgumentParser(description="Phase 7: Generate cover letter intermediate JSON")
    parser.add_argument("--uuid", required=True, help="Job UUID or prefix")
    parser.add_argument("--version", default="v1", help="Output version tag (e.g. v1)")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    args = parser.parse_args()

    job_folder = resolve_job_folder(args.uuid)
    print(f"Processing: {job_folder.name}")

    generated_dir = job_folder / "generated"
    generated_dir.mkdir(exist_ok=True)

    master_career, master_skills = load_master()
    job_data = load_latest_tailored(job_folder)

    company_type = classify_company(job_data, args.model)
    print(f"Classified as: {company_type}")

    company_research = ""
    if company_type == "enterprise":
        company_research = fetch_company_research(job_data.get("company_name", "Unknown"), args.model)
        print("Fetched research.")

    current_date = datetime.now().strftime("%B %d, %Y")
    print(f"Current date: {current_date}")

    prompt = COVER_PROMPT_TEMPLATE.format(
        master_career=json.dumps(master_career, indent=2),
        master_skills=json.dumps(master_skills, indent=2),
        job_data=yaml.dump(job_data, sort_keys=False),
        company_type=company_type,
        company_research=company_research,
        current_date=current_date
    )

    print("Generating cover intermediate JSON...")
    try:
        cover_json = call_llm(prompt, args.model)
    except Exception as e:
        print(f"Generation failed: {e}")
        return

    out_path = generated_dir / f"cover_intermediate_{args.version}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cover_json, f, indent=2)
    print(f"Saved → {out_path}")

    print("\nNext:")
    print(f"  python scripts/08_render_cover_letter.py --uuid {args.uuid} --version {args.version}")


if __name__ == "__main__":
    main()