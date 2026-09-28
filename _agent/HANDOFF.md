# Agent handoff

**Updated:** 2026-09-28  
**Status:** control-plane consolidation and root cleanup complete; broader
historical/output review remains separate work.

## What changed

- Established one generic bootstrap: `AGENTS.md` → `_agent/`.
- Separated constitution, rules, durable memory, live state, and handoff.
- Reduced route duplication by pointing pipeline and search-bot work to their
  authoritative task documentation.
- Archived older root instruction files after consolidating their durable
  content into `_agent/` and their task routing into `docs/`.
- Audited the script surface and published an active allowlist without moving or
  deleting active files.
- Classified root PowerShell wrappers; identified the broken Dice clipboard
  wrapper reference.
- Archived the first clearly legacy batch under `archive/2026-09-28/` with a
  mapper, 90-day review date, and 180-day destruction-eligibility date.
- Cleaned the root Markdown surface: stale notes and the misplaced root intake
  were archived, and coding standards moved under `docs/`.
- Archived the remaining obsolete root redirects, caches, local test/history
  artifacts, unrelated workstation files, and separate machine-maintenance
  script under `archive/2026-09-28/root_cleanup/`.
- Retargeted runtime-profile guardrails to `_agent/RULES.md` and rebuilt the
  derived profile with an offline validation pass.
- Archived stale `.codex`, `.grok`, `.antigravity`, cache, and temporary folders;
  preserved `.claude` because it contains a registered Git worktree.

## Start here next time

1. Read `AGENTS.md`, then `_agent/README.md` through `_agent/HANDOFF.md`.
2. For a normal job, read `docs/PIPELINE_OPERATOR.md` and only the named intake
   and returned job folder.
3. For search bots, read `search_bots/agent_work/README.md`, `HANDOFF.md`,
   `NEXT.md`, and `documentation/LIVE.md`.

## Open work

- Review output-heavy material and `pipeline/` utilities separately; do not
  bulk-move or delete them as routine cleanup.
- Review `docs/SCRIPT_SURFACE_AUDIT.md` before any script move batch.
- Implement and test the approved search-bot scheduler before unattended hosting.
- Keep `STATE.md` current after meaningful changes; add only durable decisions to
  `MEMORY.md`.

## Safety stop

Stop and ask Sean when a change would delete or bulk-move records, submit an
application, expose private/client information, change provider credentials, or
override a gate without an explicit reason.
