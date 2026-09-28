"""SQLite hub: phrases (round-robin), DNA, events. Export CSV so Sean can open it in Excel."""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DB = Path("data/search_bots/schedule.sqlite")
TERMS = Path("search_bots/terms.json")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(moment: datetime | None = None) -> str:
    return (moment or utc_now()).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(root: Path) -> sqlite3.Connection:
    path = root / DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS phrases (
            id INTEGER PRIMARY KEY,
            pack TEXT NOT NULL,
            query TEXT NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            last_started TEXT,
            last_finished TEXT,
            last_status TEXT,
            next_due TEXT,
            UNIQUE(pack, query)
        );
        CREATE TABLE IF NOT EXISTS dna_record (
            dna TEXT PRIMARY KEY,
            payload TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS dna_alias (
            alias TEXT PRIMARY KEY,
            dna TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            ts TEXT NOT NULL,
            kind TEXT NOT NULL,
            detail TEXT NOT NULL
        );
        """
    )
    conn.commit()
    return conn


def log_event(root: Path, kind: str, detail: dict[str, Any] | str) -> None:
    payload = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    conn = connect(root)
    try:
        conn.execute(
            "INSERT INTO events (ts, kind, detail) VALUES (?, ?, ?)",
            (iso(), kind, payload),
        )
        conn.commit()
    finally:
        conn.close()


def sync_phrases(root: Path, conn: sqlite3.Connection | None = None) -> int:
    own = conn is None
    conn = conn or connect(root)
    catalog = json.loads((root / TERMS).read_text(encoding="utf-8"))
    wanted: set[tuple[str, str]] = set()
    now = iso()
    for pack, queries in (catalog.get("categories") or {}).items():
        for query in queries:
            wanted.add((pack, query))
            conn.execute(
                """
                INSERT INTO phrases (pack, query, enabled, next_due)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(pack, query) DO UPDATE SET enabled = 1
                """,
                (pack, query, now),
            )
    for row in conn.execute("SELECT id, pack, query FROM phrases"):
        if (row["pack"], row["query"]) not in wanted:
            conn.execute("UPDATE phrases SET enabled = 0 WHERE id = ?", (row["id"],))
    conn.commit()
    if own:
        conn.close()
    return len(wanted)


def interval_hours(root: Path) -> float:
    cfg = json.loads((root / "config" / "search_bots.json").read_text(encoding="utf-8"))
    polite = cfg.get("polite") or {}
    return float(polite.get("hours_between_phrases") or 12)


def claim_next(root: Path) -> dict | None:
    """Pick the next due phrase. Does not mark it complete; next_due moves only on success."""
    conn = connect(root)
    try:
        sync_phrases(root, conn)
        now = utc_now()
        row = conn.execute(
            """
            SELECT * FROM phrases
            WHERE enabled = 1 AND (next_due IS NULL OR next_due <= ?)
            ORDER BY next_due ASC, id ASC
            LIMIT 1
            """,
            (iso(now),),
        ).fetchone()
        if row is None:
            return None
        conn.execute(
            "UPDATE phrases SET last_started = ?, last_status = 'running' WHERE id = ?",
            (iso(now), row["id"]),
        )
        conn.commit()
        log_event(root, "claim", {"id": row["id"], "pack": row["pack"], "query": row["query"]})
        return {"id": row["id"], "pack": row["pack"], "query": row["query"]}
    finally:
        conn.close()


def mark_success(root: Path, phrase_id: int) -> None:
    hours = interval_hours(root)
    due = utc_now() + timedelta(hours=hours)
    conn = connect(root)
    try:
        conn.execute(
            """
            UPDATE phrases
            SET last_finished = ?, last_status = 'ok', next_due = ?
            WHERE id = ?
            """,
            (iso(), iso(due), phrase_id),
        )
        conn.commit()
    finally:
        conn.close()
    log_event(root, "phrase_ok", {"id": phrase_id, "next_due": iso(due)})


def mark_blocked(root: Path, phrase_id: int, reason: str) -> None:
    """Do not consume the 12-hour cycle. Retry in one hour; other phrases can run meanwhile."""
    due = utc_now() + timedelta(hours=1)
    conn = connect(root)
    try:
        conn.execute(
            """
            UPDATE phrases
            SET last_status = 'blocked', next_due = ?
            WHERE id = ?
            """,
            (iso(due), phrase_id),
        )
        conn.commit()
    finally:
        conn.close()
    log_event(root, "phrase_blocked", {"id": phrase_id, "reason": reason, "retry": iso(due)})


def dna_lookup(root: Path, aliases: list[str]) -> dict[str, Any] | None:
    conn = connect(root)
    try:
        for alias in aliases:
            row = conn.execute(
                "SELECT r.payload FROM dna_alias a JOIN dna_record r ON r.dna = a.dna WHERE a.alias = ?",
                (alias,),
            ).fetchone()
            if row:
                return json.loads(row["payload"])
        return None
    finally:
        conn.close()


def dna_remember(root: Path, dna: str, aliases: list[str], record: dict[str, Any]) -> None:
    payload = json.dumps(record, ensure_ascii=False)
    conn = connect(root)
    try:
        conn.execute(
            """
            INSERT INTO dna_record (dna, payload, updated_at) VALUES (?, ?, ?)
            ON CONFLICT(dna) DO UPDATE SET payload = excluded.payload, updated_at = excluded.updated_at
            """,
            (dna, payload, iso()),
        )
        for alias in aliases:
            conn.execute(
                """
                INSERT INTO dna_alias (alias, dna) VALUES (?, ?)
                ON CONFLICT(alias) DO UPDATE SET dna = excluded.dna
                """,
                (alias, dna),
            )
        conn.commit()
    finally:
        conn.close()


def export_csv(root: Path, dest_root: Path | None = None) -> list[Path]:
    """Excel-friendly dumps so Sean does not need a SQLite GUI."""
    out_dir = root / "data" / "search_bots" / "logs" / "db_export"
    out_dir.mkdir(parents=True, exist_ok=True)
    conn = connect(root)
    written: list[Path] = []
    tables = {
        "phrases": "SELECT * FROM phrases ORDER BY next_due, id",
        "dna_record": "SELECT dna, updated_at, payload FROM dna_record ORDER BY updated_at DESC",
        "dna_alias": "SELECT alias, dna FROM dna_alias ORDER BY alias",
        "events": "SELECT id, ts, kind, detail FROM events ORDER BY id DESC LIMIT 500",
    }
    try:
        for name, sql in tables.items():
            rows = conn.execute(sql).fetchall()
            path = out_dir / f"{name}.csv"
            with path.open("w", encoding="utf-8-sig", newline="") as handle:
                if not rows:
                    handle.write("")
                else:
                    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(dict(row))
            written.append(path)
            if dest_root is not None and dest_root.exists():
                remote = dest_root / "indeed" / "db_export"
                try:
                    remote.mkdir(parents=True, exist_ok=True)
                    (remote / path.name).write_bytes(path.read_bytes())
                except OSError:
                    pass
    finally:
        conn.close()
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--sync", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--export", action="store_true", help="Write CSVs you can open in Excel")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    conn = connect(root)
    n = sync_phrases(root, conn)
    print(f"phrases enabled={n} db={root / DB}")
    if args.status or not (args.export or args.sync):
        for row in conn.execute(
            "SELECT pack, query, last_status, next_due FROM phrases WHERE enabled=1 ORDER BY next_due"
        ):
            print(
                f"  [{row['pack']}] {row['query']}  {row['last_status'] or '-'}  due={row['next_due']}"
            )
    conn.close()
    if args.export:
        dest = None
        local = root / "config" / "search_bots.local.json"
        if local.is_file():
            raw = json.loads(local.read_text(encoding="utf-8")).get("handoff_root")
            if raw and Path(raw).exists():
                dest = Path(raw)
        paths = export_csv(root, dest)
        print("exported:")
        for path in paths:
            print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
