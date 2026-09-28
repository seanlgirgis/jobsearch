# How the search-bot system works

Sean-facing. Flow: **fresh SoR → Indeed search (Playwright) → filters → OpenRouter eval → two files + CSV ledger**.

Strategy (why these phrases, avoidances, salary, week-first): **`SEARCH_STRATEGY.md`**.

## Pieces

```
You edit master career files
        ↓
.\search_bots\refresh_sor.ps1     (no LLM)
        ↓
data/master/candidate_profile_runtime.json
        ↓
.\search_bots\run_indeed.ps1 -Live -Limit N
        ↓
Headed Chrome searches the one due phrase selected from search_bots/terms.json
        ↓
Skip: DNA, excluded title/company, FT posted max under $140k, annotation/rater work.
DNA stored for Reject/excluded/too-short. **-Limit counts new jobs only, not DNA hits.**
        ↓
OpenRouter economy eval
        ↓
Apply (≥80) / Wait (60–79) / Reject (<60 or SKIP)
        ↓
Apply & Wait: two files under indeed/Apply or indeed/Wait + ledger row (human_processed=N)
```

## Stale SoR (not a random stop)

The bot rebuilds the runtime profile from master files in memory and **byte-compares** it to `data/master/candidate_profile_runtime.json`. If yaml, skills, LTM notes, rules, the searchable profile, Director `SEAN.md`, or the builder script changed, the file is **stale**. That is intentional: do not score against an old career picture.

**Live/deploy** now **auto-refreshes** that file and continues. If refresh itself fails, it stops and writes OneDrive alerts.

## Alerts (no email/SMS yet)

Per-run log (keep last 5): `data/search_bots/logs/runs/indeed_run_*.log`  
Copy of last run: `V:\Bots_Jobs\indeed\LAST_RUN.log`  
Terminal only prints start + end stats.

Watch `V:\Bots_Jobs\indeed\`:

| File | Meaning |
|------|---------|
| `BOT_STATUS.txt` | RUNNING / OK / FAILED (overwritten each run) |
| `LAST_ERROR.txt` | Last failure (SoR refresh fail, capture fail, zero jobs) |

Email/text would need a mail/SMS API; OneDrive is the pager for now.

## Current SQLite scheduler and approved replacement

```powershell
.\search_bots\run_indeed.ps1 -Scheduled -Limit 20
python scripts\search_bots_schedule.py --status
python scripts\search_bots_schedule.py --export
```

- **Current code:** each fire syncs `terms.json` into `data/search_bots/schedule.sqlite`, runs **one** due phrase, and uses `fromage=1`.
- **Approved next policy (not implemented yet):** 24 jittered, non-overlapping fires/day; `fromage=2`; dynamic batches that cover every enabled phrase daily. With 54 phrases, six fires carry 3 phrases then eighteen carry 2. Batch using history once available so light searches share a fire and slow searches can be isolated.
- Cloudflare / Indeed down: phrase **not** marked complete; retry in ~1 hour; email `seanlgirgis@gmail.com` if SMTP is in `.env`; always write `V:\Bots_Jobs\indeed\EVENTS\`.
- DNA and events live in the same SQLite file. Inspect via **CSV export** (Excel), not a SQLite GUI:
  `data/search_bots/logs/db_export/` and `V:\Bots_Jobs\indeed\db_export\`.

Windows Task Scheduler: hourly, that `-Scheduled` command.

## Command

```powershell
Set-Location D:\Workarea\jobsearch
. .\env_setter.ps1
.\search_bots\refresh_sor.ps1
.\search_bots\run_indeed.ps1 -Live -Limit 5
```

Empty DNA cache uses **7-day** lookback; later runs use **1 day**. After POC, catch-up with `-Fromage 7`. One query: `-Query "your string"`.

## Search terms (one file)

`search_bots/terms.json` — six categories and 54 short alternative phrases (Indeed already sets `l=remote`). New category = new key. Indeed `term_packs: ["*"]` uses all keys.

| Category | Intent |
|----------|--------|
| capacity_performance | IT capacity / application performance |
| observability_apm | Dynatrace, AppDynamics, Splunk, BMC, CA APM |
| practical_ai | AI enablement, Copilot adoption, workflow/RAG |
| python_reporting_automation | Python/SQL/Power BI reporting, not generic DE |
| technical_consulting | Performance/observability consulting |
| part_time_remote | Fractional / part-time / contract *search phrases* (posting may still be FT) |

## Filters (before OpenRouter)

| Rule | Where |
|------|--------|
| Recency | last **1 day**. One phrase per run. Cloudflare: human only, then stop. |
| Titles / companies | `config/search_bots_exclusions.json` |
| Full-time pay | posted **max** &lt; **$140k** USD skipped. Part-time/fractional **on the posting** (not the search phrase): no floor. Unknown / non-USD: keep. |
| DNA | Indeed `jk` or JD hash |

Search query does **not** make a job part-time. Contract alone does not.

## Verdicts

| Label | Rule | Written? |
|-------|------|----------|
| Apply | score ≥ 80 and not SKIP | Yes — advisory, not an application |
| Wait | 60–79 | Yes |
| Reject | &lt; 60 or SKIP | No (DNA only) |

Stem: `{score}_{Apply|Wait|Reject}_{date}_{time}_{company}_{id}`

## Local vs OneDrive

Full policy: `STORAGE_POLICY.md`. Short version: Bot/PC writes local (`/workspace/jobsearch/…` or `data/search_bots/`). OneDrive is the replica. Per-run output folders. Delete run dumps only after verified copy and **7 days** (24h minimum). DNA never auto-deleted.

## Local vs OneDrive (detail)

Local disk is the **source of truth** (ready files, DNA, logs, ledger). OneDrive/`V:\Bots_Jobs` is a **replica**. The bot never fails a job because the cloud blipped.

1. Write everything under `data/search_bots/` first.
2. Try to copy to OneDrive.
3. If copy fails, queue in `data/search_bots/handoff_queue.json`.
4. At **start and end** of a live run, flush the queue. Still **do not delete** local files after a successful copy (DNA and ready stay).

If `V:` is missing, the run still completes; files appear on OneDrive next time it is up.

## Where files go

```
V:\Bots_Jobs\indeed\
  ledger.csv
  Apply\
  Wait\
```

`practical_ai` / `capacity_performance` / … are **search packs** (which query found it), stored in the ledger as `search_pack`, not as folders. **Category = Apply | Wait | Reject.**

Same under `data/search_bots/ready/indeed/`. Ledger **human_processed** starts **N**; Sean sets **Y** after review (Y = reviewed, not hired).

## SoR

Edit master yaml / `bofa_stated_ai_work.md` / rules / searchable profile. Bots read `candidate_profile_runtime.json` only. `source_of_truth.json` is legacy.

## Money

OpenRouter economy. Usage on new `.eval.json` / `spend.jsonl`. Grok Bot not used for bulk eval.

## Not this bot yet

LinkedIn/Dice/Wellfound/WWR live scrape. Unlimited pagination. Windows Task Scheduler or a local container deployment. `job-runner` cache reuse of `.eval.json`.
