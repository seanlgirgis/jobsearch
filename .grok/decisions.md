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
- **2026-02-05 – Tailor Job Data Phase Added**: scripts/03_tailor_job_data.py committed. Uses LLM for structured YAML output, regex fallback.
- **2026-02-05 – Resume Intermediate Phase Added**: scripts/04_generate_resume_intermediate.py committed. Tailors JSON resume structure bound to master.
- **2026-02-05 – Resume Render Phase Added**: scripts/05_render_resume.py committed. Outputs DOCX/MD from JSON, with trim mode.
- **2026-02-05 – Cover Letter Intermediate Phase Added**: scripts/06_generate_cover_intermediate.py committed. Agency vs enterprise classification, research fetch.
- **2026-02-05 – Cover Letter Render Phase Added**: scripts/07_render_cover_letter.py committed. DOCX/MD from JSON.
- **2026-02-05 – Application Status Tracking Phase Added**: scripts/08_update_application_status.py committed. Updates metadata.yaml with apply/status/show/list-pending.
- **2026-02-05 – README Updated**: Reflected all phases 1-8 and guides in README.md.

Last updated: 2026-02-05

# Project Constitution – Guiding Framework for JobSearch

This is the high-level "constitution" for the JobSearch project: a RAG-based pipeline for job hunting, resume/cover letter tailoring, and evolving toward a "second brain" system. All code, communications, and decisions stay public in https://github.com/seanlgirgis/jobsearch.git. This is a living document – update via proposals in chats or PRs.

## Vision
- Build a modular RAG architecture using xAI/Grok models for job search, resume/cover letter generation, website updates, data storage, and tracking.
- Start with POC scripts (v0: intake, score, decision, tailor, generate).
- Evolve to full app (v1+: Streamlit UI, persistent DB, agents for interview prep).
- Long-term: Personal "second brain" (knowledge graph, notes, applications tracking) – ethical, bias-free, user-centric.

## Core Principles
- Public-first: Everything in GitHub – issues for stories, PRs for code, docs for designs.
- Modular & Reusable: Decoupled components, single responsibility, composition over inheritance.
- Iterative & MVP-focused: Fast prototypes, end-to-end flows first, add complexity only when needed.
- Ethical: Inclusive tools; no unfair bias; respect privacy (no secrets/API keys).

## Workflow
- **v0 Pipeline**: Setup profile → Intake job → Score → Decide → Tailor job data → Generate resume intermediate → Render resume → Generate cover intermediate → Render cover → Update application status.
- **User Story Format**: As a [user], I want [feature] so that [benefit]. Acceptance criteria: [list].
- **Requirements IDs**: Prefix R- (e.g., R-200.001 for stories, 200.001 for requirements). Format: XXX.YYY-ZZZ (category.subcategory-item).
- **Development Cycle**: User story → Requirements → Design (Specs/) → Implementation (scripts/) → Test/Run → Document (Teachables/ or decisions.md).
- **UI/Frontend**: Start with Streamlit for prototypes; no complex auth/multi-user.

## Standards
- **Coding Style**: Follow CodingStyle.md (PEP8, type hints, docstrings, etc.).
- **Configuration**: Centralize in config.py or settings.py (use Pydantic for validation).
- **Tools/Libs**: LangChain LCEL for RAG chains; FAISS for vectors; sentence-transformers for embeddings.
- **Storage**: Local JSON/YAML for MVP; upgrade to DB (e.g., SQLite/TinyDB) as needed.
- **Testing**: Manual CLI tests in POC; add unit tests in v1.

## How to Update This Constitution
- Propose changes in chat responses (full markdown block ready for copy-paste).
- Commit after user confirmation.
- Date all major updates at the bottom.

Last updated: 2026-02-05