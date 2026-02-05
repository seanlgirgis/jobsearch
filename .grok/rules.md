# Project Rules – Actionable Guidelines

These are specific, enforceable rules for coding, responses, and project management. See constitution.md for high-level principles; decisions.md for log.

## Coding Rules
- All code stays public in repo – no secrets/API keys/large binaries.
- Modular/OOP: Classes decoupled, no duplication; favor shared utilities (e.g., one LLM client, one vector store instance).
- Central config: Import constants/settings from config.py (e.g., paths, model names).
- Iterative commits: Small, descriptive messages (e.g., "Add score_job.py v0.1 with Grok scoring").
- Dependencies: LangChain/FAISS/sentence-transformers core; no unnecessary libs.
- Error handling: Robust (try/except, user-friendly messages); no silent failures.

## Response Style Rules
- Code-first for implementations: Provide full, ready-to-run code blocks.
- Ask clarifying questions if scope unclear.
- Proactive memory: Propose updates to decisions.md/Teachables/ for key events/milestones.
- Use tables for comparisons/lists when effective.

## Project Management Rules
- Public repo: All comms/code in GitHub.
- Workflow: Score → Decision → Tailor → Generate (intermediates for review).
- Export legacy masters (profile_export.py) before running POC scripts on data/master/.
- On rejection/hold: Optionally move files to intake/rejected/ or intake/held/.
- Numbering: Use prefix IDs for stories/reqs/specs.

Last updated: 2026-02-05