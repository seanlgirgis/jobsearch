# Prompt 05 cutover report

Completed: `05_tests_cutover.md` — Tests, Cutover and Data Safety Audit.

Recommendation: **conditional GO for one economy-only OpenRouter triage smoke
test**. The local pipeline passes the checks below. **Do not run the paid test
yet with the current configuration:** economy/quality model IDs remain null.
Configure an account-available, schema-capable economy model and review the single
job's local gate first. No real keys were used and no paid requests were made in
this task. Provider availability, billing and live schema acceptance remain untested.

## Observed verification

| Check | Observed result |
| --- | --- |
| Full offline suite | 68 tests passed: 25 canonical, 27 provider/profile, 16 runtime |
| Exact duplicate | Stopped before HTTP; normalization and historical metadata preservation checked |
| Duplicate override | Reason persisted; analysis continued through one mocked request |
| Eligibility | Closed/short intake stopped before paid stages, including with duplicate override |
| Tier 1 | Actual SDK through mocked HTTP, schema-valid packet, full readable report, triage stop |
| Suitability override | Original SKIP retained separately; explicit acceptance/reason recorded; package continued |
| Tier 2 | One mocked quality response, actual source materialization, real local resume and cover DOCX creation |
| Repeat generation | Real cache HIT for both stages; no extra HTTP and no rerender; document bytes unchanged |
| Model/request change | Cache keys changed; requested provider/model/profile persisted |
| Application | READY_TO_APPLY by default; explicit generate/apply flag recorded only the target job; history and unrelated records preserved |
| Apply-only | Zero model/render calls; identical repeats did not duplicate history; valid calendar date required |
| Failure protection | Failed attempt not retried; malformed/public-unsafe output blocked; changed artifacts preserved and application blocked |
| Local FAISS | Actual FAISS search tested with synthetic embeddings; separate read-only real-index/cached-model check returned CLEAR, zero matches |
| Runtime freshness | Standalone --check passed: 7,849 bytes, 13 bullets, zero prohibited client references |
| Source constraints | Runtime tests verified research qualification, foundational tool caps and provenance |
| Syntax/style | Python formatting and Ruff passed; wrapper PowerShell parsed; CLI help verified |

The existing pipeline tests previously replaced the cache with a mock, so they
did not establish repeat-call behavior. They were replaced with tests that run the
gate, cache, client, validation and renderer code in temporary workspaces. Only
provider HTTP and the normal semantic embedding boundary are substituted; an
additional test executes real FAISS search. Socket guards and synthetic keys
prevent provider access. DOCX tests verify structure/content, not page images.

Initial diagnostic reproduced the known bug: an eligibility-only BLOCKED gate
returned allowed=True. That defect and the unreachable suitability-reason check
are fixed. Two unused test imports flagged by Ruff were removed; final lint passed.
FAISS emitted SWIG deprecation warnings; its test and local index check succeeded.

Commands executed (environment activated in each Python shell):

```powershell
. .\env_setter.ps1
python -m unittest tests.test_canonical_pipeline -v
python -m unittest discover -s tests -p 'test_*.py' -q
python -m black --check --line-length 100 scripts\canonical_runner.py src\pipeline tests\test_canonical_pipeline.py
python -m ruff check scripts\canonical_runner.py src\pipeline tests\test_canonical_pipeline.py
python scripts\build_runtime_profile.py --check
python scripts\model_profile.py list
python scripts\canonical_runner.py --help
```

Also executed a read-only `semantic_check` against the repository's existing
FAISS index with synthetic query text. The runtime builder was exercised in
temporary fixtures; the repository's already-valid generated profile was checked
without rewriting master files.

## Changes and data audit

- `scripts/canonical_runner.py`, `job-runner.ps1`: enforced gates/reasons,
  automatic source validation, persisted decisions/states, apply-only, dry-run,
  explicit repository root, full-hash collision checks and durable handoff.
- `src/pipeline/storage.py`, `contracts.py`, `artifacts.py`: complete request
  cache identity, single-primary routing policy, request provenance, updated
  prompt namespace, immutable completed package reuse and artifact manifests.
- `tests/test_canonical_pipeline.py`: 25 integration/regression checks replacing
  the earlier five cache-mocked checks.
- `docs/PIPELINE_OPERATOR.md`, `docs/PIPELINE_ARCHITECTURE.md`,
  `docs/RUNTIME_PROFILE.md`, `CLINE_JOBSEARCH_RUNNER.md`, `config/README.md`,
  `CURRENT_STATE.md`: current commands, behavior, status and remaining limitations.
- `docs/CUTOVER_REPORT.md`: this report and the first-real-test checklist.

Before/after audit covered **7,522 files** across `data/jobs`, `data/applied_jobs`,
`data/master` and `resume_output`. All paths and content hashes matched.
Aggregate SHA-256:
`E65575F607C87E0DF63E0F9A6FDA350522788809AEC173F36196EA176793B157`.
No historical jobs, resumes, master evidence or material data were deleted.
Legacy Grok source hash remains
`54DB713AC7F521B743766FAE06C091813E6FBB6EE4434DED8100ED44D7FED50D`.

No material cleanup was warranted. The new `canonical-v2-cutover` cache namespace
excludes prior cache identities without deleting them. Legacy operational guides
retain their deprecation notices; AGENTS/driver redirect to the operator runbook.

## Retained paths excluded from the active route

| Legacy path | Reason to avoid as the normal route |
| --- | --- |
| `scripts/10_auto_pipeline.py`, `scripts/10b_force_pipeline.py` | Multi-call generation/research and application update; force variant bypasses duplicates |
| `scripts/01_score_job.py`, `03_tailor_job_data.py`, `04_generate_resume_intermediate.py`, `06_company_research.py`, `07_generate_cover_intermediate.py` | Legacy paid stages and model defaults; not routed through the canonical cache |
| `src/ai/grok_client.py` | Legacy grok-3/grok-3-mini defaults; its executable smoke example makes requests |
| `03.job-chatgpt-render.ps1` | Legacy render flow invokes application-status update |
| `00.job-chatgpt-check.ps1`, `01.job-chatgpt-check.ps1`, `02.job-chatgpt-accept.ps1`, `ps1_keep/` | Older state/cache conventions; no canonical cutover guarantees |
| `AGENTS_CONTEXT.md`, `PIPELINE_RUNBOOK.md`, `PIPELINE_SELF_RUN.md`, old driver/MyFuture/canonical overview | Historical instructions with explicit redirects |

Legacy code is preserved. The canonical adapter reuses pure local renderer
functions from 05/08 and quality_check.py, not their old generation wrappers.

## Canonical commands and first real test

Checklist before spending:

1. Save one complete, public job posting as `intake/smoke_test.md`; this task did
   not create a real-job intake. Review it for private data before sending it.
2. In `config/model_profiles.local.json`, configure only the desired economy
   primary's exact OpenRouter model ID, schema support, empty fallbacks and a
   bounded output cap (default 1,500). Verify provider pricing/account access.
   Keep the OpenRouter key in `.env`; do not paste it into prompts or reports.
3. Run the local gate below and inspect its report. Stop on duplicates, closed
   postings or unavailable checks unless a specific permitted override is justified.
4. When Sean is ready, run **triage only**. It can make one paid request on a miss.
   Do not add generate, cover or application flags to this first smoke test.
5. Expect TRIAGED, a schema-valid packet and readable report, economy/OpenRouter
   provenance, and a cache MISS. Repeat the identical triage only if the first
   completed successfully; expect HIT and no new provider request. Check actual
   charge in the provider's records; the pipeline does not collect dollar usage.

```powershell
Set-Location -LiteralPath 'D:\Workarea\jobsearch'
. .\env_setter.ps1
.\job-runner.ps1 .\intake\smoke_test.md -Mode gate
```

Exact paid smoke command after setup and a clear gate:

```powershell
.\job-runner.ps1 .\intake\smoke_test.md -Mode triage
```

Later, after explicit acceptance and quality-model setup, generate and record a
submission as separate steps. Replace the intake/date/method/notes with actuals:

```powershell
.\job-runner.ps1 .\intake\smoke_test.md -Mode generate -Cover
.\job-runner.ps1 .\intake\smoke_test.md -Mode apply -AssumeApplied -Method Indeed -Date 2026-09-12 -Notes "Submitted manually"
```

## Recovery and remaining limitations

Stop after an error and inspect the named report/ledger. Never remove ATTEMPTED
or FAILED_OR_UNCERTAIN claims to force another paid call. Preserve incomplete
packages and edited documents for diagnosis. Remove a stale lock only after
verifying its PID is no longer running. If application.json lags metadata after
interruption, the same explicit apply-only command repairs the mirror idempotently.

Provider schema acceptance, model availability and billing are still untested.
Visual DOCX review and verification of free-form prose remain manual. The local
eligibility rules are intentionally narrow. Actual token usage/dollar costs and
provider-resolved aliases are not collected. Legacy artifact layouts are retained,
not migrated automatically. Metadata writes are atomic per file, not transactional
across files; the application block is authoritative. No automatic FAISS rebuild
or copy to the historical applied store occurs. These limits do not prevent the
single economy triage test after the setup checklist is satisfied.
