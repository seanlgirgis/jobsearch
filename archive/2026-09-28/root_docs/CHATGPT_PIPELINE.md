# ChatGpt Pipeline (No Grok Scoring/Generation)

This pipeline skips Grok scoring/resume generation and uses manual ChatGPT JSON artifacts.

## Flow

1. Duplicate check
2. Accept job (creates UUID + folder shell + intake copy)
3. Drop manual JSON files into `generated/`
4. Render resume + cover in one step
5. Mark applied

## Commands

```powershell
cd D:\Workarea\jobsearch
.\job-chatgpt-check.ps1 "intake\intake.md"
.\job-chatgpt-accept.ps1
.\job-chatgpt-render.ps1
.\job-chatgpt-apply.ps1 -Method "Dice" -Notes "Applied via chatGpt pipeline"
```

## Required manual files before render

- `data/jobs/<job_id>/generated/resume_intermediate_v1.json`
- `data/jobs/<job_id>/generated/cover_intermediate_v1.json`

The job folder, UUID, metadata, and application status updates remain compatible with existing search/index/tracking scripts.
