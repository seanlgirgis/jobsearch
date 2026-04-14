"""
scripts/utils/vector_ops.py

Shared utilities for vector operations:
- Loading the SentenceTransformer model
- Generating embeddings
- Loading/Saving FAISS index and metadata

Usage:
    from scripts.utils.vector_ops import get_embedding, load_index_and_metadata, save_index_and_metadata
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import yaml
import numpy as np

# Configure paths relative to project root
# (Assumes this file is in scripts/utils/)
PROJECT_ROOT = Path(__file__).parent.parent.parent
INDEX_DIR = PROJECT_ROOT / "data" / "job_index"
INDEX_PATH = INDEX_DIR / "faiss_job_descriptions.index"
METADATA_PATH = INDEX_DIR / "jobs_metadata.yaml"
DEFAULT_EMBEDDING_MODEL = os.getenv("STUDYBOOK_EMBEDDING_MODEL") or os.getenv("DEFAULT_EMBEDDING_MODEL") or "all-MiniLM-L6-v2"
LOCAL_MODEL_DIR = PROJECT_ROOT / "models" / "sentence-transformers" / "all-MiniLM-L6-v2"
EMBEDDING_MODEL_NAME = str(LOCAL_MODEL_DIR) if LOCAL_MODEL_DIR.exists() else DEFAULT_EMBEDDING_MODEL
LOCAL_ONLY = (os.getenv("STUDYBOOK_EMBEDDING_LOCAL_ONLY", "1").strip().lower() in ("1", "true", "yes", "y", "on"))

# Lazy-loaded model to avoid overhead if not needed
_MODEL = None

def get_model():
    """Lazy load the SentenceTransformer model."""
    global _MODEL
    if _MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME, local_files_only=LOCAL_ONLY)
        except ImportError:
            raise RuntimeError("sentence-transformers not installed")
        except Exception as e:
            if LOCAL_ONLY:
                raise RuntimeError(
                    f"Embedding model not available locally ({EMBEDDING_MODEL_NAME}). "
                    "Run one-time model preload or disable local-only mode."
                ) from e
            raise
    return _MODEL

def get_embedding(text: str) -> np.ndarray:
    """Generate normalized embedding for a single text string."""
    model = get_model()
    # normalize_embeddings=True is critical for Cosine Similarity via Inner Product
    emb = model.encode([text], normalize_embeddings=True)
    return emb.astype(np.float32)

def load_index_and_metadata() -> Tuple[Optional[object], List[Dict]]:
    """
    Load FAISS index and metadata.
    Returns (index, metadata_list).
    If index/meta missing, returns (None, []).
    """
    if not METADATA_PATH.exists():
        return None, []

    metadata: List[Dict] = []
    try:
        with METADATA_PATH.open("r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f) or []
    except Exception as e:
        print(f"⚠️ Error loading metadata: {e}")
        metadata = []

    if not INDEX_PATH.exists():
        return None, metadata

    try:
        import faiss
        index = faiss.read_index(str(INDEX_PATH))
        return index, metadata
    except ImportError:
        print("⚠️ FAISS not available; semantic duplicate check disabled.")
        return None, metadata
    except Exception as e:
        print(f"⚠️ Error loading index: {e}")
        return None, metadata

def save_index_and_metadata(index: object, metadata: List[Dict]) -> None:
    """Save FAISS index and metadata to disk."""
    import faiss
    
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    
    faiss.write_index(index, str(INDEX_PATH))
    
    with METADATA_PATH.open("w", encoding="utf-8") as f:
        yaml.dump(metadata, f, allow_unicode=True, sort_keys=False)

def verify_integrity(index, metadata) -> bool:
    """Check if index size matches metadata count."""
    if not index:
        return True # Empty is valid-ish
    return index.ntotal == len(metadata)
