# Talk Track

- Unbounded table: continuous incoming data view.
- Micro-batch: small recurring processing intervals.
- Checkpoint: persisted state/progress for recovery.
- Source and sink: where data comes from and where it lands.
- Trigger interval: controls processing frequency.
- Late data: delayed records requiring policy decisions.
- Schema drift: incoming shape changes needing controls.
- Monitoring: track lag, failures, throughput, and quality.

Safe wording:
I have practical exposure to Structured Streaming concepts and operational patterns, and my stronger foundation is Spark batch pipeline reliability.

## 60-Second Interview Explanation
Structured Streaming lets Spark process continuously arriving data in micro-batches with checkpoint-based recovery. You define source, transformations, sink, and trigger interval, then monitor lag, failures, and data quality. I am careful to position this as practical concept and design exposure, while my deeper production strength is reliable batch and Spark-style ETL operations.
