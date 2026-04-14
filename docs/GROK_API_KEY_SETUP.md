# Grok API Key Setup (Desktop + Laptop)

## What the code uses
The pipeline reads `XAI_API_KEY` via `python-dotenv` in:
- `src/ai/grok_client.py`
- `scripts/test_xai_api.py`

So your Grok key should be available as an environment variable named `XAI_API_KEY`.

## Recommended setup
1. In repo root (`D:\StudyBook\temp\jobsearch` on this machine), create `.env`.
2. Add one line:
   `XAI_API_KEY=YOUR_NEW_GROK_KEY`
3. Keep `.env` local-only (already ignored by `.gitignore`).

You can start from:
- `.env.example` -> copy to `.env` and fill your key.

## How it works across machines
Environment keys are machine-local unless you explicitly sync them.

- Desktop run uses `D:\StudyBook\temp\jobsearch\.env` (or OS env var).
- Laptop run uses that laptop's repo `.env` (or laptop OS env var).
- Git will not carry `.env` to the other machine.

So you must set the key once per machine.

## Precedence rule
`load_dotenv()` does not override an existing OS environment variable by default.

That means:
- If `XAI_API_KEY` is set globally in PowerShell/Windows, that value is used.
- Otherwise `.env` value is used.

## Quick verification
From repo root:

```powershell
python -m scripts.test_xai_api
```

If configured correctly, it prints a successful response from xAI.

## Security notes
- Never paste real keys into tracked files, docs, or commits.
- Rotate keys immediately if one is exposed.
- Prefer password manager storage + manual paste on each machine for first-time setup.

