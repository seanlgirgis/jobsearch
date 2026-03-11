# Claude Training Session Prompts
*Copy-paste these into Claude.ai (web) to generate 1-2 hour training sessions.*
*Feed the output back here or to Antigravity for hands-on practice.*

Last updated: 2026-03-11

---

## How to Use This

1. Pick one topic below
2. Copy the prompt into Claude.ai web (claude.ai)
3. Read / study the output (30–45 min)
4. Come back here and paste it to Claude Code or Antigravity and say:
   **"Quiz me on this and simulate an interview on [topic]"**
5. Check off the topic when done

**Goal: one topic per day, ~2 hours total.**

---

## Monet Bank — Weak Points (Priority Order)

### 1. Databricks Platform
- [ ] Studied

**Prompt:**
```
I am a Senior Data Engineer with 20 years of experience in Python, PySpark, SQL,
AWS Glue/Athena, and Airflow. I have never used Databricks in production.
I have a job interview at a fintech bank that uses Databricks heavily.

Give me a focused 2-hour self-study session on Databricks that covers:
1. What Databricks is and how it differs from raw Spark / AWS Glue
2. The Databricks workspace: clusters, notebooks, jobs, repos
3. Delta Lake: ACID transactions, time travel, schema enforcement, Z-ordering, MERGE
4. Medallion Architecture: Bronze / Silver / Gold — what goes in each layer and why
5. Unity Catalog: what it replaces, how governance works, column-level security
6. Delta Live Tables (DLT): declarative pipelines, triggered vs continuous, quality checks
7. Databricks Workflows: job orchestration, task dependencies
8. 10 interview questions a fintech bank would ask about Databricks with strong answers

Format it as a structured tutorial with code examples in PySpark/SQL where relevant.
Bridge every concept back to AWS Glue or plain PySpark so I can anchor it to what I know.
End with a cheat sheet summary I can review in 5 minutes before the interview.
```

---

### 2. Delta Lake Deep Dive
- [ ] Studied

**Prompt:**
```
I am a Senior Data Engineer familiar with Parquet and S3-based data lakes (AWS Glue/Athena).
I need a deep-dive training session on Delta Lake for a fintech bank interview.

Cover:
1. The Delta transaction log (_delta_log) — how it works, JSON entries, checkpoints
2. ACID guarantees on a data lake — how Delta achieves atomicity and isolation
3. Time travel — VERSION AS OF, TIMESTAMP AS OF, RESTORE, retention policies
4. Schema enforcement vs schema evolution — mergeSchema, ALTER TABLE
5. OPTIMIZE and Z-Ordering — when and why to use it, how data skipping works
6. MERGE / upsert — CDC patterns, SCD Type 1 and Type 2 with Delta
7. Vacuum — what it does, why retention matters, risks of running it too early
8. Delta vs Parquet vs Iceberg — when would you choose each
9. 10 interview Q&A specifically about Delta Lake in a regulated financial environment

Use SQL and PySpark examples. Relate everything to my Parquet/S3 background.
End with a one-page cheat sheet.
```

---

### 3. Apache Spark Performance Tuning
- [ ] Studied

**Prompt:**
```
I am a Senior Data Engineer with 6 years of PySpark experience on telemetry pipelines
(AWS Glue). I need a focused session on Spark performance tuning for a senior interview.

Cover:
1. Spark execution model: jobs, stages, tasks, shuffles — what causes slowness
2. Partitioning: repartition vs coalesce, partition by key, skew handling
3. Shuffles: what triggers them, how to minimize (broadcast joins, bucketing)
4. Caching and persistence: when to cache, storage levels, when NOT to cache
5. Broadcast joins vs sort-merge joins — when to use each and why
6. Skew handling: salting, AQE (Adaptive Query Execution), skew hints
7. Small file problem — causes, detection, solutions (OPTIMIZE, coalesce)
8. Reading/writing optimization: partition pruning, predicate pushdown, columnar formats
9. Databricks-specific: AQE settings, photon engine, cluster sizing
10. 10 interview Q&A on Spark performance at scale

Use PySpark code examples. Flag which concepts are Databricks-specific vs vanilla Spark.
End with a cheat sheet of the top 10 performance levers.
```

---

### 4. dbt (Data Build Tool)
- [ ] Studied

**Prompt:**
```
I am a Senior Data Engineer who has never used dbt in production but builds SQL
transformation pipelines manually with Python and SQL. I have a job interview where
dbt is listed as a preferred skill.

Give me a 2-hour crash course on dbt covering:
1. What dbt does and where it fits in the modern data stack
2. dbt models: .sql files, SELECT-only pattern, how dbt wraps them in CREATE TABLE/VIEW
3. The ref() function: dependency resolution, DAG building
4. Materializations: table, view, incremental, ephemeral — when to use each
5. Sources and staging: how to define raw sources, freshness checks
6. Tests: built-in tests (unique, not_null, accepted_values, relationships) and custom tests
7. Macros and Jinja templating in dbt
8. dbt docs and lineage: auto-generated documentation
9. dbt Cloud vs dbt Core vs dbt on Databricks
10. 10 interview questions with answers — including "you haven't used dbt in production"

Give me real SQL/YAML examples. Show how dbt compares to what I do manually today.
End with an honest talking-point script for the interview about my dbt knowledge level.
```

---

### 5. Medallion Architecture & Data Modeling
- [ ] Studied

**Prompt:**
```
I am a Senior Data Engineer with strong ETL and dimensional modeling experience.
I need a focused training session on Medallion Architecture and modern data modeling
for a Databricks/fintech interview.

Cover:
1. Medallion Architecture: Bronze/Silver/Gold — rules for each layer, what belongs where
2. When to write to Bronze vs transform immediately — ingestion patterns
3. Silver layer design: cleaning, deduplication, standardization, joins
4. Gold layer: aggregations, business metrics, serving patterns for analysts
5. Dimensional modeling refresher: star schema, fact tables, dimension tables
6. SCD Types 1, 2, 3 — implementation in Spark/Delta Lake
7. Data Vault 2.0 basics — hubs, links, satellites (interview awareness level)
8. Lakehouse vs Data Warehouse vs Data Lake — how to explain the difference
9. How medallion maps to dbt (staging → intermediate → mart layers)
10. 10 interview Q&A including "design a medallion architecture for a payment processing system"

Use fintech/banking examples throughout — payments, transactions, ledgers.
End with a design cheat sheet I can sketch on a whiteboard.
```

---

### 6. Data Governance & Unity Catalog
- [ ] Studied

**Prompt:**
```
I am a Senior Data Engineer from a regulated banking environment (Citi).
I need a training session on modern data governance with a focus on Databricks Unity Catalog
for a fintech bank interview.

Cover:
1. Why data governance matters in financial services — compliance, audit, access control
2. Unity Catalog architecture: metastore, catalog, schema, table hierarchy
3. Unity Catalog vs old Hive metastore — what changed and why it matters
4. Access control in Unity Catalog: GRANT/REVOKE, groups, service principals
5. Column-level security and row-level filters — how to implement in UC
6. Data lineage in Unity Catalog — how it's tracked automatically
7. Data classification: PII, sensitive data tagging in Databricks
8. Comparing Unity Catalog to AWS Glue Data Catalog + Lake Formation
9. Audit logging — what gets logged, how to query audit logs
10. 10 interview Q&A on governance in a regulated environment

Relate UC concepts to my Citi experience with regulated data and access controls.
End with a cheat sheet comparing UC to what I already know from AWS.
```

---

### 7. Pipeline Reliability & Observability
- [ ] Studied

**Prompt:**
```
I am a Senior Data Engineer with strong experience in monitoring (Dynatrace, AppDynamics,
CA APM) and data pipelines (Airflow, AWS Glue). I need a training session on modern
data pipeline reliability and observability for a senior interview.

Cover:
1. What "production-grade" data pipelines means — SLAs, SLOs, error budgets
2. Monitoring vs observability — metrics, logs, traces for data pipelines
3. Airflow best practices: retries, SLAs, sensors, alerting on failure
4. Delta Live Tables quality constraints — expect, expect_or_drop, expect_or_fail
5. Data quality frameworks: Great Expectations, Soda, dbt tests — compare them
6. Incident response for data pipelines: runbooks, on-call, postmortems
7. Idempotency in pipelines — why it matters, how to design for it
8. Backfill patterns — full vs incremental backfill, handling late-arriving data
9. Databricks observability: cluster metrics, job run history, alerts
10. 10 interview Q&A on reliability including "tell me about a pipeline outage you handled"

Bridge my APM/monitoring background to modern data pipeline observability.
End with a cheat sheet of the top reliability patterns.
```

---

## Bonus: Mock Interview Session

After studying any topic above, use this prompt to simulate a real interview:

```
I just studied [TOPIC]. I am interviewing for a Senior Data Engineer role at a
fintech bank (Monet Bank) in Plano TX. They use Databricks, Apache Spark, Delta Lake,
and Airflow heavily. I have 20 years of experience but limited hands-on Databricks.

Act as a tough but fair technical interviewer. Ask me 8 interview questions on [TOPIC],
one at a time. Wait for my answer before asking the next question.
After each answer, give me feedback: what was strong, what was missing, what a great
answer would have added. At the end give me an overall score out of 10 and the 2
things I most need to improve.
```

---

## Progress Tracker

| Topic | Date Studied | Score | Ready? |
|---|---|---|---|
| Databricks Platform | — | — | No |
| Delta Lake Deep Dive | — | — | No |
| Spark Performance Tuning | — | — | No |
| dbt | — | — | No |
| Medallion Architecture | — | — | No |
| Data Governance / Unity Catalog | — | — | No |
| Pipeline Reliability | — | — | No |
