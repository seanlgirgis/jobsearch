# System Design

<a id="toc"></a>
## Table of Contents
1. [Data Warehouse](#sec-1)
2. [Data Lake](#sec-2)
3. [Lakehouse](#sec-3)
4. [Batch](#sec-4)
5. [Streaming](#sec-5)
6. [Lambda](#sec-6)
7. [Kappa](#sec-7)
8. [Bronze](#sec-8)
9. [Immutable raw ingestion layer used for replay and recovery.](#sec-9)
10. [Silver](#sec-10)
11. [Validation, deduplication, enrichment, schema enforcement, and trusted processing.](#sec-11)
12. [Gold](#sec-12)
13. [Fact Tables](#sec-13)
14. [Dimension Tables](#sec-14)
15. [Star Schema](#sec-15)
16. [Reliable pipelines are designed around failure recovery.](#sec-16)
17. [DLQ](#sec-17)
18. [Checkpointing](#sec-18)
19. [Batch Vs. Streaming](#sec-19)
20. [Performance vs operational complexity](#sec-20)
21. [Strict governance](#sec-21)
22. [Step 2 --- Architecture](#sec-22)
23. [Step 3 --- Reliability & Recovery](#sec-23)
24. [Closing Statement](#sec-24)

## Foundations

System design for data engineers focuses on building scalable, reliable,
observable, and maintainable data platforms.

Modern systems must support:

- High-volume ingestion

- Batch and streaming pipelines

- Real-time analytics

- Governance and compliance

- Failure recovery

- Distributed processing

- Cost-efficient scaling

Talk about recovery path and operational reasoning and trade-offs not
only the tools , and the happy path.

# Core Architecture Patterns

<a id="sec-1"></a>
### Data Warehouse

Curated analytics systems optimized for SQL, governance, and reporting.
*(snowflake, BigQuery, Redshift) -- OLAP Optimized*
[Back to TOC](#toc)


<a id="sec-2"></a>
### Data Lake

Low-cost storage for raw and semi-structured data. *(S3, Azure Data Lake
Storage ADLS, Google Cloud Storage GCS, Hadoop Distributed File System
HDFS)*

[Back to TOC](#toc)

<a id="sec-3"></a>
### Lakehouse

Combines lake flexibility with warehouse reliability using ACID
transactions and schema enforcement. *(DataBricks, Apache IceBerg,
Apache Hudi -streaming Friendly, Big Query with lakehouse support )*

# Batch vs Streaming

[Back to TOC](#toc)

<a id="sec-4"></a>
### Batch

Simpler Cheaper but Higher latency

[Back to TOC](#toc)

<a id="sec-5"></a>
### Streaming

Realtime analytics but Operational Complexity

[Back to TOC](#toc)

<a id="sec-6"></a>
### Lambda

Accuracy + low latency ; But Duplicate Logic

[Back to TOC](#toc)

<a id="sec-7"></a>
### Kappa

Simplified replay model ; Streaming dependency (kafka)

# Medallion Architecture 

[Back to TOC](#toc)

<a id="sec-8"></a>
### Bronze
[Back to TOC](#toc)


<a id="sec-9"></a>
### Immutable raw ingestion layer used for replay and recovery.

[Back to TOC](#toc)

<a id="sec-10"></a>
### Silver

[Back to TOC](#toc)

<a id="sec-11"></a>
### Validation, deduplication, enrichment, schema enforcement, and trusted processing.
[Back to TOC](#toc)


<a id="sec-12"></a>
### Gold

Business-ready analytics, KPIs, dashboards, and ML feature datasets.

![](media/image1.png){width="5.122753718285215in"
height="2.315638670166229in"}

Key insight: Bronze preserves truth, Silver creates trust, Gold serves
consumers.

# Modelling and Storage

Analytics modeling starts with access patterns.
[Back to TOC](#toc)


<a id="sec-13"></a>
### Fact Tables

Store measurable business events: orders, clicks, payments, shipments.

[Back to TOC](#toc)

<a id="sec-14"></a>
### Dimension Tables

Provide descriptive context: customer, product, geography, calendar.
[Back to TOC](#toc)


<a id="sec-15"></a>
### Star Schema

Fact table connected directly to dimensions for simpler analytics
queries.

- grain defines what one row represents.

- unclear grain causes duplicated metrics and inconsistent analytics.

## Governance and Observability

Governance defines ownership, lineage, discoverability, compliance, and
trust boundaries.

Observability validates both infrastructure health and data correctness

- Freshness monitoring

- Schema drift detection

- Volume anomaly detection

- Completeness checks

- SLA monitoring

- Audit logging

Green pipelines do not guarantee trustworthy data

Missing lineage makes schema changes dangerous at scale.

# Pipeline Reliability

[Back to TOC](#toc)

<a id="sec-16"></a>
### Reliable pipelines are designed around failure recovery.
[Back to TOC](#toc)


<a id="sec-17"></a>
### DLQ

Quarantine failed events.

Replayability

Rebuild trusted datasets.

Idempotency

Avoid duplicate corruption
[Back to TOC](#toc)


<a id="sec-18"></a>
### Checkpointing

Quarantine failed events.

Replayability

Recover streaming state.

Backfills

Repair historical partitions

Watermarks

Handle late-arriving data

Key insight: recovery engineering is now a core data engineering skill.

Retries without limits can amplify outages.

# Trade-Offs

[Back to TOC](#toc)

<a id="sec-19"></a>
### Batch Vs. Streaming

Simplicity vs low latency.

Lake vs Lakehouse

Flexibility vs governance.

[Back to TOC](#toc)

Heavy partitioning

<a id="sec-20"></a>
### Performance vs operational complexity
[Back to TOC](#toc)


<a id="sec-21"></a>
### Strict governance

Control vs engineering velocity.

Multi-region replication

Reliability vs infrastructure cost

Key insight: every scaling improvement introduces operational
consequences

optimizing prematurely often increases complexity without business
value.

## Common Mistakes

- Designing only the happy path

- Ignoring replay and recovery

- Over-focusing on tools

- Weak observability

- No schema governance

- Missing operational thinking

Key insight: Data Architects and Designers explain failures as clearly
as successes.

Gotcha: large systems fail in small hidden ways before they fail
visibly.

## Quick Reference

------------------------------------------------------------------------

- **OLTP** *Online Transaction Processing* Operational systems running
  live business transactions --- order placements, payments, user
  sign-ups.

- **OLAP** *Online Analytical Processing* Analytics systems built for
  reporting, aggregations and historical analysis --- not live
  transactions.

- **CDC** *Change Data Capture* Captures insert, update and delete
  mutations from database transaction logs for incremental ingestion.

- **Bronze** *Raw Immutable Layer* Raw data landed exactly as received.
  Never modified --- the source of truth for replay and recovery.

- **Silver** *Trusted Validated Layer* Cleaned, deduplicated,
  schema-validated and PII-masked data. Bad data stops here.

- **Gold** *Business-Ready Serving Layer* Aggregated, optimized datasets
  ready for BI dashboards, financial reporting and ML feature stores.

- **DLQ** *Dead Letter Queue* Quarantine location for failed or
  unparseable records --- isolated, not lost, inspectable for
  reprocessing.

- **Replayability** *Recovery from Source of Truth* Ability to rebuild
  Silver and Gold from Bronze after failure, logic change or corruption.

- **Idempotency** *Safe Repeated Processing* Same operation run multiple
  times produces the same result --- makes retries and replays safe.

- **Watermark** *Late Event Tolerance Window* Controlled waiting
  threshold that defines how long a stream waits for late-arriving
  events before closing a window.

- **Backfill** *Targeted Historical Reprocessing* Reprocessing a
  specific historical partition after a logic change or data fix ---
  scoped, not full reload.

- **Star Schema** *Fact-Centered Analytics Model* Central fact table
  surrounded by flat dimension tables --- simple joins, fast queries,
  optimized for analytics.

## System Design Walkthrough --- Global E-Commerce Analytics Platform

Scenario Design a scalable analytics platform processing millions of
daily events, supporting real-time dashboards, historical analytics, ML
training, governance, compliance, low cost, and full replay and
recovery.

Step 1 --- Clarify Requirements First Before designing, confirm:
throughput, latency expectations, regions, retention periods, recovery
SLAs, and who the consumers are.

[Back to TOC](#toc)

<a id="sec-22"></a>
### Step 2 --- Architecture

  ------------------------------------------------------------------------------
  **Layer**        **Choice**                  **Reason**
  ---------------- --------------------------- ---------------------------------
  **Ingestion**    Kafka + CDC                 Reliable, replayable event
                                               capture from all sources

  **Bronze**       Object storage (S3/GCS)     Immutable raw data --- source of
                                               truth for replay

  **Processing**   Spark + Flink               Batch and streaming on the same
                                               platform

  **Silver**       Validation +                Trust boundary --- bad data stops
                   deduplication + PII masking here

  **Gold**         BI dashboards + ML feature  Consumer-ready, optimized for
                   store                       query and training

  **Governance**   IAM + lineage + data        Security, ownership, compliance,
                   contracts                   auditability
  ------------------------------------------------------------------------------
[Back to TOC](#toc)


<a id="sec-23"></a>
### Step 3 --- Reliability & Recovery

- Bronze is immutable --- full replay from source of truth

- Idempotent writes throughout --- retries are safe

- DLQs for failed records --- nothing silently lost

- Watermarks for late events

- Freshness and completeness checks before Gold promotion

[Back to TOC](#toc)

<a id="sec-24"></a>
### Closing Statement

Strong designs explain recovery, replay, observability and failure
handling --- not just the happy path. Interviewers care more about
operational reasoning than exact tool names.
[Back to TOC](#toc)

