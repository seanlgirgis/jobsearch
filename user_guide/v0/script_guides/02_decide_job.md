# 02 - Decide Job (scripts/02_decide_job.py)

**Purpose**  
This script records your decision on a scored job. It updates the job's status in `metadata.yaml` to **ACCEPTED**, **REJECTED**, or **PENDING** (Hold). It also appends a timestamped note explaining the decision.

This step acts as a gatekeeper: only "ACCEPTED" jobs typically move forward to the tailoring and generation phases.

**Key Capabilities**
1.  **Status Update**: Changes the job status in `metadata.yaml`.
2.  **Audit Trail**: Appends a reason and timestamp to the `notes` field.
3.  **Flexible UUIDs**: Accepts full UUIDs or short (8-char) prefixes.

**Input Requirements**  
*   Job folder must exist (created by Script 01).
*   `metadata.yaml` must exist in that folder.

**Output**  
Updates `data/jobs/<uuid>/metadata.yaml`:
*   `status`: Updated to `ACCEPTED`, `REJECTED`, or `PENDING`.
*   `notes`: Appended with "• [Reason] (YYYY-MM-DD)".
*   `last_decision_at`: ISO timestamp of the decision.

**Usage**

### 1. Manual Run
```bash
# Accept a job (proceed to tailoring)
python -m scripts.02_decide_job --uuid cdb9a3fa --accept --reason "Strong fit for Python role"

# Reject a job (stop processing)
python -m scripts.02_decide_job --uuid cdb9a3fa --reject --reason "Too much legacy code"

# Hold a job (maybe later)
python -m scripts.02_decide_job --uuid cdb9a3fa --hold --reason "Waiting on referral"
```

### 2. Via Auto Pipeline
The automation script (`scripts/10_auto_pipeline.py`) automatically **ACCEPTS** the job to allow the pipeline to continue without interruption.
*   **Command used by auto-runner**:
    ```python
    python -m scripts.02_decide_job --uuid <uuid> --accept --reason "Auto-accepted by pipeline"
    ```
*   This ensures that every job run through the auto-pipeline is ready for tailoring and resume generation immediately.

**Arguments**
*   `--uuid`: The job's UUID (or first 8 chars).
*   `--accept` / `--reject` / `--hold`: **Required**. The decision.
*   `--reason`: **Optional**. A text note. If omitted, a default note is used.
*   `--dry-run`: Preview changes without saving.

**Related Files**  
- Script: `scripts/02_decide_job.py`  
- Metadata: `data/jobs/<uuid>/metadata.yaml`  
- Orchestrator: `scripts/10_auto_pipeline.py`