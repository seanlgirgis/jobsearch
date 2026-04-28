# Manual V2 Pipeline (No Auto RAG/LLM Calls)

This flow keeps duplicate checks, rendering, and system-of-record updates.
It removes automatic LLM generation steps from scripts.

## Step 1 - Create Job Shell

```powershell
.\job-v2-shell.ps1 .\intake\intake.md
```

What it does:
- Optional duplicate check via `scripts/00_check_applied_before.py`
- Creates job folder scaffold:
  - `raw`
  - `score`
  - `tailored`
  - `generated`
  - `research`
- Writes `metadata.yaml`
- Creates `.job_cache_v2.json`

## Step 2 - Generate Artifacts in ChatGPT Project

Use modes:
- `B1` -> score report text
- `C1` -> `tailored_data_v1.yaml` + `resume_intermediate_v1.json`
- `D1` -> `cover_intermediate_v1.json`

Drop files into the new job folder:
- `score/score_report_manual_v1.md`
- `tailored/tailored_data_v1.yaml`
- `generated/resume_intermediate_v1.json`
- `generated/cover_intermediate_v1.json`

## Step 3 - Validate + Render + Quality Gate

```powershell
.\job-v2-render.ps1
```

What it does:
- Validates manual artifacts (`scripts_v2/01_validate_manual_artifacts.py`)
- Normalizes resume intermediate variants (`scripts/normalize_resume_intermediate.py`)
- Renders resume (`scripts/05_render_resume.py --all --normalize`)
- Renders cover (`scripts/08_render_cover_letter.py`)
- Runs strict quality gate (`scripts/quality_check.py --strict`)

## Step 4 - Record Application

```powershell
.\job-v2-apply.ps1 -Method "LinkedIn" -Notes "Applied with manual-v2 docs"
```

Optional status updates later:

```powershell
.\job-v2-status.ps1 -NewStatus "Interview Scheduled" -Notes "Phone screen booked"
```

## Notes

- This v2 flow does not call auto score/tailor/generate scripts.
- It is designed for ChatGPT Project artifact generation + deterministic rendering/tracking.
