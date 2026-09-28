# Search-bot documentation

Start here if you want to **understand** the system.

| File | Purpose | Update when |
|------|---------|-------------|
| `HOW_IT_WORKS.md` | Operator flow: SoR, search, eval, two files, local pipeline | Behavior changes |
| `DESIGN.md` | Why it is shaped this way (decisions, not a tutorial) | Architecture changes |
| `SEARCH_STRATEGY.md` | Sean's categories, phrases, avoidances, pay policy and deployment gaps | Search preferences change |
| `STORAGE_POLICY.md` | `/workspace` vs OneDrive, per-run folders, 7-day delete | Deploy storage |
| `SCHEDULE.md` | Hourly SQLite round-robin, 12h per phrase, CSV export | Scheduler |
| `LIVE.md` | Current truth: what is built, what is not, last refresh | **Every work session** |

Agent pickup (do not crawl the whole tree): `../agent_work/README.md`
