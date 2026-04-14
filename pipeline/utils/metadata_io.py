"""Small helpers for pipeline metadata I/O."""

from pathlib import Path
from typing import Any, Dict

import yaml


def load_metadata(path: Path) -> Dict[str, Any]:
    """Load metadata.yaml as a dict."""
    if not path.is_file():
        raise FileNotFoundError(f"metadata file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"metadata is not a mapping: {path}")
    return data


def save_metadata(path: Path, metadata: Dict[str, Any]) -> None:
    """Write metadata.yaml preserving key order."""
    path.write_text(
        yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

