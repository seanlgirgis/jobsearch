# jobsearch — current state

- **Path:** `D:\Workarea\jobsearch`
- **Director:** registered 2026-09-06
- **Launcher:** `start_grok jobsearch`
- **Git:** already in `gitqall.ps1` (`jobsearch`)
- **Agent files (vanilla only):** `AGENTS.md`, `BOOTSTRAP.md`, `PROFILE.md`, this file, `PROJECT_MEMORY.md`

Canonical entry point: `job-runner.ps1`; operator instructions:
`docs/PIPELINE_OPERATOR.md`. Prompt 05 cutover adds enforced gates, request-aware
caching, persisted decisions, versioned generated packages, and local apply-only
recording. Historical job folders and legacy scripts remain in place.
No `Grok_*` agent-pack files in this repo.

## Last updated

- Date: 2026-09-14
- Reason: Search-bot session parked. Current code has hourly SQLite one-phrase / `fromage=1`; **next implementation supersedes it** with 24 jittered non-overlapping runs/day, dynamic 2–3 phrase batches across 54 phrases, and `fromage=2`. Cloudflare halt, Apply/Wait on V:\Bots_Jobs. Local Task Scheduler/container hosting is not installed. Next agent: `search_bots/agent_work/HANDOFF.md`. Sean gitqall.
