# scripts/job_decision.py
"""
CLI to update job status: accept, reject, or hold/hold.

Usage examples:
    python -m scripts.job_decision --uuid 96b16121-8608-405d-9553-af86fdbf939c --accept --reason "Strong ETL match for POC"
    python -m scripts.job_decision --uuid <uuid> --reject --reason "No healthcare exp"
    python -m scripts.job_decision --uuid <uuid> --hold --reason "Review next week"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update job decision/status")
    parser.add_argument(
        "--uuid",
        type=str,
        required=True,
        help="Job UUID (required)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--accept", action="store_true", help="Set status to ACCEPTED")
    group.add_argument("--reject", action="store_true", help="Set status to REJECTED")
    group.add_argument("--hold", "--hold", "--pending", action="store_true", help="Keep/return to PENDING")
    parser.add_argument(
        "--reason",
        "--note",
        type=str,
        default="",
        help="Reason/note for the decision (appended to notes)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    uuid = args.uuid.strip()
    job_dir = Path("data/jobs") / uuid
    metadata_path = job_dir / "metadata.yaml"

    if not metadata_path.is_file():
        print(f"Error: metadata.yaml not found at {metadata_path}")
        print("  → Run score_job.py first or verify UUID")
        sys.exit(1)

    print(f"Updating job: {uuid}")
    print(f"Metadata file: {metadata_path}")

    # Load current data
    try:
        with metadata_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Failed to read YAML: {e}")
        sys.exit(1)

    old_status = data.get("status", "unknown")

    # Determine new status
    if args.accept:
        new_status = "ACCEPTED"
        default_note = "Accepted - proceeding to tailoring"
    elif args.reject:
        new_status = "REJECTED"
        default_note = "Rejected"
    else:  # hold / hold / pending
        new_status = "PENDING"
        default_note = "Held for later review"

    reason = args.reason.strip() or default_note

    # Update
    data["status"] = new_status
    current_notes = data.get("notes", "").strip()
    if current_notes:
        data["notes"] = f"{current_notes}\n{reason}"
    else:
        data["notes"] = reason

    # Save
    try:
        with metadata_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        print(f"Success!")
        print(f"  Status: {old_status} → {new_status}")
        print(f"  Note added/appended: {reason}")
        print(f"  Updated file: {metadata_path}")
    except Exception as e:
        print(f"Failed to save YAML: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()