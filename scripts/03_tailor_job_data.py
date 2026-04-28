#!/usr/bin/env python3
"""
scripts/03_tailor_job_data.py

Phase 3:
After scoring and accepting a job, tailor / structure / enrich the raw job posting
into a strict tailored_data_<version>.yaml artifact for downstream resume and cover generation.

Fixed/hardened version:
- Enforces exact tailored_data schema
- Removes non-schema keys such as tailoring_method, llm_model, llm_version, sections, llm_error
- Validates LLM YAML before saving
- Normalizes fallback output to the same schema
- Uses strict prompt language to prevent extra fields
- Preserves known metadata when available

Usage:
    python scripts/03_tailor_job_data.py --uuid <uuid-or-prefix> [--version v1]
    [--model grok-3] [--temperature 0.0] [--no-llm] [--raw-file path]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from src.ai.grok_client import GrokClient

JOB_ROOT = Path("data/jobs")

TAILORED_SCHEMA_KEYS = [
    "company_name",
    "company_website",
    "job_title",
    "location",
    "extracted_skills",
    "job_summary",
    "responsibilities",
    "requirements",
    "preferred",
    "benefits",
    "must_have_skills",
    "nice_to_have_skills",
    "ats_keywords",
]

LIST_KEYS = {
    "extracted_skills",
    "responsibilities",
    "requirements",
    "preferred",
    "benefits",
    "must_have_skills",
    "nice_to_have_skills",
    "ats_keywords",
}

STRING_KEYS = {
    "company_name",
    "company_website",
    "job_title",
    "location",
    "job_summary",
}

SECTION_MARKERS = {
    "responsibilities": [r"(?i)(responsibilit(y|ies)|what you'll do|key duties|you will|day[- ]?to[- ]?day)"],
    "requirements": [r"(?i)(require(ments|d)|qualifications|must have|minimum)"],
    "preferred": [r"(?i)(preferred|nice to have|bonus|desired|plus)"],
    "benefits": [r"(?i)(benefit|perks|compensation|remote|hybrid)"],
}

SKILL_PATTERNS = [
    r"(?i)(python|java|javascript|typescript|go|rust|c\+\+|sql|aws|gcp|azure|docker|kubernetes|terraform|git|linux|mysql|postgresql|mongodb|redis|elasticsearch|opensearch|kafka|kinesis|spark|pyspark|hadoop|hive|glue|redshift|athena|s3|lambda|emr|airflow|databricks|snowflake|dbt|tableau|powerbi|ci/cd|devops|api|rest|machine learning|ml|ai|scikit-learn|tensorflow|pytorch|data lake|data warehouse|data warehousing|etl|elt|orchestration|data governance|dimensional modeling|parquet)"
]


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences_or_lines(text: str, max_items: int = 8) -> list[str]:
    if not text:
        return []
    parts = re.split(r"(?:\n+|•|- |\* |\.\s+)", text)
    cleaned = [p.strip(" -•\t\r\n.") for p in parts if p and p.strip(" -•\t\r\n.")]
    return cleaned[:max_items]


def extract_section(text: str, section_key: str) -> list[str]:
    markers = SECTION_MARKERS.get(section_key, [])
    if not markers:
        return []
    pattern = "|".join(markers)
    match = re.search(pattern, text)
    if not match:
        return []
    start = match.end()
    next_match = re.search(pattern, text[start:])
    end = start + next_match.start() if next_match else len(text)
    return split_sentences_or_lines(text[start:end].strip())


def extract_skills(text: str) -> list[str]:
    skills: set[str] = set()
    for pattern in SKILL_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            skill = str(match).strip()
            if skill:
                skills.add(skill)
    return sorted(skills, key=str.lower)


def normalize_string(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        blocked = {"unknown", "n/a", "na", "tbd", "your name", "para text"}
        cleaned = value.strip()
        if cleaned.lower() in blocked:
            return ""
        return cleaned
    return str(value).strip()


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        result = []
        for item in value:
            if isinstance(item, dict):
                text = " ".join(str(v).strip() for v in item.values() if str(v).strip())
            else:
                text = str(item).strip()
            if text and text.lower() not in {"unknown", "n/a", "na", "tbd", "your name", "para text"}:
                result.append(text)
        return result
    if isinstance(value, str):
        return split_sentences_or_lines(value)
    return [str(value).strip()] if str(value).strip() else []


def empty_tailored_data() -> dict[str, Any]:
    return {
        "company_name": "",
        "company_website": "",
        "job_title": "",
        "location": "",
        "extracted_skills": [],
        "job_summary": "",
        "responsibilities": [],
        "requirements": [],
        "preferred": [],
        "benefits": [],
        "must_have_skills": [],
        "nice_to_have_skills": [],
        "ats_keywords": [],
    }


def normalize_tailored_data(data: dict[str, Any], known_metadata: dict[str, str]) -> dict[str, Any]:
    normalized = empty_tailored_data()

    aliases = {
        "company_name": ["company_name", "company", "Company Name"],
        "company_website": ["company_website", "Company_website", "website", "url"],
        "job_title": ["job_title", "title", "role"],
        "location": ["location", "job_location"],
        "extracted_skills": ["extracted_skills", "skills", "technologies"],
        "job_summary": ["job_summary", "summary", "role_summary"],
        "responsibilities": ["responsibilities", "duties"],
        "requirements": ["requirements", "required", "minimum_qualifications"],
        "preferred": ["preferred", "nice_to_have", "preferred_qualifications"],
        "benefits": ["benefits", "perks"],
        "must_have_skills": ["must_have_skills", "must_haves", "required_skills"],
        "nice_to_have_skills": ["nice_to_have_skills", "nice_to_haves", "preferred_skills"],
        "ats_keywords": ["ats_keywords", "keywords"],
    }

    for target_key, possible_keys in aliases.items():
        for key in possible_keys:
            if key in data:
                if target_key in LIST_KEYS:
                    normalized[target_key] = normalize_list(data.get(key))
                else:
                    normalized[target_key] = normalize_string(data.get(key))
                break

    if not normalized["company_name"]:
        normalized["company_name"] = known_metadata.get("company_name", "")
    if not normalized["company_website"]:
        normalized["company_website"] = known_metadata.get("company_website", "")
    if not normalized["job_title"]:
        normalized["job_title"] = known_metadata.get("job_title", "")
    if not normalized["location"]:
        normalized["location"] = known_metadata.get("location", "")

    return normalized


def validate_tailored_data(data: dict[str, Any]) -> dict[str, Any]:
    keys = set(data.keys())
    required = set(TAILORED_SCHEMA_KEYS)

    missing = sorted(required - keys)
    if missing:
        raise ValueError(f"tailored_data missing required keys: {missing}")

    extra = sorted(keys - required)
    if extra:
        raise ValueError(f"tailored_data has extra top-level keys: {extra}")

    for key in STRING_KEYS:
        if not isinstance(data[key], str):
            raise ValueError(f"{key} must be a string")

    for key in LIST_KEYS:
        if not isinstance(data[key], list):
            raise ValueError(f"{key} must be a list")
        for idx, item in enumerate(data[key]):
            if not isinstance(item, str):
                raise ValueError(f"{key}[{idx}] must be a string")

    forbidden_tokens = {"Unknown", "N/A", "TBD", "Your Name", "Para text"}
    for key in STRING_KEYS:
        if data[key] in forbidden_tokens:
            raise ValueError(f"{key} contains forbidden placeholder: {data[key]!r}")

    return data


def build_naive_tailored_data(cleaned: str, known_metadata: dict[str, str]) -> dict[str, Any]:
    skills = extract_skills(cleaned)
    responsibilities = extract_section(cleaned, "responsibilities")
    requirements = extract_section(cleaned, "requirements")
    preferred = extract_section(cleaned, "preferred")
    benefits = extract_section(cleaned, "benefits")

    data = {
        "company_name": known_metadata.get("company_name", ""),
        "company_website": known_metadata.get("company_website", ""),
        "job_title": known_metadata.get("job_title", ""),
        "location": known_metadata.get("location", ""),
        "extracted_skills": skills,
        "job_summary": cleaned[:500],
        "responsibilities": responsibilities,
        "requirements": requirements,
        "preferred": preferred,
        "benefits": benefits,
        "must_have_skills": skills[:12],
        "nice_to_have_skills": [],
        "ats_keywords": skills,
    }
    return validate_tailored_data(data)


def build_tailoring_prompt(
    job_text: str,
    known_company: str = "",
    known_website: str = "",
    known_title: str = "",
    known_location: str = "",
) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are a STRICT job-posting extraction engine. "
                "Return ONLY valid YAML. No markdown. No code fences. No commentary. "
                "Your output is consumed by a parser and must match the requested schema exactly."
            ),
        },
        {
            "role": "user",
            "content": f"""Known metadata. Use these unless the job posting clearly contradicts them:
company_name: {known_company}
company_website: {known_website}
job_title: {known_title}
location: {known_location}

STRICT OUTPUT RULES:
- Output EXACTLY the top-level keys listed below.
- Do NOT add any extra top-level keys.
- Do NOT output tailoring_method, llm_model, llm_version, sections, notes, confidence, or explanations.
- Use "" for missing strings.
- Use [] for missing lists.
- Never use placeholders: Unknown, N/A, TBD, Your Name, Para text.
- Extract job facts only from the job posting and known metadata.
- Do NOT include candidate facts.
- extracted_skills, must_have_skills, nice_to_have_skills, and ats_keywords must be lists of strings.

Required YAML schema:

company_name: ""
company_website: ""
job_title: ""
location: ""
extracted_skills: []
job_summary: ""
responsibilities: []
requirements: []
preferred: []
benefits: []
must_have_skills: []
nice_to_have_skills: []
ats_keywords: []

Job posting:
{job_text}
""",
        },
    ]


def resolve_job_folder(uuid_str: str) -> Path:
    uuid_str = uuid_str.strip()
    job_dir = JOB_ROOT / uuid_str
    if job_dir.is_dir():
        return job_dir

    candidates = list(JOB_ROOT.glob(f"*_{uuid_str}*"))
    if not candidates:
        short_prefix = uuid_str[:8]
        candidates = list(JOB_ROOT.glob(f"*_{short_prefix}*"))

    if len(candidates) == 1:
        print(f"Resolved UUID/prefix → using folder: {candidates[0].name}")
        return candidates[0]

    if len(candidates) > 1:
        print("Ambiguous UUID — multiple matching folders:")
        for c in candidates:
            print(f"  - {c.name}")
        raise ValueError(f"Ambiguous UUID prefix: {uuid_str}")

    raise ValueError(
        f"Job folder not found for UUID '{uuid_str}'\n"
        f"Looked for data/jobs/{uuid_str}, data/jobs/*_{uuid_str}*, data/jobs/*_{uuid_str[:8]}*"
    )


def load_known_metadata(job_dir: Path) -> dict[str, str]:
    meta_path = job_dir / "metadata.yaml"
    known = {
        "company_name": "",
        "company_website": "",
        "job_title": "",
        "location": "",
    }

    if not meta_path.is_file():
        return known

    try:
        with meta_path.open("r", encoding="utf-8") as f:
            meta = yaml.safe_load(f) or {}
        known["company_name"] = normalize_string(meta.get("company", ""))
        known["company_website"] = normalize_string(meta.get("company_website", ""))
        known["job_title"] = normalize_string(meta.get("role", ""))
        known["location"] = normalize_string(meta.get("location", ""))
        print(f"Loaded known metadata → Company: {known['company_name']}, Website: {known['company_website']}")
    except Exception as exc:
        print(f"Warning: Could not load metadata.yaml → {exc}")

    return known


def find_raw_job_path(job_dir: Path, raw_file: Optional[str]) -> Path:
    if raw_file:
        raw_path = Path(raw_file)
        if raw_path.is_file():
            return raw_path
        raise FileNotFoundError(f"Raw file not found: {raw_path}")

    candidates = [
        job_dir / "raw" / "job_description.md",
        job_dir / "raw" / "raw_intake.md",
        job_dir / "intake.md",
        job_dir / "raw_intake.md",
    ]

    for path in candidates:
        if path.is_file():
            return path

    raise FileNotFoundError(
        f"No raw job description found for {job_dir}. Tried: "
        + ", ".join(str(p) for p in candidates)
    )


def extract_yaml_from_response(response: str) -> dict[str, Any]:
    text = response.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:yaml|yml)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    yaml_start = text.find("company_name:")
    if yaml_start > 0:
        text = text[yaml_start:]

    parsed = yaml.safe_load(text)
    if not isinstance(parsed, dict):
        raise ValueError("LLM response did not parse to a YAML dict")
    return parsed


def tailor_job(
    uuid: str,
    version: str = "v1",
    raw_file: Optional[str] = None,
    model: str = "grok-3",
    temperature: float = 0.0,
    no_llm: bool = False,
) -> None:
    job_dir = resolve_job_folder(uuid)
    print(f"Processing job folder: {job_dir.name}")

    known_metadata = load_known_metadata(job_dir)

    raw_path = find_raw_job_path(job_dir, raw_file)
    print(f"Reading raw job from: {raw_path}")

    raw_text = raw_path.read_text(encoding="utf-8")
    cleaned = clean_text(raw_text)

    if no_llm:
        print("Using naive regex extraction (no LLM)")
        tailored_data = build_naive_tailored_data(cleaned, known_metadata)
    else:
        print(f"Using LLM tailoring (model={model}, temp={temperature})")
        messages = build_tailoring_prompt(
            raw_text,
            known_company=known_metadata["company_name"],
            known_website=known_metadata["company_website"],
            known_title=known_metadata["job_title"],
            known_location=known_metadata["location"],
        )

        try:
            grok = GrokClient(model=model)
            response = grok.chat(
                messages=messages,
                temperature=temperature,
                max_tokens=4000,
            )
            llm_data = extract_yaml_from_response(response)
            normalized = normalize_tailored_data(llm_data, known_metadata)
            tailored_data = validate_tailored_data(normalized)
            print("LLM tailoring successful and schema-valid")
        except Exception as exc:
            print(f"LLM tailoring failed validation: {exc} — falling back to schema-valid naive extraction")
            tailored_data = build_naive_tailored_data(cleaned, known_metadata)

    tailored_dir = job_dir / "tailored"
    tailored_dir.mkdir(exist_ok=True)
    out_file = tailored_dir / f"tailored_data_{version}.yaml"

    with out_file.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            tailored_data,
            f,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        )

    print(f"Tailored data saved: {out_file}")
    skills = tailored_data.get("extracted_skills", [])
    print(f"Extracted/Detected skills ({len(skills)}): {', '.join(skills[:15])}{' ...' if len(skills) > 15 else ''}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tailor job data for accepted jobs (LLM + schema-valid fallback)")
    parser.add_argument("--uuid", required=True, help="Job UUID or short prefix (e.g. cdb9a3fa)")
    parser.add_argument("--version", default="v1", help="Tailored version tag (v1, llm-v1, etc.)")
    parser.add_argument("--raw-file", default=None, help="Override raw job file path")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    parser.add_argument("--temperature", type=float, default=0.0, help="LLM temperature (0.0 = deterministic)")
    parser.add_argument("--no-llm", action="store_true", help="Force naive regex mode (no LLM)")
    args = parser.parse_args()

    tailor_job(
        uuid=args.uuid,
        version=args.version,
        raw_file=args.raw_file,
        model=args.model,
        temperature=args.temperature,
        no_llm=args.no_llm,
    )


if __name__ == "__main__":
    main()
