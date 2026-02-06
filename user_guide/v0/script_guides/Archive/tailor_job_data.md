# Tailor Job Data Script Guide (tailor_job_data.py)

- **Purpose**: After accepting a job (via job_decision.py), this script structures and enriches the raw job description for better downstream use: improved RAG retrieval, keyword matching for resume/cover tailoring, and future LLM enhancements. It parses the job text into logical sections (responsibilities, requirements, preferred, benefits) and extracts key skills/keywords using regex patterns. This is Phase 3 in the v0 POC pipeline — bridges scoring/decision to generation.

- **Input**:
  - `--uuid <uuid>` (required): Job UUID from score_job.py (e.g., 28601739-4a44-4f86-8b08-bf8870a42081).
  - `--version <tag>` (optional, default: "v1"): Version tag for the output file (e.g., v1 for basic regex extraction, v2-llm for future LLM-powered version).

- **Process**:
  1. Validates the UUID and loads the job text from `data/jobs/<uuid>/raw_intake.md` (or preserved original filename).
  2. Cleans the text (removes excess whitespace, normalizes line breaks).
  3. Extracts structured sections using regex markers:
     - responsibilities: patterns like "responsibilit(y|ies)", "what you'll do", "key duties"
     - requirements: "require(ments|d)", "qualifications", "must have"
     - preferred: "preferred", "nice to have", "bonus"
     - benefits: "benefit", "perks", "compensation", "remote"
  4. Extracts skills/keywords using a predefined list of patterns (e.g., python, sql, aws, airflow, etc.).
  5. Builds a dictionary with:
     - company, role, location (hardcoded or parsed)
     - extracted sections
     - extracted_skills list
     - placeholders for future LLM fields (e.g., llm_summary, rephrased_bullets)
  6. Creates `tailored/` subfolder in the job directory if needed.
  7. Saves as `tailored/tailored_data_<version>.yaml` (YAML for readability and easy editing).
  8. Prints success message + preview of first 10 extracted skills.

- **Outsourcing**: None in v0 — pure regex and string matching (fast, deterministic, no LLM cost).  
  Future: Optional LLM call (GrokClient) for semantic summarization, bullet rephrasing, or advanced skill prioritization (commented in code).

- **Usage**:
  Standard run (recommended):
  ```powershell
  python scripts/tailor_job_data.py --uuid 28601739-4a44-4f86-8b08-bf8870a42081 --version v1
  ```

  - Omit `--version` → defaults to v1.
  - Re-run with `--version v2` to create a new file (e.g., after script improvements).
  - Example with different tag:
    ```powershell
    python scripts/tailor_job_data.py --uuid <uuid> --version initial
    ```

- **User Tips & Best Practices**:
  - Run **only after acceptance** — script assumes job is in data/jobs/<uuid>/ and has raw_intake.md.
  - Review the output YAML (`data/jobs/<uuid>/tailored/tailored_data_v1.yaml`) for accuracy:
    - Check if sections were captured correctly (some jobs have unusual headings).
    - Verify extracted skills — add missing ones manually if needed.
  - If extraction misses key parts (e.g., odd formatting), edit the YAML directly or improve SECTION_MARKERS/SKILL_PATTERNS in the script.
  - Output example (from your run):
    ```
    Tailored data saved: data\jobs\28601739-4a44-4f86-8b08-bf8870a42081\tailored\tailored_data_v1.yaml
    Extracted skills (6): airflow, data pipeline, go, python, rust, sql ...
    ```
    → Only 6 skills extracted → script is conservative. Future LLM version will catch more.
  - If error (e.g., "No raw_intake.md"): Verify folder contents with `ls data\jobs\<uuid>` and ensure score_job.py completed successfully.
  - Next after tailoring: Generate resume/cover intermediates (e.g., generate_resume.py --uuid <uuid> --version v1).

- **Output Location**:
  - `data/jobs/<uuid>/tailored/tailored_data_v1.yaml`
  - This file becomes input for resume/cover generation scripts (future versions will feed it to LLM prompts).

Run the tailoring command if you haven't already (or re-run with a new version tag if you want). Paste the YAML contents (or key excerpts like extracted_skills, responsibilities) when ready — we'll review it together and proceed to resume/cover generation next.