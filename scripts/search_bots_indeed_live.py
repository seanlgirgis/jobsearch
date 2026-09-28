"""Headed Chrome: Indeed search → click result card → expand JD. Not a naked viewjob URL."""

from __future__ import annotations

import json
import random
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

LOGS = Path("data/search_bots/logs")
DEFAULT_QUERY = "capacity planning python"
DEFAULT_LOCATION = "remote"
DESC_SELECTORS = (
    "#jobDescriptionText",
    "[id*='jobDescription']",
    "[class*='jobsearch-jobDescription']",
    "[class*='JobDescription']",
    "[data-testid*='jobDescription']",
    "#jobsearch-ViewjobPaneWrapper",
    ".jobsearch-RightPane",
)


def _click_see_more(page) -> None:
    for pattern in (r"see more", r"show more", r"^more$"):
        button = page.get_by_role("button", name=re.compile(pattern, re.I))
        if button.count():
            try:
                button.first.click(timeout=2500)
                page.wait_for_timeout(600)
                return
            except Exception:
                continue


def _first_text(page, selectors: tuple[str, ...], *, min_chars: int = 1) -> str:
    for selector in selectors:
        loc = page.locator(selector)
        if loc.count():
            text = loc.first.inner_text(timeout=4000).strip()
            if len(text) >= min_chars:
                return text
    return ""


def is_cloudflare(page) -> bool:
    blob = (page.title() + " " + page.url).lower()
    try:
        html = page.content()[:12000].lower()
    except Exception:
        html = ""
    tokens = (
        "additional verification required",
        "verify you are human",
        "just a moment",
        "cf-challenge",
        "attention required",
        "ray id",
    )
    return any(token in blob or token in html for token in tokens)


class CloudflareHalt(RuntimeError):
    """Indeed/Cloudflare wall. Do not continue to the next search phrase."""


def capture_jobs(
    *,
    query: str = DEFAULT_QUERY,
    location: str = DEFAULT_LOCATION,
    limit: int = 1,
    fromage_days: int = 1,
    log_dir: Path | None = None,
    log=None,
    profile_dir: Path | None = None,
    cloudflare_wait_sec: int = 300,
    click_sleep_sec: tuple[float, float] = (4.0, 8.0),
) -> list[dict[str, Any]]:
    """Open visible Chrome, search, click up to `limit` title links, return captures."""
    days = max(1, int(fromage_days))
    search_url = (
        f"https://www.indeed.com/jobs?q={quote_plus(query)}"
        f"&l={quote_plus(location)}&fromage={days}"
    )
    def _log(message: str) -> None:
        if log:
            log(message)

    out: list[dict[str, Any]] = []
    log_dir = log_dir or LOGS
    log_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        launch_kw = {"headless": False, "channel": "chrome"}
        context = None
        browser = None
        if profile_dir is not None:
            profile_dir.mkdir(parents=True, exist_ok=True)
            try:
                context = playwright.chromium.launch_persistent_context(
                    str(profile_dir), **launch_kw
                )
            except Exception:
                launch_kw.pop("channel", None)
                context = playwright.chromium.launch_persistent_context(
                    str(profile_dir), headless=False
                )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            try:
                browser = playwright.chromium.launch(**launch_kw)
            except Exception:
                browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
        page.set_default_timeout(30000)
        try:
            page.goto(search_url, wait_until="domcontentloaded")
            page.wait_for_timeout(3500)
            if is_cloudflare(page):
                _log(
                    f"CLOUDFLARE wall. Solve 'Verify you are human' in this window. "
                    f"Waiting {cloudflare_wait_sec}s. We will not click it."
                )
                deadline = time.time() + max(30, int(cloudflare_wait_sec))
                while time.time() < deadline:
                    page.wait_for_timeout(10000)
                    if not is_cloudflare(page) and page.locator("a.jcs-JobTitle").count():
                        _log("CLOUDFLARE cleared.")
                        break
                else:
                    raise CloudflareHalt(
                        "Cloudflare verification not cleared. Stop this run. "
                        "Sign in to Indeed in the persistent Chrome profile, then retry ONE phrase."
                    )
            title = page.title()
            if "blocked" in title.lower() or "authenticating" in title.lower():
                raise CloudflareHalt(f"Indeed blocked the browser: {title}")
            cards = page.locator("a.jcs-JobTitle")
            count = cards.count()
            if count == 0:
                raise RuntimeError(
                    f"No Indeed job titles on the search page. title={title!r} url={page.url}"
                )
            _log(f"Indeed search: {count} titles, fromage={days}, {page.url}")
            take = min(limit, count)
            index = 0
            while len(out) < take and index < page.locator("a.jcs-JobTitle").count():
                card = page.locator("a.jcs-JobTitle").nth(index)
                index += 1
                try:
                    card.scroll_into_view_if_needed(timeout=8000)
                    jk = card.get_attribute("data-jk") or ""
                    headline = card.inner_text().strip()
                    card.click(timeout=8000)
                except Exception as error:
                    _log(f"skip card {index}: {str(error).splitlines()[0]}")
                    continue
                lo, hi = click_sleep_sec
                time.sleep(random.uniform(min(lo, hi), max(lo, hi)))
                _click_see_more(page)
                description = _first_text(page, DESC_SELECTORS, min_chars=80)
                company = _first_text(
                    page,
                    (
                        "[data-testid='inlineHeader-companyName']",
                        "[data-company-name='true']",
                        ".jobsearch-InlineCompanyRating a",
                    ),
                )
                salary = _first_text(
                    page,
                    (
                        "#salaryInfoAndJobType",
                        "[data-testid='attribute_snippet_testid']",
                    ),
                )
                capture = {
                    "job_url": (
                        f"https://www.indeed.com/viewjob?jk={jk}" if jk else page.url
                    ),
                    "indeed_jk": jk,
                    "title": headline or None,
                    "company": company or None,
                    "salary": salary or None,
                    "job_description": description,
                    "search_query": query,
                    "page_title": page.title(),
                }
                if len(description) < 80:
                    _log(f"skip {jk or index}: description {len(description)} chars")
                    continue
                (log_dir / f"indeed_live_capture_{jk or index}.json").write_text(
                    json.dumps(capture, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                out.append(capture)
        finally:
            if context is not None:
                context.close()
            elif browser is not None:
                browser.close()
    return out


def capture_to_markdown(capture: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Indeed.com",
            "",
            capture.get("job_url") or "",
            "",
            f"Company: {capture.get('company') or ''}",
            f"Title: {capture.get('title') or ''}",
            f"Salary: {capture.get('salary') or ''}",
            "",
            capture.get("job_description") or "",
            "",
        ]
    )
