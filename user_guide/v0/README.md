# JobSearch Pipeline (POC v0)

This project is a script-based pipeline for managing job searches: ingesting postings, scoring fit, tailoring resumes/cover letters, rendering documents, and tracking applications. It's designed to grow into a full "second brain" with RAG for job storage/search, AI-driven updates, and more.

- **Key Features**: LLM-powered (Grok/xAI) tailoring, structured data (YAML/JSON), versioned outputs, exclusion filters, status tracking.
- **Tech Stack**: Python 3, Grok API (via `src/ai/grok_client.py`), `python-docx` for rendering, YAML/JSON for data.
- **Dependencies**: `pip install pyyaml python-docx` (plus Grok API key setup).
- **Folders**:
  - `intake/`: Raw job postings (markdown).
  - `data/jobs/<uuid>/`: Per-job folders (raw/, tailored/, generated/, score/, metadata.yaml).
  - `data/master/`: Profile data (master_career_data.json, skills.yaml, source_of_truth.json).

## Setup

1. **Clone repo**: `git clone https://github.com/seanlgirgis/jobsearch.git`
2. **Install deps**: `pip install -r requirements.txt` (add if needed: `pyyaml`, `python-docx`, `docx2pdf`)
3. **Configure Grok**: Set API key in `src/ai/grok_client.py`
4. **Run profile setup**: `python scripts/profile_source_of_truth.py --profile_input <your_data.json>` (one-time)

## Pipeline Scripts (01-10)

You can run these individually or use the **Auto Application** script (10).

1. **Score Job**
   `python scripts/01_score_job.py intake/job.md`
   → Analyzes job vs profile. Creates `data/jobs/<uuid>/` folder + `metadata.yaml`.

2. **Decide**
   `python scripts/02_decide_job.py --uuid <uuid> --accept`
   → Marks job as "ACCEPTED" to proceed with tailoring.

3. **Tailor Job Data**
   `python scripts/03_tailor_job_data.py --uuid <uuid>`
   → Extracts structured requirements/skills from the job description into `tailored_data.yaml`.

4. **Generate Resume Intermediate**
   `python scripts/04_generate_resume_intermediate.py --uuid <uuid>`
   → Maps master experience to job requirements to create the resume content structure (JSON).

5. **Render Resume**
   `python scripts/05_render_resume.py --uuid <uuid> --all`
   → Renders the JSON into Markdown and DOCX.
   → Generates **Full** (all history) and **Trimmed** (top 5 roles + summary) versions.

6. **Company Research**
   `python scripts/06_company_research.py --uuid <uuid>`
   → Classifies company (Agency vs Enterprise). Fetches culture/values research for Enterprises.

7. **Generate Cover Letter Intermediate**
   `python scripts/07_generate_cover_intermediate.py --uuid <uuid>`
   → Generates cover letter content (JSON) incorporating company research and specific job fits.

8. **Render Cover Letter**
   `python scripts/08_render_cover_letter.py --uuid <uuid>`
   → Renders cover letter JSON to DOCX/Markdown.

9. **Update Application Status**
   `python scripts/09_update_application_status.py --uuid <uuid> apply --method "LinkedIn"`
   → Logs application date, method, and notes in `metadata.yaml`.

---

### 🚀 Automation (The "Easy Button")

10. **Auto Pipeline**
    `python scripts/10_auto_pipeline.py intake/job.md`
    → **Runs Steps 01 through 09 automatically.**
    → Scores, accepts, tailors, generates all documents (resume/cover), and marks as applied.
    → *Arguments*: `--no-move`, `--model`, `--method`, `--notes`.

## Documentation Guides

Detailed guides for specific phases:

- [profile_source_of_truth.md](docs/profile_source_of_truth.md) - One-time profile unification.
- [01_score_job.md](docs/01_score_job.md)
- [02_decide_job.md](docs/02_decide_job.md)
- [03_tailor_job_data.md](docs/03_tailor_job_data.md)
- [04_generate_resume_intermediate.md](docs/04_generate_resume_intermediate.md)
- [05_render_resume.md](docs/05_render_resume.md)
- [06_company_research.md](docs/06_company_research.md)
- [07_generate_cover_intermediate.md](docs/07_generate_cover_intermediate.md)
- [08_update_application_status.md](docs/08_update_application_status.md) (Note: script is now 09, guide update pending)

## Future Extensions

- Website auto-updates (e.g., GitHub Pages resume sync).
- RAG job store search (query past jobs via embeddings).
- Interview prep / follow-up emails (LLM-generated).

See [Constitution.md](.grok/Constitution.md) for project principles.