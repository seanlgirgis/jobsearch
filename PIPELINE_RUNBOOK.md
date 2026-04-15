# Job Application Pipeline — Runbook
# Last updated: 2026-04-14

===================================================================
  THE NORMAL FLOW — 5 commands, no UUIDs, no arguments to remember
===================================================================

# STEP 1 — Check for duplicates (pass the job file once, never again)
.\job-check.ps1 "D:\StudyBook\temp\jobsearch\intake\intake.md"

# STEP 2 — Score the job (picks up file from step 1 automatically)
.\job-score.ps1

# STEP 3 — Accept it (picks up UUID from step 2 automatically)
.\job-accept.ps1

# STEP 4 — Generate everything: resume + cover letter, opens folder when done
.\job-run.ps1

# STEP 5 — After you've submitted your application, mark it as applied
.\job-apply.ps1

---

That's it. After step 4, Windows Explorer opens the generated\ folder
with your resume_v1.docx and cover_letter.docx. Submit them, then run step 5.

===================================================================
  FIRST-TIME SETUP (one time only, not every session)
===================================================================

Make sure PowerShell can run scripts:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

===================================================================
  OPTIONS YOU CAN PASS
===================================================================

job-score.ps1
    -Model        grok-3 (default)
    -Temperature  0.3 (default)

job-accept.ps1
    -Reject       pass this flag to reject instead of accept
                  Example: .\job-accept.ps1 -Reject

job-run.ps1
    -Model        grok-3 (default)
    -Version      v1 (default)

job-apply.ps1
    -Method       LinkedIn (default) | Indeed | Company Website | Referral | Email
                  Example: .\job-apply.ps1 -Method "Indeed"

===================================================================
  WHERE THE SCRIPTS LIVE
===================================================================

    C:\jobsearch\job-check.ps1
    C:\jobsearch\job-score.ps1
    C:\jobsearch\job-accept.ps1
    C:\jobsearch\job-run.ps1
    C:\jobsearch\job-apply.ps1

Run them FROM C:\jobsearch (the scripts set the directory automatically).
You can run them from anywhere — they always cd to C:\jobsearch first.

===================================================================
  WHERE YOUR OUTPUT FILES ARE
===================================================================

After job-run.ps1 finishes, the folder opens automatically. Files are at:

    C:\jobsearch\data\jobs\NNNNN_xxxxxxxx\generated\
        resume_v1.docx       <- YOUR RESUME       submit this
        cover_letter.docx    <- YOUR COVER LETTER submit this

===================================================================
  HOW THE CACHE WORKS
===================================================================

The scripts share state via:  C:\jobsearch\.job_cache.json

    job-check.ps1  writes: intake_file path
    job-score.ps1  writes: uuid, uuid_short, job_folder
    job-accept.ps1 writes: accepted = true
    job-run.ps1    writes: documents_ready = true
    job-apply.ps1  reads all of the above, then DELETES the cache when done

You never see or touch the cache file. It's automatic.

If something goes wrong and you want to reset:
    Remove-Item C:\jobsearch\.job_cache.json

===================================================================
  GROK API CALLS PER JOB
===================================================================

    job-check   0 calls  (free — local FAISS duplicate check)
    job-score   1 call   (scoring)
    job-accept  0 calls  (free — local state update)
    job-run     4-5 calls (tailor + resume + research + cover letter)
    job-apply   0 calls  (free — local status update)
    ─────────────────────────────────────────────────────────────
    Total       5-6 calls per job

===================================================================
  TROUBLESHOOTING
===================================================================

"running scripts is disabled on this system"
→ Run once in PowerShell as admin:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

"XAI API key missing" / scoring fails
→ Add your key to C:\jobsearch\.env file:
    XAI_API_KEY=your-key-here
→ The scripts load it automatically from that file.

"No cache found. Run job-check.ps1 first."
→ You must run the steps in order. Start from job-check.ps1.

"Job has not been accepted. Run job-accept.ps1 first."
→ Run .\job-accept.ps1 before .\job-run.ps1

"Documents not ready. Run job-run.ps1 first."
→ Run .\job-run.ps1 before .\job-apply.ps1

"Duplicate detected"
→ You already processed this job. Check C:\jobsearch\data\jobs\
  for the existing folder with your resume.

===================================================================
  ADVANCED — Re-run one specific step on an existing job
===================================================================

If you already ran the pipeline but want to regenerate something:

    # Re-generate resume only
    cd C:\jobsearch
    $env:PYTHONPATH = "C:\jobsearch"
    $env:PYTHONIOENCODING = "utf-8"
    C:\py_venv\JobSearch\Scripts\python.exe scripts\04_generate_resume_intermediate.py --uuid XXXXXXXX --model grok-3
    C:\py_venv\JobSearch\Scripts\python.exe scripts\05_render_resume.py --uuid XXXXXXXX --version v1 --all

    # Re-run everything from step 03 onward
    C:\py_venv\JobSearch\Scripts\python.exe scripts\10_auto_pipeline.py --uuid XXXXXXXX --model grok-3 --method "LinkedIn"

Replace XXXXXXXX with the 8-char ID from the folder name in C:\jobsearch\data\jobs\
