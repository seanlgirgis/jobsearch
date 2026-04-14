"""Manual utility to promote a pipeline job folder into data/applied_jobs."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import shutil
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote a pipeline job to applied_jobs.")
    parser.add_argument("--job-id", required=True, help="Job id, e.g. 00068_75e1a487")
    parser.add_argument("--source-root", default="data/current_jobs", help="Source root containing active jobs")
    parser.add_argument("--dest-root", default="data/applied_jobs", help="Destination root for applied jobs")
    parser.add_argument("--move", action="store_true", help="Move folder instead of copy")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print actions only")
    return parser.parse_args()


def _load_metadata(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("metadata.yaml is not a mapping")
    return data


def _save_metadata(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()

    source_root = Path(args.source_root)
    dest_root = Path(args.dest_root)
    source_job = source_root / args.job_id
    dest_job = dest_root / args.job_id
    mode = "MOVE" if args.move else "COPY"

    if not source_job.is_dir():
        print("[FAIL] Source job folder not found")
        return

    source_metadata_path = source_job / "metadata.yaml"
    if not source_metadata_path.is_file():
        print("[FAIL] metadata.yaml missing")
        return

    if dest_job.exists():
        print("[FAIL] Destination already exists")
        return

    if args.dry_run:
        print(f"[DRY RUN] Would promote job by {mode}")
        print(f"Job ID: {args.job_id}")
        print(f"Source: {source_job.as_posix()}")
        print(f"Destination: {dest_job.as_posix()}")
        return

    dest_root.mkdir(parents=True, exist_ok=True)
    applied_at = datetime.now().isoformat()

    if args.move:
        shutil.move(str(source_job), str(dest_job))
    else:
        shutil.copytree(source_job, dest_job)

    dest_metadata_path = dest_job / "metadata.yaml"
    dest_metadata = _load_metadata(dest_metadata_path)
    dest_metadata["submission_status"] = "applied"
    dest_metadata["applied_at"] = applied_at
    dest_metadata["applied_via"] = "manual"
    dest_metadata["source_root"] = args.source_root
    dest_metadata["promoted_to"] = args.dest_root
    _save_metadata(dest_metadata_path, dest_metadata)

    if args.move:
        print("[OK] Promoted job by MOVE")
        print(f"Job ID: {args.job_id}")
        print(f"Source: {source_job.as_posix()}")
        print(f"Destination: {dest_job.as_posix()}")
        print("Metadata updated in destination")
        return

    source_metadata = _load_metadata(source_metadata_path)
    source_metadata["submission_status"] = "applied"
    source_metadata["applied_at"] = applied_at
    source_metadata["applied_via"] = "manual"
    source_metadata["copied_to_applied_jobs"] = True
    source_metadata["applied_jobs_path"] = f"{args.dest_root.rstrip('/').rstrip(chr(92))}/{args.job_id}"
    _save_metadata(source_metadata_path, source_metadata)

    print("[OK] Promoted job by COPY")
    print(f"Job ID: {args.job_id}")
    print(f"Source: {source_job.as_posix()}")
    print(f"Destination: {dest_job.as_posix()}")
    print("Metadata updated in source and destination")


if __name__ == "__main__":
    main()

