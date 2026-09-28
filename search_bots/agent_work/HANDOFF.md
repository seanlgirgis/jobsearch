# Handoff — search bots (read this first)

Workspace: `D:\Workarea\jobsearch`  
Parked: **2026-09-14**. Sean tired; will `gitqall` himself.

## What this is

Custom Indeed search → filter → OpenRouter economy eval → Apply/Wait files + ledger. **Not** Grok Bot as the scraper. `job-runner.ps1` is a separate generate/apply path.

## Scheduled-policy change — implement before unattended runs

The command below reflects the **current** one-phrase implementation. Sean's new
policy supersedes it and must be implemented/tested before a scheduled deployment:

- 24 scheduled fires per day, random jitter, and a non-overlap lock.
- `-Fromage 2` for every scheduled search, giving a 48-hour overlap; DNA removes
  repeat postings.
- Cover every enabled phrase once per daily cycle. At each fire claim a dynamic batch:
  `ceil(remaining_due_phrases / remaining_run_slots_today)`. With 54 phrases this is
  six runs of 3 phrases, then eighteen runs of 2 phrases.
- Once history exists, batch by observed phrase cost: duration, pages/results, new
  jobs, DNA rate and blocks. Light phrases may share a run; an unusually heavy phrase
  may run alone. Retain run/page safety caps and defer unfinished work.
- Use a manually logged-in, persistent Chrome profile on Sean's consumer IP. Never
  automate login, CAPTCHA, or Cloudflare. Sort newest-first where Indeed supports it;
  stop only at a reliable old/DNA boundary, not on one duplicate.

## Current command (manual/testing only)

**Preferred:**

```powershell
. .\env_setter.ps1
.\search_bots\run_indeed.ps1 -Scheduled -Limit 20
python scripts\search_bots_schedule.py --status
python scripts\search_bots_schedule.py --export
```

Then look at `V:\Bots_Jobs\indeed\Wait`, `\Apply`, `ledger.csv`, `EVENTS\`, `db_export\`.

Windows Task Scheduler/container hosting is later; it must invoke the new batch policy,
not the current one-phrase command, once that policy has been implemented.

**If Cloudflare:** stop. Sean clicks Verify / Sign in in the persistent Chrome profile. Phrase stays **not** complete. Do not launch another search immediately.

## Docs map

| File | Use |
|------|-----|
| `documentation/LIVE.md` | Today |
| `documentation/HOW_IT_WORKS.md` | Operator flow |
| `documentation/SCHEDULE.md` | Hourly SQLite |
| `documentation/STORAGE_POLICY.md` | `/workspace` vs OneDrive, 7-day delete policy |
| `documentation/SEARCH_STRATEGY.md` | Phrases, pay, exclusions |
| `documentation/DESIGN.md` | Why |

## Code map

| Path | Role |
|------|------|
| `search_bots/run_indeed.ps1` | `-Live` / `-Scheduled` |
| `scripts/search_bots_indeed.py` | Eval, ledger, folders, stats, run logs |
| `scripts/search_bots_indeed_live.py` | Playwright; CloudflareHalt; persistent Chrome |
| `scripts/search_bots_schedule.py` | SQLite phrases + DNA + events + `--export` |
| `scripts/search_bots_dna.py` | jk + hash; writes SQLite |
| `scripts/search_bots_filters.py` | Pay $140k, exclusions, fromage=1 |
| `scripts/search_bots_handoff.py` | Local first; queue if V: down |
| `scripts/search_bots_notify.py` | OneDrive EVENTS + optional SMTP |
| `scripts/search_bots_sor.py` | `ensure_fresh` auto-rebuilds runtime SoR |
| `search_bots/terms.json` | All phrases (edit here) |
| `config/search_bots.json` | Floors, hourly one-phrase queue, 12h per-phrase cooldown |
| `config/search_bots.local.json` | gitignored `handoff_root`: `V:\Bots_Jobs` |

SQLite file: `data/search_bots/schedule.sqlite` (gitignored). Sean inspects **CSV export**, not the `.sqlite` itself.

## Invariants

- OpenRouter eval, not Grok Bot quota  
- LTIMindtree only in public packets  
- CAPTAIN = research  
- DNA for Reject/excluded; `-Limit` ignores dna_hits  
- `fromage=1` only (Indeed has no 12-hour fraction)  
- Hourly one-phrase fire; 12h cooldown is the scheduler’s job and DNA removes duplicate postings across overlapping one-day searches  
- Never auto-delete DNA; job dumps 7 days after **verified** OneDrive copy (policy, prune not fully wired)

## Open / next (Sean picks)

1. Review Wait/Apply; `human_processed=Y`; tighten `terms.json`  
2. Implement/test the daily 24-slot dynamic batch scheduler and `fromage=2`, then host it in Windows Task Scheduler or a local container; preserve Chrome profile, SQLite, DNA, logs and the local/OneDrive handoff.
3. SMTP in `.env` if he wants email on block  
4. Do **not** move Indeed grind onto Grok Bot (cloud IP)  
5. LinkedIn later, same SQLite/DNA pattern  
6. Merge LTM into `master_career_data.yaml`  
7. `job-runner` ingest of `.eval.json`

Python: `. .\env_setter.ps1` → `C:\py_venv\JobSearch`  
Tests: `python -m unittest tests.test_search_bots_dna`
