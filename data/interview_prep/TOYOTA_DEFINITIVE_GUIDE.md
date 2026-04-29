# Toyota Financial Services — Definitive Interview Guide
**Sean Luka Girgis · seanlgirgis@gmail.com · 214-315-2190**
**Last updated: 2026-04-28**

---

## Table of Contents

- [1. The Interview — Full Logistics](#1-the-interview--full-logistics)
- [2. The Journey — How We Got Here](#2-the-journey--how-we-got-here)
- [3. Honest Assessment — What This Interview Will Look Like](#3-honest-assessment--what-this-interview-will-look-like)
- [4. Sean vs The Job — Fit Analysis](#4-sean-vs-the-job--fit-analysis)
- [5. The Mindset — You Are the Architect](#5-the-mindset--you-are-the-architect)
- [6. Your Three Flagship Stories (Architect Framing)](#6-your-three-flagship-stories-architect-framing)
- [7. The Answer Framework — Every Design Question](#7-the-answer-framework--every-design-question)
- [8. Topic-by-Topic Prep — Priority Order](#8-topic-by-topic-prep--priority-order)
- [9. The 2.5-Day Roadmap](#9-the-25-day-roadmap)
- [10. Audio Repair Plan](#10-audio-repair-plan)
- [11. The Gap Answers — Exactly What to Say](#11-the-gap-answers--exactly-what-to-say)
- [12. Questions to Ask Abdul](#12-questions-to-ask-abdul)
- [13. Day-of Logistics Checklist](#13-day-of-logistics-checklist)

---

## 1. The Interview — Full Logistics

| Field | Detail |
|---|---|
| **Date** | Thursday, April 30, 2026 |
| **Time** | 11:00 AM – 11:45 AM (America/Chicago CT) |
| **Format** | Microsoft Teams (video — camera on) |
| **Meeting ID** | 244 798 544 632 556 · Passcode: sU6yz9z7 |
| **Duration** | 45 minutes |
| **Interviewer** | **Abdul Jaleel Dudekula** — Hiring Manager |
| **Role** | Lead Software Engineer (Python, API Microservices, DevOps) |
| **Req** | 10301655 |
| **Salary Target** | $185,000 base — one number, no range, no qualifiers |
| **Location** | Plano TX — 4 days onsite, Murphy TX ≈ 12 miles ✅ |

**Join 5 minutes early. Camera on. Notes visible on second screen. Teams working and tested night before.**

---

## 2. The Journey — How We Got Here

### The First Toyota — March 2026
Applied March 11 via LinkedIn pipeline — Lead Python Developer, different req. Pipeline auto-accepted it with an 85% score. That application is archived as job `00039_76829368`.

### Codie Marcell — April 21
Codie Marcell (Toyota Recruiting Team) reached out independently about req 10301655 — a new position: Lead Software Engineer, Python / API Microservices / DevOps. This was a separate, higher-signal opportunity. Codie ran a 30-minute recruiter screen. Passed. Referred to Ramya.

### Ramya Ravichandran — April 23 ✅ PASSED
**Ramya Ravichandran** — recruiter at Toyota Financial Services — ran a 45-minute phone screen on Thursday April 23, 2026 at 10:00 AM CT.

**What happened:** Ramya called. She said she was impressed with the resume. She noted there had been a reorg that week and she was initially inclined to reschedule — but she went ahead. Her instinct after the reorg was to share the resume upward, because the new position being created needed exactly this profile.

**How it went:** Good. Strong enough to pass cleanly. She moved you forward to the hiring manager.

**What Ramya flagged as a gap:** Terraform — explicitly. She noted it as a tool gap but did not kill the candidacy over it. Her exact signal: *you haven't used it in production.* The right response was honest and you gave it.

**What Ramya signaled the HM will focus on:**
- End-to-end architecture ownership — can you design the full system, not just write code?
- DevOps and containerization — Docker to ECS deployment, not just knowledge
- API design at scale — FastAPI, versioning, rate limiting, 12-factor patterns
- CloudFormation — she named it specifically (AWS-native IaC alternative to Terraform)
- Architectural decision-making — tradeoffs, not just implementation

**Salary stated:** $185,000. She did not push back.

### Confirmation — April 28
Official invite received from Toyota Recruiting Team. Abdul Jaleel Dudekula confirmed as interviewer. 45 minutes. Teams link issued.

---

## 3. Honest Assessment — What This Interview Will Look Like

### Abdul's Likely Format (45 min HM screen)
Abdul is a **Hiring Manager, not a pure technical screener.** In a 45-minute HM interview at a financial services company for a Lead role, the breakdown is typically:

| Block | Time | What Happens |
|---|---|---|
| Introductions + your pitch | 5–8 min | He leads, you give 90-second architect-framing opener |
| 2–3 technical design questions | 20–25 min | He picks a scenario — you walk the architecture |
| Leadership / behavioral | 8–10 min | Tell me about a time… mentor, conflict, ambiguity |
| Your questions to him | 5–7 min | You ask 2 smart questions — this is judged too |

### What He Will NOT Do
- He will not ask you to write code on a whiteboard or screen share
- He will not ask you leetcode or algorithm puzzles
- He will not go deep into Terraform syntax

### What He WILL Do
- Ask you to design something end-to-end — expect one real system design question
- Ask how you approach architecture decisions — tradeoffs, not just answers
- Ask about a hard project — probe for depth, ownership, scale
- Ask about mentoring or leading junior engineers
- Test whether you can own the technical conversation as a Lead, not just answer questions

### His Key Assessment: "Can This Person Lead the Platform?"
Abdul needs to leave the call believing you can:
1. Own the architecture of a Python microservices platform end-to-end
2. Make decisions under ambiguity with confidence
3. Bring junior engineers along
4. Communicate clearly to stakeholders

**You can do all four. The gap is framing, not substance.**

### The One Risk
The Terraform gap is known. If he presses it, own it in exactly one sentence and move immediately to what you have. Do not over-explain. CloudFormation, CDK, and deep AWS-native experience are the credible offset.

### The Hidden Opportunity
Dynatrace. Very few Python platform engineers have real production Dynatrace experience. You built the FAST project at G6 — you mined AppMon telemetry for real-user performance data that drove revenue optimization. That is genuinely rare and maps directly to Toyota's observability stack. Use it.

---

## 4. Sean vs The Job — Fit Analysis

### Strong — Lead With These
| Requirement | Your Evidence |
|---|---|
| Python — advanced platform grade | 20+ years. Citi: reusable ETL frameworks consumed by multiple teams. HorizonScale: PySpark + Prophet + scikit-learn at scale. G6: Dynatrace AppMon ETL pipeline. |
| AWS ecosystem | S3 landing zone, Glue ETL, Redshift analytics, ECS/Fargate containerized Python, Lambda triggers, CloudWatch instrumentation — all production at Citi. |
| Data pipelines / ETL at scale | 6,000+ endpoints, 65,000+ rows/month, 4 global regions, Oracle → AWS migration |
| Dynatrace | G6 Hospitality: AppMon API extraction, real-user performance mining, FAST project — directly relevant to Toyota's observability stack |
| Kafka / MSK awareness | CA Technologies + AT&T telco environments — event-driven architecture context |
| Docker / containers | ECS/Fargate at Citi, Docker packaging of Python ETL jobs |
| ML forecasting | Prophet + scikit-learn + PySpark — HorizonScale, deployed on AWS, 90%+ accuracy |
| Financial services discipline | 8 years Citi — compliance, reliability, regulated environment — same as TFS |
| Lead / mentor experience | Built onboarding templates, code review standards, made team self-sufficient |

### Partial — Prep These
| Requirement | Gap | Your Honest Frame |
|---|---|---|
| FastAPI | Know REST API design; FastAPI idioms need 4-hour sprint | "Python-first, async-ready, I've been building with the patterns" |
| ECS deployment hands-on | Know Docker; ECS task definition syntax needs one drill | ECS task def cheat sheet tonight |
| **Terraform** | Not in production — **flagged by Ramya** | "Tool gap, not knowledge gap — IaC model is identical to CloudFormation which I have" |
| CloudFormation | Understand deeply; need to write one real YAML stack | 2-hour drill tomorrow |
| pytest depth | Testing exists; fixtures/parametrize/mocking need polish | "Test-driven practice — here's how I structured testing at Citi" |
| JWT/OAuth2 | Know concepts — need one coded FastAPI middleware example | 30-min tonight |

### Thin — Acknowledge If Asked, Never Volunteer
- PyIceberg / Snowflake internals
- GitHub Actions YAML from memory (know the concept)
- Kafka from-scratch configuration (know MSK architecture, not raw broker config)

---

## 5. The Mindset — You Are the Architect

Every single answer must come from this frame:

> **You are not a developer who writes Python.**
> **You are an architect who owns the platform.**

The shift:
| Developer framing ❌ | Architect framing ✅ |
|---|---|
| "I built a pipeline that processed 6,000 endpoints" | "The architectural challenge was: how do you process telemetry from 6,000 assets in parallel, apply ML forecasting per asset, and surface bottleneck predictions in near-real-time at banking-scale reliability?" |
| "I used Prophet for forecasting" | "I chose Prophet over ARIMA because Prophet handles seasonality decomposition natively — critical for infrastructure telemetry with daily, weekly, and quarterly cycles." |
| "I containerized ETL jobs with Docker" | "Each pipeline workload is independently deployable as a Fargate task — that's the core microservices principle applied to data pipelines. One failing asset doesn't block the fleet." |
| "I haven't used Terraform in production" | "My AWS infrastructure was provisioned through CloudFormation and AWS-native tooling. The IaC model is identical — declarative desired state, reconciliation. Terraform is HCL syntax on the same mental model." |

**Your anchor phrase — say this early, repeat it:**
> *"My approach is always requirements first, then architecture, then implementation.
> I make decisions based on tradeoffs — not on what's familiar,
> but on what solves the actual problem at the scale required."*

---

## 6. Your Three Flagship Stories (Architect Framing)

### Story A — HorizonScale (Your Flagship)
**Use when:** Most impactful project · Python at scale · ML in production · Automation · Architecture ownership

**The architecture pitch:**
> "The challenge was: how do you forecast capacity for 2,000+ infrastructure assets, across four KPIs, six months ahead, when the legacy process was a ten-day manual Excel cycle?
>
> I evaluated sequential batch processing versus a generator-based parallel architecture.
> Sequential wouldn't scale — 8,000 time series processed one by one was hours, not minutes.
> I chose a generator-based parallel design where each asset pipeline runs independently —
> natural fault isolation, simultaneous processing, no single point of failure.
>
> For the ML layer I chose Prophet over ARIMA — Prophet handles seasonality decomposition
> natively, which is critical for infrastructure telemetry with daily, weekly, and quarterly cycles.
> I added scikit-learn classifiers for binary risk flagging — at-risk or not —
> so stakeholders got a signal they could act on, not just a probability score.
>
> For cloud scale: AWS Glue with PySpark Grouped Map UDFs for distributed forecasting across
> the full fleet. S3 as the data lake. Athena for ad-hoc querying of forecast outputs.
> Streamlit dashboard for real-time leadership visibility.
>
> Result: 90% cycle time reduction. Six-month-ahead bottleneck prediction at 90%+ accuracy.
> Ten days manual to minutes automated."

**Key numbers cold:** 2,000+ servers · 4 KPIs · 8,000+ time series · 180-day horizon · 90% accuracy · 90% cycle time cut

---

### Story B — Citi Capacity Planning Platform (The Scale Story)
**Use when:** End-to-end platform ownership · ETL at enterprise scale · Automation · Financial services

**The architecture pitch:**
> "The architectural problem was a 10-day manual Excel process across 65,000+ endpoints in
> four global regions. Every month, capacity analysts pulled P95 telemetry from BMC TrueSight
> manually, enriched it from AppDynamics and the CMDB, applied safety factors in spreadsheets,
> and published reports to enterprise teams. Reactive, error-prone, and didn't scale.
>
> I replaced the entire workflow with a Python ETL platform.
> SQLAlchemy + cx_Oracle for direct database queries — no manual exports.
> Pandas + NumPy for vectorized transformation across 65,000+ rows.
> The hardest architectural decision: resolving identifier mismatches across three source systems
> with different naming conventions. I built a normalized lookup layer that joined them reliably
> at scale — that was the real engineering problem, not the ETL itself.
> openpyxl generated the Excel workbooks deterministically. Streamlit provided the internal dashboard.
> GitLab with merge-required PRs for every logic change — no cowboy pushes.
>
> Result: Reports that took 5–10 days produced in the first hour after monthly data was available.
> Same deliverables, identical format, deterministic logic applied to every row every month."

---

### Story C — G6 / FAST Project (The Dynatrace Story)
**Use when:** Observability · Dynatrace · ETL for business impact · Data-driven optimization

**The architecture pitch:**
> "G6 Hospitality — Motel 6 parent — had performance problems on Brand.com, their
> revenue-generating ecommerce site. No one had a clear picture of where real users
> were experiencing slowdowns. They had infrastructure metrics, but not user behavior data.
>
> I built the FAST project — Find And Stop Trouble. An ETL pipeline that extracted
> real-user performance data directly from Dynatrace AppMon via its API.
> Transaction traces, response times, error rates, user journey data.
> I applied data mining to segment by transaction type, geography, and device —
> not to find the worst server, but to find the worst user experience.
>
> The architectural insight: infrastructure metrics are a lagging indicator.
> Real-user telemetry from Dynatrace is a leading indicator — it tells you
> what users experienced before the infrastructure alert fires.
>
> Result: Identified specific bottlenecks in checkout and search flows.
> The performance problem was not infrastructure capacity — it was specific code paths
> and third-party integrations that synthetic tests had missed entirely."

**Dynatrace hook for TFS:**
> "Toyota Financial Services uses Dynatrace for observability — I've used it in production
> for real-user performance analysis, not just infrastructure monitoring. That's a different
> level of Dynatrace fluency than most engineers have."

---

## 7. The Answer Framework — Every Design Question

When Abdul asks you to design anything, follow this pattern every time:

```
1. REQUIREMENTS FIRST
   "Before I jump to architecture, let me nail down the requirements.
   What's the scale — requests per second, data volume, SLA?
   Any compliance constraints? Existing systems I need to integrate with?"

2. IDENTIFY THE COMPONENTS
   Data layer → Service layer → API layer → Infrastructure layer

3. EVALUATE TRADEOFFS — NAME THEM
   "I evaluated X versus Y. X gives us [benefit] but costs [tradeoff].
   Y is simpler but doesn't scale past [point]. I chose X because..."

4. MAKE THE DECISION AND OWN IT
   State the choice. State why — one or two reasons.
   State what you'd watch for (failure modes, where it breaks at 10x).

5. PLAN FOR SCALE
   "What breaks first at 10x load? The [component].
   I'd add [cache / read replica / async queue / more ECS tasks]
   and measure with CloudWatch before over-provisioning."
```

**The standard end-to-end stack for TFS context:**
```
External Systems / Events
        ↓
  API Gateway (entry, auth, rate limiting)
        ↓
  Lambda / ECS service (business logic)
        ↓
  SQS (async decoupling)
        ↓
  ECS / Fargate (ETL / processing workers)
        ↓
  S3 (raw landing) → Glue ETL → Redshift (analytical)
        ↓
  FastAPI service (internal API layer)
        ↓
  Downstream consumers
```

---

## 8. Topic-by-Topic Prep — Priority Order

### Priority 1 — Must Own Cold (Interview will go here)

**Architectural Thinking**
- Requirements → Components → Tradeoffs → Decision → Scale
- Practice speaking the framework out loud — not reading it
- Time yourself: can you walk an architecture in 4 minutes?

**End-to-End System Design**
- Draw the TFS stack from memory: API Gateway → ECS → SQS → Glue → S3 → Redshift
- Be able to add Kafka/MSK for event streaming between services
- Be able to swap Redshift for Snowflake and explain why you would

**Your Three Stories in Architect Framing**
- HorizonScale: generator-based parallel architecture, Prophet seasonality, PySpark at scale
- Citi Capacity Platform: normalized lookup layer, deterministic ETL, GitLab discipline
- G6 FAST Project: real-user telemetry vs synthetic, Dynatrace API, leading vs lagging indicator

---

### Priority 2 — Know Well (Will Come Up)

**Terraform Gap Answer — One Sentence**
> "I haven't used Terraform in production — my AWS work was provisioned through CloudFormation
> and AWS-native tooling. The declarative IaC model is identical — tool gap, not knowledge gap.
> I've been hands-on with HCL since and can apply it."
Own it. Move on. Never over-explain.

**CloudFormation**
- Stack → Template → Parameters → Outputs → Change Sets
- Be able to describe an ECS Fargate service stack verbally
- Know: Change Set = preview before applying; Stack Set = multi-account deploy

**Docker + ECS/Fargate**
- Image layers, multi-stage build, CMD vs ENTRYPOINT
- ECS: Cluster → Task Definition → Service → ALB → Auto Scaling
- Fargate = serverless compute, no EC2 management
- Be able to describe deploying a Python FastAPI container to ECS

**FastAPI**
- Resource-based URLs, HTTP verbs, status codes, pagination, versioning
- Pydantic models for request/response validation
- Dependency injection, JWT authentication, OpenAPI docs at /docs
- Scaling: ECS horizontal scale, ElastiCache for read-heavy, SQS for async operations

**API Scaling Conversation**
> "My approach to API scaling starts with understanding what's actually slow.
> CPU? Add ECS tasks. Database bottleneck? Read replica + RDS Proxy.
> Repeated reads? ElastiCache cache-aside pattern.
> Long-running jobs? Decouple with SQS — API accepts, queues, returns job ID, client polls."

---

### Priority 3 — Credible Framing (Might Come Up)

**CI/CD Pipeline**
- Build → Test → Deploy gates: lint, unit tests, Docker build, push to ECR, ECS update
- Blue-green vs rolling deploy — know the difference and when to use each
- Automatic rollback on health check failure

**Testing Strategy**
- Unit tests: business logic, fast, no I/O
- Integration tests: service boundaries — API → DB, ETL transformation
- Contract tests: API shape matches OpenAPI spec
- pytest: fixtures, parametrize, mock for external calls
- Be able to describe your testing approach at Citi: GitLab CI, merge-required, coverage targets

**MSK / Kafka**
- Topic → Partition → Consumer Group → Offset
- SQS vs MSK: SQS = task queues; MSK = event streams, replay, fan-out
- Partition key by natural key (account ID) — preserves order per entity
> "For real-time event streaming I use MSK. The key design decision is partition count —
> partition by a natural key like account ID so all events for one account land in the
> same partition, preserving order."

**Observability**
- Three pillars: Metrics (CloudWatch) · Logs (structured JSON → CloudWatch/OpenSearch) · Traces (X-Ray)
- Dynatrace: full-stack APM — correlates infra metrics, application traces, user sessions
- Always instrument: request count, response time, error rate, queue depth

---

### Priority 4 — Honest Frame If Asked

**Snowflake / PyIceberg**
> "For a data lake I use S3 with Iceberg as the table format — ACID guarantees, schema evolution,
> time travel on top of object storage. Glue Catalog manages the metadata.
> Snowflake connects to Iceberg tables as external tables for sub-second query performance."

**OpenSearch**
> "For log aggregation: ECS containers → Kinesis Firehose → OpenSearch.
> CloudWatch handles metrics and alarms. OpenSearch handles log search and operational dashboards.
> Each tool doing what it does best."

---

## 9. The 2.5-Day Roadmap

### Tuesday April 28 — Evening (Tonight)

| Time | Task |
|---|---|
| Now | Read this guide end-to-end. Internalize the mindset shift. |
| 1 hour | Speak Story A (HorizonScale) out loud in architect framing. Time it at 4 minutes. Record yourself. |
| 1 hour | Speak Story C (G6/FAST/Dynatrace) out loud. Why real-user telemetry beats synthetic. |
| 30 min | FastAPI + JWT — read [fastapi.html](D:\Workarea\seanlgirgis.github.io\learning\fastapi.html), write one mental model for dependency injection |
| 30 min | Review [aws-ecs.html](D:\Workarea\seanlgirgis.github.io\learning\aws-ecs.html) — Cluster → Task Def → Service → ALB cold |
| **Audio** | Listen to `final_data-architecture.mp3` while doing anything else |

### Wednesday April 29 — Full Day

| Time | Task |
|---|---|
| Morning | Listen: `final_pipeline-design.mp3` + `final_system-design-for-data-engineers.mp3` |
| 1.5 hours | **Architect drill:** Draw the TFS end-to-end stack from memory. Add MSK. Add Snowflake. Explain each choice out loud. |
| 1.5 hours | **CloudFormation:** Read [aws-cloudformation.html](D:\Workarea\seanlgirgis.github.io\learning\aws-cloudformation.html). Describe an ECS stack verbally: Cluster → TaskDef → Service → ALB → IAM Role → LogGroup. |
| 1 hour | **Terraform framing:** Read [terraform.html](D:\Workarea\seanlgirgis.github.io\learning\terraform.html). Practice the one-sentence gap answer 5 times cold. |
| 1 hour | Speak Story B (Citi Capacity Platform) out loud in architect framing. |
| 1 hour | **Mock Q&A drill:** Have someone ask you these 5 questions — answer without notes: (1) Walk me through your approach to end-to-end architecture. (2) Tell me about HorizonScale. (3) What's your Terraform experience? (4) How do you scale a FastAPI service? (5) Tell me about your testing approach. |
| Evening | Listen: `final_terraform.mp3` + `final_fastapi.mp3` + `final_aws-ecs.mp3` |
| **Audio repair** | Re-record any audio segments that need fixing |

### Thursday April 30 — Morning Before 11 AM

| Time | Task |
|---|---|
| 7:00–8:00 AM | Listen: `final_cicd-github-ecs.mp3` + `final_aws-cloudformation.mp3` |
| 8:00–8:30 AM | Read this guide: Section 6 (Stories) and Section 11 (Gap Answers) only |
| 8:30–9:00 AM | Speak anchor phrase 10 times. Speak Terraform gap answer 10 times. |
| 9:00–10:00 AM | Rest. Walk. Eat. No new material. |
| 10:00 AM | Teams open, tested, microphone/camera checked |
| 10:30 AM | Notes open on second screen. This guide at Section 6. |
| 10:55 AM | Join Teams lobby |

---

## 10. Audio Repair Plan

The existing audio files have quality issues — Sean's voice needs re-recording. This is separate from the interview prep and should not block study.

**What to repair (Toyota-critical files first):**
1. `final_data-architecture.mp3` — already in Toyota playlist
2. `final_pipeline-design.mp3` — already in Toyota playlist
3. `final_system-design-for-data-engineers.mp3` — already in Toyota playlist
4. `final_terraform.mp3`
5. `final_fastapi.mp3`
6. `final_aws-ecs.mp3`
7. `final_aws-cloudformation.mp3`

**Updated Toyota playlist to create (`tayota_final.m3u`):**
```
#EXTM3U
final_data-architecture.mp3
final_pipeline-design.mp3
final_system-design-for-data-engineers.mp3
final_terraform.mp3
final_fastapi.mp3
final_aws-ecs.mp3
final_aws-cloudformation.mp3
final_aws-msk-kafka.mp3
final_cicd-github-ecs.mp3
final_g6-appmon.mp3
final_horizon-scale.mp3
final_interview-master.mp3
```

**Audio locations:** `D:\temp\studybook_audio\<topic>\final_<topic>.mp3`
**Phone sync script:** `D:\Workarea\StudyBook\scripts\sync_studybook_to_phone.ps1`

---

## 11. The Gap Answers — Exactly What to Say

### Terraform (Most Likely Gap Question)
> "I'll be straight — I haven't used Terraform in production.
> My AWS infrastructure work at Citi was provisioned through CloudFormation
> and internal AWS-native tooling. The IaC mental model is identical —
> you declare desired state, the tool reconciles reality to match it.
> I've been hands-on with HCL since, and the syntax is straightforward
> given deep AWS architecture experience. Tool gap, not knowledge gap."

**One sentence. Pause. Move on.**

### FastAPI (If He Presses)
> "I've been building REST APIs in Python for years — the FastAPI idioms are
> Python-native and approachable. I've been deepening my FastAPI hands-on
> experience specifically because I knew this role required it.
> The Pydantic models, dependency injection, and async patterns are clear —
> the learning curve is minimal for someone with strong Python and REST backgrounds."

### Testing (If He Asks for Depth)
> "My testing approach is pyramid-shaped. Unit tests cover all business logic —
> fast, deterministic, no I/O. Integration tests cover service boundaries —
> does the API talk correctly to the database, does the ETL transform correctly.
> At Citi I established code review standards that required CI to pass
> before any merge. Coverage target was 80%+ on core logic.
> For data pipelines specifically, I treat validation logic as code —
> schema checks, business-rule validation, dead-letter routing for bad records."

---

## 12. Questions to Ask Abdul

Ask exactly two — in this order:

**Question 1 (Highest signal):**
> "What does success look like for this role in the first 90 days?
> I want to understand where you most need a Lead to take ownership immediately."

**Question 2 (Shows platform thinking):**
> "What's the biggest architectural challenge the team is working through right now —
> the thing that keeps you up at night from a platform perspective?"

**If time permits — Question 3:**
> "What's the team structure — how many engineers, what levels, and how does
> the Lead interact with the principal and senior ICs day to day?"

**Do NOT ask about salary, benefits, or PTO in this round.**

---

## 13. Day-of Logistics Checklist

- [ ] Teams installed, tested — join a test meeting Wednesday evening
- [ ] Camera on, good lighting, quiet room confirmed
- [ ] Phone charged — 214-315-2190 as backup if Teams fails
- [ ] This guide open on second screen at Section 6
- [ ] Key numbers cold: **20+ years · 8 years Citi · 6,000+ endpoints · 65,000+ rows · 90% accuracy · 90% cycle reduction · $185,000**
- [ ] Anchor phrase ready: *"Requirements first, architecture second, implementation third. Tradeoffs drive decisions."*
- [ ] Terraform gap answer practiced to reflex: own it in one sentence, move on
- [ ] Dynatrace story ready — this is a differentiator
- [ ] Salary: **$185,000 base** — say it once, pause, do not add qualifiers
- [ ] Start date: **Immediately** — not "one week notice"
- [ ] Work authorization: **US Citizen** — no visa, no sponsorship

---

*This is your guide. Own it. You have the substance — this is about framing and delivery.*
*You built real platforms at banking scale. Abdul needs to see the architect, not the implementer.*
*Show him the architect.*
