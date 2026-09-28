# Prompt 04 Cline Operators and Human Documentation

## Recommended TUI setting

- Model: `gpt-5.6-sol`
- Reasoning: `xhigh`

## Paste into Codex TUI

You are working in `D:\Workarea\jobsearch`.

Read, in order, `AGENTS.md`, `BOOTSTRAP.md`, `PROFILE.md`, `PROJECT_MEMORY.md`, and `CURRENT_STATE.md`. Then read the canonical pipeline and runtime-profile documentation created by earlier work. Sean manages Git: do not create branches, commit, stage, reset, or alter unrelated worktree changes.

## Objective

Replace stale, overlapping job-search instructions with a small, authoritative operational documentation set for Cline and for Sean running commands manually.

## Create or update

1. `CLINE_JOBSEARCH_RUNNER.md`
   - one-page operational instruction file for a low-cost Cline runner;
   - tells it exactly what files to read and what command to run;
   - explicitly prohibits broad repository exploration unless a command fails;
   - requires duplicate gate first, explicit overrides, truth checks, cost reporting, and output-path reporting;
   - states that it must not auto-mark a job applied unless explicitly asked.

2. `CLINE_JOBSEARCH_REASONER.md`
   - one-page instruction file for a stronger discussion/maintenance agent;
   - supports career discussion, fit tradeoffs, profile maintenance, pipeline diagnosis, and real-job strategy;
   - does not mutate records or documents without an explicit request;
   - includes public-safety and positioning rules.

3. `docs/PIPELINE_OPERATOR.md`
   - concise human runbook for the new canonical pipeline;
   - quick-start commands;
   - manual gate/triage/generate/apply commands;
   - model profile switching;
   - override examples;
   - cache behavior;
   - exact output locations;
   - recovery steps.

4. `docs/PIPELINE_ARCHITECTURE.md`
   - short technical reference describing Tier 0, Tier 1, Tier 2, metadata states, cache/provenance, and cost controls.

5. Update or clearly deprecate stale instructions such as `AGENTS_CONTEXT.md`, `PIPELINE_RUNBOOK.md`, and `PIPELINE_SELF_RUN.md` without deleting historical content. The active route must be unmistakable.

## Required operating rules

- Project purpose: job intake, job scoring, tailored resumes/covers, application tracking, gigs, and application interview preparation for Sean Girgis.
- Current employer is LTIMindtree; do not name the client in public job artifacts.
- CAPTAIN is research, not production.
- Sean is strongest in capacity, performance, observability, Python automation, reporting, and practical AI workflows. Do not represent him as a generic DS/ML specialist.
- Do not invent career history, claims, metrics, dates, skill depth, or production status.
- One job or pipeline step at a time unless Sean asks otherwise.
- Sean manages Git unless he explicitly delegates it.

## Constraints

- Do not build a giant manifesto or duplicate the same rules across many files.
- Do not change pipeline code, master data, job records, or resumes in this task.
- Use `apply_patch` for edits.

## Validation and report

Check all command examples against the actual implementation. Report the authoritative file hierarchy, deprecated files, and any commands that could not be validated.

