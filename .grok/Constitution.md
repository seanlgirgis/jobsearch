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
- Ethical: Inclusive tools; no unfair bias; respect privacy (no secrets/API keys in repo).
- Model Preference: xAI/Grok API primary (leverage credits), fallbacks only if required.

## Workflow
- **v0 Pipeline**: Setup profile → Intake job → **Auto Pipeline** (Score → Decide → Tailor → Resume → Research → Cover → Render → Apply).
- **Numbering/Reference System**: Prefix-based IDs for traceability (e.g., 100.001 for user stories, 200.001 for requirements). Format: XXX.YYY-ZZZ (category.subcategory-item).
- **Development Cycle**: User story → Requirements → Design (Specs/) → Implementation (scripts/) → Test/Run → Document (Teachables/ or decisions.md).
- **Memory Management**: Proactive updates to decisions.md, rules.md, Teachables/ for all key events (e.g., script creation, job processing).
- **Teaching Moments**: Capture concepts/patterns in Teachables/NNNNN-Short-Title.md – automatic when relevant.
- **UI/Frontend**: Start with Streamlit for prototypes; no complex auth/multi-user.

## Standards
- **Coding Style**: Follow CodingStyle.md (PEP8, type hints, docstrings, etc.).
- **Windows Compatibility**: Enforce `PYTHONUTF8=1` in subprocesses; use `pathlib` for all file paths.
- **Configuration**: Centralize in config.py or settings.py (use Pydantic for validation).
- **Tools/Libs**: LangChain LCEL for RAG chains; FAISS for vectors; sentence-transformers for embeddings.
- **Storage**: Local JSON/YAML for MVP; upgrade to DB (e.g., SQLite/TinyDB) as needed.
- **Testing**: Manual CLI tests in POC; add unit tests in v1.

## How to Update This Constitution
- Propose changes in chat responses (full markdown block ready for copy-paste).
- Commit after user confirmation.
- Date all major updates at the bottom.

Last updated: 2026-02-06