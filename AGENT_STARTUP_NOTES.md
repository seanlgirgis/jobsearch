# Agent Startup Notes (Read First)

For this workspace, before running any Python command:

1. Run PowerShell env setup:
   `& ./env_setter.ps1`
2. Then run Python commands in the same shell session.

Reason:
- `python`/`py` may fail from Windows App execution aliases unless the environment is initialized with `env_setter.ps1`.

Preferred pattern:
`& ./env_setter.ps1; python <script>.py [args]`

Interview prep pipeline memory:
- `agents/002_codex_interview_audio_html_pipeline.md`
- `docs/INTERVIEW_AUDIO_HTML_PIPELINE_RECONSTRUCTED.md`
- Parallel tutorials path: `D:\Workarea\StudyBook\tutorials`
