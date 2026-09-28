"""Indeed guinea-pig bot: require fresh SoR, DNA-skip repeats, OpenRouter eval, two files."""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_runtime_profile import PROFILE_PATH, canonical, digest  # noqa: E402
from scripts.search_bots_dna import (  # noqa: E402
    indeed_jk,
    lookup,
    remember,
    text_dna,
    utc_now,
)
from scripts.search_bots_handoff import enqueue, flush_handoff  # noqa: E402
from scripts.search_bots_filters import (  # noqa: E402
    indeed_fromage_days,
    is_excluded,
    pay_skip_reason,
)
from scripts.search_bots_sor import ensure_fresh, require_fresh  # noqa: E402
from src.ai.llm_client import LLMClient, LLMError  # noqa: E402
from src.pipeline.contracts import (  # noqa: E402
    ANALYSIS_PROMPT,
    ANALYSIS_SCHEMA,
    PROMPT_VERSION,
)
from src.pipeline.local_gate import paid_job_text  # noqa: E402

SITE_ID = "indeed"
INBOX = Path("search_bots/sites/indeed/inbox")
READY = Path("data/search_bots/ready")
LOGS = Path("data/search_bots/logs")
RUNS = LOGS / "runs"
KEEP_RUN_LOGS = 5
CHECKPOINT = Path("data/search_bots/indeed_checkpoint.json")
CONFIG = Path("config/search_bots.json")
LEDGER_FIELDS = [
    "human_processed",
    "category",
    "score",
    "search_pack",
    "verdict",
    "company",
    "title",
    "location",
    "salary",
    "job_url",
    "indeed_jk",
    "search_query",
    "recommendation",
    "dna",
    "stem",
    "job_md",
    "eval_json",
    "captured_at",
    "prompt_tokens",
    "completion_tokens",
    "actual_usd",
]


def load_config(root: Path) -> dict[str, Any]:
    return json.loads((root / CONFIG).read_text(encoding="utf-8"))


def handoff_root(root: Path) -> Path | None:
    local = root / "config" / "search_bots.local.json"
    if local.is_file():
        overlay = json.loads(local.read_text(encoding="utf-8"))
        raw = overlay.get("handoff_root")
        if raw:
            path = Path(raw)
            return path if path.exists() else None
    cfg_path = root / CONFIG
    if not cfg_path.is_file():
        return None
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")).get("output") or {}
    raw = cfg.get("handoff_root")
    if not raw:
        return None
    path = Path(raw)
    return path if path.exists() else None


def write_handoff_note(root: Path, filename: str, text: str) -> Path | None:
    local = root / LOGS / filename
    local.parent.mkdir(parents=True, exist_ok=True)
    local.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    dest_rel = f"{SITE_ID}/{filename}"
    dest_root = handoff_root(root)
    try:
        if dest_root is None:
            raise OSError("handoff offline")
        dest = dest_root / SITE_ID / filename
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(local.read_bytes())
        return dest
    except OSError:
        enqueue(root, local, dest_rel)
        return local


def copy_to_handoff(
    root: Path, ready_dir: Path, stem: str, decision: str
) -> Path | None:
    dest_root = handoff_root(root)
    dest: Path | None = None
    for suffix in (".job.md", ".eval.json"):
        src = ready_dir / f"{stem}{suffix}"
        if not src.is_file():
            continue
        dest_rel = f"{SITE_ID}/{decision}/{src.name}"
        try:
            if dest_root is None:
                raise OSError("handoff offline")
            dest = dest_root / SITE_ID / decision
            dest.mkdir(parents=True, exist_ok=True)
            (dest / src.name).write_bytes(src.read_bytes())
        except OSError:
            enqueue(root, src, dest_rel)
    return dest


def verdict(analysis: dict[str, Any], root: Path | None = None) -> str:
    rec = (analysis.get("recommendation") or "").upper()
    score = analysis.get("score")
    score = int(score) if isinstance(score, int) else 0
    rules = (load_config(root or ROOT).get("evaluation") or {}).get("verdicts") or {}
    apply_min = int(rules.get("apply_min_score") or 80)
    wait_min = int(rules.get("wait_min_score") or 60)
    if rec == "SKIP" or score < wait_min:
        return "Reject"
    if score >= apply_min:
        return "Apply"
    return "Wait"


def file_stem(
    analysis: dict[str, Any], company: str | None, dna: str, *, root: Path | None = None
) -> str:
    score = analysis.get("score")
    score_part = f"{int(score):03d}" if isinstance(score, int) else "xxx"
    stamp = utc_now().replace("-", "").replace(":", "")
    date, time = stamp[:8], stamp[9:15]
    return f"{score_part}_{verdict(analysis, root)}_{date}_{time}_{slug(company)}_{dna[:8]}"


def slug(value: str | None) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", (value or "unknown").lower()).strip("-")
    return text[:40] or "unknown"


def keep_job(analysis: dict[str, Any], *, root: Path | None = None) -> bool:
    return verdict(analysis, root) in {"Apply", "Wait"}


def load_term_queries(root: Path, site_id: str = SITE_ID) -> list[dict[str, str]]:
    catalog = json.loads(
        (root / "search_bots" / "terms.json").read_text(encoding="utf-8")
    )
    categories = catalog.get("categories") or {}
    site_path = root / "search_bots" / "sites" / site_id / "site.json"
    site = (
        json.loads(site_path.read_text(encoding="utf-8")) if site_path.is_file() else {}
    )
    wanted = site.get("term_packs") or ["*"]
    names = list(categories) if "*" in wanted or not wanted else wanted
    rows: list[dict[str, str]] = []
    for pack in names:
        for query in categories.get(pack) or []:
            rows.append({"pack": pack, "query": query})
    return rows


def parse_capture(text: str) -> dict[str, Any]:
    url = None
    match = re.search(r"https?://\S*indeed\.[^\s\)]+", text, re.I)
    if match:
        url = match.group(0).rstrip(".,;")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = None
    company = None
    for index, line in enumerate(lines[:12]):
        if re.match(r"(?i)^title\s*:", line):
            title = line.split(":", 1)[1].strip() or None
        if re.match(r"(?i)^(company|employer)\s*:", line):
            company = line.split(":", 1)[1].strip() or None
            if not title and index + 1 < len(lines):
                candidate = lines[index + 1]
                if not re.match(r"(?i)^(?:https?://|salary:|location:|\$)", candidate):
                    title = re.sub(r"(?i)^title\s*:\s*", "", candidate)
    if not title:
        title = next(
            (
                line
                for line in lines
                if not re.match(
                    r"(?i)^(?:indeed(?:\.com)?$|https?://|company:|employer:|salary:|location:)",
                    line,
                )
            ),
            None,
        )
    salary = None
    for line in lines:
        if re.search(r"(?i)(?:\$\s*\d|\bUSD\s*\d)", line) and len(line) < 200:
            salary = re.sub(r"(?i)^salary\s*:\s*", "", line)
            break
    return {
        "job_url": url,
        "title": title,
        "company": company,
        "salary": salary,
        "job_description": text.strip(),
    }


def load_runtime(root: Path) -> tuple[dict[str, Any], str]:
    profile = json.loads((root / PROFILE_PATH).read_text(encoding="utf-8"))
    return profile, digest(canonical(profile))


def evaluate(
    root: Path, job_text: str, profile: dict[str, Any], factory=None
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    client = (
        factory("economy")
        if factory
        else LLMClient("economy", config_dir=root / "config", env_file=root / ".env")
    )
    payload = {"job": paid_job_text(job_text), "profile": profile}
    raw = client.chat(
        [
            {"role": "system", "content": ANALYSIS_PROMPT},
            {"role": "user", "content": canonical(payload).decode("utf-8")},
        ],
        json_schema=ANALYSIS_SCHEMA,
        schema_name="job_analysis",
    )
    return json.loads(raw), getattr(client, "last_usage", None)


def ledger_paths(root: Path) -> list[Path]:
    return [root / LOGS / "indeed_ledger.csv"]


def append_ledger(root: Path, row: dict[str, Any]) -> None:
    dna = str(row.get("dna") or "")
    for path in ledger_paths(root):
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = set()
        new_file = not path.is_file()
        if path.is_file():
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                for item in csv.DictReader(handle):
                    if item.get("dna"):
                        existing.add(item["dna"])
        if dna and dna in existing:
            continue
        with path.open("a", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=LEDGER_FIELDS, extrasaction="ignore"
            )
            if new_file:
                writer.writeheader()
            writer.writerow({key: row.get(key, "") for key in LEDGER_FIELDS})


def write_pair(
    root: Path,
    *,
    capture: dict[str, Any],
    analysis: dict[str, Any],
    dna: str,
    query: str | None,
    category: str | None = None,
    usage: dict[str, Any] | None = None,
) -> str:
    company = analysis.get("company") or capture.get("company") or "unknown"
    stem = file_stem(analysis, company, dna, root=root)
    pack = category or "uncategorized"
    label = verdict(analysis, root)
    ready = root / READY / SITE_ID / label
    ready.mkdir(parents=True, exist_ok=True)
    job_md = "\n".join(
        [
            "---",
            f"site: {SITE_ID}",
            f"company: {company}",
            f"title: {analysis.get('title') or capture.get('title')}",
            f"captured_at: {utc_now()}",
            f"job_hash: {dna}",
            f"job_url: {capture.get('job_url')}",
            f"location: {analysis.get('location')}",
            f"salary: {capture.get('salary')}",
            "hiring_person: null",
            f"search_query: {query}",
            f"category: {label}",
            f"search_pack: {pack}",
            f"score: {analysis.get('score')}",
            f"recommendation: {analysis.get('recommendation')}",
            "---",
            "",
            f"# {analysis.get('title') or capture.get('title')} — {company}",
            "",
            f"- URL: {capture.get('job_url')}",
            f"- Salary: {capture.get('salary')}",
            f"- Location: {analysis.get('location')}",
            f"- Match: {analysis.get('score')}/100 ({analysis.get('recommendation')})",
            f"- Why: {analysis.get('fit_rationale')}",
            "",
            "## Job description",
            "",
            capture["job_description"],
            "",
        ]
    )
    eval_doc = {
        "schema": "job_analysis",
        "prompt_version": PROMPT_VERSION,
        "model_profile": "economy",
        "job_hash": dna,
        "site": SITE_ID,
        "captured_at": utc_now(),
        "indeed_jk": indeed_jk(capture.get("job_url")),
        "category": label,
        "search_pack": pack,
        "usage": usage,
        "analysis": analysis,
    }
    job_path = ready / f"{stem}.job.md"
    eval_path = ready / f"{stem}.eval.json"
    job_path.write_text(job_md, encoding="utf-8", newline="\n")
    eval_path.write_text(
        json.dumps(eval_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    handoff_dir = copy_to_handoff(root, ready, stem, label)
    usage = usage or {}
    append_ledger(
        root,
        {
            "human_processed": "N",
            "category": label,
            "score": analysis.get("score"),
            "search_pack": pack,
            "verdict": label,
            "company": company,
            "title": analysis.get("title") or capture.get("title"),
            "location": analysis.get("location"),
            "salary": capture.get("salary"),
            "job_url": capture.get("job_url"),
            "indeed_jk": indeed_jk(capture.get("job_url")),
            "search_query": query,
            "recommendation": analysis.get("recommendation"),
            "dna": dna,
            "stem": stem,
            "job_md": str((handoff_dir / job_path.name) if handoff_dir else job_path),
            "eval_json": str(
                (handoff_dir / eval_path.name) if handoff_dir else eval_path
            ),
            "captured_at": utc_now(),
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "actual_usd": usage.get("actual_usd"),
        },
    )
    return stem


def rotate_run_logs(folder: Path, keep: int = KEEP_RUN_LOGS) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    files = sorted(folder.glob("indeed_run_*.log"), key=lambda path: path.stat().st_mtime, reverse=True)
    for stale in files[keep:]:
        stale.unlink(missing_ok=True)


def open_run_log(root: Path) -> Path:
    folder = root / RUNS
    rotate_run_logs(folder)
    stamp = utc_now().replace("-", "").replace(":", "")
    path = folder / f"indeed_run_{stamp}.log"
    path.write_text("", encoding="utf-8")
    return path


class RunLog:
    def __init__(self, path: Path):
        self.path = path
        self._fh = path.open("a", encoding="utf-8")

    def line(self, message: str) -> None:
        self._fh.write(message.rstrip() + "\n")
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()


def load_checkpoint(root: Path) -> dict[str, Any] | None:
    path = root / CHECKPOINT
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def save_checkpoint(root: Path, pack: str, query: str, remaining: int) -> None:
    path = root / CHECKPOINT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "ts": utc_now(),
                "last_completed_pack": pack,
                "last_completed_query": query,
                "remaining": remaining,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def clear_checkpoint(root: Path) -> None:
    path = root / CHECKPOINT
    if path.is_file():
        path.unlink()


def counts_toward_limit(status: str) -> bool:
    """DNA hits are already known; they must not eat -Limit."""
    return status != "dna_hit"


def append_dev_log(root: Path, row: dict[str, Any]) -> None:
    line = json.dumps({"ts": utc_now(), **row}, ensure_ascii=False)
    path = root / LOGS / "indeed_dev.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    dest = handoff_root(root)
    if dest is not None:
        note = dest / SITE_ID / "DEV_LOG.txt"
        note.parent.mkdir(parents=True, exist_ok=True)
        with note.open("a", encoding="utf-8") as handle:
            handle.write(
                f"{row.get('status','?'):12} limit={str(row.get('toward_limit')):5} "
                f"[{row.get('pack')}] {row.get('jk') or '-'} {row.get('query')}\n"
            )


def log_line(root: Path, event: str, detail: dict[str, Any]) -> None:
    path = root / LOGS / "indeed.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"ts": utc_now(), "site": SITE_ID, "event": event, **detail}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def process_text(
    root: Path,
    text: str,
    *,
    query: str | None = None,
    category: str | None = None,
    factory=None,
    pay: bool = True,
) -> dict[str, Any]:
    require_fresh(root)
    capture = parse_capture(text)
    if len((capture.get("job_description") or "").strip()) < 80:
        log_line(root, "too_short", {"url": capture.get("job_url")})
        if capture.get("job_url"):
            remember(
                root,
                job_text=capture["job_description"] or capture.get("job_url") or "short",
                url=capture.get("job_url"),
                record={
                    "dna": text_dna(capture["job_description"] or capture["job_url"]),
                    "site": SITE_ID,
                    "kept": False,
                    "eval_paid": False,
                    "excluded": "too_short",
                },
            )
        return {"status": "too_short", "paid": False, "record": None}
    existing = lookup(
        root, job_text=capture["job_description"], url=capture.get("job_url")
    )
    if existing:
        log_line(
            root,
            "dna_hit",
            {"dna": existing.get("dna"), "jk": existing.get("indeed_jk")},
        )
        return {"status": "dna_hit", "record": existing, "paid": False}
    reason = is_excluded(
        company=capture.get("company"), title=capture.get("title"), root=root
    )
    if not reason:
        reason = pay_skip_reason(
            title=capture.get("title"),
            salary_text=capture.get("salary"),
            query=query,
            root=root,
            job_text=capture["job_description"],
        )
    if reason:
        dna = text_dna(capture["job_description"])
        record = remember(
            root,
            job_text=capture["job_description"],
            url=capture.get("job_url"),
            record={
                "dna": dna,
                "site": SITE_ID,
                "title": capture.get("title"),
                "company": capture.get("company"),
                "kept": False,
                "eval_paid": False,
                "excluded": reason,
            },
        )
        log_line(root, "excluded", {"dna": dna, "reason": reason})
        return {"status": "excluded", "record": record, "paid": False, "reason": reason}
    dna = text_dna(capture["job_description"])
    if not pay:
        log_line(root, "dna_miss_unpaid", {"dna": dna})
        return {"status": "would_eval", "dna": dna, "paid": False}
    profile, _hash = load_runtime(root)
    try:
        analysis, usage = evaluate(
            root, capture["job_description"], profile, factory=factory
        )
    except LLMError as error:
        log_line(root, "eval_error", {"dna": dna, "error": str(error)[:240]})
        return {
            "status": "eval_error",
            "paid": True,
            "record": None,
            "error": str(error),
        }
    kept = keep_job(analysis, root=root)
    stem = None
    if kept:
        stem = write_pair(
            root,
            capture=capture,
            analysis=analysis,
            dna=dna,
            query=query,
            category=category,
            usage=usage,
        )
    record = remember(
        root,
        job_text=capture["job_description"],
        url=capture.get("job_url"),
        record={
            "dna": dna,
            "site": SITE_ID,
            "title": analysis.get("title") or capture.get("title"),
            "company": analysis.get("company") or capture.get("company"),
            "score": analysis.get("score"),
            "recommendation": analysis.get("recommendation"),
            "kept": kept,
            "ready_stem": stem,
            "eval_paid": True,
            "usage": usage,
        },
    )
    log_line(
        root, "evaluated", {"dna": dna, "kept": kept, "stem": stem, "usage": usage}
    )
    spend = root / LOGS / "spend.jsonl"
    spend.parent.mkdir(parents=True, exist_ok=True)
    with spend.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "ts": utc_now(),
                    "site": SITE_ID,
                    "dna": dna,
                    "stem": stem,
                    "usage": usage,
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    return {
        "status": "evaluated",
        "record": record,
        "paid": True,
        "kept": kept,
        "stem": stem,
        "verdict": verdict(analysis, root),
        "score": analysis.get("score"),
        "usage": usage,
    }


def inbox_files(root: Path) -> list[Path]:
    folder = root / INBOX
    if not folder.is_dir():
        return []
    skip = {"readme.md", "capture_template.md"}
    return sorted(
        p
        for p in folder.glob("*.md")
        if p.name.lower() not in skip
        and "PASTE_JOB_KEY_HERE" not in p.read_text(encoding="utf-8-sig")
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--file", type=Path, help="One Indeed capture markdown")
    parser.add_argument(
        "--inbox", action="store_true", help="Process sites/indeed/inbox/*.md"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="SoR + DNA only; no OpenRouter"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Headed Chrome: search Indeed, click cards, then DNA/eval",
    )
    parser.add_argument(
        "--limit", type=int, default=1, help="Live mode: max jobs this run (all terms)"
    )
    parser.add_argument(
        "--query",
        default=None,
        help="One Indeed query. Default: iterate all term packs on the Indeed site.",
    )
    parser.add_argument(
        "--fromage",
        type=int,
        default=None,
        help="Indeed fromage days (default: config recency)",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Ignore checkpoint; start at the first search phrase",
    )
    parser.add_argument(
        "--scheduled",
        action="store_true",
        help="Hourly fire: sync terms.json, run the next due phrase only (12h before same phrase repeats)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.live:
        from scripts.search_bots_indeed_live import (
            CloudflareHalt,
            capture_jobs,
            capture_to_markdown,
        )

        scheduled_id = None
        claimed = None
        if args.scheduled:
            from scripts.search_bots_schedule import claim_next

            claimed = claim_next(root)
            if claimed is None:
                print("No phrase due. Next hour, or check: python scripts\\search_bots_schedule.py --status")
                return 0
            scheduled_id = claimed["id"]
            print(f"Scheduled phrase: [{claimed['pack']}] {claimed['query']}")

        run_path = open_run_log(root)
        runlog = RunLog(run_path)
        print(f"Indeed live started. Log: {run_path}")
        runlog.line(f"start {utc_now()} limit={args.limit} query={args.query or '*'} scheduled={scheduled_id}")

        if claimed is not None:
            queries = [{"pack": claimed["pack"], "query": claimed["query"]}]
        elif args.query:
            queries = [{"pack": "cli", "query": args.query}]
        else:
            queries = load_term_queries(root)
        if not queries:
            print(
                "No search terms. Edit search_bots/terms.json or pass --query.",
                file=sys.stderr,
            )
            runlog.close()
            return 2
        try:
            runlog.line(ensure_fresh(root))
        except Exception as error:
            note = (
                f"{utc_now()} FAILED\n"
                f"SoR could not be refreshed.\n{error}\n"
                "Fix master career files or run .\\search_bots\\refresh_sor.ps1 then retry.\n"
            )
            write_handoff_note(root, "LAST_ERROR.txt", note)
            write_handoff_note(root, "BOT_STATUS.txt", note)
            print(f"SoR: {error}", file=sys.stderr)
            runlog.line(f"FATAL SoR {error}")
            runlog.close()
            return 2
        flush_handoff(root, handoff_root(root))
        write_handoff_note(
            root,
            "BOT_STATUS.txt",
            f"{utc_now()} RUNNING\nlimit={args.limit} fromage={args.fromage or 'config'}\nlog={run_path}\n",
        )
        paid = not args.dry_run
        remaining = max(1, args.limit)
        fromage = (
            args.fromage if args.fromage is not None else indeed_fromage_days(root)
        )
        seen = 0
        dna_hits = 0
        written = 0
        apply_n = 0
        wait_n = 0
        by_status: dict[str, int] = {}
        usd = 0.0
        polite = load_config(root).get("polite") or {}
        one_term = bool(polite.get("one_term_per_run", True))
        profile = root / str(polite.get("chrome_profile") or "data/search_bots/chrome_profile")
        cf_wait = int(polite.get("cloudflare_wait_sec") or 300)
        sleep_range = polite.get("sleep_between_terms_sec") or [180, 300]
        resume = None if args.fresh else load_checkpoint(root)
        last_pack = (resume or {}).get("last_completed_pack")
        last_query = (resume or {}).get("last_completed_query")
        skipping = bool(last_query and not args.query)
        if skipping:
            runlog.line(f"resume after completed [{last_pack}] {last_query}")
        first_term = True
        for item in queries:
            if remaining <= 0:
                break
            if skipping:
                if item.get("pack") == last_pack and item.get("query") == last_query:
                    skipping = False
                runlog.line(f"skip completed term [{item['pack']}] {item['query']}")
                continue
            if not first_term and not one_term:
                lo, hi = float(sleep_range[0]), float(sleep_range[-1])
                pause = random.uniform(min(lo, hi), max(lo, hi))
                runlog.line(f"pause {pause:.1f}s between terms")
                time.sleep(pause)
            first_term = False
            runlog.line(f"TERM [{item['pack']}] {item['query']} (need {remaining})")
            try:
                captures = capture_jobs(
                    query=item["query"],
                    limit=remaining,
                    fromage_days=fromage,
                    log_dir=root / LOGS,
                    log=runlog.line,
                    profile_dir=profile,
                    cloudflare_wait_sec=cf_wait,
                    click_sleep_sec=tuple(polite.get("click_sleep_sec") or [4, 8]),
                )
            except CloudflareHalt as error:
                runlog.line(f"CLOUDFLARE_HALT {item['query']}: {error}")
                write_handoff_note(
                    root,
                    "LAST_ERROR.txt",
                    f"{utc_now()} CLOUDFLARE_HALT\nquery={item['query']}\n{error}\n"
                    "Sign in to Indeed in Chrome. Do not keep launching searches.\n",
                )
                write_handoff_note(root, "BOT_STATUS.txt", f"{utc_now()} FAILED Cloudflare\n")
                if scheduled_id is not None:
                    from scripts.search_bots_notify import alert
                    from scripts.search_bots_schedule import mark_blocked

                    mark_blocked(root, scheduled_id, str(error))
                    alert(
                        root,
                        handoff_root(root),
                        "Indeed bot blocked (Cloudflare)",
                        f"Phrase not marked complete.\n[{item.get('pack')}] {item.get('query')}\n{error}\n",
                    )
                runlog.close()
                print("Stopped: Cloudflare. Phrase NOT marked done. Check OneDrive EVENTS / email.")
                print(f"Log: {run_path}")
                return 2
            except Exception as error:
                runlog.line(f"CAPTURE_FAIL {item['query']}: {error}")
                write_handoff_note(
                    root,
                    "LAST_ERROR.txt",
                    f"{utc_now()} CAPTURE_FAIL\nquery={item['query']}\n{error}\n",
                )
                continue
            for capture in captures:
                if remaining <= 0:
                    break
                try:
                    result = process_text(
                        root,
                        capture_to_markdown(capture),
                        query=item["query"],
                        category=item.get("pack"),
                        pay=paid,
                    )
                except Exception as error:
                    result = {"status": "error", "paid": False, "error": str(error)}
                extra = result.get("reason") or result.get("error") or ""
                status = result.get("status") or "error"
                toward = counts_toward_limit(status)
                runlog.line(
                    f"  {capture.get('indeed_jk')}: {status} paid={result.get('paid')} "
                    f"limit={'yes' if toward else 'no'} "
                    f"score={result.get('score')} {extra}"
                )
                append_dev_log(
                    root,
                    {
                        "pack": item.get("pack"),
                        "query": item.get("query"),
                        "jk": capture.get("indeed_jk"),
                        "status": status,
                        "toward_limit": toward,
                        "paid": result.get("paid"),
                        "kept": result.get("kept"),
                        "stem": result.get("stem"),
                    },
                )
                by_status[status] = by_status.get(status, 0) + 1
                usage = result.get("usage") or {}
                if usage.get("actual_usd") is not None:
                    usd += float(usage["actual_usd"])
                if status == "dna_hit":
                    dna_hits += 1
                if toward:
                    remaining -= 1
                    seen += 1
                if result.get("kept"):
                    written += 1
                    if result.get("verdict") == "Apply":
                        apply_n += 1
                    elif result.get("verdict") == "Wait":
                        wait_n += 1
            save_checkpoint(root, item["pack"], item["query"], remaining)
            if one_term:
                runlog.line("one_term_per_run: stopping after this phrase")
                break
        if seen == 0 and dna_hits == 0:
            note = (
                f"{utc_now()} FAILED\nLive capture returned no jobs.\n"
                "Check Indeed block/CAPTCHA, fromage window, or terms.json.\n"
            )
            write_handoff_note(root, "LAST_ERROR.txt", note)
            write_handoff_note(root, "BOT_STATUS.txt", note)
            runlog.line("FAILED no jobs captured")
            runlog.close()
            print("Live capture returned no jobs.", file=sys.stderr)
            print(f"Log: {run_path}")
            return 2
        stats = [
            "--- stats ---",
            f"new (toward limit): {seen}",
            f"dna_hit: {dna_hits}",
            f"evaluated: {by_status.get('evaluated', 0)}",
            f"excluded: {by_status.get('excluded', 0)}",
            f"eval_error: {by_status.get('eval_error', 0)}",
            f"Apply written: {apply_n}",
            f"Wait written: {wait_n}",
            f"usd: {usd:.6f}",
            f"log: {run_path}",
        ]
        for line in stats:
            runlog.line(line)
        runlog.close()
        write_handoff_note(root, "LAST_RUN.log", run_path.read_text(encoding="utf-8"))
        flush_handoff(root, handoff_root(root))
        write_handoff_note(
            root,
            "BOT_STATUS.txt",
            f"{utc_now()} OK\nnew_toward_limit={seen}\ndna_hits={dna_hits}\n"
            f"written_apply={apply_n}\nwritten_wait={wait_n}\nusd={usd:.6f}\n"
            f"log={run_path}\n",
        )
        print("Indeed live done.")
        print("\n".join(stats))
        if not one_term:
            clear_checkpoint(root)
        if scheduled_id is not None:
            from scripts.search_bots_schedule import export_csv, mark_success

            mark_success(root, scheduled_id)
            export_csv(root, handoff_root(root))
        return 0
    paths = [args.file] if args.file else inbox_files(root)
    if not paths:
        inbox = root / INBOX
        print(
            "Inbox is empty (README.md is ignored). "
            f"Paste one Indeed job as a .md file into:\n  {inbox}\n"
            "Then rerun: .\\search_bots\\run_indeed.ps1\n"
            "Or: .\\search_bots\\run_indeed.ps1 -File path\\to\\job.md",
            file=sys.stderr,
        )
        return 2
    paid = not args.dry_run
    for path in paths:
        text = path.read_text(encoding="utf-8-sig")
        result = process_text(root, text, query=path.name, pay=paid)
        print(f"{path.name}: {result['status']} paid={result['paid']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
