---
name: gig_pipeline_tracking
description: Track freelance, contract, and Upwork-style opportunities separately from full-time jobs. Use when creating or updating gig records under data/gigs, managing gig metadata, preserving posting/proposal artifacts, and maintaining data/gig_tracker.csv safely.
---

# SKILL: gig_pipeline_tracking

## Purpose
Track freelance / contract / Upwork-style opportunities separately from full-time jobs.

## Non-Negotiables
- Filesystem is source of truth
- Do not store gigs under `data/jobs/`
- Store freelance opportunities under `data/gigs/`
- Every gig gets its own folder
- Every gig must have `metadata.yaml`
- Central tracker must be updated in `data/gig_tracker.csv`
- Preserve original posting text in `raw/posting.md`
- Preserve proposal text in `generated/proposal_v1.md`
- Do not overwrite submitted proposal versions unless explicitly told
- If a tracker file does not exist, create it
- If a gig folder name collides, increment the numeric ID only

## Inputs
Expected input may include:
- platform (example: Upwork)
- title
- company_or_client
- posting_text
- proposal_text
- hourly_rate_sent
- type (example: mentoring, ai_engineering, etl, consulting)
- status (default: discovered or applied)
- date_found
- date_applied
- notes
- followup_due
- resume_used

## Output Artifacts
For each gig create:

data/gigs/<gig_id>_<slug>/
  raw/posting.md
  generated/proposal_v1.md
  generated/followup_v1.md
  generated/notes.md
  generated/resume_used.md
  metadata.yaml

Also create or update:
data/gig_tracker.csv

## Gig ID Rules
- Gig IDs are 5 digits
- Example: 00001, 00002, 00003
- Determine next ID by scanning `data/gigs/`
- Do not reuse deleted IDs unless explicitly instructed

## Slug Rules
- Lowercase
- Replace spaces with underscores
- Remove punctuation where practical
- Keep slug concise
- Example:
  "Seeking Mentor to Help Me Transition..." -> `upwork_analytics_mentor`

## metadata.yaml schema
Use this schema:

gig_id: "00001"
platform: "Upwork"
company: "Independent Client"
title: "Seeking Mentor to Help Me Transition from Non-Tech Background into Analytics Engineering"
type: "mentoring"
date_found: "2026-04-14"
date_applied: "2026-04-14"
status: "applied"
hourly_rate_sent: 60
proposal_version: "v1"
resume_used: "resume_data_engineer_v3.docx"
followup_due: "2026-04-18"
source_url: ""
notes: "Strong fit. U.S. only. 10-15 proposals."

## gig_tracker.csv schema
Columns:

gig_id,platform,company,title,type,date_found,date_applied,status,hourly_rate_sent,proposal_version,followup_due,resume_used,folder

Example row:

00001,Upwork,Independent Client,Seeking Mentor to Help Me Transition from Non-Tech Background into Analytics Engineering,mentoring,2026-04-14,2026-04-14,applied,60,v1,2026-04-18,resume_data_engineer_v3.docx,data/gigs/00001_upwork_analytics_mentor

## File content rules

### raw/posting.md
- Preserve the posting text as-is if provided
- If structured fields are available, place them above the posting under a small header block

### generated/proposal_v1.md
- Store the exact submitted proposal text
- If not provided yet, create a placeholder:
  `TBD - proposal not yet submitted`

### generated/followup_v1.md
- If no follow-up exists yet:
  `TBD - no follow-up sent yet`

### generated/notes.md
- Include fit notes, competition notes, and strategy notes
- Keep concise and practical

### generated/resume_used.md
- Store the filename or profile variant used
- If unknown:
  `TBD`

## Status values
Allowed statuses:
- discovered
- shortlisted
- applied
- replied
- interviewing
- followup_sent
- closed_won
- closed_lost
- skipped

## Behavior rules
- If posting exists and proposal does not, still create the gig folder
- If proposal exists, mark status as `applied` unless explicitly told otherwise
- If followup_due is not provided and status is `applied`, default to 4 days after date_applied
- If company/client is unknown, use `Independent Client`
- Never mix gig records with full-time job records

## Change safety
Only create/modify:
- data/gigs/**
- data/gig_tracker.csv

Do not modify:
- data/jobs/**
- source_of_truth.json
- resume generation pipeline files
unless explicitly instructed

## Completion report
At the end, output:
- new gig folder path
- files created
- tracker row added or updated
- inferred defaults used
