# JobSearch workspace

Sean's job-market workspace for job intake, fit analysis, tailored resumes and
covers, application tracking, gigs, and application interview preparation.

## Start here

1. Read [AGENTS.md](AGENTS.md).
2. Read the shared control plane in [`_agent/`](<./_agent/README.md>).
3. For a new job, use [the canonical operator guide](docs/PIPELINE_OPERATOR.md)
   and `job-runner.ps1`.

```powershell
Set-Location D:\Workarea\jobsearch
. .\env_setter.ps1
.\job-runner.ps1 .\intake\new_job.md -Mode gate
```

Run one stage at a time and inspect its result before continuing.

## Current routes

- Agent rules, memory, state, and handoff: `_agent/`
- Canonical pipeline: `job-runner.ps1` → `scripts/canonical_runner.py`
- Script allowlist: `scripts/README.md`
- Search bots: `search_bots/agent_work/` and `search_bots/documentation/`
- Career truth: `data/master/` and `docs/RUNTIME_PROFILE.md`
- Workspace and archive audits: `docs/WORKSPACE_CONTROL_AUDIT.md` and
  `archive/ARCHIVE_MAP.md`

## Directory discipline

- Put new job postings in `intake/`, not the repository root.
- Put active job records and generated packages under `data/jobs/`.
- Put durable operating policy in `_agent/` and technical documentation in
  `docs/`.
- Treat legacy wrappers, historical guides, scratch material, and archives as
  reference only unless a task explicitly names them.
