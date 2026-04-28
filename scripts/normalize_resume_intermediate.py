#!/usr/bin/env python3
"""
Normalize common LLM resume-intermediate variants into renderer schema.

Input (default):
  data/jobs/<job_id>/generated/resume_intermediate_v1.json

Output (default):
  data/jobs/<job_id>/generated/resume_intermediate_v1_normalized.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

JOB_ROOT = Path("data/jobs")
GROUP_KEYS = ["Languages", "Cloud & Data", "AI/ML", "Tools & Infra", "Legacy"]


class NormalizationError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize resume intermediate JSON variants.")
    parser.add_argument("--uuid", help="Job UUID or short prefix. Optional when --input is provided.")
    parser.add_argument("--version", default="v1", help="Version tag (default: v1).")
    parser.add_argument("--input", dest="input_path", help="Explicit input JSON path.")
    parser.add_argument("--output", dest="output_path", help="Explicit output JSON path.")
    return parser.parse_args()


def resolve_job_folder(uuid_str: str) -> Path:
    ref = uuid_str.strip()
    job_dir = JOB_ROOT / ref
    if job_dir.is_dir():
        return job_dir

    candidates = list(JOB_ROOT.glob(f"*_{ref}*"))
    if not candidates:
        short = ref[:8]
        candidates = list(JOB_ROOT.glob(f"*_{short}*"))

    if len(candidates) == 1:
        print(f"Resolved -> {candidates[0].name}")
        return candidates[0]
    if len(candidates) > 1:
        raise NormalizationError(f"Ambiguous UUID reference: {uuid_str}")
    raise NormalizationError(f"Job folder not found for '{uuid_str}'")


def ensure_paths(args: argparse.Namespace) -> Tuple[Path, Path]:
    if args.input_path:
        input_path = Path(args.input_path)
        output_path = Path(args.output_path) if args.output_path else input_path.with_name(f"{input_path.stem}_normalized.json")
        return input_path, output_path

    if not args.uuid:
        raise NormalizationError("Provide --uuid or --input.")

    job_dir = resolve_job_folder(args.uuid)
    generated = job_dir / "generated"
    input_path = generated / f"resume_intermediate_{args.version}.json"
    output_path = Path(args.output_path) if args.output_path else generated / f"resume_intermediate_{args.version}_normalized.json"
    return input_path, output_path


def as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def first_key(mapping: Dict[str, Any], keys: Iterable[str]) -> Tuple[str, Any]:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return key, mapping[key]
    return "", None


def add_warning(warnings: List[str], message: str) -> None:
    warnings.append(message)


def split_text_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: List[str] = []
        for item in value:
            if isinstance(item, dict):
                # Keep dict content only if there's a "text"-like key.
                key, mapped = first_key(item, ("text", "value", "description", "summary"))
                if mapped:
                    out.append(as_str(mapped))
            else:
                txt = as_str(item)
                if txt:
                    out.append(txt)
        return out
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return []
        parts = re.split(r"\n+|;\s*|•\s*|- ", raw)
        cleaned = [p.strip() for p in parts if p and p.strip()]
        if cleaned:
            return cleaned
        return [raw]
    return [as_str(value)] if as_str(value) else []


def split_dates(date_text: str) -> Tuple[str, str]:
    text = as_str(date_text)
    if not text:
        return "", ""

    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("—", "-").replace("–", "-")

    # "2017-11 - 2025-12", "Jan 2020 to Present", etc.
    match = re.match(r"^(.*?)\s*(?:to|through|thru|-|->)\s*(.*?)$", text, flags=re.IGNORECASE)
    if match:
        start = as_str(match.group(1))
        end = as_str(match.group(2))
        return start, end

    # Single-date fallback: copy to both to preserve renderer-required fields.
    return text, text


def normalize_personal(src: Any, warnings: List[str]) -> Dict[str, str]:
    data = src if isinstance(src, dict) else {}
    out: Dict[str, str] = {
        "full_name": "",
        "phone": "",
        "email": "",
        "linkedin": "",
        "github": "",
        "personal_website": "",
        "preferred_title": "",
    }

    aliases = {
        "full_name": ("full_name", "name"),
        "phone": ("phone", "mobile", "telephone"),
        "email": ("email", "mail"),
        "linkedin": ("linkedin", "linkedin_url"),
        "github": ("github", "github_url"),
        "personal_website": ("personal_website", "portfolio", "website", "url"),
        "preferred_title": ("preferred_title", "title", "headline"),
    }

    for target, keys in aliases.items():
        used_key, raw_value = first_key(data, keys)
        if raw_value is not None:
            out[target] = as_str(raw_value)
            if used_key and used_key != target:
                add_warning(warnings, f"Mapped personal.{used_key} -> personal.{target}")

    if not out["full_name"]:
        raise NormalizationError("Missing required field after normalization: personal.full_name")
    return out


def normalize_experience(src: Any, warnings: List[str]) -> List[Dict[str, Any]]:
    raw_list = src if isinstance(src, list) else []
    normalized: List[Dict[str, Any]] = []

    for idx, item in enumerate(raw_list):
        if not isinstance(item, dict):
            add_warning(warnings, f"Skipped experience[{idx}] because it is not an object.")
            continue

        exp: Dict[str, Any] = {}

        company_key, company_val = first_key(item, ("company", "employer", "organization", "org"))
        title_key, title_val = first_key(item, ("title", "role", "position"))
        start_key, start_val = first_key(item, ("start_date", "start", "from"))
        end_key, end_val = first_key(item, ("end_date", "end", "to"))
        dates_key, dates_val = first_key(item, ("dates", "date_range", "duration"))
        bullets_key, bullets_val = first_key(item, ("bullets", "highlights", "accomplishments", "responsibilities"))

        exp["company"] = as_str(company_val)
        exp["title"] = as_str(title_val)
        start_date = as_str(start_val)
        end_date = as_str(end_val)

        if (not start_date or not end_date) and dates_val is not None:
            parsed_start, parsed_end = split_dates(as_str(dates_val))
            if not start_date:
                start_date = parsed_start
            if not end_date:
                end_date = parsed_end
            add_warning(warnings, f"Mapped experience[{idx}].{dates_key} -> start_date/end_date")

        exp["start_date"] = start_date
        exp["end_date"] = end_date

        bullets = split_text_list(bullets_val)
        if not bullets:
            desc_key, desc_val = first_key(item, ("description", "summary"))
            if desc_val is not None:
                bullets = split_text_list(desc_val)
                if bullets:
                    add_warning(warnings, f"Mapped experience[{idx}].{desc_key} -> bullets")
        exp["bullets"] = bullets

        if company_key and company_key != "company":
            add_warning(warnings, f"Mapped experience[{idx}].{company_key} -> company")
        if title_key and title_key != "title":
            add_warning(warnings, f"Mapped experience[{idx}].{title_key} -> title")
        if bullets_key and bullets_key != "bullets":
            add_warning(warnings, f"Mapped experience[{idx}].{bullets_key} -> bullets")
        if start_key and start_key != "start_date":
            add_warning(warnings, f"Mapped experience[{idx}].{start_key} -> start_date")
        if end_key and end_key != "end_date":
            add_warning(warnings, f"Mapped experience[{idx}].{end_key} -> end_date")

        if not exp["company"] or not exp["title"] or not exp["start_date"] or not exp["end_date"] or not exp["bullets"]:
            add_warning(warnings, f"Skipped experience[{idx}] due to missing renderer-required fields.")
            continue

        normalized.append(exp)

    if not normalized:
        raise NormalizationError("No valid experience entries after normalization.")
    return normalized


def normalize_education(src: Any, warnings: List[str]) -> List[Dict[str, str]]:
    raw_list = src if isinstance(src, list) else []
    out: List[Dict[str, str]] = []
    for idx, item in enumerate(raw_list):
        if not isinstance(item, dict):
            continue
        degree_key, degree_val = first_key(item, ("degree", "program", "qualification"))
        inst_key, inst_val = first_key(item, ("institution", "school", "university", "college"))
        location_key, location_val = first_key(item, ("location", "city"))
        dates_key, dates_val = first_key(item, ("dates", "date_range", "duration"))
        start_key, start_val = first_key(item, ("start_date", "start", "from"))
        end_key, end_val = first_key(item, ("end_date", "end", "to"))

        dates = as_str(dates_val)
        if not dates and (start_val is not None or end_val is not None):
            start = as_str(start_val)
            end = as_str(end_val)
            if start or end:
                dates = f"{start} - {end}".strip(" -")
                add_warning(warnings, f"Mapped education[{idx}] start/end -> dates")

        row = {
            "degree": as_str(degree_val),
            "institution": as_str(inst_val),
            "location": as_str(location_val),
            "dates": dates,
        }

        if degree_key and degree_key != "degree":
            add_warning(warnings, f"Mapped education[{idx}].{degree_key} -> degree")
        if inst_key and inst_key != "institution":
            add_warning(warnings, f"Mapped education[{idx}].{inst_key} -> institution")
        if location_key and location_key != "location":
            add_warning(warnings, f"Mapped education[{idx}].{location_key} -> location")
        if dates_key and dates_key != "dates":
            add_warning(warnings, f"Mapped education[{idx}].{dates_key} -> dates")

        if row["degree"] or row["institution"] or row["location"] or row["dates"]:
            out.append(row)
    return out


def classify_skill_group(skill_name: str) -> str:
    s = skill_name.lower()
    lang_keywords = ("python", "sql", "java", "c++", "c#", "javascript", "typescript", "scala", "perl", "ksh", "bash", "go", "rust")
    cloud_keywords = ("aws", "azure", "gcp", "s3", "glue", "redshift", "emr", "athena", "spark", "hadoop", "etl", "elt", "data", "warehouse", "lake", "airflow", "kafka", "kinesis", "parquet")
    ai_keywords = ("ml", "machine learning", "scikit", "prophet", "tensorflow", "pytorch", "llm", "genai", "bedrock")
    tools_keywords = ("docker", "kubernetes", "git", "ci/cd", "devops", "linux", "unix", "streamlit", "appdynamics", "dynatrace", "pytest")

    if any(k in s for k in lang_keywords):
        return "Languages"
    if any(k in s for k in ai_keywords):
        return "AI/ML"
    if any(k in s for k in cloud_keywords):
        return "Cloud & Data"
    if any(k in s for k in tools_keywords):
        return "Tools & Infra"
    return "Legacy"


def normalize_skills(src: Any, warnings: List[str]) -> Dict[str, str]:
    grouped: Dict[str, List[str]] = {k: [] for k in GROUP_KEYS}

    if isinstance(src, dict):
        key_aliases = {
            "Languages": ("Languages", "languages", "programming_languages"),
            "Cloud & Data": ("Cloud & Data", "cloud_data", "cloud_and_data", "data_platform"),
            "AI/ML": ("AI/ML", "ai_ml", "machine_learning"),
            "Tools & Infra": ("Tools & Infra", "tools_infra", "tools_and_infra"),
            "Legacy": ("Legacy", "legacy", "other"),
        }
        for target, aliases in key_aliases.items():
            used, val = first_key(src, aliases)
            if val is None:
                continue
            if isinstance(val, list):
                grouped[target].extend([x for x in split_text_list(val) if x])
            else:
                text = as_str(val)
                if text:
                    if "|" in text:
                        grouped[target].extend([x.strip() for x in text.split("|") if x.strip()])
                    else:
                        grouped[target].append(text)
            if used and used != target:
                add_warning(warnings, f"Mapped skills.{used} -> skills.{target}")
    else:
        raw_list: List[str] = []
        if isinstance(src, list):
            for item in src:
                if isinstance(item, dict):
                    _, val = first_key(item, ("name", "skill", "value"))
                    if val is not None:
                        raw_list.extend(split_text_list(val))
                else:
                    raw_list.extend(split_text_list(item))
        elif isinstance(src, str):
            raw_list.extend([x.strip() for x in re.split(r"[,\|]", src) if x.strip()])
        elif src is not None:
            raw_list.append(as_str(src))

        if raw_list:
            add_warning(warnings, "Mapped skills list/string -> grouped skills dict")
        for skill in raw_list:
            group = classify_skill_group(skill)
            grouped[group].append(skill)

    # De-dup and stringify with pipes.
    result: Dict[str, str] = {}
    for group in GROUP_KEYS:
        deduped = list(dict.fromkeys([x for x in grouped[group] if x]))
        result[group] = " | ".join(deduped)
    return result


def normalize_projects(src: Any, warnings: List[str]) -> List[Dict[str, Any]]:
    raw_list = src if isinstance(src, list) else []
    out: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_list):
        if not isinstance(item, dict):
            continue
        name_key, name_val = first_key(item, ("name", "title", "project_name"))
        desc_key, desc_val = first_key(item, ("description", "summary", "details"))
        tech_key, tech_val = first_key(item, ("technologies", "tech_stack", "stack", "tools"))
        repo_key, repo_val = first_key(item, ("repo", "url", "github"))

        technologies = split_text_list(tech_val)
        row: Dict[str, Any] = {
            "name": as_str(name_val),
            "description": as_str(desc_val),
            "technologies": technologies,
        }
        repo = as_str(repo_val)
        if repo:
            row["repo"] = repo

        if name_key and name_key != "name":
            add_warning(warnings, f"Mapped projects[{idx}].{name_key} -> name")
        if desc_key and desc_key != "description":
            add_warning(warnings, f"Mapped projects[{idx}].{desc_key} -> description")
        if tech_key and tech_key != "technologies":
            add_warning(warnings, f"Mapped projects[{idx}].{tech_key} -> technologies")
        if repo_key and repo_key != "repo":
            add_warning(warnings, f"Mapped projects[{idx}].{repo_key} -> repo")

        if row["name"] or row["description"] or row["technologies"]:
            out.append(row)
    return out


def normalize_payload(raw: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    warnings: List[str] = []

    if not isinstance(raw, dict):
        raise NormalizationError("Input JSON must be an object.")

    personal_raw = raw.get("personal", {})
    summary_raw = raw.get("summary", raw.get("professional_summary", ""))
    experience_raw = raw.get("experience", raw.get("experiences", []))
    education_raw = raw.get("education", raw.get("educations", []))
    skills_raw = raw.get("skills", raw.get("skill_set", []))
    projects_raw = raw.get("projects", raw.get("flagship_projects", []))

    if "experiences" in raw and "experience" not in raw:
        add_warning(warnings, "Mapped top-level experiences -> experience")
    if "professional_summary" in raw and "summary" not in raw:
        add_warning(warnings, "Mapped top-level professional_summary -> summary")
    if "flagship_projects" in raw and "projects" not in raw:
        add_warning(warnings, "Mapped top-level flagship_projects -> projects")

    normalized = {
        "personal": normalize_personal(personal_raw, warnings),
        "summary": as_str(summary_raw),
        "experience": normalize_experience(experience_raw, warnings),
        "education": normalize_education(education_raw, warnings),
        "skills": normalize_skills(skills_raw, warnings),
        "projects": normalize_projects(projects_raw, warnings),
    }

    # Validate top-level schema exactly.
    expected = {"personal", "summary", "experience", "education", "skills", "projects"}
    missing = sorted(expected - set(normalized.keys()))
    if missing:
        raise NormalizationError(f"Missing required top-level keys after normalization: {', '.join(missing)}")

    # Validate renderer-required fields.
    if not normalized["personal"].get("full_name"):
        raise NormalizationError("Missing renderer-required field: personal.full_name")

    for idx, exp in enumerate(normalized["experience"]):
        for req in ("company", "title", "start_date", "end_date", "bullets"):
            if req not in exp or not exp[req]:
                raise NormalizationError(f"Missing renderer-required field: experience[{idx}].{req}")
        if not isinstance(exp["bullets"], list) or not [b for b in exp["bullets"] if as_str(b)]:
            raise NormalizationError(f"experience[{idx}].bullets must be a non-empty list")

    # Warn about extra top-level keys in original input that were ignored.
    extra_raw = sorted(set(raw.keys()) - expected - {"experiences", "professional_summary", "flagship_projects", "educations", "skill_set"})
    for key in extra_raw:
        add_warning(warnings, f"Ignored extra top-level key: {key}")

    return normalized, warnings


def main() -> None:
    args = parse_args()
    input_path, output_path = ensure_paths(args)

    if not input_path.is_file():
        raise NormalizationError(f"Input file not found: {input_path}")

    raw_data = json.loads(input_path.read_text(encoding="utf-8"))
    normalized, warnings = normalize_payload(raw_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== RESUME NORMALIZATION ===")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"- {w}")
    else:
        print("Warnings: none")
    print("Result: PASSED")


if __name__ == "__main__":
    try:
        main()
    except NormalizationError as exc:
        print(f"Result: FAILED\nReason: {exc}")
        sys.exit(1)
    except Exception as exc:  # Defensive catch with clear failure output.
        print(f"Result: FAILED\nReason: {exc.__class__.__name__}: {exc}")
        sys.exit(1)

