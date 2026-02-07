# 07 - Generate Cover Letter Intermediate (scripts/07_generate_cover_intermediate.py)

**Purpose**  
This script generates the *content* of the cover letter in a structured JSON format. It acts as the bridge between raw data and the final rendered document (Phase 8).

It combines:
1.  **Tailored Job Data** (from Script 03) for keywords and requirements.
2.  **Company Research** (from Script 06) for cultural fit and values.
3.  **Master Career Data** for factual history.

**Key Capabilities**
1.  **Hallucination Control**: Strictly binds the LLM to your `master_career_data.json` to prevent inventing facts.
2.  **Adaptive Tone**:
    *   **Enterprise**: Weaves in specific research (mission, values) to show deep interest.
    *   **Agency**: Uses a professional, skills-focused tone suitable for recruiters.
3.  **Date Injection**: Automatically inserts the current date.

**Input Requirements**  
*   Tailored Data: `tailored/tailored_data_*.yaml`
*   Research Data: `research/company_research.yaml` (optional, but improves quality)

**Output**  
Creates `data/jobs/<uuid>/generated/cover_intermediate_<version>.json`:
```json
{
  "header": { "date": "February 06, 2026", "employer_address": "..." },
  "salutation": "Dear Hiring Manager,",
  "intro": "I am writing to express my enthusiasm for the Senior Engineer role...",
  "body": [
    "At [Previous Company], I led the migration...",
    "Your focus on [Company Value] resonates with me..."
  ],
  "conclusion": "I would welcome the opportunity to discuss...",
  "sign_off": "Sincerely,\nYour Name"
}
```

**Usage**

### 1. Manual Run
```bash
# Standard run
python scripts/07_generate_cover_intermediate.py --uuid cdb9a3fa --version v1

# Custom model
python scripts/07_generate_cover_intermediate.py --uuid cdb9a3fa --model grok-3
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) runs this Step 7 immediately after company research.
*   **Command used by auto-runner**:
    ```python
    python scripts/07_generate_cover_intermediate.py --uuid <uuid> --model grok-3
    ```

**Related Files**  
- Script: `scripts/07_generate_cover_intermediate.py`  
- Input: `tailored/tailored_data_*.yaml` & `research/company_research.yaml`  
- Output: `generated/cover_intermediate_*.json`  
- Next Step: `08_render_cover_letter.py` (Visual Rendering)
