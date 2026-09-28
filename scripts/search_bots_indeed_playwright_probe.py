"""Playwright Indeed probe: one search, try one job, write a report. No DNA/eval."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "search_bots" / "logs"
QUERY = "capacity planning python"
SEARCH = f"https://www.indeed.com/jobs?q={QUERY.replace(' ', '+')}&l=remote"


def blocked(text: str) -> bool:
    blob = text.lower()
    return any(
        token in blob
        for token in ("authenticating...", "additional verification", "captcha", "access denied")
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict = {"query": QUERY, "search_url": SEARCH, "steps": []}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(25000)
        try:
            page.goto(SEARCH, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            html = page.content()
            (OUT / "indeed_pw_search.html").write_text(html, encoding="utf-8", errors="replace")
            keys = sorted(set(re.findall(r"[?&]jk=([a-fA-F0-9]{10,})", html)))
            cards = page.locator("a[data-jk], a.jcs-JobTitle, [data-jk]")
            search_row = {
                "step": "search",
                "url": page.url,
                "title": page.title(),
                "bytes": len(html),
                "jk_count": len(keys),
                "jk_sample": keys[:3],
                "locator_count": cards.count(),
                "blocked": blocked(html + " " + page.title()),
            }
            report["steps"].append(search_row)
            if keys and not search_row["blocked"]:
                jk = keys[0]
                page.goto(f"https://www.indeed.com/viewjob?jk={jk}", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                more = page.get_by_role("button", name=re.compile(r"more|see more", re.I))
                if more.count():
                    more.first.click(timeout=3000)
                    page.wait_for_timeout(500)
                job_html = page.content()
                (OUT / "indeed_pw_job.html").write_text(job_html, encoding="utf-8", errors="replace")
                desc = page.locator("#jobDescriptionText")
                desc_text = desc.inner_text() if desc.count() else ""
                report["steps"].append(
                    {
                        "step": "viewjob",
                        "jk": jk,
                        "url": page.url,
                        "title": page.title(),
                        "has_description": bool(desc_text.strip()),
                        "description_chars": len(desc_text.strip()),
                        "blocked": blocked(job_html + " " + page.title()),
                    }
                )
        except PlaywrightTimeout as error:
            report["error"] = f"timeout: {error}"
        finally:
            browser.close()
    (OUT / "indeed_pw_probe_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    search = report["steps"][0] if report.get("steps") else {}
    job = report["steps"][1] if len(report.get("steps", [])) > 1 else {}
    ok = (search.get("jk_count") or 0) > 0 and not search.get("blocked") and job.get("description_chars", 0) > 200
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
