# JobSearch Driver

Single-page operator guide to run your job search pipeline end-to-end from this folder.

Repo root:
- this folder (portable across `D:\Workarea\jobsearch` or `C:\workarea\jobsearch`)

---

## 1) Open Project

```powershell
cd <workarea>\jobsearch
```

Then activate:
```powershell
.\env_setter.ps1
```

---

## 2) Choose Your Flow

- API automation flow (normal): uses scripts to score/tailor/generate automatically.
- Manual artifact flow (v2): you paste AI outputs and pipeline renders.

If you are not sure, use API automation flow.

---

## 3) API Automation Flow (Default)

### Step A — Duplicate Gate

```powershell
.\job-check.ps1 .\intake\intake.md
```

If duplicate flagged: stop and use another job intake.

### Step B — Score

```powershell
.\job-score.ps1
```

### Step C — Accept or Reject

Accept:
```powershell
.\job-accept.ps1
```

Reject:
```powershell
.\job-accept.ps1 -Reject
```

### Step D — Generate Resume + Cover

```powershell
.\job-run.ps1
```

### Step E — Quality Check (recommended)

```powershell
$cache = Get-Content .job_cache.json | ConvertFrom-Json
python scripts\quality_check.py --uuid $cache.uuid_short --version v1 --strict
```

### Step F — Submit Externally

Send files from:
- `data\jobs\<job_id>\generated\resume.docx` (or `resume_v1.docx`)
- `data\jobs\<job_id>\generated\cover.docx`

### Step G — Mark Applied in System

```powershell
.\job-apply.ps1 -Method "Dice" -Notes "Applied via API pipeline"
```

---

## 4) Manual Artifact Flow (v2)

Use when you generate artifacts in ChatGPT/other model and only want local render + tracking.

### Step A — Create Shell

```powershell
.\job-v2-shell.ps1 .\intake\intake.md
```

If duplicate gate blocks but you still need shell:
```powershell
.\job-v2-shell.ps1 .\intake\intake.md -SkipDuplicateCheck
```

### Step B — Import Artifacts

From clipboard:
```powershell
.\job-v2-import.ps1 -FromClipboard -Force
```

From file:
```powershell
.\job-v2-import.ps1 -InputFile .\scratch\artifact_bundle.txt -Force
```

### Step C — Render + Validate

```powershell
.\job-v2-render.ps1
```

### Step D — Record Application

```powershell
.\job-v2-apply.ps1 -Method "Dice" -Notes "Applied with manual-v2 docs"
```

---

## 5) Variant Resume/Cover Targeting (Per Job)

When you want role-specific variants (APM, migration, agentic AI, etc.):

1. Edit:
- `data\jobs\<job_id>\generated\resume_intermediate_v1.json`
- `data\jobs\<job_id>\generated\cover_intermediate_v1.json`

2. Re-render resume:
```powershell
. .\env_setter.ps1
python scripts\05_render_resume.py --uuid <uuid_short> --version v1 --all
```

3. Re-render cover:
```powershell
python scripts\08_render_cover_letter.py --uuid <uuid_short> --version v1
```

4. Copy to variant names:
```powershell
Copy-Item data\jobs\<job_id>\generated\resume.docx data\jobs\<job_id>\generated\resume_<variant>.docx -Force
Copy-Item data\jobs\<job_id>\generated\resume_preview_v1.md data\jobs\<job_id>\generated\resume_<variant>.md -Force
Copy-Item data\jobs\<job_id>\generated\cover.docx data\jobs\<job_id>\generated\cover_<variant>.docx -Force
Copy-Item data\jobs\<job_id>\generated\cover_preview_v1.md data\jobs\<job_id>\generated\cover_<variant>.md -Force
```

---

## 6) Quick Utilities

### Show current cache context

```powershell
$cache = Get-Content .job_cache.json | ConvertFrom-Json
$cache
```

v2 cache:
```powershell
$cache = Get-Content .job_cache_v2.json | ConvertFrom-Json
$cache
```

### Bulk mark jobs applied via Dice (example 00081–00090)

```powershell
. .\env_setter.ps1
$jobs = Get-ChildItem data\jobs -Directory | Where-Object { $_.Name -match '^000(8[1-9]|90)_' } | Sort-Object Name
$today='2026-04-30'
foreach ($j in $jobs) {
  $u=($j.Name -split '_')[1]
  python scripts\09_update_application_status.py --uuid $u apply --date $today --method "Dice" --notes "Applied via Dice bulk update"
}
```

### Set interview status on a job

```powershell
python scripts\09_update_application_status.py --uuid <uuid_short> status --new-status "INTERVIEW SCHEDULED" --notes "HM interview on 2026-04-30 11:00 AM CT via Teams"
```

---

## 7) Error Recovery

### Error: `FAILED at: 04 Generate resume`

```powershell
. .\env_setter.ps1
$cache = Get-Content .job_cache.json | ConvertFrom-Json
python scripts\04_generate_resume_intermediate.py --uuid $cache.uuid_short --version v1 --model grok-3
python scripts\05_render_resume.py --uuid $cache.uuid_short --version v1 --all
python scripts\07_generate_cover_intermediate.py --uuid $cache.uuid_short --version v1 --model grok-3
python scripts\08_render_cover_letter.py --uuid $cache.uuid_short --version v1
```

### If cache is stale

```powershell
Remove-Item .job_cache.json -ErrorAction SilentlyContinue
Remove-Item .job_cache_v2.json -ErrorAction SilentlyContinue
```

Then restart from Step A.

---

## 8) Daily Fast Run (API)

```powershell
.\job-check.ps1 .\intake\intake.md
.\job-score.ps1
.\job-accept.ps1
.\job-run.ps1
.\job-apply.ps1 -Method "Dice" -Notes "Applied via API pipeline"
```

Use only after confirming the role is worth applying.

---

## 9) ChatGPT MyFuture Sources (Required Context)

When using ChatGPT Project `MyFuture`, keep these synced in repo:
- `docs\chatgpt_projects\MyFuture\source_of_truth.json`
- `docs\chatgpt_projects\MyFuture\AboutMe.txt`
- `docs\chatgpt_projects\MyFuture\SomeIdeas.txt`
- `docs\chatgpt_projects\MyFuture\pipeline-guide.md`
- `docs\chatgpt_projects\MyFuture\PIPELINE_RUNBOOK.md`
- `docs\chatgpt_projects\MyFuture\CHATGPT_HANDOFF_JOBSEARCH.md`
- `docs\chatgpt_projects\MyFuture\jobsearch-project-analysis.md`

Registry:
- `docs\chatgpt_projects\MyFuture\MYFUTURE_SOURCE_REGISTRY.md`

Refresh rule:
1. Replace any updated source file in `docs\chatgpt_projects\MyFuture\`
2. Update `MYFUTURE_SOURCE_REGISTRY.md` timestamp + notes
3. If `source_of_truth.json` changes, run next job from Step A (duplicate gate) so all artifacts use current truth
