# JobSearch System — Complete How-To Guide

*Sean Luka Girgis | Plano/Murphy, TX | seanlgirgis@gmail.com*
*Generated: 2026-04-27 | Project root: `D:\Workarea\jobsearch`*

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Environment Setup](#2-environment-setup)
3. [Data Architecture](#3-data-architecture)
4. [The 5-Step PS1 Workflow (Daily Use)](#4-the-5-step-ps1-workflow-daily-use)
5. [Python Scripts Reference (Under the Hood)](#5-python-scripts-reference-under-the-hood)
6. [Your Master Career Data](#6-your-master-career-data)
7. [Intake File Format](#7-intake-file-format)
8. [Tracking & Status Management](#8-tracking--status-management)
9. [Restarting After a Break](#9-restarting-after-a-break)
10. [Troubleshooting](#10-troubleshooting)
11. [Quick Reference Cheat Sheet](#11-quick-reference-cheat-sheet)

---

## 1. System Overview

This is an **AI-powered job application engine**. It handles the full lifecycle:

```
Job Posting → Duplicate Check → Score/Fit Analysis → Accept/Reject
→ Tailored Resume → Company Research → Cover Letter → Track Application
```

**Two AI systems work together:**
- **Local HuggingFace FAISS** (`all-MiniLM-L6-v2`) — duplicate detection, free, offline
- **xAI Grok API** (`grok-3` / `grok-3-mini`) — scoring, tailoring, resume generation, cover letters

**All data is file-system-based** — no database required. One folder per job under `data/jobs/`.

---

## 2. Environment Setup

### One-Time: Activate the Environment

Before running **any** script, activate the Python virtual environment:

```powershell
# Run from the project root
. .\env_setter.ps1
```

What `env_setter.ps1` does:
- Activates venv at `C:\py_venv\JobSearch`
- Sets `PROJECT_ROOT` to the repo directory (relative, auto-detected)
- Sets `PYTHONPATH` to include `src\`
- Sets data path env vars: `JOBS_DB_DIR`, `RESUMES_DIR`, `VECTOR_DB_PATH`
- Forces offline HuggingFace model use (no downloads)
- Forces UTF-8 encoding (emoji-safe)
- Sets `DEFAULT_LLM_PROVIDER=xai`, `DEFAULT_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2`

### API Key — Required for Grok

The XAI API key is **not** stored in the script. Set it before running:

```powershell
$env:XAI_API_KEY = "your-xai-key-here"
```

You can add this line temporarily after sourcing `env_setter.ps1`, or add it to `env_setter.ps1` locally (never commit it).

### Installed Packages

The venv is pre-loaded with everything from `requirements.txt`. Key packages:
- `python-docx` — DOCX rendering
- `faiss-cpu` — vector duplicate detection
- `sentence-transformers` — local embeddings (offline)
- `openai` — used as xAI/Grok SDK client
- `PyYAML`, `pandas`, `scikit-learn`, `torch`, `transformers`

### Verify Setup

```powershell
. .\env_setter.ps1
python scripts\test_imports.py
```

---

## 3. Data Architecture

```
jobsearch/
├── intake/                         ← DROP new job postings here as .md files
│   └── intake.md                   ← Overwrite or rename per job
│
├── data/
│   ├── source_of_truth.json        ← YOUR MASTER CAREER DATA — edit this to update your profile
│   ├── master/
│   │   ├── master_career_data.json ← Derived from source_of_truth (auto-exported)
│   │   ├── master_career_data.yaml ← YAML copy of career data
│   │   └── skills.yaml             ← Your skills inventory
│   │
│   ├── job_index/
│   │   ├── faiss_job_descriptions.index  ← FAISS binary index (duplicate detection)
│   │   └── jobs_metadata.yaml            ← UUID → job mapping for the index
│   │
│   ├── jobs/                       ← ONE FOLDER PER JOB
│   │   └── 00069_75e46c36/         ← Format: NNNNN_uuid8
│   │       ├── metadata.yaml       ← Status, score, company, history
│   │       ├── raw/                ← Original intake markdown
│   │       ├── score/              ← Grok fit score report
│   │       ├── tailored/           ← Structured YAML: ATS keywords, skills, requirements
│   │       ├── generated/          ← FINAL OUTPUT: resume.docx, cover.docx
│   │       └── research/           ← Company research (agency vs enterprise, culture)
│   │
│   ├── resumes/                    ← (Optional) standalone resume outputs
│   ├── gig_tracker.csv             ← Freelance/gig tracking
│   └── interview_prep/             ← Interview preparation materials
│
├── scripts/                        ← Python pipeline scripts (00–12)
├── pipeline/                       ← Newer refactored pipeline utilities
├── src/                            ← Internal libraries (grok_client, master_profile loader)
├── prompts/                        ← LLM prompt templates
├── docs/                           ← Documentation (you are here)
└── intake/                         ← Inbox for new job postings
```

**The cache file `.job_cache.json`** (project root) stores state between PS1 steps for the *current* job in progress. It is created by `job-check.ps1` and cleared by `job-apply.ps1` or `job-reject.ps1`.

---

## 4. The 5-Step PS1 Workflow (Daily Use)

> All PS1 scripts live in the project root and must be run from there.
> They auto-call `env_setter.ps1` — you do NOT need to source it separately.

### Step 1 — Check for Duplicates

```powershell
.\job-check.ps1 "intake\intake.md"
```

- Runs `scripts\00_check_applied_before.py`
- Embeds the job with HuggingFace and checks FAISS index (threshold: 0.82 similarity)
- If no duplicate: creates `.job_cache.json` and says "Run job-score.ps1 next"
- If duplicate: **stops** — you already applied to this role

**Default intake file:** `intake\intake.md` (can pass any path as arg)

---

### Step 2 — Score the Job

```powershell
.\job-score.ps1
# Or with custom model:
.\job-score.ps1 -Model grok-3 -Temperature 0.3
```

- Loads your master profile (`data/master/master_career_data.json`)
- Calls Grok to score fit: outputs `## Match Score: X%` and `## Recommendation`
- Creates job folder: `data/jobs/NNNNN_uuid8/`
- Copies intake to `raw/`, saves score report to `score/`
- Updates `.job_cache.json` with UUID

**Score calibration:**
- 85%+ = Strong Proceed (apply immediately)
- 75–84% = Proceed (good fit)
- 65–74% = Hold (borderline)
- <65% = Skip

**Review the score report:**
```
data\jobs\<NNNNN_uuid8>\score\score_report_*.md
```

---

### Step 3 — Accept or Reject

**Accept:**
```powershell
.\job-accept.ps1
# With reason:
.\job-accept.ps1 -Reason "Strong Python/AWS match, Plano location"
```

**Reject:**
```powershell
.\job-reject.ps1
# With reason:
.\job-reject.ps1 -Reason "Requires Scala, not a fit"
# Or shorthand via accept script:
.\job-accept.ps1 -Reject -Reason "Too junior"
```

- Accept: marks job `ACCEPTED` in metadata, updates `.job_cache.json`
- Reject: marks job `REJECTED`, clears `.job_cache.json` (done with this job)

---

### Step 4 — Generate Resume + Cover Letter

```powershell
.\job-run.ps1
# With options:
.\job-run.ps1 -Model grok-3 -Version v1
```

Runs these 6 Python scripts in sequence:

| Step | Script | What It Does |
|------|--------|-------------|
| 03 | `03_tailor_job_data.py` | Grok extracts ATS keywords, skills, requirements into YAML |
| 04 | `04_generate_resume_intermediate.py` | Grok rewrites resume bullets tailored to this job → JSON |
| 05 | `05_render_resume.py` | Renders JSON → `resume_v1.docx` + trimmed version (no AI) |
| 06 | `06_company_research.py` | Grok classifies company (agency vs enterprise), fetches culture |
| 07 | `07_generate_cover_intermediate.py` | Grok writes cover letter → JSON |
| 08 | `08_render_cover_letter.py` | Renders JSON → `cover.docx` (no AI) |

**Output files** (Explorer opens automatically):
```
data\jobs\<NNNNN_uuid8>\generated\
    resume_v1.docx          ← Full resume (all experience)
    resume.docx             ← Trimmed resume (top 5 roles only)
    cover.docx              ← Cover letter
    resume_intermediate_v1.json   ← Editable intermediate (tweak before re-render)
    cover_intermediate_v1.json    ← Editable intermediate
    resume_preview_v1.md          ← Markdown preview
    cover_preview_v1.md           ← Markdown preview
```

**Tip:** If you want to tweak the resume, edit the `*_intermediate_v1.json` file, then re-run steps 05/08 individually:
```powershell
. .\env_setter.ps1
python scripts\05_render_resume.py --uuid <uuid8> --version v1 --all
python scripts\08_render_cover_letter.py --uuid <uuid8> --version v1
```

---

### Step 5 — Record the Application

After submitting resume + cover letter on LinkedIn / company site:

```powershell
.\job-apply.ps1
# With options:
.\job-apply.ps1 -Method "LinkedIn" -Notes "Applied with v1 resume"
.\job-apply.ps1 -Method "Company Site" -Notes "Tailored for AWS Glue role"
```

- Calls `scripts\09_update_application_status.py` to log to `metadata.yaml`
- Records: date applied, method, notes
- **Clears `.job_cache.json`** — system is ready for the next job

---

## 5. Python Scripts Reference (Under the Hood)

All scripts use **relative paths** from the project root. Run from root dir only.

| Script | Purpose | Key Args |
|--------|---------|----------|
| `scripts/00_check_applied_before.py` | FAISS duplicate check | `<intake.md>` |
| `scripts/01_score_job.py` | Score fit via Grok | `<intake.md> --model grok-3 --temperature 0.5 --no-move` |
| `scripts/02_decide_job.py` | Accept/reject job | `--uuid <uuid8> --accept\|--reject --reason "..."` |
| `scripts/03_tailor_job_data.py` | Extract structured job data | `--uuid <uuid8> --version v1 --model grok-3-mini` |
| `scripts/04_generate_resume_intermediate.py` | Generate resume JSON | `--uuid <uuid8> --version v1 --model grok-3` |
| `scripts/05_render_resume.py` | Render DOCX from JSON | `--uuid <uuid8> --version v1 --all` |
| `scripts/06_company_research.py` | Company classification & research | `--uuid <uuid8>` |
| `scripts/07_generate_cover_intermediate.py` | Generate cover letter JSON | `--uuid <uuid8> --version v1 --model grok-3` |
| `scripts/08_render_cover_letter.py` | Render cover DOCX | `--uuid <uuid8> --version v1` |
| `scripts/09_update_application_status.py` | Log application status | `--uuid <uuid8> apply\|status\|show` |
| `scripts/10_auto_pipeline.py` | Full automated pipeline | `intake\intake.md --method "LinkedIn"` |
| `scripts/11_search_jobs.py` | Search past applications | `--query "Capital One"` |
| `scripts/12_update_job.py` | Bulk update job status | `--uuid <uuid8> --status "Interview"` |

### UUID Resolution

All scripts accept either:
- Full UUID: `cdb9a3fa-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Short 8-char prefix: `cdb9a3fa`
- The 5-digit folder name prefix: `00001`

Scripts auto-resolve: `data/jobs/*_cdb9a3fa*/`

### Run Full Auto-Pipeline (Skip Manual Gates)

```powershell
. .\env_setter.ps1
python scripts\10_auto_pipeline.py intake\intake.md --method "LinkedIn"
```

> Note: This skips the human score-review gate. Use for high-confidence roles only.

---

## 6. Your Master Career Data

**The single source of truth is: `data/source_of_truth.json`**

This JSON file drives everything: resume content, scoring context, skills lists.

### Key sections:

```json
{
  "personal_info": { "full_name": "Sean Luka Girgis", "email": "...", ... },
  "professional_summary": { "short": "...", "long": "..." },
  "education": [...],
  "experiences": [
    {
      "company": "CITI",
      "role": "Senior Capacity & Data Engineer",
      "start": "2017-11",
      "end": "2025-12",
      "highlights": ["..."],
      "exclude_from_resume": false    ← set true to hide from resume
    }
  ],
  "projects": [...],
  "certifications": [...],
  "skills": [...]
}
```

### Derived files (auto-sync from source_of_truth):
- `data/master/master_career_data.json` — used by scripts 04, 05
- `data/master/master_career_data.yaml` — YAML version
- `data/master/skills.yaml` — skills subset

**To update your profile:** Edit `data/source_of_truth.json`, then run:
```powershell
. .\env_setter.ps1
python scripts\profile_export.py
```

### To hide old roles from resume:
Set `"exclude_from_resume": true` on any experience entry in `source_of_truth.json`.

### Target Roles (from your current profile):
- Senior Data Engineer
- AI Engineer
- Cloud Data Architect
- Capacity Planning Engineer
- PySpark / AWS Specialist

---

## 7. Intake File Format

The intake file is a raw markdown job posting. Place it at `intake\intake.md`.

**Best format (add a metadata header at top):**
```markdown
Company_name: Capital One
Company_website: https://www.capitalone.com
Title: Senior Lead Data Engineer
Location: Plano, TX

[PASTE FULL JOB DESCRIPTION BELOW]

Senior Lead Data Engineer

Do you love building and pioneering in the technology space?...
```

The metadata header lets the system extract company name, website, and location automatically. Without it, the system falls back to filename parsing.

**Naming convention for multiple intakes (optional):**
```
intake\00001.CapitalOne.SeniorDataEngineer.04272026.md
```
Format: `NNNNN.Company.Role.MMDDYYYY.md` — company and role auto-extracted from filename.

---

## 8. Tracking & Status Management

### Check Status of a Job

```powershell
. .\env_setter.ps1
python scripts\09_update_application_status.py --uuid cdb9a3fa show
```

### Update Status After Application Events

```powershell
# Phone screen scheduled
python scripts\09_update_application_status.py --uuid cdb9a3fa status \
    --new-status "Phone Screen" --notes "Feb 12 with HR"

# Interview scheduled
python scripts\09_update_application_status.py --uuid cdb9a3fa status \
    --new-status "Interview Scheduled" --notes "Onsite Feb 20"

# Rejected
python scripts\09_update_application_status.py --uuid cdb9a3fa status \
    --new-status "Rejected" --notes "No feedback given"
```

### Search Past Applications

```powershell
python scripts\11_search_jobs.py --query "Capital One"
python scripts\11_search_jobs.py --query "data engineer"
```

### List All Applied Jobs (by scanning metadata)

```powershell
python scripts\11_search_jobs.py --status APPLIED
```

### The FAISS Index (Duplicate Detection)

- Lives at `data/job_index/faiss_job_descriptions.index`
- Updated automatically when you **accept** a job (script 02)
- Threshold: 0.82 cosine similarity = duplicate
- If index is stale or broken:
  ```powershell
  python pipeline\utils\rebuild_applied_jobs_index.py
  ```

---

## 9. Restarting After a Break

Since you've been away from job searching, here's exactly what to do:

### 1. Verify environment still works
```powershell
cd D:\Workarea\jobsearch
. .\env_setter.ps1
$env:XAI_API_KEY = "your-xai-key-here"
python scripts\test_imports.py
```

### 2. Review your master profile
Open `data/source_of_truth.json` — update if anything changed since last use:
- New skills learned?
- Updated preferred title?
- New certifications?

Then export:
```powershell
python scripts\profile_export.py
```

### 3. Check where you left off
```powershell
# See all job folders and their status
python scripts\11_search_jobs.py --status ALL
```

Or check if there's a stale cache:
```powershell
ls .job_cache.json
```
If `.job_cache.json` exists, you were mid-process on a job. Either complete it or delete the cache to start fresh.

### 4. Start a new application
Drop a new job posting into `intake\intake.md` and run:
```powershell
.\job-check.ps1
```

---

## 10. Troubleshooting

### "No cache found. Run job-check.ps1 first."
Delete any stale cache and start over:
```powershell
Remove-Item .job_cache.json -ErrorAction SilentlyContinue
.\job-check.ps1 "intake\intake.md"
```

### "Job folder not found for '<uuid>'"
The UUID is wrong or the folder was deleted. Find correct UUID:
```powershell
ls data\jobs | Where-Object { $_.Name -match "partial_uuid" }
```

### FAISS duplicate check fails / crashes
Rebuild the index:
```powershell
. .\env_setter.ps1
python pipeline\utils\rebuild_applied_jobs_index.py
```

### Grok API errors
- Check `$env:XAI_API_KEY` is set correctly
- Verify quota at xAI dashboard
- Fall back to `grok-3-mini` for cheaper calls: `.\job-score.ps1 -Model grok-3-mini`

### Resume JSON has bad content / placeholders
Edit the intermediate JSON directly, then re-render without calling Grok again:
```powershell
. .\env_setter.ps1
# Edit: data\jobs\NNNNN_uuid8\generated\resume_intermediate_v1.json
python scripts\05_render_resume.py --uuid <uuid8> --version v1 --all
```

### Cover letter has "Unknown" or "0" as company name
This means the intake file was missing the `Company_name:` header. Fix the JSON:
```
data\jobs\NNNNN_uuid8\generated\cover_intermediate_v1.json
```
Find and replace the placeholder, then re-render:
```powershell
python scripts\08_render_cover_letter.py --uuid <uuid8> --version v1
```

### HuggingFace model download attempts (offline error)
`env_setter.ps1` sets `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`. The model is cached at:
```
models\sentence-transformers\all-MiniLM-L6-v2\
```
If missing: temporarily remove offline flags, run once to download, re-add them.

### Python version / venv issues
```powershell
# Check which python is active
python --version
where python
# Should point to C:\py_venv\JobSearch\Scripts\python.exe
```

---

## 11. Quick Reference Cheat Sheet

### Daily Workflow (5 Commands)

```powershell
# 0. Set API key (do once per session)
$env:XAI_API_KEY = "your-key"

# 1. Drop job into intake\intake.md, then:
.\job-check.ps1

# 2. Score the job
.\job-score.ps1

# 3a. Accept
.\job-accept.ps1

# 3b. OR Reject
.\job-reject.ps1

# 4. Generate documents
.\job-run.ps1

# 5. After submitting on LinkedIn/company site
.\job-apply.ps1 -Method "LinkedIn"
```

### Model Choices

| Task | Default Model | Alternative |
|------|--------------|-------------|
| Scoring | `grok-3-mini` | `grok-3` (more thorough) |
| Tailoring | `grok-3-mini` | `grok-3` |
| Resume generation | `grok-3` | `grok-3-mini` (cheaper) |
| Cover letter | `grok-3` | `grok-3-mini` |

### Key File Locations

| Purpose | Path |
|---------|------|
| Your career data | `data/source_of_truth.json` |
| Skills list | `data/master/skills.yaml` |
| New job inbox | `intake/intake.md` |
| Job status files | `data/jobs/<id>/metadata.yaml` |
| Generated resume | `data/jobs/<id>/generated/resume_v1.docx` |
| Generated cover | `data/jobs/<id>/generated/cover.docx` |
| Score report | `data/jobs/<id>/score/score_report_*.md` |
| Duplicate index | `data/job_index/faiss_job_descriptions.index` |

### Job Count Stats
- Jobs processed: ~73 (folders in `data/jobs/`)
- Jobs applied: check `data/applied_jobs/` (~69 folders)

---

*This guide covers the v0 pipeline. See `user_guide/v0/` for individual script deep-dives.*
*For interview prep materials, see `data/interview_prep/`.*
*For audio interview prep pipeline, see `docs/INTERVIEW_AUDIO_HTML_PIPELINE_RECONSTRUCTED.md`.*
