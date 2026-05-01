# JobSearch Chat Reconstruction (Dummy Expanded)

This file is a reconstructed, expanded stand-in of the old chat so it can be used as the operational context in the current repo location.

- Original recovered source: `D:/Workarea/StudyBook/recovered_chats/00_Resume_maker_helper.md`
- New canonical workspace: `D:/Workarea/jobsearch`
- Purpose: fast onboarding, continuity, and execution without re-reading full raw transcript.

---

## 1) What This Reconstructed Chat Covers

The original thread documented the transition from a mostly API-driven job pipeline to a hybrid workflow:

1. Keep the existing repo pipeline structure and artifact discipline.
2. Replace only the expensive/AI-heavy generation steps.
3. Use ChatGPT Project (`MyFuture` / `JobSearch`) as the strategic and artifact-generation brain.
4. Keep Codex/local scripts for file placement, rendering, validation, and tracking.

This reconstruction is intentionally expanded and normalized for readability.

---

## 2) Core Decision (Final Architecture)

### Keep these pipeline strengths unchanged
- Duplicate checks
- Step sequencing
- Folder discipline per job
- Intermediate file contracts
- Resume and cover DOCX rendering
- Application status tracking

### Replace these AI-brain steps with ChatGPT-generated artifacts
- `scripts/01_score_job.py`
- `scripts/03_tailor_job_data.py`
- `scripts/04_generate_resume_intermediate.py`
- `scripts/07_generate_cover_intermediate.py`
- Optional: `scripts/06_company_research.py`

### Practical operating model
- ChatGPT handles judgment + structured outputs.
- Local repo/pipeline handles deterministic mechanics.

---

## 3) Runtime Flow (Human-in-the-loop)

1. Put posting text in `intake/intake.md`.
2. Run duplicate check.
3. If clear, use ChatGPT Project by mode to generate artifacts.
4. Import/place artifacts into job folder.
5. Run existing rendering and tracker steps.

---

## 4) Standard Commands Used in Thread

From repo root (`D:/Workarea/jobsearch`):

```powershell
Set-Location D:\Workarea\jobsearch
.\env_setter.ps1
.\job-check.ps1 .\intake\intake.md
.\job-score.ps1
```

Continuation depending on verdict and branch of workflow:

```powershell
.\job-accept.ps1
.\job-run.ps1
.\job-apply.ps1
```

V2/manual-artifact workflow exists for importing ChatGPT outputs when bypassing direct API steps.

---

## 5) ChatGPT Project Mode System (as established)

Mode IDs used:
- `A1` = Discuss/advise only
- `B1` = Score job
- `C1` = Tailor resume inputs + resume intermediate output
- `D1` = Cover letter intermediate output

### Typical call pattern

```text
MODE_ID: B1
JOB:
<paste posting>
```

```text
MODE_ID: C1
JOB:
<paste posting>
```

```text
MODE_ID: D1
JOB:
<paste posting>
```

---

## 6) Artifact Contracts (Pipeline-facing)

### Score
- `score_report.md`
- Must include match score and recommendation sections in predictable headings.

### Tailor + Resume intermediate
- `tailored_data_v1.yaml`
- `resume_intermediate_v1.json`

### Cover intermediate
- `cover_intermediate_v1.json`

### Optional research
- company research artifact (if used by your branch/scripts)

Important rule carried from thread:
- Do not invent career facts; use source-of-truth profile data only.

---

## 7) MyFuture Source Awareness (Operational Memory)

The thread established that project context files and chat exports should be cached locally so this repo has durable memory.

Expected location:
- `docs/chatgpt_projects/MyFuture/`
- `docs/chatgpt_projects/MyFuture/chats/`

Expected support files:
- source registry (tracks canonical files and freshness)
- chat cache index (tracks imported chat transcripts)

Goal:
- Make Codex aware of current ChatGPT project materials and prompt for refresh when stale.

---

## 8) Working Directory + Portability Rule

Thread outcome:
- Operate from repo root as default.
- Prefer repo-relative paths for project assets.
- One permitted absolute path convention was discussed for shared Python env (`C:/pyenv/...`) to simplify multi-machine setup.

Current effective working root for this chat:
- `D:/Workarea/jobsearch`

---

## 9) Known Issues/Notes Captured in the Old Thread

- A PowerShell parse error occurred due to encoding/punctuation in output text (em dash parsing issue in one shell context).
- Duplicate check itself ran successfully once shell/environment handling was corrected.
- There were notes about minor script messaging/version mismatches in pipeline wrappers.

---

## 10) “As-if Original Chat” Snapshot

If we treat this file as the canonical replacement of the old long thread, the active intent is:

1. Continue job processing from `D:/Workarea/jobsearch`.
2. Use ChatGPT mode calls to generate intermediate artifacts.
3. Keep existing renderer/tracker infrastructure unchanged.
4. Maintain synced `MyFuture` source/cache documents in-repo.

---

## 11) Ready-to-Use Quick Procedure

```text
A) Local prep
- cd D:/Workarea/jobsearch
- ./env_setter.ps1
- ./job-check.ps1 ./intake/intake.md

B) ChatGPT scoring
- MODE_ID: B1 + JOB text
- Decide proceed/hold/skip

C) If proceed
- MODE_ID: C1 + JOB text
- MODE_ID: D1 + JOB text
- Save artifacts into pipeline-expected paths

D) Finish pipeline
- render resume
- render cover
- update tracking/apply status
```

---

## 12) Why This Dummy Expansion Exists

- Replaces a very large transcript with an operationally equivalent, easier-to-read canonical reference.
- Supports new working-directory context without losing prior decisions.
- Keeps continuity between ChatGPT project strategy and local pipeline execution.

