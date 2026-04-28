# Data Architecture — Interview Prep Guide (2026)

## What Is Data Architecture?

Data architecture is the blueprint for how data is collected, stored, transformed, governed, secured, and consumed across an organization.

From a business perspective:
- It enables reporting, analytics, machine learning, compliance, and operational decision-making.
- It determines whether leadership trusts the data.

From a technical perspective:
- It defines systems, storage patterns, integration methods, data flow, modeling standards, governance, and scalability strategies.

A strong data architecture answers questions like:
- Where does data originate?
- How does it move?
- Who owns it?
- How is quality enforced?
- How do systems scale?
- How is access controlled?
- How do downstream teams consume trusted datasets?

Modern interviewers expect engineers to understand architecture decisions — not just tools.

---

# Why Data Architecture Matters

Poor architecture creates:
- Duplicate pipelines
- Inconsistent metrics
- Data silos
- Slow analytics
- High cloud costs
- Security risks
- Unreliable dashboards

Good architecture creates:
- Reusable data products
- Faster development
- Lower operational cost
- Trustworthy analytics
- Easier governance
- Scalable AI and ML workflows

Senior-level engineers are expected to think in systems, not isolated jobs.

---

# OLTP vs OLAP

## OLTP (Online Transaction Processing)

Purpose:
- Handles operational transactions in real time.

Examples:
- Banking systems
- E-commerce checkout
- Inventory updates
- Mobile app interactions

Characteristics:
- Small frequent writes
- Highly normalized schemas
- Millisecond latency
- ACID transactions
- Optimized for inserts/updates

Common technologies:
- PostgreSQL
- MySQL
- SQL Server
- DynamoDB
- MongoDB

Example:
A user places an order on a website.

---

## OLAP (Online Analytical Processing)

Purpose:
- Handles analytics and reporting workloads.

Characteristics:
- Large scans
- Aggregations
- Historical analysis
- Optimized for reads
- Denormalized schemas

Common technologies:
- Snowflake
- BigQuery
- Redshift
- Databricks
- ClickHouse

Example:
Revenue trends over the last two years.

---

## Interview Tradeoff

A common interview question:

“Why not run analytics directly on OLTP systems?”

Strong answer:
- Analytical queries create heavy scans and lock contention.
- OLTP systems prioritize transactional latency.
- Mixing workloads hurts production performance.
- Separate analytical systems improve scalability and reliability.

---

# Data Warehouse vs Data Lake vs Lakehouse

# Data Warehouse

Purpose:
Structured analytics.

Characteristics:
- Schema-on-write
- Curated structured data
- Strong governance
- Fast BI queries

Pros:
- Excellent performance
- Mature governance
- Strong SQL experience

Cons:
- Expensive at scale
- Less flexible for raw/semi-structured data

Examples:
- Snowflake
- Redshift
- BigQuery

---

# Data Lake

Purpose:
Store raw data cheaply at massive scale.

Characteristics:
- Schema-on-read
- Stores structured and unstructured data
- Flexible ingestion

Pros:
- Cheap storage
- Supports ML and data science
- Handles large-scale ingestion

Cons:
- Governance challenges
- Data swamps if unmanaged
- Quality inconsistencies

Examples:
- S3
- Azure Data Lake
- GCS

---

# Lakehouse

Purpose:
Combine lake flexibility with warehouse performance.

Characteristics:
- Open table formats
- ACID transactions
- Unified analytics and ML

Examples:
- Delta Lake
- Apache Iceberg
- Apache Hudi

Pros:
- Lower storage cost
- Unified architecture
- Better governance than raw lakes

Cons:
- Operational complexity
- Metadata scaling challenges

---

# Interview Perspective

Junior answer:
“A lake stores files and a warehouse stores tables.”

Senior answer:
“The decision depends on governance requirements, concurrency, workload isolation, ML requirements, storage economics, and operational complexity.”

---

# Batch vs Streaming

# Batch Processing

Processes data at intervals.

Examples:
- Daily reporting
- Overnight ETL
- Financial reconciliation

Pros:
- Simpler
- Easier debugging
- Lower operational overhead

Cons:
- Higher latency
- Not suitable for real-time use cases

Tools:
- Airflow
- Spark
- dbt

---

# Streaming Processing

Processes events continuously.

Examples:
- Fraud detection
- IoT telemetry
- Real-time dashboards
- Clickstream analytics

Pros:
- Low latency
- Real-time insights

Cons:
- Higher complexity
- Stateful processing challenges
- Ordering and replay difficulties

Tools:
- Kafka
- Flink
- Spark Structured Streaming
- Kinesis

---

# Interview Insight

Strong candidates discuss:
- Event ordering
- Idempotency
- Exactly-once myths
- Watermarking
- Backpressure
- Replay strategies

---

# Lambda vs Kappa Architecture

# Lambda Architecture

Two paths:
- Batch layer
- Speed layer

Purpose:
Balance accuracy and low latency.

Pros:
- Fault tolerance
- Historical recomputation support

Cons:
- Duplicate logic
- Operational complexity

---

# Kappa Architecture

Single streaming pipeline.

Pros:
- Simpler architecture
- Unified processing logic

Cons:
- Replay and correction complexity
- Stateful recovery concerns

---

# Practical Interview View

Most modern systems lean toward Kappa-style streaming because maintaining duplicate logic is expensive.

However:
- Batch still dominates many enterprise workflows.
- Hybrid systems remain common in large organizations.

Strong engineers avoid ideological answers.

---

# Medallion Architecture

Popularized by Databricks.

## Bronze Layer
Raw ingestion.
Minimal transformation.

Characteristics:
- Immutable
- Append-heavy
- Full audit history

---

## Silver Layer
Validated and cleaned data.

Typical operations:
- Deduplication
- Standardization
- Type enforcement
- Business rule validation

---

## Gold Layer
Business-ready datasets.

Examples:
- KPI tables
- Executive dashboards
- ML feature datasets

---

# Interview Insight

The real value:
- Clear data quality boundaries
- Easier debugging
- Better lineage
- Reprocessing flexibility

---

# Data Modeling for Analytics

# Fact Tables

Contain measurable events.

Examples:
- Sales
- Orders
- Clicks

Common fields:
- Foreign keys
- Metrics
- Timestamps

---

# Dimension Tables

Contain descriptive attributes.

Examples:
- Customer
- Product
- Geography

---

# Star Schema

Facts connected directly to dimensions.

Pros:
- Faster analytics
- Simpler queries

Cons:
- Data duplication

---

# Snowflake Schema

Normalized dimensions.

Pros:
- Reduced redundancy

Cons:
- More joins
- Higher query complexity

---

# Interview Tradeoff

Strong answer:
“Star schemas are usually preferred for analytics because query simplicity and performance matter more than normalization efficiency.”

---

# Governance, Metadata, and Lineage

Modern organizations need:
- Ownership
- Discoverability
- Compliance
- Auditability

Key concepts:
- Data catalogs
- Metadata management
- Lineage tracking
- Data contracts

Examples:
- DataHub
- OpenMetadata
- Collibra
- Amundsen

---

# Data Contracts

A producer-consumer agreement defining:
- Schema
- Semantics
- SLAs
- Ownership

Benefits:
- Prevents downstream breaking changes
- Improves reliability

Interviewers increasingly ask about this in 2026.

---

# Data Quality and Observability

Strong pipelines measure:
- Freshness
- Completeness
- Accuracy
- Uniqueness
- Volume anomalies
- Schema drift

---

# Important Concepts

## Freshness
How recent is the data?

## Completeness
Are expected records missing?

## Drift
Has the data distribution changed unexpectedly?

## SLA vs SLO

SLA:
Formal guarantee.

SLO:
Internal reliability target.

---

# Common Tools

- Great Expectations
- Monte Carlo
- Soda
- Datadog
- OpenLineage

---

# Interview Insight

Senior engineers treat data quality as an operational concern, not an afterthought.

---

# Security and Privacy Fundamentals

Key areas:
- Authentication
- Authorization
- Encryption
- Auditing
- PII handling

---

# IAM Principles

Use:
- Least privilege
- Role-based access
- Short-lived credentials

Avoid:
- Shared credentials
- Broad wildcard permissions

---

# Encryption

At rest:
- S3 SSE-KMS
- Disk encryption

In transit:
- TLS
- HTTPS

---

# PII Handling

Examples:
- Email
- SSN
- Payment data

Common controls:
- Tokenization
- Masking
- Row-level security
- Column-level encryption

---

# Cost and Performance Optimization

# Common Optimization Patterns

## Partitioning
Reduces scan volume.

## Clustering
Improves query pruning.

## Columnar Formats
Parquet and ORC reduce I/O.

## Compaction
Prevents small-file problems.

## Materialized Views
Speeds repeated aggregations.

---

# Common Anti-Patterns

## Small Files
Kills query performance.

## Over-Partitioning
Creates metadata overhead.

## Unbounded Streaming State
Leads to memory issues.

## Duplicate Pipelines
Causes inconsistent business metrics.

## No Governance
Creates “data swamp” conditions.

---

# Interview System Design Walkthrough

## Scenario

Design a scalable analytics platform for an e-commerce company.

Requirements:
- Millions of daily events
- Real-time dashboards
- Historical analytics
- ML training support
- Governance and compliance

---

# Sample Architecture

## Ingestion
- Kafka or Kinesis
- CDC from OLTP databases

## Raw Storage
- S3 data lake

## Stream Processing
- Flink or Spark Streaming

## Batch Processing
- Spark jobs orchestrated with Airflow

## Curated Storage
- Delta Lake or Iceberg tables

## Analytics Layer
- Snowflake or Databricks SQL

## Governance
- Data catalog + lineage

## Monitoring
- Freshness SLAs
- Schema drift detection
- Pipeline observability

---

# Strong Interview Discussion Points

A strong candidate explains:
- Why replayability matters
- How idempotency is enforced
- Why bronze/silver/gold separation helps
- Cost controls
- Security boundaries
- Failure recovery patterns
- Data ownership

---

# Interview Q&A

## 1. What’s the difference between a warehouse and a lake?

A warehouse stores curated structured data optimized for analytics. A lake stores raw and flexible data formats at lower cost.

---

## 2. Why use Parquet instead of CSV?

Parquet is columnar, compressed, and optimized for analytical scans.

---

## 3. What causes small-file problems?

Frequent micro-batches or excessive partitioning.

---

## 4. What’s schema evolution?

Managing controlled schema changes over time without breaking consumers.

---

## 5. What’s the purpose of a medallion architecture?

It separates raw ingestion, validated transformation, and business-ready datasets.

---

## 6. Why is lineage important?

It helps debugging, compliance, and impact analysis.

---

## 7. What’s idempotency?

The ability to safely retry processing without creating duplicates.

---

## 8. Why separate compute and storage?

Independent scaling and better cost efficiency.

---

## 9. What’s a data contract?

A formal agreement between producers and consumers about schemas and expectations.

---

## 10. Why avoid querying OLTP systems directly?

Analytics workloads degrade transactional performance.

---

## 11. What’s partition pruning?

Skipping irrelevant partitions during query execution.

---

## 12. What’s watermarking in streaming?

A strategy for handling late-arriving events.

---

## 13. What’s backpressure?

When downstream systems can’t keep up with incoming data rates.

---

## 14. Why use CDC?

Efficiently capture incremental database changes.

---

## 15. What’s the biggest architecture mistake teams make?

Building pipelines without governance, ownership, or quality monitoring.

---

## 16. When should you choose batch over streaming?

When latency requirements don’t justify streaming complexity.

---

## 17. What’s a lakehouse?

A platform combining data lake scalability with warehouse capabilities.

---

# Final Cheat Sheet

## Core Concepts
- OLTP = transactions
- OLAP = analytics
- Warehouse = curated analytics
- Lake = raw scalable storage
- Lakehouse = unified architecture

---

## Processing
- Batch = simpler
- Streaming = lower latency, higher complexity

---

## Modeling
- Facts = measurable events
- Dimensions = descriptive context
- Star schema usually preferred for analytics

---

## Reliability
- Idempotency matters
- Replayability matters
- Observability matters

---

## Governance
- Metadata
- Lineage
- Ownership
- Contracts

---

## Security
- Least privilege
- Encryption
- PII controls

---

## Senior-Level Thinking

Interviewers want to hear:
- Tradeoffs
- Scalability concerns
- Operational reliability
- Cost awareness
- Governance strategy
- Failure handling
- Cross-team ownership

That’s what separates a junior implementation answer from a senior architectural answer.