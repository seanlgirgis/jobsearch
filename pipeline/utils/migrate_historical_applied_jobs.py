"""Bulk-copy historical legacy jobs from data/jobs into data/applied_jobs.

Default mode copies all missing folders for archive/search coverage.
Optional narrow mode (--only-marked-applied) keeps legacy status filtering.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import shutil
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrate historical jobs into data/applied_jobs for archive/search.",
    )
    parser.add_argument("--source-root", default="data/jobs", help="Source root containing legacy jobs")
    parser.add_argument("--dest-root", default="data/applied_jobs", help="Destination root for applied jobs")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print actions only")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N job folders")
    parser.add_argument(
        "--only-marked-applied",
        action="store_true",
        help="Use narrow mode: copy only jobs marked as applied in metadata",
    )
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


def _is_marked_applied(metadata: dict[str, Any]) -> bool:
    status = str(metadata.get("status", "")).strip().lower()
    submission_status = str(metadata.get("submission_status", "")).strip().lower()
    return status == "accepted" or submission_status == "applied"


def _to_posix_path(path_str: str) -> str:
    return path_str.replace("\\", "/").rstrip("/")


def main() -> None:
    args = parse_args()

    source_root = Path(args.source_root)
    dest_root = Path(args.dest_root)
    source_root_label = _to_posix_path(args.source_root)
    dest_root_label = _to_posix_path(args.dest_root)

    processed = 0
    copied = 0
    skipped = 0
    warnings = 0
    failed = 0

    if not source_root.is_dir():
        print(f"[FAIL]  {source_root.as_posix()}  source root not found")
        print()
        print("=== MIGRATION SUMMARY ===")
        print(f"Processed: {processed}")
        if args.dry_run:
            print(f"Would Copy: {copied}")
        else:
            print(f"Copied: {copied}")
        print(f"Skipped: {skipped}")
        print(f"Warnings: {warnings}")
        print(f"Failed: {failed + 1}")
        print()
        print("Next step: rebuild search/index against data/applied_jobs if needed")
        return

    if not args.dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    for source_job in sorted(source_root.iterdir(), key=lambda p: p.name):
        if args.limit is not None and processed >= args.limit:
            break

        if not source_job.is_dir():
            continue

        processed += 1
        job_id = source_job.name
        source_metadata_path = source_job / "metadata.yaml"
        dest_job = dest_root / job_id
        dest_metadata_path = dest_job / "metadata.yaml"

        try:
            source_metadata: dict[str, Any] | None = None
            source_has_metadata = source_metadata_path.is_file()
            if source_has_metadata:
                source_metadata = _load_metadata(source_metadata_path)

            if args.only_marked_applied:
                if not source_has_metadata:
                    if args.dry_run:
                        print(f"[WARN]  {job_id}  metadata missing, would skip in --only-marked-applied mode")
                    else:
                        print(f"[WARN]  {job_id}  metadata missing, skipped in --only-marked-applied mode")
                    warnings += 1
                    skipped += 1
                    continue
                if not _is_marked_applied(source_metadata or {}):
                    print(f"[SKIP]  {job_id}  not marked as applied")
                    skipped += 1
                    continue

            if dest_job.exists():
                print(f"[SKIP]  {job_id}  destination already exists")
                skipped += 1
                continue

            if args.dry_run:
                if not source_has_metadata:
                    print(f"[WARN]  {job_id}  metadata missing, would copy anyway")
                    warnings += 1
                print(f"[OK]    {job_id}  would copy to {dest_root_label}")
                copied += 1
                continue

            shutil.copytree(source_job, dest_job)

            migrated_at = datetime.now().isoformat()
            dest_has_metadata = dest_metadata_path.is_file()
            if dest_has_metadata:
                dest_metadata = _load_metadata(dest_metadata_path)
                dest_metadata["migrated_to_applied_jobs"] = True
                dest_metadata["migrated_at"] = migrated_at
                dest_metadata["migration_source_root"] = source_root_label
                dest_metadata["historical_archive_mode"] = True
                _save_metadata(dest_metadata_path, dest_metadata)
            else:
                print(f"[WARN]  {job_id}  metadata missing, copied anyway")
                warnings += 1

            if source_has_metadata and source_metadata is not None:
                source_metadata["migrated_to_applied_jobs"] = True
                source_metadata["migrated_at"] = migrated_at
                source_metadata["applied_jobs_path"] = f"{dest_root_label}/{job_id}"
                source_metadata["historical_archive_mode"] = True
                _save_metadata(source_metadata_path, source_metadata)
            else:
                print(f"[WARN]  {job_id}  source metadata missing, copied anyway")
                warnings += 1

            print(f"[OK]    {job_id}  copied to {dest_root_label}")
            copied += 1
        except Exception as exc:
            print(f"[FAIL]  {job_id}  {exc}")
            failed += 1

    print()
    print("=== MIGRATION SUMMARY ===")
    print(f"Processed: {processed}")
    if args.dry_run:
        print(f"Would Copy: {copied}")
    else:
        print(f"Copied: {copied}")
    print(f"Skipped: {skipped}")
    print(f"Warnings: {warnings}")
    print(f"Failed: {failed}")
    print()
    print("Next step: rebuild search/index against data/applied_jobs if needed")


if __name__ == "__main__":
    main()
