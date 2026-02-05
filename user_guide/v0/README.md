# JobSearch Pipeline User Guide - v0 (POC: Script-Based)

## Overview
This is the proof-of-concept iteration of the JobSearch pipeline. Everything runs via individual Python scripts (no integrated app yet). The focus is on modular, auditable steps to avoid LLM over-reliance and ensure consistency (e.g., no date overlaps in resumes).

Key Principles (from .grok/Constitution.md):
- Modular: Each step is a standalone script.
- Auditable: Intermediate files for user review/editing.
- Consistent: All generations reference a "source of truth" database for your profile (e.g., job dates, field names like "portfolio" vs "website").
- No Full LLM Outsourcing: LLMs assist only in drafting intermediates; final generation is script-based (no LLM creativity).
- Public: All code/comms in https://github.com/seanlgirgis/jobsearch.git.

## Quick-Start Workflow
1. **Setup Source of Truth**: Run profile_source_of_truth.py once to build your personal job database (JSON/YAML file from source_of_truth.json). Run profile_export.py to generate legacy masters if needed.
2. **Intake a Job**: Drop a job description file in intake/ (markdown with Employer_Name, URL, Title, Location, Contents).
3. **Score the Job**: Run scoring script for fit assessment → moves to data/jobs/<uuid>/ if successful.
4. **Decide on Job**: Accept/Reject/Hold with notes; updates metadata.yaml.
5. **Tailor Job Data**: Extract sections/skills → tailored_data_v1.yaml.
6. **Generate Resume Intermediate**: LLM drafts a tailored intermediate (checked against source of truth).
7. **Review/Edit Resume Intermediate**: You manually review/edit (sanity check dates, etc.).
8. **Generate Final Resume**: Script formats from intermediate (no LLM).
9. **Generate Cover Intermediate**: Similar to resume, LLM drafts with source of truth checks.
10. **Review/Edit Cover Intermediate**: You review/edit.
11. **Generate Final Cover**: Script formats from intermediate.
12. **Track Application**: Update job status with events (e.g., "applied").

Run scripts from root: `python scripts/<script_name>.py --job_file <file> --uuid <uuid>`. See per-script guides in script_guides/ for details.

## Source of Truth
All scripts reference a single file (data/source_of_truth.json) for your immutable profile data. This prevents errors like overlapping dates. Build it once via profile_source_of_truth.py; update manually if profile changes. Run profile_export.py after updates for legacy script compatibility.

## Per-Script Guides
Detailed in script_guides/ subdir. Each includes:
- **Input**: Required files/args.
- **Process**: Step-by-step what happens.
- **Outsourcing**: Any LLM calls (limited, with prompts enforcing source of truth).