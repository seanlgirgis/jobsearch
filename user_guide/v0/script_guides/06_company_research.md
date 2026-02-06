# 06 - Company Research (scripts/06_company_research.py)

**Purpose**  
Phase 6 in the pipeline: This script acts as a research agent. It analyzes the company from the tailored data and uses an LLM (Grok) to:
1.  **Classify** the company as either an **'agency'** (staffing/recruiting firm) or an **'enterprise'** (direct employer/product company).
2.  **Research** the company if it is an 'enterprise', identifying key details like culture, mission, and values to help tailor the cover letter. Agency searches are skipped to save tokens/time.

**Input Requirements**  
- Job folder in `data/jobs/`  
- Tailored data must exist: `tailored/tailored_data_*.yaml` (generated in earlier phases).

**Output**  
Creates a YAML file in the job's `research/` subfolder:  
- `research/company_research.yaml` (or versioned like `company_research_v1.yaml`)  
  - Contains: `company`, `type` (agency/enterprise), `research` (summary text), `website`.

**Usage**

```bash
# Standard run
python scripts/06_company_research.py --uuid cdb9a3fa

# Specify model and version
python scripts/06_company_research.py --uuid cdb9a3fa --model grok-3 --version v1
```

**Behavior**  
- **Classification**:  
  - It sends the company name and website to the LLM.  
  - Prompts for a single-word classification: "agency" or "enterprise".  
  - Defaults to "enterprise" if ambiguous or if the API fails (or if running in Mock mode).
- **Research**:  
  - **Enterprise**: Fetches a 1-2 paragraph summary of the company's culture and values using the LLM.  
  - **Agency**: Skips the research step (sets research text to empty) as cover letters for agencies usually focus more on the candidate's skills than the agency's specific internal culture.

**Logic & Fallbacks**  
- **Mock Mode**: If `src.ai.grok_client` is not found, it warns and defaults to "enterprise" with mock research text.  
- **Ambiguity**: If classification returns an unexpected response, it defaults to "enterprise" to be safe.

**Related Files**  
- Script: `scripts/06_company_research.py`  
- Input: `data/jobs/0000X.../tailored/tailored_data_*.yaml`  
- Output: `data/jobs/0000X.../research/company_research.yaml`  
- Next Step: `scripts/07_generate_cover_intermediate.py`  
