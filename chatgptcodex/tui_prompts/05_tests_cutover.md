# Prompt 05 Tests Cutover and Data Safety Audit

## Recommended TUI setting

- Model: `gpt-6-astra`
- Reasoning: `ultra`

## Paste into Codex TUI

You are working in `D:\Workarea\jobsearch`.

Read, in order, `AGENTS.md`, `BOOTSTRAP.md`, `PROFILE.md`, `PROJECT_MEMORY.md`, and `CURRENT_STATE.md`. Then read the new provider/model profile, runtime profile, canonical pipeline, and operator documentation created by earlier prompts. Sean manages Git: do not create branches, commit, stage, reset, or alter unrelated worktree changes.

## Objective

Verify the new canonical job pipeline end to end without paid API calls, clean only derived/stale operational artifacts where safe, and make the new route the unambiguous default.

## Required verification

1. Run or add deterministic tests for:
   - duplicate detection stops before Tier 1;
   - explicit duplicate override is recorded and continues;
   - mocked Tier 1 produces schema-valid job packet and readable report;
   - suitability override is recorded and continues;
   - mocked Tier 2 produces renderer-compatible resume and cover JSON;
   - cache hit prevents repeated Tier 1/Tier 2 calls;
   - default completion is `READY_TO_APPLY`;
   - explicit `--assume-applied` updates only the intended job metadata.

2. Validate runtime-profile generation:
   - no client-name reference in public runtime context;
   - CAPTAIN remains research;
   - no unsupported beginner tools are described as production capabilities;
   - source provenance is present.

3. Audit data and documentation for operational confusion:
   - identify stale entry points, obsolete model defaults, and scripts that would make paid calls unexpectedly;
   - preserve legacy code and historical job records;
   - do not delete material data without Sean’s explicit approval;
   - if cleanup is appropriate, prefer deprecation notices, archival labels, or exclusion from the active route.

4. Produce `docs/CUTOVER_REPORT.md` containing:
   - tests run and observed results;
   - canonical commands;
   - legacy paths intentionally retained;
   - known limitations;
   - a short recovery procedure;
   - checklist for the first real OpenRouter economy-model smoke test.

## Constraints

- Do not use real OpenRouter, xAI, or OpenAI keys or make paid requests.
- Do not delete job folders, source evidence, resume outputs, or master career files.
- Before Python, run `.\env_setter.ps1`.
- Use `apply_patch` for edits.

## Final report

Give Sean a precise go/no-go recommendation for one real low-cost smoke test. Include files changed, commands run, actual outcomes, failures, and the exact next command to execute when Sean is ready.

