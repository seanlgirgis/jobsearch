# Job Search Pipeline — Quick Reference Guide

## First: Always Activate the Environment

Open PowerShell in the project root, then:

```powershell
. .\env_setter.ps1
```

This activates the venv AND sets PYTHONPATH. All pipeline commands below assume this has been run.

---

## The Big Picture — Pipeline Flow

```
New Job Posting
      │
      ▼
[00] Duplicate Check     ← Did we already apply to this?
      │
      ▼
[01] Score Job           ← Grok scores 0–100 against your profile
      │
      ▼
[02] Decide              ← You: ACCEPT / REJECT / HOLD
      │
      ▼
[03] Tailor Job Data     ← Grok extracts keywords, maps your experience
      │
      ▼
[04] Generate Resume     ← Grok writes tailored resume content (intermediate)
      │
      ▼
[05] Render Resume       ← Produces final resume.docx
      │
      ▼
[06] Company Research    ← Grok researches company, saves YAML
      │
      ▼
[07] Generate Cover      ← Grok writes cover letter (intermediate)
      │
      ▼
[08] Render Cover        ← Produces final cover_letter.docx
      │
      ▼
[09] Track Application   ← Record that you applied, track status
```

Or run it all at once with **[10] Auto Pipeline**.

---

## Step-by-Step Commands

### PREP — Save the job posting as a markdown file

Create a file in `intake/` using this format at the top:

```
Employer_Name: Koch Industries
URL: https://linkedin.com/jobs/view/...
Title: Senior Data Engineer
Location: Plano, TX
Contents:
<paste full job description here>
```

Save as: `intake/NNNNN.CompanyName.MMDDYYYY.md`

---

### STEP 00 — Check for duplicates (optional but recommended)

```powershell
python scripts/00_check_applied_before.py intake/your-job.md
```

If similarity > 82% to a past job, it will warn you. Use your judgment.

---

### STEP 01 — Score the job

```powershell
python scripts/01_score_job.py intake/your-job.md
```

- Creates `data/jobs/NNNNN_xxxxxxxx/` folder
- Saves `metadata.yaml` with score (0–100), recommendation, UUID
- Moves the intake file into the job folder

**Score guide:** 85+ = Strong Proceed | 70–84 = Proceed | <70 = Think twice

---

### STEP 02 — Record your decision

```powershell
# Accept
python -m scripts.02_decide_job --uuid xxxxxxxx --accept --reason "Strong Plano match, SQL+Python heavy"

# Reject
python -m scripts.02_decide_job --uuid xxxxxxxx --reject --reason "Requires relocation"

# Hold
python -m scripts.02_decide_job --uuid xxxxxxxx --hold --reason "Waiting on referral"
```

Use the short UUID (first 8 chars from the folder name).

---

### STEP 03 — Tailor job data

```powershell
python scripts/03_tailor_job_data.py data/jobs/NNNNN_xxxxxxxx
```

Grok extracts required skills, maps to your experience, writes `tailored/tailored_data_llm-v1.yaml`.

---

### STEP 04 — Generate resume content

```powershell
python scripts/04_generate_resume_intermediate.py data/jobs/NNNNN_xxxxxxxx
```

Writes the intermediate resume YAML that feeds into the renderer.

---

### STEP 05 — Render the resume (.docx)

```powershell
python scripts/05_render_resume.py data/jobs/NNNNN_xxxxxxxx
```

Output: `data/jobs/NNNNN_xxxxxxxx/generated/resume.docx`

---

### STEP 06 — Company research

```powershell
python scripts/06_company_research.py --uuid xxxxxxxx
```

Saves `data/jobs/NNNNN_xxxxxxxx/research/company_research_v1.yaml`

---

### STEP 07 — Generate cover letter content

```powershell
python scripts/07_generate_cover_intermediate.py data/jobs/NNNNN_xxxxxxxx
```

---

### STEP 08 — Render cover letter (.docx)

```powershell
python scripts/08_render_cover_letter.py data/jobs/NNNNN_xxxxxxxx
```

Output: `data/jobs/NNNNN_xxxxxxxx/generated/cover_letter_v1.docx`

---

### STEP 09 — Track your application

```powershell
# Record that you applied
python scripts/09_update_application_status.py --uuid xxxxxxxx apply \
  --date 2026-03-30 --method "LinkedIn" --notes "Tailored resume attached"

# Update status later
python scripts/09_update_application_status.py --uuid xxxxxxxx status \
  --new-status "Interview Scheduled" --notes "Phone screen April 5"

# View current status
python scripts/09_update_application_status.py --uuid xxxxxxxx show
```

---

## Run the Full Pipeline at Once

```powershell
python scripts/10_auto_pipeline.py intake/your-job.md --method "LinkedIn"
```

Runs steps 01 through 09 in sequence. Use `10b_force_pipeline.py` to re-run a job that already exists.

---

## Utility Commands

### Search your job history

```powershell
# Find by company or keyword
python scripts/11_search_jobs.py "Koch"
python scripts/11_search_jobs.py "Snowflake"
```

### Update a job record (status, notes, follow-up)

```powershell
# By company name
python scripts/12_update_job.py "Koch" --status "INTERVIEW" --note "April 5 phone screen"

# Set a follow-up reminder
python scripts/12_update_job.py "Koch" --followup 2026-04-05

# View full history
python scripts/12_update_job.py --uuid xxxxxxxx --history
```

---

## Where Things Live

| What | Where |
|---|---|
| New job postings (staging) | `intake/` |
| All job folders | `data/jobs/NNNNN_xxxxxxxx/` |
| Score report | `data/jobs/.../score/score_report_*.md` |
| Tailored data | `data/jobs/.../tailored/tailored_data_llm-v1.yaml` |
| Final resume | `data/jobs/.../generated/resume.docx` |
| Final cover letter | `data/jobs/.../generated/cover_letter_v1.docx` |
| Company research | `data/jobs/.../research/company_research_v1.yaml` |
| Your master career data | `data/master/master_career_data.yaml` |
| Skills list | `data/master/skills.yaml` |
| Source of truth (full profile) | `data/source_of_truth.json` |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'src'` | Run `. .\env_setter.ps1` first |
| `XAI_API_KEY not found` | Create `.env` file with `XAI_API_KEY=your-key` |
| `UnicodeEncodeError` | Set `$env:PYTHONIOENCODING = "utf-8"` in PowerShell |
| Wrong Python (missing packages) | Use `/c/py_venv/JobSearch/Scripts/python` explicitly |
| Need to rerun a job | Use `10b_force_pipeline.py` instead of `10_auto_pipeline.py` |

---

*Last updated: 2026-03-30 | Project: c:\pyproj\jobsearch*
