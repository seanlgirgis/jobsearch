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
import faiss
from pathlib import Path
from typing import List, Dict, Tuple

# ──────────────────────────────────────────────── Constants ─────
from scripts.utils.vector_ops import get_embedding, load_index_and_metadata

MIN_TEXT_LEN = 100
DEFAULT_THRESHOLD = 0.82
DEFAULT_TOP_K    = 5


def load_intake_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    text = path.read_text(encoding="utf-8").strip()
    # MIN_TEXT_LEN was removed, so this check is also removed.
    # if len(text) < MIN_TEXT_LEN:
    #     print(f"⚠️ Warning: Input text is short ({len(text)} chars) – results may be unreliable.")
    return text


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