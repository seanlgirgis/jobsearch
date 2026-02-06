# 01 - Score Job (scripts/01_score_job.py)

**Purpose**  
Score a job posting against your master profile using Grok (xAI) to produce a realistic match percentage (0–100), recommendation, strongest alignments, gaps/risks with mitigations, and tailored advice.  
Creates a structured job folder under `data/jobs/` using the pattern `00001_xxxxxxxx` (sequential 5-digit number + 8-char UUID prefix), copies the intake file, saves the Grok report, and initializes `metadata.yaml` with status `PENDING`.

**Current Status**  
Working / POC-stable (as of Feb 5, 2026)  
Last tested: Collective Health Staff Data Engineer → 92% Strong Proceed

**Input Requirements**  
Markdown file in `intake/` containing at minimum:  
- Employer_Name  
- URL  
- Title  
- Location  
- Full job description (preferably under "Contents:" or raw text)  

Example filename: `00001.Collective_Health.02052026.1328.md`

**Output Folder Structure**  
```
data/jobs/00001_xxxxxxxx/
├── 00001.Collective_Health.02052026.1328.md      # original intake file (copied if --no-move)
├── raw/
│   └── raw_intake.md                             # standardized copy for downstream scripts
├── score/
│   └── score_report_YYYYMMDD_HHMMSS.md           # full Grok markdown response
└── metadata.yaml                                 # core facts + score + status=PENDING
```

**Dependencies**  
- `src/loaders/master_profile.py` → requires valid data in `data/master/` (run `profile_export.py` after updating source_of_truth.json)  
- `src/ai/grok_client.py` → valid xAI API key configured  
- Python packages: argparse, re, shutil, uuid, datetime, pathlib, yaml

**Usage**

```bash
# Basic run (moves file from intake/)
python scripts/01_score_job.py intake/00001.Collective_Health.02052026.1328.md

# Safe for debugging (does NOT move file from intake/)
python scripts/01_score_job.py intake/00001.Collective_Health.02052026.1328.md --no-move

# Custom model / temperature
python scripts/01_score_job.py intake/00001...md --model grok-beta --temperature 0.7
```

**Recommended Workflow**  
1. Update master profile → run `profile_export.py` if needed  
2. Drop new job posting markdown into `intake/`  
3. Run scoring command  
4. Review printed Grok report + saved `score/score_report_*.md`  
5. Check `metadata.yaml` for score, recommendation, company/role auto-parsed from filename  
6. If score ≥ 80–85% and recommendation is "Strong Proceed" or "Proceed" → proceed to accept (phase 02)

**Known Behaviors / Gotchas**  
- Folder naming auto-increments the 5-digit prefix by scanning existing `0000X_xxxxxxxx` folders  
- Company/role parsing is heuristic-based on filename pattern  
- `--no-move` strongly recommended during development  
- `MasterProfileLoader` failure → verify `data/master/` files exist and are valid  
- Grok prompt enforces exact markdown output structure — changes require updating `parse_score_from_response()`

**Related Files**  
- Script: `scripts/01_score_job.py`  
- Example output: `data/jobs/00001_cdb9a3fa/`  
- Profile loader: `src/loaders/master_profile.py`  
- Grok client: `src/ai/grok_client.py`

**Decisions Log References**  
- Naming: `00001_xxxxxxxx` (sequential 5-digit + short UUID)  
- Subfolders: `raw/`, `score/`  
- `--no-move` flag for dev safety