"""Manual utility to set user decision (accept/reject/hold) on a job."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.metadata_io import load_metadata, save_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set a user decision for a job.")
    parser.add_argument("--job-id", required=True, help="Job folder id, e.g. 00070_3fa9c07b")

    decision_group = parser.add_mutually_exclusive_group(required=True)
    decision_group.add_argument("--accept", action="store_true", help="Set decision to accept")
    decision_group.add_argument("--reject", action="store_true", help="Set decision to reject")
    decision_group.add_argument("--hold", action="store_true", help="Set decision to hold")

    parser.add_argument("--reason", default=None, help="Optional reason for decision")
    return parser.parse_args()


def _decision_from_args(args: argparse.Namespace) -> str:
    if args.accept:
        return "accept"
    if args.reject:
        return "reject"
    return "hold"


def main() -> None:
    args = parse_args()
    decision = _decision_from_args(args)

    reason = None
    if args.reason is not None:
        stripped = args.reason.strip()
        reason = stripped if stripped else None

    metadata_path = Path("data/jobs") / args.job_id / "metadata.yaml"
    metadata = load_metadata(metadata_path)

    metadata["user_decision"] = decision
    metadata["user_decision_at"] = datetime.now().isoformat()
    metadata["user_reason"] = reason
    save_metadata(metadata_path, metadata)

    print("=== JOB DECISION UPDATED ===")
    print(f"Job ID: {args.job_id}")
    print(f"Decision: {decision}")
    print(f"Reason: {reason if reason is not None else 'None'}")
    print(f"Path: data/jobs/{args.job_id}/metadata.yaml")


if __name__ == "__main__":
    main()
