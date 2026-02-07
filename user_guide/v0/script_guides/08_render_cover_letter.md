# 08 - Render Cover Letter (scripts/08_render_cover_letter.py)

**Purpose**  
Phase 8 in the pipeline: Renders the intermediate cover letter JSON (generated in Phase 7) into human-readable formats.

It transforms the structured data into a professionally formatted document, handling alignment, margins, and font consistency.

**Input Requirements**  
*   Generated Cover Letter JSON: `generated/cover_intermediate_*.json`.

**Output**  
Creates files in the job's `generated/` subfolder:
*   `cover_letter_<version>.docx`: The final Word document ready for submission.
*   `cover_preview_<version>.md`: A Markdown preview for quick content checks.

**Usage**

### 1. Manual Run
```bash
# Standard run
python scripts/08_render_cover_letter.py --uuid cdb9a3fa --version v1
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) runs this Step 8 immediately after generating the content.
*   **Command used by auto-runner**:
    ```python
    python scripts/08_render_cover_letter.py --uuid <uuid> --version v1
    ```

**Structure & Formatting**
*   **Header**: Left-aligned candidate info; Right-aligned employer info.
*   **Body**: Standard paragraph spacing.
*   **Margins**: 1 inch all around.
*   **Font**: Arial, 11pt (standard for readability).

**Related Files**  
- Script: `scripts/08_render_cover_letter.py`  
- Input: `generated/cover_intermediate_*.json`  
- Output: `generated/cover_letter_*.docx`  
- Next Step: `09_update_application_status.py` (Tracking)
