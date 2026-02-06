#!/usr/bin/env python3
"""
scripts/06_company_research.py

Phase 6: Dynamically research and classify company, save to file.
Classifies as 'agency' or 'enterprise', fetches research if enterprise.
Saves company_research.yaml (or versioned) in job_folder/research/.

Usage:
    python scripts/06_company_research.py --uuid <uuid-or-prefix> [--model grok-3] [--version v1]
"""

import argparse
import yaml
from pathlib import Path
from typing import Dict, Optional

try:
    from src.ai.grok_client import GrokClient
except ImportError:
    print("Warning: src.ai.grok_client not found — using mock mode.")
    GrokClient = None

JOB_ROOT = Path("data/jobs")

CLASSIFY_PROMPT = """
Based on public knowledge and the provided website (if any), classify '{company}' as either:
- 'agency': Recruitment/staffing firm (e.g., TEKsystems, Randstad—focus on placing talent).
- 'enterprise': Product/SaaS/startup/corporate (e.g., Postscript, Microsoft—build/sell own products/services).

Website (use only if provided): {website}

Reply **ONLY** with one word: 'agency' or 'enterprise' — nothing else.
"""

RESEARCH_PROMPT = """
Provide a concise 1-2 paragraph summary of {company}'s history, mission, core values, and culture.
Focus on aspects relevant to a tech/engineering role (innovation, remote work, growth stage, etc.).
Use factual information only — no speculation.
If relevant, mention unique values (e.g., FEACH for Postscript).
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
        print(f"Resolved to: {candidates[0].name}")
        return candidates[0]
    elif len(candidates) > 1:
        raise ValueError(f"Ambiguous UUID prefix '{uuid_str}' — multiple matches")
    else:
        raise ValueError(f"No job folder found for '{uuid_str}'")


def load_latest_tailored(job_dir: Path) -> Dict:
    tailored_dir = job_dir / "tailored"
    if not tailored_dir.is_dir():
        raise FileNotFoundError(f"No tailored/ folder in {job_dir}")

    files = sorted(tailored_dir.glob("tailored_data_*.yaml"), reverse=True)
    if not files:
        raise FileNotFoundError("No tailored_data_*.yaml found")

    latest = files[0]
    print(f"Loading latest tailored: {latest.name}")
    with open(latest, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # Normalize company & website keys
    company = data.get("company") or data.get("company_name") or data.get("Company Name") or "Unknown Company"
    website = data.get("company_website") or data.get("Company_website") or data.get("website") or ""

    data["company"] = company.strip()
    data["company_website"] = website.strip()

    print(f"Company: '{company}'")
    print(f"Website: {website or 'none'}")
    return data


def classify_company(company: str, website: str, model: str) -> str:
    if GrokClient is None:
        print("Mock: assuming 'enterprise'")
        return "enterprise"

    grok = GrokClient(model=model)
    query = CLASSIFY_PROMPT.format(company=company, website=website or "N/A")
    try:
        resp = grok.chat([{"role": "user", "content": query}], temperature=0.0, max_tokens=20).strip().lower()
        # Robust parsing: take last word or exact match
        words = resp.split()
        last_word = words[-1] if words else ""
        if "agency" in last_word:
            return "agency"
        if "enterprise" in last_word:
            return "enterprise"
        print(f"Warning: ambiguous classification response: '{resp}' → defaulting to enterprise")
        return "enterprise"
    except Exception as e:
        print(f"Classification failed: {e} → defaulting to enterprise")
        return "enterprise"


def research_company(company: str, model: str) -> str:
    if GrokClient is None:
        return f"Mock research for {company}: innovative company with strong engineering culture."

    grok = GrokClient(model=model)
    query = RESEARCH_PROMPT.format(company=company)
    try:
        return grok.chat([{"role": "user", "content": query}], temperature=0.3, max_tokens=500).strip()
    except Exception as e:
        print(f"Research failed: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(description="Phase 6: Company research & classification")
    parser.add_argument("--uuid", required=True, help="Job UUID or prefix")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    parser.add_argument("--version", default="v1", help="Output version (optional)")
    args = parser.parse_args()

    job_folder = resolve_job_folder(args.uuid)
    print(f"Processing: {job_folder.name}")

    job_data = load_latest_tailored(job_folder)
    company = job_data.get("company", "Unknown")
    website = job_data.get("company_website", "")

    print(f"Classifying '{company}'...")
    company_type = classify_company(company, website, args.model)

    research = ""
    if company_type == "enterprise":
        print("Enterprise → fetching research...")
        research = research_company(company, args.model)
    else:
        print("Agency → skipping deep research")

    research_data = {
        "company": company,
        "type": company_type,
        "research": research,
        "website": website,
        "classified_at": str(Path().resolve()),  # optional: timestamp or model info
    }

    research_dir = job_folder / "research"
    research_dir.mkdir(exist_ok=True)

    suffix = f"_{args.version}" if args.version != "v1" else ""
    out_path = research_dir / f"company_research{suffix}.yaml"

    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(research_data, f, sort_keys=False, allow_unicode=True)

    print(f"Saved → {out_path}")
    print(f"Type: {company_type}")
    if research:
        print(f"Research length: {len(research)} chars")

    print("\nNext:")
    print(f"  python scripts/06_generate_cover_intermediate.py --uuid {args.uuid} --model {args.model}")


if __name__ == "__main__":
    main()