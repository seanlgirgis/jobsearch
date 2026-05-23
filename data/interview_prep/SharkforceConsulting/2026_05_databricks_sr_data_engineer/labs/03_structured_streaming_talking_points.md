# Structured Streaming Talking Points

## Honest Positioning
Use this framing: "I have working knowledge of Spark Structured Streaming concepts and pipeline design, and I apply the same reliability mindset I use in batch ETL."

## Core Terms
- Unbounded table: A conceptual table that keeps growing as new events arrive.
- Micro-batch: Default execution model where Spark processes small chunks at intervals.
- Checkpointing: Persisted state/progress metadata used for fault tolerance and exactly-once-style recovery patterns.
- Trigger interval: How often Spark launches a micro-batch (for example every 30 seconds).
- Sink: Destination for streaming output (Delta table, console, message system, etc.).
- Schema drift: Incoming structure changes over time; handle with schema governance/evolution strategy.
- Late data: Events arriving after expected event-time windows; handle with watermarking/window logic.
- Monitoring: Track throughput, latency, failure counts, checkpoint health, and data-quality metrics.

## 30-Second Explanation
Structured Streaming lets you write Spark transformations as if data were a table, while Spark continuously processes new records in micro-batches. You configure a source, transformations, trigger interval, checkpoint location, and sink. In production, reliability depends on checkpointing, handling late data, schema drift controls, and active monitoring.

## Safe Interview Soundbites
- "I focus on predictable recovery using checkpointing and clear sink semantics."
- "I treat streaming quality checks as first-class, not optional."
- "I can contribute quickly on streaming pipeline implementation while aligning to team standards for watermarking, schema handling, and monitoring."
