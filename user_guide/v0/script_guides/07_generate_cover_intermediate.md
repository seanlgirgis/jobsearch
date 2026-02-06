# 07 - Generate Cover Letter Intermediate (scripts/07_generate_cover_intermediate.py)

**Purpose**  
Phase 7 in the pipeline: This script generates the *content* of the cover letter in a structured JSON format. It acts as the bridge between raw data and the final rendered document (Phase 8). It orchestrates:
1.  **Classification**: Determines if the company is an agency or enterprise (using logic shared with Phase 6).
2.  **Research Integration**: If 'enterprise', it fetches specific research about the company's culture/values.
3.  **Content Generation**: Uses an LLM (Grok) to write the cover letter sections (intro, body, conclusion) based on *your* master career data, strictly following rules to avoid hallucinations.

**Input Requirements**  
- Job folder in `data/jobs/`  
- **Tailored Data**: `tailored/tailored_data_*.yaml` (from Phase 3)  
- **Master Data**: `data/master/master_career_data.json` and `data/master/skills.yaml` (source of truth for facts)  

**Output**  
Creates a JSON file in the job's `generated/` subfolder:  
- `cover_intermediate_{version}.json`  
  - **Structure**:
    ```json
    {
      "header": { "date": "...", "employer_address": "..." },
      "salutation": "Dear Hiring Manager,",
      "intro": "...",
      "body": ["Para 1...", "Para 2..."],
      "conclusion": "...",
      "sign_off": "Sincerely,\nYour Name"
    }
    ```

**Usage**

```bash
# Standard run
python scripts/07_generate_cover_intermediate.py --uuid cdb9a3fa

# Specify version tag and model
python scripts/07_generate_cover_intermediate.py --uuid cdb9a3fa --version v1 --model grok-3
```

**Behavior**  
- **Date Injection**: Automatically uses the current date (e.g., "February 06, 2026") in the header.  
- **Hallucination Control**: The system prompt explicitly instructs the LLM to use *only* facts from the provided master career data.  
- **Agency vs Enterprise**:
  - **Agency**: Generates a more generic, skills-focused letter suitable for recruiters.  
  - **Enterprise**: Weaves in specific company values and research to show cultural fit.  
- **Mock Mode**: If `src.ai.grok_client` is missing, it generates dummy/mock JSON data for testing purposes.

**Related Files**  
- Script: `scripts/07_generate_cover_intermediate.py`  
- Input: `data/jobs/.../tailored/tailored_data_*.yaml`  
- Output: `data/jobs/.../generated/cover_intermediate_*.json`  
- Next Step: `scripts/08_render_cover_letter.py` (to turn this JSON into a DOCX/PDF)  
