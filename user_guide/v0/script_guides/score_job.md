# Score Job Script Guide (score_job.py)

- **Purpose**: Scores a job posting against your master profile using Grok LLM to assess fit (match %, recommendation, strengths, gaps, advice). Creates a job folder with UUID, moves the intake file, saves the report, and initializes metadata.yaml with PENDING status.

- **Input**: Path to the job intake markdown file in intake/ (e.g., intake/00001.Company.Date.md). File should include Employer_Name, URL, Title, Location, and Contents sections for best parsing.

- **Process**:
  1. Load your master profile (summary, top skills, recent experience) from data/master/ files (ensure profile_export.py has been run after source_of_truth updates).
  2. Extract and clean job text from the markdown file.
  3. Build a structured prompt with profile/job data.
  4. Call Grok LLM for scoring (temperature 0.5, max_tokens 1200).
  5. Print report to console.
  6. Generate UUID and create data/jobs/<uuid>/ folder.
  7. Move original intake file to folder (preserves name e.g., 00001.Company.Date.md).
  8. Copy as raw_intake.md for compatibility.
  9. Save score_report_<timestamp>.md and metadata.yaml (status: PENDING).

- **Outsourcing**: LLM (Grok/xAI) for scoring analysis, with strict prompt format: system role for coaching, user prompt with profile/job details, output in exact markdown structure (Match Score, Recommendation, etc.).

- **Usage**: 
  ```
  python scripts/score_job.py intake/<job_file.md>
  ```
  Optional args:
  - --model <model> (default: grok-3)
  - --temperature <float> (default: 0.5, range 0-1 for determinism/creativity)

  Example:
  ```
  python scripts/score_job.py intake/00001.Collective_Health.02052026.1328.md
  ```

- **User Tip**: Run profile_export.py first if you've updated data/source_of_truth.json. After scoring, check data/jobs/<uuid>/score_report_*.md for details. Use the printed UUID for next steps (e.g., job_decision.py --uuid <uuid> --accept). If error (e.g., FileNotFound), verify data/master/ files exist.