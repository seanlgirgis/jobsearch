# 09 - Update Application Status (scripts/09_update_application_status.py)

**Purpose**  
Phase 9 in the pipeline: Manages the lifecycle of the job application *after* the resume has been generated.  
It serves as a "CRM" for your job search, allowing you to:
- Record when and how you applied.
- Update the status (e.g., "Interview Scheduled", "Rejected", "Offer").
- Log notes and history of interactions.
- Set and track follow-up dates.

All data is stored persistently in the job's `metadata.yaml` file.

**Current Status**  
Working / Stable (as of Feb 5, 2026)

**Input Requirements**  
- Job folder in `data/jobs/` (pattern `0000X_xxxxxxxx` or similar).  
- Existing `metadata.yaml` in that folder (created during Phase 1/2).

**Output**  
- Updates `data/jobs/0000X_xxxxxxxx/metadata.yaml` with:
  - `application` dictionary containing:
    - `applied`: boolean
    - `applied_date`: YYYY-MM-DD
    - `applied_method`: string (e.g. "LinkedIn")
    - `last_status`: string
    - `history`: list of status change events
    - `followup_date`: YYYY-MM-DD (optional)

**Usage**

The script uses subcommands: `apply`, `status`, `show`, and `list-pending`.

```bash
# 1. Record a new application
python scripts/09_update_application_status.py --uuid cdb9a3fa apply --date 2026-02-05 --method "Company Site" --notes "Tailored cover attached"

# 2. Update status (e.g., got an interview)
python scripts/09_update_application_status.py --uuid cdb9a3fa status --new-status "Interview Scheduled" --notes "Feb 12 phone screen with HR"

# 3. View current status and history for a job
python scripts/09_update_application_status.py --uuid cdb9a3fa show

# 4. List ALL jobs with pending follow-ups
python scripts/09_update_application_status.py --uuid dummy list-pending
# (Note: --uuid is required by the parser but ignored for 'list-pending', so you can pass any dummy value)
```

**Behavior**  
- **Apply**: Sets initial `applied` flag and records the method/date. Adds initial entry to history.  
- **Status**: Updates current status and appends a new event to the `history` list.  
- **Show**: Prints a clean summary of the application state, including a chronological history of changes.  
- **List Pending**: Scans *all* job folders in `data/jobs` for any with a `followup_date`.  

**Known Behaviors / Gotchas**  
- **UUID Requirement**: The `--uuid` argument is currently global and required, even for `list-pending` (where it isn't logically needed). Pass `x` or `dummy` if just running `list-pending`.  
- **Date Format**: Expects dates in `YYYY-MM-DD` format.  
- **Metadata dependency**: Fails if `metadata.yaml` is missing (i.e., you can't track an application for a job that hasn't been ingested).

**Related Files**  
- Script: `scripts/08_update_application_status.py`  
- Data: `data/jobs/0000X_xxxxxxxx/metadata.yaml`  
