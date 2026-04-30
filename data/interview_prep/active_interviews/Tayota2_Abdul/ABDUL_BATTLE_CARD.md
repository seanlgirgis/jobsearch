# Abdul Jaleel Dudekula — HM Interview Battle Card
**Thursday April 30, 2026 | 11:00–11:45 AM CT | Microsoft Teams**
Meeting ID: 244798544632556 | Passcode: sU6yz9z7

---

## THE THREE MANTRAS (say these, mean them)

> **"Architecture is tradeoffs, not tools."**
> **"Design for breakage — it's when, not if."**
> **"Bronze preserves truth. Silver creates trust. Gold serves consumers."**

---

## THE 5-STEP DESIGN ANSWER (use every time Abdul asks "how would you design...")

1. **Clarify requirements first** — latency, scale, retention, consumers, recovery SLA, compliance
2. **State the architecture** — ingestion → raw → validate → transform → serve
3. **Name the tradeoffs** — why batch vs streaming, why this tool vs that tool
4. **Explain failure modes** — DLQ, idempotency, replay, checkpointing, watermarks
5. **Close with observability** — freshness checks, schema drift alerts, lineage, SLA monitoring

> Never draw a happy-path-only system. Interviewers listen for what breaks and how you recover.

---

## SENIOR vs JUNIOR TEST

| Junior Answer | Senior Answer |
|---|---|
| Lists tools | Explains tradeoffs |
| Describes the happy path | Explains failure modes |
| Talks about what it does | Talks about cost, governance, operational ownership |
| Picks a tool | Justifies the choice vs alternatives |

Abdul will notice the difference immediately.

---

## TOPIC CHEAT SHEETS

### SYSTEM DESIGN
- Requirements first — throughput, latency, regions, retention, recovery SLA, consumers
- Architecture patterns: **Warehouse** (SQL/governance) → **Lake** (flexible/cheap) → **Lakehouse** (ACID + open storage)
- Batch = simpler, cheaper, easier to debug | Streaming = low latency but complex
- Lambda = batch + speed layers (accuracy + latency; but duplicate logic)
- Kappa = streaming only + Kafka replay (simpler; streaming dependency)
- **Key gotcha:** Large systems fail in small hidden ways before they fail visibly

### DATA ARCHITECTURE
- OLTP = operational live transactions (PostgreSQL, DynamoDB) | OLAP = analytics (Snowflake, Redshift)
- Never run analytics directly on OLTP — contention, slow prod workloads, workload isolation
- **Medallion:** Bronze (immutable raw, replay source) → Silver (validate, dedupe, PII mask, trust boundary) → Gold (curated BI, KPIs, ML features)
- Star Schema = fact table + flat dimensions, simple joins, analytics-optimized
- Snowflake Schema = normalized dimensions, less redundancy, more joins
- **Grain** = what one fact row represents. Unclear grain = duplicated metrics
- Governance: lineage, data contracts, ownership, audit trails, discoverability
- PII: masked at Silver, never exposed in Gold
- Performance: Parquet (columnar pruning), partitioning (scan reduction), compaction (small-file fix), materialized views (repeated aggregations)

### PIPELINE DESIGN
- Requirements drive architecture: fraud detection = streaming (seconds) | finance reporting = batch (daily)
- Source patterns & risks:
  - CDC = incremental OLTP changes | **Risk:** schema drift, duplicate events
  - APIs = SaaS/vendor data | **Risk:** rate limits, pagination, auth expiration
  - Files = batch exports | **Risk:** partial uploads, corrupted files, duplicates
  - Event Streams = low-latency | **Risk:** consumer lag, ordering, replay complexity
- **Schema drift** = silent pipeline killer — source changes columns, pipeline keeps running, output is wrong
  - Mitigation: schema validation at ingestion, schema registry, alerts on change, DLQ for invalid records
- Reliability checklist: immutable Bronze, idempotent writes, limited retries with backoff, DLQ, versioned logic, partition-scoped backfills, watermarks for late events
- **Performance is architectural, not cleanup:** partitioning, incremental (not full reload), compaction, shuffle reduction, storage tiering (hot→warm→cold→archive)

### FASTAPI
- **What it is:** Contract-first Python API layer — typed inputs, typed outputs, auto-generated OpenAPI docs, container-native deployment
- **What it's NOT:** A data processing engine. Heavy ETL, Spark jobs, model training belong in proper backend systems
- ASGI → Uvicorn → (Gunicorn for multi-worker) — handles concurrent I/O-heavy requests
- `async def` = use only when full call chain is async-compatible. Blocking libs inside async = frozen event loop
- `def` = fine for blocking SDKs, CPU-light endpoints
- **Pydantic models:** Request = reject bad input at boundary | Response = control output shape, prevent field leakage
- **Depends:** dependency injection for auth, DB sessions, config, service classes — keeps routes thin and testable
- **DB connections:** pool_size from DB capacity, not API optimism. More workers = more connections. PgBouncer or RDS Proxy at scale
- **Never expose arbitrary SQL** — SQL injection + no authorization + unbounded warehouse scans = liability
- **BackgroundTasks** = lightweight fire-and-forget (audit writes, notifications). For durable work: SQS, Step Functions, ECS Task, Airflow
- **JWT validation:** decode is NOT authentication — must verify signature, issuer, audience, expiry, scopes. Timed cache for IdP calls
- **OpenAPI:** auto-generated from routes + Pydantic. Treat schema as a published artifact — if it changes, the contract changed
- **ECS Fargate** = steady APIs, DB pools, VPC-heavy → **Lambda + Mangum** = low-traffic, bursty, internal tools (watch: connection storms with RDS)

---

## THREE FLAGSHIP STORIES (architect framing)

### Story 1 — HorizonScale: Scale Under Constraints
**Situation:** tens of thousands of servers, 4 KPIs, 65,000+ metrics, needed 180-day forecasts for capacity planning  
**Task:** Build a forecasting platform that could handle the scale without burying engineers in manual model work  
**Action:** Phase 1 = Apache stack (Spark + Airflow + MLflow); Phase 2 = moved to AWS (Glue + S3 + Athena + Spark). Ran a model tournament across Prophet, ARIMA, Holt-Winters — selected winner per series by error metric. Built Streamlit dashboard for consumption.  
**Result:** Reliable 180-day forecasts at scale. Enabled proactive capacity decisions.  
**Architecture angle:** "I didn't just build a model. I built a platform that could manage models — selection, training, serving, observability — at scale. The challenge was the operational layer, not the math."

### Story 2 — Citi Telemetry Pipeline: Production at Financial Scale
**Situation:** Real-time telemetry data flowing from financial infrastructure — needed to ingest, validate, and surface operational alerts  
**Task:** Build a reliable pipeline where data quality failures had business-critical consequences  
**Action:** Designed ingestion with schema validation and DLQ isolation, medallion-style processing, observability at every stage, SLA monitoring  
**Result:** Operational telemetry pipeline serving financial reporting with full replay capability  
**Architecture angle:** "In financial services, a green pipeline light is not enough. I built observability into the design — freshness checks, schema drift detection, audit trails — because the data had to be correct, not just present."

### Story 3 — G6/Dynatrace FAST Project: Observability-First Architecture
**Situation:** G6 Hospitality had a large application estate with no unified observability — blind spots across hotel tech systems  
**Task:** Architect an observability platform using Dynatrace to surface real operational signals  
**Action:** Deployed Dynatrace across the estate, combined real-user telemetry with synthetic monitoring, built FAST project dashboards, enabled SLA-level alerting  
**Result:** Reduced mean-time-to-detect for application issues. Gave operations teams the signal, not noise.  
**Architecture angle:** "This taught me that observability is an architectural decision, not a monitoring add-on. The difference is whether you design for visibility from the start or retrofit dashboards after the fact."

---

## GAP ANSWERS (Ramya flagged these — be honest, be crisp, move on)

### Terraform
> "I've designed infrastructure with CloudFormation and worked alongside Terraform-managed infrastructure in team settings. I understand the concepts — state management, provider model, plan/apply cycle — but I've done more hands-on work in CloudFormation. I'm actively closing that gap and it's on my active study list."
> 
> *Then pivot:* "What I do have is deep experience thinking about infrastructure as code as a design discipline — IaC for reproducibility, drift prevention, and deployment consistency."

### Testing
> "I write tests as part of delivery — unit tests for transformation logic, integration tests for pipeline stages, and I've used TestClient for FastAPI validation. Where I'm actively growing is systematic test coverage discipline — TDD-first approach and broader contract testing. I treat tests as the first consumer of my design."

### CloudFormation (Abdul's likely focus — lean in)
> "CloudFormation is where I'm comfortable. I've used it for defining stacks — ECS task definitions, IAM roles, VPC resources, S3 configurations. The mental model I carry: a stack is a unit of deployment, not a unit of code. You organize stacks around lifecycle boundaries, not resource types."

---

## QUESTIONS TO ASK ABDUL (pick 2-3)

1. "What does the current data platform architecture look like, and where is the team focused on evolving it?"
2. "What's the biggest reliability or quality challenge the team is working through right now?"
3. "How does the team think about the boundary between data engineering and DevOps here — is that a shared ownership model or separate teams?"
4. "What does a strong first 90 days look like for someone stepping into this Lead role?"
5. "What's the tech stack on the API and microservices side — FastAPI, or something else?"

---

## DAY-OF CHECKLIST

- [ ] Teams link ready, tested the night before
- [ ] Meeting ID: 244798544632556 | Passcode: sU6yz9z7
- [ ] Camera on, background clean, lighting good
- [ ] This battle card open on second screen or printed
- [ ] Water within reach
- [ ] Deep breath before joining — you've done the work

**Opening line when Abdul asks "tell me about yourself":**
> "I'm a Lead Software Engineer with about 12 years of experience, focused on Python, API microservices, and data platform engineering. The thread across my work has been building systems that are reliable under failure — not just on the happy path. Most recently at HorizonScale I architected a forecasting platform at the scale of tens of thousands of servers, and before that at Citi I built production telemetry pipelines for financial infrastructure. I'm drawn to this role because Toyota Financial Services is exactly the kind of environment where data reliability and operational trust matter at scale."

---

## WHAT RAMYA SIGNALED TO ABDUL

Ramya passed you through and flagged: **end-to-end architecture, DevOps, containerization, API scaling, CloudFormation, architectural decision-making.**

Abdul is going to probe **how you think**, not what tools you've touched. Lead with tradeoffs. Lead with failure modes. Lead with operational ownership.

**You are ready. Go get it.**
