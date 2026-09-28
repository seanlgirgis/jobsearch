# OpenRouter runner — Tiki-Taka note

Date: 2026-09-13

**One concept:** the runner now talks to OpenRouter like `testOpenRouter.py` (plain chat). Model switching and `.env` keys were not removed.

## What broke (one line each)

- `export` is bash → PowerShell: `$env:OPENROUTER_API_KEY = "..."` or `.env`
- Strict JSON-schema call ≠ DeepSeek; sample used plain chat
- Failed cache locked retries
- Model JSON was a bit messy (long strings / missing `score`)

## What we changed

- `src/ai/llm_client.py` — OpenRouter: plain chat, parse JSON here
- `src/pipeline/storage.py` — failed cache can retry
- `env_setter.ps1` — loads `.env` (does not print keys)
- `config/model_profiles.local.json` — economy 4000 tokens; models still switch here

**Keys stay in `.env`. Models stay in local JSON.** Profile JSON still rejects `sk-` / `xai-` keys.

## Next 10-minute touch

1. Rotate the OpenRouter key (it was pasted in chat). Put the new one in `.env` only.
2. Then:

```powershell
. .\env_setter.ps1
.\job-runner.ps1 .\intake\Synthires.md -Mode triage
```

Synthires already **TRIAGED** (`data/jobs/runner_b45014b0`) → **REVIEW**. Stop there unless you want generate.

Longer architecture note (optional, not this touch): `outbox/GROK_ENVIRONMENT_FIX_MODEL_READINESS_REPORT.md`
