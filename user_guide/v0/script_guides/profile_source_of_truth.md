# profile_source_of_truth.py Guide

- **Purpose**: One-time setup to unify your job history into a structured JSON file (data/source_of_truth.json). Includes dates, roles, skills, field names (e.g., standardize "portfolio" vs "website"). Studies existing intake files, unifies data, archives duplicates/unneeded.
- **Input**: User-provided profile data (e.g., via JSON/CSV of jobs, or pasted text). Existing intake files in intake/ for unification.
- **Process**:
  1. Parse user input (jobs, dates, etc.).
  2. Validate: Check for date overlaps (e.g., end_date < next_start_date).
  3. Standardize fields (e.g., map "site" to "website").
  4. Add lookups (e.g., skills list, achievements).
  5. Output JSON; archive old intakes if redundant.
- **Outsourcing**: Minimal — optional LLM for parsing unstructured text into structure, but with strict prompt: "Extract exact dates/roles without changes; flag overlaps."
- **Usage**: `python scripts/profile_source_of_truth.py --profile_input my_jobs.json --output data/source_of_truth.json`. Run once; update manually if profile changes. Follow with profile_export.py for legacy files.
- **User Tip**: After running, review the JSON for accuracy. This file is referenced in all generation steps.