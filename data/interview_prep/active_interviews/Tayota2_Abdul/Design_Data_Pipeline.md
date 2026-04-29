**A Data pipeline: -**

The pipeline moves data from producers to consumers through ingestion,
storage, transformation, and serving. And across all of that, I care
about observability so I know it\'s working, security so only the right
people touch the data, and cost so it\'s sustainable.

**Requirements of Data pipeline: -**

Requirements are the starting cornerstone of the process. If the main
purpose is fraud detection, then process has to be in seconds. We will
require stream processing. If it was finance reporting, then we will
look at batch processing.

The right architecture is requirement dependent and is driven by
latency, scale, retention, consumer, compliance and recovery
expectations.

**Recovery & Replay-ability**

SLA and business criticality drive recovery requirements. The higher the
business impact, the more you design for failure:

- **Idempotency** --- replaying doesn\'t duplicate results

- **Checkpointing** --- know exactly where you left off

- **Dead letter queues** --- bad records don\'t silently disappear

> \"Design for breakage\"

**Source Pattern**

A.  **Database CDC** use for incremental changes OLTP; Risk schema
    drift; ordering, duplicate events

B.  **APIs** Saas, vendor or partner data; Risk Rate limit, pagination,
    auth expiration

C.  **Files** use with batch exports, SFTP, CSV, JSON; Risk partial
    uploads, corrupted files, duplicates

D.  **Event Streams** use for low-latency needs and telemetry; risk
    consumer lag, ordering, replay complexity

E.  **Schema Drift**

Unplanned source schema changes --- new fields, renamed columns, type
changes. Dangerous because it\'s silent: pipeline keeps running but
produces wrong or incomplete data.

Mitigation: schema validation at ingestion, schema registry, alerts on
change.

What do you think a dead letter queue has to do with schema drift?

Schema drift often creates DLQ events. Instead of breaking the whole
pipeline, send invalid events to DLQ.

**Core Pipeline Architecture**

A production pipeline separates concerns: ingestion → raw storage →
validation → transformation → serving, with monitoring across all
stages.

Separation reduces blast radius --- when one stage fails, others keep
running and recovery is isolated to the failure point.

> Design assumes failure. It\'s \"when\" a stage fails, not \"if.\"

### **Medallion Flow**

**Bronze** raw ingested data ***as received* -** Immutable relay source

**Silver** cleaned validate and joined ***Trusted -*** Trusted No bad
data Here

**Gold** Business-ready analytics data ***executive/ reporting layer
-*** Optimized consumer queries

**Reliability & Recovery**

Reliable pipelines treat failures, retries, duplicates, late data, dead
letter queues, and upstream changes as **normal operating conditions**,
not exceptions.

**Key principles:**

- **Idempotency** --- same operation runs multiple times, same result.
  No corruption.

- **Immutable storage** --- Bronze is untouched, always replayable

- **Deterministic transformations** --- same input always produces same
  output

- **Partitioned writes** --- overwrite a partition, not an entire table

- **Versioned logic** --- know exactly which rules produced which data

**Backfills** run separate from production and validate through Silver
before promoting to Gold.

> If your pipeline isn\'t idempotent, retries are dangerous. If Bronze
> isn\'t immutable, recovery is guesswork.

**Pipeline Recovery Checklist**

- **raw_storage**--- Immutable --- never modified after ingestion

- **writes**--- Idempotent --- retries produce no duplicates or
  corruption

- **retries**--- Limited retries with increasing wait time

- **failed_records**--- dead_letter_queue DLQ --- bad records isolated,
  not lost

- **Transformations** --- versioned --- know which logic produced which
  data

- **backfills**--- Partition-scoped --- reprocess only affected data,
  not full pipeline

- **Late_events** --- Watermark (bounded wait) or reconciliation
  (corrective reprocess)

**Quality Governance and security**

Data Quality checks and protects consumers from silent failures. Common
checks include freshness, completeness, validity, uniqueness,
consistency, schema compatibility and drift detection.

Governance makes data trustworthy across teams. Good design define
owners, lineage, retention, audit trails, access controls and contracts
between producers and consumers.

**Controls**

- **Freshness check** - Detect late or missing loads

- **Completeness check** - Catch missing partitions, regions or records

- **Schema Contract** - prevent unexpected undocumented producer changes

- **Lineage** - Trace impact from source to consumer

- **Least privilege** - Limit pipeline access to required resources

- **PII masking**--- protects sensitive data in analytical layers.

**Performance and Cost**

[Performance and cost are architectural concerns, not cleanup
tasks.]{.mark} Designers and architects have to bake in partitioning,
pruning, incremental processing, file sizing, shuffle reduction,
compaction, retention and storage tiering into the designs.

Full-Table reloads can work on small scale and experimentation; However
in enterprise scale it becomes cost prohibitive. Streaming sounds
elegant, but mostly wasteful if low latency is not needed. Always prefer
incremental and batch processing if possible since it is easier to
implement, manage and less costly. Small files hurt Query performance by
increasing metadata overhead and reducing scan efficiency by
segmentations - choose partitions wisely.

**Key design principles**

- **Partitioning** - Enables pruning - scan what you need

- **Incremental Processing** - process new data only- not full reloads

- **File size & compaction**- Small files kill query performance ---
  metadata overhead, fragmented scans

- **Shuffle reduction** - Expensive in distributed systems - minimize
  data movement.

- **Retention & Storage Tiering** - Hot -. Warm - cold .. archive as
  data ages.

**System Design Walkthrough --- Food Delivery Platform**

**Scenario** Design a pipeline supporting near real-time order tracking,
daily financial reporting, ML recommendations, historical analytics ---
at millions of daily events.

**Step 1 --- Clarify Before You Design** Always start here. Confirm
throughput, latency, regions, retention, recovery expectations, and who
the consumers are.

**Step 2 --- Ingestion by Source**

  ----------------- ------------- -------------------------
     **Source**      **Pattern**           **Why**

   Order database        CDC      Incremental changes from
                                            OLTP

    Driver mobile       Event       Low-latency tracking
       events         streaming   

    Payment data         API         Vendor/partner data

     Restaurant         File      Controlled batch exports
       updates        ingestion   
  ----------------- ------------- -------------------------

**Step 3 --- Medallion Layers**

- **Bronze** --- all raw payloads, immutable, untouched

- **Silver** --- deduplicate, normalize schema, validate, standardize
  timestamps, mask PII

- **Gold** --- operational dashboards, finance tables, ML feature
  datasets

**Step 4 --- Reliability Layer** Retries with backoff, DLQs for failed
records, watermarks for late events, replay support from Bronze, schema
contracts, freshness checks, lineage, runbooks.

**Closing Statement**

> Replay-ability and operational simplicity matter early --- reliability
> failures hurt the business faster than temporary scale limits.
>
> A strong design has three parts: clarify requirements, present
> architecture, explain failure recovery. Never draw a happy-path-only
> system. Interviewers listen for what breaks and how you recover.

**Q: When would you choose batch over streaming?**

*Choose batch when the business can tolerate higher latency and
operational simplicity matters more than real-time response. Batch is
usually easier to debug, cheaper to operate, and simpler to recover.
Streaming should be justified by clear low-latency business value.*

**Q: Why is idempotency critical in pipeline design?**

*Distributed systems retry work constantly. Without idempotent writes,
retries and replays can create duplicates, inflate metrics, or corrupt
downstream tables. Deterministic keys, MERGE operations, and
deduplication windows are common controls.*

**Q: How would you recover from corrupted transformation logic?**

*I would stop downstream publishing, identify the affected partitions or
time range, fix and version the transformation, then replay from
immutable raw storage into silver and gold. I would validate row counts,
quality rules, and consumer impact before releasing corrected outputs.*

**Q: What pipeline metrics would you monitor?**

*I would monitor freshness, latency, throughput, failure rate, queue
lag, data quality violations, row-count anomalies, and downstream SLA
impact. Logs help with debugging, but metrics and alerts are what detect
operational failure early.*

**Q: How do you handle late-arriving events?**

*For streaming, I would use event-time processing, watermarks, grace
windows, and reconciliation jobs. For batch, I would design
partition-aware reprocessing so late records can update the correct
business period safely.*

**Q: What separates a junior answer from a senior pipeline design
answer?**

*Junior answers focus on tools and happy-path movement. Senior answers
discuss replay-ability, idempotency, data contracts, observability,
incident response, governance, cost, and long-term maintainability. The
senior mindset is about how the system behaves under failure.*

**The Medallion Flow:-**

**Bronze coding**

Minimal processing:

- ingest data

- store raw/as-is

- add metadata

- partition correctly

- preserve replay source

"Land it safely."

**Silver coding**

Most engineering logic:

- clean

- validate

- deduplicate

- standardize schema

- handle nulls/types

- join/enrich

- apply business rules

- quarantine bad records

"Make it trusted."

**Gold coding**

Consumer-ready shaping:

- aggregates

- KPIs

- marts

- dashboards

- reporting tables

- ML feature tables

"Serve the business."

Correction:\
Gold is not just waiting. Gold is **curated output for consumers**.
