"""Tell Sean: OneDrive event always; email if SMTP is configured in .env."""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

ALERT_TO = "seanlgirgis@gmail.com"


def write_event_file(root: Path, dest_root: Path | None, title: str, body: str) -> Path:
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    text = f"{title}\n{body}\n"
    local_dir = root / "data" / "search_bots" / "logs" / "events"
    local_dir.mkdir(parents=True, exist_ok=True)
    local = local_dir / f"{stamp}.txt"
    local.write_text(text, encoding="utf-8")
    if dest_root is not None and dest_root.exists():
        remote = dest_root / "indeed" / "EVENTS"
        try:
            remote.mkdir(parents=True, exist_ok=True)
            (remote / local.name).write_text(text, encoding="utf-8")
        except OSError:
            pass
    return local


def send_email(subject: str, body: str) -> str:
    """Return 'sent', 'skipped:no-smtp', or 'failed:...'."""
    host = (os.environ.get("SMTP_HOST") or "").strip()
    if not host:
        return "skipped:no-smtp"
    port = int(os.environ.get("SMTP_PORT") or "587")
    user = (os.environ.get("SMTP_USER") or "").strip()
    password = os.environ.get("SMTP_PASSWORD") or ""
    mail_from = (os.environ.get("EMAIL_FROM") or user or ALERT_TO).strip()
    mail_to = (os.environ.get("EMAIL_TO") or ALERT_TO).strip()
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port, timeout=20) as smtp:
            smtp.starttls()
            if user:
                smtp.login(user, password)
            smtp.send_message(msg)
        return "sent"
    except OSError as error:
        return f"failed:{error}"


def alert(root: Path, dest_root: Path | None, title: str, body: str) -> dict[str, str]:
    path = write_event_file(root, dest_root, title, body)
    mail = send_email(title, body + f"\n\nEvent file: {path}")
    return {"event_file": str(path), "email": mail}
