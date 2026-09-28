# JobSearch Prompt Pack (A1–D1)

## Prompt 1 — A1 (Discuss / Strategy)

```
MODE_ID: A1
TASK: Discuss and advise only (no artifact files)

GOAL:
Decide whether to apply and what positioning angle to take.

JOB:
<paste full job posting>

CONSTRAINTS:
- Use source_of_truth.json as the only career truth
- No invented experience
- Keep output concise and actionable

OUTPUT (STRICT):
1) Fit summary (2–3 lines max)
2) Decision: STRONG APPLY / APPLY / HOLD / SKIP
3) Best angle (ONE line only)
4) Top 3 risks (bullet points)
5) Next step (clear action)

EVALUATION RULES:
- Prioritize AWS + Python + Data Engineering
- Prefer Senior Data Engineer / ML Data Engineer (light ML)
- Avoid deep learning-heavy roles
- Avoid junior roles (overqualification)
- Avoid director roles unless targeted

Be direct. No optimism if fit is weak.
```

---

## Prompt 2 — B1 (Score Report)

```
MODE_ID: B1
TASK: Produce score_report.md content only

JOB:
<paste full job posting>

RULES:
- Use source_of_truth.json only
- No invented facts

OUTPUT HEADINGS (STRICT):
## Match Score: X%
## Recommendation: Strong Proceed / Proceed / Hold / Skip
## Strongest Matches
## Gaps & Risks
## ATS Keywords Present
## ATS Keywords Missing
## Advice
```

---

## Prompt 3 — C1 (Resume Intermediate)

```
MODE_ID: C1
TASK: Produce strict pipeline artifacts as downloadable files

JOB:
<paste full job posting>

POSITIONING_ANGLE:
<paste from A1>

RULES:
- Source of truth only
- No invented data
- One dominant angle only

OUTPUT:
FILES_READY: tailored_data_v1.yaml,resume_intermediate_v1.json
```

---

## Prompt 4 — D1 (Cover Intermediate)

```
MODE_ID: D1
TASK: Produce strict cover intermediate artifact

JOB:
<paste full job posting>

RULES:
- Source of truth only
- No invented claims

OUTPUT:
FILES_READY: cover_intermediate_v1.json
```

---

## Usage Flow

1. Run A1 → decide
2. Run B1 → validate score
3. Run C1 → generate resume inputs
4. Run D1 → generate cover (optional)
