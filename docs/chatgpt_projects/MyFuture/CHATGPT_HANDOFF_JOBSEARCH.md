# JobSearch Handoff For ChatGPT

## Purpose
This repository is a local, script-driven job application pipeline. It takes one intake job posting, checks for duplicates, scores fit, creates tailored resume/cover artifacts, runs a quality gate, and tracks application status.

---

## Project Root
- `D:\StudyBook\temp\jobsearch`

## Requested Handoff Output Location
- `D:\Workarea\jobsearch\docs\CHATGPT_HANDOFF_JOBSEARCH.md`

---

## End-to-End Workflow (How JobSearch Works)

### Wrapper (easy mode) sequence
1. `job-check.ps1`
2. `job-score.ps1`
3. `job-accept.ps1` (or reject)
4. `job-run.ps1`
5. `job-apply.ps1`

These wrappers share state via `.job_cache.json` in the repo root.

### What each phase does under the hood

1. **Duplicate check**
   - Script: `scripts/00_check_applied_before.py`
   - Primary path: semantic similarity using FAISS + sentence-transformers.
   - Fallback path: lexical similarity against metadata cache.

2. **Score job + create structured job folder**
   - Script: `scripts/01_score_job.py`
   - Uses master profile + Grok API scoring prompt.
   - Creates: `data/jobs/NNNNN_<uuid8>/`
   - Writes:
     - `metadata.yaml`
     - `raw/raw_intake.md`
     - `score/score_report_*.md`

3. **Decision (accept/reject/hold)**
   - Script: `scripts/02_decide_job.py`
   - Updates `metadata.yaml` status and notes.

4. **Tailor job data**
   - Script: `scripts/03_tailor_job_data.py`
   - Produces structured extraction in:
     - `tailored/tailored_data_v1.yaml` (or versioned variant)

5. **Generate resume intermediate JSON**
   - Script: `scripts/04_generate_resume_intermediate.py`
   - Uses master data + tailored job data + LLM prompt.
   - Output:
     - `generated/resume_intermediate_v1.json`

6. **Render resume**
   - Script: `scripts/05_render_resume.py`
   - Outputs markdown preview + DOCX:
     - `generated/resume_preview_v1.md`
     - `generated/resume_preview_v1_trimmed.md`
     - `generated/resume_v1.docx`
     - `generated/resume.docx` (trimmed/all mode behavior)

7. **Company research**
   - Script: `scripts/06_company_research.py`
   - Output:
     - `research/company_research.yaml`

8. **Generate cover letter intermediate JSON**
   - Script: `scripts/07_generate_cover_intermediate.py`
   - Output:
     - `generated/cover_intermediate_v1.json`

9. **Render cover letter**
   - Script: `scripts/08_render_cover_letter.py`
   - Outputs:
     - `generated/cover_preview_v1.md`
     - `generated/cover.docx`

10. **Quality gate + tracking**
    - Quality script: `scripts/quality_check.py` (placeholder checks, section checks, word count)
    - Tracking script: `scripts/09_update_application_status.py`

11. **One-command orchestration option**
    - `scripts/10_auto_pipeline.py` runs 00→09 sequence (plus strict quality check before apply).

---

## Core Architecture Inputs

### Master profile data used for scoring/tailoring
- `data/master/master_career_data.yaml`
- `data/master/master_career_data.json`
- `data/master/skills.yaml`
- `data/source_of_truth.json`

### LLM client + profile loader
- `src/ai/grok_client.py`
- `src/loaders/master_profile.py`

### Duplicate detection index utilities
- `scripts/utils/vector_ops.py`
- `scripts/utils/build_job_index.py`
- `data/job_index/jobs_metadata.yaml`

---

## Files To Give ChatGPT First (Best Context Packet)

Provide these files first for accurate guidance:

1. `PIPELINE_RUNBOOK.md`
2. `docs/pipeline-guide.md`
3. `scripts/10_auto_pipeline.py`
4. `scripts/01_score_job.py`
5. `scripts/03_tailor_job_data.py`
6. `scripts/04_generate_resume_intermediate.py`
7. `scripts/07_generate_cover_intermediate.py`
8. `scripts/08_render_cover_letter.py`
9. `scripts/quality_check.py`
10. `src/loaders/master_profile.py`
11. `src/ai/grok_client.py`

---

## Files To Give ChatGPT For A Specific Job Issue

For one specific job folder `data/jobs/NNNNN_<uuid8>/`, share:

1. `metadata.yaml`
2. `raw/raw_intake.md`
3. `tailored/tailored_data_v1.yaml`
4. latest `score/score_report_*.md`
5. `generated/resume_intermediate_v1.json`
6. `generated/cover_intermediate_v1.json`
7. optionally: `generated/resume_preview_v1.md` and `generated/cover_preview_v1.md`

Example job folder shape:
- `data/jobs/00078_5ca49264/...`

---

## Operational Notes ChatGPT Should Know

1. Wrapper scripts rely on `.job_cache.json` and step order matters.
2. UUID resolution supports short prefix in many scripts.
3. Quality gate checks for placeholders (`Unknown`, `Your Name`, etc.) and missing sections/files.
4. Data quality varies in historical jobs (`Unknown` company/role in some metadata rows).
5. Script outputs can differ slightly by mode/version (e.g., resume filenames in render step).

---

## Security / Privacy

Do **not** share these unless intentionally redacting first:

1. `.env` (contains API keys)
2. Anything with sensitive personal data if not required for the debugging question

Safe practice: redact keys, phone, email, street address before sharing externally.

---

## Suggested Prompt To Use With ChatGPT

Use this exact prompt template when sharing files:

```text
I have a local job application automation repo. Please analyze the attached files as the source of truth and help me improve reliability and output quality.

Tasks:
1) Explain current pipeline behavior from intake to apply.
2) Identify mismatches between docs and actual script behavior.
3) Recommend fixes in priority order (high/medium/low) with exact file targets.
4) For my current failing job run, diagnose likely root causes from the job folder artifacts.
5) Suggest minimal code changes first, then optional refactors.

Constraints:
- Keep all current data formats unless change is necessary.
- Do not suggest destructive changes to historical job folders.
- Point out any filename/output inconsistencies across scripts.
```

---

## Current Date Context
- Handoff prepared on: 2026-04-27

