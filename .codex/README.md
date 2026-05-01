# Codex Project Bootstrap

This folder marks `D:\Workarea\jobsearch` as a Codex project and gives a clean entrypoint.

## Start Here

1. Open this workspace in Codex.
2. Load context from `.codex/prompts/startup.md`.
3. Run:
   - `./job-v2-status.ps1`
   - `./job-v2-import.ps1` (when new jobs are ready)
   - `./job-v2-render.ps1` (to generate tailored docs)

## Project Metadata

- Manifest: `.codex/project.yaml`
- Agent role definitions: `.codex/agents/`
- Reusable prompts: `.codex/prompts/`
- Workflow commands: `.codex/workflows/`

## Notes

This scaffold is additive and does not overwrite your existing pipeline files.
