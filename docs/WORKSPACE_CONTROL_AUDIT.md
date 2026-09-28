# Workspace control audit

**Audit date:** 2026-09-28  
**Workspace:** `D:\Workarea\jobsearch`  
**Scope:** job-search pipeline, resumes, applications, gigs, interview-prep-for-applications, and search bots

## Executive finding

The workspace is operationally usable but structurally crowded. Before this
audit, the working tree was clean, while the repository contained several generations of
pipeline code, a large committed output/data surface, historical instructions,
and an unfinished search-bot scheduler transition.

The immediate control problem is documentation and routing: an agent can find
the correct path, but it can also encounter older guides that still describe
deprecated wrappers or an older source-of-truth model. The initial audit did not
delete or move files; a documented follow-up cleanup on 2026-09-28 archived the
obsolete root surfaces without deleting them.

## Evidence snapshot

- Branch: `main`, clean, one commit ahead of `origin/main`.
- HEAD: `c8a20f6` (`checking in code`), 2026-09-28.
- That commit changed **857 files**, adding about **92,799 lines**. The largest
  category was `data` (712 changed files), followed by search-bot material and
  generated/output files.
- Tracked-file shape is dominated by `data` (8,458 files), then `scripts` (57),
  `docs` (46), and `search_bots` (26). This is why a full-tree browse is a poor
  operating model.
- The IDE-open job `data/jobs/00395_7831adc7` is a historical Scale AI
  application marked `APPLIED` on 2026-09-12. It is not the canonical runner's
  current work item.
- The canonical runner smoke shell is `data/jobs/runner_420173c2`; its recorded
  result is `TIER0_CLEAR` and its next command is a triage run for
  `intake/smoke_test.md`.

## Effective control plane

Read these files for normal workspace operation, in this order:

1. `AGENTS.md`
2. `_agent/README.md`
3. `_agent/RULES.md`
4. `_agent/STATE.md`
5. The route map in `_agent/README.md`
6. `docs/PIPELINE_OPERATOR.md` or the specifically named task documentation

Use these as the active implementation surface:

- `job-runner.ps1`
- `scripts/canonical_runner.py`
- `src/pipeline/`
- `config/`
- `tests/test_canonical_pipeline.py`
- `data/master/` and the generated runtime profile described by
  `docs/RUNTIME_PROFILE.md`
- Script filter: `docs/SCRIPT_SURFACE_AUDIT.md` with the active allowlist in
  `scripts/README.md`

For search bots, use the separate control plane:

- `search_bots/agent_work/HANDOFF.md`
- `search_bots/agent_work/NEXT.md`
- `search_bots/documentation/LIVE.md`
- `search_bots/run_indeed.ps1`
- `scripts/search_bots_schedule.py` and the other specifically named bot scripts

## What changed most recently

The 2026-09-28 check-in consolidated the newer canonical pipeline and added or
recorded a substantial amount of job/search output. The meaningful operational
changes are:

- The canonical `job-runner.ps1` path is now the preferred execution route.
- The canonical pipeline has explicit gate, triage, generate, and apply-only
  stages, persisted decisions, versioned generated packages, cache identity, and
  local application recording.
- The older numbered scripts and ChatGPT/manual wrappers remain present for
  compatibility and history; they are not the normal route.
- Search bots have a working Indeed/OpenRouter/SQLite/DNA design, but the
  approved replacement scheduler is not implemented: current code is still
  one phrase per run with `fromage=1`; the planned policy is 24 jittered,
  non-overlapping runs, dynamic 2–3 phrase batches, and `fromage=2`.
- Search-bot output, logs, captures, and handoff material were committed in
  bulk. These are operational evidence and output, not additional control-plane
  instructions.

## Stale or conflicting surfaces to contain

1. **Legacy pipeline guides.** Historical root guides are now preserved under
   `archive/2026-09-28/root_cleanup/compatibility/`. `docs/CUTOVER_REPORT.md`
   identifies the remaining legacy wrappers and historical docs that should not
   be used as the normal route.
2. **Old source-of-truth language.** Several historical guides still name
   `data/source_of_truth.json` as authoritative. The current runtime path uses
   `data/master/`, stated-work evidence, rules, and the derived runtime profile;
   `source_of_truth.json` is legacy compatibility material for the bot path.
3. **Search-bot transition.** `LIVE.md`, `HANDOFF.md`, `NEXT.md`, and the bot
   design documents agree that the new scheduler is approved but pending. This
   must remain visibly marked as *planned*, not *deployed*.
4. **Generated and scratch material.** `data/jobs/`, `data/search_bots/`,
   `scratch/`, `tmp/`, and resume output are valuable records but should be
   treated as data/output zones, not documentation zones.
5. **Status freshness.** The old `CURRENT_STATE.md` was a compatibility file;
   current status is maintained in `_agent/STATE.md`.

6. **Root Markdown.** The root is limited to `AGENTS.md` and the current
   `README.md`. Historical startup notes, old manual ChatGPT guidance, stale
   project analysis, the root job intake, and compatibility redirects are
   archived. Coding conventions moved to `docs/CODING_STYLE.md`.

## Recommended control model

### Keep at the root

Only entry-point and policy files should be routinely opened from the root:
`AGENTS.md`, `_agent/`, `job-runner.ps1`, and `env_setter.ps1`.
Historical root instruction filenames are preserved in the dated archive.

### Treat as three zones

| Zone | Examples | Rule |
|---|---|---|
| Control plane | `AGENTS.md`, `docs/PIPELINE_OPERATOR.md`, runner/code/tests | Edit deliberately; keep authoritative |
| Active work | `intake/`, selected `data/jobs/runner_*`, `data/master/`, `resume_output/` | Inspect only for the current job or requested step |
| Historical/output | legacy scripts, `startingDocs/`, `user_guide/`, old MyFuture chats, bulk logs/captures | Preserve; do not route new work through it |

### Safe next cleanup sequence

1. Reconcile status documents with the canonical runner and the parked search-bot
   state.
2. Add explicit `LEGACY` or `HISTORICAL` markers to high-risk old entry-point
   docs, without deleting their contents.
3. Create a retention/index policy for generated job folders, search captures,
   logs, and scratch artifacts. Do not delete records until Sean approves the
   retention rule.
4. Finish and test the approved 24-slot search-bot scheduler before installing
   Task Scheduler or a container.
5. After the scheduler and documentation agree, consider a separate archival
   move for clearly historical material. That should be a separately reviewed,
   reversible change.

## Follow-up cleanup: 2026-09-28

The root cleanup preserved and mapped the following non-active surfaces:

- ten obsolete instruction redirects into
  `archive/2026-09-28/root_cleanup/compatibility/`;
- three unreferenced job-cache files into `root_cleanup/caches/`;
- command history and the direct OpenRouter smoke script into
  `root_cleanup/legacy_tools/`;
- an unrelated shortcut and registry backup into `root_cleanup/unrelated/`;
- the separate disk-maintenance utility into
  `root_cleanup/machine_maintenance/`.

The runtime-profile builder now treats `_agent/RULES.md` as its guardrail source,
and the derived profile was rebuilt and validated offline. See
`archive/ARCHIVE_MAP.md` for recovery and retention dates.

The same follow-up archived stale vendor-specific control folders (`.codex`,
`.grok`, `.antigravity`), generated/cache folders, and historical temporary
resume artifacts under `archive/2026-09-28/root_hidden/`. `.claude` remains in
place because Git registers a nested Claude worktree beneath it; `.git`, `.venv`,
and `.vscode` remain active repository, environment, and editor state.

## Current blockers / decisions needed

- The search-bot scheduler policy is approved but not implemented.
- Local Task Scheduler/container hosting is not installed.
- The canonical cutover report records that local model profile IDs still need
  configuration before paid stages can be treated as ready.
- Sean manages Git; this audit does not push, merge, or alter remote history.

## Audit conclusion

The workspace does not need a destructive reset. It needs a stable index,
stronger legacy labeling, and a retention policy for output-heavy directories.
The canonical runner and the search-bot handoff are the two active operating
systems; everything else should be treated as source material, history, or
generated output unless a task explicitly names it.
