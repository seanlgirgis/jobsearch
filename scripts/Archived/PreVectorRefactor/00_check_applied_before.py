#!/usr/bin/env python3
"""
scripts/00_check_applied_before.py

Phase 0: Semantic Duplicate Check
Compares new job description against indexed past jobs using FAISS + sentence-transformers.

Usage:
    python scripts/00_check_applied_before.py intake/new-job.md [--threshold 0.85] [--top-k 5]
"""

import argparse
import sys
import yaml
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import faiss
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip install faiss-cpu sentence-transformers")
    sys.exit(1)

# ──────────────────────────────────────────────── Constants ─────
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
PROJECT_ROOT = Path(__file__).parent.parent
INDEX_PATH   = PROJECT_ROOT / "data" / "job_index" / "faiss_job_descriptions.index"
META_PATH    = PROJECT_ROOT / "data" / "job_index" / "jobs_metadata.yaml"
MIN_TEXT_LEN = 100
DEFAULT_THRESHOLD = 0.82
DEFAULT_TOP_K    = 5

def load_index_and_metadata() -> Tuple[faiss.Index, List[Dict]]:
    if not INDEX_PATH.exists() or not META_PATH.exists():
        print(f"⚠️ Index/metadata not found in {INDEX_PATH.parent}")
        print("   Run: python scripts/utils/build_job_index.py --rebuild")
        sys.exit(1)

    index = faiss.read_index(str(INDEX_PATH))
    with META_PATH.open(encoding="utf-8") as f:
        metadata = yaml.safe_load(f) or []

    if index.ntotal != len(metadata):
        print(f"❌ Index/metadata mismatch: {index.ntotal} vectors vs {len(metadata)} entries")
        print("   Rebuild required: python scripts/utils/build_job_index.py --rebuild")
        sys.exit(1)

    return index, metadata


def load_intake_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    text = path.read_text(encoding="utf-8").strip()
    if len(text) < MIN_TEXT_LEN:
        print(f"⚠️ Warning: Input text is short ({len(text)} chars) – results may be unreliable.")
    return text


def get_embedding(text: str) -> np.ndarray:
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    emb = model.encode([text], normalize_embeddings=True)
    return emb.astype(np.float32)


def check_duplicates(
    new_text: str,
    index: faiss.Index,
    metadata: List[Dict],
    threshold: float,
    top_k: int
) -> bool:
    emb = get_embedding(new_text)
    distances, indices = index.search(emb, top_k)

    print(f"\n🔍 Query against {index.ntotal} past jobs (threshold {threshold:.2f}, showing top {top_k})")
    print(f"{'Sim':<8} | {'Apply Date':<12} | {'Company':<20} | {'Role':<30} | {'UUID':<10} | {'Status':<10}")
    print("-" * 100)

    found_duplicate = False
    for i in range(top_k):
        score = distances[0][i]
        idx = indices[0][i]
        if idx == -1:
            continue

        meta = metadata[idx]
        is_dupe = score >= threshold
        flag = "🔴 DUPE" if is_dupe else ""

        if is_dupe:
            found_duplicate = True

        company = (meta.get("company", "Unknown"))[:18]
        role    = (meta.get("role",    "Unknown"))[:28]
        uuid    = meta.get("uuid",     "????")[:8]
        date    = meta.get("apply_date", "N/A")
        status  = meta.get("status",   "Unknown")[:8]

        print(f"{score:.4f} | {date:<12} | {company:<20} | {role:<30} | {uuid} | {status} {flag}")

    print("-" * 100)

    if found_duplicate:
        print(f"\n❌ Duplicate likely (≥ {threshold:.2f})")
        return True
    else:
        print("\n✅ No strong duplicates found.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Semantic duplicate check before pipeline")
    parser.add_argument("intake_file", help="Path to new job markdown file")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Similarity threshold (default: {DEFAULT_THRESHOLD})")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K,
                        help=f"Number of top matches to show (default: {DEFAULT_TOP_K})")

    args = parser.parse_args()

    index, metadata = load_index_and_metadata()
    text = load_intake_text(args.intake_file)

    is_duplicate = check_duplicates(text, index, metadata, args.threshold, args.top_k)

    sys.exit(1 if is_duplicate else 0)


if __name__ == "__main__":
    main()