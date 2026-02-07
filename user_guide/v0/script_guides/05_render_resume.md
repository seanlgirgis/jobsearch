# 05 - Render Resume (scripts/05_render_resume.py)

**Purpose**  
This script takes the JSON structure (from Script 04) and renders it into the final, human-readable documents.

It is the visual layer of the pipeline, handling formatting, fonts, margins, and the "Trimmed" vs "Full" logic.

**Key Capabilities**
1.  **Dual Output**: Generates both **Full** (complete history) and **Trimmed** (Top 5 roles only) versions.
2.  **Formatting**: Renders to clean, ATS-friendly Markdown and professional DOCX.
3.  **Exclusions**: Filters out specific companies based on `source_of_truth.json` (e.g., hiding short stints).

**Input Requirements**  
*   Intermediate JSON: `generated/resume_intermediate_*.json`.
*   Master Data: `data/source_of_truth.json` (for exclusions).

**Output**  
Creates files in `data/jobs/<uuid>/generated/`:
*   `resume_<version>.docx`: The **Full** resume.
*   `resume_<version>_trimmed.docx`: The **Trimmed** resume (Top 5 roles).
*   `resume_preview_*.md`: Markdown previews for quick verification.

**Usage**

### 1. Manual Run
```bash
# Generate Standard (Full) Resume
python scripts/05_render_resume.py --uuid cdb9a3fa --version v1

# Generate ONLY Trimmed (Top 5)
python scripts/05_render_resume.py --uuid cdb9a3fa --version v1 --trim

# Generate BOTH (Full + Trimmed)
python scripts/05_render_resume.py --uuid cdb9a3fa --version v1 --all

# Output PDF (requires docx2pdf)
python scripts/05_render_resume.py --uuid cdb9a3fa --format pdf
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) uses the `--all` flag to ensure you have both options ready.
*   **Command used by auto-runner**:
    ```python
    python scripts/05_render_resume.py --uuid <uuid> --version v1 --all
    ```

**Logic Detail: Trimmed vs Full**
*   **Full**: Renders every experience listed in the intermediate JSON.
*   **Trimmed**:
    *   Retains the **Top 5** most recent/relevant roles with full bullets.
    *   **Removes** all older roles completely (no summary section).

**Related Files**  
- Script: `scripts/05_render_resume.py`  
- Input: `generated/resume_intermediate_*.json`  
- Output: `generated/resume_*.docx`  
- Next Step: `06_company_research.py` (Parallel track)
