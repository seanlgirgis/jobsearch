# Runtime candidate profile validation

- Profile: `data/master/candidate_profile_runtime.json` (derived context; do not hand-edit).
- Size: 7,849 UTF-8 bytes; 7,849 characters.
- Candidate source inputs: 43,403 bytes; reduction: 81.9% by bytes (not a token measurement).
- Profile SHA-256: `30aa0c158f287fee9ac921fffb7f296dd45a59596bc80876d362b6e3ec4e5b6a`.
- Evidence groups: 8; selected bullets: 13.
- Validation: PASS; prohibited client references 0; URLs, file paths and credential patterns 0.
- Source safety: raw master evidence and Director files are read only; no LLM calls.

## Source provenance

- `data/master/master_career_data.yaml` (career): 14,328 bytes; SHA-256 `42163e629becc8cccb76145db07520642ea2c893f1705a3728b32b356eea5aff`.
- `data/master/skills.yaml` (skills): 10,730 bytes; SHA-256 `acf5d684ac74964228e4d84af51e6a5f06f1903435c8704d0c0f0cb1420d3dcf`.
- `data/master/bofa_stated_ai_work.md` (current_work): 3,427 bytes; SHA-256 `724dd62c5cfd05679acd8dff4675a6945563c02ae02d776561c1fcf5e6e8a987`.
- `outbox/sean_girgis_searchable_profile.md` (positioning): 10,294 bytes; SHA-256 `8e944297b7fee0c69eebc6588e8ea2732a08b9a18e5eba1b7bf0d3f00195ae0c`.
- `_agent/RULES.md` (guardrails): 2,437 bytes; SHA-256 `2e01e5e95716a601d19bcd4b8cee613f39a29929d05a6d58745a3819b70afe0e`.
- `config/runtime_profile_rules.json` (rules): 6,883 bytes; SHA-256 `504c5b300696948c22e0154d5d5c1d5f8b8487271a4acc95946f42afcc83b63a`.
- `SEAN.md` (director_identity): 2,484 bytes; SHA-256 `3876601ac38589e9b022a53fa2bf9eeac0b9395f6108218a6d2083fb0ce0aa44`.
- `SEAN_NOW.md` (director_now): 2,140 bytes; SHA-256 `2ea8e730033a6017ef115c62490f1177c71f73dc89313d3e1a8a8a7cb5ad22b9`.

## Selection and exclusions

- Identity: Director name/location when present, otherwise master fields; email and phone from master. Searchable profile is positioning-only. Director current-focus notes add no employment dates or metrics.
- Skills: original source proficiency within professional, project/practical, or historical evidence groups. Years/last-used estimates and unselected inventory notes are omitted. Unrated tools carry bullet references; foundational tools are capped regardless of a future inventory label.
- Current employer: LTIMindtree only. Official title and dates remain null; function is a descriptive label. Current work is user-stated, with research explicitly separated from production.
- Excluded: current client name/abbreviations, private biography, internal prompts/data/tool details, URLs/local paths, unlisted tools, current-role savings/report-volume estimates and their derived annual totals, report counts, and production claims for research.
- Excluded for compactness: most early-career history, obsolete software versions, legacy certification inventory, duplicate bullets, generic ML/DS positioning, uncorroborated skill-only extras and promotional scale comparisons.
- Selected bullet summaries are reviewed projections of fingerprinted evidence. Source evidence changes stop the builder until the summaries and fingerprints are reviewed together; never merely refresh a hash to suppress that check.
- No independent credential verification is claimed. Existing source labels and project metrics remain attributed to their evidence scope.

## Rebuild and validate

```powershell
. .\env_setter.ps1
python scripts\build_runtime_profile.py
python scripts\build_runtime_profile.py --check
```
