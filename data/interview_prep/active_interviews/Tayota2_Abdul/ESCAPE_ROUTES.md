# Surprise Topic Escape Routes
**30 seconds per topic. Enough to have a conversation. Never go blank.**

---

## Terraform
> "I understand the model — state file, provider, plan/apply cycle, modules for reuse. I've worked alongside Terraform-managed infrastructure and I've done more hands-on work in CloudFormation. The concepts translate directly — IaC is IaC. I'd ramp on Terraform syntax quickly."

---

## AWS ECS / Fargate
> "ECS is how I'd containerize and scale a FastAPI service in production. Cluster holds task definitions, Fargate removes the EC2 management, the service keeps N tasks running, ALB routes traffic in, and auto scaling handles load. VPC integration is clean for talking to RDS, ElastiCache, private resources."

---

## CI/CD
> "Build, test, deploy with gates. Code pushed → tests run → if green, deploy. Blue-green for zero-downtime, canary for controlled rollout. The principle: every deploy should be repeatable, auditable, and rollback-able. I've built pipelines that gate on test pass before anything touches production."

---

## MSK / Kafka
> "Kafka is a distributed event log. Topics split into partitions for parallelism. Consumer groups read independently — each group maintains its own offset. MSK is managed Kafka on AWS. Key distinction from SQS: Kafka retains messages and supports replay. SQS is fire-and-forget. Use Kafka when you need event history, fan-out, or stream replay."

---

## Snowflake
> "Columnar cloud warehouse with separation of storage and compute. Virtual warehouses scale independently. Key patterns: time travel for recovery, zero-copy cloning for dev/test, data sharing across accounts. Works well as the Gold layer in a medallion architecture."

---

## dbt
> "Transformation layer that turns SQL into a tested, versioned, documented pipeline. Models are SELECT statements, tests are assertions, lineage is auto-generated. Lives in the Silver-to-Gold transformation zone. Great for analytics engineering and giving data teams ownership of their transformations."

---

## OpenSearch / Elasticsearch
> "Distributed search and analytics engine. Documents stored as JSON, queried with a DSL. Good for log analytics, full-text search, time-series metrics, and observability dashboards. AWS OpenSearch is the managed version. I used Dynatrace for observability at G6 — OpenSearch sits in the same space for self-managed log analytics."

---

## Docker
> "Package code + runtime + dependencies into an image. Build once, run anywhere. Dockerfile defines the image, docker-compose for local multi-service setup. In production images go to ECR, get pulled by ECS task definitions. The value: environment consistency from dev to prod."

---

## AWS Lambda
> "Serverless compute — event triggers a function, runs, scales to zero. Good for lightweight event-driven processing, API backends with Mangum, pipeline triggers. Tradeoffs: cold starts, no persistent connection pool, 15-min max runtime. For heavy or long-running work — ECS or Glue."

---

## AWS Step Functions
> "Serverless workflow orchestrator. Chains Lambda, ECS tasks, Glue jobs, and waits into a state machine. Built-in retry, error handling, parallel branches, and execution history. Good for multi-step pipelines where you need visibility and recovery without building a custom orchestrator."

---

## AWS Glue
> "Managed Spark ETL service. Write PySpark or use visual editor. Glue Data Catalog is the metadata store — tables, schemas, partitions. Crawlers discover schemas automatically. Good for batch ETL at scale without managing a Spark cluster. Tradeoffs: cold start latency, less control than EMR."

---

## PyIceberg / Apache Iceberg
> "Open table format on top of object storage. Gives you ACID transactions, schema evolution, time travel, and partition pruning on data lakes. Think of it as the governance and reliability layer that turns S3 into something warehouse-like. PyIceberg is the Python client. Works well with Spark, Athena, Trino."

---

## Redis
> "In-memory key-value store. Used for caching, session storage, rate limiting, pub/sub, leaderboards. Extremely fast for read-heavy workloads where staleness is acceptable. In a FastAPI service: cache expensive query results with a short TTL instead of hitting the DB every request."

---

## Python Testing
> "Unit tests for transformation logic, integration tests for pipeline stages, TestClient for FastAPI routes. pytest is the standard. Key discipline: test the failure path, not just the happy path. Dependency injection in FastAPI makes it easy to override dependencies in tests without touching production code."

---

## Security / IAM
> "Least privilege — pipelines and services get only the permissions they need, nothing more. IAM roles for services, not IAM users with keys. Secrets in Secrets Manager, not environment variables or code. PII masked at Silver, never exposed in Gold. Audit trails for who accessed what."


---

## PySpark
> "PySpark is distributed data processing. The key idea is DataFrames are lazily evaluated, transformations build a plan, and actions trigger execution. I think in partitions, joins, shuffle cost, file formats, and schema control. Good PySpark means avoiding Python UDFs when possible, using built-in functions, writing Parquet, partitioning carefully, and making jobs restartable and idempotent."

---

## Spark Performance
> "Most Spark performance issues come from bad joins, too much shuffle, skewed data, tiny files, or reading more data than needed. I would check the Spark UI, look at stage time and shuffle size, filter early, select only needed columns, broadcast small dimensions, repartition intentionally, and write columnar files like Parquet. I don't tune executors first unless I understand the data movement problem."

---

## dbt Advanced
> "dbt is not just SQL files. The production value is tests, lineage, documentation, environments, incremental models, snapshots, and CI checks. I would use dbt for warehouse transformations where analysts and engineers need version-controlled SQL. The main caution is not putting heavy procedural logic into dbt — if orchestration or distributed processing gets complex, pair it with Airflow, Dagster, Spark, or warehouse-native jobs."

---

## SQL for Data Engineering
> "SQL is the core language for validating and shaping data. For interviews, I focus on joins, window functions, CTEs, deduplication, slowly changing dimensions, incremental loads, and query performance. A strong data engineer does not just write a query that works — they understand grain, null handling, duplicate behavior, partition pruning, and how the query will scale."

---

## Pandas
> "Pandas is great for small-to-medium local data work, profiling, quick transformations, and test fixtures. I would not use pandas for large production datasets that exceed memory. For production, I either keep pandas jobs small and controlled, or move to PySpark, Polars, DuckDB, Glue, or the warehouse. The escape phrase is simple: pandas is excellent locally, but not my distributed processing engine."

---

## Airflow
> "Airflow orchestrates workflows. DAGs define task dependencies, schedules, retries, SLAs, and operational visibility. I do not use Airflow to process huge data inside the scheduler itself. I use it to trigger Spark, Glue, dbt, ECS, Lambda, SQL jobs, or APIs. The rule is: Airflow coordinates work; compute engines do the heavy work."

---

## Data Modeling
> "I start with the business question and grain. What is one row? Then I separate facts from dimensions, choose keys, define measures, handle slowly changing attributes, and make sure the model supports reporting without confusing joins. Good modeling prevents downstream chaos because dashboards, metrics, and data quality checks all depend on stable grain."

---

## Data Quality
> "Data quality means checking freshness, completeness, validity, uniqueness, referential integrity, and business rules. I like checks at multiple points: raw ingestion checks, Silver validation, and Gold business-facing assertions. The key is not just failing a pipeline — it is alerting with enough context to fix the issue quickly."

---

## Data Contracts
> "A data contract defines what upstream producers promise: schema, meaning, ownership, freshness, and allowed changes. Without contracts, downstream pipelines break silently. I would use contracts for critical datasets, especially when multiple teams depend on the same events, API payloads, or warehouse tables."

---

## CDC
> "Change Data Capture means capturing inserts, updates, and deletes from a source system instead of full reloading everything. The key issues are ordering, primary keys, deletes, schema changes, and replay. CDC is powerful because it reduces load on source systems and supports near-real-time pipelines, but it needs careful idempotent merge logic downstream."

---

## APIs as Data Sources
> "API ingestion is about pagination, rate limits, retries, auth, incremental cursors, and schema drift. I would store raw responses first, track request metadata, make the load restartable, and only transform after landing the raw data. The biggest mistake is treating an API like a database table — APIs fail, throttle, and change."

---

## File Ingestion
> "For file-based ingestion, I care about file naming, arrival time, schema, deduplication, corrupt files, and replay. I usually land files raw first, validate them, then promote clean records into curated layers. I prefer immutable raw storage because it gives me recovery, auditability, and backfill safety."

---

## Medallion Architecture
> "Bronze is raw and replayable, Silver is cleaned and conformed, Gold is business-ready. The value is separation of concerns. If a Gold metric is wrong, I can trace it back through Silver rules and Bronze source data. It also helps with quality checks, access control, and recovery."

---

## Lakehouse
> "A lakehouse combines cheap object storage with warehouse-like table management. Formats like Iceberg, Delta, or Hudi add transactions, schema evolution, time travel, and efficient reads on top of S3 or similar storage. I think of it as making the data lake reliable enough for production analytics."

---

## Orchestration vs Transformation
> "Orchestration decides when work runs and in what order. Transformation changes the data. Airflow, Step Functions, or Dagster orchestrate. dbt, Spark, SQL, or Python transform. Keeping that boundary clean makes pipelines easier to debug and operate."

---

## Batch vs Streaming
> "Batch is simpler, cheaper, and easier to replay. Streaming is for lower-latency use cases where the business truly needs data quickly. I would ask about latency requirements first. If hourly or daily is acceptable, batch is usually the better design. If seconds or minutes matter, then I consider Kafka, Flink, Spark Structured Streaming, or managed streaming services."

---

## The Data Engineer Recovery Answer
> "If a pipeline fails, I first identify whether the problem is source, code, infrastructure, schema, or data quality. Then I stop bad downstream propagation, preserve raw data, fix the root cause, replay from a safe checkpoint, and validate counts and business metrics before marking it resolved."


---

## Parquet
> "Parquet is a columnar storage format optimized for analytics. Instead of storing rows together, it stores columns together, which means analytical queries only read the columns they need. That reduces I/O dramatically. It also supports compression and encoding very efficiently. In data engineering, Parquet is usually the default format for curated datasets because it works well with Spark, Athena, Snowflake external tables, Trino, and lakehouse engines."

---

## Why Columnar Matters
> "If a table has 200 columns but the query only needs 5, Parquet only reads those 5 columns from disk. That's why analytical scans are much faster compared to row-based formats like CSV or JSON. Columnar storage is one of the biggest reasons warehouses scale efficiently."

---

## Partitioning
> "Partitioning physically organizes files by a column like date, region, or tenant. The goal is partition pruning — only scanning the folders needed for a query. Good partitions reduce scan cost and improve speed. Bad partitions create tiny files or uneven distribution. The rule is: partition by commonly filtered columns with reasonable cardinality."

---

## Small File Problem
> "Distributed systems hate millions of tiny files. Metadata overhead grows, planning slows down, and Spark performance drops. A common optimization is compaction — merging small files into larger ones, often around 128MB to 1GB depending on the engine and workload."

---

## Compression
> "Parquet supports compression like Snappy, Gzip, and ZSTD. Snappy is common because it balances speed and compression. Compression matters because storage and I/O are usually more expensive than CPU in analytics workloads."

---

## Schema Evolution
> "Schema evolution means safely adding or modifying columns over time without breaking readers. Formats like Parquet plus Iceberg or Delta support this well. The important thing is controlled evolution — not random schema drift from upstream systems."

---

## Predicate Pushdown
> "Predicate pushdown means the engine pushes filters down into the storage layer so unnecessary data is skipped early. For example, if I filter WHERE date='2026-04-01', Parquet metadata helps avoid scanning irrelevant row groups."

---

## Row Groups
> "Parquet stores data in row groups. Each row group contains metadata like min/max values for columns. Query engines use that metadata to skip irrelevant chunks of data during scans. That's one reason Parquet queries can be dramatically faster than CSV."

---

## CSV vs Parquet
> "CSV is human-readable but inefficient for analytics: no schema enforcement, no compression efficiency, no column pruning, no metadata, expensive parsing. Parquet is optimized for machines and large-scale analytics. CSV is usually for interchange or quick exports; Parquet is for production analytics storage."

---

## ORC
> "ORC is another columnar analytics format similar to Parquet. ORC historically had strong Hadoop ecosystem adoption while Parquet became more broadly adopted across cloud analytics tools. In practice, Parquet is the more common default in modern cloud data engineering."

---

## Avro
> "Avro is row-oriented and schema-focused. It's commonly used for Kafka events and serialization between systems. Parquet is better for analytical querying; Avro is better for event transport and row-based serialization."

---

## Delta Lake
> "Delta Lake adds ACID transactions, schema enforcement, time travel, and reliable upserts on top of Parquet files. Without Delta, a data lake is mostly files. Delta turns it into a transactional storage layer suitable for production pipelines."

---

## Apache Hudi
> "Hudi focuses heavily on incremental processing and upsert workloads on data lakes. It helps manage mutable datasets efficiently while still storing data in open formats on object storage."

---

## Iceberg Metadata Layer
> "Iceberg separates table metadata from physical files and tracks snapshots over time. That enables schema evolution, partition evolution, rollback, and time travel without fragile Hive-style partition management."

---

## Time Travel
> "Time travel means querying historical versions of data. Very useful for debugging, audits, recovery, accidental deletes, and reproducing reports. Snowflake, Delta, and Iceberg all support this concept."

---

## Upserts / MERGE
> "An upsert means updating existing rows and inserting new ones in one operation. In lakehouses this usually happens through MERGE statements backed by transactional table formats like Iceberg or Delta."

---

## Data Skew
> "Data skew happens when one partition or executor gets disproportionately more data than others. One hot key can slow an entire Spark job. Mitigations include salting, repartitioning, broadcast joins, or redesigning the partition strategy."

---

## Broadcast Join
> "If one table is small enough, Spark can broadcast it to all executors instead of shuffling both datasets. That reduces network shuffle cost significantly and is one of the most important Spark optimizations."

---

## Shuffle
> "Shuffle is data movement across executors during joins, aggregations, and repartitioning. Shuffle is expensive because it involves network transfer and disk spill. Most Spark optimization discussions are really shuffle reduction discussions."

---

## Lazy Evaluation
> "Spark transformations are lazily evaluated. The engine builds a DAG execution plan first, then executes only when an action happens like collect, count, or write. That allows Spark to optimize execution before running."

---

## DAG
> "Spark represents jobs as Directed Acyclic Graphs. Each transformation becomes part of the execution lineage. Understanding DAG stages helps explain where shuffles, bottlenecks, and retries occur."

---

## Idempotency
> "Idempotent pipelines can run multiple times without corrupting results. That's critical for retries, replay, and recovery. Techniques include deterministic merges, checkpointing, deduplication keys, and overwrite-by-partition patterns."

---

## Backfill
> "A backfill is reprocessing historical data for missing or corrected periods. Good pipeline design assumes backfills will happen eventually and makes them operationally safe."

---

## Replay
> "Replay means reprocessing events or files from an earlier checkpoint or offset. Kafka retention and immutable Bronze storage make replay possible. Replayability is one of the biggest reliability advantages in modern data platforms."

---

## Exactly Once vs At Least Once
> "Exactly-once delivery is difficult in distributed systems and often expensive. Many systems operate with at-least-once delivery plus idempotent consumers. The important thing is whether duplicates corrupt business results."

---

## Watermarking
> "Watermarking in streaming defines how long the system waits for late-arriving events before finalizing aggregations. It's a tradeoff between latency and correctness."

---

## Slowly Changing Dimensions (SCD)
> "SCD Type 1 overwrites old values. Type 2 preserves history with effective dates and current flags. Type 2 is common in analytics where historical business context matters."

---

## Data Lineage
> "Lineage tracks where data came from, what transformed it, and what downstream systems depend on it. Critical for debugging, governance, audits, and impact analysis."

---

## Data Catalog
> "A data catalog stores metadata about datasets: schema, ownership, lineage, definitions, freshness, and access controls. Examples include Glue Catalog, Unity Catalog, and DataHub."

---

## Observability
> "Data observability means monitoring freshness, volume, schema changes, failures, latency, and data quality over time. The goal is catching bad data before business users do."

---

## SLAs vs SLOs
> "SLA is the formal commitment. SLO is the operational target. Example: an SLO may target 99% pipeline completion by 7 AM while the SLA defines contractual consequences if missed."

---

## Dead Letter Queue (DLQ)
> "A DLQ stores records that failed processing instead of losing them entirely. That allows investigation and replay without blocking the entire pipeline."

---

## Event-Driven Architecture
> "Instead of services polling constantly, events trigger downstream processing. Producers publish events; consumers react independently. This decouples systems and improves scalability."

---

## Feature Store
> "A feature store centralizes ML features for training and inference consistency. The main value is preventing training-serving skew and avoiding duplicated feature engineering logic."

---

## Vector Database
> "Vector databases store embeddings for similarity search in AI systems. They are useful for semantic search, recommendation, and retrieval-augmented generation workloads."

---

## DuckDB
> "DuckDB is an in-process analytical database optimized for local analytics. Extremely useful for fast SQL queries directly on Parquet files without standing up infrastructure."

---

## Polars
> "Polars is a high-performance DataFrame library built around Arrow memory format. It's often significantly faster and more memory-efficient than pandas for analytical workloads."

---

## Apache Arrow
> "Arrow is an in-memory columnar format designed for efficient interoperability between systems like Spark, pandas, Polars, and DuckDB. It reduces serialization overhead during data exchange."

---


## The Universal Escape When You're Truly Stuck
> "That's an area I've touched at the edges rather than gone deep on. The way I'd approach it is [apply the principle from what I know]. Can you tell me more about how it shows up in your stack? I want to make sure I'm giving you a useful answer rather than a generic one."

---


*Honest. Curious. Buys you information. Never sounds like a dodge.*
