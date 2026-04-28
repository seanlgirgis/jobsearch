#!/usr/bin/env python3
"""
Validate manual ChatGPT artifacts before rendering documents.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml

JOB_ROOT = Path("data/jobs")
BAD_TOKENS = ("unknown", "n/a", "tbd", "your name", "para text", "mock intro")

YAML_REQUIRED_KEYS = {
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
}

RESUME_REQUIRED_KEYS = {
    "personal",
    "summary",
    "experience",
    "education",
    "skills",
    "projects",
}

COVER_REQUIRED_KEYS = {
    "header",
    "salutation",
    "intro",
    "body",
    "conclusion",
    "sign_off",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate manual-v2 artifacts.")
    parser.add_argument("--uuid", required=True, help="Job UUID or prefix.")
    parser.add_argument("--version", default="v1", help="Artifact version tag.")
    parser.add_argument("--skip-cover", action="store_true", help="Skip cover file validation.")
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
        raise ValueError(f"Ambiguous UUID reference: {uuid_str}")
    raise ValueError(f"No job folder found for: {uuid_str}")


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, dict):
        for v in value.values():
            yield from iter_strings(v)
        return
    if isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def find_bad_tokens(value: Any) -> List[str]:
    found = set()
    for text in iter_strings(value):
        lowered = text.strip().lower()
        for token in BAD_TOKENS:
            if token in lowered:
                found.add(token)
    return sorted(found)


def validate_yaml(path: Path) -> List[str]:
    errors: List[str] = []
    if not path.is_file():
        return [f"MISSING: {path}"]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        return [f"YAML_PARSE_ERROR: {exc}"]

    if not isinstance(data, dict):
        return ["YAML_SCHEMA_ERROR: top-level must be a mapping"]

    missing = sorted(YAML_REQUIRED_KEYS - set(data.keys()))
    extra = sorted(set(data.keys()) - YAML_REQUIRED_KEYS)
    if missing:
        errors.append(f"YAML_MISSING_KEYS: {', '.join(missing)}")
    if extra:
        errors.append(f"YAML_EXTRA_KEYS: {', '.join(extra)}")

    bad = find_bad_tokens(data)
    if bad:
        errors.append(f"YAML_BAD_TOKENS: {', '.join(bad)}")
    return errors


def validate_json(path: Path, required_keys: set[str], label: str) -> List[str]:
    errors: List[str] = []
    if not path.is_file():
        return [f"MISSING: {path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{label}_PARSE_ERROR: {exc}"]

    if not isinstance(data, dict):
        return [f"{label}_SCHEMA_ERROR: top-level must be an object"]

    missing = sorted(required_keys - set(data.keys()))
    extra = sorted(set(data.keys()) - required_keys)
    if missing:
        errors.append(f"{label}_MISSING_KEYS: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}_EXTRA_KEYS: {', '.join(extra)}")

    bad = find_bad_tokens(data)
    if bad:
        errors.append(f"{label}_BAD_TOKENS: {', '.join(bad)}")
    return errors


def main() -> None:
    args = parse_args()
    job_dir = resolve_job_folder(args.uuid)

    yaml_path = job_dir / "tailored" / f"tailored_data_{args.version}.yaml"
    resume_path = job_dir / "generated" / f"resume_intermediate_{args.version}.json"
    cover_path = job_dir / "generated" / f"cover_intermediate_{args.version}.json"

    errors: List[str] = []
    errors.extend(validate_yaml(yaml_path))
    errors.extend(validate_json(resume_path, RESUME_REQUIRED_KEYS, "RESUME"))
    if not args.skip_cover:
        errors.extend(validate_json(cover_path, COVER_REQUIRED_KEYS, "COVER"))

    print("=== MANUAL V2 ARTIFACT VALIDATION ===")
    print(f"Job folder: {job_dir}")
    print(f"YAML: {yaml_path}")
    print(f"RESUME JSON: {resume_path}")
    if not args.skip_cover:
        print(f"COVER JSON: {cover_path}")
    else:
        print("COVER JSON: skipped")

    if errors:
        print("RESULT: FAILED")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("RESULT: PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()

