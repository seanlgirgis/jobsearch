# 04 - Generate Resume Intermediate (scripts/04_generate_resume_intermediate.py)

**Purpose**  
After a job is **ACCEPTED** and **tailored** (via phases 02 & 03), generate a structured, job-tailored resume representation in JSON format.  
The script uses Grok to rewrite summary, experience bullets, and project descriptions — strictly bound to the master career data — while naturally incorporating job-specific keywords from the tailored job data.  
Filters out any experience entries marked `"exclude_from_resume": true`.

**Current Status**  
Working / POC-stable (as of Feb 5, 2026)  
Successfully tested: Collective Health Staff Data Engineer → produced tailored intermediate JSON with keyword-optimized bullets

**Input Requirements**  
- Job folder in `data/jobs/` (pattern `0000X_xxxxxxxx`)  
- `metadata.yaml` with status = **ACCEPTED** (recommended, not enforced)  
- Tailored job data exists: `tailored/tailored_data_*.yaml` (uses latest version by default)  
- Master profile files:  
  - `data/master/master_career_data.json`  
  - `data/master/skills.yaml`

**Output**  
Creates folder and file:  
```
data/jobs/0000X_xxxxxxxx/
└── generated/
    └── resume_intermediate_{version}.json     # e.g. resume_intermediate_llm-tailored-v1.json
```

Typical structure of the output JSON:

```json
{
  "personal": {
    "full_name": "Sean Luka Girgis",
    "email": "seanlgirgis@gmail.com",
    "phone": "...",
    "location": "Plano, TX",
    "linkedin": "..."
  },
  "summary": "Results-driven Staff Data Engineer with 8+ years of experience building scalable ETL pipelines using Python, SQL, Snowflake, and Airflow...",
  "experience": [
    {
      "company": "Company Name",
      "title": "Staff Data Engineer",
      "start": "2022-03",
      "end": "Present",
      "bullets": [
        "Designed and implemented ELT pipelines in Snowflake and Databricks, reducing processing time by 40%",
        "..."
      ]
    },
    "..."
  ],
  "education": [
    {
      "degree": "BS Computer Science",
      "institution": "University Name",
      "start": "2010",
      "end": "2014"
    }
  ],
  "skills": [
    "python", "sql", "snowflake", "airflow", "dbt", "databricks", "etl", "dimensional modeling"
  ],
  "projects": [
    {
      "name": "Enterprise Data Platform",
      "description": "Led development of modern data stack using Airflow, dbt, and Snowflake for real-time analytics..."
    }
  ]
}
```

**Usage**

```bash
# Normal run (smart UUID resolution)
python scripts/04_generate_resume_intermediate.py --uuid cdb9a3fa --version llm-tailored-v1

# Explicit folder name
python scripts/04_generate_resume_intermediate.py --uuid 00001_cdb9a3fa --version v2

# Custom model
python scripts/04_generate_resume_intermediate.py --uuid cdb9a3fa --version exp-01 --model grok-3
```

**Behavior**  
- Smart folder resolution: accepts full folder name, short UUID, or prefix (consistent with phases 02 & 03)  
- Automatically selects the latest `tailored_data_*.yaml` file  
- Applies `"exclude_from_resume": true` filter to master experiences  
- Calls Grok with strict JSON-only output prompt (temperature=0.0 enforced)  
- Aggressive cleaning of LLM response to extract valid JSON  
- Saves versioned JSON in `generated/` subfolder  
- Prints next-step guidance pointing to phase 5 renderer

**Known Behaviors / Gotchas**  
- Requires valid xAI API key (`src/ai/grok_client.py`)  
- LLM can occasionally produce malformed JSON → script will crash (future: add fallback / retry)  
- Long master profiles + job data can approach token limits → bullets/project descriptions may be auto-shortened by LLM  
- No automatic update to `metadata.yaml` yet (future: record last_resume_version)  
- Mock mode active if `GrokClient` import fails

**Related Files**  
- Script: `scripts/04_generate_resume_intermediate.py`  
- Output: `data/jobs/0000X_xxxxxxxx/generated/resume_intermediate_*.json`  
- Predecessors:  
  - `scripts/03_tailor_job_data.py` (required)  
  - `scripts/02_decide_job.py` (ACCEPTED status recommended)  
- Next typical step: resume rendering / PDF generation (phase 05)  

**Decisions Log References**  
- Output format: clean, structured JSON (no markdown)  
- Strict binding to master data — no hallucination of dates, roles, or facts  
- Smart UUID resolution: `*_{uuid prefix}*` matching  
- Versioning: free-form tag via `--version` (convention: `llm-tailored-v1`, `v2`, `exp-01`, etc.)  
- Exclusion filter applied from `master_career_data.json`  
- Prompt enforces full history + keyword tailoring without removal