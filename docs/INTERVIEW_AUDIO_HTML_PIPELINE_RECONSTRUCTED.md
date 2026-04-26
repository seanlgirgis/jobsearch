# Interview Prep Audio + HTML Pipeline (Reconstructed)

Last updated: 2026-04-26
Working execution root: `D:\Workarea\StudyBook\`

## Goal

Reconstruct and standardize the workflow that uses:

- ChatGPT Project 1 prompt for audio scripts
- StudyBook runner for TTS audio generation
- ChatGPT Project 2 prompt for learning-page HTML
- Website component wiring in `seanlgirgis.github.io`

## Repository Roles

- `D:\Workarea\StudyBook\`: orchestration root, env setup, mission prompts, scripts
- `D:\Workarea\jobsearch\`: script source storage for interview prep
- `D:\Workarea\seanlgirgis.github.io\`: website learning pages/components/projects
- `D:\Workarea\StudyBook\tutorials\`: parallel tutorials workspace for tutorial artifacts/content

## Canonical Relative Paths (from StudyBook root)

- Audio script source:
  - `..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md`
- Learning page output:
  - `..\seanlgirgis.github.io\learning\{slug}.html`
- Component card updates:
  - `..\seanlgirgis.github.io\components\learning-*.html`
- Tutorials workspace:
  - `.\tutorials\`
- Binary audio output (outside repos):
  - `D:\temp\studybook_audio\{slug}\audio_clips\`
  - `D:\temp\studybook_audio\{slug}\final_{slug}.mp3`

## Prompts and Runbooks Used

Folder:
- `prompts\codex_missions\WebsitePagesAndAudioBYCodexChatgpt\`

Core files:
- `Project-1-Audioscript-Maker.txt`
- `Project2_HTMl_Maker.txt`
- `Existing_work_pipeline_execution_master.md`
- `Existing_work_pipeline_execution_provided_files_master.md`
- `Existing_work_pipeline_execution_provided_files_runner_mode_master.md`

## End-to-End Flow (Default)

1. Open shell in StudyBook root.
2. Load environment:
   - `& .\env_setter.ps1`
3. Use Project 1 prompt to generate `audio_script_{slug}.md`.
4. Save script under `..\jobsearch\data\interview_prep\audio_prep\{slug}\`.
5. Run audio mission runner:
   - `.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md" -ChunkSize 750 -RequestTimeoutSeconds 120`
6. Confirm final audio exists:
   - `Test-Path "D:\temp\studybook_audio\{slug}\final_{slug}.mp3"`
7. Upload final MP3 to R2.
8. Use Project 2 prompt to generate/update `{slug}.html`.
9. Save HTML in `..\seanlgirgis.github.io\learning\`.
10. Update component card to make page discoverable and marked live.

## Quick Verification Commands

Run from `D:\Workarea\StudyBook\`.

```powershell
# 1) Audio src and type check
Select-String -Path "..\seanlgirgis.github.io\learning\{slug}.html" -Pattern "final_{slug}.mp3|audio/mpeg"

# 2) Find card wiring for this slug
Select-String -Path "..\seanlgirgis.github.io\components\learning-*.html" -Pattern "{slug}|learning/{slug}.html|Open Reference|Live"

# 3) Ensure no accidental repo binary artifacts
Get-ChildItem "..\jobsearch\data\interview_prep\audio_prep" -Recurse -File |
  Where-Object { $_.Name -match "{slug}.*(\.mp3|\.m4a|filelist\.txt)$" } |
  Select-Object FullName
```

## Website Layout Findings (Current)

- Learning pages are direct HTML files in `learning\`.
- Category and nav wiring is done through `components\learning-nav.html` and multiple `components\learning-*.html` card files.
- Card status pattern already used broadly:
  - `Open Reference`
  - audio live indicator (`🎧 ● Live`)
  - optional video indicator (`🎬 ○ N/A` or live)
- Project pages in `projects\` can also embed R2-hosted audio using the same `final_{slug}.mp3` convention.

## Mode Variants

- Full mode: create script + run audio + update html.
- Provided-files mode: script/html already exist; run pipeline + update wiring.
- Runner mode: user executes every command manually; agent only provides and validates command outputs.

## Naming and Consistency Guidance

- Preferred slug format: lowercase + hyphen.
- Filename conventions should stay strict:
  - `audio_script_{slug}.md`
  - `final_{slug}.mp3`
  - `{slug}.html`
- Keep encoding UTF-8 and use HTML entities for UI glyphs in generated pages to avoid mojibake.


