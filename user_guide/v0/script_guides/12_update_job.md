# 12 - Update Job (scripts/12_update_job.py)

**Purpose**  
This script is a powerful command-line tool for managing your job applications. It allows you to **search, update, and track** jobs using natural language queries instead of obscure UUIDs.

**Key Features**  
*   **Fuzzy Search**: Find jobs by Company Name, Role, or Status (e.g., "CVS", "Engineer").
*   **Boolean Logic**: Use `OR` to search multiple groups (e.g., `Google OR Amazon`). Spaces act as `AND`.
*   **Direct UUID**: Bypass search if you know the ID.
*   **History View**: See a full timeline of all updates for a job.
*   **Search Only**: Preview matches without triggering an update.

**Usage**

### 1. Basic Update (Status & Notes)
Find a job and update its status.
```bash
# Sets status to "INTERVIEW" for the best match for "CVS"
python scripts/12_update_job.py CVS --status INTERVIEW
```

### 2. Search Logic (AND / OR)
*   **Space = AND**: `CVS Engineer` finds jobs matching *both* "CVS" and "Engineer".
*   **OR**: `Google OR Amazon` finds jobs matching *either* "Google" or "Amazon".
*   **Complex**: `Data Engineer OR Analyst` finds jobs matching ("Data" AND "Engineer") OR ("Analyst").

```bash
python scripts/12_update_job.py Data Engineer OR Analyst
```

### 3. View History Trail
See the full timeline of events for a job.
```bash
python scripts/12_update_job.py Agile --history
```
*Output:*
```text
📜 History Trail: Agile Engine - Data Engineer
📁 Path: C:\jobsearch\data\jobs\00007_31466164
============================================================
[2026-02-06] Applied
   └─ Pipeline application
------------------------------
[2026-02-10] REJECTED
   └─ Email update: Added to talent pool...
```

### 4. Search Only (Safe Mode)
List matches without prompting for ANY changes. Useful for checking what exists.
```bash
python scripts/12_update_job.py Amazon --search-only
```

### 5. Direct UUID Lookup
If you have the UUID (from a previous search or file), targeting it directly is faster.
```bash
python scripts/12_update_job.py --uuid 338f7341 --status OFFER
```

### 6. Backdating an Update
You can specify the date of the event if it happened in the past.
```bash
python scripts/12_update_job.py Agile --status REJECTED --date 2026-02-01 --note "Received rejection email last week"
```

**Arguments**

| Argument | Description |
| :--- | :--- |
| `query` | Search terms. Space separated (AND). Use `OR` for multiple groups. |
| `--uuid` | Target specific job by UUID (bypasses search). |
| `--status` | value | Update the job's current status (e.g., APPLIED, REJECTED, OFFER). Syncs to both `status` and `application.last_status`. |
| `--date YYYY-MM-DD` | Date of the update/event. Defaults to today. |
| `--note "text"` | Add a note to the history log. |
| `--followup YYYY-MM-DD` | Set a Next Follow-up Date. |
| `--search-only` | List matches and exit. No changes, no interactive prompts. |
| `--history` | Print the full history trail of the job. |

**Related Files**  
*   `data/jobs/{id}/metadata.yaml`: The file being updated.
*   `scripts/12_update_job.py`: The script itself.
