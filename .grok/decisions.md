# Decisions Log – Chronological Record of Key Choices

Dated entries for traceability. Grouped by month for readability as it grows.

## February 2026
- **2026-02-04 – Initial Setup & Core Choices**: Project goal: RAG pipeline for job hunting. Primary LLM: xAI/Grok. Embeddings: all-MiniLM-L6-v2. Vector store: FAISS. Framework: LangChain LCEL. Storage: Local JSON. UI: Streamlit MVP. Memory: This decisions.md.
- **2026-02-04 – POC Step B – Scoring Script v0.1 Success**: scripts/score_job.py created. First run on Collective Health job. Output: 85% match.
- **2026-02-04 – POC Step B – Full Automation Success**: score_job.py v0.2: Auto-creates data/jobs/<uuid>/. UUID example: 96b16121-8608-405d-9553-af86fdbf939c.
- **2026-02-04 – POC Progress – Job Accepted & Decision Script Working**: Job accepted (UUID 96b16121-8608-405d-9553-af86fdbf939c). scripts/job_decision.py committed. Status: ACCEPTED. Next: tailor_job_data.py.
- **2026-02-05 – Source of Truth Unified**: Merged profile sources into data/source_of_truth.json. Archived originals to data/archive/. Prioritized recency.
- **2026-02-05 – Legacy Export Script Added**: profile_export.py to regenerate data/master/ from source_of_truth.json. Ensures v0 script compatibility.
- **2026-02-05 – Scoring Script Updated for File Preservation**: Changed to copy/move intake files with original names. Added JOB_ROOT definition.

Last updated: 2026-02-05