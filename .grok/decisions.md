# Project Decisions & Agreements
Personal RAG-powered Job Application Assistant  
(Append-only log — add new dated sections at the top when we make/revise choices)

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