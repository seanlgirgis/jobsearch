# Databricks Crash Notes

## Databricks in Plain English
Databricks is a managed analytics platform where you run Spark workloads (Python/SQL/Scala) for data engineering, analytics, and ML workflows without manually managing most cluster details.

## Core Terms
- Workspace: The shared UI where notebooks, jobs, data objects, and permissions live.
- Notebook: Interactive document for code + markdown (good for development, demos, and debugging).
- Compute: The runtime resources used to execute notebook/job code.
- Cluster/Serverless:
  - Cluster: You choose config (size/runtime) and attach notebooks/jobs.
  - Serverless: Managed compute where startup/ops overhead is reduced.
- DataFrame: Distributed table-like structure in Spark for transformations.
- Delta table: Table format on cloud storage with ACID transactions and versioning.
- Jobs/Workflows: Scheduled/orchestrated production runs of notebook/script tasks.

## AWS Mapping (S3 + PySpark + SQL)
- Storage: Raw and curated data can live in S3.
- Processing: PySpark transformations run on Databricks compute.
- Querying: SQL can query managed/external tables backed by Delta data in S3.
- Orchestration: Databricks Workflows runs pipeline steps on schedule or trigger.

## Structured Streaming (Short)
Spark Structured Streaming treats incoming events as a continuously updating table. You define transformations once, then Spark runs them repeatedly in micro-batches (or continuous mode), writes to a sink, and tracks progress with checkpoints.

## Delta Lake (Short)
Delta Lake is a table layer over files (like Parquet) that adds ACID transactions, schema enforcement/evolution, time travel/version history, and more reliable upserts/merges for ETL pipelines.
