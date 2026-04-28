# Toyota Financial Services — HM Interview Prep
**Req:** 10301655 | **Role:** Lead Software Engineer — Python, API Microservices & DevOps
**Interview:** April 30, 2026 · 11:00 AM CT · Microsoft Teams · 45 min
**Hiring Manager:** Abdul Jaleel Dudekula
**Recruiter:** Ramya (screen ✅ PASSED April 23)
**Location:** Plano, TX — 4 days onsite (Murphy TX ≈ 12 miles away ✅)

---

## 1. The Job — What Toyota Is Actually Looking For

### Core Role Signal
Toyota Financial Services is building modern Python-first microservices on AWS. They want a **hands-on tech lead** — someone who can write the code AND mentor juniors AND make architecture decisions. The title "Lead" is real: this is not a pure IC role.

### Tech Stack (From the Job Req)

| Category | Specifics |
|---|---|
| Language / API | Python, FastAPI, OpenAPI/Swagger |
| Cloud | AWS — Glue, Lambda, ECS, MSK (Kafka), S3 |
| IaC | **Terraform** (flagged by Ramya as a gap), CloudFormation |
| Containers | Docker, ECS (Fargate likely) |
| CI/CD | GitHub Actions or similar |
| Observability | CloudWatch, **Dynatrace**, **OpenSearch** |
| Security | IAM, OAuth2, JWT |
| Data | AWS Glue, MSK, potentially Snowflake/Iceberg |
| Testing | **pytest**, test-driven practices |

### What They Emphasized (Ramya's Recruiter Screen Notes)
- End-to-end architecture ownership (you own it soup-to-nuts)
- DevOps/containerization — not just knowing Docker, but deploying to ECS
- API design at scale — not just FastAPI basics, API versioning, rate limiting, 12-factor patterns
- CloudFormation hands-on (not just reading)
- **Terraform explicitly flagged as a gap** — prep even basics
- Mentoring junior engineers — be ready with a real story
- Salary target stated: **$185,000**

---

## 2. Sean vs. The Job — Honest Fit Analysis

### Strong Matches (Lead With These)
| Requirement | Sean's Evidence |
|---|---|
| Python — advanced | 20+ years, Pandas/PySpark/Prophet/scikit-learn daily at CITI/G6 |
| AWS ecosystem | S3, Glue, Athena, Bedrock in production (G6 Hospitality migration) |
| Data pipelines / ETL | AWS Glue migrations at G6, ETL at CITI (8 years) |
| Dynatrace | Used DynaTrace AppMon & Synthetics — real production experience |
| Kafka / MSK | CA Technologies + AT&T telco environments |
| Docker | Used in projects, tutorial track built |
| FastAPI / microservices | API design experience; FastAPI is Python-native and fast to prep |
| Performance engineering | CA APM, AppDynamics, profiling — direct overlap with observability ask |

### Partial Matches (Prep Needed)
| Requirement | Gap | Prep Action |
|---|---|---|
| FastAPI / OpenAPI | Know Flask/APIs but need FastAPI idioms | 4-hour FastAPI sprint (see Day 1) |
| ECS deployment | Know Docker; ECS task def syntax needs drill | ECS task def cheat sheet + ECR push |
| Terraform | **Flagged by Ramya** — biggest gap | 1-hour HCL basics + `terraform plan/apply` |
| CloudFormation | Know concept; need to write actual YAML stacks | 1 real stack exercise |
| pytest at depth | Testing exists; need fixtures/mocking/parametrize fluency | 2-hour pytest drill |
| JWT/OAuth2 flow | Know concepts; code a JWT middleware example | 30-min FastAPI + JWT snippet |
| OpenSearch | Know Elasticsearch conceptually (similar) | Skim query DSL + index patterns |

### Thin Gaps (Acknowledge If Asked, Don't Volunteer)
- PyIceberg / Snowflake deep internals
- GitHub Actions YAML from memory (know the concept; look up syntax)

---

## 3. Three Key Stories (STAR Format Ready)

These were identified from prior recruiter screen and job analysis. Have all three loaded in memory — use whichever fits the question.

### Story 1 — FAST Project (G6 Hospitality)
**Situation:** Legacy on-prem Oracle data pipelines taking 6+ hours nightly, brittle, manual intervention required.
**Task:** Migrate to AWS serverless architecture; reduce cost and latency.
**Action:** Designed Glue + Athena + S3 Lifecycle serverless lakehouse; built Python ETL with PySpark; automated with Airflow; reduced data freshness from 6hr to 30min.
**Result:** ~60% infra cost reduction, zero manual intervention, foundation for ML forecasting layer.
**Maps to:** end-to-end architecture ownership, AWS Glue, Python, data engineering leadership.

### Story 2 — HorizonScale (Capacity Forecasting Platform)
**Situation:** CITI had no automated capacity forecasting — manual Excel estimates led to over-provisioning and missed SLAs.
**Task:** Build ML-driven forecasting to predict infrastructure needs 30–90 days out.
**Action:** Built Prophet + scikit-learn time-series models; Streamlit dashboard for stakeholders; integrated with BMC TrueSight/AppDynamics alerting; deployed on AWS.
**Result:** 40% reduction in over-provisioning cost, proactive SLA protection, adopted by 3 business units.
**Maps to:** Python ML, stakeholder communication, platform thinking, observability.

### Story 3 — AWS Hybrid Platform (CITI)
**Situation:** CITI needed hybrid cloud strategy — on-prem Oracle + AWS, compliant with financial data governance.
**Task:** Lead architecture design and implementation of hybrid data platform.
**Action:** Designed IAM roles and policies for cross-account access; implemented S3 + Glue data catalog; built monitoring with CloudWatch + custom dashboards; documented runbooks for team of 8.
**Result:** Platform adopted org-wide; led mentoring of 4 junior engineers through the migration.
**Maps to:** AWS IAM, CloudWatch, mentoring, tech lead responsibilities.

---

## 4. The 3-Day Prep Plan (April 27–29)

### Day 1 — April 27 (TODAY): API + FastAPI + Testing

**Morning (3 hours) — FastAPI Sprint**
- [ ] Build a FastAPI app from scratch: `POST /ingest`, `GET /records/{id}`, `GET /health`
- [ ] Add Pydantic request/response models
- [ ] Add JWT middleware (python-jose or PyJWT)
- [ ] Add OpenAPI auto-docs — run it and see the Swagger UI
- [ ] Add rate limiting concept (fastapi-limiter or manual counter)
- Key talking points: path params vs query params, dependency injection, async def vs def, 12-factor config via env vars

**Afternoon (2 hours) — pytest Depth**
- [ ] Fixtures: `@pytest.fixture` with scope=session, scope=function
- [ ] Parametrize: `@pytest.mark.parametrize`
- [ ] Mocking: `unittest.mock.patch`, `MagicMock` for AWS calls
- [ ] FastAPI TestClient — write 3 tests for the app you built this morning
- [ ] One conftest.py pattern

**Evening (1 hour) — Terraform Survival Kit**
- [ ] Install Terraform locally (or review syntax only)
- [ ] Understand: `provider`, `resource`, `variable`, `output`, `data`
- [ ] Write a minimal S3 bucket resource in HCL
- [ ] `terraform init / plan / apply / destroy` — know the flow
- [ ] Key phrase: "I've used CloudFormation more extensively, and I've been expanding my Terraform skills — here's what I know about the HCL approach..."

---

### Day 2 — April 28: Docker + ECS + CloudFormation

**Morning (3 hours) — Docker + ECS**
- [ ] Review your multi-stage Dockerfile pattern (from `36_docker` tutorial)
- [ ] Write a Dockerfile for the FastAPI app from Day 1
- [ ] `docker build / run / push to ECR` — practice the commands
- [ ] ECS task definition: know `containerDefinitions`, `cpu`, `memory`, `logConfiguration` (CloudWatch)
- [ ] Fargate launch type vs EC2 — know when to say which
- [ ] ECS service + ALB integration: what a target group does
- [ ] Key talking point: "I've containerized pipelines with Docker and deployed to ECS Fargate — the Glue serverless work at G6 used a hybrid of Lambda + Glue, and I've been building out ECS deployment patterns more recently."

**Afternoon (2 hours) — CloudFormation**
- [ ] Write a real YAML stack: S3 bucket + Lambda function + IAM role
- [ ] Understand `Parameters`, `Outputs`, `Ref`, `!Sub`, `!GetAtt`
- [ ] Change sets: what they are and why they matter
- [ ] Stack drift: know what it means
- [ ] Cross-stack references via `Export`/`ImportValue`

**Evening (1 hour) — Observability Review**
- [ ] CloudWatch: metrics vs logs vs alarms vs dashboards — know the difference
- [ ] CloudWatch Insights query syntax: `fields @timestamp, @message | filter @message like /ERROR/`
- [ ] Dynatrace: you have real production experience — prep 2 sentences: "At CITI/G6 I used DynaTrace AppMon and Synthetics to monitor JVM performance and set up synthetic transaction monitors for SLA tracking."
- [ ] OpenSearch: it's Elasticsearch-compatible. Know: index, document, shard, mapping, `_search` with `query.bool.must`

---

### Day 3 — April 29: Architecture + Storytelling + Whiteboard

**Morning (2 hours) — System Design Drill**

Practice this design out loud (set a 35-minute timer, Abdul will expect this):

> **"Design a real-time transaction processing pipeline for Toyota Financial Services"**
>
> Answer structure:
> 1. Clarify requirements (volume? latency? compliance?)
> 2. Ingest: MSK (Kafka) topic per transaction type
> 3. Processing: Lambda consumer OR ECS service (explain tradeoff)
> 4. Storage: S3 raw → Glue catalog → Redshift/Snowflake for analytics
> 5. API layer: FastAPI on ECS Fargate, JWT-authenticated
> 6. Observability: CloudWatch metrics, Dynatrace APM, OpenSearch log aggregation
> 7. IaC: CloudFormation for stable infra, Terraform for cross-account

**Morning (1 hour) — Lead / Mentoring Story**
- [ ] Prep specific mentoring story: "I led 4 junior engineers through the CITI hybrid AWS migration — I did weekly 1:1s, code review with teaching notes, and built a runbook template they could own."
- [ ] Prep conflict/disagreement story: "An architect proposed a batch approach; I advocated for stream processing because... Here's how we resolved it..."
- [ ] Prep failure story (they WILL ask): Pick something real, show what you learned.

**Afternoon (2 hours) — Full Mock Interview**
- [ ] Time-box 45 minutes, simulate the Teams call
- [ ] Answer these questions out loud:
  - "Walk me through a complex API you designed end-to-end."
  - "How do you handle a microservice that's becoming a monolith?"
  - "Tell me about a time you improved system reliability."
  - "How do you mentor engineers who are resistant to feedback?"
  - "What's your approach to CI/CD for a Python service?"
  - "How would you secure an API that handles financial data?"

**Evening — Logistics + Questions**
- [ ] Teams audio/video test
- [ ] Have 3–5 questions ready for Abdul (see Section 6)
- [ ] Re-read the job req one more time
- [ ] Sleep. Seriously.

---

## 5. Day-of Checklist (April 30)

**Before 10:30 AM**
- [ ] Teams open and tested (camera, mic)
- [ ] VSCode open with a blank Python file — you may want to share screen / type
- [ ] Job req open in one window, this doc open in another
- [ ] Water, quiet room, no distractions

**11:00 AM — Interview Structure (Expected)**
- ~5 min: intros / small talk / Abdul's background
- ~25 min: technical questions + system design
- ~10 min: behavioral / leadership
- ~5 min: your questions

**Salary Anchoring**
- If asked: **"I'm targeting $185,000 base, consistent with what I shared with Ramya. I'm open to discussing the full package."**
- Do NOT go lower unless there's a compelling equity/bonus component to discuss.

---

## 6. Questions to Ask Abdul

Good questions signal you're already thinking like a lead:

1. **"What does the current architecture look like for the microservices layer — are we greenfield or migrating existing services?"**
2. **"What's the team composition — how many engineers, and what's the split between senior and mid-level?"**
3. **"What does the DevOps ownership model look like — do engineers own their own deployments, or is there a dedicated platform team?"**
4. **"What's the biggest technical challenge the team is working through right now?"**
5. **"What would success look like at 90 days for someone in this role?"**

Avoid: salary (done), vacation, "what does your company do" (know it already).

---

## 7. Sean's Strongest Differentiators (Close With These If Given The Chance)

1. **20+ years, not just years — depth.** CITI 8 years in production financial systems, real compliance, real scale. This is a financial services company — that background is gold.
2. **Full-stack data + platform engineering.** You're not a pure data engineer who can't touch infra, and not a pure DevOps who can't touch data. You bridge both — that's exactly what the job description is.
3. **Dynatrace in production.** Most candidates will say "I know CloudWatch" — you can say "I used DynaTrace AppMon and Synthetics at scale in a Tier-1 financial institution."
4. **GenAI / Bedrock experience.** Toyota is a large enterprise. They'll be thinking about AI tooling. You've built Text-to-SQL agents on Bedrock — very few lead candidates can say that.
5. **Already in Plano.** Murphy TX is 12 miles away. No relocation friction, ready day one.

---

## 8. Reference Files

| File | Location |
|---|---|
| Full job rec | `D:\Workarea\jobsearch\data\jobs\url_captures\toyota_req_10301655_capture_2026-04-24.md` |
| 13-phase technical roadmap | `D:\Workarea\jobsearch\data\interview_prep\active_interviews\toyota_technical_interview_roadmap.md` |
| Recruiter screen notes | `D:\Workarea\jobsearch\data\interview_prep\active_interviews\toyota_ramya_recruiter_1655.md` |
| Personal profile | `D:\Workarea\jobsearch\docs\sean_girgis_profile.json` |
| This document | `D:\Workarea\jobsearch\docs\toyota_hm_interview_apr30.md` |

---

*Last updated: 2026-04-27 | Interview: 2026-04-30 11:00 AM CT*
