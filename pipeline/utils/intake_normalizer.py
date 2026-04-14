"""Text normalization helpers for intake content."""


def normalize_text(text: str) -> str:
    """Normalize intake text by trimming and collapsing whitespace."""
    return " ".join(text.strip().split())

