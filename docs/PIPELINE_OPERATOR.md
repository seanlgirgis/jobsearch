# Pipeline operator

Authoritative commands for Sean and Cline. Start with [AGENTS.md](../AGENTS.md).
Use the [Cline runner](../CLINE_JOBSEARCH_RUNNER.md) for execution and the
[reasoner](../CLINE_JOBSEARCH_REASONER.md) for discussion/maintenance. Technical
details are in [architecture](PIPELINE_ARCHITECTURE.md); verification and first
paid-test conditions are in [CUTOVER_REPORT.md](CUTOVER_REPORT.md).

## One job, one step

Replace new_job.md with the actual intake. The wrapper activates Python and uses
its own repository root. Run from the repository root for simple relative paths.

```powershell
Set-Location -LiteralPath 'D:\Workarea\jobsearch'
. .\env_setter.ps1
.\job-runner.ps1 .\intake\new_job.md -Mode gate
.\job-runner.ps1 .\intake\new_job.md -Mode triage
.\job-runner.ps1 .\intake\new_job.md -Mode generate -Cover
```

Run each command separately, inspecting its result before proceeding. Gate writes
a local job shell/report and makes zero provider calls. -DryRun is an alias for
gate-only execution. Eligibility blocks stop all paid stages. Duplicates and
unavailable duplicate checks stop unless explicitly overridden. Runtime source
freshness is automatically verified before analysis, including on cache hits.

Triage makes at most one selected analysis-profile request and stops at TRIAGED. Read the full
job_packet.json and llm_gate_report.md. Generation is an explicit request to
prepare documents; REVIEW/SKIP recommendations require a suitability override.
It records that decision separately from the model recommendation and local gate.
There is no separate accept/reject command; decline by stopping. Omit -Cover for
resume only. Successful generation persists READY_TO_APPLY and prints exact paths.

## Overrides and submission recording

Supply an authorized nonblank reason. Examples are not automatic permission.
The same -Reason value covers both switches when both are supplied.

```powershell
.\job-runner.ps1 .\intake\new_job.md -Mode triage -OverrideDuplicate -Reason "Verified distinct requisition"
.\job-runner.ps1 .\intake\new_job.md -Mode generate -Cover -OverrideSuitability -Reason "Strategic application despite the stated gaps"
```

Repeat a duplicate override on later steps if needed. It does not override
eligibility problems; resolve a closed or incomplete posting first. Decisions,
reasons and analysis references are saved in metadata and the job packet.

Review facts and every DOCX page, then submit externally. When Sean confirms
submission or explicitly requests recording it, use the local apply-only command:

```powershell
.\job-runner.ps1 .\intake\new_job.md -Mode apply -AssumeApplied -Method Indeed -Date 2026-09-12 -Notes "Submitted manually"
```

Use the real method/date/notes. This verifies the completed package, updates only
that job's application record, makes zero provider calls, and does not re-render.
Identical repeated application entries are idempotent; history is retained.
The explicit flags also work with generate when that full workflow is intended.
No command submits to a website. Intake, historical records and previous packages
are retained. Application metadata is authoritative; application.json is its mirror.
The runner does not copy records into data/applied_jobs or rebuild FAISS.

## Model setup and cost

```powershell
. .\env_setter.ps1
python scripts\model_profile.py list
python scripts\model_profile.py show
python scripts\model_profile.py use discussion
python scripts\model_profile.py use economy
```

The active selection affects clients that omit a profile name. This runner defaults
Tier 1 to `economy` and Tier 2 to `quality`, but either stage can use any configured
named profile. Cline's own model is separate.
Configure actual primary IDs in config/model_profiles.local.json using
[model setup](../config/README.md); never store keys there. Use schema-capable
primaries and no fallbacks; the selected generation profile must also set
allow_artifacts=true. Unconfigured IDs,
fallback lists and disabled artifact policy fail before the affected paid call.

For example, after configuring profiles named `economy_deepseek` and
`quality_claude` in the local overlay:

```powershell
.\job-runner.ps1 .\intake\new_job.md -Mode triage -AnalysisProfile economy_deepseek
.\job-runner.ps1 .\intake\new_job.md -Mode generate -Cover -AnalysisProfile economy_deepseek -GenerationProfile quality_claude
```

Default output caps: economy 1,500 tokens; quality 4,500. These are output limits,
not dollar budgets. At most one request per stage/cache key; COMPLETE hits reuse
output without calls. Identity includes provider/model settings, profile hash,
prompt version, schema and request hashes, and package analysis/cover dependencies.
A model or prompt change can therefore incur a fresh call.

runner_result.json and terminal output report cache HIT/MISS, keys, requested
provider/model/profile, call bound, exact paths and a suggested next command.
When a provider supplies them, token usage and actual dollar cost are recorded;
provider-resolved aliases are not. Failed attempts remain claimed: never erase
the ledger to obtain a paid retry.

The terminal normally prints a short human summary. Full JSON remains saved in
the job folder and cache; add `-Json` to `job-runner.ps1` only when you need a
machine-readable result on standard output.

## Output locations

The returned folder is data/jobs/runner_<first-eight-job-hash-characters>. A full
hash comparison detects a conflicting pre-existing folder before writes.

| Within that job folder | Contents |
| --- | --- |
| raw/job_description.md; metadata.yaml | Preserved intake and current tracking |
| score/local_gate.json; score/llm_gate_report.md | Local gate and full readable analysis |
| tailored/job_packet.json | Analysis, separate decisions, Tier 1 provenance |
| runner_result.json | Latest command handoff |
| generated/packages/<package-id>/ | Versioned document package; use returned paths |
| application.json | Explicit application mirror |

Each generated package contains resume_intermediate_v1.json, resume.docx,
resume_preview_v1.md, quality_report.json and artifact_manifest.json. Cover
requests add cover_intermediate_v1.json, cover.docx and cover_preview_v1.md.
The manifest records both stages' provenance and file hashes. Cached reruns
verify completed files and reuse them without overwriting manual edits. A cover
from an older package is never reported as the current resume-only cover.

## Recovery

- BLOCKED: inspect score/local_gate.json and resolve the exact cause; overrides
  require a reason. Gate exit code is 1 when blocked.
- Runtime freshness failure: follow [runtime maintenance](RUNTIME_PROFILE.md).
  Review evidence before rebuilding; do not hand-edit derived context.
- Configuration or provider failure: inspect only the relevant local settings and
  safe error. FAILED_OR_UNCERTAIN/ATTEMPTED claims prevent automatic paid retries.
  Preserve the cache key and request targeted diagnosis.
- Stale lock: read data/pipeline_cache/runner.lock and verify its PID has stopped
  before targeted removal. Never remove an active lock or bulk-clear cache.
- Render failure/changed document: inspect that package's JSON and quality report.
  Partial packages and manual edits are preserved; diagnose before retrying.
  Apply-only refuses missing or modified completed artifacts.
- An interrupted apply may leave application.json behind metadata.yaml. Repeating
  the same explicit apply command repairs the mirror without adding duplicate history.

Errors return code 2. The runner never retries paid failures automatically.
READY_TO_APPLY means local content/structure checks passed; visual review and
judgment about free-form summary/cover claims remain manual.
