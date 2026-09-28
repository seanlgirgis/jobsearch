# Prompt 01 Provider and Model Profile Foundation

## Recommended TUI setting

- Model: `gpt-6-astra`
- Reasoning: `ultra`

## Paste into Codex TUI

You are working in `D:\Workarea\jobsearch`.

Read, in order, `AGENTS.md`, `BOOTSTRAP.md`, `PROFILE.md`, `PROJECT_MEMORY.md`, and `CURRENT_STATE.md`. Then read only the files needed for this task. Follow all project rules. Sean manages Git: do not create branches, commit, stage, reset, or modify unrelated worktree changes.

## Objective

Build the provider-neutral foundation for the job-search pipeline so every future paid LLM call can use OpenRouter, xAI, or OpenAI through one interface and can switch models through named profiles.

The current active code is Grok/xAI-specific through `src/ai/grok_client.py`. Preserve backward compatibility during this step; do not refactor the full pipeline yet.

## Required deliverables

1. Add one provider-neutral client under `src/ai/` that supports:
   - OpenRouter through the OpenAI-compatible API;
   - xAI through its existing OpenAI-compatible API;
   - OpenAI directly;
   - one uniform chat method;
   - model fallback lists when configured;
   - structured JSON-schema output when the selected provider/model supports it;
   - safe, concise errors that never reveal API keys.

2. Add committed, safe examples only:
   - `config/model_profiles.example.json`;
   - `.env.example` additions for OpenRouter without placing real values in any committed file.

3. Add gitignored local configuration support:
   - `config/model_profiles.local.json` must be ignored if it does not already exist;
   - it may contain the selected profile and actual OpenRouter model IDs, but do not create it with real keys or invent model IDs.

4. Add a small command-line utility, preferably `scripts/model_profile.py`, with:
   - `list` — show configured profiles without revealing secrets;
   - `show` — display the active profile;
   - `use <profile>` — select an active profile in the local config;
   - clear validation when a profile is absent.

5. Define three profile concepts in the example config:
   - `economy`: Tier 1 fit analysis, low temperature, strict structured output, modest output budget;
   - `quality`: accepted-job resume and cover package, stronger model, controlled output budget;
   - `discussion`: interactive job/career discussion, no automatic artifact generation.

6. Add focused tests or a no-network smoke-test path for config loading, provider selection, profile switching, and fallback request construction. Do not make paid calls.

## Constraints

- Do not hard-code a cheap model name in source. Model IDs belong in local configuration because availability and pricing change.
- Keep real keys only in `.env`; never print `.env` contents.
- Existing `GrokClient` consumers must keep working for now, either through a compatibility adapter or minimal safe migration.
- Do not touch document renderers, job history, application status, resumes, or master career data in this task.
- Before any Python command, run `.\env_setter.ps1` in that shell.
- Use `apply_patch` for edits.

## Validation and report

Run relevant local tests only. Report:

- files changed and why;
- exact commands run;
- test results;
- any compatibility limitations;
- the single command Sean will use to switch to an economy profile.

