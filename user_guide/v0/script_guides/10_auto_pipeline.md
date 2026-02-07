# 10 - Auto Pipeline (scripts/10_auto_pipeline.py)

**Purpose**  
This script is the **orchestrator** for the entire job search workflow. It chains Scripts 01 through 09 into a single, automated command.

Instead of running each step manually and copying UUIDs, this script handles:
1.  **Scoring & Decision**: Runs Script 01, extracts the UUID, and automatically accepts the job (Script 02).
2.  **Asset Generation**: Runs tailoring, resume gen, and cover letter gen (Scripts 03, 04, 07).
3.  **Rendering**: Produces PDF/DOCX outputs (Scripts 05, 08).
4.  **Research**: Fetches company info (Script 06).
5.  **Tracking**: Logs the application in your metadata (Script 09).

**Input Requirements**  
*   A markdown intake file (e.g., `intake/job.md`).

**Output**  
*   A fully processed job folder with:
    *   Tailored resume & cover letter (DOCX/MD).
    *   Company research (YAML).
    *   Application status set to "Applied".

**Usage**

### 1. Standard Run
```bash
# Process a job from intake to "Applied"
python scripts/10_auto_pipeline.py intake/job.md --method "LinkedIn"
```

### 2. Custom Application Details
```bash
python scripts/10_auto_pipeline.py intake/job.md \
  --method "Referral" \
  --date "2026-02-06" \
  --notes "Referred by John Doe"
```

### 3. Model & Version Overrides
```bash
python scripts/10_auto_pipeline.py intake/job.md \
  --model "grok-3" \
  --version "experiment-v2" \
  --temperature 0.7
```

**Workflow Steps**
The script executes the following sequence:
1.  **01_score_job.py**: Scores job & extracts UUID.
2.  **02_decide_job.py**: Auto-accepts with reason "Auto-accepted by pipeline".
3.  **03_tailor_job_data.py**: Creates tailored YAML.
4.  **04_generate_resume_intermediate.py**: Creates resume JSON.
5.  **05_render_resume.py**: Renders DOCX/MD (both Full & Trimmed).
6.  **06_company_research.py**: Fetches company info.
7.  **07_generate_cover_intermediate.py**: Creates cover letter JSON.
8.  **08_render_cover_letter.py**: Renders cover letter DOCX.
9.  **09_update_application_status.py**: Marks as Applied.

**Known Behaviors**
*   **Stop on Failure**: If any step fails (non-zero exit code), the pipeline stops immediately.
*   **UTF-8 Enforcement**: Automatically sets `PYTHONUTF8=1` to handle emojis on Windows consoles.
*   **No Resume PDF**: PDF generation is skipped by default unless `docx2pdf` is installed and configured in script 05 (currently defaults to DOCX only).

**Related Files**  
- Script: `scripts/10_auto_pipeline.py`  
- All other scripts in `scripts/` (01-09).
