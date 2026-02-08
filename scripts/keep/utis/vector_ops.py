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
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Lazy-loaded model to avoid overhead if not needed
_MODEL = None

def get_model():
    """Lazy load the SentenceTransformer model."""
    global _MODEL
    if _MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Suppress verbose output if possible
            _MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except ImportError:
            print("❌ Helper Error: sentence-transformers not installed.")
            sys.exit(1)
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
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        return None, []

    try:
        import faiss
        index = faiss.read_index(str(INDEX_PATH))
        
        with METADATA_PATH.open("r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f) or []
            
        return index, metadata
    except ImportError:
        print("❌ Helper Error: faiss-cpu not installed.")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ Error loading index: {e}")
        return None, []

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
