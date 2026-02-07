# 03 - Tailor Job Data (scripts/03_tailor_job_data.py)

**Purpose**  
This script transforms a raw job description into structured, tailored data. It uses an LLM (Grok) to extract skills, rephrase responsibilities, and identify ATS keywords.

This structured data (`tailored_data.yaml`) is the **foundational input** for both the Resume (Script 04) and Cover Letter (Script 07) generators.

**Key Capabilities**
1.  **Structure**: Converts messy free-text job descriptions into clean YAML.
2.  **Enrichment**: Extracts "Must Have" vs "Nice to Have" skills.
3.  **Metadata Preservation**: Reads `metadata.yaml` to ensure the Company Name and Website are carried over accurately (fixing issues where LLMs might hallucinate them).

**Input Requirements**  
*   Job folder with raw job text (from Script 01).
*   `metadata.yaml` (optional but recommended for accurate company info).

**Output**  
Creates `data/jobs/<uuid>/tailored/tailored_data_<version>.yaml`:
```yaml
company_name: "StartUp Inc"
job_title: "Senior Engineer"
extracted_skills: [python, sql, aws]
must_have_skills: [python, system design]
nice_to_have_skills: [kubernetes]
ats_keywords: [distributed systems, ci/cd]
responsibilities:
  - "Design and build scalable APIs..."
requirements:
  - "5+ years experience..."
```

**Usage**

### 1. Manual Run
```bash
# Standard run (creates tailored_data_v1.yaml)
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --version v1

# Custom version tag
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --version llm-v2

# Force naive regex (no LLM cost)
python scripts/03_tailor_job_data.py --uuid cdb9a3fa --no-llm
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) runs this immediately after accepting the job.
*   **Command used by auto-runner**:
    ```python
    python scripts/03_tailor_job_data.py --uuid <uuid> --version v1
    ```

**Arguments**
*   `--uuid`: The job's UUID.
*   `--version`: Label for this tailoring iteration (e.g., `v1`, `experiment-A`).
*   `--model`: LLM model (default: `grok-3`).
*   `--no-llm`: Skip AI and use simple regex matching (faster, less accurate).

**Related Files**  
- Script: `scripts/03_tailor_job_data.py`  
- Output: `data/jobs/<uuid>/tailored/tailored_data_*.yaml`  
- Next Steps: `04_generate_resume_intermediate.py` and `07_generate_cover_intermediate.py`