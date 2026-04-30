# Cram Sheet — Abdul Interview Answers
**Retype each answer. That is the drill.**

---

## Q: Tell me about yourself

I'm Sean Girgis — Lead Software Engineer with about 12 years in Python, data platform engineering, and cloud-native automation. Most of my recent work has been at Citi, where I replaced a 10-day manual capacity process with a deterministic ETL pipeline that ran in under two hours — more reliable, fully auditable. I also built an ML forecasting platform on PySpark and AWS that delivered 180-day capacity forecasts across tens of thousands of servers. Before that at G6 Hospitality I built a Dynatrace telemetry pipeline that helped the team improve their Brand.com site performance — treated ops as the customer, not just the endpoint. More recently I built an AI RAG pipeline for my own job search — I stay current by building.

I'm drawn to Toyota Financial Services because reliability at scale in financial services is exactly where I do my best work — and the Mobility for All mission is something I genuinely believe in.

---

## Q: Why Toyota specifically?

I'm drawn to Toyota Financial Services because reliability at scale is exactly where I do my best work. Toyota's continuous improvement mindset — Kaizen — and Go see for yourself — Genchi Genbutsu — is exactly how I like to operate. And Toyota's Mobility for All mission resonates with me deeply. Enabling people to own vehicles they otherwise couldn't — that's where data reliability becomes a real-world equity story. That matters to me.

---

## Q: Walk me through your most complex data platform design

Citi High-Scale Telemetry Pipeline. When I joined, the team was processing tens of thousands of telemetry records monthly — joining to CMDB and AppDynamics data — entirely in Excel. It took 10 days and many people. Everyone accepted it as status quo.

I proposed and built a 5-step pipeline:
A — Ingested and validated data from TrueSight (Oracle), CMDB (SQL Server), and AppDynamics
B — Normalized identifiers to canonical hostnames so datasets could be reliably joined
C — Joined and enriched telemetry with CMDB and AppDynamics data — flagged unmatched records instead of silently dropping them
D — Calculated P95 utilization, applied a 1.15 confidence factor, set ceiling at 90%, classified endpoint health
E — Loaded idempotently into monthly and master SQL databases — published Excel and Streamlit outputs

Result: 10 days down to under 2 hours. More reliable, fully auditable, provably correct.

The team went from trusting a spreadsheet nobody wanted to touch, to a pipeline that proved its own correctness on every run. That shift — from "it ran" to "it proved it was right" — that's what I care about.

---

## Q: How do you handle pipeline failures at scale?

A reliable pipeline treats failure as a normal operating condition, not an exception.

First — design for failure from the start. At scale, failures will happen. I stage clear boundaries between pipeline layers so one failure doesn't cascade. Retries for transient errors with backoff. Dead Letter Queues for unrecoverable records — isolated, not lost, inspectable. Idempotent writes throughout so reprocessing never duplicates data.

Second — observability that tells you the truth. Structured logs, tracing, latency metrics, row-count anomalies, freshness checks. Alerts tied to business impact — not just job status. A green pipeline light is not enough. The data has to be correct.

Third — recovery has to be fast and consistent. Runbooks. Replay patterns from immutable Bronze. Partition-scoped backfills so you reprocess only what broke, not everything. Automated rollback where possible.

That combination — design for failure, prove correctness, recover fast — is what makes a pipeline trustworthy at scale.

---

## Q: Tell me about a time a system failed

At Citi, a monthly capacity run completed successfully — green status, no errors. But when I inspected the output statistics, the numbers were way off.

I traced the root cause quickly. Upstream had changed column coding and values in a source system — classic schema drift — which silently broke the joins. Records weren't failing, they were just matching wrong.

I confirmed the change was permanent, not an extraction error. Fixed the transformation logic, reran the pipeline, validated the results against known baselines. Then I added schema validation checks and alerts at the join stage so if column definitions change again, we catch it before we publish — not after.

The report was corrected in time. But the bigger result was the lesson: a pipeline that runs is not the same as a pipeline that's correct. Green status is not a data quality guarantee. You have to prove correctness, not assume it.

---

## Q: CloudFormation — how would you structure stacks for a data platform?

Think modularly. Organize by ownership, lifecycle, and blast radius.

- Foundation — VPC, subnets, routes
- Security — IAM, KMS, security groups, permission boundaries
- Storage — S3, lake controls, data catalog
- Compute — Glue, Lambda, ECS/Fargate, EMR, Step Functions
- Observability — alarms, logs, dashboards
- Domain separation — Customers / Orders / Finance + Dev / Test / Prod

Keep stateful resources in their own stacks, separate from frequently changing application resources.

The rule: a failed pipeline deploy should never risk the network foundation. Stack boundaries are blast radius boundaries.

---

## Q: FastAPI — how do you secure and scale a data API?

Security is not a feature you add later — it's the first design decision.

Secure first: enforce authn/authz with JWT/OAuth2 — validate token signature, issuer, audience, expiry, and scopes. Role-based access control. Strict input validation with Pydantic. Parameterized queries. Secrets from a managed store, never in code. Rate limiting. TLS everywhere. Private networking. Full audit logging.

Scale second: keep endpoints stateless. Run multiple workers and replicas behind a load balancer. Tune DB connection pooling — size from DB capacity, not API optimism. Add caching for reads with proper TTL. Offload long jobs to async workers and queues. Health checks and autoscaling with upper limits. Observability — latency, error rate, saturation, P95.

---

## Q: Tell me about a time you convinced someone to change direction

The team was leaning toward hourly full reloads — simpler to build under deadline pressure. I could see that at forecasted data growth, it would become cost-prohibitive and operationally fragile.

Instead of arguing in the meeting, I built a cost and runtime projection — current table size, growth rate, hourly reload frequency — and showed what Q3 would look like in dollars and runtime. Numbers, not opinions.

I proposed incremental processing and offered to own the design so the added complexity was on me, not the team. No ego. Just: here's the data, here's the solution, I'll carry it.

The team agreed. Months later when volume grew significantly, the pipeline stayed stable and cost stayed controlled. The lesson: influence works best when you bring data, remove friction, and keep ego out of the room.

---

## Q: Terraform — how familiar are you?

I understand the model well — state file, provider ecosystem, plan/apply cycle, modules for reuse. My hands-on production work has been more in CloudFormation, but the concepts translate directly — IaC is IaC.

Where Terraform shines over CloudFormation is multi-provider shops. If you have AWS alongside Databricks, Snowflake, BigQuery, or an on-prem farm — Terraform manages all of it from one codebase. CloudFormation stops at the AWS boundary.

One hard rule I always enforce: never let two tools manage the same resource. If Terraform and CloudFormation both think they own a bucket policy, you've created a future incident.

I'm actively deepening my Terraform hands-on experience and would ramp quickly in a team that uses it.

---

## Q: What questions do you have for me?

1. What is the biggest data reliability or quality challenge the team is dealing with right now?
2. What would make someone in this role unusually successful — not just good, but exceptional?

---

## Key One-Liners to Memorize

- "Architecture is tradeoffs, not tools."
- "Design for breakage — it's when, not if."
- "Bronze preserves truth. Silver creates trust. Gold serves consumers."
- "You can redeploy code. You cannot un-delete data."
- "Green pipelines don't guarantee correct data."
- "I treated ops as the customer, not the endpoint."
- "The merge IS the deployment trigger."
- "I stay current by building."
