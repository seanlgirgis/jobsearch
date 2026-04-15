# Capital One Interview Skills Focus (Lead Data Engineer)

## Strengths to Lead With
- Python + SQL pipeline engineering at enterprise scale (6,000+ endpoints, automated ETL).
- AWS data platform experience: S3, Glue, Redshift, ECS/EC2.
- Forecasting/data science in production (Prophet, scikit-learn) tied to business outcomes.
- Strong ownership in ambiguous environments and hands-on IC mindset.

## Areas to Strengthen (Most Likely Probes)
- Streaming depth: Kafka concepts, partitions, consumer groups, delivery semantics.
- Distributed processing depth: Spark/PySpark performance patterns (shuffle, skew, joins).
- Architecture articulation: tradeoffs across batch vs streaming, warehouse vs lake.
- Senior IC engineering breadth: testing strategy, risk/security thinking, database choice rationale.
- Broader stack fluency for this JD: Java/Scala awareness, NoSQL patterns (Mongo/Cassandra), real-time use cases.

## What to Practice Before Interview Rounds
- 2-minute architecture walkthrough: `S3 -> Glue -> Redshift`, plus orchestration and monitoring.
- 1-minute answers for:
  - Why this role
  - Why Capital One
  - Why Lead DE over Lead/Senior Lead SWE
- Clear "gap but learning" statement for streaming:
  - "Stronger in batch/warehouse; actively ramping in event-driven/Kafka patterns."
- System-design framing:
  - Requirements -> scale/SLA -> data model -> pipeline pattern -> reliability/testing -> security/risk -> cost.

## Priority Study Order (From Discussion Notes)
1. Airflow
2. PySpark
3. AWS Step Functions
4. Databricks
5. dbt
6. Kinesis + deeper Kafka

## Interview Message to Reinforce
- You are a hands-on Lead Data Engineer who ships production data systems, not just tool familiarity.
- You can explain both implementation details and architecture decisions clearly.
