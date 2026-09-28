# Handover — jobsearch search bots (Indeed guinea pig)

**Date:** 2026-09-14  
**Repo:** `D:\Workarea\jobsearch`  
**Authoring session:** Sean + Grok, then parked for `gitqall`  
**Next agent door:** `search_bots/agent_work/HANDOFF.md`  
**Sean-facing live page:** `search_bots/documentation/LIVE.md`

This file is the **outbox narrative**: status, idea, what shipped, how the code evolved. It is not a substitute for `HANDOFF.md` (file map) or `SEARCH_STRATEGY.md` (phrases/pay).

---

## 1. Status (when we stopped)

**Working on this PC**

- Headed Chrome (Playwright) can search Indeed, click a result **card** (not a naked `viewjob` URL), capture JD, DNA-skip repeats, OpenRouter-eval, write Apply/Wait files + ledger.
- Cloudflare **already caught** a fast grind (`fromage=7`, many phrases). Screenshot: “Additional Verification Required / Verify you are human.”
- Product path for later: **one phrase per hour**, same phrase not again for **12 hours**, SQLite orchestrator, `fromage=1` (Indeed has no 12-hour filter).
- Funnel from a noisy run: on the order of **~1% Apply / ~10% Wait** of jobs that were actually processed. That is a tight filter, not a dead bot.
- OpenRouter evals are cheap (flash: well under a cent per job when usage is stored).

**Not done**

- Windows Task Scheduler not installed.
- SMTP email on block not configured (code exists; needs `.env`).
- LinkedIn / Dice / Wellfound / WWR live scrapers.
- Auto-delete of local dumps after OneDrive verify.
- `job-runner` ingest of `.eval.json` (skip paid triage).
- LTM bullets merged into `master_career_data.yaml`.
- Grok Bot **not** used as the scraper (deliberate).

**Sean’s next human work:** review `V:\Bots_Jobs\indeed\Wait` and `\Apply`, set ledger `human_processed=Y`, then keep/kill phrases in `search_bots/terms.json`.

---

## 2. The idea

Sean needs **off-hours / career-shaped** jobs without a second full-time hunt. Evaluation must match `job-runner` (OpenRouter economy), not Grok chat quota.

**Architecture in one line:**  
shared brain (SoR + rules) → site bot → filters → paid eval once → two files + ledger → Sean decides Apply/Wait.

**Decisions that stuck**

| Decision | Why |
|----------|-----|
| OpenRouter for scoring | Same models as `job-runner`; Grok Bot has a **separate** weekly pool |
| Runtime SoR, not `source_of_truth.json` | Old SoR is stale AWS-DE / ends at Citi |
| Bots do not write SoR | No invented employment |
| Indeed first | Public listings; LinkedIn login/See-more is harder |
| Headed real Chrome | Headless = Blocked; `viewjob?jk=` = Sign In |
| DNA (`jk` + text hash) | Never pay twice for the same posting |
| Apply ≥80 / Wait 60–79 / Reject silent | Sean sorts by filename; junk stays off OneDrive |
| Folders = Apply/Wait, not `practical_ai` | “Category” means **decision**, not search pack |
| `fromage=1` only | Indeed days, not hours; 12h schedule overlaps 24h + DNA |
| One phrase per scheduled fire, 12h before that phrase repeats | Cloudflare / ban risk |
| Do not click Cloudflare | Human only; halt; don’t mark phrase done |
| Local disk canonical; OneDrive replica | Cloud hiccups; Grok Bot can’t see `D:\…\data\` |
| SQLite hub + CSV export | Sean has no SQLite GUI |
| Grok Bot ≠ scraper | Cloud IP; weekly quota; `/workspace` is real but not Explorer |

**Positioning:** capacity/performance + practical AI enablement; public employer **LTIMindtree** only; CAPTAIN = research.

---

## 3. Work done (this arc)

1. Session bootstrap in jobsearch; BofA/LTM AI work captured → `data/master/bofa_stated_ai_work.md`; searchable profile in `outbox/`.
2. Toloka FDE resume (copy, not overwrite consulting resume); old `job-check` pipeline also run (score 42%, skip-then-accept).
3. Canonical runner OpenRouter path: drop strict json_schema; plain chat + local JSON (matching `testOpenRouter.py`); failed-cache retry; `.env` load in `env_setter.ps1`.
4. Search-bot skeleton: five site folders, then **Indeed live**.
5. Playwright: headless fail → headed Chrome search works.
6. Filters: 24h, $140k FT floor, annotation/rater denylist, DataAnnotation company.
7. Output: two files, score+verdict in the **name**, ledger `human_processed=N`, drop to `V:\Bots_Jobs`.
8. Ops: SoR auto-refresh; run logs last 5; quiet terminal + stats; DNA hits don’t eat `-Limit`; Cloudflare wait-then-halt; persistent Chrome profile.
9. Schedule: SQLite phrases + DNA + events; `--export` CSV; `-Scheduled`; 12h per phrase; block ≠ success.
10. Docs: `search_bots/documentation/*`, `search_bots/agent_work/*`, this outbox file.

---

## 4. Code map (what to open)

| Path | Role |
|------|------|
| `search_bots/run_indeed.ps1` | `-Live` / `-Scheduled` |
| `scripts/search_bots_indeed.py` | Eval, DNA remember, ledger, stats, folders |
| `scripts/search_bots_indeed_live.py` | Playwright capture, CloudflareHalt |
| `scripts/search_bots_schedule.py` | SQLite: phrases, DNA, events, `--export` |
| `scripts/search_bots_dna.py` | `jk` + hash; SQLite write |
| `scripts/search_bots_filters.py` | Pay, exclusions, fromage |
| `scripts/search_bots_handoff.py` | Local first; queue if `V:` down |
| `scripts/search_bots_notify.py` | OneDrive EVENTS + optional SMTP |
| `scripts/search_bots_sor.py` | `ensure_fresh` / `refresh_sor.ps1` |
| `search_bots/terms.json` | All search phrases |
| `config/search_bots.json` | Floors, polite, 12h interval |
| `config/search_bots_exclusions.json` | Title/company skips |
| `config/search_bots.local.json` | gitignored `handoff_root` = `V:\Bots_Jobs` |
| `data/search_bots/schedule.sqlite` | Runtime DB (gitignored) |
| `data/search_bots/chrome_profile/` | Persistent Chrome (gitignored) |
| `src/ai/llm_client.py` | OpenRouter = **plain chat**, not json_schema |

**Commands**

```powershell
. .\env_setter.ps1
.\search_bots\refresh_sor.ps1
.\search_bots\run_indeed.ps1 -Scheduled -Limit 20
python scripts\search_bots_schedule.py --status
python scripts\search_bots_schedule.py --export
```

Inspect jobs: `V:\Bots_Jobs\indeed\Wait` and `\Apply`.  
Inspect DB without SQLite: `data\search_bots\logs\db_export\`.

---

## 5. Code evolution (why it looks like this)

**v0 — Paste inbox.** Indeed HTTP 401. User: “why am I pasting?”

**v1 — httpx probe.** 401 Authenticating / RSS 403.

**v2 — Playwright headless.** Title `Blocked - Indeed.com`.

**v3 — Headed Chrome, click `a.jcs-JobTitle`.** Search works. Naked `viewjob` → Sign In. Description often in `#jobsearch-ViewjobPaneWrapper`, not `#jobDescriptionText`.

**v4 — DNA + eval + two files.** Limit counted DNA hits → “only 3 jobs” while 84 DNA records existed. Fixed: DNA does not consume `-Limit`. Reject still DNA-stamped.

**v5 — Filters.** `$140k` FT max; part-time only if the **posting** says so; annotation titles; `fromage` as Indeed’s day filter.

**v6 — UX.** Filename `{score}_{Apply|Wait|Reject}_…`. Folders were wrongly search-pack names (`practical_ai`); Sean meant **Apply/Wait**. Ledger: `category` = decision, `search_pack` = query family.

**v7 — Ban.** Fast multi-phrase + `fromage=7` → Cloudflare. Stopped automating the widget. One phrase per process; 5 min human wait; then halt; persistent profile.

**v8 — Schedule.** Round-robin SQLite: hourly fire, **12h** before the same phrase; sync `terms.json` every run; block does **not** consume the 12h; events + optional email; CSV export because Sean won’t use a SQLite GUI.

**v9 — Storage story.** Laptop `data/` is guinea pig only. Grok Bot **does** have `/workspace` (shared by all Bots, not `/opt`). OneDrive is what Sean can open. Policy: local write, flush replica, delete dumps only after verified copy + 7 days (24h floor). DNA never auto-delete.

**Opinion parked with Sean:** containers (or Windows Task on this PC) for the grind; **Grok Bot is the teammate**, not the Indeed scraper (cloud IP).

---

## 6. Known sharp edges

- Cloudflare / Ray ID walls after aggressive runs.  
- Invisible card scroll timeouts (Indeed junk rows) — skipped, noisy in old terminal, now in run log.  
- Hourly eval JSON can omit `score` (filled as 0 → Reject).  
- Dual DNA (json files + SQLite) during transition; SQLite is the intended hub.  
- `source_of_truth.json` still exists and is **wrong** as SoR.  
- Sign-in helps; it does **not** immunize a cloud IP or a 10k grind.

---

## 7. Do not regress

- Do not send OpenRouter `json_schema` + `require_parameters` (DeepSeek/Baidu).  
- Do not click Cloudflare.  
- Do not score with `source_of_truth.json`.  
- Do not name BofA in public packets.  
- Do not treat Apply in a filename as “already applied.”

Sean closes this session and runs **gitqall**.

---

## 8. Late-night reconciliation — Sean + Codex (2026-09-14)

This addendum records the decisions made while validating the strategy and is the
tie-breaker if older POC notes conflict.

- **Human responsibility stays simple:** the bot discovers, filters, pays for one
  evaluation, and labels it `Apply`, `Wait`, or `Reject`. Sean reviews the Apply/Wait
  drops and decides what to pursue. `Apply` is not an application. Reject is retained
  only in DNA and is not written to either local or OneDrive ready folders.
- **Search direction:** capacity/performance, observability/APM, practical AI
  enablement, Python/reporting automation, technical consulting, and flexible work.
  `terms.json` now has six categories and 54 phrases. Practical AI includes Forward
  Deployed Engineer variants for general/full-time, contract and part-time discovery;
  it does not claim Sean is an ML specialist.
- **Avoidances/pay:** keep the title-based annotation/rater/AI-tutor denylist and the
  DataAnnotation company exclusion. Do not add blanket company bans or treat daily
  reposting as spam without evidence. Full-time posted maximum below $140k is excluded;
  unknown pay and explicitly part-time/flexible postings remain reviewable.
- **Operating shape:** Sean chose a strong local machine that wakes, runs a short
  browser session, and exits quietly **hourly**. The scheduler already implements
  this: one due phrase per fire, `fromage=1`, with a **12-hour cooldown for that exact
  phrase** after success. This is deliberately different from running all phrases at
  once, which caused Cloudflare trouble.
- **Deployment boundary:** the SQLite scheduler code exists, but Windows Task
  Scheduler and a local container deployment are not installed. Tomorrow's deployment
  work is to choose one host mechanism and prove it preserves the Chrome profile,
  SQLite/DNA, logs, runtime SoR, and local-to-OneDrive handoff. Do not call live
  Indeed or OpenRouter merely to test documentation.

## 9. Final scheduled-search policy — Sean (2026-09-14)

This supersedes the earlier one-phrase/hour, 12-hour-per-phrase policy and is a
**documented target, not yet the code's behavior**.

1. Schedule 24 runs per day with random jitter and a non-overlap lock.
2. Use `-Fromage 2` for a two-day overlap. DNA prevents repeat processing and removes
   a missed-run black hole.
3. Cover every enabled phrase once daily. At a given fire calculate
   `ceil(remaining_due_phrases / remaining_run_slots_today)`. With 54 phrases: six
   batches of 3, then eighteen batches of 2.
4. After the first day, store phrase history and pair small/light searches; high-volume
   or slow searches may run alone. Keep page/time ceilings and defer remaining work.
5. Use the persistent manually logged-in consumer-IP Chrome profile, newest-first
   results where available, and stop only at a reliable old/DNA boundary. Never
   automate authentication, CAPTCHA, or Cloudflare.
