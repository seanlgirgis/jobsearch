# 06 - Company Research (scripts/06_company_research.py)

**Purpose**  
This script acts as a research agent. It analyzes the company from the tailored data and uses an LLM (Grok) to:
1.  **Classify** the company as either an **'agency'** (staffing/recruiting firm) or an **'enterprise'** (direct employer/product company).
2.  **Research** the company if it is an 'enterprise', identifying key details like culture, mission, and values to help tailor the cover letter. Agency searches are skipped to save tokens/time (as cover letters for agencies focus on the candidate, not the agency).

**Input Requirements**  
*   Tailored Job Data: `tailored/tailored_data_*.yaml` (from Script 03).

**Output**  
Creates `data/jobs/<uuid>/research/company_research_<version>.yaml`:
```yaml
company: "Postscript"
type: "enterprise"
research: |
  Postscript is a SMS marketing platform for Shopify... 
  Core values include "High impact, low ego"...
website: "https://postscript.io"
classified_at: "..."
```

**Usage**

### 1. Manual Run
```bash
# Standard run
python scripts/06_company_research.py --uuid cdb9a3fa --version v1

# Custom model
python scripts/06_company_research.py --uuid cdb9a3fa --model grok-3
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) runs this Step 6 in parallel (conceptually) with the resume generation.
*   **Command used by auto-runner**:
    ```python
    python scripts/06_company_research.py --uuid <uuid> --version v1 --model grok-3
    ```

**Logic & Fallbacks**
*   **Agency Detection**: If the LLM classifies the company as a recruiting firm (e.g., TekSystems, Robert Half), it sets `type: agency` and **skips** the detailed research to avoid hallucinating "values" for a staffing firm.
*   **Mock Mode**: If `src.ai.grok_client` is missing, it defaults to "enterprise" with dummy research text.

**Related Files**  
- Script: `scripts/06_company_research.py`  
- Input: `tailored/tailored_data_*.yaml`  
- Output: `research/company_research_*.yaml`  
- Next Step: `07_generate_cover_intermediate.py` (which uses this research)
