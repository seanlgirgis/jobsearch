## 2026-02-04 – Initial Setup & Core Choices
- **Project Goal**: Build incremental RAG pipeline for job hunting → semantic search over jobs/applications, tailored resume/cover letter generation, job data storage. Long-term: evolve toward full "second brain" (website updates, interview prep, tracking, etc.).
- **Primary LLM**: xAI Grok API (leverage free $150/mo credits where possible), with OpenAI-compatible fallbacks only if needed.
- **Embeddings (MVP)**: sentence-transformers/all-MiniLM-L6-v2 (fast, lightweight 384-dim, solid baseline for semantic similarity on job descriptions/resumes).
- **Vector Store (MVP)**: FAISS (flat/L2 index first — simple, fast on CPU, no server needed).
- **RAG Framework**: LangChain LCEL chains to start (quick to prototype, explicit control over retrieval + generation). LlamaIndex as potential alternative if query engine patterns prove cleaner later.
- **Storage (MVP)**: Local JSON files in `/data/` (jobs, resumes, user profile, applications). TinyDB if we need light querying before real DB pain hits.
- **UI (First Prototype)**: Streamlit single-page app with tabs/sections (e.g., Upload Resume → Add Jobs → Search & Generate Tailored Docs). No auth/multi-user — personal tool only.
- **Development Style**: Fastest practical path → MVP that works end-to-end → only add complexity when current version hits clear limitations. Honest feedback on over-engineering. Code/comms stay public in repo.
- **Project Memory**: This `decisions.md` file in root (or `.grok/`) — we maintain jointly: user adds my suggested blocks after agreements.

## Ideas Parked / To Revisit Later
- Switch to better embeddings (bge-large-en-v1.5, voyage-3, etc.) once MVP retrieval quality is measurable and lacking.
- Hybrid search (BM25 + semantic).
- Reranker step (cross-encoder or LLM-based).
- Persistent vector DB (Chroma, pgvector, Weaviate) if FAISS indexing/search slows noticeably >1–2k docs.
- Auto-tracking applications (email parsing, browser extension, LinkedIn API — ethical/legal checks first).
- Multi-agent flows or advanced routing in RAG.

## Open Questions / Validation Needed
- Exact job listing schema (fields: title, company, url, description, posting_date, location, salary?, tags?, etc.)
- User career profile structure (skills, experience bullets, preferred keywords, target roles/companies)
- How to handle resume versions / templates (Markdown? DOCX? Both?)
- Rate limiting / cost monitoring for Grok API calls during dev.

(End of initial version – 2026-02-04)


## 2026-02-04 – Job Data Storage Choice (MVP)
- **Primary**: Local JSON files in `/data/jobs/`
  - Per-job files: `/data/jobs/job_{job_id}.json` (recommended for easy management)
  - Optional single `/data/all_jobs.json` if fewer files preferred
- **Schema fields** (initial): job_id, title, company, location, url, posting_date, scrape_date, description_raw, description_clean, keywords_extracted (list), salary, status, notes, application_date, resume_version_used, tags (list)
- **Light querying**: Start with Python list comprehensions / pandas if needed; introduce TinyDB when filtering gets annoying
- **Future triggers to upgrade**: >1–2k jobs, complex metadata filters, concurrency needs → TinyDB → Chroma/pgvector

# Project Decisions & Agreements
Personal RAG-powered Job Application Assistant  
(Append-only log — add new dated sections at the top when we make/revise choices)


## 2026-02-04 – Vectorization & Future Data Store Evolution
- **Short-term (MVP)**: Stick with JSON files + FAISS as decided — no vector DB yet.
- **Expected future move**: Yes — will migrate to a proper vector database (likely Chroma first) for combined semantic + metadata retrieval once we hit scale (~500+ jobs), complex filters, or noticeable retrieval slowdowns.
- **Triggers to upgrade**: Slow search/indexing, need for hybrid filtering (e.g., location + date + semantic similarity), frequent updates/deletes, advanced RAG patterns.
- **Planned progression**: JSON/FAISS → TinyDB (metadata help) → Chroma (local vector DB) → pgvector/Weaviate if full relational + vector power needed.

## 2026-02-XX – Resume & Cover Letter Generation MVP Choices

* **Core Principle** — Do **not** just copy a static resume.md from seanlgirgis.github.io. Instead, maintain a clean **base_resume.md** (or equivalent structured source) in this repo and **always generate job-specific versions** via RAG-driven customization.
* **Output Formats (MVP)**:
  - Markdown (.md) — primary editable/source format; easy to diff, store, preview on GitHub, and feed back into RAG loops.
  - DOCX (.docx) — primary submission/ATS-friendly format; allows precise styling control (fonts, margins, headings, tables) to match the clean aesthetic of seanlgirgis.github.io.
  - PDF — deferred / on-demand only (user can export from DOCX or use Pandoc one-liner later; no need to build native PDF rendering into MVP to avoid complexity).
* **Why MD + DOCX only for now**:
  - MD: Matches original source style, perfect for version control and RAG input/output.
  - DOCX: Better ATS compatibility than PDF in many cases; python-docx is lightweight, pure-Python, no external deps like WeasyPrint/Pandoc for core generation.
  - Reduces Behemoth complexity — we extract formatting logic/style rules, not the full multi-format pipeline.
* **Generation Flow (high-level)**:
  1. Start from base_resume.md (copy/structure from seanlgirgis.github.io resume.md, but store here as editable base).
  2. RAG retrieves relevant job data + user profile/experience chunks.
  3. LLM (Grok) generates tailored content: summary rephrase, bullet optimizations, skill highlighting, keyword insertion.
  4. Apply changes to structured MD representation.
  5. Render final MD.
  6. Convert structured content to DOCX using python-docx with predefined style rules mimicking website (sans-serif 11–12pt body, bold uppercase headings, indented bullets, inline contact, etc.).
  7. Same pipeline for cover letters (separate base_cover_letter.md template: greeting → intro para → 2–3 body paras → closing).
* **Style Matching**:
  - Pull typography/layout cues from seanlgirgis.github.io: clean sans-serif, high contrast, uppercase bold section headers, generous whitespace, bullet hierarchy, optional skills table/matrix.
  - Hardcode defaults in a styles/config file; allow minor overrides per generation if needed.
* **Repo Placement**:
  - Base templates: data/base_resume.md, data/base_cover_letter.md
  - Generator module: src/resume_generator/ (with generate.py, styles.py, md_parser.py, docx_renderer.py, etc.)
  - Outputs go to: data/generated/{job_id}/ or applications/{app_id}/ (with links/notes stored in job JSON)
* **Future Triggers to Expand**:
  - User demand for native PDF → add Pandoc integration.
  - Need for LaTeX/Word templates → extend renderer.
  - Bulk generation or versioning → add resume_version field in application tracking.

This closes the open question on resume handling and sets the foundation for the next coding steps.

## 2025-XX-XX – Master profile & structured data

- Primary human-readable source: data/master/master_profile.md
- Structured full career data: data/master/master_career_data.json
- Granular skills inventory: data/master/skills.json
- Decision: Keep markdown as editable master; JSON(s) for RAG / programmatic use
- All future resume/cover-letter/job-match generations should reference these files

## 2026-XX-XX   Core modules status & responsibilities

### src/loaders/master_profile.py
- **Purpose** — central place for loading all master data (yaml + md fallback)
- **Main class** — `MasterProfileLoader`
- **Important methods**
  - `get_personal_info()`
  - `get_summary()` / `get_short_summary()`
  - `get_recent_experience(n=3)`
  - `get_top_skills(n=10, min_years=...)`
  - `get_skill_names(...)`
- **Status** — working + smoke test passes
- **Test command** — `python -m src.loaders.master_profile`

### src/ai/grok_client.py
- **Purpose** — clean wrapper around xAI Grok API (using openai-compatible client)
- **Main class** — `GrokClient`
- **Important methods**
  - `chat(messages, temperature=..., max_tokens=...)`
  - `generate_tailored_summary(job_description, master_summary)`
- **Status** — working + smoke test passes (real API response)
- **Test command** — `python -m src.ai.grok_client`

### Current decision / convention
- We use **OpenAI compatible client** for Grok (not native xai-sdk)
- Default model right now → `grok-3` (can be changed in constructor)
- All important modules should have small `__main__` smoke test

## 2026-02-04   POC Phase Kickoff
- Agreed to start with hands-on POC using real job desc → step-by-step tailoring → then formalize code/specs.
- Modules ready: MasterProfileLoader (data ingestion), GrokClient (LLM calls).
- Created Specs/ folder for formal designs post-POC.
- Next: Wait for user-provided job desc to begin interactive POC.





