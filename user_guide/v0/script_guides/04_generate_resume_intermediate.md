# 04 - Generate Resume Intermediate (scripts/04_generate_resume_intermediate.py)

**Purpose**  
This script is the bridge between raw data and the final resume. It uses the LLM to **map your master experience to the tailored job requirements**, producing a structured JSON file.

It rewrites bullet points and summaries to highlight relevance *without* inventing facts. This JSON file (`resume_intermediate_v1.json`) is what gets rendered into the final DOCX/PDF.

**Key Capabilities**
1.  **Tailoring**: Rewrites your professional summary and experience bullets to match the job's keywords (from Script 03).
2.  **Fact-Checking**: Strictly bound to `master_career_data.json`—it cannot invent roles or dates.
3.  **Exclusions**: Respects the `exclude_from_resume: true` flag in your master data.

**Input Requirements**  
*   **Job Tailored Data**: `tailored/tailored_data_*.yaml` (from Script 03).
*   **Master Profile**: `data/master/master_career_data.json` and `skills.yaml`.

**Output**  
Creates `data/jobs/<uuid>/generated/resume_intermediate_<version>.json`.
This JSON contains the *exact text* that will appear on the resume.

**Usage**

### 1. Manual Run
```bash
# Standard run (creates resume_intermediate_v1.json)
python scripts/04_generate_resume_intermediate.py --uuid cdb9a3fa --version v1

# Use a specific model
python scripts/04_generate_resume_intermediate.py --uuid cdb9a3fa --version v1 --model grok-3
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) runs this Step 4 immediately after tailoring.
*   **Command used by auto-runner**:
    ```python
    python scripts/04_generate_resume_intermediate.py --uuid <uuid> --version v1 --model grok-3
    ```

**Arguments**
*   `--uuid`: The job's UUID.
*   `--version`: Label for this generation (default: `v1`).
*   `--model`: LLM model (default: `grok-3`).

**Related Files**  
- Script: `scripts/04_generate_resume_intermediate.py`  
- Input: `tailored/tailored_data_*.yaml`  
- Output: `generated/resume_intermediate_*.json`  
- Next Step: `05_render_resume.py` (Visual Rendering)