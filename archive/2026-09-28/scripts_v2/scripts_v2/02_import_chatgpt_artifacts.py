#!/usr/bin/env python3
"""
Import ChatGPT artifact outputs into the active manual-v2 job folder.

Supports either:
- FILE block format:
    === FILE: tailored_data_v1.yaml ===
    ...
    === END FILE ===
- Raw B1 score markdown (saved to score/score_report_manual_v1.md)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

JOB_ROOT = Path("data/jobs")
CACHE_PATH = Path(".job_cache_v2.json")

FILE_BLOCK_RE = re.compile(
    r"===\s*FILE:\s*(?P<name>.+?)\s*===\s*(?P<body>.*?)\s*===\s*END FILE\s*===",
    flags=re.IGNORECASE | re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import ChatGPT file-block artifacts into job folder.")
    parser.add_argument("--uuid", help="Job UUID or short prefix. Defaults to .job_cache_v2.json")
    parser.add_argument("--input", dest="input_path", help="Text file containing ChatGPT response.")
    parser.add_argument("--from-clipboard", action="store_true", help="Read ChatGPT response from clipboard.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing non-empty files.")
    return parser.parse_args()


def resolve_job_folder(uuid_str: str) -> Path:
    ref = uuid_str.strip()
    job_dir = JOB_ROOT / ref
    if job_dir.is_dir():
        return job_dir
    candidates = list(JOB_ROOT.glob(f"*_{ref}*"))
    if not candidates:
        short = ref[:8]
        candidates = list(JOB_ROOT.glob(f"*_{short}*"))
    if len(candidates) == 1:
        print(f"Resolved -> {candidates[0].name}")
        return candidates[0]
    if len(candidates) > 1:
        raise ValueError(f"Ambiguous UUID reference: {uuid_str}")
    raise ValueError(f"No job folder found for '{uuid_str}'")


def job_from_cache() -> Path:
    if not CACHE_PATH.is_file():
        raise ValueError("No .job_cache_v2.json found; provide --uuid.")
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    folder = cache.get("job_folder", "")
    if not folder:
        raise ValueError(".job_cache_v2.json missing job_folder; provide --uuid.")
    job_dir = Path(folder)
    if not job_dir.is_dir():
        raise ValueError(f"Cached job_folder not found: {job_dir}")
    return job_dir


def read_clipboard_text() -> str:
    # PowerShell clipboard read for Windows.
    cmd = ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed reading clipboard: {result.stderr.strip()}")
    return result.stdout


def read_input_text(args: argparse.Namespace) -> str:
    if args.input_path:
        return Path(args.input_path).read_text(encoding="utf-8")
    if args.from_clipboard:
        return read_clipboard_text()
    raise ValueError("Provide --input <file> or --from-clipboard.")


def clean_body(text: str) -> str:
    body = text.strip()
    # Strip optional code fences if present inside a file block.
    if body.startswith("```") and body.endswith("```"):
        lines = body.splitlines()
        if len(lines) >= 2:
            body = "\n".join(lines[1:-1]).strip()
    return body


def extract_file_blocks(text: str) -> List[Tuple[str, str]]:
    blocks: List[Tuple[str, str]] = []
    for match in FILE_BLOCK_RE.finditer(text):
        name = match.group("name").strip()
        body = clean_body(match.group("body"))
        blocks.append((name, body))
    return blocks


def target_path(job_dir: Path, filename: str) -> Path | None:
    lower = filename.lower()
    if lower == "tailored_data_v1.yaml":
        return job_dir / "tailored" / "tailored_data_v1.yaml"
    if lower == "resume_intermediate_v1.json":
        return job_dir / "generated" / "resume_intermediate_v1.json"
    if lower == "cover_intermediate_v1.json":
        return job_dir / "generated" / "cover_intermediate_v1.json"
    if lower in ("score_report.md", "score_report_manual_v1.md"):
        return job_dir / "score" / "score_report_manual_v1.md"
    return None


def write_artifact(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0 and not force:
        raise ValueError(f"Refusing overwrite non-empty file without --force: {path}")
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def maybe_import_raw_score(text: str, job_dir: Path, force: bool) -> bool:
    # If no file blocks, allow direct B1 markdown import.
    if "## Match Score:" in text and "## Recommendation:" in text:
        out = job_dir / "score" / "score_report_manual_v1.md"
        write_artifact(out, text.strip(), force=force)
        print(f"Imported raw score markdown -> {out}")
        return True
    return False


def main() -> None:
    args = parse_args()
    job_dir = resolve_job_folder(args.uuid) if args.uuid else job_from_cache()
    text = read_input_text(args)

    blocks = extract_file_blocks(text)
    if not blocks:
        if maybe_import_raw_score(text, job_dir, force=args.force):
            return
        raise ValueError("No FILE blocks found. Expected format: === FILE: <name> === ... === END FILE ===")

    imported: Dict[str, Path] = {}
    skipped: List[str] = []

    for name, body in blocks:
        dest = target_path(job_dir, name)
        if dest is None:
            skipped.append(name)
            continue
        write_artifact(dest, body, force=args.force)
        imported[name] = dest

    if not imported:
        raise ValueError(f"No recognized artifact file names found in blocks. Skipped: {', '.join(skipped)}")

    print("=== IMPORT COMPLETE ===")
    print(f"Job folder: {job_dir}")
    for name, dest in imported.items():
        size = dest.stat().st_size if dest.exists() else 0
        print(f"- {name} -> {dest} ({size} bytes)")
    if skipped:
        print(f"Skipped unrecognized blocks: {', '.join(skipped)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Import failed: {exc}")
        sys.exit(1)

