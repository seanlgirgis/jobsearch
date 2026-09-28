# Current workspace state

**Last reviewed:** 2026-09-28

## Control plane

- Generic control files are consolidated under `_agent/`.
- Root `AGENTS.md` is the only required bootstrap file.
- Older root filenames were archived after the generic control plane became the
  sole active route.
- Workspace audit: `docs/WORKSPACE_CONTROL_AUDIT.md`.
- Script audit: `docs/SCRIPT_SURFACE_AUDIT.md`; active allowlist:
  `scripts/README.md`.
- Root PowerShell review confirms only `job-runner.ps1` and `env_setter.ps1` are
  current application controls; the numbered ChatGPT wrappers are legacy/manual.
- Known legacy defect: `06d.intake-from-clipboard-dice.ps1` references a missing
  `05a...` wrapper.

## Canonical pipeline

- Entry point: `job-runner.ps1`.
- Commands: `docs/PIPELINE_OPERATOR.md`.
- Implementation: `scripts/canonical_runner.py` and `src/pipeline/`.
- Stages: gate, triage, generate, and apply-only recording.
- Historical jobs and legacy wrappers remain preserved but are not the normal
  route for new work.

## Search bots

- Work is parked. Current code is one phrase per run with `fromage=1`.
- Approved replacement: 24 jittered non-overlapping runs, dynamic 2–3 phrase
  batches, and `fromage=2`; not implemented yet.
- Task Scheduler/container hosting is not installed.
- Search-bot handoff: `search_bots/agent_work/HANDOFF.md`.

## Current change set

- This control-plane hardening is intentionally documentation-only.
- No job data, credentials, or active pipeline code was deleted or moved.
- The first reversible archive batch moved 11 root legacy wrappers plus
  `ps1_keep/` and `scripts_v2/`; see `archive/ARCHIVE_MAP.md`.
- Root Markdown was reduced to the active README and universal entry point.
  Historical notes, compatibility bridges, and unrelated root artifacts were
  archived; coding style moved to `docs/CODING_STYLE.md`.
- The runtime-profile builder now uses `_agent/RULES.md` for guardrails; the
  derived profile was rebuilt and validated offline.
- Stale vendor-specific root folders and generated temporary/cache folders were
  archived under `archive/2026-09-28/root_hidden/`. `.claude` remains because
  Git registers a nested worktree beneath it; `.git`, `.venv`, and `.vscode`
  remain active state.
