"""
gmail_scanner.py — Scan Gmail for job-related emails and produce a daily digest.

Usage:
    python scripts/gmail_scanner.py

Reads:  data/jobs/*/metadata.yaml  (company names + statuses)
Writes: data/gmail_digest.md

Requires auth token from: python scripts/gmail_auth.py
"""

import os
import re
import base64
import glob
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES       = ["https://www.googleapis.com/auth/gmail.readonly"]
REPO_ROOT    = Path(__file__).resolve().parent.parent
TOKEN_PATH   = REPO_ROOT / "data" / "gmail_token.json"
DIGEST_PATH  = REPO_ROOT / "data" / "gmail_digest.md"
JOBS_GLOB    = str(REPO_ROOT / "data" / "jobs" / "*" / "metadata.yaml")
LOOKBACK_DAYS = 30

# Keywords that signal something needs attention
ACTION_KEYWORDS = [
    "interview", "phone screen", "video call", "technical assessment",
    "coding challenge", "offer", "offer letter", "next steps",
    "schedule", "availability", "follow up", "follow-up",
    "rejected", "rejection", "unfortunately", "not moving forward",
    "thank you for applying", "application received", "we regret",
    "would like to", "pleased to", "congratulations",
]


# ── Load jobs ────────────────────────────────────────────────────────────────

def load_jobs() -> list[dict]:
    jobs = []
    for path in glob.glob(JOBS_GLOB):
        with open(path, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        if meta and meta.get("company"):
            jobs.append({
                "job_id":  meta.get("job_id", ""),
                "company": meta.get("company", "").strip(),
                "role":    meta.get("role", ""),
                "status":  meta.get("status", ""),
                "applied": meta.get("application", {}).get("applied", False),
            })
    return jobs


# ── Gmail auth ───────────────────────────────────────────────────────────────

def get_credentials() -> Credentials:
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(
            f"Token not found at {TOKEN_PATH}.\n"
            "Run first: python scripts/gmail_auth.py"
        )
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


# ── Gmail fetch ──────────────────────────────────────────────────────────────

def fetch_recent_messages(service, days: int = LOOKBACK_DAYS) -> list[dict]:
    after = (datetime.utcnow() - timedelta(days=days)).strftime("%Y/%m/%d")
    query = f"after:{after}"
    result = service.users().messages().list(userId="me", q=query, maxResults=200).execute()
    messages = result.get("messages", [])
    full = []
    for msg in messages:
        detail = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["Subject", "From", "Date"]
        ).execute()
        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        full.append({
            "id":      msg["id"],
            "subject": headers.get("Subject", "(no subject)"),
            "from":    headers.get("From", ""),
            "date":    headers.get("Date", ""),
            "snippet": detail.get("snippet", ""),
        })
    return full


# ── Matching ─────────────────────────────────────────────────────────────────

def match_email_to_job(email: dict, jobs: list[dict]) -> dict | None:
    text = f"{email['subject']} {email['from']} {email['snippet']}".lower()
    for job in jobs:
        if job["company"].lower() in text:
            return job
    return None


def detect_action_needed(email: dict) -> str | None:
    text = f"{email['subject']} {email['snippet']}".lower()
    for kw in ACTION_KEYWORDS:
        if kw in text:
            return kw
    return None


def is_job_related(email: dict) -> bool:
    text = f"{email['subject']} {email['snippet']}".lower()
    triggers = [
        "job", "position", "role", "opportunity", "application", "applied",
        "hiring", "recruiter", "talent", "career", "resume", "interview",
        "offer", "rejected", "linkedin", "indeed", "glassdoor",
    ]
    return any(t in text for t in triggers)


# ── Digest writer ─────────────────────────────────────────────────────────────

def write_digest(matched: dict, unmatched: list[dict]) -> None:
    lines = [
        f"# Gmail Job Search Digest",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Lookback: last {LOOKBACK_DAYS} days",
        "",
    ]

    if matched:
        lines.append("## Matched Jobs\n")
        for job_id, data in sorted(matched.items()):
            job   = data["job"]
            emails = data["emails"]
            lines.append(f"### {job['company']} — {job['role']}")
            lines.append(f"Status: `{job['status']}`  |  Applied: {'✅' if job['applied'] else '❌'}")
            lines.append("")
            for e in emails:
                action = detect_action_needed(e)
                flag = f" ⚠️ **ACTION: {action}**" if action else ""
                lines.append(f"- **{e['date'][:16]}** | {e['subject']}{flag}")
                lines.append(f"  > {e['snippet'][:120]}")
            lines.append("")
    else:
        lines.append("## Matched Jobs\n")
        lines.append("_No emails matched existing job applications._\n")

    lines.append("---\n")
    lines.append("## Unmatched Job-Related Emails\n")
    if unmatched:
        lines.append("_Emails that look job-related but don't match a tracked company:_\n")
        for e in unmatched:
            action = detect_action_needed(e)
            flag = f" ⚠️ **{action}**" if action else ""
            lines.append(f"- **{e['date'][:16]}** | From: {e['from'][:50]}")
            lines.append(f"  Subject: {e['subject']}{flag}")
            lines.append(f"  > {e['snippet'][:120]}")
            lines.append("")
    else:
        lines.append("_None found._\n")

    DIGEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DIGEST_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Loading job metadata...")
    jobs = load_jobs()
    print(f"  {len(jobs)} jobs loaded")

    print("Connecting to Gmail...")
    creds   = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    print(f"Fetching emails (last {LOOKBACK_DAYS} days)...")
    emails = fetch_recent_messages(service)
    print(f"  {len(emails)} emails fetched")

    # Bucket emails
    matched: dict = {}    # job_id → {job, emails[]}
    unmatched: list = []

    for email in emails:
        job = match_email_to_job(email, jobs)
        if job:
            jid = job["job_id"]
            if jid not in matched:
                matched[jid] = {"job": job, "emails": []}
            matched[jid]["emails"].append(email)
        elif is_job_related(email):
            unmatched.append(email)

    write_digest(matched, unmatched)

    # Summary
    action_count = sum(
        1 for data in matched.values()
        for e in data["emails"]
        if detect_action_needed(e)
    ) + sum(1 for e in unmatched if detect_action_needed(e))

    print(f"\n✅ Digest written to: {DIGEST_PATH}")
    print(f"   Matched jobs with emails : {len(matched)}")
    print(f"   Unmatched job-related    : {len(unmatched)}")
    print(f"   Items needing action     : {action_count}")
    if action_count:
        print(f"   ⚠️  Open digest and review flagged items")


if __name__ == "__main__":
    main()
