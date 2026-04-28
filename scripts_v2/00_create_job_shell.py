#!/usr/bin/env python3
"""
Create a new manual-v2 job shell from intake text.

This script does not run any LLM/RAG generation steps.
It only prepares folder structure + metadata for manual ChatGPT artifacts.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
JOBS_ROOT = PROJECT_ROOT / "data" / "jobs"
CACHE_PATH = PROJECT_ROOT / ".job_cache_v2.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create manual-v2 job shell folder.")
    parser.add_argument("intake_file", help="Path to intake markdown file.")
    parser.add_argument(
        "--skip-duplicate-check",
        action="store_true",
        help="Skip duplicate check before creating job shell.",
    )
    parser.add_argument(
        "--allow-duplicate",
        action="store_true",
        help="Continue even if duplicate check is flagged.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.82,
        help="Duplicate threshold passed to scripts/00_check_applied_before.py.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Top-k matches passed to duplicate check script.",
    )
    parser.add_argument(
        "--move-intake",
        action="store_true",
        help="Move intake file into job folder root (default is copy).",
    )
    return parser.parse_args()


def run_duplicate_check(intake_path: Path, threshold: float, top_k: int) -> int:
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "00_check_applied_before.py"),
        str(intake_path),
        "--threshold",
        str(threshold),
        "--top-k",
        str(top_k),
    ]
    print("=== DUPLICATE CHECK ===")
    print(" ".join(cmd))
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    return result.returncode


def get_next_job_number() -> int:
    pattern = re.compile(r"^(\d{5})_[0-9a-f]{8}$")
    numbers: List[int] = []

    if not JOBS_ROOT.exists():
        return 1

    for child in JOBS_ROOT.iterdir():
        if not child.is_dir():
            continue
        match = pattern.match(child.name)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) + 1 if numbers else 1


def extract_front_matter(job_text: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    lines = job_text.splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("---"):
            continue
        if ":" not in stripped:
            break
        key, value = stripped.split(":", 1)
        key = key.strip().lower().replace(" ", "_").replace("-", "_")
        value = value.strip()
        if value:
            data[key] = value
    return data


def extract_metadata_from_filename(filename: str) -> Dict[str, str]:
    stem = Path(filename).stem
    parts = stem.split(".")
    if len(parts) < 3:
        return {"company": "Unknown", "role": "Unknown"}

    company = parts[1].replace("_", " ").title()
    rest_parts = parts[2:]
    role_parts: List[str] = []
    for part in rest_parts:
        if re.match(r"^\d{8,}", part):
            break
        role_parts.append(part.replace("_", " "))

    role = " ".join(role_parts).title().strip()
    if not role:
        role = "Unknown Role"
    return {"company": company, "role": role}


def create_job_shell(intake_path: Path, move_intake: bool) -> Dict[str, Any]:
    job_uuid = str(uuid.uuid4())
    job_number = get_next_job_number()
    job_id = f"{job_number:05d}_{job_uuid[:8]}"

    job_dir = JOBS_ROOT / job_id
    for subdir in ("raw", "score", "tailored", "generated", "research"):
        (job_dir / subdir).mkdir(parents=True, exist_ok=True)

    text = intake_path.read_text(encoding="utf-8")
    front_matter = extract_front_matter(text)
    meta_from_filename = extract_metadata_from_filename(intake_path.name)

    company = front_matter.get("company_name", front_matter.get("company", meta_from_filename["company"]))
    role = front_matter.get("title", front_matter.get("job_title", meta_from_filename["role"]))

    job_root_copy = job_dir / intake_path.name
    if move_intake:
        intake_path.replace(job_root_copy)
        source_label = "moved"
    else:
        shutil.copy2(intake_path, job_root_copy)
        source_label = "copied"

    raw_path = job_dir / "raw" / "raw_intake.md"
    shutil.copy2(job_root_copy, raw_path)

    metadata = {
        "uuid": job_uuid,
        "job_id": job_id,
        "original_filename": intake_path.name,
        "company": company,
        "role": role,
        "company_website": front_matter.get("company_website", ""),
        "location": front_matter.get("location", ""),
        "status": "PENDING",
        "score": None,
        "recommendation": None,
        "pipeline_mode": "manual_v2",
        "created_at": datetime.now().isoformat(),
        "notes": "Manual-v2 shell created. Awaiting ChatGPT artifacts.",
    }
    metadata_path = job_dir / "metadata.yaml"
    metadata_path.write_text(
        yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    score_template_path = job_dir / "score" / "score_report_manual_v1.md"
    score_template_path.write_text(
        (
            "# Manual Score Report\n\n"
            "Paste MODE B1 output below using the exact section headings:\n\n"
            "## Match Score: X%\n"
            "## Recommendation: Strong Proceed / Proceed / Hold / Skip\n"
            "## Strongest Matches\n"
            "## Gaps & Risks\n"
            "## ATS Keywords Present\n"
            "## ATS Keywords Missing\n"
            "## Advice\n"
        ),
        encoding="utf-8",
    )

    handoff_path = job_dir / "manual_handoff_v2.md"
    handoff_path.write_text(
        (
            "# Manual V2 Artifact Handoff\n\n"
            "Drop files into this job folder:\n\n"
            "- score/score_report_manual_v1.md (MODE B1 text)\n"
            "- tailored/tailored_data_v1.yaml (MODE C1)\n"
            "- generated/resume_intermediate_v1.json (MODE C1)\n"
            "- generated/cover_intermediate_v1.json (MODE D1)\n"
        ),
        encoding="utf-8",
    )

    # Create empty placeholders for manual ChatGPT artifacts (v1 contract).
    # These are intentionally empty so you can paste/download artifacts into them.
    placeholder_paths = [
        job_dir / "tailored" / "tailored_data_v1.yaml",
        job_dir / "generated" / "resume_intermediate_v1.json",
        job_dir / "generated" / "cover_intermediate_v1.json",
    ]
    for placeholder in placeholder_paths:
        placeholder.touch(exist_ok=True)

    cache_data = {
        "intake_file": str(intake_path),
        "job_id": job_id,
        "uuid": job_uuid,
        "uuid_short": job_uuid[:8],
        "job_folder": str(job_dir),
        "created_at": datetime.now().isoformat(),
        "manual_v2": True,
        "documents_ready": False,
        "applied": False,
    }
    CACHE_PATH.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")

    return {
        "job_id": job_id,
        "uuid": job_uuid,
        "uuid_short": job_uuid[:8],
        "job_dir": job_dir,
        "metadata_path": metadata_path,
        "raw_path": raw_path,
        "score_template_path": score_template_path,
        "handoff_path": handoff_path,
        "placeholder_paths": placeholder_paths,
        "source_label": source_label,
    }


def main() -> None:
    args = parse_args()
    intake_path = Path(args.intake_file)
    if not intake_path.is_file():
        print(f"[ERROR] Intake file not found: {intake_path}")
        sys.exit(1)

    if not args.skip_duplicate_check:
        dup_rc = run_duplicate_check(intake_path, threshold=args.threshold, top_k=args.top_k)
        if dup_rc == 1 and not args.allow_duplicate:
            print("[STOP] Duplicate flagged. Shell not created.")
            print("Use --allow-duplicate to override.")
            sys.exit(1)
        if dup_rc == 2:
            print("[WARN] Duplicate check blocked. Continuing with shell creation.")
        if dup_rc == 1 and args.allow_duplicate:
            print("[WARN] Duplicate flagged but override enabled. Continuing.")

    result = create_job_shell(intake_path, move_intake=args.move_intake)

    print()
    print("=== MANUAL V2 SHELL CREATED ===")
    print(f"JOB_ID: {result['job_id']}")
    print(f"UUID: {result['uuid']}")
    print(f"UUID_SHORT: {result['uuid_short']}")
    print(f"JOB_FOLDER: {result['job_dir']}")
    print(f"INTAKE_{result['source_label'].upper()}: {result['raw_path']}")
    print(f"METADATA: {result['metadata_path']}")
    print(f"SCORE_TEMPLATE: {result['score_template_path']}")
    print(f"HANDOFF: {result['handoff_path']}")
    print("PLACEHOLDERS:")
    for p in result["placeholder_paths"]:
        print(f"- {p}")
    print(f"CACHE_FILE: {CACHE_PATH}")
    print()
    print("Next: run ChatGPT modes B1, C1, D1 and place files into this job folder.")


if __name__ == "__main__":
    main()
