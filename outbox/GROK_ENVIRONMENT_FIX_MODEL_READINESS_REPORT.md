# Grok environment, fix, and model-readiness report

Date: 2026-09-12  
Repository: `D:\Workarea\jobsearch`  
Task: execute `GROK_JOBSEARCH_PIPELINE_HANDOFF_PROMPT.md`  
Paid model calls made: **0**

---

## A. Executive Summary

**Readiness: CONDITIONAL GO** for one supervised **economy-only** triage smoke test.

The three reviewed defects are fixed, regression tests pass, and the economy model ID is configured through the existing local overlay. The system is **not** ready for unattended operation. Human review remains the final gate. No autonomous application submission was added.

**Not safe to run the paid smoke test in this session** until `OPENROUTER_API_KEY` is present in `.env`. The key file exists; OpenRouter is **not** set. `XAI_API_KEY` is present but must **not** be substituted for the OpenRouter economy route.

Quality model remains unconfigured (`null`). That is acceptable for **triage only**. Do not run `-Mode generate` until a quality model ID is set.

---

## B. Environment Findings

| Item | Observed |
| --- | --- |
| Root / cwd | `D:\Workarea\jobsearch` |
| Branch | `main` tracking `origin/main`; dirty working tree (many pre-existing uncommitted files plus this task) |
| Python | 3.12.9 via `.\env_setter.ps1` → `C:\py_venv\JobSearch` |
| Dependencies | `requirements.txt` (`openai==2.16.0`, `httpx==0.28.1`) |
| Canonical entry | `job-runner.ps1` → `scripts/canonical_runner.py --root <repo>` |
| Modes | `gate`, `triage`, `generate`, `apply`; `-DryRun` aliases gate |
| Config | `config/model_profiles.example.json` (tracked, economy model still `null`) + gitignored `config/model_profiles.local.json` |
| Model routing | Named profiles only; runner **fixes** Tier 1 = `economy`, Tier 2 = `quality`; empty fallbacks required |
| Cache | `data/pipeline_cache/<sha>.json`; identity includes `job_hash`, prompt/schema hashes, **request_sha256** |
| Intake | `intake\`; smoke file added: `intake/smoke_test.md` |
| Outbox | `D:\Workarea\jobsearch\outbox` |
| Tests | `tests/test_canonical_pipeline.py`, `test_model_profiles.py`, `test_runtime_profile.py` |
| Protected evidence | `data/master/` including `bofa_stated_ai_work.md`; runtime profile `candidate_profile_runtime.json` |
| `.env` | Present. `OPENROUTER_API_KEY` **absent**. `XAI_API_KEY` present. No secrets printed or committed. |

**Blockers for paid smoke**

1. Set `OPENROUTER_API_KEY` in `.env` (never in profile JSON).
2. Confirm the OpenRouter account actually serves `deepseek/deepseek-v4-flash-0731` with JSON schema.
3. Keep quality `null` until generate is explicitly authorized.

Dry-run of the smoke intake (no HTTP) produced `TIER0_CLEAR` and created `data/jobs/runner_420173c2`. That is a local gate shell only.

---

## C. Files Changed

| Path | Reason | Change |
| --- | --- | --- |
| `src/pipeline/local_gate.py` | Cache identity | Added `paid_job_text()`: NFKC + whitespace collapse, **no** casefold |
| `scripts/canonical_runner.py` | Defects A–C | Payload/cache uses `paid_job_text`; failed runs write current `FAILED` `runner_result.json`; `continuation_command()` emits one `-Reason` and keeps `-Cover` |
| `tests/test_canonical_pipeline.py` | Regression | Three tests: whitespace cache HIT, stale-success replacement, continuation flags |
| `config/model_profiles.local.json` | Economy ID | Gitignored overlay: OpenRouter `deepseek/deepseek-v4-flash-0731`; quality left unset |
| `config/README.md` | Operator note | Documents economy overlay + `OPENROUTER_API_KEY` |
| `intake/smoke_test.md` | Prepared smoke | Synthetic posting for the documented triage command |
| `CURRENT_STATE.md` | Status | Pointer to this report and remaining key/quality gaps |
| `outbox/GROK_ENVIRONMENT_FIX_MODEL_READINESS_REPORT.md` | Required output | This file |
| `data/jobs/runner_420173c2/` | Dry-run side effect | Local gate records; **no** paid analysis |

No Git commit, push, reset, or history rewrite.

---

## D. Defect Fixes

### 1. Whitespace-only repeat spend

**Problem.** `job_hash()` already normalized whitespace (and casefold) for folder identity, but `stage_call` hashed **raw** job text in `request_sha256`, so spaces/newlines produced a new paid cache key.

**Implementation.** LLM payload and therefore `request_sha256` now use `paid_job_text(text)` (whitespace/Unicode collapse only). Explicit regeneration still happens when prompt, schema, profile, or model settings change. Case-only differences are **not** merged in the paid key.

**Regression.** `test_whitespace_only_intake_reuses_paid_cache` — second triage is cache **HIT**, one HTTP mock.

**Validation.** Pass.

### 2. Stale success `runner_result.json`

**Problem.** On exception the runner set metadata `FAILED` and re-raised **without** rewriting `runner_result.json`, so a prior success file still looked current.

**Implementation.** The `except` block writes `failure_handoff(...)` (`state=FAILED`, no resume/cover, `next_command=None`) then re-raises.

**Regression.** `test_failed_rerun_replaces_stale_success_handoff`.

**Validation.** Pass.

### 3. Broken continuation command

**Problem.** Duplicate + suitability overrides emitted two `-Reason` parameters (invalid PowerShell) and dropped `-Cover`.

**Implementation.** `continuation_command()`: at most one `-Reason` (same string covers both switches, matching `PIPELINE_OPERATOR.md`); `-OverrideDuplicate` / `-OverrideSuitability` as needed; `-Cover` preserved when originally requested.

**Regression.** `test_continuation_keeps_one_reason_and_cover`.

**Validation.** Pass. Helper smoke:  
`.\job-runner.ps1 '.\intake\smoke_test.md' -Mode generate -Cover -OverrideDuplicate -OverrideSuitability -Reason 'Verified distinct requisition'`

---

## E. Model Configuration

| Field | Value |
| --- | --- |
| Economy model | `deepseek/deepseek-v4-flash-0731` |
| Provider | `openrouter` |
| Location | `config/model_profiles.local.json` (gitignored; merges over example) |
| Example file | Economy `model` still `null` (tests assert that) |
| Structured output | `required`; `supports_json_schema: true`; fallbacks `[]` |
| Quality model | **Unconfigured** (`null`) |
| Discussion model | Unconfigured |
| API key variable | `OPENROUTER_API_KEY` in `.env` (not in JSON) |
| Key present now | **No** |

`python scripts\model_profile.py list` shows economy `openrouter / deepseek/deepseek-v4-flash-0731`.

---

## F. Tests

Commands (after `. .\env_setter.ps1`):

```powershell
python -m unittest tests.test_canonical_pipeline.CanonicalPipelineTests.test_whitespace_only_intake_reuses_paid_cache tests.test_canonical_pipeline.CanonicalPipelineTests.test_failed_rerun_replaces_stale_success_handoff tests.test_canonical_pipeline.CanonicalPipelineTests.test_continuation_keeps_one_reason_and_cover -v
python -m unittest discover -s tests -p "test_*.py" -q
python -m black --check --line-length 100 scripts\canonical_runner.py src\pipeline\local_gate.py tests\test_canonical_pipeline.py
python -m ruff check scripts\canonical_runner.py src\pipeline\local_gate.py tests\test_canonical_pipeline.py
python scripts\model_profile.py list
python scripts\model_profile.py show
python scripts\canonical_runner.py intake\smoke_test.md --root D:\Workarea\jobsearch --dry-run
```

| Run | Result |
| --- | --- |
| Three new regressions | 3 passed |
| Full `tests/test_*.py` | **71 passed** (was 68) |
| Black | clean after formatting the new tests |
| Ruff | All checks passed |
| Dry-run smoke | `TIER0_CLEAR`, `max_new_provider_requests: 0` |
| Skipped | 0 |
| Failures | 0 |
| Warnings | FAISS SWIG deprecation on import (pre-existing) |

---

## G. Cost / Paid Calls

```text
Paid model calls made: 0
```

No OpenRouter or xAI inference. Dry-run and unittest HTTP mocks only.

---

## H. Remaining Risks

- **No OpenRouter key** — paid triage will fail at credential skip/error until `.env` is updated.
- **Live schema/account** — model ID is configured but untested against the real OpenRouter catalog.
- **Quality ID still null** — generate/cover will fail before a paid quality call (by design).
- **Human gate** — still required; READY_TO_APPLY is not auto-submit.
- **CAPTAIN / LTM truth** — still only from `data/master/`; not merged into yaml; do not invent.
- **Dry-run folder** `data/jobs/runner_420173c2` exists; reuse it for the same smoke intake.
- **Dirty Git tree** — this work is uncommitted; Sean owns Git.

---

## I. Exact Recommended Next Command

Do **not** run until `OPENROUTER_API_KEY` is set. Then, **once**, supervised:

```powershell
Set-Location -LiteralPath 'D:\Workarea\jobsearch'
. .\env_setter.ps1
.\job-runner.ps1 .\intake\smoke_test.md -Mode triage
```

If the key is still missing, the first required step is: add `OPENROUTER_API_KEY` to `.env`, then re-run `python scripts\model_profile.py show` (still offline) and only then the command above. Do not retry automatically on failure. Do not proceed to generate unless asked.

---

## J. Suggested Next Prompt

> Confirm `OPENROUTER_API_KEY` is in `.env` (do not print it). Run exactly one supervised `.\job-runner.ps1 .\intake\smoke_test.md -Mode triage`. Capture cache HIT/MISS, model ID, and any error. Do not generate resume/cover. Do not retry. Stop and report.
