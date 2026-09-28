# Agent instructions

This is Sean's job-market workspace: job intake, scoring, resumes, applications,
gigs, and application interview preparation.

This file is the vendor-neutral entry point for every coding or agentic tool.
Read it first, then follow the control plane below.

## Startup

1. Read `_agent/README.md`.
2. Read `_agent/CONSTITUTION.md`, `_agent/RULES.md`, `_agent/MEMORY.md`,
   `_agent/STATE.md`, and `_agent/HANDOFF.md`.
3. Follow the route map in `_agent/README.md` and read only the files needed for
   the requested step.

Do not crawl all of `data/jobs/`, `data/search_bots/`, or `search_bots/`.

Before running Python, activate the project environment:

```powershell
. .\env_setter.ps1
```

## Non-negotiable boundaries

- Do not invent employment history, metrics, dates, titles, or production depth.
- Use `data/master/` and the runtime-profile rules for career facts.
- Keep the current employer as LTIMindtree only; never name its client in public
  artifacts. Treat CAPTAIN as research, not production.
- Do not write ALOK, learning, python_dsa, or local_memory work here.
- Do not submit applications or mark them applied without Sean's explicit
  confirmation.
- Preserve historical records and user changes. Do not delete, bulk-move, reset,
  push, or rewrite Git history unless Sean explicitly delegates it.

The old agent-specific filenames are preserved under the dated archive. They
are not separate policy sources.
