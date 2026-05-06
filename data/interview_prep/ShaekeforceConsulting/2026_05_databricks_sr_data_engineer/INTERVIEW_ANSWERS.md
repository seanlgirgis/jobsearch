# Interview Answers (Polished + Honest)

## Tell me about yourself.
I am a Python and SQL-focused data engineer with strong AWS experience building and supporting reliable data pipelines. A lot of my work has involved telemetry-style data, ETL transformations, validation checks, monitoring, and producing clean datasets for reporting and forecasting use cases. I am strongest in practical delivery: building pipelines that run consistently, are testable, and are easy to troubleshoot.

## What is your Databricks experience?
I have about one year of practical Databricks exposure and focused study, built on a stronger PySpark and AWS data engineering background. I am comfortable with Databricks notebooks, Spark DataFrame transformations, SQL workflows, Delta tables, and job-oriented pipeline patterns.
For hands-on practice, I use Databricks Free Edition via Google login (`sean.girgis@gmail.com`).

## Have you used Databricks in production?
My strongest production depth is in Python/AWS/PySpark pipeline engineering overall. On Databricks specifically, my experience is more recent and developing, so I present it as about one year of practical exposure rather than long-term platform ownership.

## Explain a data pipeline you built.
One representative pipeline ingested telemetry/event data, applied PySpark transformations, validated schema and key metrics, and published curated outputs for downstream analytics. I included quality gates such as null checks, row-count reconciliation, and threshold alerts, plus logging/monitoring for operational support. The goal was stable daily delivery with clear failure visibility and quick recovery.

## How do you ensure data quality?
I use layered controls:
- Input validation: schema, required fields, type checks.
- Transformation validation: row counts, uniqueness, null rates, range checks.
- Business-rule checks: key metric comparisons vs expected bounds.
- Operational monitoring: alerts, run logs, and failure triage playbooks.
- Testing: unit tests for transform logic and regression checks for critical outputs.

## What is your AWS experience?
I have hands-on AWS data engineering experience centered on S3-based data workflows plus Python-driven ETL processing and automation patterns. I am comfortable designing batch-oriented pipelines, organizing raw-to-curated data layers, and supporting reliable operational runs with monitoring and troubleshooting.
For personal AWS lab work, I use account email `sean.l.girgis@gmail.com`.

## How would you approach entity resolution / duplicate records?
I would start with deterministic normalization rules (name cleanup, casing, punctuation removal, standard formats), then build blocking keys to reduce comparison volume. Next, I would add probabilistic scoring across attributes (for example name similarity + email/phone/address signals), define match thresholds (auto-match, review, non-match), and continuously measure precision/recall with sampled validation.

## What is your compensation expectation?
For this contract scope, I am aligned with $85/hour on 1099, which is within the posted range.

## Are you eligible for Public Trust?
Yes. I am a U.S. citizen and eligible for Public Trust processing.

## Why are you interested in this role?
This role matches my strengths in Python, SQL, AWS data engineering, and reliable pipeline delivery, and it also gives me room to keep deepening Databricks in a practical environment. I like roles where data quality and operational reliability matter, and where I can contribute quickly while collaborating with a delivery team.
