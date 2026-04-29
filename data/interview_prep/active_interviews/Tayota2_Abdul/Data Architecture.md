# Data Architecture

## Foundations

Data architecture is the blueprint for how data is collected, stored,
transformed, governed, secured and consumed across organizations. It
created business trust with technical design: dashboards, compliance,
machine learning and operations reporting all depend on sound
architectural decisions made upstream.

The one should explain architecture as a system of trade of not a list
of tools. The important Question where data originated, how to move it,
who owns it, how to enforce its quality and correctness, and how down
stream teams consume the trusted processed datasets.

Mental hook:

"Data architecture turns raw data into trusted business decisions."

### OLTP

Operational transactions with low latency. ***Ex: PostgreSQL, Oracle,
DynamoDB***

### OLAP

Analytics, reporting, Aggregations, historical scan. ***Ex: snowflake,
BigQuery, Redshift, DataBricks\***

## Core Architecture Patterns

A warehouse (snowflake, BigQuery and red shift) prioritizes curated SQL
analytics and governance.

A Data Lake (S3, Azure Data Lakes, GCS) prioritizes flexible, low-cost
storage for raw and semi-structured data.

A Lakehouse (Databricks , Apache Iceberg, Apache Hudi) raw storage with
warehouse-like ACID transactions, schema enforcement and query
performance on top

### ACID

Atomicity, Consistency, Isolation, Durability

## Batch, Streaming, Lambda and Kappa

Batch processing is simpler, cheaper and easier to debug.

Streaming is more complex. While providing low latency, it introduces
event ordering, late arrivals, state management, and replay.

Lamda architecture uses Batch and speed layers to process

Kappa architecture simplifies over lambda by using kafka stream and
replay as source of truth.

## Modelling and Storage

Analytics modeling starts with access patterns.

Fact tables store measurable business events, orders, clicks, payments,
or shipments.

Dimensions tables add restrictive context such as customer, product,
geography, or calendar attributes.

Star Schema preferred for analytics because they keep queries simple and
performant.

Snowflake Schema reduces redundancy by normalizing dimensions, but
adding joins increases complexity.

## Governance, Quality and Security

Governance defines ownership, discoverability, compliance and
durability. Metadata, catalogs, lineage systems and data contracts help
teams understand where data comes from, who owns it and what will break
if a schema or metric changes.

Quality and Observability make data systems operationally trustworthy.
Good pipelines monitor freshness, completeness, uniqueness, schema
Drift, volume anomalies and distribution change. Successful job is not
enough. Data has to be correct and usable.

Security enforces who can access what and ensures data is protected at
every layer

- Least privilege --- pipelines and users access only what they need

- PII masking --- applied at Silver, never exposed in Gold

- Encryption --- at rest and in transit

- Audit trails --- who accessed what and when

## Performance and Cost

Performance and cost are connected. Columnar formats such as Parquet
reduce I/O by reading only required columns. Partitioning reduces scan
volume. Clustering improves pruning. Materialized views speed repeated
aggregations. Compaction prevents query engines from wasting time
opening thousands of tiny files.

- Partitioning - Reduces scanned data

- Parquet - Column pruning and compression

- Compaction - Fixes small-file overhead

- Materialized views - Faster dashboards

## System Design Walkthrough

### Scenario

Design a scalable analytics platform for a large e-commerce company
handling:

- millions of daily events

- real-time dashboards

- historical analytics

- ML training

- governance and compliance requirements

------------------------------------------------------------------------

A strong design starts with reliable ingestion.

Use:

- event streams for user activity

- CDC for operational database changes

Technologies commonly used:

- Apache Kafka

- Amazon Kinesis

Raw immutable data lands in Bronze object storage.

Processing layers:

- validate

- clean

- standardize

- enrich

- deduplicate

Common engines:

- Apache Spark

- Apache Flink

- dbt workflows

Trusted Silver data is stored in:

- Delta Lake

- Apache Iceberg

Gold publishes:

- BI tables

- KPIs

- dashboards

- ML feature datasets

Architecture flow:

OLTP Apps

\|

\|\-- CDC / Events

v

Kafka / Kinesis

\|

v

Bronze Raw Storage (S3)

\|

v

Spark / Flink Processing

\|

v

Silver Trusted Tables

\|

v

Gold BI + ML Features

Interview focus is usually NOT the tool list.

Interviewers care more about:

- replayability

- idempotency

- observability

- schema evolution

- security boundaries

- late event handling

- retries and recovery

- failure isolation

Do not design only the happy path.

Always explain:

- what happens if schemas drift

- how late events are handled

- how corrupted data is quarantined

- how replay/backfill works

- how dashboards recover from bad downstream data

Mental hook:

"Good architecture plans for failure, not just success."

**Q: Why not run analytics directly on OLTP databases?**

*OLTP systems are optimized for low-latency transactions, not large
analytical scans. Heavy reporting queries can create contention and slow
production workloads. Separating OLTP from OLAP improves reliability,
scalability, and workload isolation.*

**Q: How do you choose between a data warehouse, lake, and lakehouse?**

*Use a warehouse when governed SQL analytics is the primary need. Use a
lake for low-cost raw storage and flexible ingestion. Use a lakehouse
when you need open storage, ACID table behavior, ML support, and
warehouse-like reliability.*

**Q: When should batch be preferred over streaming?**

*Choose batch when the business does not require real-time decisions.
Batch is simpler to debug, cheaper to operate, and easier to reason
about. Streaming is valuable when low latency justifies the added
complexity.*

**Q: What is the value of medallion architecture?**

*It creates clear quality boundaries between raw, validated, and
business-ready data. Bronze supports replay and audit history, silver
applies validation and standardization, and gold serves trusted
consumption. This structure improves debugging and ownership.*

**Q: Why is idempotency important in data pipelines?**

*Distributed systems fail and retry constantly. Idempotent processing
ensures retries or replays do not create duplicate or corrupted results.
This is essential for reliable CDC, streaming, backfills, and recovery
workflows.*

**Q: What separates a senior architecture answer from a junior answer?**

*Junior answers focus on definitions and tools. Senior answers explain
tradeoffs, failure modes, cost, governance, data quality, and
operational ownership. Interviewers want to know how the design behaves
under pressure.*
