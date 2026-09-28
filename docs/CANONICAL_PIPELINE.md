> **Superseded overview — Prompt 04.** Use [PIPELINE_OPERATOR.md](PIPELINE_OPERATOR.md)
> for operation and [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md) for verified
> behavior and implementation gaps. The original Prompt 03 overview below is kept
> as history; it overstates enforcement of eligibility, overrides, and provenance.

# Canonical job runner

`job-runner.ps1` is the documented cost-controlled route for one new intake.
Legacy scripts remain available for compatibility.

## Flow

1. Tier 0 writes `score/local_gate.json`, checks exact hashes/raw descriptions in
   both job stores, then runs the existing local FAISS cosine check offline. It
   makes zero paid calls; unavailable FAISS resources block safely.
2. Tier 1 makes at most one structured request using `economy` by default (or the
   selected analysis profile) and writes
   `tailored/job_packet.json` plus `score/llm_gate_report.md`.
3. `triage` stops at the advisory recommendation. Generate requires `PROCEED` or
   an explicit suitability override with a reason; duplicate overrides also need a
   reason.
4. Tier 2 makes at most one structured package request using `quality` by default
   (or the selected generation profile) for resume and
   optional cover content. Local code supplies identity, dates, titles, education,
   and source-locked bullets.
5. Existing local renderers create DOCX/Markdown; a structural/content quality
   boundary runs. Visual DOCX review is still required before submission.
6. Generation ends at `READY_TO_APPLY`. Only `--assume-applied` with `--method`
   and `--date YYYY-MM-DD` writes `application.json` and yields `ASSUMED_APPLIED`.

## Commands

```powershell
. .\env_setter.ps1
.\job-runner.ps1 .\intake\new_job.md -Mode gate
.\job-runner.ps1 .\intake\new_job.md -Mode triage
.\job-runner.ps1 .\intake\new_job.md -Mode generate -Cover
.\job-runner.ps1 .\intake\new_job.md -Mode triage -AnalysisProfile economy_deepseek
.\job-runner.ps1 .\intake\new_job.md -Mode generate -Cover -AnalysisProfile economy_deepseek -GenerationProfile quality_claude
.\job-runner.ps1 .\intake\new_job.md -Mode generate -OverrideDuplicate -Reason "New requisition" -Cover
.\job-runner.ps1 .\intake\new_job.md -Mode generate -AssumeApplied -Method Indeed -Date 2026-09-12 -Notes "Submitted manually"
```

The wrapper prints the job folder, artifact paths, cache hit/miss information,
quality result, and state. `--assume-applied` is never implicit.

## Cache and safety

Cache records under `data/pipeline_cache/` include job hash, runtime-profile hash,
prompt version, model-profile identity, and a result hash. Hits do not call a
provider. Failed or interrupted claims remain non-retryable, and an exclusive
workspace lock prevents concurrent runs. Canonical Tier 1 and Tier 2 each permit
one provider request with no fallbacks. Job text is untrusted data. Structured
schemas, local public-safety checks, and source-locked evidence fail closed.

The runtime profile is the only candidate context sent to models. The renderer
adapter bypasses legacy CLI generation and master-source reloads. Configure local
model IDs before live use; tests use mocks and never contact providers.
