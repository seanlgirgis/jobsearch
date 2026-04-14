"""Manual utility to backfill normalized job_hash into existing metadata.yaml files."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import yaml

from hashes import compute_sha256
from intake_normalizer import normalize_text


JOBS_ROOT = Path("data/jobs")
RAW_CANDIDATES = (
    Path("raw/raw_intake.md"),
    Path("raw/job_description.md"),
    Path("raw_intake.md"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill job_hash for existing jobs.")
    parser.add_argument("--dry-run", action="store_true", help="Compute only; do not write metadata.")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N jobs.")
    parser.add_argument("--job-id", type=str, default=None, help="Process a single job folder id.")
    return parser.parse_args()


def iter_job_dirs(job_id: str | None) -> Iterable[Path]:
    if job_id:
        yield JOBS_ROOT / job_id
        return

    for path in sorted(JOBS_ROOT.iterdir(), key=lambda p: p.name):
        if path.is_dir():
            yield path


def find_raw_file(job_dir: Path) -> Path | None:
    for rel_path in RAW_CANDIDATES:
        candidate = job_dir / rel_path
        if candidate.is_file():
            return candidate
    return None


def main() -> None:
    args = parse_args()

    processed = 0
    updated = 0
    skipped = 0
    failed = 0

    for job_dir in iter_job_dirs(args.job_id):
        if args.limit is not None and processed >= args.limit:
            break

        processed += 1
        job_id = job_dir.name

        if not job_dir.is_dir():
            print(f"[FAIL]  {job_id}  job folder not found")
            failed += 1
            continue

        raw_file = find_raw_file(job_dir)
        if raw_file is None:
            print(f"[FAIL]  {job_id}  no raw job file found")
            failed += 1
            continue

        metadata_path = job_dir / "metadata.yaml"
        if not metadata_path.is_file():
            print(f"[FAIL]  {job_id}  metadata.yaml missing")
            failed += 1
            continue

        try:
            raw_text = raw_file.read_text(encoding="utf-8")
            normalized = normalize_text(raw_text)
            digest = compute_sha256(normalized)

            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) or {}
            if not isinstance(metadata, dict):
                raise ValueError("metadata.yaml is not a mapping")

            metadata["job_hash"] = digest

            if args.dry_run:
                print(f"[SKIP]  {job_id}  dry-run only")
                skipped += 1
                continue

            metadata_path.write_text(
                yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            print(f"[OK]    {job_id}  hash updated")
            updated += 1
        except Exception as exc:
            print(f"[FAIL]  {job_id}  {exc}")
            failed += 1

    print()
    print("=== BACKFILL SUMMARY ===")
    print(f"Processed: {processed}")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()

