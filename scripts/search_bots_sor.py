"""Refresh or require the search-bot source of record. No LLM calls. Bots do not edit master files."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_runtime_profile import (  # noqa: E402
    PROFILE_PATH,
    REPORT_PATH,
    RuntimeProfileError,
    build_profile,
    canonical,
)

AUDIT = Path("data/search_bots/audit/sor_refresh.jsonl")


def _audit(root: Path, action: str, ok: bool, detail: str) -> None:
    path = root / AUDIT
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "action": action,
        "ok": ok,
        "detail": detail,
        "runtime_profile": PROFILE_PATH.as_posix(),
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def refresh(root: Path) -> str:
    """Rebuild candidate_profile_runtime.json from master sources."""
    profile, report = build_profile(root, root.parent / "Grok_DIRECTOR")
    content = canonical(profile) + b"\n"
    (root / PROFILE_PATH).write_bytes(content)
    (root / REPORT_PATH).write_text(report, encoding="utf-8", newline="\n")
    detail = f"{len(content)} bytes; {len(profile['bullet_bank'])} bullets"
    _audit(root, "refresh", True, detail)
    return detail


def require_fresh(root: Path) -> str:
    """Fail if runtime SoR is missing or does not match a rebuild from master."""
    profile, report = build_profile(root, root.parent / "Grok_DIRECTOR")
    content = canonical(profile) + b"\n"
    output, report_file = root / PROFILE_PATH, root / REPORT_PATH
    if not output.is_file() or not report_file.is_file():
        raise RuntimeProfileError("Runtime SoR missing. Run: .\\search_bots\\refresh_sor.ps1")
    if output.read_bytes() != content or report_file.read_text(encoding="utf-8") != report:
        raise RuntimeProfileError(
            "Runtime SoR is stale (on-disk profile != rebuild from master files). "
            "Master yaml/skills/LTM notes/rules/profile builder changed since last refresh."
        )
    detail = f"fresh; {len(content)} bytes"
    _audit(root, "require", True, detail)
    return detail


def ensure_fresh(root: Path) -> str:
    """Deploy path: rebuild runtime SoR if missing or stale, then continue."""
    try:
        return require_fresh(root)
    except RuntimeProfileError as error:
        _audit(root, "ensure", False, str(error))
        detail = refresh(root)
        require_fresh(root)
        return f"auto-refreshed after stale/missing SoR; {detail}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--require",
        action="store_true",
        help="Check freshness only (what each site bot runs first). No writes to the profile.",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.require:
            detail = require_fresh(root)
            print(f"SoR fresh: {detail}")
        else:
            detail = refresh(root)
            require_fresh(root)
            print(f"SoR refreshed: {detail}")
        return 0
    except RuntimeProfileError as error:
        _audit(root, "require" if args.require else "refresh", False, str(error))
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
