# Scheduled Indeed policy

> **Current code is one phrase / `fromage=1`. The policy below is Sean's approved
> replacement and must be implemented and tested before unattended scheduling.**

Run 24 non-overlapping scheduled fires per day, with a small random delay. Use
`fromage=2` (a 48-hour window) for every search. DNA removes overlap and protects
against a missed/late run becoming a blind spot.

## Daily dynamic batching

Every enabled phrase should be searched once in a daily cycle. On each fire, calculate:

```text
phrases_this_run = ceil(remaining_due_phrases / remaining_run_slots_today)
```

With the current 54 phrases and 24 fires, that yields six 3-phrase runs followed by
eighteen 2-phrase runs. It is a 24-run/day budget, not a claim that there are only 24
individual Indeed queries.

After an initial day, let SQLite retain per-phrase history (duration, pages/results,
new jobs, DNA-hit rate, and block/error rate). Use it to group light phrases and allow
a high-volume/slow phrase to run alone. A run still needs duration/page ceilings; defer
unprocessed phrases rather than extending a browser session indefinitely.

Sort newest-first where Indeed supports it. Page until a reliable boundary of old,
DNA-known results is reached; never stop on one duplicate because sponsored/reposted
listings can be intermixed. Never automate login, CAPTCHA, or Cloudflare. A persistent
manually logged-in Chrome profile on Sean's consumer IP is the intended session.

## Command (Task Scheduler)

```
D:\Workarea\jobsearch\search_bots\run_indeed.ps1 -Scheduled -Limit 20
```

Working directory: `D:\Workarea\jobsearch`. The eventual scheduler must calculate a
batch, not simply claim one phrase.

## Hosting boundary

The SQLite schedule code is ready; **no Windows Task Scheduler task or container is
installed yet**. Sean chose a local-machine deployment that wakes hourly, runs one
phrase, then exits quietly. Do not replace that with an all-query process.

Either host option must keep these paths persistent between fires:

- `data/search_bots/schedule.sqlite` (phrases, DNA and events)
- `data/search_bots/chrome_profile/` (Indeed's headed Chrome session)
- `data/search_bots/logs/`, `data/search_bots/ready/`, and the handoff queue
- `data/master/candidate_profile_runtime.json` and the master inputs used to refresh it

The live adapter uses headed Chrome. A container is acceptable only after it is proven
to provide a supported visible/virtual display and persistent browser profile; do not
assume a headless container will work with Indeed.

## Inspect the database (no SQLite app required)

```powershell
. .\env_setter.ps1
python scripts\search_bots_schedule.py --status
python scripts\search_bots_schedule.py --export
```

Open `data\search_bots\logs\db_export\phrases.csv` (and `dna_record.csv`, `events.csv`). Copies go to `V:\Bots_Jobs\indeed\db_export\` when V: is up.

## Email

Set in `.env` if you want mail on Cloudflare/block:

```
SMTP_HOST=...
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
EMAIL_FROM=...
EMAIL_TO=seanlgirgis@gmail.com
```

Without SMTP, events still land on disk and OneDrive. We never click Cloudflare.
