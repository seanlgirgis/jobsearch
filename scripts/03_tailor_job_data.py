#!/usr/bin/env python3
"""
scripts/03_tailor_job_data.py

Phase 3 in POC pipeline:
After scoring & accepting a job → tailor / structure / enrich the job data
for better RAG retrieval, resume/cover matching, keyword optimization.

Now uses Grok LLM for high-quality structured output (with naive regex fallback).
Supports smart UUID resolution like 02_decide_job.py.

Usage:
    python scripts/03_tailor_job_data.py --uuid <uuid-or-prefix> [--version llm-v1]
    [--model grok-3] [--temperature 0.0] [--no-llm] [--raw-file path]
"""

import argparse
import yaml
import re
from pathlib import Path
from typing import Dict, Any, Optional

# Core imports (assumes src/ structure exists)
from src.ai.grok_client import GrokClient

JOB_ROOT = Path("data/jobs")

# Naive section extractors + skill patterns (kept for fallback)
SECTION_MARKERS = {
    "responsibilities": [r"(?i)(responsibilit(y|ies)|what you'll do|key duties|you will|day[- ]?to[- ]?day)"],
    "requirements": [r"(?i)(require(ments|d)|qualifications|must have|minimum)"],
    "preferred": [r"(?i)(preferred|nice to have|bonus|desired|plus)"],
    "benefits": [r"(?i)(benefit|perks|compensation|remote|hybrid)"],
}

SKILL_PATTERNS = [
    r"(?i)(python|java|javascript|typescript|go|rust|c\+\+|sql|aws|gcp|azure|docker|kubernetes|terraform|react|node\.js|django|flask|spring|kubernetes|ansible|jenkins|git|linux|windows|mysql|postgresql|mongodb|redis|elasticsearch|kafka|spark|hadoop|tableau|powerbi|excel|agile|scrum|devops|ci/cd|microservices|api|rest|graphql|machine learning|ai|data science|big data|cloud|security|networking|database|frontend|backend|fullstack|mobile|ios|android|flutter|react native|swift|kotlin|php|ruby|scala|perl|bash|shell|html|css|bootstrap|angular|vue|express|laravel|symfony|asp\.net|sql server|oracle|sap|salesforce|dynamics|erp|crm|blockchain|ethereum|bitcoin|nft|web3|vr|ar|unity|unreal|photoshop|illustrator|figma|sketch|invision|seo|sem|google analytics|adsense|adwords|content marketing|social media|email marketing|copywriting|ux|ui|product management|project management|leadership|team building|communication|problem solving|analytical|critical thinking)"
]

def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_section(text: str, section_key: str) -> str:
    markers = SECTION_MARKERS.get(section_key, [])
    if not markers:
        return ""
    pattern = '|'.join(markers)
    match = re.search(pattern, text)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(pattern, text[start:])
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()

def extract_skills(text: str) -> list[str]:
    skills = set()
    for pattern in SKILL_PATTERNS:
        matches = re.findall(pattern, text)
        skills.update(m.lower() for m in matches)
    return sorted(skills)

def build_tailoring_prompt(job_text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are an expert job description analyst for career applications and ATS optimization. "
                "Output ONLY valid YAML — no explanations, no markdown, no code blocks, no ``` fences."
            ),
        },
        {
            "role": "user",
            "content": f"""Parse the following job description.

Job description:
{job_text}

Output **exactly** this YAML structure (fill in the values):

extracted_skills:
- python
- sql
- aws
- ...

job_summary: |
  3-5 sentence concise summary of the role, company, key responsibilities, and requirements.

responsibilities:
- Clean, rephrased bullet point
- Another bullet point
- ...

requirements:
- Bullet point
- ...

preferred:
- ...

benefits:
- ...

must_have_skills:
- critical skill
- ...

nice_to_have_skills:
- ...

ats_keywords:
- keyword phrase one
- keyword phrase two
- ...
"""
        },
    ]

def tailor_job(
    uuid: str,
    version: str = "v1",
    raw_file: Optional[str] = None,
    model: str = "grok-3",
    temperature: float = 0.0,
    no_llm: bool = False,
) -> None:
    uuid_str = uuid.strip()

    # Try direct folder name first
    job_dir = JOB_ROOT / uuid_str

    # Smart resolution if not found (same logic as 02_decide_job.py)
    if not job_dir.is_dir():
        # Look for folders like 00001_cdb9a3fa when given cdb9a3fa
        candidates = list(JOB_ROOT.glob(f"*_{uuid_str}*"))
        if len(candidates) == 0:
            # Try even shorter prefix (first 8 chars)
            short_prefix = uuid_str[:8]
            candidates = list(JOB_ROOT.glob(f"*_{short_prefix}*"))

        if len(candidates) == 1:
            job_dir = candidates[0]
            print(f"Resolved UUID/prefix → using folder: {job_dir.name}")
        elif len(candidates) > 1:
            print("Ambiguous UUID — multiple matching folders:")
            for c in candidates:
                print(f"  - {c.name}")
            raise ValueError(f"Ambiguous UUID prefix: {uuid_str}")
        else:
            raise ValueError(
                f"Job folder not found for UUID '{uuid_str}'\n"
                f"Looked for:\n"
                f"  - data/jobs/{uuid_str}\n"
                f"  - data/jobs/*_{uuid_str}*\n"
                f"  - data/jobs/*_{uuid_str[:8]}*"
            )

    # Now we have a valid job_dir
    print(f"Processing job folder: {job_dir.name}")

    # Determine raw file path
    if raw_file:
        raw_path = Path(raw_file)
    else:
        # Try common locations
        candidates = [
            job_dir / "raw" / "job_description.md",
            job_dir / "raw" / "raw_intake.md",
            job_dir / "raw_intake.md",           # sometimes people put it directly
        ]
        for p in candidates:
            if p.is_file():
                raw_path = p
                break
        else:
            raise FileNotFoundError(
                f"No raw job description found in {job_dir / 'raw'}\n"
                "Tried: job_description.md, raw_intake.md"
            )

    print(f"Reading raw job from: {raw_path}")

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned = clean_text(raw_text)

    if no_llm:
        print("Using naive regex extraction (no LLM)")
        tailored_data: Dict[str, Any] = {
            "extracted_skills": extract_skills(cleaned),
            "sections": {
                "responsibilities": extract_section(cleaned, "responsibilities"),
                "requirements": extract_section(cleaned, "requirements"),
                "preferred": extract_section(cleaned, "preferred"),
                "benefits": extract_section(cleaned, "benefits"),
            },
            "tailoring_method": "naive",
        }
    else:
        print(f"Using LLM tailoring (model={model}, temp={temperature})")
        messages = build_tailoring_prompt(raw_text)
        try:
            grok = GrokClient(model=model)
            response = grok.chat(
                messages=messages,
                temperature=temperature,
                max_tokens=4000,
            )

            # Aggressive cleaning of LLM output
            response_clean = response.strip()
            # Remove common markdown fences
            if response_clean.startswith("```"):
                parts = re.split(r"```(?:yaml)?", response_clean, maxsplit=2)
                if len(parts) > 1:
                    response_clean = parts[1].strip()
            # Remove any trailing explanation
            yaml_start = response_clean.find("extracted_skills:")
            if yaml_start > 0:
                response_clean = response_clean[yaml_start:]

            llm_data = yaml.safe_load(response_clean)
            if not isinstance(llm_data, dict):
                raise ValueError("LLM response did not parse to a valid dict")

            tailored_data = llm_data
            tailored_data["tailoring_method"] = "llm"
            tailored_data["llm_model"] = model
            tailored_data["llm_version"] = version
            print("LLM tailoring successful")

        except Exception as e:
            print(f"LLM tailoring failed: {e} — falling back to naive")
            tailored_data = {
                "extracted_skills": extract_skills(cleaned),
                "sections": {
                    "responsibilities": extract_section(cleaned, "responsibilities"),
                    "requirements": extract_section(cleaned, "requirements"),
                    "preferred": extract_section(cleaned, "preferred"),
                    "benefits": extract_section(cleaned, "benefits"),
                },
                "tailoring_method": "llm_fallback_naive",
                "llm_error": str(e),
            }

    # Save result
    tailored_dir = job_dir / "tailored"
    tailored_dir.mkdir(exist_ok=True)
    out_file = tailored_dir / f"tailored_data_{version}.yaml"

    with open(out_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(tailored_data, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

    print(f"Tailored data saved: {out_file}")
    skills = tailored_data.get("extracted_skills") or tailored_data.get("sections", {}).get("requirements", "").lower().split()
    print(f"Extracted/Detected skills ({len(skills)}): {', '.join(skills[:15])}{' ...' if len(skills) > 15 else ''}")


def main():
    parser = argparse.ArgumentParser(description="Tailor job data for accepted jobs (LLM + naive fallback)")
    parser.add_argument("--uuid", required=True, help="Job UUID or short prefix (e.g. cdb9a3fa)")
    parser.add_argument("--version", default="v1", help="Tailored version tag (v1, llm-v1, etc.)")
    parser.add_argument("--raw-file", default=None, help="Override raw job file path")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    parser.add_argument("--temperature", type=float, default=0.0, help="LLM temperature (0.0 = deterministic)")
    parser.add_argument("--no-llm", action="store_true", help="Force naive regex mode (no LLM)")
    args = parser.parse_args()

    try:
        tailor_job(
            args.uuid,
            args.version,
            args.raw_file,
            args.model,
            args.temperature,
            args.no_llm,
        )
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()