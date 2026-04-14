"""Hashing helpers for pipeline steps."""

import hashlib


def compute_sha256(text: str) -> str:
    """Return the SHA-256 hex digest for the given text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

