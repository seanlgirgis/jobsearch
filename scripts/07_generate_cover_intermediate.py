# FIXED VERSION
# Added:
# - Basic JSON validation hook
# - No structural changes to pipeline

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
You are a strict cover letter writer. Use ONLY facts from master_career and master_skills — NO invention.

RULES (violation = invalid output):
1. FACTS: Every claim must trace to master_career or master_skills. No invented metrics, no new companies, no changed dates.
2. TAILORING: Naturally weave in keywords from must_have_skills, ats_keywords, and responsibilities — without distorting facts.
3. INTRO (1–2 sentences): Open with "I am applying for the {job_title} position at {company_name}." Then one sentence of genuine excitement tied to a specific aspect of the company or role from job_data or company_research.
4. BODY (2–3 paragraphs): Each paragraph maps a concrete experience from master_career to a specific job requirement. Include at least one metric from master data per paragraph (numbers, percentages, scale).
5. COMPANY VALUES: If company_type='enterprise' and company_research names specific values, programs, or culture terms (e.g., "FEACH", "customer obsession"), reference at least one by name in the body or conclusion. If 'agency', keep generic.
6. LENGTH: 220–320 words total. Formal, confident tone — no filler phrases ("I am excited to", "I believe", "I am passionate").
7. HEADER ADDRESS: If the job location contains "Remote" or location is unknown, set header['employer_address'] to "" (empty string). Only populate it for on-site roles with a real city.
8. DATE: Use EXACTLY the current_date provided for header['date'].
9. OUTPUT: ONLY this JSON — no other text:
{{
  "header": {{"name": "...", "address": "...", "phone": "...", "email": "...", "date": "...", "employer_address": ""}},
  "salutation": "Dear Hiring Manager,",
  "intro": "paragraph text",
  "body": ["paragraph 1 text", "paragraph 2 text", "paragraph 3 text"],
  "conclusion": "paragraph text",
  "sign_off": "Sincerely,\\nFull Name"
}}
10. CRITICAL: company name = "{company_name}", job title = "{job_title}". Use exactly these — never "Unknown" or "0".

Current date: {current_date}
Master career (JSON): {master_career}
Master skills (JSON): {master_skills}
Job data (YAML): {job_data}
Company type: {company_type}
Company research: {company_research}

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


def load_research_from_file(job_folder: Path) -> tuple[str, str] | None:
    """Load company type and research from Script 06's saved file. Returns (type, research) or None."""
    research_dir = job_folder / "research"
    candidates = sorted(research_dir.glob("company_research*.yaml"), reverse=True) if research_dir.is_dir() else []
    if not candidates:
        return None
    with open(candidates[0], "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    company_type = data.get("type", "").strip().lower()
    research = data.get("research", "").strip()
    if company_type in ("agency", "enterprise"):
        print(f"Loaded research from {candidates[0].name} (type={company_type})")
        return company_type, research
    return None


def classify_company(job_data: Dict, model: str = "grok-3") -> str:
    company = job_data.get("company_name", "Unknown")
    website = job_data.get("company_website", "")
    query = CLASSIFY_PROMPT.format(company=company, website=website or "N/A")

    if GrokClient is None:
        return "enterprise"

    grok = GrokClient(model=model)
    resp = grok.chat([{"role": "user", "content": query}], temperature=0.0, max_tokens=10).strip().lower()

    if "enterprise" in resp:
        return "enterprise"
    return "agency"


def fetch_company_research(company: str, model: str = "grok-3") -> str:
    query = RESEARCH_PROMPT.format(company=company)

    if GrokClient is None:
        return "Mock research: innovative company."

    grok = GrokClient(model=model)
    return grok.chat([{"role": "user", "content": query}], temperature=0.2, max_tokens=500).strip()


def extract_json_from_response(response: str) -> Dict:
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON from LLM")


def sanitize_public_address(address: str, fallback_location: str = "") -> str:
    """Return city/state style address only; remove street-level details."""
    text = (address or "").strip()
    fallback = (fallback_location or "").strip()
    source = text or fallback
    if not source:
        return ""

    if re.search(r"\bremote\b", source, flags=re.IGNORECASE):
        return "Remote"

    city_state_matches = list(re.finditer(r"([A-Za-z][A-Za-z .'-]+,\s*[A-Z]{2})", source))
    city_state = city_state_matches[-1].group(1).strip() if city_state_matches else ""
    paren = re.search(r"(\([^)]+\))", source)
    if city_state:
        if paren and paren.group(1) not in city_state:
            return f"{city_state} {paren.group(1)}"
        return city_state

    # Fallback cleanup if city/state cannot be extracted confidently.
    cleaned = re.sub(r"\b\d{5}(?:-\d{4})?\b", "", source)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" ,")
    if re.search(r"\d", cleaned):
        return ""
    return cleaned


def enforce_cover_output_rules(cover_json: Dict, job_data: Dict, metadata: Dict, current_date: str) -> Dict:
    if not isinstance(cover_json, dict):
        raise ValueError("Cover JSON must be an object")

    header = cover_json.get("header")
    if not isinstance(header, dict):
        header = {}
    cover_json["header"] = header

    fallback_location = str(job_data.get("location") or metadata.get("location") or "")
    header["address"] = sanitize_public_address(str(header.get("address", "")), fallback_location)
    header["date"] = current_date

    # Never ship unknown placeholders.
    if str(cover_json.get("salutation", "")).strip() == "":
        cover_json["salutation"] = "Dear Hiring Manager,"

    return cover_json


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

    metadata = {}
    metadata_path = job_folder / "metadata.yaml"
    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f) or {}

    # Use Script 06's saved research if available (avoids 2 redundant API calls)
    cached = load_research_from_file(job_folder)
    if cached:
        company_type, company_research = cached
    else:
        print("No cached research found — calling API...")
        company_type = classify_company(job_data, args.model)
        print(f"Classified as: {company_type}")
        company_research = ""
        if company_type == "enterprise":
            company_research = fetch_company_research(job_data.get("company_name", "Unknown"), args.model)
            print("Fetched research.")

    current_date = datetime.now().strftime("%B %d, %Y")
    print(f"Current date: {current_date}")

    company_name = job_data.get("company_name") or metadata.get("company", "the company")
    job_title = job_data.get("job_title") or metadata.get("role", "the role")

    prompt = COVER_PROMPT_TEMPLATE.format(
        master_career=json.dumps(master_career, separators=(',', ':')),
        master_skills=json.dumps(master_skills, separators=(',', ':')),
        job_data=yaml.dump(job_data, sort_keys=False),
        company_type=company_type,
        company_research=company_research,
        current_date=current_date,
        company_name=company_name,
        job_title=job_title
    )

    print("Generating cover intermediate JSON...")
    try:
        cover_json = call_llm(prompt, args.model)
        cover_json = enforce_cover_output_rules(cover_json, job_data, metadata, current_date)
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
