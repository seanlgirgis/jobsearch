# Prompt 02 Sanitized Runtime Profile

## Recommended TUI setting

- Model: `gpt-6-astra`
- Reasoning: `xhigh`

## Paste into Codex TUI

You are working in `D:\Workarea\jobsearch`.

Read, in order, `AGENTS.md`, `BOOTSTRAP.md`, `PROFILE.md`, `PROJECT_MEMORY.md`, and `CURRENT_STATE.md`. Sean manages Git: do not create branches, commit, stage, reset, or alter unrelated worktree changes.

## Objective

Create a compact, sanitized runtime candidate profile for job-analysis and application-generation prompts. This should reduce prompt size and prevent stale, irrelevant, confidential, or exaggerated content from reaching cheap runner models.

## Authoritative inputs

- `data/master/master_career_data.yaml`
- `data/master/skills.yaml`
- `data/master/bofa_stated_ai_work.md`
- `outbox/sean_girgis_searchable_profile.md` for positioning only, never as stronger evidence than master sources
- Director `SEAN.md` and `SEAN_NOW.md` if present

## Required deliverables

1. Add `scripts/build_runtime_profile.py` that deterministically builds a compact JSON runtime profile from the inputs above.

2. Write the generated profile to `data/master/candidate_profile_runtime.json` and a short provenance/validation report next to it. Treat the generated file as derived data; do not overwrite the raw master evidence.

3. Include only:
   - public preferred identity/contact data required for documents;
   - target positioning: capacity, performance, observability, Python automation, reporting, practical AI, and selective part-time consulting/senior roles;
   - verified skill tiers;
   - concise recent and flagship evidence;
   - a compact selected-bullet bank;
   - public-safety constraints;
   - target job-family keywords.

4. Encode safety rules in the runtime profile:
   - current employer is LTIMindtree;
   - do not name the client publicly;
   - CAPTAIN is research/investigation, not production;
   - do not claim Databricks, Delta Lake, dbt, Snowflake, Unity Catalog, DLT, or Azure data-platform foundations as professional production expertise;
   - do not invent titles, dates, metrics, certifications, or production status;
   - do not position Sean as a generic data-science or ML specialist.

5. Add validation that fails clearly if required source files are missing or if prohibited client wording appears in the generated runtime profile.

6. Add a short `docs/RUNTIME_PROFILE.md` explaining sources, regeneration command, intended consumers, and the difference between source evidence and derived runtime context.

## Constraints

- Do not delete, rewrite, or “clean up” master history. Sanitization means generating a smaller derived profile, not destroying evidence.
- Do not expose internal prompts, internal client data, credentials, URLs, or unlisted tools.
- Do not run paid LLM calls.
- Before Python, run `.\env_setter.ps1`.
- Use `apply_patch` for edits.

## Validation and report

Run the builder and validation locally. Report profile size, source files used, exclusions made, and proof that prohibited client references are absent.

