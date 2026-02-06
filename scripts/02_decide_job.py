# scripts/02_decide_job.py
"""
CLI to make a decision on a scored job: accept, reject, or hold.

Usage examples:
    python -m scripts.02_decide_job --uuid 96b16121-8608-405d-9553-af86fdbf939c --accept --reason "Strong match — ETL & Snowflake heavy"
    python -m scripts.02_decide_job --uuid <uuid> --reject --reason "Requires on-site 5 days — not possible"
    python -m scripts.02_decide_job --uuid <uuid> --hold --reason "Waiting for referral / better offer"
    python -m scripts.02_decide_job --uuid cdb9a3fa --accept --reason "Strong match - proceeding"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

import yaml


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Make decision on scored job (accept / reject / hold)")
    parser.add_argument(
        "--uuid",
        type=str,
        required=True,
        help="Job UUID (required)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--accept", action="store_true", help="Accept → status = ACCEPTED")
    group.add_argument("--reject", action="store_true", help="Reject → status = REJECTED")
    group.add_argument(
        "--hold",
        "--pending",
        "--later",
        action="store_true",
        help="Hold / Pending → status = PENDING",
    )
    parser.add_argument(
        "--reason",
        "--note",
        type=str,
        default="",
        help="Reason or note for this decision (will be appended to notes)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing to disk",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    uuid_str = args.uuid.strip()
    job_dir = Path("data/jobs") / uuid_str   # ← changed: we now expect UUID folder directly (simpler)

    # More flexible: also allow short-uuid prefix folders (00005_96b16121)
    if not job_dir.exists():
        candidates = list(Path("data/jobs").glob(f"*_{uuid_str[:8]}"))
        if len(candidates) == 1:
            job_dir = candidates[0]
            print(f"Resolved UUID prefix → using folder: {job_dir.name}")
        elif len(candidates) > 1:
            print(f"Ambiguous UUID prefix — multiple matches:\n" + "\n".join(str(c) for c in candidates))
            sys.exit(1)
        else:
            print(f"Error: No job folder found for UUID {uuid_str}")
            print("  Looked for: data/jobs/<uuid>  or  data/jobs/*_<short-uuid>")
            sys.exit(1)

    metadata_path = job_dir / "metadata.yaml"

    if not metadata_path.is_file():
        print(f"Error: metadata.yaml not found → {metadata_path}")
        print("  → Run 01_score_job.py first or check UUID")
        sys.exit(1)

    print(f"Decision for job: {job_dir.name}")
    print(f"Metadata: {metadata_path}")

    # Load current metadata
    try:
        with metadata_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Failed to read metadata.yaml: {e}")
        sys.exit(1)

    old_status = data.get("status", "UNKNOWN").upper()

    # Determine new status + default note
    if args.accept:
        new_status = "ACCEPTED"
        default_note = "Accepted — moving to application/tailoring phase"
    elif args.reject:
        new_status = "REJECTED"
        default_note = "Rejected"
    else:  # hold
        new_status = "PENDING"
        default_note = "Held for later review"

    note = (args.reason.strip() or default_note).strip()

    # Show preview
    print("\n" + "─" * 60)
    print(f"  Status change:  {old_status:12} → {new_status}")
    print(f"  Note to append: {note}")
    print("─" * 60)

    if args.dry_run:
        print("[DRY RUN] No changes written.")
        return

    # Apply update
    data["status"] = new_status

    current_notes = (data.get("notes") or "").strip()
    if current_notes:
        data["notes"] = f"{current_notes}\n• {note} ({datetime.now().strftime('%Y-%m-%d')})"
    else:
        data["notes"] = f"• {note} ({datetime.now().strftime('%Y-%m-%d')})"

    # Optional: record decision timestamp
    data["last_decision_at"] = datetime.now().isoformat()
    data["last_decision"] = new_status

    try:
        with metadata_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        print("✓ Decision saved successfully")
        print(f"  New status   : {new_status}")
        print(f"  Note added   : {note}")
        print(f"  Updated file : {metadata_path}")
    except Exception as e:
        print(f"Failed to save metadata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()