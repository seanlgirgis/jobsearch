"""Local disk is canonical. OneDrive is a replica flushed in batches."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

QUEUE = Path("data/search_bots/handoff_queue.json")
READY = Path("data/search_bots/ready")
LOGS = Path("data/search_bots/logs")


def _load_queue(root: Path) -> list[dict[str, str]]:
    path = root / QUEUE
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return list(data) if isinstance(data, list) else []


def _save_queue(root: Path, rows: list[dict[str, str]]) -> None:
    path = root / QUEUE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def enqueue(root: Path, src: Path, dest_rel: str) -> None:
    rows = _load_queue(root)
    item = {"src": str(src), "dest_rel": dest_rel}
    if item not in rows:
        rows.append(item)
        _save_queue(root, rows)


def copy_one(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())


def flush_handoff(root: Path, dest_root: Path | None) -> dict[str, Any]:
    """Copy queued + standard artifacts to OneDrive. Never deletes local files."""
    result = {"ok": 0, "failed": 0, "skipped": 0, "error": None}
    if dest_root is None or not dest_root.exists():
        result["error"] = "handoff_root missing"
        return result
    rows = _load_queue(root)
    leftover: list[dict[str, str]] = []
    for row in rows:
        src = Path(row["src"])
        dest = dest_root / row["dest_rel"]
        if not src.is_file():
            result["skipped"] += 1
            continue
        try:
            copy_one(src, dest)
            result["ok"] += 1
        except OSError:
            leftover.append(row)
            result["failed"] += 1
    _save_queue(root, leftover)
    extras = [
        (root / READY / "indeed" / "Apply", dest_root / "indeed" / "Apply"),
        (root / READY / "indeed" / "Wait", dest_root / "indeed" / "Wait"),
        (root / LOGS / "indeed_ledger.csv", dest_root / "indeed" / "ledger.csv"),
        (root / LOGS / "runs", dest_root / "indeed" / "logs"),
    ]
    for src, dest in extras:
        try:
            if src.is_file():
                copy_one(src, dest)
                result["ok"] += 1
            elif src.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                logs = sorted(src.glob("indeed_run_*.log"), key=lambda p: p.stat().st_mtime)
                for item in logs[-5:]:
                    copy_one(item, dest / item.name)
                    result["ok"] += 1
        except OSError as error:
            result["failed"] += 1
            result["error"] = str(error)
    return result
