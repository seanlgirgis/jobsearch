# Design decisions

Durable. Change this file when the architecture changes, not for day-to-day status (`LIVE.md`). Phrase catalog and avoidances: `SEARCH_STRATEGY.md`.

## Goals

1. One career record for any bot that scores a job.
2. Same eval stack as `job-runner` (OpenRouter economy) so search scores match triage scores.
3. Configurable searches without code changes.
4. Cheap: do not pay twice for the same job (save `.eval.json`).
5. Safe public output: LTIMindtree only; CAPTAIN is research; no client internals.

## Why not `source_of_truth.json`

It is a stale AWS-DE / Citi-ending profile. Older docs still call it master. **Canonical scoring uses the derived runtime profile.** Treat SoR JSON as a future generated compatibility dump, not an independent authority.

## Why bots do not write SoR

Invented titles and dates. Humans (or an agent **after Sean approves**) edit master files. `refresh_sor.ps1` rebuilds. `--require` is the gate.

## Why OpenRouter not Grok Bot for eval

- Grok Bot has its **own** weekly quota (not SuperGrok chat, but still limited).
- OpenRouter is already how `job-runner` scores (DeepSeek flash). Standardized results, pay-per-token, keys in `.env`.

## Why two files

`.job.md` is human/local-pipeline intake. `.eval.json` is the paid artifact. Same stem, unique `shortid` + `job_hash` so LinkedIn and Indeed cannot clobber the same role.

## Why exclude work types before employers

Annotation/rater titles are skippable everywhere. The same staffing firm can also post a real consulting role. Company bans wait until results show a pattern. Daily repost ≠ spam; DNA only matches `jk` or identical normalized text.

## Why per-site bots under shared config

Shared: SoR, cutoff, guards, output layout.  
Per site: URLs, which term packs, what fields exist (hiring person, See more).

## Why OneDrive is not the brain

Sync lag and collisions. Disk is source for logs/audit. OneDrive is a drop box for local apply machines. World-writable share links must not hold secrets.

## Cutoff rule

Score-led filenames so Sean can ignore far-fetched files in Explorer:

- Apply ≥ 80 (not SKIP)
- Wait 60–79
- Reject below 60 or SKIP (not written)

Known full-time posted maximum pay under $140k is excluded before eval. Ranges reaching
$140k and unknown pay remain eligible. Explicit part-time/flexible work has no floor;
a search phrase or contract label cannot establish part-time hours.

## One terms file

`search_bots/terms.json` holds every category. A new category is a new JSON key, not a new file. Indeed uses `"*"`.

The catalog now has six categories and 54 short alternative phrases. See
[SEARCH_STRATEGY.md](SEARCH_STRATEGY.md) for role selection and exclusion rationale.
Category is the discovery route; duplicate jobs retain the first route. Human review
determines whether the actual duties, hours and pay fit Sean.

The approved scheduler target uses 24 jittered, non-overlapping fires/day and a
two-day Indeed window. It dynamically batches all enabled phrases across those fires;
DNA removes overlap. With 54 phrases, the first cycle is six 3-phrase batches followed
by eighteen 2-phrase batches. Current code is still one phrase / `fromage=1`, so this
needs implementation and testing before unattended use. For a deliberate initial
catch-up, pass `-Fromage 7` once. Windows Task Scheduler/container hosting and
all-page unlimited capture are deployment work, not configuration settings.

## Handoff and ledger

Local path `V:\Bots_Jobs` (OneDrive) is a **replica**. Canonical writes stay on `D:\Workarea\jobsearch\data\search_bots\`. Flush at run start/end; queue if OneDrive is down. Never delete local after copy. Folders on the replica are **Apply** and **Wait**.

## Playwright

Indeed blocks headless HTTP. Headed real Chrome can search; job text is taken from the results pane (`#jobsearch-ViewjobPaneWrapper`), not a standalone viewjob URL.

## OpenRouter call shape

Native `json_schema` + `require_parameters` fails on DeepSeek/Baidu. Client uses **plain chat**, then local JSON parse/coerce (`src/ai/llm_client.py`). Do not “fix” that back to strict schema without a live test.
