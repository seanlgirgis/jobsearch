"""Job DNA cache: never pay to evaluate the same posting twice."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from scripts.search_bots_schedule import dna_lookup, dna_remember
from src.pipeline.local_gate import job_hash, paid_job_text

CACHE = Path("data/search_bots/cache")
INDEX = CACHE / "index.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def indeed_jk(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urlparse(url.strip())
    query = parse_qs(parsed.query)
    raw = (query.get("jk") or [None])[0]
    if raw:
        return raw.strip()
    match = re.search(r"[?&]jk=([a-fA-F0-9]+)", url)
    return match.group(1) if match else None


def text_dna(job_text: str) -> str:
    return job_hash(paid_job_text(job_text))


def load_index(root: Path) -> dict[str, Any]:
    path = root / INDEX
    if not path.is_file():
        return {"by_dna": {}, "by_alias": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_index(root: Path, index: dict[str, Any]) -> None:
    path = root / INDEX
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record_path(root: Path, dna: str) -> Path:
    return root / CACHE / "dna" / f"{dna}.json"


def lookup(root: Path, *, job_text: str, url: str | None = None) -> dict[str, Any] | None:
    """Hit if this Indeed jk or this JD hash was already evaluated."""
    aliases = []
    jk = indeed_jk(url)
    if jk:
        aliases.append(f"indeed:jk:{jk}")
    aliases.append(f"hash:{text_dna(job_text)}")
    hit = dna_lookup(root, aliases)
    if hit:
        return hit
    index = load_index(root)
    for alias in aliases:
        dna = index.get("by_alias", {}).get(alias)
        if not dna:
            continue
        path = record_path(root, dna)
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    return None


def remember(
    root: Path,
    *,
    job_text: str,
    url: str | None,
    record: dict[str, Any],
) -> dict[str, Any]:
    dna = record.get("dna") or text_dna(job_text)
    record = {**record, "dna": dna, "job_url": url, "updated_at": utc_now()}
    record.setdefault("first_seen", record["updated_at"])
    path = record_path(root, dna)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    index = load_index(root)
    index.setdefault("by_dna", {})[dna] = path.as_posix()
    index.setdefault("by_alias", {})[f"hash:{dna}"] = dna
    jk = indeed_jk(url)
    if jk:
        index["by_alias"][f"indeed:jk:{jk}"] = dna
        record["indeed_jk"] = jk
        path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    save_index(root, index)
    aliases = [f"hash:{dna}"]
    if jk:
        aliases.append(f"indeed:jk:{jk}")
    dna_remember(root, dna, aliases, record)
    return record
