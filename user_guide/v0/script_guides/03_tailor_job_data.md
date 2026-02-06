
```markdown
# 03 - Tailor Job Data (scripts/03_tailor_job_data.py)

**Purpose**  
After a job has been **ACCEPTED** (via `02_decide_job.py`), enrich and structure the raw job description for downstream use:  
- Better semantic retrieval in RAG pipelines  
- Keyword/ATS optimization for resume & cover letter tailoring  
- Clear separation of must-have vs nice-to-have skills  
- Concise summary + rephrased bullets  

The script uses Grok (xAI) to produce high-quality structured output in YAML format, with a naive regex-based fallback if LLM fails or `--no-llm` is used.

**Current Status**  
Working / POC-stable (as of Feb 5, 2026)  
Successfully tested: Collective Health Staff Data Engineer → produced structured YAML with skills, summary, bullets, ATS keywords

**Input Requirements**  
- Job folder already exists in `data/jobs/` (pattern `0000X_xxxxxxxx`)  
- `metadata.yaml` exists and status = **ACCEPTED** (strongly recommended, not strictly enforced yet)  
- Raw job text exists in one of:  
  - `raw/job_description.md`  
  - `raw/raw_intake.md`  
  - (or override with `--raw-file`)

**Output**  
Creates/updates folder:  
```
data/jobs/0000X_xxxxxxxx/
└── tailored/
    └── tailored_data_{version}.yaml          # e.g. tailored_data_llm-v1.yaml
```

Typical content of the YAML file:

```yaml
extracted_skills:
- python
- sql
- snowflake
- databricks
- airflow
job_summary: |
  Company is seeking a Staff Data Engineer to build and maintain scalable data pipelines...
responsibilities:
- Design and implement ETL pipelines using Airflow and dbt
- ...
requirements:
- 5+ years of Python and SQL experience
- ...
preferred:
- Experience with Snowflake or Databricks
- ...
must_have_skills:
- python
- sql
- etl
nice_to_have_skills:
- airflow
- dbt
ats_keywords:
- data engineering
- etl pipelines
- snowflake
- python sql
tailoring_method: llm
llm_model: grok-3
llm_version: llm-v1
```

**Usage**

```bash
# Normal run (smart UUID resolution)
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --version llm-v1

# Explicit folder name
python scripts/03_tailor_job_data.py --uuid 00001_cdb9a3fa --version llm-v2

# Force naive regex mode (no LLM call)
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --version naive-v1 --no-llm

# Custom model / temperature
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --version exp-01 --model grok-3 --temperature 0.2

# Override raw file
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --version llm-v1 --raw-file intake/custom-job.md
```

**Behavior**  
- Smart folder resolution: accepts full folder name, short UUID, or prefix (same logic as `02_decide_job.py`)  
- Tries multiple common raw file locations  
- Primary path: calls Grok with strict YAML-only prompt  
- Aggressive response cleaning (removes fences, extra text)  
- Falls back to naive regex section/skill extraction if LLM fails  
- Saves versioned file in `tailored/` subfolder  
- Prints detected skills preview on success

**Known Behaviors / Gotchas**  
- Requires Grok API access (`src/ai/grok_client.py` configured)  
- LLM output can occasionally be malformed → fallback is automatic  
- `--temperature 0.0` is strongly recommended for structured YAML output  
- Naive mode (`--no-llm`) produces much simpler output (only basic sections + skills)  
- Does **not** yet update `metadata.yaml` with tailoring status/version (future enhancement)

**Related Files**  
- Script: `scripts/03_tailor_job_data.py`  
- Output: `data/jobs/0000X_xxxxxxxx/tailored/tailored_data_*.yaml`  
- Predecessor: `scripts/02_decide_job.py` (should be ACCEPTED)  
- Next typical step: resume/cover letter generation, keyword injection, application tracking  

**Decisions Log References**  
- Output format: clean YAML, no markdown fences  
- Smart UUID resolution: `*_{uuid prefix}*` matching  
- Fallback: naive regex → `tailoring_method: llm_fallback_naive`  
- LLM prompt enforces strict structure (skills, summary, bullets, must/nice, ATS keywords)  
- Versioning: free-form tag via `--version` (convention: `llm-v1`, `naive-v1`, `exp-01`, etc.)
```

This file should be saved as:

```
docs/03_tailor_job_data.md
```

(or wherever you are keeping phase documentation — consistent with `01_score_job.md` and `02_decide_job.md`).

Let me know when you're ready to move to phase 04 (e.g. resume tailoring, cover letter generation, or application tracker).