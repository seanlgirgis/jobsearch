# One-Page Execution Board — Toyota First
**Date:** April 24, 2026  
**Primary Goal:** Win Toyota technical interview (Req 10301655)  
**Secondary Goal:** Stay ready for Capital One coding outcome/next step

---

## Priority Stack

| Priority | Track | Focus | Mission |
|---|---|---:|---|
| 1 | **Toyota** | **70%** | Present as platform architect: design, tradeoffs, scale, delivery |
| 2 | **Capital One** | **20%** | Strengthen shared technical depth: data engineering, SQL, platform reliability |
| 3 | **Extras** | **10%** | Keep reusable interview assets ready for opportunistic calls |

---

## Toyota Roadmap (In Exact Order)

| Order | Topic | Must Own |
|---|---|---|
| 1 | Architectural Thinking Framework | requirements -> components -> tradeoffs -> decision -> 10x scale plan |
| 2 | End-to-End System Design | source -> ingest -> process -> store -> API -> consumer |
| 3 | API Design + Scaling | REST correctness, latency bottlenecks, queue-offload, caching, rate limits |
| 4 | Docker + ECS/Fargate | container lifecycle, task/service scaling, deploy reliability |
| 5 | CI/CD Design | build/test/deploy gates, rollback strategy, zero-downtime release |
| 6 | AWS Deep Dive | S3, Glue, Redshift, SQS, CloudWatch, IAM decision rationale |
| 7 | CloudFormation | stack design, change sets, safe update strategy |
| 8 | Terraform Framing | honest gap + fast-ramp narrative (tool gap, not architecture gap) |
| 9 | Testing Strategy | unit/integration/contract pyramid with production gate logic |
| 10 | Observability | metrics/logs/traces, alarms, bottleneck detection loop |

---

## Capital One Secondary Plan (Technical Depth Only)

| Order | Topic | Must Own |
|---|---|---|
| 1 | Data Engineering Architecture | ingestion -> transform -> storage -> serving, with reliability controls |
| 2 | SQL Depth | joins, window functions, CTEs, optimization, indexing, explain-plan mindset |
| 3 | Python for Data Platforms | modular pipelines, testing, error handling, orchestration patterns |
| 4 | Cloud Platform Decisions | AWS service choice tradeoffs (S3/Glue/Redshift/SQS/Lambda/ECS) |
| 5 | Observability + Data Quality | metrics/logs/alerts, data validation, dead-letter and replay strategy |

---

## Weekly Checkboxes

### Toyota (Primary)
- [ ] Run 2 architecture whiteboard drills (10-minute each, spoken)
- [ ] Run 2 end-to-end system design drills (API + data pipeline)
- [ ] Rehearse 4 core stories in architect framing
- [ ] Review AWS decision tradeoffs doc once end-to-end
- [ ] Practice Terraform gap answer 3 times (confident, brief)

### Capital One (Secondary)
- [ ] Run 2 technical walkthroughs (data pipeline + API/data-serving design)
- [ ] Complete 2 SQL drills (windowing + optimization-focused)
- [ ] Rehearse platform tradeoff answers (service choice + scaling + reliability)

### Extras
- [ ] Keep one polished salary/start-date/authorization script handy
- [ ] Keep one cross-company intro script updated

---

## Anchor Script (Use In Every Technical Round)

> "My approach is requirements first, then architecture, then implementation.  
> I make decisions based on tradeoffs and scale constraints, not convenience."
