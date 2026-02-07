# 01 - Score Job (scripts/01_score_job.py)

**Purpose**  
The entry point of the pipeline. It parses a raw job posting, compares it against your master profile using an LLM (Grok/xAI), and produces a "Score Report" with a match percentage (0–100) and recommendation.

Crucially, it **initializes the job folder** structure and generates the **Job UUID** that tracks the application through the entire system.

**Key Capabilities**
1.  **Scoring**: Generates a detailed match report (Strengths, Gaps, Advice).
2.  **Parsing**: Extracts metadata (Company, Role, Website, Location) from both the filename and the file's front matter.
3.  **Automation Ready**: Outputs a machine-parsable `🆔 Job UUID:` line used by `scripts/10_auto_pipeline.py`.

**Input Requirements**  
Markdown file in `intake/` containing the job description.
*   **Filename Convention**: `0000X.Company.Role.Date.Time.md` (e.g., `00001.DeepMind.Senior_Reseacher.02062026.1328.md`)
*   **Front Matter**: The script scans the top of the file for lines like:
    ```text
    Company_website: https://careers.google.com
    Location: Remote
    ```
    (This metadata is saved to `metadata.yaml` for later use by the Cover Letter generator).

**Output folder Structure**  
Creates `data/jobs/00001_xxxxxxxx/` (where `xxxxxxxx` is the short UUID):
```
data/jobs/00001_cdb9a3fa/
├── 00001.Company...md                 # Original intake file (moved from intake/)
├── raw/
│   └── raw_intake.md                  # Standardized copy
├── score/
│   └── score_report_YYYYMMDD.md       # Full Grok analysis
└── metadata.yaml                      # Core DB record (UUID, Status, Score, Website, etc.)
```

**Usage**

### 1. Manual Run (Standalone)
```bash
# Standard run (moves file from intake/ to data/jobs/...)
python scripts/01_score_job.py intake/00001.JobFile.md

# Dev Mode (Keeps file in intake/ for re-running)
python scripts/01_score_job.py intake/00001.JobFile.md --no-move

# Custom Model
python scripts/01_score_job.py intake/00001.JobFile.md --model grok-3 --temperature 0.7
```

### 2. Via Auto Pipeline (Recommended)
This script is automatically called as **Step 1** by the auto-runner:
```bash
# The runner captures the UUID from script 01's output to trigger steps 02-09
python scripts/10_auto_pipeline.py intake/00001.JobFile.md
```

** stdout Integration**  
The script prints the following line, which is critical for the automation pipeline:
`🆔 Job UUID: e4648120-....`
*Do not remove or change this print statement if you modify the script, as script 10 relies on it.*

**Related Files**  
- Script: `scripts/01_score_job.py`  
- Profile Loader: `src/loaders/master_profile.py`  
- Orchestrator: `scripts/10_auto_pipeline.py`