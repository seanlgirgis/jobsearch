# Codex Refactor Spec (v1)

## Goal
Reduce xAI call count from 5 calls/job to:
- 1 call for most jobs
- 2 calls only for accepted high-value jobs
- 0 calls for rejected jobs after Tier 0 gate

## Current -> Target Mapping
- Replace `01_score_job.py` + `03_tailor_job_data.py` with `01_analyze_job.py`
- Replace `06_company_research.py` + `07_generate_cover_intermediate.py` with `06_generate_cover_package.py`
- Replace/absorb `04_generate_resume_intermediate.py` into `04_generate_application_package.py` (Tier 2 only)
- Keep local scripts unchanged in purpose:
  - `00_check_applied_before.py`
  - `02_decide_job.py`
  - `05_render_resume.py`
  - `08_render_cover_letter.py`
  - `09_update_application_status.py`
  - `10_auto_pipeline.py` (orchestration and branching)

## New Script Contracts

## `01_analyze_job.py` (Tier 1 single call)
Inputs:
- `data/jobs/<id>/raw/*.md`
- `data/source_of_truth.json` (or derived compact profile snapshot)
- optional cache key context (`prompt_version`, `model`, profile hash)

Outputs:
- `data/jobs/<id>/score/local_gate.json` (copied/linked from Tier 0 decision)
- `data/jobs/<id>/score/llm_gate_report.md`
- `data/jobs/<id>/tailored/job_packet.json`
- metadata update in `data/jobs/<id>/metadata.yaml`:
  - `analysis_hash`
  - `profile_hash`
  - `prompt_version`
  - `model`
  - `decision` (`skip|hold|proceed`)
  - `score`

Single LLM response must include:
- fit score + recommendation
- rationale
- structured extraction:
  - role/title/company/location/employment type
  - must-have and nice-to-have skills
  - requirements/responsibilities
  - ATS keywords
  - missing skills/risk flags
  - positioning angle

Rules:
- one parse/write pass produces both score and tailored outputs
- if cache key exists, skip LLM call

## `04_generate_application_package.py` (Tier 2 premium call)
Run conditions:
- Tier 1 decision = `proceed`
- score >= Tier 2 threshold
- job priority = high

Inputs:
- `tailored/job_packet.json`
- `data/source_of_truth.json`
- optional existing company profile cache

Outputs:
- `generated/resume_intermediate_v1.json`
- `generated/cover_intermediate_v1.json` (optional if cover requested)
- `research/company_profile_v1.yaml`
- `generated/application_package_preview.md`

Single LLM response must include:
- resume intermediate structure
- cover intermediate structure
- company/tone values summary
- evidence/grounding block (keywords and source snippets)

Rules:
- max one premium call in this stage
- renderers stay local-only

## `06_generate_cover_package.py` (interim merge path)
If incremental migration is preferred before full `04_generate_application_package.py`:
- Merge company research + cover generation in one call.
- Never run standalone company-research-only LLM call.

## Orchestrator Branching (`10_auto_pipeline.py`)
Branch modes:
- `triage`: Tier 0 -> Tier 1 -> stop unless proceed
- `accepted_resume_only`: Tier 0 -> Tier 1 -> Tier 2 resume path -> render
- `accepted_resume_and_cover`: Tier 0 -> Tier 1 -> Tier 2 package -> render both

Stop rules:
- duplicate/local reject: stop immediately
- Tier 1 `skip`: stop
- Tier 1 `hold`: queue manual review

## Cache & Idempotency Requirements
Before any LLM call, check artifacts:
- if `tailored/job_packet.json` exists and hashes match, reuse
- if `generated/resume_intermediate_v1.json` exists and hashes match, reuse
- if `generated/cover_intermediate_v1.json` exists and hashes match, reuse

Cache key:
- `job_hash + profile_hash + prompt_version + model`

## Implementation Order
1. Build `01_analyze_job.py` and wire into `10_auto_pipeline.py`.
2. Remove direct calls to `03_tailor_job_data.py` from pipeline path.
3. Add metadata hash/version fields and cache checks.
4. Build `06_generate_cover_package.py` (if doing incremental migration).
5. Build `04_generate_application_package.py` and gate it by Tier 2 conditions.
6. Decommission superseded scripts after parity tests pass.

## Acceptance Criteria
- Rejected jobs incur 0 paid calls after local gate.
- Most jobs finish with 1 paid call total.
- Top-tier jobs use at most 2 paid calls total.
- No duplicate paid call occurs when cache artifacts are valid.
- Renderers (`05`, `08`) run without AI dependencies.
