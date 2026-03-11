# Pipeline Runner — Step by Step
Use this document every time you process a new job.
Replace the intake filename with your actual file each time.

---

## Before You Start — Activate the Environment

```powershell
cd C:\jobsearch
.\env_setter.ps1
```

---

## Set Your Job File (do this once per session)

```powershell
$JOB = "intake\00024.monet.dataEngineer.031120261512.md"
```

Change the filename to whatever job you are running.

---

## Step 0 — Duplicate Check

```powershell
python scripts/00_check_applied_before.py $JOB
```

**What to look for:**
- `✅ No strong duplicates found` → continue
- `❌ Duplicate likely` → stop, you already applied to this role

---

## Step 1 — Score the Job

```powershell
python scripts/01_score_job.py $JOB
```

**What to look for:**
- `## Match Score: XX%`
- `## Recommendation: Strong Proceed / Proceed / Hold / Skip`
- At the bottom: `🆔 Job UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Copy the UUID now.** You need it for every step after this.

```powershell
$UUID = "paste-your-uuid-here"
```

Example:
```powershell
$UUID = "cdb9a3fa-4618-4d9e-a636-6709f514c968"
```

---

## Step 2 — Make Your Decision

Read the score report first:
```powershell
Get-ChildItem data\jobs\*$UUID.Substring(0,8)*\score\
```

**If you want to proceed:**
```powershell
python -m scripts.02_decide_job --uuid $UUID --accept --reason "your reason here"
```

**If you want to skip:**
```powershell
python -m scripts.02_decide_job --uuid $UUID --reject --reason "your reason here"
```

**If you want to decide later:**
```powershell
python -m scripts.02_decide_job --uuid $UUID --hold --reason "your reason here"
```

> Only continue to Step 3 if you accepted.

---

## Step 3 — Tailor the Job Data

```powershell
python scripts/03_tailor_job_data.py --uuid $UUID
```

**What to look for:**
- `Tailored data saved: ...tailored_data_v1.yaml`
- A list of extracted skills

---

## Step 4 — Generate Resume (Intermediate JSON)

```powershell
python scripts/04_generate_resume_intermediate.py --uuid $UUID --version v1
```

**What to look for:**
- `Success! Intermediate resume saved → ...resume_intermediate_v1.json`
- If it asks "Overwrite? [y/N]" → type `y` and Enter

---

## Step 5 — Render Resume (DOCX)

```powershell
python scripts/05_render_resume.py --uuid $UUID --version v1 --all
```

`--all` generates both full and trimmed versions.

**What to look for:**
- `DOCX → ...resume_v1.docx`
- `DOCX → ...resume_v1_trimmed.docx`

---

## Step 6 — Company Research

```powershell
python scripts/06_company_research.py --uuid $UUID
```

**What to look for:**
- `Type: enterprise` or `Type: agency`
- If enterprise: research is fetched and saved

---

## Step 7 — Generate Cover Letter (Intermediate JSON)

```powershell
python scripts/07_generate_cover_intermediate.py --uuid $UUID --version v1
```

**What to look for:**
- `Saved → ...cover_intermediate_v1.json`

---

## Step 8 — Render Cover Letter (DOCX)

```powershell
python scripts/08_render_cover_letter.py --uuid $UUID --version v1
```

**What to look for:**
- `DOCX saved → ...cover_letter_v1.docx`

---

## Step 9 — Record the Application

Run this after you actually submit the application:

```powershell
python scripts/09_update_application_status.py --uuid $UUID apply `
  --method "LinkedIn" `
  --notes "Applied via LinkedIn easy apply"
```

Change `--method` to: `"LinkedIn"` / `"Company Website"` / `"Email"` / `"Referral"`

---

## Where Are Your Files?

```powershell
$SHORT = $UUID.Substring(0,8)
Get-ChildItem data\jobs\*$SHORT*\generated\
```

Your files are in:
```
data\jobs\NNNNN_xxxxxxxx\
  generated\
    resume_v1.docx           ← full resume
    resume_v1_trimmed.docx   ← top 5 roles only
    cover_letter_v1.docx     ← cover letter
  score\
    score_report_*.md        ← Grok's full analysis
  tailored\
    tailored_data_v1.yaml    ← extracted requirements
```

---

## Later — Update Status After Applying

When something happens (interview, rejection, ghosted):

```powershell
python scripts/12_update_job.py "Monet" --status "INTERVIEW" --notes "Phone screen scheduled"
python scripts/12_update_job.py "Monet" --status "REJECTED" --notes "Email received"
python scripts/12_update_job.py "Monet" --status "GHOSTED" --notes "No response after 3 weeks"
```

No UUID needed — it finds the job by company name.

---

## Quick Search Across All Jobs

```powershell
python scripts/11_search_jobs.py "Databricks"
python scripts/11_search_jobs.py "REJECTED"
python scripts/11_search_jobs.py "Monet"
```

---

## Full Auto Mode (Skips the Human Gate)

Only use this if you already reviewed the job and want it processed automatically:

```powershell
python scripts/10_auto_pipeline.py $JOB --method "LinkedIn"
```

This runs Steps 0 through 9 in one pass and auto-accepts the job.

---

## Current Job

| File | `00024.monet.dataEngineer.031120261512.md` |
|------|-------------------------------------------|
| Company | Monet Bank |
| Role | Data Engineer |
| Location | Plano, TX |
| Status | Ready to run |
