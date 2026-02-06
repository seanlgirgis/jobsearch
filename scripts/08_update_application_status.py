#!/usr/bin/env python3
"""
scripts/08_update_application_status.py

Phase 8 in POC pipeline:
Track job application status, dates, notes, follow-ups.
Updates metadata.yaml in the job folder.

Subcommands:
  apply     - Record new application
  status    - Update status + optional note
  show      - Display current status & history
  list-pending - Show all jobs with pending follow-ups

Usage examples:
  python scripts/08_update_application_status.py --uuid cdb9a3fa apply --date 2026-02-05 --method "Company Site" --notes "Tailored cover attached"
  python scripts/08_update_application_status.py --uuid cdb9a3fa status --new-status "Interview Scheduled" --notes "Feb 12 phone screen"
  python scripts/08_update_application_status.py --uuid cdb9a3fa show
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime
import sys

JOB_ROOT = Path("data/jobs")


def resolve_job_folder(uuid_str: str) -> Path:
    uuid_str = uuid_str.strip()
    job_dir = JOB_ROOT / uuid_str
    if job_dir.is_dir():
        return job_dir
    candidates = list(JOB_ROOT.glob(f"*_{uuid_str}*"))
    if not candidates:
        short = uuid_str[:8]
        candidates = list(JOB_ROOT.glob(f"*_{short}*"))
    if len(candidates) == 1:
        print(f"Resolved → {candidates[0].name}")
        return candidates[0]
    elif len(candidates) > 1:
        print("Ambiguous UUID — matches:")
        for c in candidates:
            print(f"  - {c.name}")
        sys.exit(1)
    else:
        print(f"No job folder found for '{uuid_str}'")
        sys.exit(1)


def load_metadata(job_dir: Path) -> dict:
    meta_path = job_dir / "metadata.yaml"
    if not meta_path.is_file():
        print(f"metadata.yaml not found: {meta_path}")
        sys.exit(1)
    with open(meta_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_metadata(job_dir: Path, data: dict):
    meta_path = job_dir / "metadata.yaml"
    with open(meta_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    print(f"Updated: {meta_path}")


def cmd_apply(args):
    job_dir = resolve_job_folder(args.uuid)
    meta = load_metadata(job_dir)

    today = datetime.now().strftime("%Y-%m-%d")
    apply_date = args.date or today

    application = meta.setdefault("application", {})
    application["applied"] = True
    application["applied_date"] = apply_date
    application["applied_method"] = args.method
    application["application_notes"] = args.notes or ""

    if args.followup_date:
        application["followup_date"] = args.followup_date

    # Append to history
    history = application.setdefault("history", [])
    history.append({
        "date": apply_date,
        "status": "Applied",
        "notes": args.notes or f"Applied via {args.method}"
    })

    save_metadata(job_dir, meta)
    print(f"Application recorded: {apply_date} via {args.method}")


def cmd_status(args):
    job_dir = resolve_job_folder(args.uuid)
    meta = load_metadata(job_dir)

    today = datetime.now().strftime("%Y-%m-%d")
    new_status = args.new_status.strip().upper()

    application = meta.setdefault("application", {})
    application["last_status"] = new_status
    application["last_status_date"] = today

    # Append to history
    history = application.setdefault("history", [])
    entry = {
        "date": today,
        "status": new_status,
        "notes": args.notes or ""
    }
    history.append(entry)

    if args.followup_date:
        application["followup_date"] = args.followup_date

    save_metadata(job_dir, meta)
    print(f"Status updated to: {new_status}")


def cmd_show(args):
    job_dir = resolve_job_folder(args.uuid)
    meta = load_metadata(job_dir)

    application = meta.get("application", {})
    if not application.get("applied"):
        print("No application recorded yet.")
        return

    print("Application Status:")
    print(f"  Applied:        {application.get('applied_date', '—')}")
    print(f"  Method:         {application.get('applied_method', '—')}")
    print(f"  Notes:          {application.get('application_notes', '—')}")
    print(f"  Current status: {application.get('last_status', 'Applied')}")
    print(f"  Last updated:   {application.get('last_status_date', '—')}")
    if application.get("followup_date"):
        print(f"  Follow-up due:  {application['followup_date']}")

    history = application.get("history", [])
    if history:
        print("\nHistory:")
        for entry in history:
            print(f"  {entry['date']} → {entry['status']}")
            if entry.get("notes"):
                print(f"      {entry['notes']}")


def cmd_list_pending(args):
    pending = []
    for folder in JOB_ROOT.iterdir():
        if not folder.is_dir():
            continue
        meta_path = folder / "metadata.yaml"
        if not meta_path.is_file():
            continue
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f) or {}
        app = meta.get("application", {})
        if app.get("applied") and app.get("followup_date"):
            pending.append((folder.name, app["followup_date"], meta.get("job_title", "—")))

    if not pending:
        print("No jobs with pending follow-ups.")
        return

    print("Pending follow-ups:")
    for folder, date, title in sorted(pending, key=lambda x: x[1]):
        print(f"  {date} | {title} | {folder}")


def main():
    parser = argparse.ArgumentParser(description="Phase 8: Update job application status & tracking")
    parser.add_argument("--uuid", required=True, help="Job UUID or short prefix")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # apply
    apply_parser = subparsers.add_parser("apply", help="Record new application")
    apply_parser.add_argument("--date", help="Application date (YYYY-MM-DD), default today")
    apply_parser.add_argument("--method", required=True, help="How applied (e.g. LinkedIn, Company Site)")
    apply_parser.add_argument("--notes", help="Optional notes")
    apply_parser.add_argument("--followup-date", help="Optional follow-up date (YYYY-MM-DD)")
    apply_parser.set_defaults(func=cmd_apply)

    # status
    status_parser = subparsers.add_parser("status", help="Update application status")
    status_parser.add_argument("--new-status", required=True, help="New status (e.g. Interview Scheduled)")
    status_parser.add_argument("--notes", help="Optional notes")
    status_parser.add_argument("--followup-date", help="Optional new follow-up date")
    status_parser.set_defaults(func=cmd_status)

    # show
    show_parser = subparsers.add_parser("show", help="Show current status & history")
    show_parser.set_defaults(func=cmd_show)

    # list-pending
    list_parser = subparsers.add_parser("list-pending", help="List jobs with pending follow-ups")
    list_parser.set_defaults(func=cmd_list_pending)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()