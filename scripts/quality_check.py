#!/usr/bin/env python3
"""
scripts/quality_check.py

Quality gate for the job application pipeline.
Runs after steps 05 and 08 — before the application is recorded (step 09).

Checks:
- Cover letter: no placeholder text (0, Unknown, garbled dates, template strings)
- Cover letter: reasonable word count
- Resume: no placeholder text
- Resume: has required sections (experience, skills)
- Output files: cover.docx and resume.docx actually exist

Usage:
    python scripts/quality_check.py --uuid <uuid>
    python scripts/quality_check.py --uuid <uuid> --strict   # exits 1 on any warning
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

JOB_ROOT = Path("data/jobs")


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
        return candidates[0]
    elif len(candidates) > 1:
        raise ValueError(f"Ambiguous UUID: {uuid_str}")
    else:
        raise ValueError(f"Job folder not found for '{uuid_str}'")


BAD_PATTERNS_COVER = {
    " 0 ":            "Company name rendered as '0'",
    " at 0":          "Company name rendered as '0'",
    "at 0.":          "Company name rendered as '0'",
    "'s focus on 0":  "Company name rendered as '0'",
    "to 0.":          "Company name rendered as '0'",
    "Unknown":        "Company name or field is 'Unknown'",
    "112026":         "Garbled date/position ID in text",
    "position at 0":  "Placeholder not replaced",
    "Your Name":      "Name placeholder not replaced",
    "Para text":      "Template placeholder not replaced",
    "Mock intro":     "Mock/test content in letter",
    "[company]":      "Bracket placeholder not replaced",
    "[role]":         "Bracket placeholder not replaced",
    "[COMPANY]":      "Bracket placeholder not replaced",
}

BAD_PATTERNS_RESUME = {
    "Your Name":      "Name placeholder not replaced",
    "[company]":      "Bracket placeholder in resume",
    "Lorem ipsum":    "Placeholder text in resume",
    "PLACEHOLDER":    "Placeholder text in resume",
}


def check_cover(generated_dir: Path, version: str) -> list:
    issues = []

    # Check JSON intermediate
    json_path = generated_dir / f"cover_intermediate_{version}.json"
    if not json_path.exists():
        issues.append(f"MISSING: cover_intermediate_{version}.json not found")
        return issues

    with open(json_path, "r", encoding="utf-8") as f:
        cover = json.load(f)

    full_text = " ".join([
        cover.get("intro", ""),
        " ".join(cover.get("body", [])),
        cover.get("conclusion", ""),
        cover.get("header", {}).get("employer", ""),
    ])

    for pattern, msg in BAD_PATTERNS_COVER.items():
        if pattern.lower() in full_text.lower():
            issues.append(f"COVER: {msg} (pattern: '{pattern.strip()}')")

    header = cover.get("header", {}) if isinstance(cover, dict) else {}
    address = str(header.get("address", "")).strip()
    if address:
        if re.search(r"\d", address):
            issues.append("COVER: Header address contains numeric street/zip detail; use city/state only")
        if re.search(r"\b(st|street|ave|avenue|rd|road|blvd|boulevard|dr|drive|ln|lane|apt|suite)\b", address, flags=re.IGNORECASE):
            issues.append("COVER: Header address looks like street-level address; use city/state only")

    # Word count check
    word_count = len(full_text.split())
    if word_count < 80:
        issues.append(f"COVER: Too short — only {word_count} words (minimum 80)")
    elif word_count > 450:
        issues.append(f"COVER: Too long — {word_count} words (maximum 450)")

    # Check DOCX exists
    docx_path = generated_dir / "cover.docx"
    if not docx_path.exists():
        issues.append("COVER: cover.docx not found — run step 08")

    return issues


def check_resume(generated_dir: Path, version: str) -> list:
    issues = []

    # Check JSON intermediate
    json_path = generated_dir / f"resume_intermediate_{version}.json"
    if not json_path.exists():
        issues.append(f"MISSING: resume_intermediate_{version}.json not found")
        return issues

    with open(json_path, "r", encoding="utf-8") as f:
        resume = json.load(f)

    summary = str(resume.get("summary", ""))
    if summary:
        body = summary.split(".", 1)[1] if "." in summary else summary
        if re.search(r"\b(I|I'm|I am|my|me)\b", body, flags=re.IGNORECASE):
            issues.append("RESUME: Summary uses first-person language; use third-person style")

    # Build full text from all resume fields
    parts = []
    if isinstance(resume, dict):
        for key, val in resume.items():
            if isinstance(val, str):
                parts.append(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        parts.extend(str(v) for v in item.values())

    full_text = " ".join(parts)

    for pattern, msg in BAD_PATTERNS_RESUME.items():
        if pattern.lower() in full_text.lower():
            issues.append(f"RESUME: {msg} (pattern: '{pattern.strip()}')")

    # Check required sections exist
    if not resume.get("experience") and not resume.get("experiences"):
        issues.append("RESUME: No experience section found")
    if not resume.get("skills"):
        issues.append("RESUME: No skills section found")
    if not resume.get("summary") and not resume.get("professional_summary"):
        issues.append("RESUME: No summary section found")

    # Check DOCX exists
    docx_path = generated_dir / "resume.docx"
    if not docx_path.exists():
        issues.append("RESUME: resume.docx not found — run step 05 with --all")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Quality gate for job application output")
    parser.add_argument("--uuid", required=True, help="Job UUID or prefix")
    parser.add_argument("--version", default="v1", help="Version tag (e.g. v1)")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any issue (blocks pipeline)")
    args = parser.parse_args()

    job_folder = resolve_job_folder(args.uuid)
    generated_dir = job_folder / "generated"

    print("\n" + "=" * 55)
    print("  APPLICATION QUALITY CHECK")
    print(f"  Job: {job_folder.name}")
    print("=" * 55)

    cover_issues = check_cover(generated_dir, args.version)
    resume_issues = check_resume(generated_dir, args.version)
    all_issues = cover_issues + resume_issues

    if cover_issues:
        print("\nCOVER LETTER:")
        for i in cover_issues:
            print(f"  WARNING  {i}")
    else:
        print("\nCOVER LETTER:   OK")

    if resume_issues:
        print("\nRESUME:")
        for i in resume_issues:
            print(f"  WARNING  {i}")
    else:
        print("\nRESUME:         OK")

    print("\n" + "=" * 55)
    if all_issues:
        print(f"  RESULT: {len(all_issues)} issue(s) found — review before sending")
        print("=" * 55 + "\n")
        if args.strict:
            sys.exit(1)
    else:
        print("  RESULT: PASSED — safe to apply")
        print("=" * 55 + "\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
