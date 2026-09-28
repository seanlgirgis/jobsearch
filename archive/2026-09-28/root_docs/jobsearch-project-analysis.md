# JobSearch Project — Complete Analysis
**Generated:** 2026-02-26
**Analyzed by:** Claude (Sonnet 4.6)
**Repo:** seanlgirgis/jobsearch
**Location on disk:** `C:\jobsearch`

---

## 1. WHAT IS THIS PROJECT

### Purpose & Goal (Plain Language)

This is **Sean Luka Girgis's personal AI-powered job application engine.** It is a command-line pipeline that takes a raw job posting (a markdown file), and automatically:

1. Checks whether Sean has already applied to something similar
2. Scores how well the job fits his profile using an AI model
3. Tailors his resume specifically for that job
4. Generates a custom cover letter mentioning the company's values
5. Renders both into Word documents ready to submit
6. Records the application, tracks its status, and keeps a history

### Problem It Solves for Sean

Sean is a Senior Data Engineer with 20+ years of experience who is actively job searching (as of early 2026). The problem: managing dozens of job applications manually is brutal — you copy-paste, tweak resumes, forget which version you sent, lose track of follow-up dates, and waste hours writing generic cover letters.

This system eliminates that friction. Sean drops a job posting into the `intake/` folder, runs one command, and gets a tailored resume and cover letter in minutes. The system also prevents duplicate applications and tracks every status change.

**Sean's target roles:** Senior Data Engineer, AI Engineer, Cloud Data Architect, Capacity Planning Engineer, PySpark/AWS Specialist
**Sean's location:** Murphy/Plano, TX (DFW area, prefers remote or hybrid)

---

## 2. ARCHITECTURE

### How the System is Structured

```
jobsearch/
├── intake/                    ← Drop new job postings here (markdown)
├── data/
│   ├── source_of_truth.json  ← MASTER: Sean's full career profile (canonical)
│   ├── master/               ← Derived exports from source_of_truth.json
│   │   ├── master_career_data.json   ← Used by pipeline scripts (JSON format)
│   │   ├── master_career_data.yaml   ← Used by master_profile.py (YAML format)
│   │   └── skills.yaml               ← Standalone skills list
│   ├── jobs/                 ← One folder per job application
│   │   └── 00001_cdb9a3fa/   ← Format: NNNNN_uuid8
│   │       ├── metadata.yaml         ← Status, score, history, UUID
│   │       ├── raw/                  ← raw_intake.md (original posting)
│   │       ├── score/                ← score_report_TIMESTAMP.md
│   │       ├── tailored/             ← tailored_data_v1.yaml (LLM-extracted)
│   │       ├── generated/            ← resume_*.json, resume_*.docx, cover_*.docx
│   │       └── research/             ← company_research.yaml (enterprise only)
│   ├── job_index/            ← RAG vector index
│   │   ├── faiss_job_descriptions.index  ← FAISS binary index
│   │   └── jobs_metadata.yaml            ← Index metadata (company, role, status)
│   ├── resumes/              ← Reserved, currently empty (.gitkeep only)
│   └── vectorstore/          ← Reserved, currently empty (.gitkeep only)
├── scripts/                  ← The 13 pipeline scripts (00-12)
├── scripts/utils/            ← Shared vector/FAISS utilities
├── src/
│   ├── ai/grok_client.py     ← xAI Grok API wrapper
│   └── loaders/master_profile.py  ← Loads career data for pipeline
├── user_guide/v0/            ← Per-script documentation
├── startingDocs/             ← Design decisions & session history
├── Teachables/               ← Learning notes from the build process
└── Specs/                    ← Architecture specs (minimal so far)
```

### How the Scripts Connect and Flow

```
[New Job .md file in intake/]
        │
        ▼
00_check_applied_before.py  →  FAISS semantic search → exit if duplicate
        │ (passes)
        ▼
01_score_job.py  →  Grok API → Score + recommendation → creates data/jobs/NNNNN_uuid/
        │
        ▼
02_decide_job.py  →  User decision (accept/reject/hold) → updates metadata.yaml
        │           → on ACCEPT: triggers build_job_index.py to re-index
        │ (if ACCEPTED)
        ▼
03_tailor_job_data.py  →  Grok API → structured YAML of job requirements/skills
        │
        ▼
04_generate_resume_intermediate.py  →  Grok API → tailored resume JSON
        │
        ▼
05_render_resume.py  →  python-docx → resume_v1.docx + resume_v1_trimmed.docx
        │
        ▼
06_company_research.py  →  Grok API → classify agency/enterprise → research YAML
        │
        ▼
07_generate_cover_intermediate.py  →  Grok API → cover letter JSON
        │
        ▼
08_render_cover_letter.py  →  python-docx → cover_letter_v1.docx
        │
        ▼
09_update_application_status.py  →  records applied date/method/notes → metadata.yaml
```

**Script 10 (auto_pipeline.py)** runs steps 01–09 as a single command. Steps 11 and 12 are standalone utilities for searching and updating existing job records.

### What the RAG Component Does

RAG (Retrieval-Augmented Generation) is used in two distinct ways:

**1. Semantic Duplicate Detection (script 00)**
When a new job is submitted, it is embedded using a local sentence-transformer model (`all-MiniLM-L6-v2`), and the resulting vector is compared against all previously indexed job descriptions using FAISS (cosine similarity). If similarity ≥ 0.82, the job is flagged as a likely duplicate and the pipeline exits. This prevents wasting time re-applying to essentially the same role.

**2. Implicit RAG in Resume/Cover Generation (scripts 04, 07)**
The LLM (Grok) is grounded by receiving:
- Sean's full master career data (JSON)
- The tailored job data (YAML with extracted requirements, skills, ATS keywords)
- Company research context

This is prompt-based RAG — the retrieved context (career data + job data + company research) is injected directly into the prompt, constraining the LLM to only use real facts from Sean's history.

---

## 3. THE SCRIPTS — All 13

### Script 00 — `00_check_applied_before.py`
**What it does:** Semantic duplicate check. Embeds the new job posting, queries the FAISS index, and prints a similarity table. Exits with code 1 (blocking) if any past job exceeds the threshold (default: 0.82).
**When Sean uses it:** Automatically at the start of `10_auto_pipeline.py`. Can also be run standalone before manually processing a job.

---

### Script 01 — `01_score_job.py`
**What it does:** The intake and scoring engine. Reads the job markdown, extracts metadata from the filename and front-matter (company, website, location), calls Grok to compare the job against Sean's profile, parses the score (0–100) and recommendation (Strong Proceed / Proceed / Hold / Skip), creates the structured job folder (`data/jobs/NNNNN_uuid/`), moves the file from `intake/`, writes `metadata.yaml` and `score/score_report_*.md`.
**When Sean uses it:** First step on any new job. Either directly (`python scripts/01_score_job.py intake/job.md`) or via the auto pipeline.

---

### Script 02 — `02_decide_job.py`
**What it does:** Simple decision gate. Updates `metadata.yaml` with `--accept`, `--reject`, or `--hold` status plus a reason note. If accepting, triggers an automatic FAISS index rebuild so future duplicate checks include this job.
**When Sean uses it:** After reviewing the score report. When running the auto pipeline, this step auto-accepts every scored job (bypassing human review).

---

### Script 03 — `03_tailor_job_data.py`
**What it does:** Deep job parsing via LLM. Sends the raw job description to Grok with instructions to output a clean YAML structure containing: `company_name`, `company_website`, `job_title`, `location`, `extracted_skills`, `job_summary`, `responsibilities`, `requirements`, `preferred`, `benefits`, `must_have_skills`, `nice_to_have_skills`, and `ats_keywords`. Falls back to naive regex extraction if the LLM fails. Saves to `tailored/tailored_data_v1.yaml`.
**When Sean uses it:** Third step in the pipeline, after accepting a job.

---

### Script 04 — `04_generate_resume_intermediate.py`
**What it does:** Resume generation engine. Loads Sean's master career data (JSON) and skills (YAML), loads the tailored job data, and calls Grok with strict instructions: rewrite up to 4–6 bullets per role (prioritizing job relevance), write a professional summary weaving in job keywords, sort skills with job-relevant ones first, keep ALL experience entries and projects. Outputs a structured JSON file to `generated/resume_intermediate_v1.json`.
**When Sean uses it:** Fourth step. The JSON can be manually edited before rendering if needed.

---

### Script 05 — `05_render_resume.py`
**What it does:** Resume renderer. Reads the intermediate JSON and produces two outputs: (1) a Markdown preview (`.md`) for quick review, and (2) a Word document (`.docx`) using `python-docx` with proper formatting, hyperlinks for LinkedIn/GitHub, bullet lists, Arial font, tight margins. Has two modes: `--trim` (top 5 roles only) or full (all roles). `--all` generates both. Also supports PDF via `docx2pdf`.
**When Sean uses it:** Fifth step. He reviews the `.md` preview, then uses the `.docx` for submission.

---

### Script 06 — `06_company_research.py`
**What it does:** Company intelligence. Asks Grok to classify the company as `agency` (staffing firm) or `enterprise` (product/SaaS company). If enterprise, fetches a 1–2 paragraph research summary about the company's mission, values, and culture. Saves to `research/company_research.yaml`.
**When Sean uses it:** Sixth step, before generating the cover letter. Agencies get skipped; enterprises get researched so the cover letter can mention specific values.

---

### Script 07 — `07_generate_cover_intermediate.py`
**What it does:** Cover letter generation engine. Loads master career data, skills, tailored job data, and company research (if enterprise). Calls Grok to produce a structured JSON with `header`, `salutation`, `intro`, `body` (2–3 paragraphs), `conclusion`, `sign_off`. Rules: 250–400 words, use only facts from master data, weave in job keywords naturally, incorporate company research for enterprise roles, always use the exact current date. Saves to `generated/cover_intermediate_v1.json`.
**When Sean uses it:** Seventh step. Can also be tweaked before rendering.

---

### Script 08 — `08_render_cover_letter.py`
**What it does:** Cover letter renderer. Reads the cover intermediate JSON and renders it to both Markdown preview and Word document. Formats as a proper business letter with left-aligned contact header, right-aligned employer address, proper paragraph structure, Arial 11pt font.
**When Sean uses it:** Eighth step. The `.docx` is the submission-ready letter.

---

### Script 09 — `09_update_application_status.py`
**What it does:** Application tracker. Subcommands: `apply` (records application date, method like "LinkedIn" or "Company Website", notes, optional follow-up date), `status` (updates with values like "Interview Scheduled", "Offer", "Rejected"), `show` (displays current status + full history), `list-pending` (lists all jobs with upcoming follow-up dates).
**When Sean uses it:** Right after submitting an application, and whenever the status changes (interview invite, rejection, etc.).

---

### Script 10 — `10_auto_pipeline.py`
**What it does:** The "easy button." Orchestrates scripts 00–09 in sequence by calling each as a subprocess. Captures the UUID from script 01's output and threads it through all subsequent steps. Also supports resuming from an existing UUID (skipping intake/scoring). Enforces UTF-8 for Windows compatibility.
**When Sean uses it:** When he wants to go from intake to submitted application in one command: `python scripts/10_auto_pipeline.py intake/job.md --method "LinkedIn"`.

---

### Script 11 — `11_search_jobs.py`
**What it does:** Keyword search across all jobs. Loads metadata + raw description for every job folder, does case-insensitive substring matching across company, role, status, and full description text. Outputs a formatted table (uses `rich` library if available). Reports which field matched.
**When Sean uses it:** Ad-hoc lookup — "show me all jobs mentioning Snowflake" or "find jobs at Google."

---

### Script 12 — `12_update_job.py`
**What it does:** Fuzzy search + update tool. More powerful than script 09 — finds jobs by company name, role, status, or UUID without needing the exact UUID. Supports AND/OR logic in queries. Prioritizes by match score (UUID match = 10pts, company/role = 3pts). Can update status, add notes, set follow-up dates, backdate events, and print full history trails. Interactive prompt if multiple matches found.
**When Sean uses it:** Whenever he gets an update (interview invite, rejection email) and wants to record it quickly by company name instead of UUID.

---

## 4. DATA & DATABASE

### What Data is Stored

**No traditional database.** Everything is files on disk — YAML, JSON, Markdown, and binary (FAISS index, DOCX).

### How It Is Structured

**Per-job data** (`data/jobs/NNNNN_uuid8/`):
- `metadata.yaml` — single source of truth for a job's status, score, history, timestamps, company/role info
- `raw/raw_intake.md` — original job posting, unchanged
- `score/score_report_YYYYMMDD_HHMMSS.md` — Grok's scoring output in markdown
- `tailored/tailored_data_v1.yaml` — LLM-parsed structured job requirements
- `generated/resume_intermediate_v1.json` — LLM-tailored resume content
- `generated/resume_v1.docx` + `resume_v1_trimmed.docx` — ready-to-submit resumes
- `generated/cover_intermediate_v1.json` — LLM-generated cover letter content
- `generated/cover_letter_v1.docx` — ready-to-submit cover letter
- `research/company_research.yaml` — company classification + research text

**FAISS vector index** (`data/job_index/`):
- `faiss_job_descriptions.index` — binary FAISS flat inner-product index
- `jobs_metadata.yaml` — metadata list parallel to index rows (company, role, status, path)
- Embedding model: `all-MiniLM-L6-v2` (384-dimensional vectors, cosine similarity)

**Global index** (`data/job_index/jobs_metadata.yaml`):
- Currently shows `apply_date: N/A` for all jobs — this field is not being populated

### Where source_of_truth.json Fits In

`data/source_of_truth.json` is **Sean's master career profile** — the canonical record of everything about him. It contains:
- Personal info (name, contact, LinkedIn, GitHub, location, target roles)
- Professional summaries (short + long)
- Full work experience with highlights/bullets
- Education and certifications
- Skills with proficiency levels and years of experience
- Projects

However, the pipeline scripts **do not read `source_of_truth.json` directly.** They read the derived files in `data/master/`. The `profile_export.py` script converts `source_of_truth.json` → `master_career_data.json` + `master_career_data.yaml` + `skills.yaml`. This export must be re-run manually after any profile updates.

**Key data tension:** `source_of_truth.json` and `data/master/` can go out of sync if someone edits one but not the other. The pipeline will silently use stale data.

---

## 5. AI INTEGRATION

### Which AI Models Are Used

**Primary LLM:** xAI Grok — default model `grok-3`
**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` (local, no API cost)

### How They Are Called

The `GrokClient` class (`src/ai/grok_client.py`) wraps the **OpenAI Python SDK** pointed at xAI's API endpoint (`https://api.x.ai/v1`). This works because xAI's API is OpenAI-compatible. The API key is loaded from a `.env` file as `XAI_API_KEY`.

```python
# How every Grok call works under the hood:
self.client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
response = self.client.chat.completions.create(model="grok-3", messages=[...])
```

All scripts call `grok.chat(messages, temperature, max_tokens)`. The model can be overridden via `--model` CLI flag.

### What Each AI Call Generates

| Script | Grok Task | Output | Tokens |
|--------|-----------|--------|--------|
| 01 | Score job vs profile → match %, recommendation, strengths, gaps, advice | Structured markdown | ~1,200 |
| 03 | Parse job description → structured YAML with skills, requirements, ATS keywords | YAML document | ~4,000 |
| 04 | Rewrite resume bullets for job relevance, tailored summary, sorted skills | JSON resume object | ~8,192 |
| 06 | Classify company (agency/enterprise), generate company research | Plain text | ~520 |
| 07 | Generate cover letter sections grounded in career facts + company research | JSON cover object | ~1,500 |

**Embedding (local, no API):** `sentence-transformers` generates 384-dimensional vectors for FAISS indexing and duplicate detection.

---

## 6. CURRENT STATE

### What Is Working ✅

- **Full pipeline functional** — scripts 00 through 09 all execute successfully
- **23 jobs ingested** across multiple companies (Geico, Capital One, Anthropic, Google, CVS, Sephora, SCRIBD, AT&T, DTCC, Fisher Investments, etc.)
- **107 DOCX files generated** — every job has a tailored resume; 23 jobs have cover letters
- **FAISS duplicate detection working** — semantic similarity search operational
- **Status tracking working** — history with dates logged in `metadata.yaml` (e.g., Geico job 00004 shows: Applied 2026-02-06 → Rejected 2026-02-13 with "Email, they decided to move with other candidates")
- **Auto pipeline working** — single command runs full flow 00→09
- **Scripts 11 and 12 working** — keyword search and fuzzy-match update tools operational
- **Company research working** — enterprise vs. agency classification + culture research
- **Two resume formats** — Full (all roles) and Trimmed (top 5 roles)
- **Code style standards documented** — CodingStyle.md defines PEP 8 + strict typing + black + ruff

### What Is Broken or Incomplete ⚠️

1. **`apply_date: N/A` in FAISS index** — The index metadata always shows `apply_date: N/A`. The code reads `meta.get("application", {}).get("date", "N/A")` but the actual key in metadata.yaml is `applied_date`, not `date`. Minor bug.

2. **Auto pipeline skips the human decision gate** — `10_auto_pipeline.py` auto-accepts every job (Step 02 runs with `--accept --reason "Auto-accepted by pipeline"`). This means Sean gets documents generated for jobs he hasn't actually decided to pursue. There's no pause for human review of the score before committing.

3. **source_of_truth.json sync** — `profile_export.py` must be manually run to keep `data/master/` in sync with `source_of_truth.json`. No automation, no guard, no warning if out of sync.

4. **`data/resumes/` and `data/vectorstore/`** — Both contain only `.gitkeep`. These were placeholder directories that were never utilized. Resumes go into per-job `generated/` folders instead.

5. **`docs/` folder is empty** — The user guide mentions `docs/` paths but the actual guides live in `user_guide/v0/script_guides/`. Documentation references are inconsistent.

6. **No Streamlit UI** — The README mentions Streamlit as planned. Never built.

7. **No reporting/analytics** — No script to summarize pipeline metrics: jobs applied vs. rejected, avg score, which companies respond, skill gaps across rejections.

8. **No NLP conversational chat** — The vision document (`startingDocs/00016.solutionsForward.md`) describes a `chat_with_data.py` script for natural language queries like "What's the status on that Google role?" — never built.

9. **No automatic website sync** — GitHub Pages resume was a planned feature. Not built.

10. **No interview prep generation** — Planned but not built.

11. **`data/vectorstore/` never used** — The README mentioned Chroma/FAISS but the codebase uses only FAISS in `data/job_index/`. The `vectorstore/` placeholder is orphaned.

12. **Job 00001 role shows "Unknown Role"** — The role extraction from the filename for the first job failed (no role segment in the filename pattern).

### What Is the Biggest Limitation Right Now

**The human is removed from the most critical decision point.** The auto pipeline auto-accepts every job it scores, meaning tailored resumes and cover letters get generated for jobs Sean may never apply to. This burns API tokens and dilutes the value. The ideal design would pause after Step 01 (show the score), let Sean decide, and only continue if he confirms. This is the single change that would most improve the system's real-world usefulness.

The **second biggest limitation** is the lack of a natural language interface. Currently Sean must know the UUID (or use fuzzy search) to interact with any job record. A simple "chat with my data" layer — even just a Python REPL that parses queries like "show me all ACCEPTED jobs" — would make the system dramatically more usable as a daily tool.

---

## 7. DEPENDENCIES

### APIs Used

| Service | Purpose | Cost Model |
|---------|---------|------------|
| xAI Grok API (api.x.ai) | All LLM tasks (scoring, tailoring, resume gen, cover gen, research) | Pay-per-token (default: grok-3) |

**Estimated API cost per job application (rough):** ~16,000–20,000 tokens input + ~14,000 tokens output across all 5 Grok calls = roughly $0.20–0.40 per job at current xAI pricing.

### External Services

- **GitHub** — Public repository for version control and code hosting
- **GitHub Pages** — Sean's personal website (planned integration, not yet active)

### Local Dependencies (No API cost)

| Library | Version | Purpose |
|---------|---------|---------|
| openai | 2.16.0 | Grok API client (OpenAI-compatible) |
| sentence-transformers | 5.2.2 | Local embeddings for FAISS |
| faiss-cpu | 1.13.2 | Vector similarity search (duplicate detection) |
| python-docx | 1.2.0 | Resume and cover letter DOCX rendering |
| docx2pdf | 0.1.8 | Optional PDF conversion |
| PyYAML | 6.0.3 | All data storage/reading |
| numpy | 2.4.2 | Vector math for FAISS |
| python-dotenv | 1.2.1 | API key loading from `.env` |
| rich | (optional) | Pretty terminal tables in scripts 11 & 12 |
| torch | 2.10.0 | Required by sentence-transformers |
| scikit-learn | 1.8.0 | Available, not currently used in pipeline |
| black, ruff, isort, mypy | various | Code quality tools |
| jupyterlab | 4.5.3 | Exploration notebooks |

### Cost Structure Summary

- **AI costs:** Pay-per-use, Grok API only. No OpenAI costs.
- **Compute:** Entirely local (Windows 11, Python 3.12, CPU-only FAISS)
- **Storage:** Local disk only. No cloud storage.
- **Infrastructure cost:** $0 beyond API fees.

---

## 8. VISION & GAPS

### What Sean Was Trying to Build

The original vision (captured in `startingDocs/` and `Teachables/`) is a **"second brain for job searching"** — an autonomous, RAG-powered personal assistant that:

1. **Ingests and scores** jobs automatically (built ✅)
2. **Generates tailored documents** (resume + cover) for each job (built ✅)
3. **Tracks the full lifecycle** — applied → interview → offer/rejection (built ✅)
4. **Searches intelligently** — "show me data engineering jobs I applied to last month" (partially built — keyword search ✅, semantic/NLP search ❌)
5. **Chats with your own data** — conversational interface to query and update records (not built ❌)
6. **Prevents duplicate effort** — semantic duplicate detection (built ✅)
7. **Learns from rejections** — report on which skills are missing across rejected jobs (not built ❌)
8. **Keeps resume always current** — auto-sync to GitHub Pages website (not built ❌)
9. **Scales to full pipeline** — from job discovery to offer acceptance, all tracked (partial ✅)

### What Is Missing to Complete That Vision

**Priority 1 — Immediately Useful:**
- **Human gate in auto pipeline** — pause after scoring, let Sean approve before generating documents
- **Simple reporting dashboard** — even a CLI script that prints "23 applied, 3 interviews, 20 rejections, avg score 78%"
- **Fix `apply_date` bug** in FAISS metadata

**Priority 2 — Medium Term:**
- **Natural language query layer** — a `chat_with_data.py` that understands "what's the status on the Google job?" using the existing FAISS index + Grok
- **source_of_truth.json auto-export** — run `profile_export.py` automatically whenever `source_of_truth.json` changes
- **Skills gap analysis** — after N rejections, analyze what skills consistently appear in job requirements but not in Sean's profile

**Priority 3 — Full Vision:**
- **Streamlit web UI** — point-and-click interface instead of CLI commands
- **Email integration** — auto-detect rejection/interview emails and update job status
- **GitHub Pages sync** — auto-update Sean's online resume when he accepts a job
- **Web scraping** — paste a URL instead of copying the job description manually
- **Interview prep generator** — given a job and company, generate likely interview questions and suggested answers from Sean's actual experience

### Technical Debt to Address

1. Consolidate `source_of_truth.json` ↔ `master_career_data.*` duplication — the pipeline should read directly from `source_of_truth.json` without a manual export step
2. Add field mapping fix for `apply_date` in `build_job_index.py` (use `applied_date`, not `date`)
3. Add a `--pause-for-review` flag to `10_auto_pipeline.py` so auto mode can optionally wait for human approval between Step 01 and Step 02
4. Remove orphaned directories: `data/resumes/`, `data/vectorstore/`
5. Unify the documentation: guides in `user_guide/v0/` reference `docs/` paths that don't exist

---

## QUICK REFERENCE — Command Cheat Sheet

```bash
# NEW JOB: Full automated pipeline
python scripts/10_auto_pipeline.py intake/job.md --method "LinkedIn"

# NEW JOB: Step by step
python scripts/00_check_applied_before.py intake/job.md
python scripts/01_score_job.py intake/job.md
python scripts/02_decide_job.py --uuid <uuid8> --accept --reason "Good fit"
python scripts/03_tailor_job_data.py --uuid <uuid8>
python scripts/04_generate_resume_intermediate.py --uuid <uuid8>
python scripts/05_render_resume.py --uuid <uuid8> --all
python scripts/06_company_research.py --uuid <uuid8>
python scripts/07_generate_cover_intermediate.py --uuid <uuid8>
python scripts/08_render_cover_letter.py --uuid <uuid8>
python scripts/09_update_application_status.py --uuid <uuid8> apply --method "LinkedIn"

# UPDATE STATUS
python scripts/12_update_job.py CVS --status "INTERVIEW" --notes "Phone screen Feb 28"
python scripts/12_update_job.py Geico --history

# SEARCH
python scripts/11_search_jobs.py "Snowflake"
python scripts/12_update_job.py "Data Engineer" --search-only

# REBUILD FAISS INDEX
python scripts/utils/build_job_index.py --rebuild

# EXPORT PROFILE (after editing source_of_truth.json)
python scripts/profile_export.py
```

---

## NUMBERS AT A GLANCE (as of 2026-02-26)

| Metric | Value |
|--------|-------|
| Total jobs in system | 23 |
| DOCX files generated | 107 |
| Cover letters | 23 |
| Companies | Geico, Capital One, CVS, AT&T, Anthropic, Google, Sephora, SCRIBD, DTCC, Fisher Investments, ClickUp, Hershey, PostScript, RTX, Stefanini, AgileEngine, Oden Technologies, Collective Health, Hartford, DBT Labs, Qode |
| AI model | xAI Grok-3 (default) |
| Embedding model | all-MiniLM-L6-v2 (local) |
| Python version | 3.12 |
| Platform | Windows 11 Pro |
| Repo status | Active, ~5 commits/week |

---

*This document was generated by reading every script, data file, and documentation file in the repository. It represents the complete state of the project as of the analysis date.*
