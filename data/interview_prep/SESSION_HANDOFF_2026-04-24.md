# Job Search Session Handoff — April 24, 2026

> Load this file at the start of a new session to restore full context instantly.
> All referenced files are current as of April 24, 2026.

---

## WHO

**Sean Luka Girgis** — Murphy, TX (Plano area) · 214-315-2190 · seanlgirgis@gmail.com
U.S. Citizen · No sponsorship · Available immediately (off since Dec 2025, Citi role eliminated — not performance)
20+ years experience · 8 years Citi as Senior Capacity & Data Engineer

**Key numbers (memorize):** 6,000+ endpoints · 90% forecast accuracy · 6-month prediction horizon · 90% cycle time reduction · CodeSignal GCA 540/600

---

## SYSTEM LOCATION

```
D:\StudyBook\temp\jobsearch\
  data/source_of_truth.json          ← master profile (updated Apr 24)
  data/interview_prep/active_interviews/
    toyota_ramya_recruiter_1655.md   ← Ramya screen (COMPLETE)
    toyota_technical_interview_roadmap.md  ← 13-phase technical prep (PRIMARY)
  data/jobs/url_captures/
    toyota_req_10301655_capture_2026-04-24.md
    capitalone_r238448_capture_2026-04-24.md
  prompts/
    learning_artifact_prompt_template.md   ← Codex/Gemini prompt template (NEW)
```

Memory file: `C:\Users\shareuser\.claude\projects\D--StudyBook\memory\project_jobsearch.md`

---

## ACTIVE PIPELINE

### 🟡 Toyota Financial Services — Lead Senior Python Developer (Req 10301655)
- **Status:** ✅ Codie referral → ✅ Applied → ✅ Ramya screen PASSED (Apr 23) → 📅 Technical HM interview PENDING
- **Next:** Technical interview with Technical Manager — week of April 28 (exact date TBD)
- **Signal from Ramya:** Terraform flagged as a gap. Other possible gaps: FastAPI, MSK, CI/CD hands-on
- **Salary target:** $185,000 base
- **Key framing:** "I build reusable Python frameworks other teams consume" — platform architect, not pipeline developer
- **Prep doc:** `toyota_technical_interview_roadmap.md` — 13 phases, study order mapped to dates

### 🟡 Capital One — Senior Lead Data Engineer (R238448)
- **Status:** CodeSignal GCA submitted Apr 24 — Q1 ✅ Q2 ✅ Q3 attempted (knew the approach, ran out of time) — outcome pending
- **Salary range (Plano TX):** $209,000–$238,500
- **Action:** Wait for response. If they advance, Cap One prep overlaps heavily with Toyota prep.

### ❌ Samsung Austin Semiconductor — Capacity Planning Engineer
- **Status:** Declined Apr 24. Closed.

---

## WHAT WAS DONE THIS SESSION

1. **Ramya screen completed** — Apr 23, phone call, passed. Terraform flagged.
2. **Samsung closed** — declined, removed from active pipeline.
3. **CodeSignal submitted** — Q1+Q2 solved, Q3 attempted (grid shape stamp problem).
4. **CodeSignal problems reconstructed** into 4 notebooks in `D:\StudyBook\playground\`:
   - `0163.codesignal_triplet_count.ipynb` — sliding window, count s[i]==s[i+2]
   - `0164.codesignal_vowel_word_transform.ipynb` — reverse middle of vowel-bounded words
   - `0165.codesignal_grid_shape_stamp.ipynb` — stamp shapes onto grid, first-fit scan
   - `0166.codesignal_building_span.ipynb` — monotonic stack (≈ LC 901)
5. **Toyota technical roadmap updated** — Phases 11–13 added (MSK/Kafka, Snowflake/PyIceberg, OpenSearch/Dynatrace). Terraform elevated to 🔴 Critical. Study order mapped to Apr 24–30.
6. **Source of truth updated** — 9 missing skills added: Terraform, FastAPI, CI/CD Pipelines, AWS MSK/Kafka, PyIceberg/Iceberg, OpenSearch, REST API/Microservices, OAuth2/JWT, pytest.
7. **Learning artifact system designed** — 3 artifacts per topic (audio script, tutorial+Q&A, capstone). Prompt template created for Codex/Gemini generation.

---

## IMMEDIATE NEXT PRIORITIES

| Priority | Task |
|----------|------|
| 🔴 1 | **Terraform hands-on** — build a real ECS stack. Ramya flagged it. Must have working knowledge before technical HM interview. Phase 8 of roadmap. |
| 🔴 2 | **FastAPI hands-on** — REST API with Pydantic, auth, OpenAPI docs. Phase 3 of roadmap. |
| 🟠 3 | **CI/CD hands-on** — GitHub Actions → Docker → ECR → ECS deploy. Phase 5. |
| 🟠 4 | **CloudFormation hands-on** — same ECS stack as Terraform, AWS-native. Phase 7. |
| 🟡 5 | **MSK/Kafka concepts** — SQS vs MSK, producer/consumer, Phase 11. |
| 🟡 6 | **Snowflake + PyIceberg** — data lake architecture, Phase 12. |
| 🔵 7 | **Capital One** — wait for CodeSignal outcome before investing prep time. |

---

## LEARNING ARTIFACT SYSTEM

For each technical topic, generate **3 artifacts** using Codex or Gemini (saves Claude tokens):

- **A) Audio Script** — conversational, no code, for listening. Concepts + analogies + light recap Q&A at end.
- **B) Tutorial + Interview Q&A** — code examples, patterns, interview questions with answers integrated.
- **C) Capstone Project** — hands-on deliverable that proves the knowledge. Clear spec + validation criteria.

Prompt template: `D:\StudyBook\temp\jobsearch\prompts\learning_artifact_prompt_template.md`

**Topic queue (in order):**
1. Terraform
2. FastAPI
3. CI/CD (GitHub Actions + Docker + ECS)
4. CloudFormation
5. AWS MSK / Kafka
6. Snowflake + PyIceberg
7. OpenSearch / Elasticsearch

---

## KEY STORIES (Use Everywhere)

| Story | Use When |
|-------|----------|
| **HorizonScale** — PySpark+Prophet+sklearn, 90% cycle reduction, 6-month ML forecasting | Most impactful project, Python at scale, ML in production |
| **FAST Project** — Dynatrace AppMon ETL at G6, data-mined real-user perf data | Dynatrace experience, observability, ETL for business impact |
| **AWS Hybrid Platform** — S3+Glue+Redshift+ECS, containerized Python ETL | AWS architecture, cloud migration, platform engineering |
| **Citi Capacity Planning** — 6,000+ endpoints, BMC TrueSight, Oracle, 10→2 days | End-to-end data platform, scale, automation |

---

## ARCHITECT ANSWER PATTERN (Toyota Technical Interview)

Every design question → follow this structure:
1. **Requirements first** — business problem, non-functional requirements, constraints
2. **Identify components** — data, service, API, infrastructure layers
3. **Evaluate tradeoffs** — consistency vs availability, build vs buy, cost vs performance
4. **Make the decision** — state clearly, state why, state risks
5. **Plan for scale** — what breaks at 10x, where to add cache/async/horizontal scale

Anchor phrase: *"My approach is always requirements first, then architecture, then implementation. I make decisions based on tradeoffs — not on what's familiar, but on what solves the actual problem at the scale required."*
