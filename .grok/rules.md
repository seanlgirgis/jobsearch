# Project Rules – Actionable Guidelines

These are specific, enforceable rules for coding, responses, and project management. See constitution.md for high-level principles; decisions.md for log.

## 🤖 Automation & Pipeline
- **Primary Entry Point:** Use `scripts/10_auto_pipeline.py` for end-to-end processing.
- **Pipeline Steps:** Maintain the 01-09 numbering convention for individual scripts.
- **Idempotency:** Scripts should be re-runnable without destructive side effects (unless explicitly overwritten).

## 💻 Coding Standards
- **Windows Compatibility:**
  - Enforce `PYTHONUTF8=1` in subprocess calls to handle emojis/Unicode.
  - Use `pathlib.Path` for all file system operations (avoid string concatenation for paths).
- **Environment:**
  - `src.ai.grok_client` is the standard LLM interface.
  - Fail gracefully with "Mock Mode" if keys/clients are missing.
- **Arguments:** Use `argparse` for all CLI scripts. Standardization:
  - `--uuid`: Required for job-specific scripts.
  - `--version`: Optional version tagging (default: `v1`).
  - `--model`: Allow model overrides (default: `grok-3`).

## 📂 Data Structure
- **Job Data:** All job-specific data lives in `data/jobs/<uuid>/` or `data/jobs/<prefix>_<name>/`.
- **Subfolders:**
  - `tailored/`: YAML data tailored to the job.
  - `generated/`: JSON intermediates and final rendered docs (DOCX/MD/PDF).
  - `research/`: Company research YAML.
- **Metadata:** `metadata.yaml` is the single source of truth for job status and application history.

## 📝 Documentation
- **User Guide:** Keep `user_guide/v0/` updated when scripts change.
- **Script Guides:** Ensure `user_guide/v0/script_guides/` mirrors the actual arguments and behavior of the scripts.
- **Artifacts:** Store intermediate outputs (JSON/YAML) to allow debugging and re-rendering without re-running LLM inference.

## ⚠️ Error Handling
- **Fail Fast:** Pipeline scripts should exit with non-zero status codes on critical errors.
- **Validation:** Validate UUID resolution (support full UUID, short prefix, or folder name match) before processing.
- **Logging:** Print clear emojis (✅, ❌, 🚀) to indicate status in console output.

Last updated: 2026-02-06