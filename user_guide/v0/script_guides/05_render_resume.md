# 05 - Render Resume (scripts/05_render_resume.py)

**Purpose**  
Phase 5 in the pipeline: After the intermediate JSON structure is generated (in phase 04), this script renders it into human-readable formats:  
- **Microsoft Word (.docx)**: The primary formatted output for submission.  
- **Markdown (.md)**: A quick preview format for verification.  
- **PDF (.pdf)**: Optional PDF export (requires `docx2pdf`).

It supports generating both **full-length detailed** resumes and **trimmed** versions (strictly limited to the 5 most recent roles).

**Current Status**  
Working / Stable (as of Feb 6, 2026)  
Recently updated to improve formatting, fix hyperlink generation, and refine "Trimmed" vs "Full" logic.

**Input Requirements**  
- Job folder in `data/jobs/` (pattern `0000X_xxxxxxxx` or similar)  
- Generated intermediate JSON exists: `generated/resume_intermediate_{version}.json`  
- **Exclusions**: Reads `data/source_of_truth.json` (primary) or `data/master/master_career_data.json` (fallback) to find companies marked with `"exclude_from_resume": true`.

**Output**  
Creates files in the job's `generated/` subfolder:  
- `resume_{version}.docx` (Full Word data)  
- `resume_preview_{version}.md` (Markdown preview)  
- `resume_{version}_trimmed.docx` (If trimmed or --all)  
- `resume_preview_{version}_trimmed.md` (If trimmed or --all)

**Usage**

```bash
# Standard run (renders specific version)
python scripts/05_render_resume.py --uuid cdb9a3fa --version llm-tailored-v1

# Generate trimmed version only (Top 5 recent jobs ONLY)
python scripts/05_render_resume.py --uuid cdb9a3fa --version llm-tailored-v1 --trim

# Generate BOTH full and trimmed versions
python scripts/05_render_resume.py --uuid cdb9a3fa --version llm-tailored-v1 --all

# Generate PDF (requires docx2pdf)
python scripts/05_render_resume.py --uuid cdb9a3fa --version llm-tailored-v1 --format pdf
```

**Behavior**  
- **Smart folder resolution**: Matches partial UUIDs (`cdb9a3fa`) or exact folder names.  
- **Intermediate JSON Loading**: Looks for `resume_intermediate_{version}.json`. If not found, falls back to the latest `resume_intermediate_*.json`.  
- **Exclusions**: Filters out companies marked with `"exclude_from_resume": true` in the master data (`source_of_truth.json`).  
- **Formatting Logic**:  
  - Name is rendered in **16pt** font.  
  - Headers are **13pt**, body text is **11pt**.  
  - **Flagship Projects**: Descriptions are split into new lines for each sentence. "Technologies:" and "Repo:" labels are bolded.  
  - **Hyperlinks**: Clickable links for LinkedIn, GitHub, Portfolio, and project Repos.  
- **Length Differentiation**:
  - **Full Version**: Renders **ALL** jobs in the history with full detail (bullets, dates, etc.).
  - **Trimmed Version**: Renders **ONLY** the top 5 most recent/relevant roles in detail. Older roles are **completely removed** (no summary section).

**Known Behaviors / Gotchas**  
- **Font Dependency**: Uses "Arial" by default.  
- **Formatting Specifics**: The script has hardcoded font sizes and margins (0.5" top/bottom, 0.6" left/right).  
- **PDF Generation**: Disabled by default unless `--format pdf` is passed. Requires `pip install docx2pdf`.
- **HCL / Entergy**: Specifically excluded via `source_of_truth.json` configuration.

**Related Files**  
- Script: `scripts/05_render_resume.py`  
- Input: `data/jobs/0000X_xxxxxxxx/generated/resume_intermediate_*.json`  
- Master Data: `data/source_of_truth.json`
- Output: `data/jobs/0000X_xxxxxxxx/generated/resume_*.docx`  
