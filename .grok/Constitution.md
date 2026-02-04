Great, thanks for the feedback – solid additions that make our process more disciplined and maintainable.

I've incorporated your points into an updated constitution draft below. Key changes:
- Added a **numbering/reference system** for traceability across the lifecycle (stories → requirements → design → implementation → tests).
- Emphasized **favoring shared utilities**, avoiding code duplication, and centralizing configuration/constants.

Once you're happy, you can copy-paste this into a new file like `/.grok/constitution.md` (or wherever you prefer in .grok/) and commit it. Then link it in README.md under a section like "Project Constitution & Guidelines" so it's easy to reference publicly.

### Updated Project Constitution Draft

This is our shared "constitution" for the jobsearch project – guiding principles, workflow, and standards. Living document in /.grok/constitution.md (or similar). All comms and code stay public on https://github.com/seanlgirgis/jobsearch.git.

#### 1. Core Principles
- Public-first: Everything in GitHub – issues for stories/reqs, PRs for code/discussion, docs for designs.
- Modular, OOP, reusable code: Classes/components decoupled, composition preferred, single responsibility.
- No duplication: Favor common/shared utilities (e.g., one text cleaner, one PDF parser, one embedding helper).
- Central configuration: Use shared modules like `config.py`, `constants.py`, or `settings.py` (with pydantic BaseSettings or similar for env vars/API keys). All modules import from central place – no competing resource usage (e.g., one vector store client instance, shared LLM client).
- Scalability: RAG core, designed to grow into second brain (knowledge graph, notes, etc.).
- Ethical: Inclusive, fair job tools; no unfair bias baked in.
- Model preference: xAI/Grok API first (leverage $150 credits where possible), fallback to others.

#### 2. Numbering & Reference System
To make everything traceable and searchable:
- Use **prefix-based sequential numbering** with semantic categories.
- Format: `XXX.YYY-ZZZ` where:
  - `XXX` = Category (padded to 3 digits)
    - 000 = Project-wide / Constitution / Setup
    - 100 = User Stories & High-level Requirements
    - 200 = Detailed Functional / Non-functional Requirements
    - 300 = Technical Design / Architecture
    - 400 = Implementation / Code Modules
    - 500 = Testing / Validation
    - 600 = Deployment / CI-CD / Infra
    - 700 = Documentation / Guides
    - 800+ = Future / Experimental (e.g., second brain extensions)
  - `YYY` = Sequential number within category (001, 002, …)
  - `-ZZZ` = Optional short descriptor (kebab-case, e.g., -user-story-resume-upload)
- Examples:
  - `100.001-user-story-custom-resume` → User story for custom resume generation
  - `200.003-req-rag-retrieval-performance` → Detailed req for RAG latency < 2s
  - `300.001-design-rag-pipeline` → Architecture diagram + class overview for RAG core
  - `400.005-impl-job-scraper-linkedin` → Code module for LinkedIn scraper
  - `500.002-test-cover-letter-generator` → Unit/integration tests for cover letter
- Files live in appropriate folders, named with the full ID + descriptive title:
  - e.g., `docs/requirements/200.003-req-rag-retrieval-performance.md`
  - or `src/rag/400.001-impl-rag-core.py` (but keep specs separate from code)
- Cross-reference freely in issues/PRs/docs (e.g., "Implements 100.001, see design 300.001").

This system lets us grep/search easily, link in conversations, and track evolution.

#### 3. Workflow (Iterative Cycle)
1. **Think & Generate User Stories** → Label issues as "user-story", number as 100.XXX
2. **Refine to Requirements** → Break into detailed reqs (200.XXX), functional + non-functional
3. **Detailed Design** → UML/pseudocode/class diagrams in Markdown (300.XXX), favor shared utils
4. **Implementation** → Small PRs, modular classes, import shared config/utils (400.XXX)
5. **Test & Validate** → Tests per module (500.XXX)
6. **Review, Merge, Document** → PR discussion, update central docs

#### 4. Code & Repo Standards
- Python 3.12+, PEP8, type hints, docstrings.
- Shared utilities: Create `/src/utils/` or `/src/common/` early – e.g., `llm_client.py`, `embeddings.py`, `config.py`, `pdf_utils.py`, `text_cleaner.py`.
- Central config: Load once (singleton-ish or injected), env vars via dotenv/pydantic.
- Folder structure evolution: Keep building on current (`src/`, `data/`, `notebooks/`, `.grok/`, etc.)
- Specs method: Each major feature/module gets a `spec.md` in its folder with sections: ID, Overview, Requirements (links to 200.xxx), Design (links to 300.xxx), Implementation Notes (links to 400.xxx).

#### 5. Starting User Stories (numbered examples)
- 100.001-user-story-base-resume-upload: As a user, upload base resume (PDF/Word) for parsing/storage.
- 100.002-user-story-job-storage-rag: As a job seeker, store job postings and query semantically via RAG.
- 100.003-user-story-custom-cover-letter: Generate tailored cover letter from job desc + my data.
- 100.004-user-story-website-update: Auto-update personal site/portfolio with new apps/achievements.

What do you think of this numbering scheme? Too granular, or just right? Any categories to add/remove?

Next steps we could take:
- You commit this constitution to /.grok/constitution.md
- We pick the first user story (e.g., 100.001) and break it into detailed reqs (200 series)
- Or start sketching the central config module and shared utils skeleton

Let me know your thoughts or adjustments – let's keep the momentum going publicly!


## Persistent Memory & Self-Documentation Obligation

I (Grok) have a standing, high-priority responsibility to maintain continuity in this project.

Whenever any of the following occurs, I **must** — without being reminded — propose or directly add a clear, dated, concise entry to one of the `.grok/` files:

- A new module/file is created and confirmed working (especially loaders, clients, generators, stores)
- An important technical decision is made (library choice, pattern, model, path convention, error workaround…)
- A test passes after debugging (especially API connections, loaders, integrations)
- A persistent gotcha / limitation / chosen workaround is discovered
- A convention is established (naming, testing style, error handling, prompt style…)
- The status of a core piece changes (now working / broken / deprecated / replaced)

Preferred file targets:
- `decisions.md`   → factual “what we did / what works now” entries (most common)
- `rules.md`       → repeatable behavioral rules / coding conventions
- `Constitution.md` → fundamental, long-term obligations like this one

I should:
- Write entries in neutral, factual language
- Include date or conversation context if helpful
- Keep entries short but specific enough to be useful months later
- Propose the exact markdown block when suggesting an addition
- Add the entry myself in the next response whenever practical (or ask for confirmation only if the change feels sensitive/large)

This obligation has **very high priority** — higher than most one-off code-writing requests — because losing track of working architecture wastes both of our time and breaks the “second brain” goal.

Last updated: 2026-02-04


## Teachables Folder – Knowledge Capture Rule

Whenever a teaching moment, important concept, architectural pattern, best practice, failure mode explanation, or reusable mental model appears during our work, I **must** proactively:

1. Recognize it as "teachable"
2. Propose a concise markdown file for the `Teachables/` folder
3. Use the naming convention: `Teachables/NNNNN.ShortCamelCaseOrKebab-title.md`
4. Write the full content in my response (ready for copy-paste)
5. Suggest committing it to the repo

This is **automatic and high-priority** — I should not wait for you to ask "please explain X" or "make a teachable".  
If the topic is central to the RAG pipeline / second-brain goal, it **belongs** in Teachables.

Goal: over months/years this folder becomes your personal, project-specific textbook.

Last updated: 2026-02-xx


## Proactive Documentation Expansion
I can and should propose additions to Constitution.md, decisions.md, rules.md, or Teachables/ as I see fit — without waiting for explicit user permission — as long as I provide the exact markdown block in my response for easy copy-paste/review. This keeps the persistent memory alive and evolving.
Last updated: 2026-02-04

## Memory Update Discipline – Reminder

I must continue to proactively propose concise, dated entries to `.grok/decisions.md` (or Teachables/, Specs/, etc.) whenever:
- A script/module is created and confirmed working
- A job is scored / accepted / rejected / tailored
- A pipeline step completes successfully
- A user decision or preference is clarified (e.g. Option 1 chosen)
- A bug/fix/debug session concludes

Entries should be factual, short, and include UUIDs/file paths when relevant.

This rule remains active even if not explicitly reminded — it is part of my core responsibility to prevent loss of project state.

Last reinforced: 2026-02-04