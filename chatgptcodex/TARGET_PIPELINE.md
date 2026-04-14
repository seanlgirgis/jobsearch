# Target Pipeline (Cost-Optimized v1)

## Objective
Hit the charter targets:
- 60-80% lower paid LLM usage
- Max 1 paid call for most jobs
- Max 2 paid calls only for top-tier jobs
- Zero paid calls for rejected jobs

## Tier 0 (Free / Local First)
Run these steps for every incoming job before any paid LLM:
- Normalize posting text and hash content (`sha256`) for cache keys.
- Duplicate check:
  - exact hash match
  - high-similarity embedding match (FAISS threshold >= 0.82)
- Rule-based filters:
  - hard blockers (location, visa, salary floor, contract type)
  - title/domain allowlist + denylist
- Lightweight keyword score from local extracted terms:
  - must-have skills match rate
  - years-of-experience phrase match
  - seniority mismatch penalty

Output:
- `data/jobs/<id>/score/local_gate.json`
- Decision: `reject_early`, `needs_llm`, `strong_match`

Cost rule:
- If `reject_early`, stop pipeline (0 paid calls).

## Tier 1 (Cheap LLM: Single Consolidated Call)
For `needs_llm` and `strong_match`, do one low-cost LLM call that combines:
- fit scoring
- structured extraction (requirements, ATS keywords, must/nice-to-have)
- brief resume tailoring plan (not full prose rewrite)
- decision recommendation (`skip`, `hold`, `proceed`)

Prompt contract:
- strict JSON schema
- deterministic settings where possible
- include only compact context (job text + minimal profile summary)

Caching:
- key = `job_hash + profile_hash + prompt_version + model`
- if cache hit, reuse output and skip call

Output:
- `tailored/job_packet.json`
- `score/llm_gate_report.md`

Cost rule:
- Most jobs end here (max 1 paid call total).

## Tier 2 (Premium LLM: Only For High-Value Jobs)
Run only when all conditions are true:
- Tier 1 decision is `proceed`
- score above configured threshold (example: >= 78)
- job priority is `high` (salary/company/role signal)

Premium call scope (single call):
- final resume bullet rewrites
- cover letter draft
- targeted ATS phrasing polish

Render locally after premium call:
- DOCX generation remains Python-only

Output:
- `generated/resume_intermediate.json`
- `generated/cover_letter_intermediate.json`
- rendered `.docx` files

Cost rule:
- Max 2 paid calls total only for top-tier jobs.

## Decision Matrix
- `duplicate` -> stop
- `local_reject` -> stop
- `local_uncertain` -> Tier 1 only
- `Tier1_skip` -> stop
- `Tier1_hold` -> queue for manual review
- `Tier1_proceed_low_priority` -> resume plan only, no Tier 2
- `Tier1_proceed_high_priority` -> Tier 2

## Script Refactor Plan
- Merge current scripts `01 + 03` into one Tier 1 unified call step.
- Gate current scripts `04 + 07` behind Tier 2 conditions.
- Keep `05 + 08 + 09` local/non-LLM.
- Keep duplicate/indexing logic in Tier 0 and improve exact-hash cache first.

## Metrics To Track Weekly
- paid calls per job
- % jobs rejected at Tier 0
- cache hit rate
- average cost per accepted application
- resume/cover quality pass rate (manual)

## v1 Defaults (Starting Values)
- duplicate threshold: `0.82`
- Tier 2 threshold: `78`
- max paid calls/job: `2`
- default path: Tier 0 -> Tier 1 -> stop
