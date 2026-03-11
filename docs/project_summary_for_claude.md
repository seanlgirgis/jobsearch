# JobSearch Project Summary for Claude

This document provides a complete, end-to-end summary of the JobSearch project. It is intended to give Claude complete context over the system's architecture, data flow, scripts, and environment setup.

## 1. Project Overview

The project is an AI-powered job application engine. It takes raw job postings and automates the process of checking for duplicates, scoring the job fit against a master career profile, tailoring a resume, researching the company, generating a custom cover letter, and tracking the application status. 

There is no traditional database. The system relies entirely on flat files (JSON, YAML, Markdown) and a local binary FAISS vector index.

## 2. Environment Setup (`env_setter.ps1`)

The environment is managed via a PowerShell script `env_setter.ps1` which activates the Virtual Environment and exports necessary environment variables. The script:
1. Activates the Python 3.12 virtual environment located at `C:\py_venv\JobSearch`.
2. Sets `PROJECT_ROOT` to the directory containing the script (`C:\jobsearch`).
3. Appends `src` to the `PYTHONPATH`.
4. Configures necessary storage paths mapping to folders within the project (`JOBS_DB_DIR`, `RESUMES_DIR`, `VECTOR_DB_PATH`).
5. Sets parameters for local embeddings (`sentence-transformers/all-MiniLM-L6-v2`) and designates `xai` (Grok) as the default LLM provider.
6. The user manually sets API keys in a `.env` file (like `XAI_API_KEY`).

To initialize the environment, the user runs:
```powershell
.\env_setter.ps1
```

## 3. Data Architecture (Inputs, Middle Storage, Outputs)

### Inputs
- **Job Postings:** Raw job descriptions stored as Markdown files in the `intake/` folder.
- **Master Profile:** The canonical source of truth for the user's career data is `data/source_of_truth.json`. However, scripts read derived exports located in `data/master/` (`master_career_data.json`, `master_career_data.yaml`, and `skills.yaml`).

### Middle Storage
Each job, once accepted, gets a uniquely generated UUID and its own folder under `data/jobs/NNNNN_uuid8/` containing:
- `metadata.yaml`: Single source of truth for the job's track record (status, score, history, dates, company info).
- `raw/raw_intake.md`: The original ingested job posting.
- `score/score_report_TIMESTAMP.md`: Grok's evaluation of the job against the master profile.
- `tailored/tailored_data_v1.yaml`: LLM-extracted structured YAML containing parsed job requirements, ATS keywords, and skills.
- `generated/resume_intermediate_v1.json`: Intermediate JSON containing the LLM-tailored resume content.
- `research/company_research.yaml`: If an enterprise job, contains LLM company culture research text.
- `generated/cover_intermediate_v1.json`: Intermediate JSON containing the LLM-generated cover letter content.
- `data/job_index/`: Contains the RAG vector index files: a binary FAISS index (`faiss_job_descriptions.index`) and its corresponding metadata (`jobs_metadata.yaml`).

### Outputs
- **Tailored Resumes:** `generated/resume_v1.docx` (full) and `resume_v1_trimmed.docx` (top 5 roles only), rendered using `python-docx`. Markdown previews of resumes are also generated.
- **Tailored Cover Letters:** `generated/cover_letter_v1.docx` rendered as a proper business document.

## 4. How We RAG into Grok

Retrieval-Augmented Generation (RAG) is utilized in two distinct manners across the pipeline:

### Semantic Duplicate Detection (Local vector search)
- Script `00_check_applied_before.py` embeds the incoming job description using a local `sentence-transformers/all-MiniLM-L6-v2` model.
- It calculates cosine similarity using the flat FAISS index over past indexed job descriptions. If the similarity is ≥ 0.82, it flags the job as a duplicate.

### Prompt-Based Generation (LLM RAG)
Scripts involving generation (`04` and `07`) ground the LLM by explicitly injecting multiple contexts directly into the system prompt.
1. The AI module lives in `src/ai/grok_client.py` where a `GrokClient` wrapper initializes the `openai` Python SDK targeting the `https://api.x.ai/v1` base URL.
2. The user's parsed career text (`data/master/`), the tailored job data (`tailored/tailored_data_v1.yaml`), and company research (if available) are collectively passed to the prompt.
3. Grok strict-parses this injected reality and only operates using real facts from the master data, actively incorporating extracted ATS keywords natively.

## 5. Pipeline Scripts Detailed Breakdown

There are 13 main scripts inside the `scripts/` directory simulating the pipeline flow.

- `00_check_applied_before.py`: Performs the initial semantic FAISS check against existing jobs to prevent duplicate applications.
- `01_score_job.py`: Reads the raw Markdown job in `intake/`, fetches metadata from the filename/front-matter, calls Grok to score the job, creates the structured job folder under `data/jobs/`, and saves the score report.
- `02_decide_job.py`: A decision gate that updates `metadata.yaml` with an `--accept`, `--hold`, or `--reject`. Accepting triggers the FAISS index rebuild utility so this job is indexed for future duplicate checks.
- `03_tailor_job_data.py`: Commands Grok to convert the raw job description into a structured YAML containing extracted requirements, nice-to-have skills, and ATS keywords.
- `04_generate_resume_intermediate.py`: Loads the master career JSON and the newly tailored job YAML. Calls Grok to rewrite bullets, write a summary, and rank skills. Outputs a structured `resume_intermediate_v1.json`.
- `05_render_resume.py`: Uses `python-docx` to read the intermediate JSON and render heavily stylized Word documents (`resume_v1.docx` and a trimmed variant).
- `06_company_research.py`: Classifies the company as an `agency` or `enterprise`. If enterprise, fetches research on company culture/values via Grok and saves to `research/company_research.yaml`.
- `07_generate_cover_intermediate.py`: Injects master career data, tailored job requirements, and company research into Grok to draft a targeted cover letter, outputting `cover_intermediate_v1.json`.
- `08_render_cover_letter.py`: Renders the intermediate cover letter JSON into a properly formatted `.docx`.
- `09_update_application_status.py`: Primary application tracker. Logs applied dates, methods, status changes (Interviews, Rejections), and populates `metadata.yaml`.
- `10_auto_pipeline.py`: The single-button orchestrator. Combines 00 through 09 as subprocesses in one pass. Bypasses the human decision gate (Step 02) entirely by auto-accepting.
- `11_search_jobs.py`: Ad-hoc substring search utility across all previous jobs' metadata and raw descriptions for simple querying (e.g. "Google").
- `12_update_job.py`: An advanced version of script 09 utilizing fuzzy search to locate jobs by parts of their names, capable of mass status updates and printing history trails.
