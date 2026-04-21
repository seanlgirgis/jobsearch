# Toyota Financial Services — Lead Python Developer
**Recruiter:** Codie Marcell (Toyota Recruiting Team)
**Call:** Tuesday April 21, 2026 — 1:00 PM CT
**Phone:** They call you at 214-315-2190
**Format:** 30 min recruiter screen — background filter, no live coding

---

## Table of Contents

- [Mock Feedback — April 21](#mock-feedback--april-21)
- [Reading Codie](#reading-codie)
- [The Role In Plain English](#the-role-in-plain-english)
- [Salary](#salary)
- [Your Opening 2 Minutes](#your-opening-2-minutes-toyota-version)
- [Key Reframe: Capital One vs Toyota](#key-reframe-capital-one-vs-toyota-language)
- [Your 4 Key Stories](#your-4-key-stories-toyota-framing)
- [Likely Questions Codie Will Ask](#likely-questions-codie-will-ask)
- [What Codie Will NOT Ask](#what-codie-will-not-ask-save-for-technical-screen)
- [Questions To Ask Codie](#questions-to-ask-codie)
- [Logistics Checklist](#logistics-checklist)
- [After The Call](#after-the-call)
- [Technical Screen Prep](#technical-screen-prep--full-gap-coverage)
  - [Python OOP & Framework Design](#python-oop--framework-design)
  - [Apache Airflow](#apache-airflow--dag-design)
  - [APIs & Microservices](#apis--microservices)
  - [Real-Time Streaming / Kafka](#real-time-streaming--kafka)
  - [Data Validation Frameworks](#data-validation-frameworks)
  - [Logging, Testing, Security & Instrumentation](#logging-testing-security--instrumentation)
  - [Docker & CI/CD](#docker--cicd)
  - [SQL & NoSQL](#sql--nosql-databases)
  - [Version Control](#version-control--branching--code-reviews)
  - [Mentoring Engineers](#mentoring-engineers)
  - [Hiring & Talent Attraction](#hiring--talent-attraction)
  - [Self-Service Tools](#self-service-tools--frameworks)
  - [Why Toyota — Company Research](#why-toyota-specifically--company-research)
  - [Job Requirements Coverage Checklist](#job-requirements-coverage-checklist)

---

## Mock Feedback — April 21

> Notes from live mock drill on April 21, 2026.

**Overall: Strong — would move forward from this call.**

### What Landed Well ✓
- ETL pipeline story — 10 days to 2 days is concrete and memorable
- ML forecasting depth — Prophet, scikit-learn, seasonality, 6-month horizon
- Campus/Plano detail — genuine personal touch, stood out
- Questions at the end — exactly the right two to ask
- Closing strong — confident without being pushy

### Three Things To Tighten ⚠
1. **Salary — single anchor, not a range.** Said $175K–$185K which hands them the lower number. Always anchor at **$185,000 base**, full stop.
2. **"Continuous improvement" not "coniferous"** — likely nerves. For Toyota, the word is **Kaizen** — use it naturally, it signals homework done.
3. **Opening missing platform framing** — add: *"My focus has always been building reusable platforms — not just pipelines for one team, but frameworks that accelerate delivery across the entire organization."*

### Start Date
Said "one week notice" — prep doc says **immediately**. Immediately is stronger at recruiter stage.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Reading Codie

- Recruiter, not a technologist — don't go deep on stack
- Toyota uses automated scheduling (Phenom) — large recruiting operation
- Same playbook as Sam Ali: warm, confident, concise, let them lead

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## The Role In Plain English

Toyota Financial Services Enterprise Platforms team needs someone to **build reusable Python frameworks and tools that other engineering teams consume** — not just pipelines for one use case, but platforms at enterprise scale.

This is different from Capital One's "build a pipeline" ask.
Toyota wants: **"I build the tools that let OTHER engineers build faster."**

That framing must come through in every answer.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Salary

Toyota Financial Services Plano market rate: ~$160k–$195k for Lead Python Developer.

**Your number: $185,000 base — single anchor, no range.**
> "Based on the role and my experience, I'm targeting around $185,000 base.
> I'm flexible depending on the overall package."

**Do NOT say a range.** Giving $175K–$185K hands them the lower number. Say $185K once, then pause.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Your Opening 2 Minutes (Toyota Version)

> "I'm in Plano — great fit for your location. I'm a Lead Python Developer
> and Data Engineer with over 20 years of experience, and my sweet spot
> is exactly what this role describes: building reusable Python frameworks
> and platforms that other engineering teams build on top of.
>
> My focus has always been building platforms — not just pipelines for one
> team, but reusable frameworks that accelerate delivery across the entire
> organization. That's a thread through my entire career.
>
> Most recently I spent 8 years at Citi where I owned the entire data
> infrastructure for capacity planning — I didn't just build pipelines,
> I built the reusable framework that automated the entire process across
> 6,000+ endpoints. Python, Airflow orchestration, AWS cloud platform,
> Docker — all production-grade, all built to be consumed by other teams
> not just by me.
>
> One of my recent projects, HorizonScale, is a platform I built from scratch
> — a full AI-driven capacity forecasting engine with a reusable pipeline
> architecture, Streamlit dashboards, and ML forecasting. That's the kind
> of platform thinking I bring to a Lead role.
>
> The TFS Enterprise Platforms team is exactly the environment I'm
> looking for — hands-on technical lead, building at enterprise scale,
> in Plano. And honestly, Toyota's Kaizen culture — continuous improvement —
> is exactly how I approach engineering. You ship a framework, you iterate,
> you make it better."

*(Target: 90 seconds. Hits: Plano, frameworks, platform thinking, Citi, HorizonScale, Kaizen)*

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Key Reframe: Capital One vs Toyota Language

| Capital One framing | Toyota framing |
|--------------------|---------------|
| "I built data pipelines" | "I built reusable frameworks other teams consume" |
| "I automated ETL processes" | "I built automation platforms that accelerated delivery across teams" |
| "I built an AWS hybrid platform" | "I architected a cloud-native platform with enterprise standards" |
| "I built ML forecasting" | "I built a scalable forecasting engine designed for reuse and extensibility" |

The work is the same. The framing shifts from **"I solved my team's problem"** to **"I built the platform that solves everyone's problem."**

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Your 4 Key Stories (Toyota Framing)

### Story 1 — Reusable ETL Framework at Scale
**Situation:** Citi had a fragmented, manual capacity planning process across 6,000+ endpoints — Excel sheets, 10-day cycle, error-prone.
**Task:** Build something automated, reusable, and reliable — not a one-off script.
**Action:** Designed a Python framework with reusable ingestion modules pulling from BMC TrueSight, AppDynamics, and other systems. Pandas transformation layers, Oracle schemas built for historical retention and extensibility. Any new data source could be onboarded without rewriting core logic.
**Result:** Reports delivered in the first 2 days of each month instead of 10. Multiple teams consumed the framework. Errors eliminated. Unified disparate feeds into a single reporting platform.

> *Use when asked: "Tell me about a Python framework or platform you built"*

---

### Story 2 — HorizonScale Platform (Your Flagship for Toyota)
**Situation:** Legacy forecasting was manual, slow, and not reusable across infrastructure domains.
**Task:** Build a full AI-driven forecasting platform — not a script, a platform.
**Action:** Architected HorizonScale from scratch: parallel generator-based pipeline (90% faster), Prophet + scikit-learn ML models accounting for seasonality and holidays, Streamlit dashboard for real-time insights, RAG-based agentic reasoning layer. Built for extensibility — new data sources plug in without touching core logic.
**Result:** Forecasting cycles reduced 90%. 6-month ahead bottleneck prediction at 90%+ accuracy. Platform designed so other engineers could extend it without depending on me.

> *Use when asked: "Tell me about a project you're most proud of" / "Show me platform thinking"*

---

### Story 3 — AWS Cloud-Native Platform
**Situation:** Oracle on-prem couldn't scale for ML forecasting workloads.
**Task:** Extend to AWS without disrupting existing reporting.
**Action:** Designed hybrid architecture — S3 landing zone, Glue ETL, Redshift for analytics, Docker/ECS for containerized Python workloads. Built with reusability — each layer independently testable and replaceable.
**Result:** Cloud-native platform at enterprise scale. On-prem reporting intact. Forecasting workloads scaled on demand.

> *Use when asked: "AWS experience" / "Cloud-native platform design"*

---

### Story 4 — Mentoring and Technical Leadership
**Situation:** At Citi, junior engineers needed to onboard to complex pipeline infrastructure.
**Task:** Reduce dependency on me and raise team capability.
**Action:** Built documentation standards, code review practices, and onboarding templates. Mentored engineers on Python best practices, pipeline patterns, and AWS tooling. Goal was to make myself replaceable on the details.
**Result:** Team became self-sufficient on the framework. Onboarding time reduced significantly. Code quality improved measurably.

> *Use when asked: "Tell me about your leadership style" / "Mentoring experience"*

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Likely Questions Codie Will Ask

### "Tell me about yourself"
Use the Opening 2 Minutes above. Hit platform framing hard.

**Concise recruiter version (45-60 seconds):**
> "I'm a Senior Data Engineer and Python developer with over 20 years of experience
> building scalable data platforms and reusable frameworks. I'm based in Plano,
> so the location is a perfect fit. Most recently at Citi, I led capacity-planning
> data infrastructure across more than 6,000 endpoints, building reusable automation
> and ML forecasting platforms that reduced manual effort by 90% and improved
> planning accuracy significantly. What I'm looking for is a hands-on lead role
> where I build reusable Python frameworks that help multiple teams move faster —
> which is exactly the Toyota Financial Services Enterprise Platforms mission."

---

### "Why Toyota / Why TFS?"
> "Toyota Financial Services sits at the intersection of two things I find
> genuinely compelling — financial-scale data problems and Toyota's engineering
> culture. The Toyota Way, Kaizen — continuous improvement — is honestly how I
> approach platform engineering. You ship a framework, you iterate, you make
> it better. That philosophy fits me naturally. And Plano is home — this is
> exactly where I want to be doing this work."

---

### "What are you looking for in your next role?"
> "Hands-on technical lead work — building Python platforms and frameworks
> at enterprise scale. I want to design the architecture and get into the code,
> not purely manage. The Lead Python Developer title at TFS fits that perfectly."

---

### "Why are you leaving / what happened at Citi?"
> "I was at Citi for 8 years and delivered strong results. My role was eliminated
> as part of a broader organizational restructuring — not performance related.
> I've used the time to sharpen my skills and I'm now actively looking for the
> right long-term fit. TFS is at the top of my list."

---

### "Are you interviewing elsewhere?"
> "Yes, I have a few conversations in progress — including with Capital One and
> Samsung. That said, Toyota Financial Services is one of my top priorities
> because of the enterprise platform focus, the long-term stability, and the
> Kaizen culture that strongly matches how I work."

---

### "What's your salary expectation?"
> "Based on the role and my experience, I'm targeting around $185,000 base.
> I'm flexible depending on the full comp package."

**Say $185,000 once. Pause. Do not offer a range.**

---

### "When can you start?"
> "I am available to start immediately and can align with your preferred onboarding timeline."

---

### "Do you require sponsorship?"
> "No. As a U.S. citizen I'm fully authorized to work for any employer and do not require sponsorship now or in the future."

---

### "Airflow experience?"
> "Yes — Airflow for orchestrating ETL pipelines at Citi. DAG design, task dependencies,
> retry logic, scheduling. Sensor tasks for data arrival, transformation steps with
> upstream dependencies, load tasks with idempotency checks to prevent duplicate writes."

---

### "Docker / CI/CD?"
> "Yes. Containerized Python ETL workloads on ECS at Citi — Docker for packaging,
> ECS for scaling. Git-based CI/CD with feature branches, PR-required code review,
> and automated testing on every push."

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## What Codie Will NOT Ask (Save For Technical Screen)

- Actual Python code or algorithms
- SQL query writing
- Deep Airflow internals
- Kafka / streaming architecture
- System design deep dives

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Questions To Ask Codie

1. "What does the interview process look like after this call?"
2. "What does the team structure look like for the Lead Python Developer role?"
3. "Is this a new headcount or a backfill?"
4. "What's the biggest platform challenge the Enterprise Platforms team is tackling right now?"
5. "Is the role hybrid or fully on-site in Plano?"

**Top 2 if time is short:**
1. "What does the interview process look like after this call?"
2. "What does the team structure look like for the Lead Python Developer role?"

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Logistics Checklist

- [ ] Phone charged, quiet room ready at 12:50 PM
- [ ] They call you at 214-315-2190
- [ ] Have this doc open on second screen
- [ ] Key numbers: 20+ years, 8 years Citi, 6,000+ endpoints, 10 days → 2 days, $185K
- [ ] Key phrase: *"reusable frameworks that other teams build on top of"*
- [ ] Key word: **Kaizen** — use it naturally in "Why Toyota"
- [ ] Salary: $185,000 — single number, no range

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## After The Call

If it goes well, Codie schedules you with hiring manager or technical screen.
Typical Toyota loop: Recruiter → Technical screen → Hiring manager → Panel

After the call — update `data/applied_jobs/00039_76829368/metadata.yaml` status to `INTERVIEW`.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

## Technical Screen Prep — Full Gap Coverage

Sections marked **[NOTE TO SELF — DRILL BEFORE TECHNICAL SCREEN]** need live practice before the next round.
Sections marked **[PULLED FROM CAPITAL ONE PLAYBOOK]** are already battle-tested answers — just review.

---

### Python OOP & Framework Design

**What They Want:** Reusable Python frameworks, templates, libraries — not scripts.

> "My core approach is to design frameworks as composable layers.
> At Citi I built a reusable ETL framework with a clean ingestion interface —
> any new data source could be onboarded by implementing one interface,
> without touching the core pipeline. That's the Strategy pattern in practice:
> define the contract, let each implementation vary independently.
>
> For HorizonScale I used a generator-based pipeline architecture —
> each asset's time-series flows through the same processing stages independently,
> which gave me natural parallelism via multiprocessing.Pool and cut cycle
> time by 90%.
>
> The patterns I reach for most: Strategy for pluggable components,
> Factory for object creation without tight coupling, Pipeline for
> sequential data transformations. All implemented with Python dataclasses
> or Pydantic models at boundaries so data contracts are enforced at runtime."

```python
# Decorator pattern
def retry(times):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try: return fn(*args, **kwargs)
                except Exception: pass
        return wrapper
    return decorator

# Context manager
class DBConnection:
    def __enter__(self): self.conn = connect(); return self.conn
    def __exit__(self, *args): self.conn.close()

# Abstract base class (Strategy pattern)
from abc import ABC, abstractmethod
class Extractor(ABC):
    @abstractmethod
    def extract(self) -> pd.DataFrame: ...
```

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Apache Airflow — DAG Design

**What They Want:** Integrations with orchestration tools like Airflow or Prefect.

> "I used Airflow for orchestrating ETL pipelines at Citi — DAG design,
> task dependencies, retry logic, and scheduling. My DAGs were structured
> with sensor tasks for data arrival detection, followed by transformation
> tasks with upstream dependencies, then load tasks with idempotency checks
> to prevent duplicate writes.
>
> Key design principles: keep tasks atomic and idempotent, use XCom sparingly
> (pass file paths not data), parameterize DAGs with Jinja templating for
> reuse across environments, and use task groups for readability in complex DAGs."

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG('capacity_etl', start_date=datetime(2025,1,1), schedule_interval='@daily') as dag:
    extract = PythonOperator(task_id='extract', python_callable=run_extract)
    transform = PythonOperator(task_id='transform', python_callable=run_transform)
    load = PythonOperator(task_id='load', python_callable=run_load)
    extract >> transform >> load
```

**[NOTE TO SELF — DRILL BEFORE TECHNICAL SCREEN]**
- Prefect: Never used directly. Frame as: *"Haven't used Prefect in production but
  understand it's a Python-first modern alternative to Airflow — dynamic DAGs,
  built-in observability, no scheduler overhead. Would ramp quickly given my
  Airflow foundation."*

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### APIs & Microservices

**What They Want:** Proficiency in APIs, microservices architectures.

> "I've built API integrations throughout my career — at Citi I used REST APIs
> to pull telemetry from BMC TrueSight and CMDB systems into my Python pipelines.
> HorizonScale includes an API integration layer for pulling external data feeds.
>
> For microservices, at Citi I containerized Python ETL workloads on ECS —
> each workload independently deployable and scalable. That's the core
> microservices principle applied to data pipelines.
>
> For building APIs, my tool is FastAPI — typed with Pydantic models,
> async-ready, auto-generates OpenAPI docs."

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ForecastRequest(BaseModel):
    asset_id: str
    horizon_days: int = 180

@app.post("/forecast")
async def get_forecast(req: ForecastRequest) -> dict:
    result = run_forecast(req.asset_id, req.horizon_days)
    return {"asset_id": req.asset_id, "forecast": result}
```

**[NOTE TO SELF — DRILL BEFORE TECHNICAL SCREEN]**
- REST vs gRPC tradeoffs, API versioning strategy, rate limiting patterns.
- Mulesoft / Apigee: *"Enterprise API gateway tools — I've worked with the REST
  layer they manage but not configured the gateways themselves. Could ramp quickly."*

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Real-Time Streaming / Kafka

**[PULLED FROM CAPITAL ONE PLAYBOOK]**

> "Kafka is a strong platform for event-driven architectures and real-time
> data movement, especially in high-volume environments like banking.
> My deepest experience has been in batch and warehouse-focused data engineering,
> where I've built reliable production pipelines at scale.
>
> In recent months I've been actively studying Kafka concepts — topics,
> partitions, consumer groups, offset management, and delivery semantics
> (at-least-once vs exactly-once). I understand the architecture and
> can ramp quickly in production contexts."

**[NOTE TO SELF — DRILL BEFORE TECHNICAL SCREEN]**
- AWS Kinesis vs Kafka: Kinesis = AWS-managed, Kafka = open source / MSK on AWS.
- Key concepts cold: topic/partition/offset, consumer group, producer acks,
  at-least-once vs exactly-once, log compaction.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Data Validation Frameworks

**[PULLED FROM CAPITAL ONE PLAYBOOK]**

> "We treated data quality as code, not a manual afterthought. In Glue,
> we used Deequ to define schema checks, business-rule validation, and
> anomaly detection as versioned tests — similar to unit testing for data pipelines.
>
> For malformed records: dead-letter pattern — bad records tagged with reason
> codes and routed to quarantine S3 instead of failing the full pipeline.
>
> For alerting: CloudWatch + EventBridge + SNS when validation failures
> crossed a threshold — issues caught early, not discovered in reports."

**Toyota framing — self-service angle:**
> "The validation framework was reusable — any new data source plugged in
> by defining its own rule set. Platform teams shouldn't rebuild validation
> logic per pipeline."

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Logging, Testing, Security & Instrumentation

**Logging:**
> "Structured JSON logging via Python's logging module — queryable in
> CloudWatch Log Insights. Log levels enforced: DEBUG for pipeline internals,
> INFO for stage completion, WARNING for data anomalies, ERROR for failures.
> Correlation IDs on every record so you can trace a single run across tasks."

**Testing:**
> "pytest for unit testing pipeline logic — mock external calls (S3, DB),
> test transformation functions with known inputs/outputs. Integration tests
> against real infrastructure in dev. Coverage target: 80%+ on core logic."

**Security:**
> "IAM least-privilege for all AWS resources — role-per-service, secrets
> in AWS Secrets Manager, never in code. At G6 Hospitality I implemented
> TLS 1.2 during a Dynatrace upgrade — security as part of deployment."

**Instrumentation:**
> "CloudWatch metrics + dashboards for pipeline health: records processed,
> error rates, job duration. Custom metrics via boto3 PutMetricData.
> HorizonScale Streamlit dashboard gave real-time pipeline observability
> alongside forecast results."

**[NOTE TO SELF — DRILL BEFORE TECHNICAL SCREEN]**
- OpenTelemetry: traces, metrics, logs as three pillars — know the concept.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Docker & CI/CD

> "At Citi I containerized Python ETL workloads on ECS using Docker —
> each pipeline packaged with its dependencies as a Fargate task.
> Environment parity guaranteed: dev, staging, and prod ran identical containers.
>
> CI/CD: Git feature branches, PR-required code review, automated test runs
> on push. Deployment pipelines trigger container builds, push to ECR,
> update ECS task definitions. Infrastructure as Code via CloudFormation
> to prevent environment drift."

**[NOTE TO SELF — DRILL BEFORE TECHNICAL SCREEN]**
- GitHub Actions vs AWS CodePipeline — know both at concept level.
- Kubernetes: *"ECS at Citi — understand K8s concepts (pods, deployments,
  services) and could ramp given the ECS foundation."*

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### SQL & NoSQL Databases

**SQL — strong. Key concepts cold:**
- Window functions: ROW_NUMBER, RANK, LAG/LEAD, PARTITION BY
- CTEs vs subqueries — readability vs optimizer behavior
- Indexing: clustered vs non-clustered, covering indexes
- Query plan: EXPLAIN, statistics, cardinality estimation
- Oracle: materialized CTEs, histogram stats, RAC

**[NOTE TO SELF — DRILL BEFORE TECHNICAL SCREEN — NoSQL Gap]**
- Direct NoSQL experience is thin. Honest framing:
  > *"Production depth is relational — Oracle, Redshift. I understand NoSQL
  > modeling principles: document stores (MongoDB) for flexible schema,
  > key-value (DynamoDB/Redis) for low-latency lookups, columnar (Cassandra)
  > for time-series at scale. I'd apply the right store for the workload."*
- Study: DynamoDB partition key design, MongoDB document modeling, Redis use cases.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Version Control — Branching & Code Reviews

> "Git-based workflow: feature branches off main, PRs required before merge,
> no direct commits to main. Branch naming: feature/, fix/, chore/.
>
> Code reviews: correctness first, then edge cases, then readability.
> Comments as questions — 'have you considered X?' not 'do X.'
>
> At Citi I established code review standards for the capacity team:
> minimum one approval, CI must pass, no unresolved comments. Onboarding
> time dropped because new engineers had clear patterns to follow."

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Mentoring Engineers

> "At Citi I built documentation standards, code review practices, and
> onboarding templates so new engineers could contribute without depending
> on me. Goal: make myself replaceable on the details so I could focus
> on harder problems. Team became self-sufficient. Onboarding time cut significantly."

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Hiring & Talent Attraction

**[NOTE TO SELF — BUILD THIS STORY BEFORE TECHNICAL SCREEN]**
- No direct full-cycle recruiting ownership.
- Honest frame: *"I've participated in technical screens, defined the bar for
  what 'strong' looks like on a Python data engineering team, and contributed
  to onboarding that retained engineers. Full hiring ownership is a growth
  area I'm ready to step into at Lead level."*
- Prep: one specific example where you influenced a hiring decision or defined technical bar.

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Self-Service Tools & Frameworks

**This is a strength — use it proactively:**
> "HorizonScale's Streamlit dashboard is exactly this — capacity analysts
> explore forecasts, filter by resource class, drill into at-risk assets
> without touching any code. Engineer builds it once, ten people use it independently.
>
> Same philosophy in the ETL framework at Citi — onboarding a new data source
> required filling in a config file, not touching core pipeline logic.
> Self-service by design."

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Why Toyota Specifically — Company Research

From `data/applied_jobs/00039_76829368/research/company_research.yaml`:
- Toyota Motor North America HQ in **Plano, TX** — local, no relocation friction
- **Toyota Way:** Kaizen (continuous improvement) + respect for people — use it naturally
- TFS is the finance/insurance arm — financial-scale volume, compliance, real customer impact
- Toyota invests heavily in AI, electrification, autonomous driving — forward-looking culture
- Hybrid work model for many corporate/tech roles — confirm on-site expectations with Codie

[↑ Back to top](#toyota-financial-services--lead-python-developer)

---

### Job Requirements Coverage Checklist

| Requirement | Section | Status |
|-------------|---------|--------|
| Reusable Python frameworks | Story 1, Story 2, Python OOP | ✓ Ready |
| ETL/ELT pipelines | Story 1, AWS story | ✓ Ready |
| SQL databases | SQL section | ✓ Ready |
| AWS cloud platform | Story 3 | ✓ Ready |
| Apache Airflow | Airflow section | ✓ Ready |
| Docker / CI-CD | Docker section | ✓ Ready |
| APIs & microservices | APIs section | ✓ Ready |
| Data validation frameworks | Validation section | ✓ Ready |
| Logging / testing / security / instrumentation | Dedicated section | ✓ Ready |
| Version control / code reviews | Version control section | ✓ Ready |
| Mentoring engineers | Story 4 | ✓ Ready |
| Real-time streaming / Kafka | Streaming section | ⚠ Honest framing only |
| NoSQL databases | SQL/NoSQL section | ⚠ Drill before tech screen |
| Prefect | Airflow section | ⚠ Honest framing — research before tech screen |
| Hiring / talent attraction | Hiring section | ⚠ Build story before tech screen |
| Kafka / Kinesis (preferred) | Streaming section | ⚠ Honest framing only |
| Mulesoft / Apigee (preferred) | APIs section | ⚠ Honest framing only |
| Self-service tools (preferred) | Self-service section | ✓ HorizonScale + Streamlit |

[↑ Back to top](#toyota-financial-services--lead-python-developer)
