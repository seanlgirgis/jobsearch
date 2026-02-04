# JobSearch – Personal RAG-powered Job Application Assistant

Personal pipeline / second brain for job hunting:

- Store & manage job listings
- Semantic search over past applications/jobs
- Auto-generate tailored resumes + cover letters
- Eventually: website updates, interview prep, tracking

Goal: RAG architecture using local embeddings + LLM calls (xAI/Grok API preferred, fallbacks possible)

## Status (early 2026)

- Setting up base environment & structure
- Next: data models, job ingestion, basic RAG retrieval, resume/cover generation

## Tech stack (planned)

- Python 3.12
- LangChain (or LlamaIndex) for RAG
- Sentence-Transformers / local embeddings
- FAISS / Chroma for vector store
- xAI Grok API (or OpenAI-compatible endpoint)
- Streamlit for quick UI
- Local JSON/TinyDB for jobs/resumes

## Quick Start

1. Python at `C:\pyver\py312`
2. Create & activate venv:
   ```powershell
   C:\pyver\py312\python -m venv C:\py_venv\JobSearch
   .\C:\py_venv\JobSearch\env_setter.ps1   # or manual activation