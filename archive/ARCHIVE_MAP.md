# Archive map

## Retention policy

- **Review:** 90 days after archive (`2026-12-27`).
- **Destruction eligible:** 180 days after archive (`2027-03-27`).
- **Deletion:** never automatic; requires explicit Sean approval after a
  dependency and recovery check.
- **Recovery:** move the mapped entry back to its original path, preserving the
  relative structure shown below.

## Archive batch: 2026-09-28

| Original path | Archived path | Reason |
|---|---|---|
| `00.job-chatgpt-check.ps1` | `archive/2026-09-28/00.job-chatgpt-check.ps1` | Legacy manual duplicate-check wrapper |
| `01.job-chatgpt-check.ps1` | `archive/2026-09-28/01.job-chatgpt-check.ps1` | Legacy manual duplicate-check wrapper |
| `02.job-chatgpt-accept.ps1` | `archive/2026-09-28/02.job-chatgpt-accept.ps1` | Legacy manual acceptance/v2 shell wrapper |
| `03.job-chatgpt-render.ps1` | `archive/2026-09-28/03.job-chatgpt-render.ps1` | Legacy manual render/apply wrapper |
| `04.job-chatgpt-stats.ps1` | `archive/2026-09-28/04.job-chatgpt-stats.ps1` | Legacy statistics helper |
| `05.job-chatgpt-search.ps1` | `archive/2026-09-28/05.job-chatgpt-search.ps1` | Legacy metadata search helper |
| `06d.intake-from-clipboard-dice.ps1` | `archive/2026-09-28/06d.intake-from-clipboard-dice.ps1` | Legacy and references missing `05a...` |
| `06I.intake-from-clipboard-indeed.ps1` | `archive/2026-09-28/06I.intake-from-clipboard-indeed.ps1` | Legacy clipboard intake helper |
| `06L.intake-from-clipboard-linkedin.ps1` | `archive/2026-09-28/06L.intake-from-clipboard-linkedin.ps1` | Legacy clipboard intake helper |
| `06m.intake-from-clipboard-monster.ps1` | `archive/2026-09-28/06m.intake-from-clipboard-monster.ps1` | Legacy clipboard intake helper |
| `06w.intake-from-clipboard-wellfound.ps1` | `archive/2026-09-28/06w.intake-from-clipboard-wellfound.ps1` | Legacy clipboard intake helper |
| `ps1_keep/` | `archive/2026-09-28/ps1_keep/` | Preserved backup wrappers |
| `scripts_v2/` | `archive/2026-09-28/scripts_v2/` | Manual artifact pipeline superseded by canonical runner |
| `JobSearch_V2/` | `archive/2026-09-28/JobSearch_V2/` | Historical manual prompt/template project; not part of the current executable pipeline |

## Root Markdown batch: 2026-09-28

| Original path | Archived path | Reason |
|---|---|---|
| `AGENT_STARTUP_NOTES.md` | `archive/2026-09-28/root_docs/AGENT_STARTUP_NOTES.md` | Superseded by `_agent/` startup contract |
| `CHATGPT_PIPELINE.md` | `archive/2026-09-28/root_docs/CHATGPT_PIPELINE.md` | Describes archived manual wrappers |
| `jobsearch-project-analysis.md` | `archive/2026-09-28/root_docs/jobsearch-project-analysis.md` | Stale February architecture analysis |
| `intake_inspiren_senior_data_engineer_2026-04-13.md` | `archive/2026-09-28/root_docs/intake_inspiren_senior_data_engineer_2026-04-13.md` | Historical job intake misplaced at repository root |

`CodingStyle.md` was not destroyed; it was relocated to
`docs/CODING_STYLE.md`, where technical standards belong.

## Root cleanup batch: 2026-09-28

| Original path(s) | Archived path | Reason |
|---|---|---|
| `AGENTS_CONTEXT.md`, `BOOTSTRAP.md`, `CLINE_JOBSEARCH_REASONER.md`, `CLINE_JOBSEARCH_RUNNER.md`, `CURRENT_STATE.md`, `JOBSEARCH_DRIVER.md`, `PIPELINE_RUNBOOK.md`, `PIPELINE_SELF_RUN.md`, `PROFILE.md`, `PROJECT_MEMORY.md` | `archive/2026-09-28/root_cleanup/compatibility/` | Superseded root redirects; durable control now lives in `AGENTS.md` and `_agent/` |
| `.job_cache.json`, `.job_cache_chatgpt.json`, `.job_cache_v2.json` | `archive/2026-09-28/root_cleanup/caches/` | Unreferenced legacy/manual cache state |
| `commands_history.lst`, `testOpenRouter.py` | `archive/2026-09-28/root_cleanup/legacy_tools/` | Local history and superseded direct OpenRouter smoke script |
| `data - Shortcut.lnk`, `RunKey_Backup_OperaRemoval.reg` | `archive/2026-09-28/root_cleanup/unrelated/` | Unrelated workstation artifacts |
| `nightly-drive-maintenance.ps1` | `archive/2026-09-28/root_cleanup/machine_maintenance/` | Separate disk-maintenance utility, not a job-search control |

## Hidden root cleanup batch: 2026-09-28

| Original path | Archived path | Reason |
|---|---|---|
| `.codex/` | `archive/2026-09-28/root_hidden/.codex/` | Stale vendor-specific scaffold referencing archived `job-v2-*` commands; superseded by `AGENTS.md` and `_agent/` |
| `.grok/` | `archive/2026-09-28/root_hidden/.grok/` | Older vendor-specific constitution/rules; superseded by the vendor-neutral control plane |
| `.antigravity/` | `archive/2026-09-28/root_hidden/.antigravity/` | Unused vendor-specific placeholder memory/rules |
| `.ruff_cache/` | `archive/2026-09-28/root_hidden/.ruff_cache/` | Regenerable linter cache |
| `.tmp_lasalle_resume/` | `archive/2026-09-28/root_hidden/.tmp_lasalle_resume/` | Historical temporary resume build artifacts |
| `.tmp_resume_qa_8be8a18b/` | `archive/2026-09-28/root_hidden/.tmp_resume_qa_8be8a18b/` | Empty temporary QA directory |

## Deliberately not archived

- `job-runner.ps1` and `env_setter.ps1` — active controls.
- `nightly-drive-maintenance.ps1` — separate machine-maintenance utility.
- `pipeline/` — older maintenance utilities still referenced by historical
  documentation; requires a separate dependency review.
- Active files listed in `scripts/README.md` and current search-bot wrappers.

## Restore pattern

Restore a whole group only after checking the original path is free:

```powershell
Move-Item -LiteralPath .\archive\2026-09-28\ps1_keep -Destination .\ps1_keep
Move-Item -LiteralPath .\archive\2026-09-28\scripts_v2 -Destination .\scripts_v2
Move-Item -LiteralPath .\archive\2026-09-28\JobSearch_V2 -Destination .\JobSearch_V2
```

The root cleanup groups can be restored by moving their individual files back to
the repository root only after checking that the current path is intentionally
free. The compatibility group should not be restored as an active policy
surface; use `_agent/` as the authoritative control plane.

The hidden root groups preserve their dot-prefixed names under
`root_hidden/`. `.claude/` is intentionally not listed as archived: Git reports
`.claude/worktrees/determined-cori-b1ea34` as a registered worktree, so moving
it without a deliberate Git worktree operation could corrupt repository state.

For root files, move the exact filename from `archive/2026-09-28/` to the
repository root. Do not bulk-restore the archive without reviewing the map.
