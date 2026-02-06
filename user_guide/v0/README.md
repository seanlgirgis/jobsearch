# JobSearch Pipeline (POC v0)

This project is a script-based pipeline for managing job searches: ingesting postings, scoring fit, tailoring resumes/cover letters, rendering documents, and tracking applications. It's designed to grow into a full "second brain" with RAG for job storage/search, AI-driven updates, and more.

- **Key Features**: LLM-powered (Grok/xAI) tailoring, structured data (YAML/JSON), versioned outputs, exclusion filters, status tracking.
- **Tech Stack**: Python 3, Grok API (via src/ai/grok_client.py), python-docx for rendering, YAML/JSON for data.
- **Dependencies**: `pip install pyyaml python-docx` (plus Grok API key setup).
- **Folders**:
  - `intake/`: Raw job postings (markdown).
  - `data/jobs/<uuid>/`: Per-job folders (raw/, tailored/, generated/, score/, metadata.yaml).
  - `data/master/`: Profile data (master_career_data.json, skills.yaml).

## Setup

1. Clone repo: `git clone https://github.com/seanlgirgis/jobsearch.git`
2. Install deps: `pip install -r requirements.txt` (add if needed: pyyaml, python-docx)
3. Configure Grok: Set API key in `src/ai/grok_client.py`
4. Run profile setup: `python scripts/profile_source_of_truth.py --profile_input <your_data.json>` (one-time)

## Final Pipeline Flow (v0 POC – Script-Based)

1. **Profile Setup** (One-time)  
   `python scripts/profile_source_of_truth.py --profile_input my_jobs.json`  
   → Unifies your history into `data/master/source_of_truth.json`.  
   *Guide*: [profile_source_of_truth.md](docs/profile_source_of_truth.md)

2. **Intake Job**  
   Drop raw job posting (markdown) into `intake/` or paste via script.

3. **Score Job** (optional)  
   `python scripts/01_score_job.py intake/job.md`  
   → Creates `data/jobs/<uuid>/` folder + `metadata.yaml` (status: PENDING).  
   *Guide*: [01_score_job.md](docs/01_score_job.md)

4. **Decide** (accept/reject/hold)  
   `python scripts/02_decide_job.py --uuid <uuid> --accept --reason "..."`  
   → Updates `metadata.yaml`.  
   *Guide*: [02_decide_job.md](docs/02_decide_job.md)

5. **Tailor Job Data** (recommended, but skippable)  
   `python scripts/03_tailor_job_data.py --uuid <uuid> [--version v1]`  
   → Creates `data/jobs/<uuid>/tailored/tailored_data_v1.yaml` (structured sections: responsibilities, requirements, skills, etc.).  
   → If skipped, intermediate uses raw job text (less precise tailoring).  
   *Guide*: [03_tailor_job_data.md](docs/03_tailor_job_data.md)

6. **Generate Resume Intermediate**  
   `python scripts/04_generate_resume_intermediate.py --uuid <uuid> --version v1`  
   → Uses tailored YAML (if exists) or raw job text → produces `resume_intermediate_v1.json`.  
   *Guide*: [04_generate_resume_intermediate.md](docs/04_generate_resume_intermediate.md)

7. **Review Intermediate**  
   Manually check/edit JSON (dates, facts, tone).

8. **Render Resume**  
   `python scripts/05_render_resume.py --uuid <uuid> --version v1 [--all]`  
   → Produces Markdown + DOCX (trimmed & full).  
   *Guide*: [05_render_resume.md](docs/05_render_resume.md)

9. **Generate Cover Intermediate**  
   `python scripts/06_generate_cover_intermediate.py --uuid <uuid> --version v1`  
   → Produces `cover_intermediate_v1.json` (tailored to company type: agency/generic vs enterprise/personalized).

10. **Render Cover Letter**  
    `python scripts/07_render_cover_letter.py --uuid <uuid> --version v1`  
    → Produces Markdown + DOCX cover letter.

11. **Update Application Status**  
    `python scripts/08_update_application_status.py --uuid <uuid> apply --method "LinkedIn" --notes "..."`  
    → Tracks status, history, follow-ups in `metadata.yaml`.  
    *Guide*: [08_update_application_status.md](docs/08_update_application_status.md)

## Documentation Guides

Detailed guides for each phase/script:

- [profile_source_of_truth.md](docs/profile_source_of_truth.md) - One-time profile unification.
- [01_score_job.md](docs/01_score_job.md) - Job scoring.
- [02_decide_job.md](docs/02_decide_job.md) - Decision making.
- [03_tailor_job_data.md](docs/03_tailor_job_data.md) - Job data structuring.
- [04_generate_resume_intermediate.md](docs/04_generate_resume_intermediate.md) - Resume JSON generation.
- [05_render_resume.md](docs/05_render_resume.md) - Resume rendering.
- [08_update_application_status.md](docs/08_update_application_status.md) - Application tracking.

## Future Extensions

- Cover letter generation (phases 06/07).
- Website auto-updates (e.g., GitHub Pages resume sync).
- RAG job store search (query past jobs via embeddings).
- Interview prep / follow-up emails (LLM-generated).

See [Constitution.md](.grok/Constitution.md), [rules.md](.grok/rules.md), and [decisions.md](.grok/decisions.md) for project principles.

Coding style: [CodingStyle.md](CodingStyle.md)