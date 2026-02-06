# 05 - Render Resume (scripts/05_render_resume.py)

**Purpose**  
Phase 5 in the pipeline: After the intermediate JSON structure is generated (in phase 04), this script renders it into human-readable formats:  
- **Microsoft Word (.docx)**: The primary formatted output for submission.  
- **Markdown (.md)**: A quick preview format for verification.  

It supports generating both full-length resumes and trimmed versions (limited to the 5 most recent roles) for cases where a shorter resume is preferred.

**Current Status**  
Working / Stable (as of Feb 5, 2026)  
Recently updated to improve formatting of "Flagship Projects" (sentence splitting, bold labels).

**Input Requirements**  
- Job folder in `data/jobs/` (pattern `0000X_xxxxxxxx` or similar)  
- Generated intermediate JSON exists: `generated/resume_intermediate_{version}.json`  
- Master profile file (optional but recommended for exclusions): `data/master/master_career_data.json`  

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

# Generate trimmed version only (5 recent jobs)
python scripts/05_render_resume.py --uuid cdb9a3fa --version llm-tailored-v1 --trim

# Generate BOTH full and trimmed versions
python scripts/05_render_resume.py --uuid cdb9a3fa --version llm-tailored-v1 --all
```

**Behavior**  
- **Smart folder resolution**: Matches partial UUIDs (`cdb9a3fa`) or exact folder names.  
- **Intermediate JSON Loading**: Looks for `resume_intermediate_{version}.json`. If not found, falls back to the latest `resume_intermediate_*.json`.  
- **Exclusions**: Reads `master_career_data.json` to filter out companies marked with `"exclude_from_resume": true`.  
- **Formatting Logic**:  
  - Name is rendered in **16pt** font.  
  - Headers are **13pt**, body text is **11pt**.  
  - **Flagship Projects**: Descriptions are split into new lines for each sentence. "Technologies:" and "Repo:" labels are bolded.  
  - **Hyperlinks**: Clickable links for LinkedIn, GitHub, Portfolio, and project Repos.  
  - **Trim Mode**: Limits "Professional Experience" to the 5 most recent roles. Full version moves older roles to "Additional Experience" or keeps them in main flow depending on logic (currently appends older ones if not trimmed, or trims strictly if requested).  

**Known Behaviors / Gotchas**  
- **Font Dependency**: Uses "Arial" by default.  
- **Formatting Specifics**: The script has hardcoded font sizes and margins (0.5" top/bottom, 0.6" left/right).  
- **Deprecation Warnings**: May show warnings from `python-docx` regarding style lookups (these are harmless for now).  

**Related Files**  
- Script: `scripts/05_render_resume.py`  
- Input: `data/jobs/0000X_xxxxxxxx/generated/resume_intermediate_*.json`  
- Output: `data/jobs/0000X_xxxxxxxx/generated/resume_*.docx`  
- Predecessors:  
  - `scripts/04_generate_resume_intermediate.py` (Required to create the JSON input)  
