#!/usr/bin/env python3
"""
scripts/utils/build_job_index.py

Utility script to (re)build a FAISS index and metadata cache for all past job descriptions.
This enables RAG-based features like duplicate checking in the JobSearch pipeline.

The script scans all job folders in data/jobs/, extracts the main job description text,
embeds it using sentence-transformers, and stores vectors in a FAISS index along with
YAML metadata for quick lookups.

Usage:
    python scripts/utils/build_job_index.py [--rebuild]

- --rebuild: Force a full rebuild even if index exists.

Standards followed:
- PEP 8 style.
- Strict type hints (PEP 484).
- Docstrings (Google style).
- Pathlib for file operations.
- UTF-8 encoding enforced.
- Idempotent: Safe to re-run.
- Error handling: Graceful skips for invalid folders; exit on critical failures.

Dependencies:
- faiss-cpu (or faiss-gpu)
- sentence-transformers
- numpy
- pyyaml

Install via: pip install faiss-cpu sentence-transformers numpy pyyaml
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import faiss
import numpy as np
import yaml
from sentence_transformers import SentenceTransformer

# ──────────────────────────────────────────────── CONFIG ─────
JOB_ROOT: Path = Path("data/jobs")
INDEX_DIR: Path = Path("data/job_index")
INDEX_PATH: Path = INDEX_DIR / "faiss_job_descriptions.index"
METADATA_PATH: Path = INDEX_DIR / "jobs_metadata.yaml"
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
MIN_TEXT_LENGTH: int = 100  # Skip very short/invalid descriptions

INDEX_DIR.mkdir(parents=True, exist_ok=True)
# ──────────────────────────────────────────────────────────────


def get_job_description_text(job_dir: Path) -> Optional[str]:
    """Extract the main job description text from a job folder.

    Prioritizes the canonical raw/job_description.md file.
    Falls back to any other .md file in the root folder (e.g., original intake).

    Args:
        job_dir: Path to the job folder (e.g., data/jobs/00016_5407d0d2).

    Returns:
        The cleaned text content if found, else None.

    Raises:
        UnicodeDecodeError: If file encoding fails (though UTF-8 is enforced).
    """
    # Priority 1: Canonical raw location
    canonical_path: Path = job_dir / "raw" / "job_description.md"
    if canonical_path.is_file():
        return canonical_path.read_text(encoding="utf-8").strip()

    # Priority 2: Any .md in job folder root
    md_files: List[Path] = list(job_dir.glob("*.md"))
    if md_files:
        # Sort by name or size if needed; for now, take the first
        selected_path: Path = md_files[0]
        return selected_path.read_text(encoding="utf-8").strip()

    print(f"⚠️ No valid .md description found in {job_dir.name}", file=sys.stderr)
    return None


def collect_job_data() -> Tuple[List[str], List[Dict[str, str]]]:
    """Collect job description texts and metadata from all job folders.

    Iterates over data/jobs/*, extracts text, and loads key metadata from metadata.yaml.

    Returns:
        A tuple of (texts, metadatas) where:
        - texts: List of job description strings ready for embedding.
        - metadatas: List of dicts with UUID, path, company, role, apply_date, status.

    Raises:
        ValueError: If no valid job folders are found.
    """
    job_folders: List[Path] = [p for p in JOB_ROOT.iterdir() if p.is_dir()]
    if not job_folders:
        raise ValueError(f"No job folders found in {JOB_ROOT}")

    print(f"ℹ️ Found {len(job_folders)} job folders. Collecting data...")

    texts: List[str] = []
    metadatas: List[Dict[str, str]] = []

    for job_dir in job_folders:
        text: Optional[str] = get_job_description_text(job_dir)
        if text is None or len(text) < MIN_TEXT_LENGTH:
            continue  # Skip invalid/short entries

        texts.append(text)

        meta_file: Path = job_dir / "metadata.yaml"
        meta: Dict = {}
        if meta_file.is_file():
            with meta_file.open(encoding="utf-8") as f:
                meta = yaml.safe_load(f) or {}

        description_path: str = "unknown"
        if (job_dir / "raw" / "job_description.md").exists():
            description_path = str(job_dir / "raw" / "job_description.md")
        elif list(job_dir.glob("*.md")):
            description_path = str(list(job_dir.glob("*.md"))[0])

        metadatas.append({
            "uuid": job_dir.name,
            "description_path": description_path,
            "company": meta.get("company", "Unknown"),
            "role": meta.get("role", "Unknown"),
            "apply_date": meta.get("application", {}).get("date", "N/A"),
            "status": meta.get("status", "Unknown"),
        })

    if not texts:
        raise ValueError("No valid job descriptions found across all folders.")

    return texts, metadatas


def build_index() -> None:
    """Build or rebuild the FAISS index and metadata YAML.

    Process:
    1. Collect texts and metadatas.
    2. Embed texts using sentence-transformers.
    3. Create and populate FAISS index (Inner Product for cosine similarity).
    4. Save index binary and metadata YAML.

    Prints progress and success checks.

    Raises:
        RuntimeError: If embedding or indexing fails.
    """
    print("🚀 Starting index build...")

    try:
        texts, metadatas = collect_job_data()
    except ValueError as e:
        print(f"❌ Data collection failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Collected {len(texts)} valid job descriptions.")

    try:
        model: SentenceTransformer = SentenceTransformer(EMBEDDING_MODEL_NAME)
        embeddings: np.ndarray = model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True,
            batch_size=8,  # Adjustable for memory
        )
        print(f"✅ Embedded {len(embeddings)} descriptions (dim: {embeddings.shape[1]}).")
    except Exception as e:
        raise RuntimeError(f"Embedding failed: {e}") from e

    try:
        dim: int = embeddings.shape[1]
        index: faiss.IndexFlatIP = faiss.IndexFlatIP(dim)
        index.add(embeddings.astype(np.float32))
        faiss.write_index(index, str(INDEX_PATH))
        print(f"💾 Saved FAISS index to {INDEX_PATH}.")
    except Exception as e:
        raise RuntimeError(f"FAISS indexing failed: {e}") from e

    try:
        with METADATA_PATH.open("w", encoding="utf-8") as f:
            yaml.dump(metadatas, f, allow_unicode=True, sort_keys=False)
        print(f"💾 Saved metadata YAML to {METADATA_PATH}.")
    except Exception as e:
        raise RuntimeError(f"Metadata save failed: {e}") from e

    print(f"\n✅ Build complete! Indexed {len(texts)} jobs successfully.")
    print(f"   - Index size: {INDEX_PATH.stat().st_size / 1024:.1f} KB")
    print(f"   - Metadata entries: {len(metadatas)}")


def main() -> None:
    """Main entry point: Parse args and trigger build if needed."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Build or rebuild job description FAISS index and metadata."
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force full rebuild (default: build only if missing).",
    )

    args: argparse.Namespace = parser.parse_args()

    if args.rebuild or not INDEX_PATH.exists() or not METADATA_PATH.exists():
        try:
            build_index()
        except RuntimeError as e:
            print(f"❌ Build failed: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"ℹ️ Index already exists at {INDEX_PATH} (use --rebuild to recreate).")
        sys.exit(0)


if __name__ == "__main__":
    main()