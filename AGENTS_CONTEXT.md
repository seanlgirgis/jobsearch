# JobSearch Agent Context

Use this file when the user says the focus is `JobSearch`.

## Context Key

- Key: `JobSearch`
- Repository: `D:Workareajobsearch`
- Primary Goal: run and maintain the job application pipeline (score, decide, tailor, generate resume/cover, track application status).

## Startup Rules for JobSearch Work

1. Enter repo:
   - `cd D:Workareajobsearch`

2. Initialize Python environment:
   - `.env_setter.ps1 -NonInteractive`
   - If interactive session is required: `.env_setter.ps1`

3. Use relative paths only:
   - Correct: `data/jobs/...`, `scripts/...`
   - Avoid absolute paths unless user explicitly asks.

4. Encoding safety (Windows shell):
   - Before Python script runs in automation shells:
     - `$env:PYTHONIOENCODING='utf-8'`
   - This prevents Unicode print failures from script console output.

## Canonical Pipeline (POC v0)

1. Duplicate check:
   - `python scripts/00_check_applied_before.py <intake_file>`
   - This is a mandatory gate and must run first before scoring/tailoring.
   - Record outcome in job tracking artifacts (`metadata.yaml` notes/history and/or score report):
     - `duplicate_check: clear` when no likely duplicate
     - `duplicate_check: flagged` when likely duplicate
     - `duplicate_check: blocked` when the check cannot run (include exact blocker reason)
   - If flagged, stop and ask user whether to `skip`, `force apply`, or `hold`.

2. Score:
   - `python scripts/01_score_job.py <intake_file>`
   - Capture UUID from output.

3. Decide:
   - `python scripts/02_decide_job.py --uuid <uuid> --accept|--reject|--hold --reason "..."`

4. Tailor:
   - `python scripts/03_tailor_job_data.py --uuid <uuid>`

5. Resume intermediate:
   - `python scripts/04_generate_resume_intermediate.py --uuid <uuid> --version v1`

6. Resume render:
   - `python scripts/05_render_resume.py --uuid <uuid> --version v1 --all`

7. Company research:
   - `python scripts/06_company_research.py --uuid <uuid>`

8. Cover intermediate:
   - `python scripts/07_generate_cover_intermediate.py --uuid <uuid> --version v1`

9. Cover render:
   - `python scripts/08_render_cover_letter.py --uuid <uuid> --version v1`

10. Mark applied (after real submit):
   - `python scripts/09_update_application_status.py --uuid <uuid> apply --method "LinkedIn" --notes "..."`

## Folder and Artifact Expectations

- Per job folder: `data/jobs/<job_id_or_uuid_prefix>/`
- Expected subfolders: `raw/`, `score/`, `tailored/`, `generated/`
- Core files:
  - `metadata.yaml`
  - `score/score_report_*.md`
  - `tailored/tailored_data_v1.yaml`
  - `generated/resume_intermediate_v1.json`
  - `generated/cover_intermediate_v1.json`
  - `generated/resume_preview_v1.md`
  - `generated/resume_preview_v1_trimmed.md`
  - `generated/resume.docx` (trimmed default)
  - `generated/resume_v1.docx` (full)
  - `generated/cover_preview_v1.md`
  - `generated/cover.docx`

## Quality Checks Before Calling a Job “Done”

1. Encoding check:
   - Ensure no mojibake (`â€”`, `â€“`, etc.) in generated markdown/json.

2. Identifier consistency:
   - `metadata.yaml` job_id must match folder job id.
   - score report Job ID must match folder job id.

3. Application tracking consistency:
   - Keep top-level decision status (`ACCEPTED`, etc.).
   - Track real submission in `application` block:
     - `applied: true`
     - `applied_date: 'YYYY-MM-DD'`
     - `applied_method`
     - prepend an `Applied` history item.

4. Resume size sanity:
   - Prefer trimmed resume for typical applications.
   - Full resume is optional for roles explicitly asking for extended history.

## Known Practical Notes

- `python-docx` must exist in the environment for render scripts.
- If `docx2pdf` is missing, PDF generation is skipped; DOCX output still valid.
- Secrets warnings from `env_setter.ps1` can appear and are not always blockers for local rendering tasks.

## Mandatory User-Facing Response Contract (Job Intake)

When the user provides a job posting (full text, partial text, or screenshot transcription), respond immediately with this format before any optional deep pipeline steps:

1. `Fit score` out of `100`.
2. `Match summary`:
   - top strengths
   - main gaps/risks
3. `Recommendation`:
   - `Apply` or `Skip` (or `Apply with caution` when mixed).
4. `Next action`:
   - one concrete step the user should take now.

Behavior rules:
- Do not stay silent or defer this summary when enough job detail is present.
- Keep it concise and decision-oriented.
- If critical job details are missing, still provide a provisional score/rationale and explicitly list what is missing.

## Autonomous Full-Cycle Rule (No Re-Ask)

Default operating behavior for JobSearch in this repo:

- When the user provides a job and asks to process it, run the full cycle end-to-end without asking for repeated confirmation between steps.
- Execute in one flow:
  1. Run duplicate check first and register the result in tracker artifacts.
  2. Evaluate and score.
  3. Provide Apply/Skip recommendation.
  4. If user intent is to proceed, create/update job folder and tracker artifacts.
  5. Generate tailored resume + cover artifacts.
  6. Return job directory path and key output files.
- When user states submission is complete (for example: "submitted"), immediately update application status to applied in tracking metadata without asking follow-up confirmation.

Exception handling:
- Ask only when there is high-risk ambiguity that could cause incorrect company/job mapping or destructive data changes.

## AI-Native Execution Rule (Preferred Default)

- Default to agent-driven execution using built-in AI reasoning and direct file updates.
- Do not depend on xAI/Grok-backed generation scripts for normal job processing.
- Use local scripts only as optional helpers for rendering or indexing when they do not require external model keys.
- If an external-model key is missing, continue without blocking:
  - generate score/match analysis directly,
  - create/update job artifacts directly,
  - generate resume/cover content directly.

## Reject/Skip Storage Rule

- If the user decision is `reject` or `skip` and there was no application submitted, do not create a job folder under `data/jobs/...`.
- Keep the decision in conversational output only (score, rationale, and recommendation).
- Create/update `data/jobs/...` artifacts only when:
  - the user has applied, or
  - the user explicitly asks to save/archive a non-applied rejected job.
