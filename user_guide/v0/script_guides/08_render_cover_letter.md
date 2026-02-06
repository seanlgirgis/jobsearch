# 08 - Render Cover Letter (scripts/08_render_cover_letter.py)

**Purpose**  
Phase 8 in the pipeline: Renders the intermediate cover letter JSON (generated in Phase 6) into human-readable formats:
- **Microsoft Word (.docx)**: The primary formatted output for submission.
- **Markdown (.md)**: A quick preview format for verification.

It takes the structured JSON data (header, salutation, body paragraphs) and applies standard formatting suitable for a professional cover letter.

**Current Status**  
Working / Stable (as of Feb 5, 2026)

**Input Requirements**  
- Job folder in `data/jobs/` (pattern `0000X_xxxxxxxx` or similar).
- Generated intermediate cover letter JSON exists: `generated/cover_intermediate_{version}.json` (from Phase 6).

**Output**  
Creates files in the job's `generated/` subfolder:
- `cover_letter_{version}.docx` (Final Word document)
- `cover_preview_{version}.md` (Markdown preview)

**Usage**

```bash
# Standard run
python scripts/08_render_cover_letter.py --uuid cdb9a3fa --version llm-tailored-v1
```

**Behavior**  
- **Smart folder resolution**: Matches partial UUIDs (`cdb9a3fa`) or exact folder names.
- **Intermediate JSON Loading**: Looks for `cover_intermediate_{version}.json`. If not found, falls back to the latest `cover_intermediate_*.json`.
- **Formatting Logic**:
  - **Header**: Includes Name, Address, Phone/Email, Date, and Hiring Manager address.
  - **Body**: Renders paragraphs sequentially.
  - **Sign-off**: Standard Left-aligned closing.
  - **Margins**: 1 inch all around.
  - **Font**: Arial, 11pt.

**Known Behaviors / Gotchas**  
- **Font Dependency**: Uses "Arial" by default.
- **Hardcoded Styling**: Margins and font sizes are hardcoded in the script.
- **Pre-requisite**: Phase 6 (Generate Cover Intermediate) MUST be run first to create the input JSON.

**Related Files**  
- Script: `scripts/08_render_cover_letter.py`
- Input: `data/jobs/0000X_xxxxxxxx/generated/cover_intermediate_*.json`
- Output: `data/jobs/0000X_xxxxxxxx/generated/cover_letter_*.docx`
- Predecessors:
  - `scripts/06_generate_cover_intermediate.py` (Required to create the JSON input)
