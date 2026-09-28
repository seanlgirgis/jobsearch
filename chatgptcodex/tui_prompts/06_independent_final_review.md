# Prompt 06 Independent Final Architecture Review

## Recommended TUI setting

- Model: `gpt-6-astra`
- Reasoning: `ultra`

## Paste into Codex TUI

You are conducting a read-only independent review of the job-search pipeline in `D:\Workarea\jobsearch` after an OpenRouter/model-profile and Tier 0/1/2 pipeline revamp.

Read `AGENTS.md`, `BOOTSTRAP.md`, `PROFILE.md`, `PROJECT_MEMORY.md`, `CURRENT_STATE.md`, the current canonical docs, active commands, provider client, runtime-profile builder, tests, and cutover report. Do not alter any files, run paid calls, modify job records, or perform Git operations.

## Review questions

1. Is there exactly one clear operational pipeline route?
2. Can an economy Cline runner process one job without broad repository discovery?
3. Are duplicate and suitability gates local/cheap first and explicitly overrideable?
4. Are paid calls bounded to one economy analysis call and one quality package call for accepted jobs?
5. Do caching and provenance prevent duplicate spend?
6. Can model switching occur through one local profile configuration rather than source edits?
7. Does the public candidate profile avoid client identification, unsupported claims, and DS/ML over-positioning?
8. Does normal completion stop at `READY_TO_APPLY`, with application logging only by explicit request/flag?
9. Are legacy paths clearly retained but non-default?
10. Are tests adequate before a first real low-cost smoke test?

## Required output

Provide a concise review with:

- go / conditional-go / no-go verdict;
- strengths;
- blockers ordered by severity;
- exact file paths and line references for actionable findings;
- recommended first real smoke-test command;
- no edits.

