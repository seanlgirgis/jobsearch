# 02 - Decide Job (scripts/02_decide_job.py)

**Purpose**  
Update the decision/status of a scored job to ACCEPTED, REJECTED, or PENDING (hold).  
Appends a reason/note to `metadata.yaml` with timestamp.  
Used after reviewing the Grok score report to commit to next steps (tailoring/application) or archive the opportunity.

**Current Status**  
Working / stable (as of Feb 5, 2026)  
Successfully tested: accepted Collective Health role → status updated, note appended

**Input Requirements**  
- Existing job folder in `data/jobs/` matching pattern `0000X_xxxxxxxx` or containing the UUID  
- `metadata.yaml` present (created by `01_score_job.py`)

**Supported Actions**  
- `--accept`   → status = ACCEPTED  
- `--reject`   → status = REJECTED  
- `--hold` / `--pending` / `--later` → status = PENDING  
Exactly one action flag is required.

**Output**  
Updates `metadata.yaml` in the job folder:  
- `status` field changed  
- `notes` field appended with bullet + reason + date  
- `last_decision` and `last_decision_at` fields added/updated  

**Usage**

```bash
# Accept with reason
python -m scripts.02_decide_job --uuid cdb9a3fa --accept --reason "Strong ETL/Snowflake match + Plano location"

# Reject example
python -m scripts.02_decide_job --uuid cdb9a3fa --reject --reason "Requires 3 days/week on-site"

# Hold / pending
python -m scripts.02_decide_job --uuid cdb9a3fa --hold --reason "Waiting for referral confirmation"

# Short UUID prefix works (first 8 chars)
python -m scripts.02_decide_job --uuid cdb9a3fa --accept --reason "Proceed"

# Dry-run (preview without saving)
python -m scripts.02_decide_job --uuid cdb9a3fa --accept --reason "Test" --dry-run
```

**Behavior**  
- Resolves folder using full UUID or short prefix (`*_${uuid[:8]}`)  
- Shows before/after preview of status + note  
- Appends note as bullet with date (YYYY-MM-DD)  
- Adds `last_decision` and `last_decision_at` for traceability  
- Safe: aborts on missing folder/file, invalid YAML, etc.

**Known Behaviors / Gotchas**  
- Requires exactly one of `--accept` / `--reject` / `--hold`  
- `--reason` is optional (falls back to default phrase)  
- Uses system date for note timestamp  
- Folder lookup prefers exact UUID match, then short prefix  
- Multiple short-prefix matches → error (rare)

**Related Files**  
- Script: `scripts/02_decide_job.py`  
- Updated file: `data/jobs/00001_cdb9a3fa/metadata.yaml`  
- Predecessor: `scripts/01_score_job.py`  
- Next typical step: tailoring script (03) after ACCEPTED

**Decisions Log References**  
- Status values: ACCEPTED / REJECTED / PENDING (uppercase)  
- Note format: bullet + reason + (YYYY-MM-DD)  
- UUID resolution: full or prefix (8 chars)  
- Added `--dry-run` for safety during testing