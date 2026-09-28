# Work log

Newest first.

## 2026-09-14 (parked)

- Session end. Sean will gitqall. Cloudflare catch on fast fromage=7 grind. Strategy: one phrase/hour, 12h before same phrase, SQLite hub (phrases+DNA+events), CSV export, Cloudflare halt + human wait, persistent Chrome, Apply/Wait folders, OneDrive replica/queue. Do not use Grok Bot as the scraper. HANDOFF/LIVE/NEXT updated.
- Codex reconciliation: catalog is 54 phrases across six categories, including general, contract and part-time Forward Deployed Engineer variants. Search policy remains Apply / Wait / silent Reject; only Apply/Wait files reach local/OneDrive folders. Deployment direction is Sean's strong local machine with quiet hourly short runs, not a long all-query grind. Task Scheduler/container hosting is still to be installed; the SQLite one-phrase queue already exists.

## 2026-09-13 (docs review)

- Reviewed terms, exclusions, pay/recency, SEARCH_STRATEGY.md. Synced HOW_IT_WORKS, LIVE, HANDOFF, NEXT, README, DESIGN, CURRENT_STATE, PROJECT_MEMORY. `config/search_bots.json` `term_packs` set to `*` (was stale 3-pack list). Ready gitkeeps for decision folders.

## 2026-09-13 (search strategy and working filters)

- Then-current six categories / 48 phrases in terms.json. Capacity/APM and practical AI focus; Python/reporting and technical consulting alternatives; flexible searches tied to concrete work. The current catalog is 54 phrases; see the 2026-09-14 parked entry.
- Expanded annotation/rating/ads-assessor title exclusions; retained DataAnnotation company exclusions, with no new blanket company bans.
- First-week then daily-lookback settings support the intended twelve-hour cadence. Scheduler/unlimited pagination remain unimplemented and are documented.
- Corrected capture of short company/pay fields, Title/Salary parsing, explicit pay-unit conversion and search-query part-time exemption. $140k maximum-of-range policy retained; unknown pay goes to review.
- Removed dead keep_if configuration and used the supplied root for verdicts/filenames/retention. Human decisions and runtime career profile unchanged.
- See SEARCH_STRATEGY.md for employer vocabulary sources and deployment handoff notes.
- Verification: 19 focused regression tests passed; Black/Ruff passed. Catalog validated as 48 unique phrases across six categories. Read-only replay of Sean's Marathon/Hexad captures recovered titles and hourly/annual pay. No paid evaluations, live searches or scheduler installation.

## 2026-09-13 (docs persist)

- Synced HOW_IT_WORKS, LIVE, HANDOFF, NEXT, README to match: terms.json, category folders, ledger, verdicts 80/60, V:\Bots_Jobs, Playwright live Indeed.

## 2026-09-13 (ledger + folders)

- Kept jobs under `indeed/{category}/`. CSV ledger with `human_processed=N`, score, category, verdict, paths, usage.

## 2026-09-13 (terms.json)

- Collapsed three pack files into `search_bots/terms.json`. Indeed `term_packs: ["*"]`.

## 2026-09-13 (verdicts + multi-term)

- Live iterates all term categories. Apply ≥80, Wait 60–79, Reject otherwise.

## 2026-09-13 (pay + exclusions + recency)

- FT skip below $140k. Annotation denylist. `fromage=1`.

## 2026-09-13 (Indeed live)

- Playwright headed Chrome. DNA. First job eHealth 72 REVIEW. Five-job test four new evals ~$0.00095. Filename score_verdict.

## 2026-09-13 (Playwright)

- Package + Chromium installed. Headless blocked; headed Chrome search OK; viewjob Sign In.

## 2026-09-13 (SoR / OpenRouter)

- `refresh_sor.ps1`. OpenRouter plain chat. Failed cache retry. `.env` loaded in env_setter.
