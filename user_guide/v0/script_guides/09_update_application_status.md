# 09 - Update Application Status (scripts/09_update_application_status.py)

**Purpose**  
Phase 9 in the pipeline: Manages the lifecycle of the job application *after* generation.  
It serves as a "CRM" for your job search, storing all events in `metadata.yaml`.

**Key Capabilities**
1.  **Apply**: Records the initial submission (Date, Method, Notes).
2.  **Status**: Updates the current state (e.g., "Interviewing", "Rejected").
3.  **Track**: Lists pending follow-ups across *all* jobs.

**Input Requirements**  
*   Job folder with `metadata.yaml`.

**Output**  
*   Updates `data/jobs/<uuid>/metadata.yaml` with:
    *   `application` block (applied date, method, history log).

**Usage**

### 1. Manual Run (Subcommands)
```bash
# Record that you just applied
python scripts/09_update_application_status.py --uuid cdb9a3fa apply --method "LinkedIn" --notes "Easy Apply"

# Update status later
python scripts/09_update_application_status.py --uuid cdb9a3fa status --new-status "Interview" --notes "Phone screen w/ HR"

# View history
python scripts/09_update_application_status.py --uuid cdb9a3fa show

# List all pending follow-ups (UUID ignored but required)
python scripts/09_update_application_status.py --uuid x list-pending
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) runs this Step 9 as the final action to mark the job as "Applied".
*   **Command used by auto-runner**:
    ```python
    python scripts/09_update_application_status.py --uuid <uuid> apply --date <today> --method <method> --notes <notes>
    ```

**Related Files**  
- Script: `scripts/09_update_application_status.py`  
- Data: `data/jobs/<uuid>/metadata.yaml`
