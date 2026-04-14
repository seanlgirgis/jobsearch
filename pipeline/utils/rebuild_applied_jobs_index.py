"""Manual utility to rebuild FAISS index from data/applied_jobs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import faiss
import numpy as np
import yaml

from scripts.utils.vector_ops import get_model, save_index_and_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild semantic index from applied jobs.")
    parser.add_argument("--source-root", default="data/applied_jobs", help="Source root containing applied jobs")
    parser.add_argument("--min-text-length", type=int, default=80, help="Minimum text length to index")
    return parser.parse_args()


def _load_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.is_file():
            return p
    return None


def _pick_text_file(job_dir: Path) -> Path | None:
    candidates = [
        job_dir / "raw" / "job_description.md",
        job_dir / "raw" / "raw_intake.md",
    ]
    for p in sorted(job_dir.glob("*.md"), key=lambda x: x.name):
        candidates.append(p)
    return _first_existing(candidates)


def main() -> None:
    args = parse_args()
    source_root = Path(args.source_root)

    if not source_root.is_dir():
        print(f"[FAIL] Source root not found: {source_root.as_posix()}")
        return

    scanned = 0
    indexed = 0
    skipped_missing_text = 0
    skipped_short_text = 0
    failed = 0

    texts: list[str] = []
    metadatas: list[dict[str, Any]] = []

    for job_dir in sorted(source_root.iterdir(), key=lambda p: p.name):
        if not job_dir.is_dir():
            continue
        scanned += 1
        job_id = job_dir.name

        try:
            text_path = _pick_text_file(job_dir)
            if text_path is None:
                skipped_missing_text += 1
                continue

            text = text_path.read_text(encoding="utf-8").strip()
            if len(text) < args.min_text_length:
                skipped_short_text += 1
                continue

            meta = _load_metadata(job_dir / "metadata.yaml")
            texts.append(text)
            metadatas.append(
                {
                    "uuid": job_id,
                    "description_path": text_path.as_posix(),
                    "company": meta.get("company", "Unknown"),
                    "role": meta.get("role", "Unknown"),
                    "apply_date": meta.get("application", {}).get("date", "N/A")
                    if isinstance(meta.get("application"), dict)
                    else "N/A",
                    "status": meta.get("status", "Unknown"),
                    "submission_status": meta.get("submission_status", "Unknown"),
                    "source_root": source_root.as_posix(),
                }
            )
            indexed += 1
        except Exception as exc:
            print(f"[WARN] {job_id}  skipped: {exc}")
            failed += 1

    if not texts:
        print("[FAIL] No indexable job texts found.")
        print()
        print("=== INDEX SUMMARY ===")
        print(f"Scanned: {scanned}")
        print(f"Indexed: {indexed}")
        print(f"Skipped (missing text): {skipped_missing_text}")
        print(f"Skipped (short text): {skipped_short_text}")
        print(f"Failed: {failed}")
        return

    model = get_model()
    embeddings: np.ndarray = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,
        batch_size=8,
    )
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings.astype(np.float32))
    save_index_and_metadata(index, metadatas)

    print()
    print("=== INDEX SUMMARY ===")
    print(f"Scanned: {scanned}")
    print(f"Indexed: {indexed}")
    print(f"Skipped (missing text): {skipped_missing_text}")
    print(f"Skipped (short text): {skipped_short_text}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
