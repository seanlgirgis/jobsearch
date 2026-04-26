# Codex Agent Operating Contract — Interview Prep Audio + HTML Pipeline

Last updated: 2026-04-26

## Mission Scope

This repository (`D:\Workarea\jobsearch`) stores interview-prep script source files.
The paired website repository is `..\seanlgirgis.github.io` (sibling to `..\StudyBook`).
The execution root for mission commands is always `..\StudyBook`.
Parallel tutorials workspace lives at `..\StudyBook\tutorials`.

## Path Migration (Old -> New)

- `D:\StudyBook\` -> `D:\Workarea\StudyBook\`
- `D:\StudyBook\temp\jobsearch` -> `D:\Workarea\jobsearch\`
- `D:\StudyBook\temp\seanlgirgis.github.io` -> `D:\Workarea\seanlgirgis.github.io\`

## Non-Negotiables

1. Use relative paths in commands and docs whenever possible.
2. Start from `D:\Workarea\StudyBook\` for pipeline execution.
3. Run environment setup before Python/OpenAI pipeline calls:
   - `& .\env_setter.ps1`
4. Keep generated binary audio outside repos:
   - `D:\temp\studybook_audio\{slug}\...`
5. Keep text artifacts in repos only:
   - Script source: `..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md`
   - HTML page: `..\seanlgirgis.github.io\learning\{slug}.html`
   - Component wiring: `..\seanlgirgis.github.io\components\*.html`
6. Keep tutorial assets/content in:
   - `..\StudyBook\tutorials\`

## Reconstructed Pipeline (Project 1 + Project 2)

1. Generate audio script in ChatGPT Project 1 using:
   - `prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\Project-1-Audioscript-Maker.txt`
2. Save script to:
   - `..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md`
3. Run audio generation + stitch from StudyBook:
   - `.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120`
4. Upload `D:\temp\studybook_audio\{slug}\final_{slug}.mp3` to R2.
5. Generate or refresh HTML in ChatGPT Project 2 using:
   - `prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\Project2_HTMl_Maker.txt`
6. Save page to:
   - `..\seanlgirgis.github.io\learning\{slug}.html`
7. Ensure audio source points to:
   - `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{slug}.mp3`
8. Ensure site card discoverability in `..\seanlgirgis.github.io\components\...`:
   - clickable card
   - `Open Reference`
   - status format like `🎧 ● Live` and `🎬 ○ N/A` when applicable

## Website Layout Notes (Observed)

- Learning pages live in: `..\seanlgirgis.github.io\learning\`
- Learning hub/category cards live in: `..\seanlgirgis.github.io\components\learning-*.html`
- Project pages live in: `..\seanlgirgis.github.io\projects\`
- Typical learning-page audio block uses `audio/mpeg` and R2 `final_{slug}.mp3` naming.

## Master Prompt/Runbook Sources

Primary folder:
- `..\StudyBook\prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\`

Key files:
- `Project-1-Audioscript-Maker.txt`
- `Project2_HTMl_Maker.txt`
- `Existing_work_pipeline_execution_master.md`
- `Existing_work_pipeline_execution_provided_files_master.md`
- `Existing_work_pipeline_execution_provided_files_runner_mode_master.md`

## Execution Mode Selection

- New topic from scratch: use full triplet flow (script -> audio pipeline -> html).
- Existing script + existing html: use provided-files mode.
- User wants manual commands only: use runner mode.


