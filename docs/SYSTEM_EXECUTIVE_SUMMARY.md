# JobSearch Pipeline: Executive Exhaustive Summary
*Detailed Architecture, AI Integration, and Directory Structure*

---

## 1. Executive Overview

This system is an **autonomous, AI-powered job application engine**. It orchestrates the entire lifecycle of a job application—from discovering a job description to generating tailored resumes and cover letters, avoiding duplicate applications, and tracking the application status.

The system relies on a hybrid AI architecture:
- **Local HuggingFace Models + FAISS** for semantic duplicate detection (free, local, privacy-first).
- **xAI's Grok API** for heavy NLP lifting: scoring applications, tailoring resumes, and writing cover letters.

Instead of a traditional relational database, the system uses a **file-system-based architecture** (Markdown, YAML, JSON, and DOCX) to persist all data.

---

## 2. AI Integrations: What Uses xAI vs. HuggingFace?

The system strategically splits its AI workloads to optimize for cost, privacy, and speed.

### HuggingFace & FAISS (Local / No Cost)
***Used strictly for Duplicate Search and Retrieval Augmented Generation (RAG) Indexing.***

- **The Model:** Uses local `sentence-transformers/all-MiniLM-L6-v2` (a popular HuggingFace model) to convert job descriptions into 384-dimensional vector embeddings.
- **How we search for duplicates (Script 00):** Whenever a new job is dropped into the system, the text is embedded using the HuggingFace model. This vector is then queried against a **FAISS (Facebook AI Similarity Search) Binary Index** located at `data/job_index/faiss_job_descriptions.index`. 
- **The Threshold:** If the FAISS cosine-similarity search finds a past job with a similarity score of $\ge$ 0.82, the system flags the new job as a duplicate and halts. This ensures you do not accidentally re-apply to essentially the same role posted under different URLs.

### xAI (Grok API)
***Used for all generative and reasoning tasks requiring LLM intelligence.***

The Grok API (`grok-3`) is engaged during the active pipeline to evaluate, extract, and write content:
1. **Scoring (Script 01):** Reads your master profile and compares it to the job description to output a fit score and recommendation (Proceed/Hold/Skip).
2. **Data Extraction (Script 03):** Parses raw markdown postings into structured YAML (extractingATS keywords, skills, requirements).
3. **Resume Generation (Script 04):** Rewrites your resume bullets to favor the required ATS keywords and experience.
4. **Company Research (Script 06):** Classifies companies as agency vs. enterprise and fetches core company values.
5. **Cover Letter Generation (Script 07):** Writes highly tailored 3-paragraph cover letters grounding your historical data with the newly researched company values.

---

## 3. The Pipeline Jobs (Scripts) & How They Work

The system is powered by 13 discrete Python scripts in `/scripts/`, executed either individually or orchestrated automatically via `10_auto_pipeline.py`.

### Phase 1: Intake & Scoring
- **`00_check_applied_before.py`**: The gatekeeper. Embeds the new raw markdown using HuggingFace `all-MiniLM-L6-v2` and checks FAISS for duplicates. If a duplicate is found, it terminates the pipeline.
- **`01_score_job.py`**: The evaluator. Calls **xAI** to score the job against your master profile. It sets up the new job's directory in `data/jobs/`, moves the intake markdown into `raw/`, and generates a `score_report.md`.
- **`02_decide_job.py`**: The manual gate. Allows you to flag the job as `--accept`, `--reject`, or `--hold`. If accepted, it triggers a background FAISS index rebuild to add this new job to the duplicate-detection ledger.

### Phase 2: Tailoring & Extraction
- **`03_tailor_job_data.py`**: The structurer. Sends the raw job to **xAI** to cleanly parse into a YAML file containing extracted requirements, must-have skills, nice-to-have skills, and ATS keywords.

### Phase 3: Resume Generation
- **`04_generate_resume_intermediate.py`**: The drafter. Feeds your master career JSON and the tailored job YAML into **xAI**. Grok rewrites and reorders your resume bullets, sorting job-relevant skills to the top. Outputs a structural JSON file.
- **`05_render_resume.py`**: The publisher. pure Python (no AI). Uses `python-docx` to render the intermediate JSON into polished, strictly formatted Word documents (`resume.docx` and `resume_trimmed.docx`).

### Phase 4: Cover Letter Generation
- **`06_company_research.py`**: The researcher. Calls **xAI** to figure out if the poster is a staffing agency or a real enterprise, and if enterprise, asks Grok to research their cultural values.
- **`07_generate_cover_intermediate.py`**: The composer. Pushes your career facts, tailored job keywords, and the company research to **xAI** to draft a cover letter JSON.
- **`08_render_cover_letter.py`**: The publisher. Converts the cover letter JSON into a polished `.docx` business letter.

### Phase 5: Tracking & Maintenance
- **`09_update_application_status.py`**: The tracker. Logs how you applied (e.g., LinkedIn) and updates the local job's `metadata.yaml` with timestamps.
- **`10_auto_pipeline.py`**: The orchestrator. Wraps scripts 00 through 09 into an automated "fire and forget" macro.
- **`11_search_jobs.py` & `12_update_job.py`**: The lookup tools. Allows you to fuzzy-search past applications and globally update applicant statuses (like adding an interview date).

---

## 4. Directory Structure: What Goes Where

Everything revolves around a "database as a file system" concept.

```text
jobsearch/
├── intake/                   ← (INBOX) You drop new job postings here as raw `.md` files.
│
├── data/
│   ├── source_of_truth.json  ← (MASTER) The absolute single source of truth for your career history.
│   │
│   ├── master/               ← (DERIVED) Read-only JSON/YAML exports of the source_of_truth. 
│   │                           Used by the AI pipeline to ground hallucinations.
│   │
│   ├── job_index/            ← (VECTOR RAG STORE) Where the HuggingFace/FAISS duplicate-checking index lives.
│   │   ├── faiss_job_descriptions.index  ← The binary array of 384-dimensional vectors.
│   │   └── jobs_metadata.yaml            ← Text ledger mapping the vectors to Job UUIDs.
│   │
│   └── jobs/                 ← (THE DATABASE) One folder per processed job.
│       └── 00001_cdb9a3fa/   ← Format: NNNNN_uuid8
          ├── metadata.yaml         ← The status, score, company, and history logs of this job.
          ├── raw/                  ← The original intake markdown file.
          ├── score/                ← The Grok evaluation markdown report.
          ├── tailored/             ← The Grok-extracted job keywords and requirements.
          ├── generated/            ← The final AI-generated JSONs and ready-to-submit DOCX files.
          └── research/             ← Company research files.
│
├── scripts/                  ← (THE ENGINE) All the executable Python pipeline jobs (00 to 12).
├── src/                      ← (LIBRARIES) Internal wrappers (e.g., grok_client.py, data loaders).
└── docs/                     ← (DOCUMENTATION) Where this summary and pipeline guides live.
```

---

## 5. Summary of Data Flow per Job

When a job `intake.md` is processed, its final state rests inside `data/jobs/<ID>/`. 
Its raw text is preserved forever in `/raw/`. Its extracted semantic features live in `/tailored/`. Its matching scores live in `/score/`, and the final artifacts are securely placed into `/generated/`. Concurrently, the script automatically updates `metadata.yaml` to track state changes natively locally. It finally injects mathematical representations of the job into `data/job_index/` via HuggingFace transformers, permanently immunizing your pipeline from ever generating duplicate applications to the same role.
