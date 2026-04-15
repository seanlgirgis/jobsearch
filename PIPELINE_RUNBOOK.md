# Job Application Pipeline — Full Runbook
# Last updated: 2026-04-14
# Intake file: D:\StudyBook\temp\jobsearch\intake\intake.md

---

## ONE-TIME SETUP (do this once per terminal session)

Open **PowerShell** and run these two commands:

```powershell
cd C:\jobsearch
. .\env_setter.ps1
```

Then set UTF-8 encoding (prevents emoji errors on Windows):

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$env:PYTHONPATH = "C:\jobsearch"
```

You are now ready to run the pipeline.

---

## OPTION A — Full Auto Pipeline (one command, runs everything)

This runs all 9 steps automatically, pauses for you to review the score,
then continues if you accept.

```powershell
python scripts\10_auto_pipeline.py `
  "D:\StudyBook\temp\jobsearch\intake\intake.md" `
  --model grok-3 `
  --method "LinkedIn" `
  --no-move
```

> **--no-move** keeps your intake file on D:\ (does not delete it)
> **--method** options: "LinkedIn" | "Indeed" | "Company Website" | "Referral"

When it finishes, your files are in:
```
C:\jobsearch\data\jobs\NNNNN_xxxxxxxx\
  generated\resume_v1.docx
  generated\cover_letter.docx
```

---

## OPTION B — Step by Step (full control)

Use this when you want to review each output before continuing.

---

### STEP 00 — Duplicate Check (free, no API call)
Checks if you already applied to this job before.

```powershell
python scripts\00_check_applied_before.py `
  "D:\StudyBook\temp\jobsearch\intake\intake.md"
```

✅ If it says **no duplicate** → continue to Step 01
⛔ If it says **duplicate found** → skip this job

---

### STEP 01 — Score Job (1 Grok API call)
Scores the job against your profile. Creates the job folder.

```powershell
python scripts\01_score_job.py `
  "D:\StudyBook\temp\jobsearch\intake\intake.md" `
  --model grok-3 `
  --temperature 0.3 `
  --no-move
```

📋 **READ THE OUTPUT CAREFULLY.**
It will print:
- Match Score (0-100%)
- Recommendation: Strong Proceed / Proceed / Hold / Skip
- Your UUID — **COPY IT** — you need it for all remaining steps

Example UUID: `10a9397a-828f-4e0e-8fef-5a9d00570620`

---

### STEP 02 — Accept or Reject

**To ACCEPT** (continue pipeline):
```powershell
python scripts\02_decide_job.py --uuid YOUR-UUID-HERE --accept
```

**To REJECT** (stop here):
```powershell
python scripts\02_decide_job.py --uuid YOUR-UUID-HERE --reject
```

**To HOLD** (decide later):
```powershell
python scripts\02_decide_job.py --uuid YOUR-UUID-HERE --hold
```

---

### STEP 03 — Extract & Structure Job Data (1 Grok API call)
Extracts skills, ATS keywords, responsibilities from the job posting.

```powershell
python scripts\03_tailor_job_data.py --uuid YOUR-UUID-HERE --model grok-3
```

Output: `data\jobs\NNNNN_xxxxxxxx\tailored\tailored_data_v1.yaml`

---

### STEP 04 — Generate Resume Intermediate (1 Grok API call)
Rewrites your resume bullets to match this specific job.

```powershell
python scripts\04_generate_resume_intermediate.py `
  --uuid YOUR-UUID-HERE `
  --model grok-3
```

Output: `data\jobs\NNNNN_xxxxxxxx\generated\resume_intermediate_v1.json`

When prompted "Overwrite? [y/N]" → type `y` and hit Enter

---

### STEP 05 — Render Resume to DOCX (no API call — free)
Converts the JSON into your final Word document.

```powershell
python scripts\05_render_resume.py --uuid YOUR-UUID-HERE --version v1 --all
```

Output:
- `data\jobs\NNNNN_xxxxxxxx\generated\resume_v1.docx`  ← FULL resume
- `data\jobs\NNNNN_xxxxxxxx\generated\resume.docx`     ← trimmed (top 5 roles)

---

### STEP 06 — Company Research (1–2 Grok API calls)
Classifies company as agency or enterprise. Fetches company info if enterprise.

```powershell
python scripts\06_company_research.py --uuid YOUR-UUID-HERE --model grok-3
```

Output: `data\jobs\NNNNN_xxxxxxxx\research\company_research.yaml`

---

### STEP 07 — Generate Cover Letter Intermediate (1 Grok API call)
Writes a tailored cover letter in JSON format.

```powershell
python scripts\07_generate_cover_intermediate.py `
  --uuid YOUR-UUID-HERE `
  --model grok-3
```

Output: `data\jobs\NNNNN_xxxxxxxx\generated\cover_intermediate_v1.json`

---

### STEP 08 — Render Cover Letter to DOCX (no API call — free)
Converts cover letter JSON to a formatted Word document.

```powershell
python scripts\08_render_cover_letter.py --uuid YOUR-UUID-HERE --version v1
```

Output: `data\jobs\NNNNN_xxxxxxxx\generated\cover_letter.docx`

---

### STEP 09 — Mark as Applied (no API call — free)
Updates the job status to APPLIED in your tracker.

```powershell
python scripts\09_update_application_status.py `
  --uuid YOUR-UUID-HERE `
  --method "LinkedIn" `
  --notes "Applied via pipeline"
```

---

## QUICK REFERENCE — Full Step-by-Step with UUID placeholder

Replace `YOUR-UUID` with the actual UUID from Step 01.

```powershell
# Setup (once per session)
cd C:\jobsearch
. .\env_setter.ps1
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$env:PYTHONPATH = "C:\jobsearch"

# Pipeline
python scripts\00_check_applied_before.py "D:\StudyBook\temp\jobsearch\intake\intake.md"
python scripts\01_score_job.py "D:\StudyBook\temp\jobsearch\intake\intake.md" --model grok-3 --temperature 0.3 --no-move
# --- COPY UUID FROM OUTPUT ---
python scripts\02_decide_job.py --uuid YOUR-UUID --accept
python scripts\03_tailor_job_data.py --uuid YOUR-UUID --model grok-3
python scripts\04_generate_resume_intermediate.py --uuid YOUR-UUID --model grok-3
python scripts\05_render_resume.py --uuid YOUR-UUID --version v1 --all
python scripts\06_company_research.py --uuid YOUR-UUID --model grok-3
python scripts\07_generate_cover_intermediate.py --uuid YOUR-UUID --model grok-3
python scripts\08_render_cover_letter.py --uuid YOUR-UUID --version v1
python scripts\09_update_application_status.py --uuid YOUR-UUID --method "LinkedIn"
```

---

## WHERE TO FIND YOUR OUTPUT FILES

After the pipeline runs, your files are at:

```
C:\jobsearch\data\jobs\NNNNN_xxxxxxxx\
  metadata.yaml                         ← job info, score, status
  raw\raw_intake.md                     ← original job posting
  score\score_report_*.md               ← Grok's scoring analysis
  tailored\tailored_data_v1.yaml        ← extracted job requirements
  research\company_research.yaml        ← company background
  generated\
    resume_intermediate_v1.json         ← resume data (editable)
    resume_v1.docx                      ← YOUR RESUME — submit this
    cover_intermediate_v1.json          ← cover letter data (editable)
    cover_letter.docx                   ← YOUR COVER LETTER — submit this
```

---

## GROK API COST SUMMARY

| Step | API Calls | Notes |
|------|-----------|-------|
| 00 | 0 | Free — local FAISS |
| 01 | 1 | Scoring |
| 02 | 0 | Free — local state |
| 03 | 1 | Job extraction |
| 04 | 1 | Resume generation |
| 05 | 0 | Free — local render |
| 06 | 1–2 | Classify + research |
| 07 | 1 | Cover letter |
| 08 | 0 | Free — local render |
| 09 | 0 | Free — local state |
| **Total** | **5–6 calls** | Per job application |

---

## TROUBLESHOOTING

**"No module named src"**
→ Make sure you set: `$env:PYTHONPATH = "C:\jobsearch"`

**"UnicodeEncodeError"**
→ Make sure you set: `$env:PYTHONIOENCODING = "utf-8"`

**"Job folder not found"**
→ Your UUID might be wrong. Check `C:\jobsearch\data\jobs\` for the folder name.
→ You can use just the first 8 characters of the UUID.

**"Overwrite? [y/N]"**
→ Type `y` and hit Enter to regenerate. Type `n` to keep existing file.

**Step 01 failed / no UUID printed**
→ Check your XAI_API_KEY is set. Run: `echo $env:XAI_API_KEY`
→ If blank, set it: `$env:XAI_API_KEY = "your-key-here"`
