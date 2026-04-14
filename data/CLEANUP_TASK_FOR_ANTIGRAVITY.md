# source_of_truth.json — Cleanup & Enhancement Task
# Run this with Antigravity against: D:\StudyBook\temp\jobsearch\data\source_of_truth.json
# Goal: clean data quality issues + tighten content so the pipeline produces better outputs

---

## ISSUE 1 — Encoding corruption in `dates` and `highlights` fields

All em-dashes are stored as mojibake `â€"` (should be `–`) and arrows are `â†'` (should be `→`).

Find and replace globally throughout the file:
- `â€"` → `–`
- `â€"` → `–` (there may be variations)
- `â†'` → `→`
- Any other `â` sequences are UTF-8 corruption — fix to the correct Unicode character

---

## ISSUE 2 — Citi experience has 22+ duplicate/redundant highlights

File location: `experiences[0]` (company: "CITI")

The highlights array currently has ~22 bullets. Many are near-duplicates.
**Consolidate to exactly 10 strong, quantified bullets. Keep the best version of each theme and delete redundant ones.**

Keep (prioritize bullets with metrics/impact):
1. "Architected automated ETL pipelines (Python/Pandas) ingesting P95 telemetry from 6,000+ endpoints (BMC TrueSight/TSCO), replacing legacy manual processes."
2. "Designed optimized Oracle schemas for historical retention, enabling seasonal risk forecasting."
3. "Developed ML forecasting models (Prophet, scikit-learn) predicting capacity bottlenecks 6 months ahead with 90%+ accuracy, improving provisioning lead time."
4. "Built hybrid AWS/Oracle data platform: S3 landing zone for raw telemetry from 6,000+ endpoints, AWS Glue for ETL, and Redshift for ML forecasting workloads."
5. "Containerized Python ETL pipeline jobs on EC2/ECS, enabling scalable on-demand processing for capacity forecasting."
6. "Migrated heavy ML forecasting workloads (Prophet, scikit-learn) from on-prem Oracle to Redshift, enabling parallel forecasting at cloud scale."
7. "Integrated disparate monitoring feeds (TrueSight, CA Wily, AppDynamics) into unified Oracle reporting with executive dashboards."
8. "Identified underutilized infrastructure via data mining across 6,000+ endpoints, driving hardware consolidation and measurable cost savings."
9. "Managed dual APM environments (CA Wily 9.7/10.5, AppDynamics) and enterprise capacity planning across banking infrastructure."
10. "Developed interactive Streamlit/matplotlib/seaborn/plotly dashboards surfacing real-time capacity insights for senior stakeholders."

**Delete all other highlights that are redundant with the above 10.**

---

## ISSUE 3 — Add `exclude_from_resume: true` to very old / irrelevant entries

Add `"exclude_from_resume": true` to these experiences:

1. `experiences` where company = "Simplex International - Canada" (1999–2001): Add `"exclude_from_resume": true`
2. `experiences` where company = "Humber College" (1996–1999): Add `"exclude_from_resume": true`

Keep these in the file but flagged so the pipeline skips them.

---

## ISSUE 4 — Mark legacy skills that will never appear in modern job postings

For each skill where `years: null` AND the technology is clearly obsolete/legacy, add `"legacy": true` to the skill object. Do NOT delete them — just flag them.

Skills to mark as legacy (examples — apply to ALL similar ones):
- COBOL, MicroFocus COBOL
- CVS, ClearCase, Star Team (old version control)
- TSO, CICS, USS (mainframe)
- CORBA
- VB6, VC++
- Tuxedo, Jolt
- Maestro, QuickSelect, PS2PDF, Syncsort, Focus
- AMDOCS CC (highly niche)
- MQ Series (still used, but Sean's usage was 2001-2007 — mark legacy if last_used is null)
- Life Ray Portal
- Mercury Test Director
- IPCS, Semaphores, Locks (too low-level — mark legacy)
- UML, Rational Rose (not relevant for modern data roles)
- Awk, Sed (keep but mark legacy — too low-level to feature)

---

## ISSUE 5 — Fix null years for skills with estimable duration

Skills that have `years: null` but we can infer approximate years from the experiences:

- `C` → `years: 15`, `last_used: "2007"` (used at Corpus/Sprint through 2007)
- `C#` → `years: 3`, `last_used: "2011"` (used through CA Technologies era)
- `PostgreSQL` → `years: 3`, `last_used: "2017"` (used at G6 Hospitality)
- `DB2` → `years: 2`, `last_used: "2008"` (CSC/IRS project)
- `MySQL` → `years: 2`, `last_used: "2010"` (Sabre migration project)
- `JMX Monitoring` → `years: 2`, `last_used: "2011"` (AT&T)
- `AppDynamics` → `years: 5`, `last_used: "2025"` (Citi — already in Citi skills)
- `matplotlib` → `years: 8`, `last_used: "2025"` (Citi)
- `seaborn` → `years: 6`, `last_used: "2025"` (Citi)
- `plotly` → `years: 6`, `last_used: "2025"` (Citi)

---

## ISSUE 6 — Tighten professional_summary.long

Replace the current verbose `long` summary with this tighter version:

```
"long": "Senior Data Engineer and AI practitioner with 20+ years of enterprise IT experience spanning data engineering, cloud infrastructure, and performance engineering. Expert in Python/PySpark ETL pipeline design, AWS serverless architectures (Glue, Athena, S3, Bedrock), and ML-driven capacity forecasting (Prophet, scikit-learn). At Citi (Nov 2017–Dec 2025), built production pipelines ingesting telemetry from 6,000+ endpoints, migrated ML workloads to Redshift, and developed GenAI Text-to-SQL agents using Claude 3 Sonnet. Currently self-studying Databricks (Delta Lake, DLT, Unity Catalog), dbt, and Snowflake to bridge toward modern lakehouse roles. U.S. Citizen, no sponsorship required, based in Murphy, TX (Dallas–Fort Worth area)."
```

---

## ISSUE 7 — Fix project timeframe

In `projects`, find:
- `"name": "Serverless Lakehouse Platform (AWS)"` where `"timeframe": "Recent"`
- Change `"timeframe"` to `"2025"`

---

## ISSUE 8 — Preferred title enhancement

In `personal_info.preferred_title`, update to:

```
"Senior Data Engineer | AWS Data Platform & AI/ML Pipeline Specialist"
```

(Removes "Capacity Planning" which is niche; leads with modern data platform and AI/ML which are higher-demand search terms)

---

## VALIDATION AFTER EDITS

After making all edits, verify:
1. The JSON is still valid (no syntax errors)
2. `experiences[0].highlights` has exactly 10 bullets
3. `experiences` for Simplex and Humber College both have `"exclude_from_resume": true`
4. No `â€"` or `â†'` characters remain anywhere in the file
5. `personal_info.preferred_title` is updated
6. `projects[2].timeframe` is "2025" not "Recent"

Save back to: `D:\StudyBook\temp\jobsearch\data\source_of_truth.json`
