# LIVE — search bots (update every session)

**Last updated:** 2026-09-14  
**Owner:** Sean. Stopped for the night. Next agent: `../agent_work/HANDOFF.md`.

## Now

- Indeed guinea pig is **live** (headed Chrome, Playwright). **Do not grind 10k / 54 phrases in one process.** Cloudflare already caught a fast `fromage=7` run.
- **Hourly product path:** `.\search_bots\run_indeed.ps1 -Scheduled -Limit 20`
  - Syncs `terms.json` → SQLite first
  - One due phrase, `fromage=1`
  - Same phrase waits **12 hours** after success
  - Block/Cloudflare: **do not** mark phrase complete; OneDrive `EVENTS\`; email only if SMTP in `.env`
- **Manual path:** `-Live` still exists; default **one phrase per process**; persistent profile `data/search_bots/chrome_profile`
- **Never** click Cloudflare from code. Sean signs in / solves the check in Chrome.
- Folders: `V:\Bots_Jobs\indeed\Apply\` and `\Wait\` (not search-pack names). Ledger `category` = Apply/Wait; `search_pack` = query family; `human_processed=N`.
- Verdicts: Apply ≥80, Wait 60–79, Reject not written (DNA yes).
- DNA: SQLite `schedule.sqlite` **and** leftover json cache. Inspect via `--export` CSVs (Excel), not a SQLite GUI.
- SoR: live **auto-refreshes** if stale. Runtime: `data/master/candidate_profile_runtime.json`.
- OpenRouter economy for eval. Grok Bot is **not** the scraper (cloud IP + quota). Sean's direction is this PC with quiet hourly short runs; Task Scheduler/container hosting is still not installed.
- Sample funnel: ~300 processed → ~3 Apply / ~30 Wait. Filters doing their job.

## Do not

- Score with `data/source_of_truth.json`
- Name Bank of America in bot output
- Revert OpenRouter to strict json_schema
- Automate Cloudflare
- Treat Apply filename as applied
- Put keys in JSON or `/workspace` job folders

## Log (newest first)

- 2026-09-14: Session parked. SQLite round-robin 12h, DNA in DB, CSV export, Cloudflare halt + 5 min human wait, one-term-per-run, OneDrive replica/queue, Apply/Wait folders. Sean will `gitqall`.
- 2026-09-14: Codex reconciled strategy and handover: 54 phrases/six categories, including Forward Deployed Engineer variants; human reviews Apply/Wait while Reject remains DNA-only. Hourly fire means one due phrase, never a long all-term browser run; 12h is the successful-phrase cooldown.
- 2026-09-14: Sean approved the replacement scheduler policy: 24 jittered non-overlapping fires/day, `fromage=2`, dynamic batches covering all enabled phrases daily (54 currently = six 3-phrase runs then eighteen 2-phrase runs). History should pair light phrases and isolate heavy ones; current code has **not** implemented this yet.
