# Prompt 03 Canonical Cost Controlled Pipeline

## Recommended TUI setting

- Model: `gpt-6-astra`
- Reasoning: `ultra`

## Paste into Codex TUI

You are working in `D:\Workarea\jobsearch`.

Read, in order, `AGENTS.md`, `BOOTSTRAP.md`, `PROFILE.md`, `PROJECT_MEMORY.md`, and `CURRENT_STATE.md`. Then read the provider/model-profile implementation and runtime-profile implementation already completed in this repository. Sean manages Git: do not create branches, commit, stage, reset, or alter unrelated worktree changes.

## Objective

Finish the migration to one canonical, cost-controlled job pipeline. Preserve legacy scripts during migration, but make one new documented path authoritative.

## Required flow

```text
intake
  -> Tier 0 local duplicate and eligibility gate
  -> Tier 1 one economy structured LLM analysis
  -> explicit user/agent decision or explicit override
  -> Tier 2 one quality LLM package call for resume and optional cover
  -> local render and quality check
  -> READY_TO_APPLY by default
  -> ASSUMED_APPLIED only with an explicit flag
```

## Required behavior

1. Tier 0:
   - normalize intake;
   - exact-hash and existing FAISS duplicate check before paid calls;
   - create a stable `score/local_gate.json`;
   - never make a paid call;
   - if duplicate/blocked, stop unless the caller passes an explicit duplicate override with a reason.

2. Tier 1:
   - use the `economy` model profile;
   - make at most one structured analysis call per unique cache key;
   - write `tailored/job_packet.json` and a readable `score/llm_gate_report.md`;
   - provide score, fit rationale, key strengths, gaps, recommendation, keywords, and tailoring plan;
   - use the compact runtime profile, not the old large source-of-truth dump.

3. Decision and override:
   - preserve separate `tier0_decision`, `llm_decision`, and `user_decision` fields;
   - support explicit duplicate override and suitability override, each requiring a reason;
   - never silently accept or reject based on model output alone.

4. Tier 2:
   - run only after explicit acceptance/override or an explicit generate command;
   - use the `quality` model profile;
   - produce resume intermediate JSON and optional cover intermediate JSON in one package call where practical;
   - use existing local renderers after structured artifacts exist;
   - do not add a paid company-research-only call to the normal route.

5. Final state:
   - default to `READY_TO_APPLY` and print exact job folder, resume path, cover path, model/profile used, cache result, and next command;
   - support `--assume-applied --method <method> --date <YYYY-MM-DD> --notes <text>` to record an application intentionally;
   - never automatically mark an application submitted without that explicit flag.

6. Caching/provenance:
   - cache key must include job hash, runtime-profile hash, prompt version, and model/profile identity;
   - cache hits must avoid paid calls;
   - write provenance to generated artifacts or adjacent metadata.

## Suggested interface

Prefer one new clear command, for example:

```powershell
.\job-runner.ps1 .\intake\intake.md -Mode triage
.\job-runner.ps1 .\intake\intake.md -Mode generate
.\job-runner.ps1 .\intake\intake.md -Mode generate -OverrideDuplicate -Reason "New requisition"
.\job-runner.ps1 .\intake\intake.md -Mode generate -OverrideSuitability -Reason "Strategic application"
.\job-runner.ps1 .\intake\intake.md -Mode generate -AssumeApplied -Method LinkedIn
```

You may choose exact file names and a Python/PowerShell split that fits existing conventions, but keep it simple and document it.

## Constraints

- Keep legacy scripts untouched unless a minimal compatibility change is necessary.
- Do not delete historical job folders, application records, or master data.
- Do not call paid models during tests. Add mock/dry-run paths.
- Before Python, run `.\env_setter.ps1`.
- Use `apply_patch` for edits.

## Required tests

1. Duplicate job: zero paid calls and explicit override path.
2. Triage path: Tier 0 then one mocked Tier 1 analysis, then stop.
3. Accepted generation path: mocked Tier 1 and Tier 2 artifacts, then local renderer boundary verification.
4. Cache hit: no additional Tier 1 or Tier 2 call.
5. `READY_TO_APPLY` versus explicit `--assume-applied` state behavior.

Report changed files, commands, actual test results, compatibility notes, and the exact canonical commands for Sean.

