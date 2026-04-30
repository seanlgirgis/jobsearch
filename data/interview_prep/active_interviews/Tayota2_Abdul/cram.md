# Cram Sheet — Abdul Interview Answers
<a id="toc"></a>
## Table of Contents
2. [Q: Tell me about yourself](#sec-2)
3. [Q: Why Toyota specifically?](#sec-3)
4. [Q: Walk me through your most complex data platform design](#sec-4)
5. [Q: How do you handle pipeline failures at scale?](#sec-5)
6. [Q: Tell me about a time a system failed](#sec-6)
7. [Q: Tell me about the G6 Dynatrace project](#sec-7)
8. [Q: CloudFormation — how would you structure stacks for a data platform?](#sec-8)
9. [Q: Tell me about the HorizonScale forecasting platform](#sec-9)
10. [Q: FastAPI — how do you secure and scale a data API?](#sec-10)
11. [Q: Tell me about a time you convinced someone to change direction](#sec-11)
12. [Q: Terraform — how familiar are you?](#sec-12)
13. [Q: What questions do you have for me?](#sec-13)
14. [Q: What is the Medallion Architecture?](#sec-14)
15. [Q: Batch vs Streaming — how do you decide?](#sec-15)
16. [Q: Why never run analytics on an OLTP database?](#sec-16)
17. [Q: ECS Fargate or Lambda for FastAPI?](#sec-17)
18. [Q: What is idempotency and why does it matter?](#sec-18)
19. [Q: What is schema drift and why is it dangerous?](#sec-19)
20. [Q: What is a Docker image vs a Docker container?](#sec-20)
21. [Q: What triggers CI and what triggers CD?](#sec-21)
22. [Q: Kafka vs SQS — what is the difference?](#sec-22)
23. [Q: What is the 5-step design framework?](#sec-23)
24. [Q: What is a JWT and what must you validate?](#sec-24)
25. [Q: What is Kaizen and Genchi Genbutsu?](#sec-25)
26. [Q: Why should we hire Sean Girgis?](#sec-26)
27. [The Three Sean Principles](#sec-27)
28. [Key One-Liners to Memorize](#sec-28)

<a id="sec-2"></a>
## Q: Tell me about yourself

I am Sean Girgis — Lead Software Engineer with 12 years in Python, data engineering, and cloud-native automation.

At Citi I converted a 10-day manual Excel process into an auditable ETL pipeline that ran in 2 hours — idempotent, documented, better reports. I also built an ML forecasting pipeline that evolved from Pandas to PySpark to AWS — producing 180-day forecasts in a fraction of the time, giving the business actionable capacity decisions.

At G6 Hospitality I mined Dynatrace telemetry and created a data pipeline that gave ops a single pane of glass to understand real Brand.com performance — unmasking underserved customers whose issues were hidden by good averages. Ops introduced targeted solutions that improved conversion rate.

I am drawn to Toyota because reliability at scale is where I do my best work — and the Mobility for All mission is one I would be genuinely proud to be part of.

---


[Back to TOC](#toc)

<a id="sec-3"></a>
## Q: Why Toyota specifically?

I'm drawn to Toyota Financial Services because reliability at scale is exactly where I do my best work. Toyota's continuous improvement mindset — Kaizen — and Go see for yourself — Genchi Genbutsu — is exactly how I like to operate. And Toyota's Mobility for All mission resonates with me deeply. Enabling people to own vehicles they otherwise couldn't — that's where data reliability becomes a real-world equity story. That matters to me.

---


[Back to TOC](#toc)

<a id="sec-4"></a>
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


[Back to TOC](#toc)

<a id="sec-5"></a>
## Q: How do you handle pipeline failures at scale?

A reliable pipeline treats failure as a normal operating condition, not an exception.

First — design for failure from the start. At scale, failures will happen. I stage clear boundaries between pipeline layers so one failure doesn't cascade. Retries for transient errors with backoff. Dead Letter Queues for unrecoverable records — isolated, not lost, inspectable. Idempotent writes throughout so reprocessing never duplicates data.

Second — observability that tells you the truth. Structured logs, tracing, latency metrics, row-count anomalies, freshness checks. Alerts tied to business impact — not just job status. A green pipeline light is not enough. The data has to be correct.

Third — recovery has to be fast and consistent. Runbooks. Replay patterns from immutable Bronze. Partition-scoped backfills so you reprocess only what broke, not everything. Automated rollback where possible.

That combination — design for failure, prove correctness, recover fast — is what makes a pipeline trustworthy at scale.

---


[Back to TOC](#toc)

<a id="sec-6"></a>
## Q: Tell me about a time a system failed

At Citi, a monthly capacity run completed successfully — green status, no errors. But when I inspected the output statistics, the numbers were way off.

I traced the root cause quickly. Upstream had changed column coding and values in a source system — classic schema drift — which silently broke the joins. Records weren't failing, they were just matching wrong.

I confirmed the change was permanent, not an extraction error. Fixed the transformation logic, reran the pipeline, validated the results against known baselines. Then I added schema validation checks and alerts at the join stage so if column definitions change again, we catch it before we publish — not after.

The report was corrected in time. But the bigger result was the lesson: a pipeline that runs is not the same as a pipeline that's correct. Green status is not a data quality guarantee. You have to prove correctness, not assume it.

---


[Back to TOC](#toc)

<a id="sec-7"></a>
## Q: Tell me about the G6 Dynatrace project

G6's direct booking site and mobile app performance directly impacts conversion rates. Dynatrace gave good diagnosis at the transaction level but no total vision. The problem: good transactions and fast devices were masking the experience of users with low bandwidth, older devices, and different geographies. We were blind to where we were losing money.

I converted that problem into an opportunity. I mined the full transaction telemetry from Dynatrace, tagged data with geography, bandwidth, device family and model, and created running P95 averages — rejecting the favorable scenarios that were hiding the real picture.

This revealed weak paths we were losing revenue on. The result: the app and site were reworked with conditional loading based on the customer's actual situation. Service gaps were identified and addressed.

I converted Ops from a team chasing alerts into a team making decisions. From reactive to proactive. I treated Ops as the customer, not the endpoint.

---


[Back to TOC](#toc)

<a id="sec-8"></a>
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

[Back to TOC](#toc)


<a id="sec-9"></a>
## Q: Tell me about the HorizonScale forecasting platform

The business needed to act in advance, not react. Monthly telemetry reporting wasn't enough — they needed forward-looking forecasts that accounted for seasonality and periodic changes across tens of thousands of servers.

BMC TrueSight had a forecasting component but at that scale it was a dogfight for resources — grinding to a halt. We were essentially using OLTP for OLAP. The models were limited and forecast quality was poor.

I saw the opportunity. I proposed running an ML pipeline outside of TrueSight entirely.

Phase 1 — Pandas. We got results but it was slow and painful — days to process.
Phase 2 — PySpark on Hadoop. Faster, parallel, scalable.
Phase 3 — AWS. Full cloud-native data lake with distributed processing.

We modeled against Prophet, SARIMA, and XGBoost. Trained on 18 months of data, tested on 6. Competed models per series and selected the best fit automatically. Produced 6-month forecasts.

Result: customers received 3 months of high-confidence, actionable forecasts — understanding what the next 90 days would look like. Processing that once took days now ran in a fraction of the time.

The lesson: move the problem to the right platform. Don't fight the tool — replace it.

---


[Back to TOC](#toc)

<a id="sec-10"></a>
## Q: FastAPI — how do you secure and scale a data API?

Security is not a feature you add later — it's the first design decision.

Secure first: enforce authn/authz with JWT/OAuth2 — validate token signature, issuer, audience, expiry, and scopes. Role-based access control. Strict input validation with Pydantic. Parameterized queries. Secrets from a managed store, never in code. Rate limiting. TLS everywhere. Private networking. Full audit logging.

Scale second: keep endpoints stateless. Run multiple workers and replicas behind a load balancer. Tune DB connection pooling — size from DB capacity, not API optimism. Add caching for reads with proper TTL. Offload long jobs to async workers and queues. Health checks and autoscaling with upper limits. Observability — latency, error rate, saturation, P95.

---


[Back to TOC](#toc)

<a id="sec-11"></a>
## Q: Tell me about a time you convinced someone to change direction

The team was leaning toward hourly full reloads — simpler to build under deadline pressure. I could see that at forecasted data growth, it would become cost-prohibitive and operationally fragile.

Instead of arguing in the meeting, I built a cost and runtime projection — current table size, growth rate, hourly reload frequency — and showed what Q3 would look like in dollars and runtime. Numbers, not opinions.

I proposed incremental processing and offered to own the design so the added complexity was on me, not the team. No ego. Just: here's the data, here's the solution, I'll carry it.

The team agreed. Months later when volume grew significantly, the pipeline stayed stable and cost stayed controlled. The lesson: influence works best when you bring data, remove friction, and keep ego out of the room.

---


[Back to TOC](#toc)

<a id="sec-12"></a>
## Q: Terraform — how familiar are you?

I understand the model well — state file, provider ecosystem, plan/apply cycle, modules for reuse. My hands-on production work has been more in CloudFormation, but the concepts translate directly — IaC is IaC.

Where Terraform shines over CloudFormation is multi-provider shops. If you have AWS alongside Databricks, Snowflake, BigQuery, or an on-prem farm — Terraform manages all of it from one codebase. CloudFormation stops at the AWS boundary.

One hard rule I always enforce: never let two tools manage the same resource. If Terraform and CloudFormation both think they own a bucket policy, you've created a future incident.

I'm actively deepening my Terraform hands-on experience and would ramp quickly in a team that uses it.

---


[Back to TOC](#toc)

<a id="sec-13"></a>
## Q: What questions do you have for me?

1. What is the biggest data reliability or quality challenge the team is dealing with right now?
2. What would make someone in this role unusually successful — not just good, but exceptional?

---


[Back to TOC](#toc)

<a id="sec-14"></a>
## Q: What is the Medallion Architecture?

Bronze preserves truth. Silver creates trust. Gold serves consumers.

Bronze — data landed as-is, immutable raw source. Never modified. Enables idempotent reprocessing and full replay when needed.

Silver — clean it up, validate, normalize, join, deduplicate, mask PII. Queryable but not yet business-ready. Bad data stops here.

Gold — business-ready. Aggregated, business logic built in, optimized for analytics, executive dashboards, and ML consumption.

---


[Back to TOC](#toc)

<a id="sec-15"></a>
## Q: Batch vs Streaming — how do you decide?

Streaming sounds elegant but it's costly and not always needed. Use it only when latency must be in seconds — fraud detection, real-time tracking. When latency of 15 minutes or more is acceptable, batch is the right choice — easier to implement, cheaper to operate, and produces consistent results. Always justify streaming with a clear business latency requirement.

---


[Back to TOC](#toc)

<a id="sec-16"></a>
## Q: Why never run analytics on an OLTP database?

OLTP is optimized for low-latency transactions — fast row reads and writes for live business operations. Analytics runs massive scans across huge datasets. Run both together and you get contention — analytics grinds OLTP to a halt, live transactions slow down, production suffers. You separate them for workload isolation. OLAP systems — Snowflake, Redshift, Athena — are columnar, partitioned, and built for analytical scans. Let each system do what it's designed for.

---


[Back to TOC](#toc)

<a id="sec-17"></a>
## Q: ECS Fargate or Lambda for FastAPI?

ECS Fargate is my default for FastAPI in production. Containers stay warm, connection pools persist, VPC integration is clean for databases and private resources. Predictable and stable.

Lambda with Mangum works for low-traffic, bursty, or internal APIs where cold starts are acceptable. The danger with Lambda is relational databases — every invocation opens a new connection. At burst you get connection storms. If I use Lambda with a DB I put RDS Proxy in front.

The decision rule: steady production API with DB pools → ECS Fargate. Lightweight, bursty, event-driven → Lambda.

---

[Back to TOC](#toc)


<a id="sec-18"></a>
## Q: What is idempotency and why does it matter?

Idempotency means running the same operation multiple times produces the same result as running it once. In pipelines this is critical because failures and retries are normal operating conditions. If your writes aren't idempotent, every retry is a corruption risk. Bronze being immutable is the foundation — you always have a safe source to replay from.

---
[Back to TOC](#toc)



<a id="sec-19"></a>
## Q: What is schema drift and why is it dangerous?

Data schema drift is when an upstream source quietly changes its structure — renaming a field, changing a type, dropping a column. The pipeline keeps running. Often it comes out green. But the data is wrong. Green pipeline, broken output.

To address it: schema validation at ingestion — use Pydantic contracts — rather break than false success. Send drifted records to DLQ, never let them silently reach Gold. Add drift detection alerts and audit trails. Set measurable KPI thresholds on output quality and alert on variances. Define acceptance levels for data output so you know when something crossed a line.

The rule: a pipeline that runs is not the same as a pipeline that's correct.

---

[Back to TOC](#toc)


<a id="sec-20"></a>
## Q: What is a Docker image vs a Docker container?

Image is the blueprint. Container is the running instance — live, isolated, ephemeral.

---


[Back to TOC](#toc)

<a id="sec-21"></a>
## Q: What triggers CI and what triggers CD?

CI fires when a PR is opened — runs tests, lint, security scan. CD fires when the PR is merged to main — builds the image, tags with commit SHA, pushes to ECR, deploys to ECS. The merge IS the deployment trigger.

---


[Back to TOC](#toc)

<a id="sec-22"></a>
## Q: Kafka vs SQS — what is the difference?

Kafka is a distributed event streaming platform. Messages are written to a log, retained with an expiry, and multiple independent consumer groups can read the same message at their own pace. Built for replay, fan-out, and event history.

SQS is a managed message queue — simpler, serverless. Message is consumed once and deleted. One consumer per message. No replay.

Use SQS for simple task queues. Use Kafka when you need event history, replay, or multiple consumers reading the same stream independently.

---


[Back to TOC](#toc)

<a id="sec-23"></a>
## Q: What is the 5-step design framework?

1. Clarify requirements first — latency, scale, retention, consumers, recovery SLA, compliance
2. State the architecture — ingestion → raw → validate → transform → serve
3. Name the tradeoffs — why batch vs streaming, why this tool vs that tool
4. Explain failure modes — DLQ, idempotency, replay, checkpointing, watermarks
5. Close with observability — freshness checks, schema drift alerts, lineage, SLA monitoring

Never draw a happy-path-only system. Interviewers listen for what breaks and how you recover.

---


[Back to TOC](#toc)

<a id="sec-24"></a>
## Q: What is a JWT and what must you validate?

JWT is a signed self-contained token carrying identity and claims — subject, issuer, audience, scopes, expiry. Anyone can decode it. That is not security.

You must validate: signature — was it signed by the right party, expiry — is it still valid, issuer — did the right authority issue it, audience — was it intended for your service.

Decoding is free. Validation is what counts. Decode plus trust is not authentication. Decode plus validate is.

---


[Back to TOC](#toc)

<a id="sec-25"></a>
## Q: What is Kaizen and Genchi Genbutsu?

Kaizen is how I think about everything — continuous improvement. It is never good enough, there is always an opportunity. I apply it professionally and personally — always asking what can be better, what is worth knowing more deeply.

Genchi Genbutsu is about reality. Never about who says what or first impressions. Go investigate. See for yourself. Test the assumptions and theories. Arrive at the real root cause. It is a must for senior engineers and managers — never manage from the high tower. Foot on the ground, see for yourself, then decide.

---


[Back to TOC](#toc)

<a id="sec-26"></a>
## Q: Why should we hire Sean Girgis?

I'm fight-tested. Twelve years in enterprise environments — Citi, G6, HorizonScale — I've seen systems fail, rebuilt them, and made them better. I don't just fit into teams, I lift them.

My values match Toyota's before I even knew the names for them. Kaizen — I've always operated that way. Genchi Genbutsu — boots on the ground, root cause first, no assumptions.

What you get with me is someone who will not just perform the role but will own the outcomes. Team success and company mission above everything. And Toyota's mission — Mobility for All — is one I'm genuinely proud to fight for.

---


[Back to TOC](#toc)

<a id="sec-27"></a>
## The Three Sean Principles

> **"Architecture is about tradeoffs, not tools."**
> Use when choosing any technology. Never say "I use X." Say "I chose X because of this tradeoff."

> **"Design for breakage and failure — it's about when, not if."**
> Use in any system or pipeline design. Show you think beyond the happy path.

> **"Bronze preserves truth. Silver creates trust. Gold serves consumers."**
> Use for any medallion architecture question. One sentence that says everything.

---

[Back to TOC](#toc)


<a id="sec-28"></a>
## Key One-Liners to Memorize

- "Architecture is tradeoffs, not tools."
- "Design for breakage — it's when, not if."
- "Bronze preserves truth. Silver creates trust. Gold serves consumers."
- "You can redeploy code. You cannot un-delete data."
- "Green pipelines don't guarantee correct data."
- "I treated ops as the customer, not the endpoint."
- "The merge IS the deployment trigger."
- "I stay current by building."
- "Rather break than false success."
- "Same input, same output, always — that's idempotency."

[Back to TOC](#toc)

