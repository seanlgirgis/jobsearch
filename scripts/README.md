# Script catalog

This directory contains both the current implementation and preserved legacy
routes. New work should use the active set below.

## Root PowerShell entry points

- `..\job-runner.ps1` — **current application entry point; keep/use**.
- `..\env_setter.ps1` — **current environment bootstrap; keep/use**.
- Archived `nightly-drive-maintenance.ps1` — machine maintenance only; not part
  of the job-search pipeline. It is preserved under the dated archive.
- Archived root `00.job-chatgpt-*.ps1`, `04.job-chatgpt-stats.ps1`,
  `05.job-chatgpt-search.ps1`, and `06*.intake-*.ps1` — legacy/manual wrappers;
  see `..\archive\2026-09-28\` and its map if recovery is needed.

The archived `06d.intake-from-clipboard-dice.ps1` references a missing `05a...`
wrapper and is broken legacy code.

## Active canonical pipeline

Normal entry point: `..\job-runner.ps1`.

Keep and use these files for the current pipeline:

- `canonical_runner.py` — gate, triage, generate, and apply-only orchestration.
- `build_runtime_profile.py` — builds/checks the derived candidate profile.
- `model_profile.py` — local model-profile inspection and selection.
- `05_render_resume.py` — renderer dynamically loaded by the canonical package.
- `08_render_cover_letter.py` — cover renderer dynamically loaded by the package.
- `normalize_resume_intermediate.py` — renderer support.
- `quality_check.py` — package quality checks.
- `utils/vector_ops.py` — duplicate-gate support used by `src/pipeline`.

`src/pipeline/` is part of the canonical implementation even though it lives
outside this folder.

## Active search-bot support

Use only for the search-bot route described in
`search_bots/agent_work/HANDOFF.md`:

- `search_bots_indeed.py`
- `search_bots_indeed_live.py`
- `search_bots_schedule.py`
- `search_bots_dna.py`
- `search_bots_filters.py`
- `search_bots_handoff.py`
- `search_bots_notify.py`
- `search_bots_sor.py`

The probe files are diagnostics, not the normal search path:
`search_bots_indeed_probe.py` and `search_bots_indeed_playwright_probe.py`.

## Preserved legacy or optional material

The following groups are not the current normal route:

- numbered `00_`–`04_`, `06_`, `07_`, `09_`–`12_` pipeline scripts;
- `10_auto_pipeline.py` and `10b_force_pipeline.py`;
- `scripts_v2/`, `pipeline/`, `ps1_keep/`, `scripts/keep/`, and
  `scripts/Archived/`;
- root `00.job-chatgpt-*.ps1` and `06*.intake-*.ps1` wrappers;
- audio, Gmail, direct-generation, old provider smoke tests, and one-off
  migration/export utilities.

Preserved legacy groups are either already under `archive/` or remain in place
pending a separate dependency review. Do not call them for new work.
