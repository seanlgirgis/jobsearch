# Job-search pipeline handoff revalidation

Date: 2026-09-13  
Repository: `D:\Workarea\jobsearch`  
Requested prompt: `D:\Users\shareuser\Downloads\GROK_JOBSEARCH_PIPELINE_HANDOFF_PROMPT.md`  
Paid model calls made: **0**

## A. Executive summary

**Readiness: CONDITIONAL GO** for exactly one supervised, economy-only triage smoke test.

The three findings from the independent architecture review are implemented in
the working tree and passed fresh focused regression tests. The full offline
test suite passed (71 tests), runtime candidate-profile validation passed, and
the active economy profile is configured for OpenRouter model
`deepseek/deepseek-v4-flash-0731` with strict JSON-schema output and no
fallbacks.

This is not approval for unattended operation or automatic website submission.
Human review remains required. Quality remains intentionally unconfigured, so
document generation is not ready until Sean explicitly configures the quality
profile.

The pre-existing 2026-09-12 readiness report and its recorded environment check
say `OPENROUTER_API_KEY` was absent. I did not inspect `.env` values in this
revalidation. Before a paid call, Sean must ensure that variable is present in
the root `.env` without sharing it in chat or configuration JSON.

## B. Environment findings

| Item | Verified state |
| --- | --- |
| Repository / current directory | `D:\Workarea\jobsearch` |
| Git | Branch `main`; working tree already has extensive user-owned modifications and untracked material. No Git changes were made. Git also warned that the user-level global exclude file could not be read. |
| Python environment | Python 3.12.9, activated by `env_setter.ps1` from `C:\py_venv\JobSearch` |
| Dependencies | `requirements.txt`; includes `openai==2.16.0`, `httpx==0.28.1`, `jsonschema`, `pydantic`, `python-dotenv`, `faiss-cpu`, and `python-docx` |
| Canonical route | `job-runner.ps1` to `scripts/canonical_runner.py`, with modes `gate`, `triage`, `generate`, and `apply` |
| Operator documentation | `docs/PIPELINE_OPERATOR.md`; narrow Cline instructions are in `CLINE_JOBSEARCH_RUNNER.md` |
| Intake / output | `intake\`; `outbox\`; canonical per-job output is `data\jobs\runner_<hash8>` |
| Cache | `data\pipeline_cache\<sha256>.json`; one-attempt persistent ledger with HIT/MISS provenance |
| Protected evidence | `data\master\`; validated compact profile at `data\master\candidate_profile_runtime.json` |
| Economy profile | `openrouter / deepseek/deepseek-v4-flash-0731`, 1,500-token cap, strict schema, no fallbacks |
| Quality profile | Model remains unset; artifact policy is enabled but generation must fail safely until an ID is configured |
| Smoke intake | `intake\smoke_test.md` exists; its existing local gate shell is `data\jobs\runner_420173c2` |

The root `.env` exists. Its contents and secrets were not read or printed in
this run. The expected key name is `OPENROUTER_API_KEY`; it belongs only in
`.env` or the process environment, never in model-profile JSON.

## C. Files changed

### This execution

| Path | Reason | Change |
| --- | --- | --- |
| `outbox/GROK_ENVIRONMENT_FIX_MODEL_READINESS_REPORT_2026-09-13.md` | Required handoff artifact | New, versioned revalidation report; the prior report was preserved. |

### Previously implemented handoff fixes, verified here

| Path | Reason | Existing implementation verified |
| --- | --- | --- |
| `src/pipeline/local_gate.py` | Repeat-spend protection | `paid_job_text()` supplies normalized Unicode/whitespace posting text for paid request content while avoiding case-folding. |
| `scripts/canonical_runner.py` | Findings A–C | Paid request identity uses normalized paid text; failures write a current `FAILED` handoff; continuation commands preserve `-Cover` and emit one `-Reason`. |
| `tests/test_canonical_pipeline.py` | Regression coverage | Contains one regression each for whitespace cache reuse, stale-success handoff replacement, and continuation flags. |
| `config/model_profiles.local.json` | Economy configuration | Gitignored local overlay configures the exact DeepSeek OpenRouter model; quality remains unset. |

No candidate evidence, existing job record, cache ledger, resume artifact, model
example configuration, or Git history was changed in this execution.

## D. Defect fixes and validation

### 1. Whitespace-only repeat spend

**Original issue:** the folder/job identity normalized whitespace, but the paid
request hash used raw intake text. A whitespace-only edit could therefore make
another Tier 1 request.

**Implementation:** `stage_call()` supplies `paid_job_text(text)` to the model
payload, which is then incorporated into `request_sha256`.

**Regression / result:**
`CanonicalPipelineTests.test_whitespace_only_intake_reuses_paid_cache` passed.
It proves the second triage uses the same job folder and cache key and is a
cache HIT after whitespace-only changes.

### 2. Stale successful handoff after failure

**Original issue:** a failing rerun wrote metadata state `FAILED` but could
leave a prior successful `runner_result.json` as the apparent current result.

**Implementation:** the runner's exception handler now writes
`failure_handoff(...)`, with `state: FAILED`, no resume/cover paths, and no next
command before raising the safe error.

**Regression / result:**
`CanonicalPipelineTests.test_failed_rerun_replaces_stale_success_handoff`
passed. It proves the previous `TRIAGED` handoff is replaced by `FAILED`.

### 3. Invalid continuation command

**Original issue:** combined duplicate and suitability overrides could emit two
PowerShell `-Reason` parameters, and an originally requested `-Cover` switch
was omitted.

**Implementation:** `continuation_command()` constructs tokenized command parts,
retains `-Cover`, retains both override flags when needed, and supplies one
escaped reason string. The same reason covers both authorized overrides, as the
operator guide specifies.

**Regression / result:**
`CanonicalPipelineTests.test_continuation_keeps_one_reason_and_cover` passed.
It asserts exactly one `-Reason`, the expected `-Cover`, both override flags,
and `-Mode generate`.

## E. Model configuration

| Field | Value |
| --- | --- |
| Economy provider | `openrouter` |
| Economy model ID | `deepseek/deepseek-v4-flash-0731` |
| Configuration location | Gitignored `config/model_profiles.local.json`, layered over `config/model_profiles.example.json` |
| Schema policy | `required`; primary reports `supports_json_schema: true` |
| Fallbacks | `[]`; canonical stages reject fallbacks |
| Output cap | 1,500 tokens |
| Quality model | Unconfigured (`null` in effective settings) |
| Required credential name | `OPENROUTER_API_KEY` |

Offline `python -B scripts\model_profile.py show` confirmed the active economy
profile exactly as above. This validates routing/config parsing only; it does
not prove OpenRouter availability, account access, or live schema compatibility.

## F. Tests and local validation

The environment was activated before every Python command. Test code creates
temporary isolated fixtures and mocks provider HTTP/socket access; it does not
call providers or mutate repository job records.

```powershell
. .\env_setter.ps1
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m unittest tests.test_canonical_pipeline.CanonicalPipelineTests.test_whitespace_only_intake_reuses_paid_cache tests.test_canonical_pipeline.CanonicalPipelineTests.test_failed_rerun_replaces_stale_success_handoff tests.test_canonical_pipeline.CanonicalPipelineTests.test_continuation_keeps_one_reason_and_cover -v
python -B -m unittest discover -s tests -p 'test_*.py' -q
python -B -m black --check --line-length 100 scripts\canonical_runner.py src\pipeline\local_gate.py tests\test_canonical_pipeline.py
python -B -m ruff check scripts\canonical_runner.py src\pipeline\local_gate.py tests\test_canonical_pipeline.py
python -B scripts\build_runtime_profile.py --check
python -B scripts\model_profile.py show
python -B scripts\canonical_runner.py --help
```

| Validation | Result |
| --- | --- |
| Focused reviewed-defect regressions | 3 passed |
| Full offline test suite | 71 passed, 0 failed, 0 skipped |
| Black check | 3 files would be left unchanged |
| Ruff check | All checks passed |
| Runtime profile | Validated: 7,849 bytes; 13 bullets; zero prohibited client references |
| Profile loading / route selection | Economy profile shown with configured DeepSeek ID |
| Runner parsing | Help output includes all canonical modes and switches |

The full suite emitted three pre-existing FAISS/SWIG deprecation warnings at
import. They did not cause test failures.

## G. Cost and paid calls

```text
Paid model calls made: 0
```

No OpenRouter, xAI, or other provider request was attempted. No automatic retry
was triggered. The runner tests use synthetic keys and mocked HTTP only.

## H. Remaining risks and manual requirements

- A real OpenRouter credential must be available as `OPENROUTER_API_KEY` before
  the first paid triage. Do not disclose its value.
- Live provider support for the configured exact model ID and strict JSON-schema
  request remains unproven until one authorized supervised call.
- Quality is deliberately unconfigured, so `-Mode generate` is not ready.
- A `TRIAGED` or `READY_TO_APPLY` state never authorizes automatic submission.
  Resume/cover facts and every DOCX page require human review before application.
- Candidate safety boundaries remain essential: no current-client identity,
  unsupported metrics, invented claims, or promotion of foundational tools to
  production expertise.
- The Git worktree is already dirty and user-owned. Nothing was committed,
  reset, staged, pushed, or otherwise altered through Git.

## I. Exact recommended next command

After Sean has confirmed `OPENROUTER_API_KEY` is available and authorizes one
paid test in that session, run this command once, observe the result, and stop:

```powershell
Set-Location -LiteralPath 'D:\Workarea\jobsearch'
. .\env_setter.ps1
.\job-runner.ps1 .\intake\smoke_test.md -Mode triage
```

Do not add generation, cover, apply, retry, or fallback flags. The expected
successful state is `TRIAGED` with at most one economy request on a cache miss.

## J. Suggested next prompt

> Confirm that `OPENROUTER_API_KEY` is configured without displaying it, then
> authorize exactly one supervised economy-only run of
> `./job-runner.ps1 ./intake/smoke_test.md -Mode triage`. Report cache HIT/MISS,
> requested model, result state, and safe error text if any. Do not retry,
> generate documents, or record an application.
