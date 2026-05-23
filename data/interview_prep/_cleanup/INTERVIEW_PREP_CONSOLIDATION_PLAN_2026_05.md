# Interview Prep Consolidation Plan (Safe, No-Change) - 2026-05

Canonical interview prep root:
- `D:\Workarea\jobsearch\data\interview_prep`

Confirmed naming decision:
- Use `SharkforceConsulting` as correct spelling.
- `ShaekeforceConsulting` is legacy/misspelled variant.

Proposed archive folder name (do not create yet):
- `D:\Workarea\jobsearch\data\interview_prep\_archive_before_cleanup_2026_05`

## Scope Inspected
- `D:\Workarea\jobsearch\data\interview_prep\ShaekeforceConsulting`
- `D:\Workarea\jobsearch\data\interview_prep\SharkforceConsulting`
- `D:\Workarea\jobsearch\data\interview_prep\active_interviews`

## 1) Folder Tree Summary + Counts

### A. ShaekeforceConsulting (legacy spelling)
Path:
- `D:\Workarea\jobsearch\data\interview_prep\ShaekeforceConsulting`

Top-level tree summary:
- `2026_05_databricks_sr_data_engineer\...` (full package, labs, fast_labs, docs/assets)
- `aCall.md`
- `cover.docx`
- `rec.md`
- `resume.docx`
- `source_of_truth.json`

Counts:
- Total files: `43`

### B. SharkforceConsulting (canonical spelling)
Path:
- `D:\Workarea\jobsearch\data\interview_prep\SharkforceConsulting`

Top-level tree summary:
- `2026_05_databricks_sr_data_engineer\README.md`

Counts:
- Total files: `1`

### C. active_interviews
Path:
- `D:\Workarea\jobsearch\data\interview_prep\active_interviews`

Top-level tree summary:
- Folder: `Tayota2_Abdul\` (contains mixed interview docs/pdf/html/md)
- Files at root:
  - `capitalone_recruiter_2026-04-16.md`
  - `samsung_hm_2026-04-22.md`
  - `Tayota2_Abdultayota_research.md`
  - `toyota_ramya_recruiter_1655.md`
  - `toyota_recruiter_2026-04-21.md`
  - `toyota_technical_interview_roadmap.md`

Counts:
- Total files: `31`
- Total subfolders: `1`

## 2) Duplicate and Unique Analysis (Shaekeforce vs Sharkforce)

Comparison results:
- Shaekeforce files: `43`
- Sharkforce files: `1`
- Common relative paths: `1`
- Exact duplicates (same path + same hash): `0`
- Same path but different content: `1`
- Unique in Shaekeforce: `42`
- Unique in Sharkforce: `0`

Likely duplicate files:
- Relative path in both folders with different content:
  - `2026_05_databricks_sr_data_engineer\README.md`

Unique files:
- Unique to `ShaekeforceConsulting`: all substantive package files (42), including:
  - `01_JOB_BRIEF.md`, `02_MATCH_AND_RISKS.md`, `03_RECRUITER_QA.md`, `04_CLIENT_TECHNICAL_QA.md`, `05_DATABRICKS_CRASH_GUIDE.md`, `06_STORIES_BANK.md`
  - `INTERVIEW_ANSWERS.md`, `JOB_MATCH.md`, `MOCK_QA.md`
  - `labs\...`, `fast_labs\...`, `sharkforce-pyspark-lab-fixed.zip`, and top-level recruiter/resume/support files
- Unique to `SharkforceConsulting`: none

## 3) Recommended Canonical Destination Per Item Type (Plan Only)

- Keep canonical company spelling target:
  - `D:\Workarea\jobsearch\data\interview_prep\SharkforceConsulting`

- Planned destination for legacy Shaekeforce content:
  - Move entire substantive package into canonical path, preserving structure:
    - From `...\ShaekeforceConsulting\2026_05_databricks_sr_data_engineer\*`
    - To   `...\SharkforceConsulting\2026_05_databricks_sr_data_engineer\*`

- For top-level legacy files currently in Shaekeforce root:
  - `aCall.md`, `rec.md`, `cover.docx`, `resume.docx`, `source_of_truth.json`
  - Recommended destination later:
    - Either under `...\SharkforceConsulting\2026_05_databricks_sr_data_engineer\_recruiter_materials\`
    - Or under `...\SharkforceConsulting\_legacy_top_level\` (if you want strict provenance retention)

- For current canonical Sharkforce `README.md` conflict:
  - Manual review and merge required before overwrite.

## 4) active_interviews Classification and Placement Recommendation

### Root files
- `capitalone_recruiter_2026-04-16.md`
  - Class: `ACTIVE`
  - Recommendation: move later to a company-specific canonical folder.
- `samsung_hm_2026-04-22.md`
  - Class: `HISTORICAL`
  - Recommendation: move later to historical company folder under canonical root.
- `Tayota2_Abdultayota_research.md`
  - Class: `DUPLICATE_POINTER`
  - Reason: filename suggests accidental concatenation/overlap with Toyota content.
  - Recommendation: manual review, then move or archive later.
- `toyota_ramya_recruiter_1655.md`
  - Class: `HISTORICAL`
  - Recommendation: move later to Toyota-specific folder.
- `toyota_recruiter_2026-04-21.md`
  - Class: `HISTORICAL`
  - Recommendation: move later to Toyota-specific folder.
- `toyota_technical_interview_roadmap.md`
  - Class: `HISTORICAL`
  - Recommendation: move later to Toyota-specific folder.

### Subfolder
- `Tayota2_Abdul\` (all contained files)
  - Class: `REVIEW_NEEDED`
  - Reason: mixed content, mixed naming (`Tayota` typo, multiple topic docs), and unclear if fully active vs historical.
  - Recommendation: review manually, then split into company-specific folder(s) with canonical naming.

## 5) Risks and Guardrails

Risks:
- Overwriting the one existing file in canonical Sharkforce path (`README.md`) without review could lose intent.
- Mixed Toyota/Tayota naming can cause hidden duplicates and broken references.
- Top-level recruiter documents in Shaekeforce root may lose context if moved without a provenance note.

Guardrails for future execution:
1. Create backup snapshot/archive root first: `D:\Workarea\jobsearch\data\interview_prep\_archive_before_cleanup_2026_05`.
2. Use copy-then-verify hashes before any move.
3. Resolve README conflict explicitly (manual diff/merge).
4. Rename typo paths only after link/reference check.
5. Keep a move log (`source -> destination`) for reversibility.

## 6) Exact Planned Actions (Not Executed)

1. Prepare archive folder (later):
   - `D:\Workarea\jobsearch\data\interview_prep\_archive_before_cleanup_2026_05`
2. Diff and merge:
   - `Shaekeforce...\2026_05_databricks_sr_data_engineer\README.md`
   - `Sharkforce...\2026_05_databricks_sr_data_engineer\README.md`
3. Consolidate all Shaekeforce package files into Sharkforce canonical tree.
4. Relocate Shaekeforce top-level recruiter files into a clearly named canonical subfolder.
5. Normalize `active_interviews` by creating company-specific canonical folders and moving each classified file.
6. Retire empty/legacy folders only after verification (archive first).

Status for this run:
- Planning/reporting only.
- No deletions.
- No moves.
- No renames.
- No `.claude` worktree modifications.
