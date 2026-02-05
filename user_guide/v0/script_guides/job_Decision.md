# Job Decision Script Guide (job_decision.py)

- **Purpose**: Updates the status of a scored job to ACCEPTED, REJECTED, or PENDING (hold). Appends a reason/note to the job's metadata.yaml. This is the manual decision gate after scoring — only accepted jobs proceed to tailoring, resume/cover generation, and tracking.

- **Input**: 
  - `--uuid <uuid>` (required): The job UUID printed by score_job.py (e.g., 28601739-4a44-4f86-8b08-bf8870a42081).
  - One of: `--accept`, `--reject`, or `--hold` (mutually exclusive, required).
  - `--reason` or `--note` (optional): Text explaining the decision (appended to existing notes in metadata.yaml).

- **Process**:
  1. Validates the UUID and checks for data/jobs/<uuid>/metadata.yaml (must exist from score_job.py).
  2. Loads current metadata (status, notes, etc.).
  3. Determines new status:
     - `--accept` → ACCEPTED (default note: "Accepted - proceeding to tailoring")
     - `--reject` → REJECTED (default note: "Rejected")
     - `--hold` → PENDING (default note: "Held for later review")
  4. Appends the provided reason/note (or default) to the notes field.
  5. Saves updated metadata.yaml.
  6. Prints success message with old → new status and the added note.

- **Outsourcing**: None — pure file I/O and YAML handling. No LLM calls.

- **Usage**:
  Basic examples:
  ```powershell
  # Accept a job and add reason
  python scripts/job_decision.py --uuid 28601739-4a44-4f86-8b08-bf8870a42081 --accept --reason "Strong 85% match; Plano location; excellent SQL/Python/ETL alignment; gaps mitigable"

  # Hold for later review
  python scripts/job_decision.py --uuid <uuid> --hold --reason "Review salary range next week"

  # Reject
  python scripts/job_decision.py --uuid <uuid> --reject --reason "Too much people management required"
  ```

  Shortcuts / aliases:
  - `--hold`, `--visit-later`, or `--pending` all set status to PENDING.

- **User Tips & Best Practices**:
  - Always run score_job.py first — it creates the UUID and metadata.yaml.
  - Check status before running: open data/jobs/<uuid>/metadata.yaml or run `ls data/jobs/<uuid>`.
  - Use descriptive reasons — they are appended forever and help later review.
  - After --accept: Proceed to `tailor_job_data.py --uuid <uuid> --version v1`, then generate resume/cover.
  - If error "metadata.yaml not found": Verify UUID (copy exactly from score_job.py output) and that the job was scored successfully.
  - Future enhancement idea: Add --cleanup-on-reject flag to move rejected jobs to intake/rejected/.

- **Output Example** (what you just saw):
  ```
  Updating job: 28601739-4a44-4f86-8b08-bf8870a42081
  Metadata file: data\jobs\28601739-4a44-4f86-8b08-bf8870a42081\metadata.yaml
  Success!
    Status: PENDING → ACCEPTED
    Note added/appended: Strong 85% match; Plano location; excellent SQL/Python/ETL alignment; gaps mitigable
    Updated file: data\jobs\28601739-4a44-4f86-8b08-bf8870a42081\metadata.yaml
  ```

Next step after acceptance: Run tailoring to prepare the job data for resume/cover generation.

```powershell
python scripts/tailor_job_data.py --uuid 28601739-4a44-4f86-8b08-bf8870a42081 --version v1
```

Paste the output when done, and we'll move to generating the resume/cover intermediates.