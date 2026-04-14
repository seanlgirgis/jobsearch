"""Manual helper to inspect a pipeline job folder."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect one pipeline job folder.")
    parser.add_argument("--job-id", required=True, help="Job id, e.g. 00068_75e1a487")
    parser.add_argument("--root", default="data/current_jobs", help="Root folder containing job folders")
    return parser.parse_args()


def _read_metadata(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return None
    return data


def _exists_str(path: Path) -> str:
    return "yes" if path.is_file() else "no"


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    job_dir = root / args.job_id

    if not job_dir.is_dir():
        print("[FAIL] Source job folder not found")
        print(f"Job ID: {args.job_id}")
        print(f"Path: {job_dir.as_posix()}")
        return

    metadata_path = job_dir / "metadata.yaml"
    raw_path = job_dir / "raw" / "raw_intake.md"
    local_gate_path = job_dir / "score" / "local_gate.json"
    job_packet_path = job_dir / "tailored" / "job_packet.json"

    print("=== PIPELINE JOB ===")
    print(f"Job ID: {args.job_id}")
    print(f"Root: {root.as_posix()}")
    print(f"Path: {job_dir.as_posix()}")
    print()
    print("=== FILE CHECK ===")
    print(f"metadata.yaml: {_exists_str(metadata_path)}")
    print(f"raw/raw_intake.md: {_exists_str(raw_path)}")
    print(f"score/local_gate.json: {_exists_str(local_gate_path)}")
    print(f"tailored/job_packet.json: {_exists_str(job_packet_path)}")

    metadata = _read_metadata(metadata_path)
    if metadata is None:
        print()
        print("=== METADATA SUMMARY ===")
        print("metadata.yaml missing or invalid")
        return

    print()
    print("=== METADATA SUMMARY ===")
    print(f"status: {metadata.get('status')}")
    print(f"tier0_decision: {metadata.get('tier0_decision')}")
    print(f"llm_decision: {metadata.get('llm_decision')}")
    print(f"score: {metadata.get('score')}")


if __name__ == "__main__":
    main()

