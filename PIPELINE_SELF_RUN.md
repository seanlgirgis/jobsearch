# JobSearch Self-Run Pipeline (No Assistant Needed)

Use this checklist to run a full job application from `intake\intake.md` to final status update.

## 0) Open PowerShell in project root

```powershell
cd D:\Workarea\jobsearch
```

## 1) Duplicate check (required)

```powershell
.\job-check.ps1 .\intake\intake.md
```

Expected result:
- If duplicate: stop and do not apply.
- If clear: continue.

## 2) Score the job

```powershell
.\job-score.ps1
```

Notes:
- This creates a new job folder under `data\jobs\`.
- Intake file is kept in place (no move mode).

## 3) Decide accept/reject

Accept:
```powershell
.\job-accept.ps1
```

Reject:
```powershell
.\job-accept.ps1 -Reject
```

If rejected, pipeline ends.

## 4) Generate resume + cover (API flow)

```powershell
.\job-run.ps1
```

This runs:
- 03 tailor job data
- 04 generate resume intermediate
- 05 render resume
- 06 company research
- 07 generate cover intermediate
- 08 render cover

## 5) Quick quality check (recommended)

```powershell
$cache = Get-Content .job_cache.json | ConvertFrom-Json
python scripts\quality_check.py --uuid $cache.uuid_short --version v1 --strict
```

If strict check fails, fix artifacts first, then re-run step 4 or specific script(s).

## 6) Submit application externally

Submit these files from the job folder `generated` directory:
- `resume.docx` (or `resume_v1.docx`)
- `cover.docx`

## 7) Record application in system of record

```powershell
.\job-apply.ps1 -Method "Dice" -Notes "Applied via API pipeline"
```

This updates metadata and clears cache for next job.

---

## Fast Troubleshooting

### A) Duplicate check blocked
Run a different intake (new job) and retry from step 1.

### B) `FAILED at: 04 Generate resume`
Run only that step after environment is loaded:
```powershell
. .\env_setter.ps1
$cache = Get-Content .job_cache.json | ConvertFrom-Json
python scripts\04_generate_resume_intermediate.py --uuid $cache.uuid_short --version v1 --model grok-3
```
Then continue:
```powershell
python scripts\05_render_resume.py --uuid $cache.uuid_short --version v1 --all
python scripts\07_generate_cover_intermediate.py --uuid $cache.uuid_short --version v1 --model grok-3
python scripts\08_render_cover_letter.py --uuid $cache.uuid_short --version v1
```

### C) Need current job UUID quickly
```powershell
$cache = Get-Content .job_cache.json | ConvertFrom-Json
$cache.uuid
$cache.uuid_short
$cache.job_folder
```

### D) Start over for a fresh intake
Delete only cache:
```powershell
Remove-Item .job_cache.json -ErrorAction SilentlyContinue
```
Then restart at step 1.

---

## One-Line Standard Flow

```powershell
.\job-check.ps1 .\intake\intake.md; .\job-score.ps1; .\job-accept.ps1; .\job-run.ps1; .\job-apply.ps1 -Method "Dice" -Notes "Applied via API pipeline"
```

Use only after you trust the job and want a fast run.
