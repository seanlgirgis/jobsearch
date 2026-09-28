"""One-shot Indeed probe: search, try to open one job, report what HTML we actually got."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "search_bots" / "logs"
SEARCH = "https://www.indeed.com/jobs"
QUERY = "capacity planning python remote"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def title_of(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "(no title)"


def job_keys(html: str) -> list[str]:
    return sorted(set(re.findall(r"[?&]jk=([a-fA-F0-9]{10,})", html)))


def blocked(html: str, status: int) -> bool:
    blob = html.lower()
    if status in {401, 403, 429}:
        return True
    return any(
        token in blob
        for token in ("captcha", "additional verification", "access denied", "blocked")
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict = {"query": QUERY, "search_url": SEARCH, "steps": []}
    with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=25.0) as client:
        search = client.get(SEARCH, params={"q": QUERY, "l": "remote"})
        (OUT / "indeed_probe_search.html").write_text(search.text, encoding="utf-8", errors="replace")
        keys = job_keys(search.text)
        search_row = {
            "step": "search",
            "http": search.status_code,
            "final_url": str(search.url),
            "bytes": len(search.text),
            "title": title_of(search.text),
            "jk_count": len(keys),
            "jk_sample": keys[:3],
            "blocked": blocked(search.text, search.status_code),
        }
        report["steps"].append(search_row)
        if keys and not search_row["blocked"]:
            jk = keys[0]
            job = client.get("https://www.indeed.com/viewjob", params={"jk": jk})
            (OUT / "indeed_probe_job.html").write_text(job.text, encoding="utf-8", errors="replace")
            soup = BeautifulSoup(job.text, "html.parser")
            desc = soup.select_one("#jobDescriptionText")
            report["steps"].append(
                {
                    "step": "viewjob",
                    "jk": jk,
                    "http": job.status_code,
                    "bytes": len(job.text),
                    "title": title_of(job.text),
                    "has_description_div": bool(desc),
                    "description_chars": len(desc.get_text(" ", strip=True)) if desc else 0,
                    "blocked": blocked(job.text, job.status_code),
                }
            )
    (OUT / "indeed_probe_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    search_ok = report["steps"][0]["jk_count"] > 0 and not report["steps"][0]["blocked"]
    job_ok = len(report["steps"]) > 1 and report["steps"][1].get("description_chars", 0) > 200
    return 0 if search_ok and job_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
