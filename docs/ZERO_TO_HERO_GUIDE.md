# JobSearch Project — Zero to Hero Guide

> **Complete reference:** architecture, data, scripts, schemas, and pipeline flow.  
> Everything about how this system works, in one place.

---

## Table of Contents

1. [What This Project Is](#1-what-this-project-is)
2. [Directory Structure](#2-directory-structure)
3. [Setup & Environment](#3-setup--environment)
4. [Master Profile — Source of Truth](#4-master-profile--source-of-truth)
5. [Pipeline Overview — How One Job Goes End-to-End](#5-pipeline-overview--how-one-job-goes-end-to-end)
6. [Every Script — What It Does, What It Reads, What It Creates](#6-every-script--what-it-does-what-it-reads-what-it-creates)
   - [00 — Duplicate Check (FAISS)](#00--duplicate-check-faiss)
   - [01 — Score Job](#01--score-job)
   - [02 — Decide Job](#02--decide-job)
   - [03 — Tailor Job Data](#03--tailor-job-data)
   - [04 — Generate Resume Intermediate](#04--generate-resume-intermediate)
   - [05 — Render Resume](#05--render-resume)
   - [06 — Company Research](#06--company-research)
   - [07 — Generate Cover Intermediate](#07--generate-cover-intermediate)
   - [08 — Render Cover Letter](#08--render-cover-letter)
   - [09 — Update Application Status](#09--update-application-status)
   - [10 — Auto Pipeline (Orchestrator)](#10--auto-pipeline-orchestrator)
   - [10b — Force Pipeline](#10b--force-pipeline)
   - [11 — Search Jobs](#11--search-jobs)
   - [12 — Update Job](#12--update-job)
7. [Utility Scripts](#7-utility-scripts)
   - [vector_ops.py](#vector_opspy)
   - [build_job_index.py](#build_job_indexpy)
8. [Source Modules (src/)](#8-source-modules-src)
   - [GrokClient](#grokcllient)
   - [MasterProfileLoader](#masterprofileloader)
9. [Data Structures & File Schemas](#9-data-structures--file-schemas)
   - [Intake Markdown](#intake-markdown)
   - [Job Folder Layout](#job-folder-layout)
   - [metadata.yaml](#metadatayaml)
   - [score_report.md](#score_reportmd)
   - [tailored_data.yaml](#tailored_datayaml)
   - [resume_intermediate.json](#resume_intermediatejson)
   - [cover_intermediate.json](#cover_intermediatejson)
   - [company_research.yaml](#company_researchyaml)
   - [master_career_data.yaml](#master_career_datayaml)
   - [skills.yaml](#skillsyaml)
   - [FAISS Index & Metadata](#faiss-index--metadata)
10. [Configuration Files](#10-configuration-files)
11. [Full Data Flow Diagram](#11-full-data-flow-diagram)
12. [Day-to-Day Usage Cheatsheet](#12-day-to-day-usage-cheatsheet)
13. [Archived & Legacy Scripts](#13-archived--legacy-scripts)
14. [Documentation Files Reference](#14-documentation-files-reference)

---

## 1. What This Project Is

This is a **fully automated, AI-powered job application system**. You drop a job posting Markdown file into `intake/`, run one command, and out comes:

- A **tailored resume** (`.docx` + Markdown preview)  
- A **tailored cover letter** (`.docx` + Markdown preview)  
- A **score report** — how well you match, what the gaps are  
- **Structured job data** — extracted requirements, ATS keywords, must-haves  
- **Company research** — culture/values for enterprise employers  
- **Full tracking** — applied date, method, follow-up history  

**Stack:**
- **LLM:** xAI Grok API (OpenAI-compatible SDK)
- **Embeddings + Vector search:** `sentence-transformers/all-MiniLM-L6-v2` + FAISS (local, no GPU needed)
- **Document rendering:** `python-docx`
- **Data format:** YAML + JSON + Markdown flat files (no database)

**50 jobs have been processed.** Every one has its own folder under `data/jobs/` with the full artifact set.

---

## 2. Directory Structure

```
c:\jobsearch\
│
├── .env                          # API keys + model config (never committed)
├── env_setter.ps1                # PowerShell: activate venv + set env vars
├── requirements.txt              # All Python dependencies (160+ packages)
├── CodingStyle.md                # Coding standards enforced in this project
│
├── intake/                       # DROP NEW JOB FILES HERE
│   └── NNNNN.CompanyName.MMDDYYYY.HHMM.md
│
├── data/
│   ├── master/                   # YOUR PROFILE — the source of truth
│   │   ├── master_career_data.yaml    # Personal, summary, experience, projects
│   │   ├── master_career_data.json    # JSON export of the above (auto-generated)
│   │   └── skills.yaml                # All skills with years/proficiency metadata
│   │
│   ├── jobs/                     # One folder per job processed
│   │   └── NNNNN_xxxxxxxx/       # e.g. 00001_cdb9a3fa
│   │       ├── NNNNN.Company.Date.md      # Original intake file (moved here)
│   │       ├── metadata.yaml              # Tracking: status, score, history
│   │       ├── raw/
│   │       │   └── raw_intake.md          # Verbatim copy of intake
│   │       ├── score/
│   │       │   └── score_report_TIMESTAMP.md
│   │       ├── tailored/
│   │       │   └── tailored_data_llm-v1.yaml
│   │       ├── research/
│   │       │   └── company_research_v1.yaml
│   │       └── generated/
│   │           ├── resume_intermediate_llm-tailored-v1.json
│   │           ├── resume_llm-tailored-v1.docx          ← SUBMIT
│   │           ├── resume_llm-tailored-v1_trimmed.docx  ← shorter version
│   │           ├── resume_preview_llm-tailored-v1.md
│   │           ├── cover_intermediate_v1.json
│   │           ├── cover_letter_v1.docx                 ← SUBMIT
│   │           └── cover_preview_v1.md
│   │
│   ├── job_index/                # FAISS duplicate-detection index
│   │   ├── faiss_job_descriptions.index
│   │   └── jobs_metadata.yaml
│   │
│   ├── resumes/                  # (Reserved — currently unused)
│   └── vectorstore/              # (Reserved — currently unused)
│
├── scripts/                      # Main pipeline scripts (00-12)
│   ├── 00_check_applied_before.py
│   ├── 01_score_job.py
│   ├── 02_decide_job.py
│   ├── 03_tailor_job_data.py
│   ├── 04_generate_resume_intermediate.py
│   ├── 05_render_resume.py
│   ├── 06_company_research.py
│   ├── 07_generate_cover_intermediate.py
│   ├── 08_render_cover_letter.py
│   ├── 09_update_application_status.py
│   ├── 10_auto_pipeline.py       # ← Use this for full automation
│   ├── 10b_force_pipeline.py     # ← Skip duplicate check
│   ├── 11_search_jobs.py
│   ├── 12_update_job.py
│   ├── utils/
│   │   ├── vector_ops.py         # Embedding + FAISS helpers
│   │   └── build_job_index.py    # Rebuild FAISS index
│   ├── keep/                     # Backup copies of specific scripts
│   └── Archived/                 # Deprecated pre-refactor versions
│
├── src/                          # Python modules (importable)
│   ├── ai/
│   │   └── grok_client.py        # GrokClient wrapper
│   └── loaders/
│       └── master_profile.py     # MasterProfileLoader
│
├── docs/                         # Documentation
├── .claude/                      # Claude Code harness config
├── .vscode/                      # VS Code settings
├── notebooks/                    # Jupyter notebooks
├── tests/                        # Test suite
└── startingDocs/                 # Historical/reference docs
```

---

## 3. Setup & Environment

### Virtual Environment
The project uses `C:\py_venv\JobSearch` — expected on every machine at that path.

**Activate (PowerShell):**
```powershell
.\env_setter.ps1
```

This script:
1. Activates `C:\py_venv\JobSearch`
2. Sets `PROJECT_ROOT` dynamically from the script's own path
3. Sets `PYTHONPATH` to `$PROJECT_ROOT\src`
4. Sets `JOBS_DB_DIR`, `RESUMES_DIR`, `VECTOR_DB_PATH` relative to root

**Or activate manually:**
```powershell
C:\py_venv\JobSearch\Scripts\Activate.ps1
```

### Python Path
Always run scripts from the **project root** so `from src.ai.grok_client import ...` resolves:
```bash
cd c:\jobsearch
python scripts/01_score_job.py intake/myjob.md
```

### VS Code
`.vscode/settings.json` configures:
- Interpreter: `C:\py_venv\JobSearch\Scripts\python.exe`
- `python.analysis.extraPaths`: `["${workspaceFolder}/src"]`
- Terminal env: `PYTHONPATH`, `PROJECT_ROOT`, etc. all via `${workspaceFolder}`

### Environment Variables (`.env`)
```
DEFAULT_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
DEFAULT_LLM_PROVIDER=xai
XAI_API_KEY=xai-...
```

Only the API key and model config live here. All path vars are computed by `env_setter.ps1` or VS Code at runtime — not hardcoded in `.env`.

### Install Dependencies
```bash
pip install -r requirements.txt
```

Key packages:
| Package | Purpose |
|---|---|
| `openai` | SDK used to talk to Grok (xAI-compatible) |
| `sentence-transformers` | Local embeddings for duplicate detection |
| `faiss-cpu` | Vector index for semantic search |
| `torch`, `transformers` | Embedding model backend |
| `python-docx` | Render DOCX resumes and cover letters |
| `pyyaml` | Read/write all YAML data files |
| `python-dotenv` | Load `.env` |
| `rich` | Pretty console output |
| `pandas`, `numpy` | Data utilities |
| `pytest`, `black`, `ruff` | Dev/testing |

---

## 4. Master Profile — Source of Truth

The master profile is **never modified by any script** — it is only ever read. It is the canonical set of facts that Grok draws from when tailoring resumes and cover letters. The LLM is instructed never to invent — only to select and reorder from what exists here.

### `data/master/master_career_data.yaml`

```yaml
personal:
  name: string
  title: string
  location: string
  email: string
  phone: string
  linkedin: URL
  github: URL

summary:
  short: string    # ~120 chars — for tight resume headers
  long: string     # 500-1000 chars — for cover letter context

experience:
  - company: string
    role: string
    location: string
    start: "YYYY-MM"
    end: "YYYY-MM"   # or "Present"
    highlights:
      - "Achievement-focused bullet (quantified where possible)"
      - ...

flagship_projects:
  - name: string
    description: string
    technologies: [list]
    timeframe: string
    repo: URL  # optional
```

The `experience` section is ordered most-recent-first. When `05_render_resume.py` creates the trimmed version it takes the first 5 entries.

If any role should never appear on a resume (e.g. a very old or irrelevant position), set `exclude_from_resume: true` on that experience entry — script 04 will skip it.

### `data/master/master_career_data.json`

Auto-generated from the YAML via `scripts/profile_export.py`. Script 04 loads this file because JSON parsing is safer for LLM-generated output round-trips.

```bash
python scripts/profile_export.py   # regenerate after editing the YAML
```

### `data/master/skills.yaml`

```yaml
- name: "SQL / Oracle"
  years: 18
  proficiency: "Expert"     # Expert | Advanced | Intermediate-Advanced | Intermediate
  last_used: "2025"
  categories:
    - "Databases"
  notes: "Schema design, partitioning, PL/SQL, Pro*C, querying"

- name: "Python"
  years: 15
  proficiency: "Expert"
  last_used: "2025"
  categories:
    - "Data Engineering"
  notes: "Pandas, generators, ETL pipelines, scripting, multiprocessing"
```

`MasterProfileLoader.get_top_skills(n=15, min_years=2.0)` returns the top-N skills sorted by years × proficiency weight. This is what gets embedded in the LLM prompt as "your skill set."

---

## 5. Pipeline Overview — How One Job Goes End-to-End

### Input Format
Drop a file into `intake/` named:
```
NNNNN.CompanyName.MMDDYYYY.HHMM.md
```
Example: `00051.Stripe.04032026.0900.md`

The file can optionally start with front-matter key-value pairs:
```
Company_website: https://stripe.com
Location: Remote - US
Employment_type: Full-time

[Paste job description below this line]
```

### One-Command Automation
```bash
python scripts/10_auto_pipeline.py intake/00051.Stripe.04032026.0900.md --method "Company Website"
```

That single command runs all 10 steps (00 through 09) and produces the complete artifact set.

### Manual Step-by-Step
If you want control at each step:
```bash
python scripts/00_check_applied_before.py intake/myjob.md
python scripts/01_score_job.py intake/myjob.md
python scripts/02_decide_job.py --uuid <uuid> --accept --reason "Good fit"
python scripts/03_tailor_job_data.py --uuid <uuid>
python scripts/04_generate_resume_intermediate.py --uuid <uuid>
python scripts/05_render_resume.py --uuid <uuid>
python scripts/06_company_research.py --uuid <uuid>
python scripts/07_generate_cover_intermediate.py --uuid <uuid>
python scripts/08_render_cover_letter.py --uuid <uuid>
python scripts/09_update_application_status.py --uuid <uuid> apply --date 2026-04-03 --method "LinkedIn"
```

The `--uuid` flag accepts the full UUID or just the 8-character prefix (e.g., `cdb9a3fa`).

---

## 6. Every Script — What It Does, What It Reads, What It Creates

---

### 00 — Duplicate Check (FAISS)

**File:** `scripts/00_check_applied_before.py`  
**Purpose:** Prevent wasting time on jobs already applied to (or near-duplicates from the same posting re-listed on multiple boards).

**How it works:**
1. Reads the intake `.md` file
2. Embeds the job description text using `sentence-transformers/all-MiniLM-L6-v2` (local model, no API call)
3. Queries the FAISS index with cosine similarity
4. Prints a ranked table of the top-K similar past jobs
5. If any match exceeds the threshold (default 0.82), exits with code `1` — the pipeline stops

**Reads:**
- `intake/job.md` (command arg)
- `data/job_index/faiss_job_descriptions.index`
- `data/job_index/jobs_metadata.yaml`

**Creates/Modifies:** Nothing — read-only.

**Usage:**
```bash
python scripts/00_check_applied_before.py intake/myjob.md
python scripts/00_check_applied_before.py intake/myjob.md --threshold 0.90 --top-k 10
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `--threshold` | `0.82` | Cosine similarity above which = duplicate |
| `--top-k` | `5` | How many similar past jobs to display |

**Output (console):**
```
Similarity  Job ID          Company         Role                    Applied
0.91        00003_e4648120  PostScript      Senior Data Engineer    2026-02-05
0.78        00011_a2b3c4d5  Stripe          Data Platform Lead      2026-02-12
```

---

### 01 — Score Job

**File:** `scripts/01_score_job.py`  
**Purpose:** First contact with the LLM. Scores how well you match the job (0–100%) and creates the job folder.

**How it works:**
1. Parses the intake filename: `NNNNN.Company.MMDDYYYY.HHMM.md` → extracts sequence number, company, date
2. Reads optional front-matter from the top of the file (Company_website, Location, etc.)
3. Generates a UUID for this job
4. Creates `data/jobs/NNNNN_uuid8chars/` folder structure
5. Copies intake to `raw/raw_intake.md`
6. Calls Grok with: master profile + job description → score report
7. Writes `score/score_report_TIMESTAMP.md` and `metadata.yaml`
8. Moves intake file out of `intake/` (unless `--no-move`)
9. Prints `🆔 Job UUID: <full-uuid>` — orchestrator (script 10) captures this

**Reads:**
- `intake/job.md` (command arg)
- `data/master/master_career_data.yaml`
- `data/master/skills.yaml`
- `.env` (XAI_API_KEY)

**Creates:**
```
data/jobs/NNNNN_uuid8/
    metadata.yaml
    raw/
        raw_intake.md
    score/
        score_report_YYYYMMDD_HHMMSS.md
```

**Usage:**
```bash
python scripts/01_score_job.py intake/myjob.md
python scripts/01_score_job.py intake/myjob.md --model grok-3 --temperature 0.5 --no-move
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `--model` | `grok-3` | Grok model to use |
| `--temperature` | `0.5` | LLM temperature |
| `--no-move` | off | Keep intake file in place after processing |

---

### 02 — Decide Job

**File:** `scripts/02_decide_job.py`  
**Purpose:** Record your decision: proceed, reject, or hold. This is the human gate in the pipeline.

**How it works:**
1. Finds job folder by UUID (full or 8-char prefix)
2. Loads `metadata.yaml`
3. Sets `status` → `ACCEPTED` / `REJECTED` / `HELD`
4. Appends decision + reason + timestamp to metadata
5. If `ACCEPTED`: calls `scripts/utils/build_job_index.py` to add this job to the FAISS index

**Reads:**
- `data/jobs/NNNNN_uuid/metadata.yaml`

**Modifies:**
- `data/jobs/NNNNN_uuid/metadata.yaml` (updates status, last_decision, notes)
- `data/job_index/` (triggers rebuild if accepted)

**Usage:**
```bash
python scripts/02_decide_job.py --uuid cdb9a3fa --accept
python scripts/02_decide_job.py --uuid cdb9a3fa --reject --reason "Too junior"
python scripts/02_decide_job.py --uuid cdb9a3fa --hold --reason "Revisit in 2 weeks"
python scripts/02_decide_job.py --uuid cdb9a3fa --accept --dry-run
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `--uuid` | required | Full UUID or 8-char prefix |
| `--accept` / `--reject` / `--hold` | — | Exactly one required |
| `--reason` | — | Note saved to metadata |
| `--dry-run` | off | Preview without writing |

---

### 03 — Tailor Job Data

**File:** `scripts/03_tailor_job_data.py`  
**Purpose:** Extract structured data from the raw job posting. This is the foundation all later scripts rely on.

**How it works:**
1. Loads `raw/raw_intake.md`
2. Calls Grok with an extraction prompt: parse requirements, responsibilities, benefits, must-haves, ATS keywords
3. Parses the YAML-formatted response (with regex fallback if parsing fails)
4. Merges `company_name` and `company_website` from `metadata.yaml` if available
5. Saves to `tailored/tailored_data_v1.yaml`

**Reads:**
- `data/jobs/NNNNN_uuid/raw/raw_intake.md`
- `data/jobs/NNNNN_uuid/metadata.yaml` (for company name/website)

**Creates:**
```
data/jobs/NNNNN_uuid/tailored/
    tailored_data_llm-v1.yaml
```

**Usage:**
```bash
python scripts/03_tailor_job_data.py --uuid cdb9a3fa
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --version v2 --model grok-3 --temperature 0.0
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --no-llm   # regex only
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `--uuid` | required | — |
| `--version` | `v1` | Output file version suffix |
| `--temperature` | `0.0` | Use 0.0 for extraction (deterministic) |
| `--no-llm` | off | Use regex fallback instead of LLM |

---

### 04 — Generate Resume Intermediate

**File:** `scripts/04_generate_resume_intermediate.py`  
**Purpose:** Use Grok to select and rewrite resume content, tailored to this specific job — using ONLY facts from the master profile (no invention).

**How it works:**
1. Loads `master_career_data.json` and `skills.yaml`
2. Filters out experiences with `exclude_from_resume: true`
3. Loads `tailored_data_v1.yaml`
4. Sends LLM prompt: "Given this master profile and this job, produce a JSON resume. Select the most relevant experience bullets. Do not invent anything."
5. Parses and validates the JSON output
6. Saves to `generated/resume_intermediate_llm-tailored-v1.json`

**Reads:**
- `data/master/master_career_data.json`
- `data/master/skills.yaml`
- `data/jobs/NNNNN_uuid/tailored/tailored_data_*.yaml`

**Creates:**
```
data/jobs/NNNNN_uuid/generated/
    resume_intermediate_llm-tailored-v1.json
```

**Usage:**
```bash
python scripts/04_generate_resume_intermediate.py --uuid cdb9a3fa
python scripts/04_generate_resume_intermediate.py --uuid cdb9a3fa --overwrite
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `--uuid` | required | — |
| `--version` | `v1` | Version suffix |
| `--overwrite` | off | Force regeneration if file exists |

---

### 05 — Render Resume

**File:** `scripts/05_render_resume.py`  
**Purpose:** Turn the JSON intermediate into a submission-ready Word document.

**How it works:**
1. Loads `resume_intermediate_*.json`
2. Builds a `python-docx` Document with: header, contact, summary, projects, experience, skills, education
3. Renders full version (all experience entries)
4. Renders trimmed version (top 5 entries — fits 1-2 pages)
5. Renders a Markdown preview for quick review without opening Word

**Reads:**
- `data/jobs/NNNNN_uuid/generated/resume_intermediate_llm-tailored-v1.json`
- `data/master/master_career_data.json` (for `exclude_from_resume` check)

**Creates:**
```
data/jobs/NNNNN_uuid/generated/
    resume_llm-tailored-v1.docx         # Full version
    resume_llm-tailored-v1_trimmed.docx # Top 5 experience only
    resume_preview_llm-tailored-v1.md   # Markdown preview
```

**Usage:**
```bash
python scripts/05_render_resume.py --uuid cdb9a3fa
python scripts/05_render_resume.py --uuid cdb9a3fa --all   # no trimming
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `--uuid` | required | — |
| `--version` | `v1` | Which intermediate file to load |
| `--all` | off | Include all experiences (skip trimmed logic) |

**DOCX document structure:**
```
[Name — Preferred Title]
[Address | Phone | Email | LinkedIn | GitHub]
─────────────────────────────────────────
SUMMARY
[4-6 tailored sentences]

FLAGSHIP PROJECTS
[Name] | [Description] | [Tech stack] | [Timeframe]

EXPERIENCE
[Company]                          [Start – End]
[Title]
  • Bullet 1 (most relevant first)
  • Bullet 2
  ...

SKILLS
[Comma-separated, job-relevant skills first]

EDUCATION
[School] | [Degree] | [Year]
```

---

### 06 — Company Research

**File:** `scripts/06_company_research.py`  
**Purpose:** Determine if the employer is a staffing agency (skip deep research) or a real product/SaaS company (fetch culture and values for the cover letter).

**How it works:**
1. Loads company name and website from `tailored_data.yaml`
2. First Grok call: "Is this company an agency/staffing firm or a product/enterprise company?"
3. If `enterprise`: second Grok call fetches company history, mission, culture, tech focus
4. Saves both classification and research text

**Reads:**
- `data/jobs/NNNNN_uuid/tailored/tailored_data_*.yaml`

**Creates:**
```
data/jobs/NNNNN_uuid/research/
    company_research_v1.yaml
```

**Usage:**
```bash
python scripts/06_company_research.py --uuid cdb9a3fa
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `--uuid` | required | — |
| `--version` | `v1` | — |
| `--model` | `grok-3` | — |

---

### 07 — Generate Cover Intermediate

**File:** `scripts/07_generate_cover_intermediate.py`  
**Purpose:** Draft a tailored professional cover letter in structured JSON.

**How it works:**
1. Loads master career data + tailored job data + company research (if available)
2. Calls Grok: "Write a 250-400 word professional cover letter. Use company research to personalize. Base all claims on the master profile only."
3. Parses JSON: header, salutation, intro, body paragraphs, conclusion, sign-off
4. Saves to `generated/cover_intermediate_v1.json`

**Reads:**
- `data/master/master_career_data.json`
- `data/master/skills.yaml`
- `data/jobs/NNNNN_uuid/tailored/tailored_data_*.yaml`
- `data/jobs/NNNNN_uuid/research/company_research_*.yaml` (if exists)

**Creates:**
```
data/jobs/NNNNN_uuid/generated/
    cover_intermediate_v1.json
```

**Usage:**
```bash
python scripts/07_generate_cover_intermediate.py --uuid cdb9a3fa
```

---

### 08 — Render Cover Letter

**File:** `scripts/08_render_cover_letter.py`  
**Purpose:** Turn the JSON cover letter into a submission-ready Word document and Markdown preview.

**How it works:**
1. Loads `cover_intermediate_*.json`
2. Builds a `python-docx` Document as a formal business letter
3. Exports Markdown preview

**Reads:**
- `data/jobs/NNNNN_uuid/generated/cover_intermediate_v1.json`

**Creates:**
```
data/jobs/NNNNN_uuid/generated/
    cover_letter_v1.docx      # Business letter format
    cover_preview_v1.md       # Markdown preview
```

**Usage:**
```bash
python scripts/08_render_cover_letter.py --uuid cdb9a3fa
```

**DOCX document structure:**
```
[Name]
[Address]
[Phone | Email]

[Date]

[Company]
[Employer Address]

Dear Hiring Manager,

[Intro: excitement about role + mission]

[Body paragraph 1: key experience alignment]
[Body paragraph 2: tooling/achievements + how they map to job needs]

[Conclusion: call to action, interview request]

Sincerely,
[Name]
```

---

### 09 — Update Application Status

**File:** `scripts/09_update_application_status.py`  
**Purpose:** Record that you applied and track subsequent events (interviews, rejections, offers).

**How it works:**
- Loads `metadata.yaml`
- Supports four subcommands (see below)
- Appends each status change to the `application.history` array

**Reads/Modifies:**
- `data/jobs/NNNNN_uuid/metadata.yaml`

**Usage:**
```bash
# Record application
python scripts/09_update_application_status.py --uuid cdb9a3fa apply \
    --date 2026-04-03 --method "Company Website" --notes "Submitted tailored v1"

# Update status later (interview, rejection, offer, etc.)
python scripts/09_update_application_status.py --uuid cdb9a3fa status \
    --status "Interview Scheduled" --notes "Phone screen April 10"

# View current status + full history
python scripts/09_update_application_status.py --uuid cdb9a3fa show

# List all jobs pending a follow-up action
python scripts/09_update_application_status.py list-pending
```

**Application method options:** `Company Website`, `LinkedIn`, `Indeed`, `Recruiter`, `Referral`, `Email`, `Other`

---

### 10 — Auto Pipeline (Orchestrator)

**File:** `scripts/10_auto_pipeline.py`  
**Purpose:** Run the entire pipeline (steps 00–09) with one command.

**How it works:**
1. Accepts intake file or existing UUID
2. Runs step 00 (duplicate check) — stops if duplicate found
3. Runs step 01, captures `🆔 Job UUID:` from stdout → extracts UUID
4. Auto-accepts (runs step 02 with `--accept`) — no manual gate
5. Chains steps 03 → 04 → 05 → 06 → 07 → 08 → 09 with the UUID
6. Each step runs as a subprocess with `env["PYTHONUTF8"] = "1"` for emoji safety on Windows

**Usage:**
```bash
# Full run from intake file
python scripts/10_auto_pipeline.py intake/myjob.md --method "LinkedIn"

# Resume an existing job (skip 00+01, run from 02 onward)
python scripts/10_auto_pipeline.py --uuid cdb9a3fa

# With overrides
python scripts/10_auto_pipeline.py intake/myjob.md \
    --model grok-3 \
    --version v2 \
    --temperature 0.3 \
    --date 2026-04-03 \
    --method "Recruiter" \
    --notes "Via James at TechRecruit"
```

**Key args:**
| Arg | Default | Meaning |
|---|---|---|
| `intake_file` | — | Path to intake .md (positional) |
| `--uuid` | — | Resume an existing job instead |
| `--method` | `Company Website` | Application method |
| `--date` | today | Application date |
| `--notes` | — | Notes saved to tracking |
| `--model` | `grok-3` | Passed to all LLM-calling steps |
| `--version` | `v1` | Passed to all versioned steps |
| `--no-move` | off | Don't move intake file |

**Console output** uses emoji markers: `🚀` (starting step), `✅` (success), `❌` (failure, exits).

---

### 10b — Force Pipeline

**File:** `scripts/10b_force_pipeline.py`  
**Purpose:** Same as `10_auto_pipeline.py` but **skips step 00** (the duplicate check).

**When to use:**
- You already applied to this company 3+ months ago — the original application is stale
- A job was re-posted with different requirements
- You want to re-run the pipeline on a job that was previously flagged as a duplicate

**Usage:** Identical to `10_auto_pipeline.py`.

---

### 11 — Search Jobs

**File:** `scripts/11_search_jobs.py`  
**Purpose:** Quick substring search across all your past jobs.

**How it works:**
- Walks all folders in `data/jobs/`
- Loads `metadata.yaml` and raw intake text
- Matches query against: company, role, status, description
- Displays results as a Rich console table

**Usage:**
```bash
python scripts/11_search_jobs.py "snowflake"
python scripts/11_search_jobs.py "remote data engineer"
python scripts/11_search_jobs.py "ACCEPTED"
```

**Output:**
```
UUID        Company         Role                    Status      Score
cdb9a3fa    Collective Health   Staff Data Engineer     ACCEPTED    92%
```

---

### 12 — Update Job

**File:** `scripts/12_update_job.py`  
**Purpose:** Advanced fuzzy search + mass update for job tracking. A more powerful version of script 09.

**How it works:**
- Fuzzy matches jobs by company/role/status/UUID (supports OR/AND logic)
- If multiple matches: interactive selection
- Updates: status, notes, follow-up date
- Appends change to `application.history`

**Usage:**
```bash
python scripts/12_update_job.py "Stripe" --status "Rejected" --notes "No response after 2 weeks"
python scripts/12_update_job.py "staff engineer" --follow-up 2026-04-17
python scripts/12_update_job.py "ACCEPTED" --notes "Batch note: check LinkedIn"
```

---

## 7. Utility Scripts

### vector_ops.py

**File:** `scripts/utils/vector_ops.py`  
**Purpose:** Shared low-level functions for all FAISS and embedding operations. Used by scripts 00 and `build_job_index.py`.

**Constants:**
```python
PROJECT_ROOT    = Path(__file__).parent.parent.parent
INDEX_DIR       = PROJECT_ROOT / "data" / "job_index"
INDEX_PATH      = INDEX_DIR / "faiss_job_descriptions.index"
METADATA_PATH   = INDEX_DIR / "jobs_metadata.yaml"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

**Key functions:**

```python
get_model() -> SentenceTransformer
# Lazy-loads the embedding model (cached after first call)

get_embedding(text: str) -> np.ndarray
# Returns shape (1, 384), float32, L2-normalized
# Normalized so inner product == cosine similarity

load_index_and_metadata() -> tuple[faiss.Index, list[dict]]
# Loads binary FAISS index + YAML metadata from disk

save_index_and_metadata(index: faiss.Index, metadata: list[dict]) -> None
# Writes both to disk
```

**FAISS index type:** `IndexFlatIP` (inner product on normalized vectors = cosine similarity).  
**Vector dimension:** 384 (from `all-MiniLM-L6-v2`).

---

### build_job_index.py

**File:** `scripts/utils/build_job_index.py`  
**Purpose:** Build or rebuild the FAISS index from scratch by re-embedding all accepted jobs.

**When to run manually:**
- Index is corrupted
- You added/removed jobs directly without going through script 02
- First setup on a new machine

**How it works:**
1. Walks `data/jobs/` — loads each job's raw description text
2. Embeds with `get_embedding()`
3. Creates new `faiss.IndexFlatIP`
4. Adds all vectors, saves index + metadata YAML

**Usage:**
```bash
python scripts/utils/build_job_index.py
python scripts/utils/build_job_index.py --rebuild   # force full rebuild
```

**Also automatically called by:** `02_decide_job.py` whenever a job is `ACCEPTED`.

---

## 8. Source Modules (src/)

### GrokClient

**File:** `src/ai/grok_client.py`

The API wrapper. Uses `openai` Python SDK pointed at xAI's endpoint.

**Constructor:**
```python
client = GrokClient(model="grok-3")
# Reads XAI_API_KEY from .env automatically via load_dotenv()
# Base URL: https://api.x.ai/v1
```

**Key methods:**

```python
client.chat(
    messages: list[dict],   # [{"role": "user", "content": "..."}]
    temperature: float = 0.7,
    max_tokens: int = 800,
    **kwargs
) -> str
# Generic completion. Returns content string directly.

client.query(
    prompt: str,
    model: str = None,
    temperature: float = 0.0,
    max_tokens: int = 4500
) -> str
# Convenience: wraps prompt in a single user message.

client.generate_tailored_summary(
    job_description: str,
    master_summary: str,
    max_tokens: int = 400
) -> str
# Specialized: ATS-optimized resume summary generation.
```

**Example:**
```python
from src.ai.grok_client import GrokClient

client = GrokClient(model="grok-3")
response = client.chat([
    {"role": "system", "content": "You are a resume expert."},
    {"role": "user", "content": "Score this job fit: ..."}
], temperature=0.5, max_tokens=1000)
print(response)
```

---

### MasterProfileLoader

**File:** `src/loaders/master_profile.py`

Loads and caches master profile data. Provides query methods used in resume/cover generation.

**Constructor:**
```python
loader = MasterProfileLoader(data_dir=None)
# Defaults to data/master/ relative to project root
```

**Key methods:**
```python
loader.get_personal_info()          -> dict
loader.get_summary(variant="short") -> str   # "short" or "long"
loader.get_experience(n=None)       -> list[dict]
loader.get_recent_experience(n=3)   -> list[dict]
loader.get_flagship_projects()      -> list[dict]
loader.get_skills(min_years=0.0)    -> list[dict]
loader.get_top_skills(n=15, min_years=2.0) -> list[dict]  # sorted by expertise
loader.get_skill_names(n=20)        -> list[str]
```

**Usage:**
```python
from src.loaders.master_profile import MasterProfileLoader

loader = MasterProfileLoader()
print(loader.get_personal_info())
print(loader.get_top_skills(15))
for job in loader.get_experience():
    print(job["company"], job["role"])
```

---

## 9. Data Structures & File Schemas

### Intake Markdown

**Location:** `intake/NNNNN.CompanyName.MMDDYYYY.HHMM.md`

```markdown
Company_website: https://stripe.com
Location: Remote - US
Employment_type: Full-time

# Staff Data Engineer — Stripe

## About the Role
[job description body starts here]

## Requirements
- 7+ years data engineering
- Python, SQL
- ...

## Nice to Have
- Spark experience
- ...
```

The front-matter key-values before the first blank line are parsed by script 01.

---

### Job Folder Layout

```
data/jobs/00001_cdb9a3fa/
├── 00001.Collective_Health.02052026.1328.md    # original intake (moved here)
├── metadata.yaml                               # master tracking file
├── raw/
│   └── raw_intake.md                          # verbatim copy of intake
├── score/
│   └── score_report_20260205_194847.md        # Grok scoring output
├── tailored/
│   └── tailored_data_llm-v1.yaml              # extracted job requirements
├── research/
│   └── company_research_v1.yaml               # company classification + research
└── generated/
    ├── resume_intermediate_llm-tailored-v1.json
    ├── resume_llm-tailored-v1.docx
    ├── resume_llm-tailored-v1_trimmed.docx
    ├── resume_preview_llm-tailored-v1.md
    ├── cover_intermediate_v1.json
    ├── cover_letter_v1.docx
    └── cover_preview_v1.md
```

---

### metadata.yaml

The tracking file for every job. Written by scripts 01, 02, 09, 12.

```yaml
uuid: "cdb9a3fa-4618-4d9e-a636-6709f514c968"
job_id: "00001_cdb9a3fa"
original_filename: "00001.Collective_Health.02052026.1328.md"
company: "Collective Health"
role: "Staff Data Engineer"
status: "ACCEPTED"          # PENDING | ACCEPTED | REJECTED | HELD
score: 92                   # 0-100
recommendation: "Strong Proceed"
score_date: "2026-02-05T19:48:47"
created_at: "2026-02-05T19:45:00"
location_preference: "Remote"
notes: "Great mission fit. Strong Snowflake requirement."
last_decision: "ACCEPTED"
last_decision_at: "2026-02-05T20:00:00"

application:
  applied: true
  applied_date: "2026-02-05"
  applied_method: "Company Site"
  application_notes: "Tailored cover letter attached"
  history:
    - date: "2026-02-05"
      status: "Applied"
      notes: "Submitted via company portal"
    - date: "2026-02-10"
      status: "Interview Scheduled"
      notes: "Phone screen with recruiter 2026-02-14"
    - date: "2026-02-14"
      status: "Phone Screen Complete"
      notes: "Went well, expect technical round next week"
```

---

### score_report.md

Generated by script 01. Plain Markdown, for human reading.

```markdown
# Score Report for 00001.Collective_Health.02052026.1328

## Match Score: 92%
## Recommendation: Strong Proceed

## Strongest Matches
- **Data Engineering Depth**: 20+ years — well above required 8+
- **Python & SQL**: Expert level in both core requirements
- **Cloud / AWS**: Strong AWS serverless background matches stack
- **Dimensional Modeling**: Directly relevant to their data warehouse needs

## Gaps & Risks
- **Snowflake**: Not in recent experience. *Mitigation*: Strong SQL + 
  AWS Redshift background makes ramp-up fast; can self-study.
- **dbt**: Not listed. *Mitigation*: Pipeline/transformation experience 
  is analogous; quick to learn.

## Advice
- Emphasize Snowflake adjacency (Redshift, Athena) and willingness to ramp
- Lead with dimensional modeling wins at CITI
- Include the Prophet/scikit-learn forecasting work — shows ML awareness
```

---

### tailored_data.yaml

Generated by script 03. Structured extraction of the job posting.

```yaml
company_name: "Collective Health"
company_website: "https://collectivehealth.com"
job_title: "Staff Data Engineer"
location: "Remote - US"

job_summary: >
  Design and maintain data infrastructure for Collective Health's
  healthcare data platform including Snowflake warehouse and ELT pipelines.

responsibilities:
  - "Build and maintain ELT pipelines using dbt and Airflow"
  - "Design dimensional models for analytics consumers"
  - "Partner with data science on ML feature pipelines"
  - "Own data quality monitoring and alerting"

requirements:
  - "8+ years data engineering"
  - "Expert SQL and data modeling"
  - "Python or Scala"
  - "Experience with Snowflake or similar cloud warehouse"

preferred:
  - "dbt experience"
  - "Airflow or similar orchestration"
  - "Healthcare data familiarity"

must_have_skills:
  - "data engineering"
  - "SQL"
  - "Python"
  - "data warehouse modeling"
  - "ELT pipelines"

nice_to_have_skills:
  - "dbt"
  - "Airflow"
  - "Databricks"
  - "Spark"

extracted_skills:
  - "python"
  - "sql"
  - "snowflake"
  - "dbt"
  - "airflow"
  - "databricks"
  - "spark"
  - "aws"

ats_keywords:
  - "data engineer"
  - "staff data engineer"
  - "ELT pipelines"
  - "dimensional modeling"
  - "data warehouse"
  - "Snowflake"
  - "dbt"

benefits:
  - "Comprehensive health coverage"
  - "Equity"
  - "Remote-first"
```

---

### resume_intermediate.json

Generated by script 04. The JSON that script 05 renders into DOCX.

```json
{
  "personal": {
    "full_name": "Sean Luka Girgis",
    "preferred_title": "Staff Data Engineer | Snowflake · dbt · ELT Pipelines",
    "address": "Murphy, TX 75094",
    "phone": "214-315-2190",
    "email": "seanlgirgis@gmail.com",
    "linkedin": "https://linkedin.com/in/seanlgirgis",
    "github": "https://github.com/seanlgirgis",
    "personal_website": "",
    "location_preference": "Remote - US"
  },
  "summary": "Staff Data Engineer with 20+ years designing enterprise-grade ELT pipelines and dimensional data models. Proven track record automating ingestion for 6,000+ endpoints at CITI, building ML forecasting with Prophet/scikit-learn, and delivering Redshift/Athena-based analytics. Eager to bring this expertise to Collective Health's healthcare data platform.",
  "flagship_projects": [
    {
      "name": "Capacity Forecasting Platform — CITI",
      "description": "Built ML pipeline ingesting P95 telemetry from 6,000+ production endpoints, generating 90-day capacity forecasts that eliminated 3 infrastructure outages",
      "technologies": ["Python", "Pandas", "Prophet", "scikit-learn", "Oracle", "AWS S3"],
      "timeframe": "2021–2023"
    }
  ],
  "experience": [
    {
      "company": "CITI",
      "title": "Senior Capacity & Data Engineer",
      "start_date": "2017-11",
      "end_date": "2025-12",
      "bullets": [
        "Architected automated ELT pipelines (Python/Pandas) ingesting P95 telemetry from 6,000+ endpoints into dimensional Oracle schemas — reduced manual reporting from 3 days to 2 hours",
        "Designed star-schema data models optimized for time-series and historical retention queries across 8TB+ of capacity data",
        "Built ML forecasting models (Prophet, scikit-learn) achieving 94% accuracy on 90-day infrastructure demand forecasts",
        "Deployed AWS Glue + Athena pipelines to replace on-prem ETL jobs — reduced operational cost by 35%",
        "Mentored 4 junior engineers on Python best practices, testing, and data pipeline design patterns"
      ]
    },
    ...
  ],
  "skills": [
    "Python", "SQL / Oracle", "AWS (Glue, Athena, S3, Lambda)",
    "Snowflake", "dbt", "Airflow", "Pandas", "scikit-learn",
    "Prophet", "Spark (PySpark)", "Redshift", "ETL/ELT Pipelines"
  ],
  "education": [
    {
      "school": "University of Texas at Dallas",
      "degree": "B.S.",
      "field": "Computer Science",
      "graduation": "2004"
    }
  ]
}
```

---

### cover_intermediate.json

Generated by script 07. The JSON that script 08 renders into DOCX.

```json
{
  "header": {
    "name": "Sean Luka Girgis",
    "address": "424 Oriole Dr., Murphy, TX 75094",
    "phone": "214-315-2190",
    "email": "seanlgirgis@gmail.com",
    "date": "April 2026",
    "employer_address": "Collective Health\nHiring Manager\nSan Francisco, CA"
  },
  "salutation": "Dear Hiring Manager,",
  "intro": "I am excited to apply for the Staff Data Engineer position at Collective Health. The mission to simplify healthcare for millions of Americans resonates deeply, and I believe my 20+ years of data engineering expertise is a strong match for your platform needs.",
  "body": [
    "In my most recent role as Senior Capacity & Data Engineer at CITI, I architected automated ELT pipelines processing P95 telemetry from over 6,000 production endpoints into dimensional Oracle schemas — reducing reporting latency from 3 days to 2 hours. I also designed star-schema data models supporting 8TB+ of time-series capacity data and built ML forecasting models achieving 94% accuracy on 90-day infrastructure demand projections.",
    "I am particularly drawn to Collective Health's Snowflake-centered stack. While my most recent warehouse work was with Oracle and AWS Redshift, the dimensional modeling and ELT pipeline patterns translate directly. I have delivered Airflow-orchestrated pipelines and am deeply familiar with the practices dbt formalizes — column-level lineage, incremental models, and test-first data quality."
  ],
  "conclusion": "I would welcome the chance to discuss how my background can accelerate Collective Health's data platform roadmap. Thank you for your time and consideration.",
  "sign_off": "Sincerely,\nSean Luka Girgis"
}
```

---

### company_research.yaml

Generated by script 06. Feeds into script 07 for cover letter personalization.

```yaml
company: "Collective Health"
type: "enterprise"          # "enterprise" | "agency"
website: "https://collectivehealth.com"
classified_at: "jobsearch"

research: |
  Collective Health is a San Francisco-based health benefits platform
  founded in 2013 that manages self-funded health plans for employers.
  The company serves 70+ enterprise clients with over $1.5B in healthcare
  spend processed annually. Their mission centers on making healthcare
  more transparent and navigable for plan members.

  Technology stack is modern: Snowflake data warehouse, dbt for
  transformation, Airflow for orchestration, Python-first engineering
  culture. Engineering values include data reliability, observability
  (Monte Carlo), and treating data as a product.

  Recent focus includes expanding ML-driven care navigation features
  and deepening their analytics platform for employer clients.
```

If `type: "agency"`, the research field is blank — cover letters for agencies get a generic closing rather than mission-specific personalization.

---

### master_career_data.yaml

Full schema (abridged here; the real file has all roles):

```yaml
personal:
  name: "Sean Luka Girgis"
  title: "Senior Data Engineer"
  location: "Murphy, TX (Dallas area)"
  email: "seanlgirgis@gmail.com"
  phone: "214-315-2190"
  linkedin: "https://linkedin.com/in/seanlgirgis"
  github: "https://github.com/seanlgirgis"

summary:
  short: "Senior Data Engineer with 20+ years in enterprise ETL/ELT, ML pipelines, and cloud data platforms."
  long: "..."

experience:
  - company: "CITI"
    role: "Senior Capacity & Data Engineer"
    location: ""
    start: "2017-11"
    end: "2025-12"
    highlights:
      - "Architected automated ETL pipelines (Python/Pandas) ingesting P95 telemetry from 6,000+ endpoints..."
      - "Designed optimized Oracle schemas for historical retention..."
      - "Developed ML forecasting models (Prophet, scikit-learn)..."
      - "..."
    # exclude_from_resume: true   ← add this to hide a role

  - company: "Previous Company"
    role: "Data Engineer"
    ...

flagship_projects:
  - name: "Capacity Forecasting Platform"
    description: "..."
    technologies: ["Python", "Pandas", "Prophet", "Oracle", "AWS"]
    timeframe: "2021–2023"
```

---

### skills.yaml

```yaml
- name: "SQL / Oracle"
  years: 18
  proficiency: "Expert"
  last_used: "2025"
  categories: ["Databases"]
  notes: "Schema design, partitioning, PL/SQL, Pro*C, querying"

- name: "Python"
  years: 15
  proficiency: "Expert"
  last_used: "2025"
  categories: ["Data Engineering", "Scripting"]
  notes: "Pandas, generators, ETL pipelines, scripting, multiprocessing"

- name: "AWS (Glue, Athena, S3, Lambda)"
  years: 6
  proficiency: "Advanced"
  last_used: "2025"
  categories: ["Cloud", "Data Engineering"]
  notes: "Serverless ETL, data lake architecture, cost optimization"

- name: "Snowflake"
  years: 1
  proficiency: "Intermediate"
  last_used: "2024"
  categories: ["Databases", "Cloud"]
  notes: "Learning; Redshift/Athena background is directly transferable"
```

`proficiency` weight used by `get_top_skills()`:
| Value | Weight |
|---|---|
| Expert | 4 |
| Advanced | 3 |
| Intermediate-Advanced | 2.5 |
| Intermediate | 2 |
| Beginner | 1 |

---

### FAISS Index & Metadata

**Binary index:** `data/job_index/faiss_job_descriptions.index`  
**Type:** `IndexFlatIP` (384-dimensional, normalized vectors)  
**Similarity:** Inner product on L2-normalized vectors = cosine similarity  

**Metadata YAML:** `data/job_index/jobs_metadata.yaml`

```yaml
- uuid: "cdb9a3fa-4618-4d9e-a636-6709f514c968"
  job_id: "00001_cdb9a3fa"
  company: "Collective Health"
  role: "Staff Data Engineer"
  status: "ACCEPTED"
  apply_date: "2026-02-05"
  description: "[full job description text used for embedding]"

- uuid: "..."
  ...
```

The FAISS index and this YAML are always kept in sync. Vector `i` in the index corresponds to `metadata[i]`.

---

## 10. Configuration Files

### `.env`
```bash
DEFAULT_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
DEFAULT_LLM_PROVIDER=xai
XAI_API_KEY=xai-...
```
Only non-path configuration. All directory paths are computed at runtime.

### `.vscode/settings.json`
```json
{
  "python.defaultInterpreterPath": "C:\\py_venv\\JobSearch\\Scripts\\python.exe",
  "python.analysis.extraPaths": ["${workspaceFolder}/src"],
  "terminal.integrated.env.windows": {
    "PROJECT_ROOT": "${workspaceFolder}",
    "PYTHONPATH": "${workspaceFolder}\\src;${env:PYTHONPATH}",
    "JOBS_DB_DIR": "${workspaceFolder}\\data\\jobs",
    "RESUMES_DIR": "${workspaceFolder}\\data\\resumes",
    "VECTOR_DB_PATH": "${workspaceFolder}\\data\\vectorstore",
    "DEFAULT_EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2",
    "DEFAULT_LLM_PROVIDER": "xai",
    "PATH": "C:\\py_venv\\JobSearch\\Scripts;C:\\py_venv\\JobSearch;${env:PATH}"
  }
}
```

### `.claude/settings.json`
```json
{
  "permissions": {
    "allow": ["Bash(*)", "Edit(*)", "Write(*)", "Read(*)", "MultiEdit(*)", 
              "NotebookEdit(*)", "WebFetch(*)", "WebSearch(*)", "TodoWrite(*)"],
    "deny": []
  }
}
```

### `env_setter.ps1`
```powershell
$venvPath = "C:\py_venv\JobSearch"
& "$venvPath\Scripts\Activate.ps1"
$env:PROJECT_ROOT = Convert-Path (Split-Path -Parent $MyInvocation.MyCommand.Path)
$env:PYTHONPATH   = "$env:PROJECT_ROOT\src;$env:PYTHONPATH"
$env:JOBS_DB_DIR    = "$env:PROJECT_ROOT\data\jobs"
$env:RESUMES_DIR    = "$env:PROJECT_ROOT\data\resumes"
$env:VECTOR_DB_PATH = "$env:PROJECT_ROOT\data\vectorstore"
$env:DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
$env:DEFAULT_LLM_PROVIDER    = "xai"
Write-Host "JobSearch environment activated [OK]" -ForegroundColor Green
```

---

## 11. Full Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│  INPUT: intake/NNNNN.Company.MMDDYYYY.HHMM.md           │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  00: Duplicate?     │ ← FAISS cosine search
              │  similarity ≥ 0.82  │   all-MiniLM-L6-v2
              │  → EXIT if dup      │
              └──────────┬──────────┘
                         │ not a dup
              ┌──────────▼──────────────────────┐
              │  01: Score Job                   │
              │  • Parse filename → company/date │
              │  • Create data/jobs/NNNNN_uuid/  │
              │  • Grok: 0-100% fit + advice     │
              │  • WRITES: metadata.yaml         │
              │            raw/raw_intake.md     │
              │            score/report.md       │
              └──────────┬──────────────────────┘
                         │ UUID emitted to stdout
              ┌──────────▼───────────────┐
              │  02: Decide              │
              │  • ACCEPT / REJECT / HOLD│
              │  • If ACCEPT → rebuild   │
              │    FAISS index           │
              │  • WRITES: metadata.yaml │
              └──────────┬───────────────┘
                         │ ACCEPTED
              ┌──────────▼────────────────────────────┐
              │  03: Tailor Job Data                   │
              │  • Grok: extract requirements,         │
              │    skills, ATS keywords, must-haves    │
              │  • WRITES: tailored/tailored_data.yaml │
              └──────────┬────────────────────────────┘
                         │
     ┌───────────────────┴──────────────────┐
     │                                      │
┌────▼──────────────────────┐   ┌───────────▼────────────────┐
│  04: Resume Intermediate  │   │  06: Company Research       │
│  • Load: master + tailored│   │  • Grok: agency vs          │
│  • Grok: tailor bullets   │   │    enterprise?             │
│    (master facts only)    │   │  • If enterprise: fetch     │
│  • WRITES: resume_int.json│   │    culture/values/mission  │
└────┬──────────────────────┘   │  • WRITES:                 │
     │                          │    research/research.yaml  │
┌────▼──────────────────────┐   └───────────┬────────────────┘
│  05: Render Resume        │               │
│  • python-docx rendering  │   ┌───────────▼────────────────┐
│  • WRITES:                │   │  07: Cover Intermediate    │
│    resume.docx            │   │  • Load: master + tailored │
│    resume_trimmed.docx    │   │    + company research      │
│    resume_preview.md      │   │  • Grok: write cover letter│
└───────────────────────────┘   │  • WRITES: cover_int.json  │
                                └───────────┬────────────────┘
                                            │
                                ┌───────────▼────────────────┐
                                │  08: Render Cover Letter   │
                                │  • python-docx rendering   │
                                │  • WRITES:                 │
                                │    cover_letter.docx       │
                                │    cover_preview.md        │
                                └───────────┬────────────────┘
                                            │
                                ┌───────────▼────────────────┐
                                │  09: Update Status         │
                                │  • Record: applied,        │
                                │    method, date, notes     │
                                │  • WRITES: metadata.yaml   │
                                └───────────┬────────────────┘
                                            │
┌───────────────────────────────────────────▼───────────────┐
│  FINAL OUTPUT: data/jobs/NNNNN_uuid/                       │
│  ├── metadata.yaml          (full tracking history)        │
│  ├── raw/raw_intake.md      (original job posting)         │
│  ├── score/score_report.md  (fit %, gaps, advice)          │
│  ├── tailored/tailored_data.yaml (requirements, keywords)  │
│  ├── research/company_research.yaml (culture/values)       │
│  └── generated/                                            │
│      ├── resume_intermediate.json                          │
│      ├── resume.docx              ← SUBMIT THIS            │
│      ├── resume_trimmed.docx      ← shorter option         │
│      ├── resume_preview.md        ← quick review           │
│      ├── cover_intermediate.json                           │
│      ├── cover_letter.docx        ← SUBMIT THIS            │
│      └── cover_preview.md         ← quick review           │
└────────────────────────────────────────────────────────────┘
```

---

## 12. Day-to-Day Usage Cheatsheet

### Process a new job (fully automated)
```bash
python scripts/10_auto_pipeline.py intake/00051.Stripe.04032026.0900.md \
    --method "Company Website"
```

### Process a new job but skip duplicate check
```bash
python scripts/10b_force_pipeline.py intake/00051.Stripe.04032026.0900.md
```

### Re-run just the resume (after editing master profile)
```bash
python scripts/04_generate_resume_intermediate.py --uuid cdb9a3fa --overwrite
python scripts/05_render_resume.py --uuid cdb9a3fa
```

### Re-run just the cover letter (after editing master profile)
```bash
python scripts/07_generate_cover_intermediate.py --uuid cdb9a3fa
python scripts/08_render_cover_letter.py --uuid cdb9a3fa
```

### Record a status update
```bash
# Applied
python scripts/09_update_application_status.py --uuid cdb9a3fa apply \
    --date 2026-04-03 --method "LinkedIn" --notes "Referred by James"

# Interview scheduled
python scripts/09_update_application_status.py --uuid cdb9a3fa status \
    --status "Interview Scheduled" --notes "Technical round April 10 at 2pm"

# View history
python scripts/09_update_application_status.py --uuid cdb9a3fa show
```

### Search your jobs
```bash
python scripts/11_search_jobs.py "snowflake"
python scripts/11_search_jobs.py "ACCEPTED"
python scripts/11_search_jobs.py "remote senior engineer"
```

### Mass-update + fuzzy search
```bash
python scripts/12_update_job.py "Stripe" --status "No Response" --notes "Following up"
```

### Rebuild FAISS index from scratch
```bash
python scripts/utils/build_job_index.py --rebuild
```

### Export master profile to JSON (after editing YAML)
```bash
python scripts/profile_export.py
```

---

## 13. Archived & Legacy Scripts

| File | Status | Superseded By |
|---|---|---|
| `scripts/Archived/PreVectorRefactor/00_check_applied_before.py` | Archived | `scripts/00_check_applied_before.py` (uses FAISS) |
| `scripts/Archived/generate_resume.py` | Archived | `scripts/04 + 05` split |
| `scripts/Archived/resume_intermediate.py` | Archived | `scripts/04_generate_resume_intermediate.py` |
| `scripts/Archived/tailor_job_data.py` | Archived | `scripts/03_tailor_job_data.py` |
| `scripts/keep/00_check_applied_before.py` | Backup | Current `scripts/00` |
| `scripts/keep/02_decide_job.py` | Backup | Current `scripts/02` |
| `scripts/generate_cover_letter.py` | Legacy | `scripts/07 + 08` split |
| `scripts/resume_generation.py` | Legacy | `scripts/04 + 05` split |

The major refactor was the **Vector Refactor** — moving duplicate detection from simple substring matching to FAISS semantic search. Pre-refactor scripts live in `Archived/PreVectorRefactor/`.

---

## 14. Documentation Files Reference

| File | Contents |
|---|---|
| `docs/pipeline-runner.md` | Manual step-by-step walkthrough of all 10 steps with expected outputs |
| `docs/project_summary_for_claude.md` | Context document for Claude Code sessions — architecture overview |
| `docs/job-search-strategy.md` | 27 target roles, Tier 1/2/3 job boards, recruiter outreach templates |
| `docs/agentic-rag-curriculum.md` | Self-study curriculum for AI/LLM/Bedrock/Agents to upskill for AI-adjacent roles |
| `docs/claude-training-prompts.md` | Interview prep prompts for LLM APIs, Bedrock, agent systems |
| `docs/desired_salary.md` | Salary negotiation strategy, ranges, BATNA |
| `CodingStyle.md` | Project coding standards: PEP 8, type hints, docstrings, naming conventions |
| `README.md` | Quick-start overview |
| `startingDocs/` | Historical documents from initial project setup (reference only) |

---

*Last updated: 2026-04-03*
