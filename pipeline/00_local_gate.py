"""Minimal local gate step: read, normalize, preview, and hash intake text."""

import argparse
import json
from pathlib import Path
import shutil
import uuid
from datetime import datetime
import yaml

from utils.duplicate_check import run_duplicate_check
from utils.hashes import compute_sha256
from utils.intake_normalizer import normalize_text
from utils.job_paths import create_job_folder, get_next_job_number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run minimal local gate on intake file.")
    parser.add_argument("intake_path", help="Path to intake markdown/text file.")
    parser.add_argument("--threshold", type=float, default=0.82, help="Duplicate threshold.")
    parser.add_argument("--top-k", type=int, default=5, help="Top matches to inspect.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    intake_path = Path(args.intake_path)

    raw_text = intake_path.read_text(encoding="utf-8")
    normalized = normalize_text(raw_text)
    digest = compute_sha256(normalized)
    duplicate_result = run_duplicate_check(
        normalized_text=normalized,
        threshold=args.threshold,
        top_k=args.top_k,
    )

    print("=== NORMALIZED PREVIEW ===")
    print(normalized[:500])
    print()
    print(f"Length: {len(normalized)} chars")
    print(f"Hash: {digest}")
    print()
    print("=== DUPLICATE CHECK ===")
    print(f"Mode: {duplicate_result['mode']}")
    print(f"Duplicate Found: {duplicate_result['duplicate_found']}")
    print(f"Score: {duplicate_result['score']:.4f}")
    print(f"Matched Job ID: {duplicate_result['matched_job_id']}")
    print(f"Reason: {duplicate_result['reason']}")

    job_uuid = str(uuid.uuid4())
    job_number = get_next_job_number()
    job_id = f"{job_number:05d}_{job_uuid[:8]}"
    job_dir = create_job_folder(job_id)
    raw_path = job_dir / "raw" / "raw_intake.md"
    shutil.copy2(intake_path, raw_path)

    print()
    print("=== JOB FOLDER CREATED ===")
    print(f"Job ID: {job_id}")
    print(f"Path: data/jobs/{job_id}")
    print("Raw file: raw/raw_intake.md")

    rules = {
        "location_ok": True,
        "visa_ok": True,
        "salary_ok": True,
        "contract_ok": True,
        "title_ok": True,
    }
    reason_codes = ["duplicate_found"] if duplicate_result["duplicate_found"] else []
    tier0_decision = "reject_early" if duplicate_result["duplicate_found"] else "needs_llm"

    local_gate_artifact = {
        "artifact_type": "local_gate",
        "artifact_schema_version": "v1",
        "job_id": job_id,
        "job_hash": digest,
        "duplicate_check": {
            "mode": duplicate_result["mode"],
            "duplicate_found": duplicate_result["duplicate_found"],
            "score": duplicate_result["score"],
            "matched_job_id": duplicate_result["matched_job_id"],
            "reason": duplicate_result["reason"],
        },
        "rules": rules,
        "tier0_decision": tier0_decision,
        "reason_codes": reason_codes,
    }

    score_dir = job_dir / "score"
    score_dir.mkdir(parents=True, exist_ok=True)
    local_gate_path = score_dir / "local_gate.json"
    local_gate_path.write_text(
        json.dumps(local_gate_artifact, indent=2),
        encoding="utf-8",
    )

    print()
    print("=== LOCAL GATE ARTIFACT WRITTEN ===")
    print(f"Path: data/jobs/{job_id}/score/local_gate.json")
    print(f"Tier0 Decision: {tier0_decision}")

    metadata = {
        "uuid": job_uuid,
        "job_id": job_id,
        "original_filename": intake_path.name,
        "created_at": datetime.now().isoformat(),
        "status": "PENDING",
        "job_hash": digest,
        "tier0_decision": tier0_decision,
        "llm_decision": None,
        "user_decision": "pending",
        "score": None,
    }
    metadata_path = job_dir / "metadata.yaml"
    metadata_path.write_text(
        yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    print()
    print("=== METADATA WRITTEN ===")
    print(f"Path: data/jobs/{job_id}/metadata.yaml")
    print("Status: PENDING")
    print(f"Tier0 Decision: {tier0_decision}")

    reason_codes_display = ", ".join(reason_codes) if reason_codes else "none"
    final_result = (
        "stopping pipeline before any LLM call"
        if tier0_decision == "reject_early"
        else "job is eligible for next pipeline stage"
    )

    print()
    print("=== TIER 0 FINAL DECISION ===")
    print(f"Decision: {tier0_decision}")
    print(f"Result: {final_result}")
    print(f"Reason Codes: {reason_codes_display}")


if __name__ == "__main__":
    main()
