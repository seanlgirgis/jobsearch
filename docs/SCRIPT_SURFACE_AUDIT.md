# Script surface audit

**Audit date:** 2026-09-28  
**Scope:** root wrappers, `scripts/`, `scripts_v2/`, `pipeline/`, and related
execution entry points

## Finding

The workspace has one current application pipeline plus a separate search-bot
system. Most of the remaining scripts are preserved older routes, diagnostics,
or one-off utilities. The safest immediate filter is an explicit active allowlist;
physical moves or deletion should be a later, separately reviewed change.

## Evidence used

- `job-runner.ps1` invokes only `scripts/canonical_runner.py`.
- `env_setter.ps1` is loaded by the current runner and prepares the repository
  environment; it is an active bootstrap, not a pipeline stage.
- The archived root `00.job-chatgpt-*.ps1` through `06*.intake-*.ps1` invoked the
  old manual ChatGPT/numbered route. They were not referenced by the canonical
  runner.
- Archived `06d.intake-from-clipboard-dice.ps1` references a missing `05a...`
  file and is broken legacy material.
- `archive/2026-09-28/root_cleanup/machine_maintenance/nightly-drive-maintenance.ps1`
  performs disk/volume maintenance and is not a job-search pipeline dependency.
- `scripts/canonical_runner.py` imports `scripts/build_runtime_profile.py` and
  the `src/` pipeline/AI modules.
- `src/pipeline/artifacts.py` dynamically loads
  `05_render_resume.py`, `08_render_cover_letter.py`, and `quality_check.py`.
- `src/pipeline/local_gate.py` uses `scripts/utils/vector_ops.py` for the
  duplicate gate.
- Runtime-profile and model-profile tests import
  `build_runtime_profile.py` and `model_profile.py`.
- `search_bots/run_indeed.ps1` and `refresh_sor.ps1` route to the eight
  `search_bots_*` support scripts listed in `scripts/README.md`.
- `docs/CUTOVER_REPORT.md` explicitly identifies the numbered generation
  scripts, multi-call orchestrators, and older wrappers as legacy for normal
  execution.

## Keep/use now

| Area | Active files |
|---|---|
| Entry | `job-runner.ps1`, `env_setter.ps1` |
| Canonical pipeline | `scripts/canonical_runner.py`, `build_runtime_profile.py`, `model_profile.py` |
| Artifact support | `05_render_resume.py`, `08_render_cover_letter.py`, `normalize_resume_intermediate.py`, `quality_check.py` |
| Gate support | `scripts/utils/vector_ops.py` |
| Search bots | `search_bots_indeed.py`, `search_bots_indeed_live.py`, `search_bots_schedule.py`, `search_bots_dna.py`, `search_bots_filters.py`, `search_bots_handoff.py`, `search_bots_notify.py`, `search_bots_sor.py` |

## Root PowerShell classification

| Classification | Files | Action |
|---|---|---|
| Keep/use | `job-runner.ps1`, `env_setter.ps1` | Current route |
| Separate maintenance | `archive/2026-09-28/root_cleanup/machine_maintenance/nightly-drive-maintenance.ps1` | Keep outside the job-search route; restore/run manually only |
| Archived legacy/manual | `archive/2026-09-28/00.job-chatgpt-*.ps1`, `archive/2026-09-28/06*.intake-*.ps1` | Recover only through the archive map |

## Do not use for new work

- `scripts/00_check_applied_before.py` through `09_update_application_status.py`
  as a pipeline route; they belong to the pre-cutover workflow, although the
  renderers they call are still reused by the canonical package.
- `scripts/10_auto_pipeline.py` and `10b_force_pipeline.py`; the force variant
  bypasses safeguards identified in the cutover report.
- `scripts_v2/`, `pipeline/`, and `ps1_keep/`; preserved manual or historical
  routes.
- `scripts/Archived/`, `scripts/keep/`, root ChatGPT wrappers, audio/Gmail
  utilities, old provider tests, and one-off export/migration helpers.
- Search-bot probe files except when explicitly diagnosing browser behavior.
- Archived root ChatGPT wrappers and clipboard intake helpers except when
  deliberately reproducing the old manual flow.

## Recommended filtering sequence

1. Use `scripts/README.md` as the active allowlist immediately.
2. Search only active documentation and code before moving any legacy file.
3. Run the canonical offline tests and the focused search-bot test after each
   move batch.
4. Move confirmed legacy files to a clearly named archive area, preserving
   relative references or adding a redirect README.
5. Delete nothing until the archive has been used successfully for one cycle.

The first archive batch moved 11 root wrappers plus `ps1_keep/` and `scripts_v2/`
on 2026-09-28. The full mapping and retention dates are in
`archive/ARCHIVE_MAP.md`.
