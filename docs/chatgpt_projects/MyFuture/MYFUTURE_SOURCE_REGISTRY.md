# MyFuture Source Registry

Purpose: track the files used in ChatGPT Project `MyFuture` so pipeline work stays aligned.

## Canonical Folder
- `D:\Workarea\jobsearch\docs\chatgpt_projects\MyFuture`

## Source Files (Current Snapshot)
- `source_of_truth.json`
- `AboutMe.txt`
- `SomeIdeas.txt`
- `pipeline-guide.md`
- `PIPELINE_RUNBOOK.md`
- `CHATGPT_HANDOFF_JOBSEARCH.md`
- `jobsearch-project-analysis.md`

## Operational Rule
- ChatGPT strategy uses these files as context.
- Local pipeline execution remains in this repo (`jobsearch`) and reads/writes normal `data\jobs\...` artifacts.
- If any source changes, copy the updated file here first, then continue job runs.

## Refresh Log
- 2026-04-30: Initial import from `D:\Users\shareuser\Downloads` and workflow registration.
