# Sanitized runtime candidate profile

`data/master/candidate_profile_runtime.json` is compact, derived context for job
analysis and application-writing prompts. It is not a replacement for master
career evidence, a ready-to-submit resume, or independent verification of claims.
Do not hand-edit it; rebuild it from the reviewed sources and projection rules.

## Sources and precedence

- `data/master/master_career_data.yaml`: employment records, selected projects,
  education, and public email/phone.
- `data/master/skills.yaml`: selected source proficiency labels. Professional,
  project/practical, historical, foundational-only, and unrated skills remain
  separate. A skill label does not establish current production experience.
- `data/master/bofa_stated_ai_work.md`: user-stated current-work evidence, mapped
  to reviewed public summaries without client identifiers or unconfirmed metrics.
- `outbox/sean_girgis_searchable_profile.md`: positioning context only; it cannot
  upgrade career evidence or supply accomplishments, dates, or proficiency.
- Optional `D:\Workarea\Grok_DIRECTOR\SEAN.md`: preferred public name/location
  override the older master identity fields when present. No other biography is
  copied. An unexpected employer change requires review.
- Optional Director `SEAN_NOW.md`: current-focus context, recorded in provenance;
  its private notes are not copied or treated as new employment evidence.
- `_agent/RULES.md`: required operating-guardrail reference. Safety policy is
  encoded in the builder; changed prose does not automatically rewrite policy.
- `config/runtime_profile_rules.json`: reviewed selection and summarization
  recipe, not independent career evidence. It specifies positioning, selected
  bullets, skill groups, and fingerprints of the underlying career records.

The builder uses a narrow allowlist, not an LLM or a general-purpose text
redactor. Selected employment/project fields are read from master records;
sanitized summaries come from the reviewed recipe. If a selected record or
current-work source changes, the build stops. Review the evidence and summaries
together before updating their fingerprints; never refresh a hash just to bypass
the check. Changes to positioning or guardrails also need human review.

## Regenerate and check

Run from the jobsearch root:

```powershell
. .\env_setter.ps1
python scripts\build_runtime_profile.py
python scripts\build_runtime_profile.py --check
```

The first command writes only the derived JSON and adjacent
`candidate_profile_runtime_validation.md`. The report records source sizes and
SHA-256 hashes, exclusions, output size, and safety results. Source and Director
files are never rewritten. No credentials, network access, or paid calls are used.

`--check` is read-only: it rebuilds in memory, validates the saved profile, and
fails if either generated file is missing, stale, or altered. Required missing
sources and prohibited current-client wording fail clearly. Output is canonical
UTF-8 JSON with no timestamps; identical inputs produce identical artifacts.
The profile has a 12,000-byte ceiling. Byte reduction is not a token measurement.

Offline tests:

```powershell
. .\env_setter.ps1
python -m unittest discover -s tests -p test_runtime_profile.py -v
```

## Public-safety boundaries

Current employer is LTIMindtree only. Current official title and dates remain
null until confirmed; the function label is descriptive. Knowledge-base research
is explicitly non-production, and its codename must not appear in public
documents. Current-role savings, report volumes, and derived totals are omitted.

Databricks, Delta Lake, dbt, Snowflake, Unity Catalog, Delta Live Tables/DLT, Azure
data-platform foundations, and related foundational entries cannot be promoted
to production skills or accomplishment bullets. The profile also forbids invented
titles, dates, metrics, certifications, production status, and generic ML/data
science specialist positioning.

Excluded content includes current-client identifiers, private biography, internal
prompts/data, unlisted tools, URLs and local paths, credentials, most early-career
detail, outdated skill-year estimates, and duplicate or promotional claims.
Public email is the only permitted domain-bearing contact field. Validation
checks common identifier variants and URL/path/credential patterns; it is not a
universal secret detector, so future projection changes still require review.

## Intended consumers

Use the JSON for compact job-fit analysis, keyword matching, resume tailoring,
cover letters, and recruiter-message drafts. Preserve all `public_safety` rules,
skill-tier distinctions, evidence status, and bullet-to-evidence links in prompts.
Unknown values are not permission to guess. Keep the provenance report local;
do not append it or raw source files to public-document prompts.

The canonical runner (`job-runner.ps1`) automatically verifies this profile and
report against the source projection after the local gate and before analysis,
including cache hits. Standalone `--check` remains available for diagnosis.
Follow [PIPELINE_OPERATOR.md](PIPELINE_OPERATOR.md) for the active commands.
Consult master evidence locally when detail is missing, then review/update the
projection instead of letting a runner model invent that detail.
