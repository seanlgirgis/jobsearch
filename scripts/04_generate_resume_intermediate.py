#!/usr/bin/env python3
"""
scripts/04_generate_resume_intermediate.py

Phase 4:
After job is ACCEPTED and tailored, generate a tailored resume in structured JSON format.

Fixed/hardened version:
- Enforces strict resume_intermediate_v1.json schema
- Requires POSITIONING_ANGLE or derives a safe default
- Forces summary to start with POSITIONING_ANGLE exactly
- Prevents schema drift (role/dates/highlights/name/etc.)
- Prevents generic source_of_truth summary copy/paste
- Validates output before saving
- Keeps Grok call structure compatible with current pipeline

Usage:
    python scripts/04_generate_resume_intermediate.py --uuid 402a89d6 --version v1 --angle "AWS Data Engineer specializing in ML-enabled pipelines and scalable data platforms" [--model grok-3]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

try:
    from src.ai.grok_client import GrokClient
except ImportError:
    print("Warning: src.ai.grok_client not found — mock mode enabled.")
    GrokClient = None

JOB_ROOT = Path("data/jobs")
MASTER_ROOT = Path("data/master")

DEFAULT_POSITIONING_ANGLE = "AWS Data Engineer specializing in ML-enabled pipelines and scalable data platforms"

REQUIRED_TOP_LEVEL_KEYS = {
    "personal",
    "summary",
    "experience",
    "education",
    "skills",
    "projects",
}

REQUIRED_PERSONAL_KEYS = {
    "full_name",
    "phone",
    "email",
    "linkedin",
    "github",
    "personal_website",
    "preferred_title",
}

REQUIRED_EXPERIENCE_KEYS = {
    "company",
    "title",
    "start_date",
    "end_date",
    "bullets",
}

REQUIRED_EDUCATION_KEYS = {
    "degree",
    "institution",
    "location",
    "dates",
}

REQUIRED_SKILL_KEYS = {
    "Languages",
    "Cloud & Data",
    "AI/ML",
    "Tools & Infra",
    "Legacy",
}

FIRST_PERSON_PATTERN = re.compile(r"\b(i|i'm|i’ve|i'd|i'll|my|me)\b", flags=re.IGNORECASE)

RESUME_PROMPT_TEMPLATE = """
You are a STRICT resume intermediate JSON generator.

YOUR OUTPUT WILL BE PARSED BY CODE.
ANY SCHEMA DRIFT IS INVALID.

OUTPUT RULES:
- Output ONLY valid JSON.
- No markdown.
- No code fences.
- No explanation.
- No text before or after the JSON object.
- Do NOT rename keys.
- Do NOT add extra top-level keys.
- Do NOT use alternative schemas.

SOURCE OF TRUTH RULES:
- source_of_truth/master career data is the only candidate truth.
- Never invent employers, titles, dates, metrics, tools, education, certifications, projects, or skills.
- If a field is missing, use "" or [] only.
- Do NOT copy or reuse sentences from source_of_truth summaries.
- Rewrite summary content from job alignment and POSITIONING_ANGLE.

POSITIONING_ANGLE:
{positioning_angle}

CRITICAL POSITIONING RULES:
- The "summary" field MUST begin EXACTLY with POSITIONING_ANGLE.
- The first sentence of "summary" MUST be:
  "{positioning_angle}."
- Do NOT rewrite, soften, expand, rename, or reinterpret POSITIONING_ANGLE.
- Do NOT prepend anything before POSITIONING_ANGLE.
- Never replace "AWS Data Engineer" with "AWS ML Data Engineer" unless POSITIONING_ANGLE explicitly says that.
- Keep ML positioned as ML-enabled data engineering, forecasting, scikit-learn, Prophet, and pipeline support unless the job and source data clearly justify otherwise.
- Avoid generic phrases such as "cloud infrastructure and performance engineering" unless the job explicitly requires that language.

SKILL HONESTY RULES:
- Do not overstate beginner/learning skills as production expertise.
- Do not claim expert Kafka, TensorFlow, PyTorch, Databricks, Snowflake, Terraform, Kubernetes, or deep learning unless the source data supports that exact level.
- Kafka may be included only as familiarity/learning unless source data proves production depth.
- TensorFlow and PyTorch must be excluded unless explicitly supported by source data.

REQUIRED JSON SCHEMA EXACTLY:
{
  "personal": {
    "full_name": "",
    "phone": "",
    "email": "",
    "linkedin": "",
    "github": "",
    "personal_website": "",
    "preferred_title": ""
  },
  "summary": "",
  "experience": [
    {
      "company": "",
      "title": "",
      "start_date": "",
      "end_date": "",
      "bullets": [""]
    }
  ],
  "education": [
    {
      "degree": "",
      "institution": "",
      "location": "",
      "dates": ""
    }
  ],
  "skills": {
    "Languages": "",
    "Cloud & Data": "",
    "AI/ML": "",
    "Tools & Infra": "",
    "Legacy": ""
  },
  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": []
    }
  ]
}

FORBIDDEN KEY NAMES:
- personal.name
- personal.location
- experience.role
- experience.dates
- experience.highlights
- skills as a list

REQUIRED KEY NAMES:
- personal.full_name
- experience.title
- experience.start_date
- experience.end_date
- experience.bullets
- skills must be an object with the five required skill categories.

CONTENT RULES:
- Summary must be concise: 2-3 lines total.
- Experience must preserve real company names, titles, and dates from master data.
- Use strongest relevant evidence first:
  - AWS S3, Glue, Redshift
  - Python / SQL
  - PySpark / Spark
  - ETL pipelines
  - Data warehousing / data lakes
  - ML forecasting with Prophet and scikit-learn
- Preserve real metrics exactly where available:
  - 6,000+ endpoints
  - 90%+ accuracy
  - 90% cycle reduction
  - 95% hardware footprint reduction
  - 20% throughput improvement
- Do not invent new metrics.
- Do not invent new outcomes.
- Projects must come only from master data.
- Education must come only from master data.

FINAL SELF-CHECK BEFORE ANSWERING:
- Does summary start exactly with "{positioning_angle}."?
- Did you use full_name, title, start_date, end_date, bullets?
- Did you avoid role, dates, highlights, and skills list?
- Did you avoid generic source summary phrases?
- Did you output valid JSON only?

Master career data:
{career_json}

Master skills:
{skills_json}

Job data:
{job_yaml}
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
    if len(candidates) > 1:
        print("Ambiguous UUID — multiple matches:")
        for c in candidates:
            print(f"  - {c.name}")
        raise ValueError(f"Ambiguous UUID: {uuid_str}")
    raise ValueError(f"Job folder not found for '{uuid_str}'")


def load_master() -> tuple[Dict[str, Any], Dict[str, Any]]:
    source_of_truth_path = Path("data/source_of_truth.json")
    career_path = MASTER_ROOT / "master_career_data.json"
    skills_path = MASTER_ROOT / "skills.yaml"

    if source_of_truth_path.is_file():
        with source_of_truth_path.open("r", encoding="utf-8") as f:
            master = json.load(f)
    elif career_path.is_file():
        with career_path.open("r", encoding="utf-8") as f:
            master = json.load(f)
    else:
        raise FileNotFoundError("Missing data/source_of_truth.json or data/master/master_career_data.json")

    if "experiences" in master:
        orig_len = len(master["experiences"])
        master["experiences"] = [
            exp for exp in master["experiences"]
            if not exp.get("exclude_from_resume", False)
        ]
        if len(master["experiences"]) < orig_len:
            print(f"Excluded {orig_len - len(master['experiences'])} experience entries (exclude_from_resume)")

    if skills_path.is_file():
        with skills_path.open("r", encoding="utf-8") as f:
            skills = yaml.safe_load(f) or {}
    else:
        skills = {"skills": master.get("skills", [])}

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
    with latest.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def extract_json_from_response(response: str) -> Dict[str, Any]:
    text = response.strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        data = json.loads(fenced.group(1))
        if isinstance(data, dict):
            return data

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        data = json.loads(text[start:end + 1])
        if isinstance(data, dict):
            return data

    print("\nJSON extraction failed. First 2000 chars of response:")
    print(response[:2000])
    raise ValueError("Could not extract valid JSON object from LLM response")


def require_keys(obj: Dict[str, Any], required: set[str], context: str) -> None:
    missing = sorted(required - set(obj.keys()))
    if missing:
        raise ValueError(f"{context} missing required keys: {missing}")


def sanitize_summary_style(summary: str, positioning_angle: str) -> str:
    """Best-effort cleanup: remove first-person language from summary body."""
    if not isinstance(summary, str):
        return summary

    required_start = f"{positioning_angle}."
    if not summary.startswith(required_start):
        return summary

    prefix = required_start
    body = summary[len(prefix):]
    body = re.sub(r"\bI am\b", "This candidate is", body, flags=re.IGNORECASE)
    body = re.sub(r"\bI'm\b", "This candidate is", body, flags=re.IGNORECASE)
    body = re.sub(r"\bI have\b", "Has", body, flags=re.IGNORECASE)
    body = re.sub(r"\bI led\b", "Led", body, flags=re.IGNORECASE)
    body = re.sub(r"\bI built\b", "Built", body, flags=re.IGNORECASE)
    body = re.sub(r"\bI designed\b", "Designed", body, flags=re.IGNORECASE)
    body = re.sub(r"\bmy\b", "the candidate's", body, flags=re.IGNORECASE)
    body = re.sub(r"\bme\b", "the candidate", body, flags=re.IGNORECASE)
    body = re.sub(r"\bI\b", "the candidate", body, flags=re.IGNORECASE)
    for verb in [
        "excel", "specialize", "focus", "build", "design", "lead", "drive",
        "deliver", "develop", "manage", "architect", "optimize", "support",
        "enable", "leverage", "collaborate",
    ]:
        body = re.sub(
            rf"\bthe candidate {verb}\b",
            f"the candidate {verb}s",
            body,
            flags=re.IGNORECASE,
        )
    body = re.sub(r"\s{2,}", " ", body).strip()
    return f"{prefix} {body}" if body else prefix


def validate_resume_schema(data: Dict[str, Any], positioning_angle: str) -> Dict[str, Any]:
    require_keys(data, REQUIRED_TOP_LEVEL_KEYS, "resume root")

    extra_top = sorted(set(data.keys()) - REQUIRED_TOP_LEVEL_KEYS)
    if extra_top:
        raise ValueError(f"resume root has extra top-level keys: {extra_top}")

    if not isinstance(data["personal"], dict):
        raise ValueError("personal must be an object")
    require_keys(data["personal"], REQUIRED_PERSONAL_KEYS, "personal")

    if "name" in data["personal"]:
        raise ValueError("Invalid key personal.name. Use personal.full_name.")

    summary = data.get("summary", "")
    if not isinstance(summary, str):
        raise ValueError("summary must be a string")

    required_start = f"{positioning_angle}."
    if not summary.startswith(required_start):
        raise ValueError(
            "summary must start exactly with POSITIONING_ANGLE. "
            f"Expected start: {required_start!r}. Got: {summary[:120]!r}"
        )

    forbidden_summary_phrases = [
        "cloud infrastructure, and performance engineering",
        "enterprise IT experience spanning data engineering",
        "AWS ML Data Engineer",
    ]
    for phrase in forbidden_summary_phrases:
        if phrase in summary:
            raise ValueError(f"summary contains forbidden generic/drift phrase: {phrase!r}")

    summary_body = summary[len(required_start):]
    if FIRST_PERSON_PATTERN.search(summary_body):
        raise ValueError("summary must be third-person and must not use first-person pronouns (I/my/me)")

    if not isinstance(data["experience"], list):
        raise ValueError("experience must be a list")
    for idx, exp in enumerate(data["experience"]):
        if not isinstance(exp, dict):
            raise ValueError(f"experience[{idx}] must be an object")
        require_keys(exp, REQUIRED_EXPERIENCE_KEYS, f"experience[{idx}]")
        forbidden = {"role", "dates", "highlights"}
        present_forbidden = sorted(forbidden.intersection(exp.keys()))
        if present_forbidden:
            raise ValueError(f"experience[{idx}] has forbidden keys: {present_forbidden}")
        if not isinstance(exp.get("bullets"), list):
            raise ValueError(f"experience[{idx}].bullets must be a list")

    if not isinstance(data["education"], list):
        raise ValueError("education must be a list")
    for idx, edu in enumerate(data["education"]):
        if not isinstance(edu, dict):
            raise ValueError(f"education[{idx}] must be an object")
        require_keys(edu, REQUIRED_EDUCATION_KEYS, f"education[{idx}]")

    if not isinstance(data["skills"], dict):
        raise ValueError("skills must be an object, not a list")
    require_keys(data["skills"], REQUIRED_SKILL_KEYS, "skills")
    for key in REQUIRED_SKILL_KEYS:
        if not isinstance(data["skills"].get(key), str):
            raise ValueError(f"skills.{key} must be a comma-separated string")

    if not isinstance(data["projects"], list):
        raise ValueError("projects must be a list")
    for idx, project in enumerate(data["projects"]):
        if not isinstance(project, dict):
            raise ValueError(f"projects[{idx}] must be an object")
        require_keys(project, {"name", "description", "technologies"}, f"projects[{idx}]")
        if not isinstance(project.get("technologies"), list):
            raise ValueError(f"projects[{idx}].technologies must be a list")

    return data


def call_llm(prompt: str, positioning_angle: str, model: str = "grok-3") -> Dict[str, Any]:
    if GrokClient is None:
        print("Mock mode: returning dummy resume JSON")
        return validate_resume_schema(
            {
                "personal": {
                    "full_name": "Sean Luka Girgis",
                    "phone": "214-315-2190",
                    "email": "seanlgirgis@gmail.com",
                    "linkedin": "",
                    "github": "",
                    "personal_website": "",
                    "preferred_title": "Senior Data Engineer",
                },
                "summary": f"{positioning_angle}. Senior Data Engineer with AWS, Python, PySpark, ETL, and ML-enabled forecasting experience.",
                "experience": [
                    {
                        "company": "CITI",
                        "title": "Senior Capacity & Data Engineer",
                        "start_date": "2017-11",
                        "end_date": "2025-12",
                        "bullets": ["Built ETL pipelines using Python and AWS."]
                    }
                ],
                "education": [
                    {"degree": "", "institution": "", "location": "", "dates": ""}
                ],
                "skills": {
                    "Languages": "Python, SQL",
                    "Cloud & Data": "AWS, S3, Glue, Redshift",
                    "AI/ML": "scikit-learn, Prophet",
                    "Tools & Infra": "Docker, Airflow",
                    "Legacy": "Oracle"
                },
                "projects": [
                    {"name": "HorizonScale", "description": "ML forecasting engine.", "technologies": ["Python"]}
                ]
            },
            positioning_angle,
        )

    grok = GrokClient(model=model)
    print(f"Calling Grok ({model}) for resume tailoring...")
    response = grok.chat([{"role": "user", "content": prompt}], max_tokens=4096, temperature=0.0)
    parsed = extract_json_from_response(response)
    if isinstance(parsed, dict) and isinstance(parsed.get("summary"), str):
        parsed["summary"] = sanitize_summary_style(parsed["summary"], positioning_angle)
    return validate_resume_schema(parsed, positioning_angle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 4: Generate tailored resume intermediate JSON")
    parser.add_argument("--uuid", required=True, help="Job UUID or short prefix")
    parser.add_argument("--version", default="v1", help="Output version tag (e.g. v1-postscript)")
    parser.add_argument("--model", default="grok-3", help="Grok model to use")
    parser.add_argument(
        "--angle",
        default=DEFAULT_POSITIONING_ANGLE,
        help="Exact POSITIONING_ANGLE. Summary must start with this exact text.",
    )
    args = parser.parse_args()

    positioning_angle = args.angle.strip() or DEFAULT_POSITIONING_ANGLE

    job_folder = resolve_job_folder(args.uuid)
    print(f"Processing job: {job_folder.name}")
    print(f"POSITIONING_ANGLE: {positioning_angle}")

    generated_dir = job_folder / "generated"
    generated_dir.mkdir(exist_ok=True)

    out_path = generated_dir / f"resume_intermediate_{args.version}.json"
    if out_path.exists():
        print(f"\nWarning: {out_path} already exists.")
        if input("Overwrite? [y/N] ").strip().lower() != "y":
            print("Aborted.")
            sys.exit(0)

    try:
        master_career, master_skills = load_master()
        job_data = load_latest_tailored_job(job_folder)
    except Exception as e:
        print(f"Error loading input data: {e}")
        sys.exit(1)

    prompt = (
        RESUME_PROMPT_TEMPLATE
        .replace("{career_json}", json.dumps(master_career, separators=(",", ":"), ensure_ascii=False))
        .replace("{skills_json}", json.dumps(master_skills, separators=(",", ":"), ensure_ascii=False))
        .replace("{job_yaml}", yaml.dump(job_data, sort_keys=False, allow_unicode=True))
        .replace("{positioning_angle}", positioning_angle)
    )

    print("Generating tailored resume intermediate JSON...")
    try:
        tailored_resume = call_llm(prompt, positioning_angle, args.model)
    except Exception as e:
        print(f"LLM / parsing / validation failed: {e}")
        sys.exit(1)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(tailored_resume, f, indent=2, ensure_ascii=False)

    print(f"\nSuccess! Intermediate resume saved → {out_path}")

    print("\nNext steps:")
    print("1. Review and manually tweak the JSON if needed")
    print("2. Proceed to rendering:")
    print(f"   python scripts/05_render_resume.py --uuid {args.uuid} --version {args.version} [--format pdf] [--trim]")


if __name__ == "__main__":
    main()
