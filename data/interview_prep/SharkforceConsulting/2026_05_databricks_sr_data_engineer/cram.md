# cram.md

<a id="toc"></a>
## Table of Contents

### 03 Recruiter QA
- [03_01 1) Tell me about yourself.](#q-03_01)
- [03_02 2) Are you a U.S. citizen and eligible for Public Trust?](#q-03_02)
- [03_03 3) What is your compensation expectation?](#q-03_03)
- [03_04 4) What is your availability?](#q-03_04)
- [03_05 5) Why are you interested in this role?](#q-03_05)
- [03_06 6) How many years of data engineering experience do you have?](#q-03_06)
- [03_07 7) How many years of Python experience do you have?](#q-03_07)
- [03_08 8) What is your Databricks experience?](#q-03_08)
- [03_09 9) What is your AWS experience?](#q-03_09)
- [03_10 10) Tell me about a data pipeline you built.](#q-03_10)
- [03_11 11) Have you used Databricks in production?](#q-03_11)
- [03_12 12) What is your Spark Structured Streaming experience?](#q-03_12)
- [03_13 13) What is your Lambda experience?](#q-03_13)
- [03_14 14) How would you approach entity resolution and deduplication?](#q-03_14)
- [03_15 15) How do you ensure data quality and testing?](#q-03_15)

### 04 Client Technical QA
- [04_01 Q01. Python Pipeline Design](#q-04_01)
- [04_02 Q02. SQL Optimization Approach](#q-04_02)
- [04_03 Q03. ETL vs ELT Decisioning](#q-04_03)
- [04_04 Q04. Batch Pipeline Design](#q-04_04)
- [04_05 Q05. Schema and Data Modeling](#q-04_05)
- [04_06 Q06. Large Files and Partition Handling](#q-04_06)
- [04_07 Q07. Troubleshooting Slow or Failing Pipelines](#q-04_07)
- [04_08 Q08. S3 Landing Zone Design](#q-04_08)
- [04_09 Q09. AWS Glue and PySpark Pattern](#q-04_09)
- [04_10 Q10. Redshift Analytical Pattern](#q-04_10)
- [04_11 Q11. Lambda in Data Pipelines](#q-04_11)
- [04_12 Q12. CloudWatch and Monitoring](#q-04_12)
- [04_13 Q13. IAM and Security Awareness](#q-04_13)
- [04_14 Q14. What Is Databricks?](#q-04_14)
- [04_15 Q15. Spark DataFrames in Practice](#q-04_15)
- [04_16 Q16. Delta Lake and Delta Tables](#q-04_16)
- [04_17 Q17. Medallion Architecture](#q-04_17)
- [04_18 Q18. Jobs and Workflows](#q-04_18)
- [04_19 Q19. Databricks vs AWS Glue](#q-04_19)
- [04_20 Q20. Structured Streaming Basics](#q-04_20)
- [04_21 Q21. Unity Catalog and Governance Basics](#q-04_21)
- [04_22 Q22. Data Quality Framework](#q-04_22)
- [04_23 Q23. Schema, Null, and Duplicate Checks](#q-04_23)
- [04_24 Q24. Reconciliation and Row Counts](#q-04_24)
- [04_25 Q25. Unit Testing for Python and Spark](#q-04_25)
- [04_26 Q26. Monitoring and Alerting](#q-04_26)
- [04_27 Q27. Incident Response and Operational Support](#q-04_27)
- [04_28 Q28. Entity Resolution Approach](#q-04_28)
- [04_29 Q29. Deterministic vs Probabilistic Matching](#q-04_29)
- [04_30 Q30. False Positives and False Negatives](#q-04_30)
- [04_31 Q31. Feature Engineering Support for ML](#q-04_31)
- [04_32 Q32. Operationalizing ML Outputs](#q-04_32)
- [04_33 Q33. Explaining Technical Concepts to Non-Technical Stakeholders](#q-04_33)
- [04_34 Q34. Working with Data Scientists and Architects](#q-04_34)
- [04_35 Q35. Agile Delivery, Jira, Confluence, and Production Mindset](#q-04_35)
- [04_36 Q36. Supporting AI/ML Teams as a Data Engineer](#q-04_36)
- [04_37 Q37. How would you connect Databricks with AWS S3?](#q-04_37)
- [04_38 Q38. How would you implement data quality checks in Databricks?](#q-04_38)
- [04_39 Top 10 questions to rehearse first](#q-04_39)
- [04_40 Top 5 weak areas to defend carefully](#q-04_40)
- [04_41 Top 5 stories to reuse](#q-04_41)

### 05 Databricks Crash Guide - Interview Answers
- [05_01 3 sentence version](#q-05_01)
- [05_02 60 second version](#q-05_02)
- [05_03 If asked: How deep are you?](#q-05_03)
- [05_04 If asked: Have you used it in production?](#q-05_04)
- [05_05 Workspace](#q-05_05)
- [05_06 Notebook](#q-05_06)
- [05_07 Cluster](#q-05_07)
- [05_08 Serverless compute](#q-05_08)
- [05_09 SQL warehouse](#q-05_09)
- [05_10 Spark DataFrame](#q-05_10)
- [05_11 Delta table](#q-05_11)
- [05_12 Delta Lake](#q-05_12)
- [05_13 DBFS / cloud object storage concept](#q-05_13)
- [05_14 Metastore](#q-05_14)
- [05_15 Unity Catalog](#q-05_15)
- [05_16 Jobs](#q-05_16)
- [05_17 Workflows](#q-05_17)
- [05_18 DLT / Delta Live Tables](#q-05_18)
- [05_19 Medallion architecture](#q-05_19)
- [05_20 Auto Loader](#q-05_20)
- [05_21 Structured Streaming](#q-05_21)
- [05_22 Checkpointing](#q-05_22)
- [05_23 MLflow](#q-05_23)
- [05_24 Q1. What is Databricks?](#q-05_24)
- [05_25 Q2. What is your Databricks experience?](#q-05_25)
- [05_26 Q3. Have you used Databricks in production?](#q-05_26)
- [05_27 Q4. What is Delta Lake?](#q-05_27)
- [05_28 Q5. What is a Delta table?](#q-05_28)
- [05_29 Q6. What is medallion architecture?](#q-05_29)
- [05_30 Q7. How do Jobs and Workflows work?](#q-05_30)
- [05_31 Q8. What is Structured Streaming?](#q-05_31)
- [05_32 Q9. How would you connect Databricks with AWS S3?](#q-05_32)
- [05_33 Q10. How would you implement data quality checks in Databricks?](#q-05_33)
- [05_34 Q11. How would you support ML or feature engineering pipelines in Databricks?](#q-05_34)
- [05_35 Q12. What would you need to ramp on quickly in this role?](#q-05_35)

## 03 Recruiter QA

<a id="q-03_01"></a>
### 03_01 1) Tell me about yourself.

Question:
Tell me about yourself.

Short Answer:
I’m a senior data engineer with strong production depth in Python, SQL, AWS, Spark-style ETL, and large-scale data pipeline operations. I also have practical Databricks exposure built on that Spark and data engineering foundation.

At Citi, I built and supported telemetry and capacity data pipelines at enterprise scale, including ingestion from thousands of endpoints and tens of thousands of metrics. My focus has been reliable delivery: ingestion, transformation, quality checks, monitoring, and clean handoff to analytics, forecasting, and business teams.

Expanded Answer:
I bring 20+ years in enterprise IT, with my recent years focused on senior data engineering work. From 2017 to 2025 at Citi, I built and supported Python and SQL data pipelines for telemetry and capacity use cases, including high-volume ingestion, transformation, validation, and reporting support. I have strong AWS and PySpark-style ETL foundations, and I am comfortable owning day-to-day pipeline reliability, data quality, and operational follow-through. I work well with both technical and business stakeholders, and I keep communication clear and practical.

Interview Notes:
Use short answer first in quick recruiter screens. Use expanded answer if they ask for background detail. Guardrail: keep it focused on data engineering and avoid drifting into unrelated legacy tools.

Risk Level: LOW

[Back to TOC](#toc)

<a id="q-03_02"></a>
### 03_02 2) Are you a U.S. citizen and eligible for Public Trust?

Question:
Are you a U.S. citizen and eligible for Public Trust?

Short Answer:
Yes. I’m a U.S. citizen and I’m eligible to go through the Public Trust clearance process.

Expanded Answer:
Yes. I’m a U.S. citizen and I’m eligible to go through the Public Trust clearance process. I understand that this is a hard requirement for the role, and I can complete the process based on client timelines.

Interview Notes:
Always use short answer unless they ask about timing. Guardrail: keep it direct and do not add extra legal detail unless requested.

Risk Level: LOW

[Back to TOC](#toc)

<a id="q-03_03"></a>
### 03_03 3) What is your compensation expectation?

Question:
What is your compensation expectation?

Short Answer:
Based on the role requirements and the 1099 structure, I’m targeting around $85 per hour. I’m flexible within the posted range depending on the full scope, duration, and expectations.

Expanded Answer:
Based on the role requirements and the 1099 structure, I’m targeting around $85 per hour. I’m flexible within the posted range depending on the full scope, duration, and expectations. Since this is a senior data engineering role with strong Python, AWS, SQL, and pipeline ownership needs, that range feels aligned and practical.

Interview Notes:
Use short answer in most cases. Use expanded answer if recruiter pushes for negotiation context. Guardrail: avoid jumping below range too early.

Risk Level: LOW

[Back to TOC](#toc)

<a id="q-03_04"></a>
### 03_04 4) What is your availability?

Question:
What is your availability?

Short Answer:
I can move quickly after interview completion and onboarding steps. I am available for remote work and can align to standard U.S. business hours.

Expanded Answer:
I can move quickly after final interview and onboarding steps are complete. I am comfortable in remote settings, I can align with standard U.S. business hours, and I can support cross-time-zone coordination when needed. My focus at the start is to learn current pipelines quickly, stabilize priority workflows, and provide predictable delivery.

Interview Notes:
Use short answer unless they ask for start-date planning. Guardrail: do not commit to a hard date before confirming constraints.

Risk Level: LOW

[Back to TOC](#toc)

<a id="q-03_05"></a>
### 03_05 5) Why are you interested in this role?

Question:
Why are you interested in this role?

Short Answer:
It matches my strongest skills in Python, SQL, AWS, and scalable data pipeline delivery. I also like that it emphasizes data quality, entity resolution, and support for AI/ML data workflows.

Expanded Answer:
I’m interested because the role is closely aligned to what I do best in production: Python, SQL, AWS data engineering, and reliable ETL operations. I also like that quality, validation, and monitoring are core expectations, not side tasks. The Databricks requirement is also a good fit for me right now because I have practical exposure and focused study there, and I can apply my stronger Spark and pipeline foundations to contribute quickly.

Interview Notes:
Use short answer for pace. Use expanded answer when recruiter asks why this specific role. Guardrail: avoid sounding like Databricks is your deepest production area.

Risk Level: LOW

## 2. Role Fit

[Back to TOC](#toc)

<a id="q-03_06"></a>
### 03_06 6) How many years of data engineering experience do you have?

Question:
How many years of data engineering experience do you have?

Short Answer:
I have 20+ years in enterprise IT, with strong recent senior data engineering focus. At Citi from 2017 to 2025, I was directly focused on data pipelines, telemetry processing, quality, and reporting support.

Expanded Answer:
I have 20+ years of enterprise IT experience overall, and my recent years are strongly data engineering focused. In my Citi role from late 2017 through 2025, I worked on Python and SQL pipeline delivery, telemetry ingestion and transformation, data quality controls, and operational reliability. I also supported forecasting and analytics workflows with stable data handoff and monitoring.

Interview Notes:
Use short answer first, then add Citi timeline if asked. Guardrail: keep timeline clear and factual.

Risk Level: LOW

[Back to TOC](#toc)

<a id="q-03_07"></a>
### 03_07 7) How many years of Python experience do you have?

Question:
How many years of Python experience do you have?

Short Answer:
Around 12 years of practical Python use. I use it for ETL pipelines, validation logic, automation, and operational support.

Expanded Answer:
I have about 12 years of practical Python experience. Most of that is in data engineering workflows such as ingestion, transformation, validation checks, quality gates, and monitoring support. In recent years, Python has been central to telemetry pipelines, forecasting support workloads, and reporting-oriented data preparation.

Interview Notes:
Use short answer unless they ask for use-case detail. Guardrail: avoid inflating years beyond stated number.

Risk Level: LOW

[Back to TOC](#toc)

<a id="q-03_08"></a>
### 03_08 8) What is your Databricks experience?

Question:
What is your Databricks experience?

Short Answer:
I have about one year of practical exposure and focused study in Databricks. My stronger production foundation is Python, SQL, AWS, and PySpark-style ETL.

I’m comfortable with the core Databricks data engineering concepts: notebooks, Spark DataFrames, SQL, Delta tables, jobs and workflows, and lakehouse patterns. I would not present myself as a long-time Databricks platform administrator, but I can build on my Spark and data pipeline background quickly.

Expanded Answer:
I position my Databricks experience as about 1 year of practical exposure and focused study. My strongest production foundation is Python, SQL, AWS, and PySpark-style pipeline engineering, which transfers well into Databricks workflows. I am comfortable with notebook-based development, Spark DataFrame transformations, SQL usage, Delta table concepts, jobs and workflows, and lakehouse patterns like medallion-style layering. I do not position myself as a long-time Databricks platform administrator.

Interview Notes:
Use short answer first to stay precise. Use expanded answer when recruiter needs confidence on transferability. Guardrail: explicitly avoid claiming deep admin ownership.

Risk Level: MEDIUM

[Back to TOC](#toc)

<a id="q-03_09"></a>
### 03_09 9) What is your AWS experience?

Question:
What is your AWS experience?

Short Answer:
I have strong AWS data engineering experience, especially with S3, Glue, Redshift, and serverless architecture patterns. I have used AWS services to support scalable ingestion, ETL/ELT, data quality, and operational monitoring.

Expanded Answer:
My AWS background is strong and practical for this role. I have worked with S3-centered data flows, Glue and Redshift patterns, and serverless architecture approaches in support of data pipelines and reporting workloads. My focus is building reliable ingestion and transformation paths, enforcing quality checks, and keeping data operations observable and supportable. That lines up well with the role’s need for scalable pipelines and operational discipline.

Interview Notes:
Use short answer in initial screen. Expand with specific services if asked. Guardrail: do not claim deep ownership of services not listed in source truth.

Risk Level: LOW

[Back to TOC](#toc)

<a id="q-03_10"></a>
### 03_10 10) Tell me about a data pipeline you built.

Question:
Tell me about a data pipeline you built.

Short Answer:
At Citi, I supported Python/Pandas telemetry pipelines ingesting data from 6,000+ endpoints into AWS data layers. The pipeline included transformation, validation, monitoring, and downstream reporting and forecasting support.

Expanded Answer:
One strong example is a telemetry pipeline at Citi. We ingested high-volume endpoint data from more than 6,000 sources, processed it through Python-based transformation steps, and applied validation checks before downstream use. The outputs fed reporting and capacity forecasting workflows, so consistency and timeliness were important. I focused on reliable runs, quality controls, and operational monitoring so issues could be identified quickly and resolved with minimal disruption.

Interview Notes:
Use short answer for quick fit checks. Use expanded answer if recruiter asks for a concrete story. Guardrail: avoid unsupported hard metrics beyond the 6,000+ endpoint fact.

Risk Level: LOW

## 3. Risk Defense

[Back to TOC](#toc)

<a id="q-03_11"></a>
### 03_11 11) Have you used Databricks in production?

Question:
Have you used Databricks in production?

Short Answer:
My production experience is stronger on the Python, SQL, AWS, and PySpark-style pipeline side. Databricks is newer for me as a managed platform, but the engineering patterns it supports are familiar: ingestion, transformation, validation, monitoring, orchestration, and reliable handoff to analytics or ML teams.

Expanded Answer:
My production experience is stronger on the Python, SQL, AWS, and PySpark-style pipeline side. Databricks is newer for me as a managed platform, but the engineering patterns it supports are familiar: ingestion, transformation, validation, monitoring, orchestration, and reliable handoff to analytics or ML teams. So I am transparent that I am not claiming long-term Databricks platform ownership, while still being confident in my ability to deliver pipeline outcomes quickly.

Interview Notes:
Use short answer exactly as written when this comes up. Use expanded answer if they push on risk. Guardrail: never imply multi-year Databricks ownership.

Risk Level: HIGH

[Back to TOC](#toc)

<a id="q-03_12"></a>
### 03_12 12) What is your Spark Structured Streaming experience?

Question:
What is your Spark Structured Streaming experience?

Short Answer:
I have practical exposure to Structured Streaming concepts and patterns, including micro-batch processing, checkpointing, and sink design. I present this as working capability built on strong Spark foundations, not heavy long-term streaming platform ownership.

Expanded Answer:
I have practical exposure to Structured Streaming and understand core concepts like unbounded data, micro-batch execution, checkpointing for recovery, trigger intervals, and sink behavior. I can discuss how to design reliable streaming data paths and how to monitor them for lag and failures. I stay honest that my strongest production background is broader batch and near-real-time pipeline engineering rather than deep multi-year ownership of large streaming platforms.

Interview Notes:
Use short answer first. Expand only if they ask. Guardrail: avoid claiming large-scale Kafka or deep streaming platform ownership.

Risk Level: HIGH

[Back to TOC](#toc)

<a id="q-03_13"></a>
### 03_13 13) What is your Lambda experience?

Question:
What is your Lambda experience?

Short Answer:
I have practical Lambda experience in AWS serverless architecture patterns for event-driven automation around data workflows. I focus on maintainable Python logic, integration reliability, and monitoring.

Expanded Answer:
I have used Lambda as part of AWS serverless architecture patterns to support data workflows, especially event-driven and integration-oriented tasks. My approach is to keep functions simple, testable, and observable, with clear logging and predictable behavior under retries. I do not frame myself as a deep Lambda-only specialist, but as a data engineer who uses Lambda where it is the right operational fit.

Interview Notes:
Use short answer for recruiter pace. Use expanded answer when they probe depth. Guardrail: do not overstate deep Lambda platform specialization.

Risk Level: HIGH

[Back to TOC](#toc)

<a id="q-03_14"></a>
### 03_14 14) How would you approach entity resolution and deduplication?

Question:
How would you approach entity resolution and deduplication?

Short Answer:
I start by defining what counts as a duplicate using business rules, then profile source data and normalize key fields. I use deterministic match keys first, then probabilistic matching, and I review false positives and false negatives with a feedback loop.

Expanded Answer:
I treat entity resolution as a business and data problem together. First, define duplicate criteria with stakeholders because match rules depend on business context. Next, profile the data and normalize fields like names, emails, phone numbers, and addresses. I start with deterministic keys for high-confidence matches, then apply probabilistic matching for ambiguous cases. After that, I review false positives and false negatives, tune thresholds, and maintain a feedback loop so matching quality improves over time.

Interview Notes:
Use short answer first. Use expanded answer when recruiter asks how practical your approach is. Guardrail: avoid claiming specialized research-level matching systems unless asked and supported.

Risk Level: MEDIUM

[Back to TOC](#toc)

<a id="q-03_15"></a>
### 03_15 15) How do you ensure data quality and testing?

Question:
How do you ensure data quality and testing?

Short Answer:
I use schema checks, null checks, duplicate checks, row counts, and reconciliation at each pipeline stage. I add automated tests, monitoring, alerting, and operational support so issues are detected and resolved quickly.

Expanded Answer:
I build quality into the pipeline from the start. That includes schema checks, null checks, duplicate checks, row-count controls, and source-to-target reconciliation. I add automated tests for Python and Spark logic, plus validation tests for expected outputs and edge cases. In production, I rely on monitoring and alerting so failures or drifts are visible quickly, and I pair that with practical pipeline operational support so incidents are triaged and corrected with clear runbook steps.

Interview Notes:
Use short answer in most recruiter calls. Use expanded answer when they ask how hands-on you are with reliability. Guardrail: do not claim perfect quality outcomes, focus on controls and response.

Risk Level: MEDIUM

## Tonight Priority: Memorize These 7
1. Tell me about yourself.
2. Are you a U.S. citizen and eligible for Public Trust?
3. What is your compensation expectation?
4. What is your Databricks experience?
5. Have you used Databricks in production?
6. What is your AWS experience?
7. How do you ensure data quality and testing?

## Questions to Ask the Recruiter

Do not answer "Nope" when asked if you have questions. Always ask at least one.

Option 1:
- Yes, thank you. Is this expected to go to a client technical round, and if so, what areas should I prepare to discuss in more depth?

Option 2:
- Yes. What characteristics or behaviors would make someone highly successful in this role beyond simply meeting the listed requirements?

For tomorrow, ask these two:
1. Is this expected to go to a client technical round, and if so, what areas should I prepare to discuss in more depth?
2. What characteristics or behaviors would make someone highly successful in this role beyond simply meeting the listed requirements?

## Additional Recruiter Fit Question

Question:
Why should we send you to the client?

Polished Answer:
Because I can contribute immediately in the core areas this role needs most: Python, SQL, AWS, and Spark-style data pipeline delivery, with strong data quality and operational reliability.

I’m also transparent about Databricks being newer for me, with practical exposure built on those foundations. That creates low risk in execution and clear upside as I ramp into your client’s specific Databricks environment.

Shorter Recruiter Version:
Because I match the core needs: Python, SQL, AWS, Spark-style data pipelines, data quality, and operational reliability. I’m honest about Databricks being newer for me, but it builds directly on my Spark and data engineering foundation, so I can ramp quickly in the client environment.

[Back to TOC](#toc)

## 04 Client Technical QA

<a id="q-04_01"></a>
### 04_01 Q01. Python Pipeline Design

Question:
How do you design a Python data pipeline for reliability and scale?

Best Answer:
I design pipelines as clear stages: ingest, validate, transform, publish, and monitor. I keep each stage modular so failures are isolated and easier to recover. In production, reliability comes from idempotent writes, strong logging, data quality checks, and clear runbook steps.

Deepening Points:
- Stage boundaries make troubleshooting faster.
- Idempotency prevents duplicate data during retries.
- Quality checks are built in, not added later.

Sean Story Anchor:
Citi telemetry pipeline from 6,000+ endpoints.

Risk / Guardrail:
Do not claim specific throughput numbers unless documented.

[Back to TOC](#toc)

<a id="q-04_02"></a>
### 04_02 Q02. SQL Optimization Approach

Question:
How do you optimize SQL used in data pipelines?

Best Answer:
I start with query plans and data access patterns, then reduce unnecessary scans and expensive joins. I prefer clean CTE structure, selective filters early, and stable join keys. I also align SQL design with table layout and partition strategy so runtime stays predictable.

Deepening Points:
- Push filters early to shrink data volume.
- Validate join cardinality before production runs.
- Use practical explain-plan review before tuning.

Sean Story Anchor:
Citi reporting and warehouse-oriented SQL workloads.

Risk / Guardrail:
Avoid claiming engine-specific tuning tricks unless directly used.

[Back to TOC](#toc)

<a id="q-04_03"></a>
### 04_03 Q03. ETL vs ELT Decisioning

Question:
When do you choose ETL versus ELT?

Best Answer:
I choose based on where transformation is most reliable and efficient. ETL is useful when data must be standardized before landing in analytics stores. ELT is useful when platform compute can handle transformations with better flexibility and lineage.

Deepening Points:
- Early cleansing helps when source quality is inconsistent.
- ELT can speed iteration for analytics teams.
- Governance and cost can change the choice.

Sean Story Anchor:
AWS S3/Glue/Redshift migration pattern.

Risk / Guardrail:
Do not present ETL or ELT as always better. Frame as context-driven.

[Back to TOC](#toc)

<a id="q-04_04"></a>
### 04_04 Q04. Batch Pipeline Design

Question:
How do you design robust batch pipelines?

Best Answer:
I define clear input windows, deterministic transformations, and repeatable outputs. Every batch run includes validation checks, reconciliation, and operational signals so we know if data is complete and correct. I also design backfill paths because real systems need safe reruns.

Deepening Points:
- Deterministic logic supports reproducibility.
- Backfill strategy is part of design, not afterthought.
- Reconciliation is key for trust.

Sean Story Anchor:
Citi telemetry and capacity reporting workflows.

Risk / Guardrail:
Avoid claiming real-time ownership when discussing batch patterns.

[Back to TOC](#toc)

<a id="q-04_05"></a>
### 04_05 Q05. Schema and Data Modeling

Question:
How do you approach schema design and data modeling?

Best Answer:
I start with business questions, then define entities, keys, and grain carefully. I use dimensional modeling patterns where they improve reporting performance and clarity. I keep schema evolution controlled so downstream teams are not surprised by breaking changes.

Deepening Points:
- Correct grain prevents aggregation errors.
- Surrogate and business keys both matter.
- Versioned schema changes reduce downstream breakage.

Sean Story Anchor:
Data warehouse and dimensional modeling background.

Risk / Guardrail:
Do not claim ownership of enterprise-wide governance programs unless true.

[Back to TOC](#toc)

<a id="q-04_06"></a>
### 04_06 Q06. Large Files and Partition Handling

Question:
How do you handle large files and partitions in pipelines?

Best Answer:
I control file and partition strategy based on access patterns and processing cost. I avoid both over-partitioning and very large single partitions, and I validate downstream query behavior before finalizing layout. The goal is balanced performance for ingest and consumption.

Deepening Points:
- Partition by high-value query dimensions.
- Repartition/compact as data shape changes.
- Validate with representative production-like data.

Sean Story Anchor:
Large-scale telemetry processing with PySpark-style ETL.

Risk / Guardrail:
Avoid naming platform-specific advanced tuning settings unless directly used.

[Back to TOC](#toc)

<a id="q-04_07"></a>
### 04_07 Q07. Troubleshooting Slow or Failing Pipelines

Question:
How do you troubleshoot a slow or failing pipeline?

Best Answer:
I separate the issue into data, code, and platform signals. First I confirm where latency or failure starts, then I isolate the stage and validate inputs, transformation logic, and resource behavior. I document root cause and prevention actions so the same incident does not repeat.

Deepening Points:
- Use logs, metrics, and run metadata together.
- Reproduce with a smaller controlled slice when possible.
- Close with preventive change and runbook update.

Sean Story Anchor:
Operational support and observability-heavy background.

Risk / Guardrail:
Do not overstate formal SRE ownership. Emphasize practical incident response.

## 2. AWS Data Engineering

[Back to TOC](#toc)

<a id="q-04_08"></a>
### 04_08 Q08. S3 Landing Zone Design

Question:
How do you design an S3 landing zone for data pipelines?

Best Answer:
I separate raw, refined, and curated layers with consistent naming and partition conventions. I keep source lineage clear and make sure each dataset has ownership and retention expectations. This supports reliable ingestion, replay, and downstream analytics consumption.

Deepening Points:
- Separate environments and data tiers clearly.
- Keep naming standards predictable.
- Preserve lineage metadata from ingest.

Sean Story Anchor:
AWS S3-centered pipeline architecture at Citi.

Risk / Guardrail:
Do not claim enterprise cloud governance ownership unless documented.

[Back to TOC](#toc)

<a id="q-04_09"></a>
### 04_09 Q09. AWS Glue and PySpark Pattern

Question:
How have you used AWS Glue with PySpark-style workloads?

Best Answer:
I have used Glue-oriented patterns to run transformation workflows over S3 data with Spark-style processing. The value is managed execution with repeatable ETL behavior and integration into broader AWS data flows. I focus on stable transformations, validation checkpoints, and reliable publish steps.

Deepening Points:
- Glue works well with S3-centered ETL layers.
- Spark-style transforms support scale and flexibility.
- Validation gates are part of every run.

Sean Story Anchor:
AWS S3/Glue/Redshift migration pattern.

Risk / Guardrail:
Avoid claiming niche Glue internals if not directly used.

[Back to TOC](#toc)

<a id="q-04_10"></a>
### 04_10 Q10. Redshift Analytical Pattern

Question:
How do you use Redshift in an analytics pipeline?

Best Answer:
I treat Redshift as a serving layer for curated, analysis-ready data. Pipeline design focuses on clean model structure, reliable load cadence, and query performance for reporting users. I align transformations so business metrics are consistent across dashboards.

Deepening Points:
- Curated load quality matters more than raw volume.
- Model clarity improves analyst productivity.
- Consistent metric definitions reduce reporting drift.

Sean Story Anchor:
Citi reporting and analytics support with Redshift patterns.

Risk / Guardrail:
Do not claim deep Redshift admin specialization unless true.

[Back to TOC](#toc)

<a id="q-04_11"></a>
### 04_11 Q11. Lambda in Data Pipelines

Question:
How do you use Lambda in data engineering workflows?

Best Answer:
I use Lambda in serverless architecture patterns for event-driven steps and lightweight control actions around pipelines. I keep Lambda logic focused, testable, and observable, rather than placing heavy transformations there. It is a good fit for automation glue between services.

Deepening Points:
- Best for event triggers and orchestration helpers.
- Keep functions small and explicit.
- Build retries and error handling intentionally.

Sean Story Anchor:
AWS serverless architecture patterns in pipeline support.

Risk / Guardrail:
Do not claim deep Lambda platform ownership.

[Back to TOC](#toc)

<a id="q-04_12"></a>
### 04_12 Q12. CloudWatch and Monitoring

Question:
What do you monitor in AWS data pipelines?

Best Answer:
I monitor run success, latency, freshness, data quality indicators, and error patterns. Alerts should be actionable, not noisy, and tied to ownership. I also use dashboards so teams can see pipeline health quickly.

Deepening Points:
- Monitor both technical and data-quality signals.
- Alert thresholds should map to business impact.
- Trend views help prevent recurring incidents.

Sean Story Anchor:
Telemetry monitoring and dashboarding background.

Risk / Guardrail:
Avoid claiming ownership of every monitoring platform in the organization.

[Back to TOC](#toc)

<a id="q-04_13"></a>
### 04_13 Q13. IAM and Security Awareness

Question:
How do you approach IAM and security in data pipelines?

Best Answer:
I apply least-privilege access and separate duties across environments. I make sure service roles are scoped to what each pipeline needs and validate access paths during deployment. Security controls should support delivery without creating hidden operational risk.

Deepening Points:
- Least privilege is the baseline.
- Separate dev, test, and production access patterns.
- Review role scope as pipelines evolve.

Sean Story Anchor:
Enterprise AWS delivery with operational reliability focus.

Risk / Guardrail:
Do not claim to be a security architect. Position as strong engineering security hygiene.

## 3. Databricks / Spark / Delta

[Back to TOC](#toc)

<a id="q-04_14"></a>
### 04_14 Q14. What Is Databricks?

Question:
How do you describe Databricks to a client team?

Best Answer:
I describe it as a managed Spark platform for building data and analytics pipelines with Python and SQL. It provides notebook development, job orchestration, and lakehouse table patterns. My experience is practical exposure and focused study built on stronger PySpark and AWS foundations.

Deepening Points:
- Managed compute reduces operational overhead.
- Strong fit for Spark-based ETL and analytics.
- Workflow and Delta features support reliability.

Sean Story Anchor:
Databricks transition preparation plus strong PySpark base.

Risk / Guardrail:
Do not claim long production Databricks ownership.

[Back to TOC](#toc)

<a id="q-04_15"></a>
### 04_15 Q15. Spark DataFrames in Practice

Question:
How do you use Spark DataFrames in pipeline development?

Best Answer:
I use DataFrames for scalable transformation steps such as joins, aggregations, standardization, and quality checks. I keep logic modular and testable, then validate results against expected business rules. This mirrors how I approached large telemetry ETL patterns.

Deepening Points:
- DataFrames support clear transformation chains.
- Validate schema and record-level behavior.
- Design with downstream consumption in mind.

Sean Story Anchor:
PySpark-style ETL and large telemetry processing.

Risk / Guardrail:
Avoid claiming Databricks-specific optimization depth beyond practical exposure.

[Back to TOC](#toc)

<a id="q-04_16"></a>
### 04_16 Q16. Delta Lake and Delta Tables

Question:
Why use Delta Lake and Delta tables?

Best Answer:
Delta Lake is a storage layer that brings database-like reliability to data lake files, usually Parquet files. It uses a transaction log to support reliable writes, schema enforcement, time travel, and MERGE or upsert patterns.

The practical value is that it helps prevent a data lake from becoming messy or inconsistent. If a job fails, you have better protection against partial or unreliable writes. You can also query previous versions for auditing, recovery, or debugging.

For data engineering, Delta Lake is useful because it supports bronze, silver, and gold pipeline layers where raw data can be cleaned, validated, and prepared for analytics or ML use cases.

Deepening Points:
- ACID improves trust in table updates.
- Schema enforcement reduces silent data drift.
- Versioning supports auditability and rollback patterns.

Sean Story Anchor:
Databricks focused study and ETL reliability mindset.

Risk / Guardrail:
Do not imply years of enterprise Delta administration.

[Back to TOC](#toc)

<a id="q-04_17"></a>
### 04_17 Q17. Medallion Architecture

Question:
How do you apply medallion architecture?

Best Answer:
Medallion architecture is a layered data design: bronze, silver, and gold.

Bronze preserves the raw source data as-is. It is useful for replay, auditability, and recovery.

Silver is where data becomes trusted. You clean, validate, normalize, deduplicate, join, and apply protections like masking if needed.

Gold is business-ready data. It has business logic, aggregations, and optimized structures for reporting, analytics, dashboards, or ML consumption.

The simple way I remember it is: bronze preserves truth, silver builds trust, and gold delivers business value.

Deepening Points:
- Bronze preserves raw lineage.
- Silver applies normalization and quality checks.
- Gold aligns with reporting and feature consumers.

Sean Story Anchor:
AWS layered pipeline experience mapped to lakehouse patterns.

Risk / Guardrail:
Frame as studied and practically understood pattern, not long platform ownership.

[Back to TOC](#toc)

<a id="q-04_18"></a>
### 04_18 Q18. Jobs and Workflows

Question:
How do Jobs and Workflows improve data engineering delivery?

Best Answer:
Databricks Jobs and Workflows are used to orchestrate repeatable data pipeline runs. A job can run a notebook, Python script, SQL task, or other task, and a workflow can connect multiple tasks with dependencies.

The value is scheduling, retries, parameters, alerts, and run visibility. For example, a workflow might load raw data, transform it into a silver Delta table, run data quality checks, then publish a gold table for analytics. That reduces manual execution risk and gives the team better operational control.

Deepening Points:
- Dependency control avoids out-of-order runs.
- Retry behavior improves resilience.
- Run history supports incident triage.

Sean Story Anchor:
Operational reliability and production support background.

Risk / Guardrail:
Do not claim advanced Databricks admin or enterprise platform operations.

[Back to TOC](#toc)

<a id="q-04_19"></a>
### 04_19 Q19. Databricks vs AWS Glue

Question:
How do you compare Databricks and AWS Glue for ETL workloads?

Best Answer:
Both can support Spark-style transformations, but tradeoffs depend on team workflow, governance model, and operational preference. Glue can fit native AWS-centric managed ETL patterns, while Databricks can provide integrated notebook and lakehouse workflows. I choose based on delivery fit, reliability, and team operating model.

Deepening Points:
- Selection depends on context, not brand preference.
- Existing platform standards matter.
- Reliability and support model should drive choice.

Sean Story Anchor:
AWS Glue strength plus Databricks practical ramping.

Risk / Guardrail:
Do not frame as deep expert in all platform internals.

[Back to TOC](#toc)

<a id="q-04_20"></a>
### 04_20 Q20. Structured Streaming Basics

Question:
How would you explain Spark Structured Streaming?

Best Answer:
I explain it as processing incoming data as an unbounded table, usually in micro-batches, with checkpointing for recovery and state tracking. Operationally, you tune trigger intervals, monitor lag and failures, and validate output quality at the sink. I present this as practical knowledge, not heavy long-term production streaming ownership.

Deepening Points:
- Core concepts: source, transform, sink, checkpoint.
- Operational focus: latency, throughput, lag, failures.
- Quality checks still apply in streaming paths.

Sean Story Anchor:
Spark foundation and reliability-first engineering approach.

Risk / Guardrail:
Do not claim heavy production Structured Streaming ownership.

[Back to TOC](#toc)

<a id="q-04_21"></a>
### 04_21 Q21. Unity Catalog and Governance Basics

Question:
What is your understanding of Unity Catalog and data governance?

Best Answer:
Unity Catalog provides centralized governance for tables, permissions, and metadata organization. I see it as a way to enforce consistent access control and improve lineage visibility across teams. My grounding is from practical study and mapping governance concepts to enterprise data practices.

Deepening Points:
- Centralized permissions reduce drift across workspaces.
- Clear catalog/schema structure improves discoverability.
- Lineage helps audits and impact analysis.

Sean Story Anchor:
Enterprise data controls mindset plus Databricks study.

Risk / Guardrail:
Do not claim hands-on platform admin ownership unless confirmed.

## 4. Data Quality / Testing / Operations

[Back to TOC](#toc)

<a id="q-04_22"></a>
### 04_22 Q22. Data Quality Framework

Question:
What is your data quality framework for production pipelines?

Best Answer:
I use a layered framework: schema validation, completeness checks, duplicate detection, business rule checks, and reconciliation. Each layer has pass/fail criteria and ownership for remediation. This keeps quality measurable and operationally actionable.

Deepening Points:
- Define quality gates per pipeline stage.
- Track defects by type and recurrence.
- Tie checks to business-critical fields first.

Sean Story Anchor:
Citi telemetry validation and operational support patterns.

Risk / Guardrail:
Do not claim zero-defect outcomes. Emphasize controls and response.

[Back to TOC](#toc)

<a id="q-04_23"></a>
### 04_23 Q23. Schema, Null, and Duplicate Checks

Question:
How do you implement schema, null, and duplicate checks?

Best Answer:
I codify expected schema and required fields, then enforce thresholds for nulls and duplicates. I separate hard-fail conditions from warning conditions so teams can respond appropriately. I also store check results for trend analysis.

Deepening Points:
- Hard-fail for critical key violations.
- Warning tiers for non-critical drifts.
- Persisted results support continuous improvement.

Sean Story Anchor:
Data quality and reliability work across telemetry pipelines.

Risk / Guardrail:
Avoid claiming proprietary frameworks unless they exist.

[Back to TOC](#toc)

<a id="q-04_24"></a>
### 04_24 Q24. Reconciliation and Row Counts

Question:
How do you handle reconciliation between source and target datasets?

Best Answer:
I validate row counts and key aggregates across pipeline boundaries and investigate mismatches before publish. Reconciliation includes expected filters and business logic context, not just raw counts. This is one of the fastest ways to catch silent data issues.

Deepening Points:
- Compare both counts and control totals.
- Document expected variance rules.
- Block downstream publish on unresolved critical gaps.

Sean Story Anchor:
Reporting and telemetry pipeline handoff discipline.

Risk / Guardrail:
Do not overstate perfect reconciliation in every scenario.

[Back to TOC](#toc)

<a id="q-04_25"></a>
### 04_25 Q25. Unit Testing for Python and Spark

Question:
How do you unit test Python and Spark pipeline code?

Best Answer:
I test transformation functions with known inputs and expected outputs, then add edge-case coverage for nulls, type changes, and duplicates. For Spark-style logic, I validate schema and deterministic results using representative fixtures. I use pytest at a practical level to keep tests readable and repeatable.

Deepening Points:
- Test business rules, not just syntax.
- Include negative cases and bad data inputs.
- Keep tests fast enough for regular execution.

Sean Story Anchor:
Practical/intermediate pytest use in pipeline workflows.

Risk / Guardrail:
Do not claim full-scale QA automation ownership if not true.

[Back to TOC](#toc)

<a id="q-04_26"></a>
### 04_26 Q26. Monitoring and Alerting

Question:
What do you monitor and alert on in production pipelines?

Best Answer:
I monitor freshness, latency, failure rates, and key quality metrics tied to business impact. Alerts should route to owners with enough context to act quickly. I also use dashboards to track trends and recurring risk areas.

Deepening Points:
- Operational and quality signals both matter.
- Alert fatigue is reduced with tuned thresholds.
- Trend visibility helps prevent repeat incidents.

Sean Story Anchor:
Telemetry monitoring and dashboard background.

Risk / Guardrail:
Do not imply sole ownership of enterprise observability strategy.

[Back to TOC](#toc)

<a id="q-04_27"></a>
### 04_27 Q27. Incident Response and Operational Support

Question:
How do you handle pipeline incidents in production?

Best Answer:
Short version:

I triage impact first, contain the issue, restore safely, then fix root cause. After that, I improve monitoring, validation, and documentation so the same issue does not repeat or go unnoticed.

Long version:

For a production pipeline failure, I triage first: identify what failed, what data is affected, what downstream reports or systems are impacted, and whether the issue is still active.

Then I contain the impact and restore safely. That may mean pausing downstream consumption, rerunning a failed step, replaying from a checkpoint or raw source, or applying a controlled short-term fix.

After service is stable, I focus on root cause and prevention: fix the underlying issue, improve monitoring or validation, document the incident, and add checks so the same failure does not repeat or go unnoticed.

Deepening Points:
- Separate immediate recovery from long-term fix.
- Communicate status and risk clearly.
- Close incidents with preventive controls.

Sean Story Anchor:
Operational reliability and observability-heavy career history.

Risk / Guardrail:
Avoid claiming formal incident commander role unless explicitly true.

## 5. Entity Resolution / Matching / AI-ML Support

[Back to TOC](#toc)

<a id="q-04_28"></a>
### 04_28 Q28. Entity Resolution Approach

Question:
How would you approach entity resolution in this role?

Best Answer:
I start with a clear business definition of what counts as a duplicate, then profile source data quality. Next I standardize and normalize fields, apply deterministic match keys first, and then probabilistic scoring for ambiguous pairs. I tune thresholds with human review and maintain a feedback loop to improve match quality over time.

Deepening Points:
- Business rules define the target behavior.
- Deterministic first, probabilistic second.
- Continuous quality monitoring is required.

Sean Story Anchor:
Data quality and matching-style pipeline design mindset.

Risk / Guardrail:
Do not claim specialized research-level identity graph ownership.

[Back to TOC](#toc)

<a id="q-04_29"></a>
### 04_29 Q29. Deterministic vs Probabilistic Matching

Question:
How do you explain deterministic versus probabilistic matching?

Best Answer:
Deterministic matching uses exact or rule-based keys for high-confidence links. Probabilistic matching scores similarity across multiple attributes for likely matches where exact keys are missing. In practice, good systems use both with clear threshold bands.

Deepening Points:
- Deterministic rules reduce ambiguity early.
- Probabilistic scoring captures fuzzy real-world variation.
- Threshold bands support auto-match and review queues.

Sean Story Anchor:
Practical matching framework aligned with data quality controls.

Risk / Guardrail:
Avoid claiming patented or advanced proprietary scoring algorithms.

[Back to TOC](#toc)

<a id="q-04_30"></a>
### 04_30 Q30. False Positives and False Negatives

Question:
How do you manage false positives and false negatives in matching?

Best Answer:
I monitor both error types because each has business cost. I tune thresholds with labeled samples, add review queues for uncertain cases, and feed adjudication results back into rules and weights. Match quality should be monitored as an ongoing operational metric.

Deepening Points:
- Precision and recall tradeoff must be explicit.
- Ambiguous bands need human review.
- Feedback loops improve model and rule quality.

Sean Story Anchor:
Quality-gate and validation mindset from enterprise pipelines.

Risk / Guardrail:
Do not claim perfect match accuracy.

[Back to TOC](#toc)

<a id="q-04_31"></a>
### 04_31 Q31. Feature Engineering Support for ML

Question:
How do you support feature engineering for ML teams?

Best Answer:
I focus on delivering clean, versioned, and well-documented feature datasets with reliable refresh cycles. I align transformations with business definitions and preserve lineage so model teams can trust inputs. My role is to make feature pipelines stable and repeatable.

Deepening Points:
- Feature consistency matters across training and scoring.
- Lineage and documentation reduce model risk.
- Data freshness and completeness are monitored.

Sean Story Anchor:
Capacity forecasting support using Prophet and scikit-learn workflows.

Risk / Guardrail:
Do not position as lead data scientist unless asked and accurate.

[Back to TOC](#toc)

<a id="q-04_32"></a>
### 04_32 Q32. Operationalizing ML Outputs

Question:
How do you operationalize ML outputs into downstream pipelines?

Best Answer:
I treat ML outputs as governed data products with schema checks, versioning, and monitored publish steps. I add validation and reconciliation before downstream consumption to avoid propagating bad predictions. The goal is reliable integration, not just model execution.

Deepening Points:
- Validate output schema and ranges.
- Track model output freshness and drift indicators.
- Define rollback or fallback path for bad runs.

Sean Story Anchor:
Forecasting and reporting pipeline support in enterprise operations.

Risk / Guardrail:
Do not claim ownership of full MLOps platform engineering.

## 6. Behavioral / Delivery / Client Communication

[Back to TOC](#toc)

<a id="q-04_33"></a>
### 04_33 Q33. Explaining Technical Concepts to Non-Technical Stakeholders

Question:
How do you explain complex data issues to non-technical stakeholders?

Best Answer:
I translate technical details into business impact, decision risk, and next actions. I keep language simple, use concrete examples, and provide clear timelines for mitigation. Stakeholders need clarity and confidence, not jargon.

Deepening Points:
- Lead with impact, then cause, then fix.
- Keep status updates short and regular.
- Document decisions and assumptions clearly.

Sean Story Anchor:
Citi reporting and cross-functional operational communication.

Risk / Guardrail:
Avoid overly deep technical detail unless requested.

[Back to TOC](#toc)

<a id="q-04_34"></a>
### 04_34 Q34. Working with Data Scientists and Architects

Question:
How do you collaborate with data scientists and architects?

Best Answer:
I align early on data contracts, quality expectations, and delivery cadence. With data scientists, I focus on reliable feature and inference data paths. With architects, I focus on design tradeoffs and operational supportability.

Deepening Points:
- Define interfaces and ownership up front.
- Review assumptions before implementation.
- Keep design pragmatic and operable.

Sean Story Anchor:
Forecasting support and enterprise architecture collaboration patterns.

Risk / Guardrail:
Do not claim final architectural authority for all systems.

[Back to TOC](#toc)

<a id="q-04_35"></a>
### 04_35 Q35. Agile Delivery, Jira, Confluence, and Production Mindset

Question:
How do you deliver in Agile while maintaining production reliability?

Best Answer:
I break work into small, testable increments and track execution in Jira with clear acceptance criteria. I document technical decisions, runbooks, and handoffs in Confluence so support is consistent. I always balance sprint speed with long-term pipeline stability.

Deepening Points:
- Small increments reduce deployment risk.
- Documentation supports team continuity.
- Reliability is part of definition of done.

Sean Story Anchor:
Long-running enterprise delivery with operational support focus.

Risk / Guardrail:
Avoid saying process is perfect. Emphasize continuous improvement.

[Back to TOC](#toc)

<a id="q-04_36"></a>
### 04_36 Q36. Supporting AI/ML Teams as a Data Engineer

![AI/ML Support Reference](licensed-image.jpg)

Question:
How do you support AI/ML teams as a data engineer?

Best Answer:
As a data engineer, I support AI and ML teams by making sure the data pipeline produces reliable features, not just raw data. Usually that means building trusted silver and gold layers where features are calculated consistently.

One important point is keeping training and inference aligned. The logic used to create features for model training should match the logic used when the model runs on new data. I also watch for data leakage, where training accidentally uses information that would not have been available in the real world at prediction time.

I also think about point-in-time correctness, data drift, monitoring, and feedback loops. Once the actual outcome becomes available, that ground truth should flow back into the pipeline so the model can be evaluated and improved.

Deepening Points:
- Keep training and inference feature logic aligned.
- Prevent leakage and validate point-in-time correctness.
- Monitor drift and feed outcomes back for model evaluation.

Sean Story Anchor:
Capacity forecasting and ML pipeline support.

Risk / Guardrail:
Position this as data pipeline and feature reliability support, not lead model scientist ownership.

[Back to TOC](#toc)

<a id="q-04_37"></a>
### 04_37 Q37. How would you connect Databricks with AWS S3?

Question:
How would you connect Databricks with AWS S3?

Best Answer:
Short version: I would use IAM role-based access, preferably through Unity Catalog storage credentials and external locations. AWS controls the S3 permissions, Databricks assumes the role securely, and the external location maps the S3 path into the Databricks governance model.

Long version: A common secure pattern is to connect Databricks to S3 through Unity Catalog using an IAM role, rather than hardcoded access keys.

At a high level, AWS has an IAM policy that grants access to the target S3 bucket, then an IAM role with a trust relationship that allows Databricks to assume that role. In Databricks, you create a storage credential using the role ARN, then define an external location that maps to the S3 path.

The value is security and governance: Databricks can read and write to S3 through controlled permissions, without passing around long-lived secrets. After that, pipelines can read raw data from S3, transform it with Spark, and write managed or external Delta tables depending on the design.

Deepening Points:
- Use IAM role assumption, not hardcoded access keys.
- Use Unity Catalog storage credentials and external locations for governed access.
- Keep S3 access controlled and auditable while supporting Spark-to-Delta pipeline flows.

Sean Story Anchor:
AWS S3/Glue/Redshift migration pattern plus Databricks governance ramp.

Risk / Guardrail:
Do not claim long production ownership of Unity Catalog administration. Frame this as secure architecture knowledge and practical implementation approach.

[Back to TOC](#toc)

<a id="q-04_38"></a>
### 04_38 Q38. How would you implement data quality checks in Databricks?

Question:
How would you implement data quality checks in Databricks?

Best Answer:
Short -> I would put quality checks directly into the Databricks workflow: schema checks, null checks, duplicate checks, row counts, reconciliation, and business-rule validation before data moves from bronze to silver to gold.

Long-> I would implement data quality checks at each layer of the pipeline: schema validation, completeness checks, null checks, duplicate detection, business rule checks, and reconciliation.

In Databricks, those checks can run inside notebooks or jobs as part of the workflow. For example, before promoting data from bronze to silver or silver to gold, I would validate expected columns, row counts, duplicate keys, and business rules. Each check should have pass/fail criteria, logging, and ownership for remediation.

The goal is to make quality measurable and operationally actionable, not just something people inspect manually after the fact.

Deepening Points:
- Enforce quality gates at each promotion step (bronze to silver to gold).
- Define pass/fail criteria with clear logging and ownership.
- Make checks actionable through workflow integration, not manual review.

Sean Story Anchor:
Data Quality and Validation Framework.

Risk / Guardrail:
Do not claim perfect data quality outcomes. Emphasize measurable controls and fast remediation.
## Client Round Priority List

[Back to TOC](#toc)

<a id="q-04_39"></a>
### 04_39 Top 10 questions to rehearse first

1. Q01. Python Pipeline Design
2. Q08. S3 Landing Zone Design
3. Q09. AWS Glue and PySpark Pattern
4. Q10. Redshift Analytical Pattern
5. Q14. What Is Databricks?
6. Q16. Delta Lake and Delta Tables
7. Q20. Structured Streaming Basics
8. Q22. Data Quality Framework
9. Q28. Entity Resolution Approach
10. Q35. Agile Delivery, Jira, Confluence, and Production Mindset

[Back to TOC](#toc)

<a id="q-04_40"></a>
### 04_40 Top 5 weak areas to defend carefully

1. Q14. What Is Databricks?
2. Q18. Jobs and Workflows
3. Q20. Structured Streaming Basics
4. Q21. Unity Catalog and Governance Basics
5. Q11. Lambda in Data Pipelines

[Back to TOC](#toc)

<a id="q-04_41"></a>
### 04_41 Top 5 stories to reuse

1. Citi telemetry pipeline (6,000+ endpoints)
2. AWS S3/Glue/Redshift migration pattern
3. Capacity forecasting support (Prophet and scikit-learn)
4. Data quality and validation framework
5. Operational monitoring and incident support background

[Back to TOC](#toc)

## 05 Databricks Crash Guide Interview Answers

<a id="q-05_01"></a>
### 05_01 3 sentence version

My Databricks experience is about 1 year of practical exposure and focused study. My deeper production experience is Python, SQL, AWS, and PySpark-style ETL. Databricks is newer for me as a platform, but it maps naturally to those foundations.

[Back to TOC](#toc)

<a id="q-05_02"></a>
### 05_02 60 second version

I position Databricks as a practical and growing skill with about 1 year of exposure and focused study. I am comfortable with notebooks, Spark DataFrames, SQL, Delta tables, jobs/workflows, and lakehouse concepts like medallion architecture. Where I bring deeper production strength is Python, SQL, AWS, PySpark-style ETL, data quality, monitoring, and operational reliability. That foundation transfers well into Databricks delivery, so I can contribute quickly while continuing to ramp platform-specific depth.

[Back to TOC](#toc)

<a id="q-05_03"></a>
### 05_03 If asked: How deep are you?

I would describe my Databricks depth as practical and developing, not long-tenure platform ownership. I am confident in core engineering workflows and strongest in transferable Spark/AWS pipeline foundations.

[Back to TOC](#toc)

<a id="q-05_04"></a>
### 05_04 If asked: Have you used it in production?

My deeper production experience is Python, SQL, AWS, and PySpark-style ETL. Databricks is newer for me as a platform, but the engineering patterns it supports are familiar: ingestion, transformation, validation, monitoring, orchestration, and reliable handoff to analytics or ML teams.

## 3. Core Databricks Concepts

[Back to TOC](#toc)

<a id="q-05_05"></a>
### 05_05 Workspace

What it is:
Shared environment for notebooks, jobs, data assets, and permissions.
Why it matters:
Central place for team collaboration and controlled access.
Sean-safe wording:
I am familiar with workspace organization from practical Databricks exposure.

[Back to TOC](#toc)

<a id="q-05_06"></a>
### 05_06 Notebook

What it is:
Interactive document for Python, SQL, and markdown.
Why it matters:
Speeds development, debugging, and technical walkthroughs.
Sean-safe wording:
I am comfortable building and explaining pipeline logic in notebooks.

[Back to TOC](#toc)

<a id="q-05_07"></a>
### 05_07 Cluster

What it is:
Spark compute resources configured for jobs or notebook sessions.
Why it matters:
Compute sizing and config affect runtime and cost.
Sean-safe wording:
I understand cluster-backed execution and how it supports Spark workloads.

[Back to TOC](#toc)

<a id="q-05_08"></a>
### 05_08 Serverless compute

What it is:
Managed compute option with less setup overhead.
Why it matters:
Faster startup and simpler operations for many workloads.
Sean-safe wording:
I am familiar with when serverless is useful versus custom cluster control.

[Back to TOC](#toc)

<a id="q-05_09"></a>
### 05_09 SQL warehouse

What it is:
Compute endpoint optimized for SQL analytics.
Why it matters:
Supports BI/reporting use cases with governed SQL access.
Sean-safe wording:
It aligns well with my SQL and reporting foundation.

[Back to TOC](#toc)

<a id="q-05_10"></a>
### 05_10 Spark DataFrame

What it is:
Distributed table-like API for transformations and aggregations.
Why it matters:
Core abstraction for scalable ETL/ELT processing.
Sean-safe wording:
This maps directly to my PySpark-style ETL background.

[Back to TOC](#toc)

<a id="q-05_11"></a>
### 05_11 Delta table

What it is:
Table stored in Delta format on cloud object storage.
Why it matters:
Reliable writes, updates, and schema controls.
Sean-safe wording:
I am comfortable with Delta table concepts and practical usage patterns.

[Back to TOC](#toc)

<a id="q-05_12"></a>
### 05_12 Delta Lake

What it is:
Table layer over Parquet with transaction log and reliability features.
Why it matters:
Improves consistency, auditability, and safe updates.
Sean-safe wording:
I have focused study and practical exposure to Delta Lake patterns.

[Back to TOC](#toc)

<a id="q-05_13"></a>
### 05_13 DBFS / cloud object storage concept

What it is:
Databricks access layer and paths over storage like S3.
Why it matters:
Pipelines read and write cloud data through consistent interfaces.
Sean-safe wording:
I map this to my existing S3 landing and curated data patterns.

[Back to TOC](#toc)

<a id="q-05_14"></a>
### 05_14 Metastore

What it is:
Catalog of table metadata such as schema and location.
Why it matters:
Enables discoverability and shared table access.
Sean-safe wording:
I understand metastore concepts from SQL and data warehouse experience.

[Back to TOC](#toc)

<a id="q-05_15"></a>
### 05_15 Unity Catalog

What it is:
Centralized governance for catalog/schema/table permissions and lineage.
Why it matters:
Improves access control and audit readiness.
Sean-safe wording:
I am familiar with Unity Catalog concepts and governance benefits.

[Back to TOC](#toc)

<a id="q-05_16"></a>
### 05_16 Jobs

What it is:
Scheduled or triggered task execution in Databricks.
Why it matters:
Turns notebook logic into repeatable production runs.
Sean-safe wording:
This fits my orchestration and operational reliability mindset.

[Back to TOC](#toc)

<a id="q-05_17"></a>
### 05_17 Workflows

What it is:
Task orchestration with dependencies, retries, and run history.
Why it matters:
Supports controlled multi-step pipeline execution.
Sean-safe wording:
I am comfortable with workflow concepts built on orchestration experience.

[Back to TOC](#toc)

<a id="q-05_18"></a>
### 05_18 DLT / Delta Live Tables

What it is:
Managed framework for declarative ETL pipelines on Delta tables.
Why it matters:
Adds built-in quality expectations and monitoring patterns.
Sean-safe wording:
I have studied DLT concepts and how they support reliable data pipelines.

[Back to TOC](#toc)

<a id="q-05_19"></a>
### 05_19 Medallion architecture

What it is:
Layered model: bronze raw, silver cleaned, gold business-ready.
Why it matters:
Improves lineage, quality control, and serving consistency.
Sean-safe wording:
It maps naturally to raw-to-curated patterns I used in AWS pipelines.

[Back to TOC](#toc)

<a id="q-05_20"></a>
### 05_20 Auto Loader

What it is:
Databricks feature for incremental file ingestion from cloud storage.
Why it matters:
Reduces manual file tracking and scales ingestion handling.
Sean-safe wording:
I am familiar with Auto Loader concepts from Databricks focused study.

[Back to TOC](#toc)

<a id="q-05_21"></a>
### 05_21 Structured Streaming

What it is:
Spark model for processing continuous data as an unbounded table.
Why it matters:
Supports near-real-time pipelines with checkpoint-based recovery.
Sean-safe wording:
I can explain and design around concepts while continuing to build deeper production depth.

[Back to TOC](#toc)

<a id="q-05_22"></a>
### 05_22 Checkpointing

What it is:
Persisted state/progress used by streaming jobs for recovery.
Why it matters:
Enables fault tolerance and consistent continuation.
Sean-safe wording:
Checkpointing is central to reliable streaming operations.

[Back to TOC](#toc)

<a id="q-05_23"></a>
### 05_23 MLflow

What it is:
Tooling for experiment tracking and model lifecycle support.
Why it matters:
Improves reproducibility and model handoff discipline.
Sean-safe wording:
I focus on how data pipelines support ML workflows and tracked outputs.

## 4. Databricks Maps to Sean's Existing Strengths
| Databricks concept | Sean's existing foundation | Safe interview wording |
|---|---|---|
| Spark DataFrames | PySpark-style ETL | This is directly aligned with my Spark-style transformation background. |
| Delta tables | Parquet/data lake/data quality foundation | I use Delta concepts as an extension of reliable lake-based data engineering. |
| Jobs/Workflows | Airflow/orchestration/pipeline scheduling foundation | Databricks workflows map to orchestration patterns I already use. |
| Unity Catalog | Governance/security/compliance awareness | I understand governance goals and permission control concepts. |
| Structured Streaming | Batch pipeline foundation plus streaming concepts | I understand core streaming concepts and apply reliability-first thinking. |
| SQL warehouse | SQL/data warehouse/reporting foundation | This aligns with my SQL and reporting delivery experience. |
| S3 integration | AWS S3 landing zone experience | I map Databricks processing on top of S3 patterns I already know well. |
| Monitoring jobs | Telemetry/operational monitoring background | Monitoring and operational support are core strengths in my production work. |

## 5. Delta Lake in Plain English
Delta Lake is built on Parquet files plus a transaction log that tracks changes. The transaction log adds ACID-like reliability for data updates and helps avoid inconsistent reads. Delta supports schema enforcement, version history (time travel), and merge/upsert patterns for incremental pipelines. It fits medallion architecture where bronze/silver/gold layers each have controlled quality. In practice, this improves data quality because changes are auditable, schema drift is better managed, and corrections are safer.

Short answer Sean can say:
Delta Lake is a reliability layer on top of Parquet that adds transaction logging, schema controls, and safer upserts. It helps teams run scalable pipelines with better data quality and auditability.

## 6. Medallion Architecture
Bronze:
Raw landed data with minimal transformation.

Silver:
Cleaned, standardized, validated data ready for broader reuse.

Gold:
Business-ready tables for reporting, analytics, and ML features.

How it maps to raw -> validated -> reporting:
Bronze is raw intake, silver is validated/refined, gold is consumption-ready output.

How Sean can relate it to Citi pipelines:
This is very similar to how I approached telemetry pipelines: ingest raw signals, apply validation and transformation layers, then publish trusted outputs for reporting and forecasting.

Plain-text diagram:
`Source files/events -> Bronze (raw) -> Silver (clean + validated) -> Gold (reporting/features)`

## 7. Structured Streaming Without Overclaiming
Structured Streaming concepts:
- Unbounded table: continuously arriving data viewed as a growing table.
- Micro-batches: processing happens in small repeated intervals.
- Checkpointing: progress/state persisted for recovery.
- Trigger interval: how often batches run.
- Source: input stream location.
- Sink: output destination such as Delta table.
- Late data: delayed events handled by time logic and policy.
- Schema drift: source structure changes that require controlled handling.
- Monitoring failed batches: watch failures, lag, and data quality indicators.

Safe answer for recruiter:
I have practical exposure to Structured Streaming concepts like micro-batches, checkpointing, and sink design, and I apply a reliability-first approach based on my stronger pipeline operations background.

Deeper answer for client:
I frame Structured Streaming as a controlled pipeline with source, transformation logic, checkpointing, and sink guarantees. I pay attention to trigger interval tuning, late data handling, schema drift safeguards, and monitoring failed batches. My strongest production depth is broader batch and Spark-style ETL, and I am continuing to deepen streaming-specific production practice.

Guardrail against overclaiming:
Do not claim heavy multi-year production ownership of complex streaming platforms.

## 8. Databricks + AWS Pattern
Role-relevant pattern:
S3 raw landing zone
-> Databricks notebook/job
-> Spark transformations
-> Delta silver table
-> quality checks
-> Delta gold table
-> SQL/reporting/ML features
-> monitoring and alerts

Plain-text architecture diagram:
`S3 Raw -> Databricks Job -> Spark Transform -> Delta Silver -> Validation -> Delta Gold -> SQL/BI/ML -> Alerts`

How this maps to Sean's stronger AWS foundation:
This pattern is consistent with my stronger AWS delivery background using S3/Glue/Redshift-style layers. Databricks provides a managed Spark and Delta workflow on top of similar raw-to-curated data engineering principles.

## 9. Entity Resolution Mini-Pattern in Databricks
Conceptual flow:
1. Ingest records into a bronze Delta table.
2. Standardize field formats.
3. Normalize names, addresses, and IDs.
4. Create deterministic match keys first.
5. Add probabilistic scoring for ambiguous records.
6. Tune thresholds for match/non-match/review.
7. Track false positives and false negatives.
8. Write matched outputs to silver/gold Delta tables.
9. Monitor match quality over time and update rules.

Simple PySpark-style pseudocode:
```python
# bronze -> standardized
df = spark.table("bronze_customers")
std = standardize_columns(df)
norm = normalize_identity_fields(std)

# deterministic first
det = norm.withColumn("match_key", build_match_key(norm))

# probabilistic for unmatched or ambiguous
candidates = build_candidate_pairs(det)
scored = score_similarity(candidates)  # name/address/id features

# thresholds
matched = scored.filter("score >= 0.92")
review = scored.filter("score >= 0.75 AND score < 0.92")

# quality tracking
metrics = compute_match_metrics(matched, review)  # fp/fn trends over time

# write outputs
matched.write.format("delta").mode("overwrite").saveAsTable("gold_customer_matches")
review.write.format("delta").mode("overwrite").saveAsTable("silver_match_review_queue")
```

## 10. Interview Answers

[Back to TOC](#toc)

<a id="q-05_24"></a>
### 05_24 Q1. What is Databricks?

Short Answer:
Databricks is a managed Spark platform for building data pipelines and analytics workflows with notebooks, SQL, jobs/workflows, and Delta Lake.

Expanded Answer:
I describe Databricks as a managed Spark environment where data teams build ETL/ELT pipelines using Python and SQL, usually on cloud storage like S3. It supports notebook development, scheduled workflows, and Delta table patterns that improve reliability and governance. It is commonly used by data engineering and ML teams for scalable transformation and data delivery.

Guardrail:
Do not claim platform admin ownership.

[Back to TOC](#toc)

<a id="q-05_25"></a>
### 05_25 Q2. What is your Databricks experience?

Short Answer:
I have about 1 year of practical exposure and focused study in Databricks, built on stronger Python, SQL, AWS, and PySpark-style ETL foundations.

Expanded Answer:
I position my Databricks experience as practical and growing, around 1 year of exposure and study. I am comfortable with notebooks, Spark DataFrames, SQL, Delta tables, jobs/workflows, and lakehouse concepts like medallion architecture. My deeper production strength is broader AWS/Python/PySpark pipeline reliability, which transfers well into Databricks.

Guardrail:
Do not frame as long-tenure Databricks owner.

[Back to TOC](#toc)

<a id="q-05_26"></a>
### 05_26 Q3. Have you used Databricks in production?

Short Answer:
My deeper production experience is Python, SQL, AWS, and PySpark-style ETL. Databricks is newer for me as a managed platform, but the pipeline patterns are familiar.

Expanded Answer:
I stay transparent that my strongest production depth is on the Python, SQL, AWS, and PySpark side. Databricks is newer for me, but the core patterns are the same ones I have delivered: ingestion, transformation, validation, monitoring, orchestration, and reliable handoff to analytics and ML consumers. So I can contribute quickly while continuing to build platform-specific depth.

Guardrail:
Do not imply multi-year Databricks production ownership.

[Back to TOC](#toc)

<a id="q-05_27"></a>
### 05_27 Q4. What is Delta Lake?

Short Answer:
Delta Lake is a reliability layer on top of Parquet that adds transaction logging, schema controls, and versioned operations.

Expanded Answer:
Delta Lake combines Parquet storage with a transaction log so updates are consistent and auditable. It supports schema enforcement, time travel, and safer incremental operations such as merge/upsert. For data engineering, it helps reduce pipeline fragility and improves data quality management.

Guardrail:
Do not claim deep internals expertise.

[Back to TOC](#toc)

<a id="q-05_28"></a>
### 05_28 Q5. What is a Delta table?

Short Answer:
A Delta table is table data stored in Delta format, usually on cloud object storage, with reliable write/update behavior.

Expanded Answer:
A Delta table is how you store and manage data with Delta features enabled. It is practical for production ETL because append, overwrite, and merge patterns are more controlled than plain file-based approaches. It also supports better governance and reproducibility over time.

Guardrail:
Do not overstate enterprise-wide Delta administration.

[Back to TOC](#toc)

<a id="q-05_29"></a>
### 05_29 Q6. What is medallion architecture?

Short Answer:
It is a layered data model: bronze raw, silver cleaned/validated, gold business-ready.

Expanded Answer:
Medallion architecture organizes data quality progression across layers. Bronze keeps source fidelity, silver applies normalization and validation, and gold serves analytics or feature consumers with trusted outputs. It maps directly to raw-to-curated practices used in enterprise pipelines.

Guardrail:
Present as practical pattern knowledge, not proprietary framework ownership.

[Back to TOC](#toc)

<a id="q-05_30"></a>
### 05_30 Q7. How do Jobs and Workflows work?

Short Answer:
Jobs and Workflows schedule and orchestrate tasks with dependencies, retries, and run tracking.

Expanded Answer:
You define tasks such as notebooks or scripts, connect them with dependency order, and set schedule or trigger behavior. Workflows provide retry handling and run history, which supports reliable operations and faster incident triage. It turns development logic into repeatable delivery.

Guardrail:
Do not claim deep Databricks platform operations management.

[Back to TOC](#toc)

<a id="q-05_31"></a>
### 05_31 Q8. What is Structured Streaming?

Short Answer:
Structured Streaming is Spark's model for processing continuous data using unbounded-table semantics, micro-batches, checkpoints, and sinks.

Expanded Answer:
I explain Structured Streaming as a framework where incoming data is processed continuously with repeated micro-batches and recovery via checkpointing. In operations, you tune trigger intervals, handle late data, watch schema drift, and monitor failed batches and lag. I present this as practical understanding built on strong pipeline reliability experience.

Guardrail:
Do not claim heavy multi-year production streaming ownership.

[Back to TOC](#toc)

<a id="q-05_32"></a>
### 05_32 Q9. How would you connect Databricks with AWS S3?

Short Answer:
I would land raw data in S3, process it in Databricks with Spark, write Delta tables, and publish curated outputs for SQL/reporting/ML use.

Expanded Answer:
A practical pattern is S3 raw landing, then Databricks jobs for transformation and validation, then Delta silver/gold outputs for consumption. This mirrors the AWS data pipeline discipline I already use with S3/Glue/Redshift. Databricks adds managed Spark execution and Delta table reliability on top of that foundation.

Guardrail:
Do not claim you led full-scale Databricks migrations.

[Back to TOC](#toc)

<a id="q-05_33"></a>
### 05_33 Q10. How would you implement data quality checks in Databricks?

Short Answer:
I would implement schema, null, duplicate, row-count, and reconciliation checks at each layer, with monitoring and alerting tied to job runs.

Expanded Answer:
I apply quality gates from bronze to silver to gold, including schema enforcement, required-field checks, duplicate detection, threshold checks, and source-target reconciliation. Failures are logged with actionable context and alerts so operators can respond quickly. The key is to make quality checks part of pipeline design, not post-processing.

Guardrail:
Do not claim perfect quality outcomes. Emphasize controls and rapid response.

[Back to TOC](#toc)

<a id="q-05_34"></a>
### 05_34 Q11. How would you support ML or feature engineering pipelines in Databricks?

Short Answer:
I focus on delivering clean, versioned, and reliable feature datasets with predictable refresh and validation.

Expanded Answer:
I support ML teams by building stable data preparation flows, enforcing quality checks, and documenting lineage for feature sets. Databricks can serve as the transformation and delivery layer to produce consistent inputs for training or inference consumers. My strength is reliable data pipeline operations that make ML workflows more dependable.

Guardrail:
Do not position as lead model scientist unless explicitly true.

[Back to TOC](#toc)

<a id="q-05_35"></a>
### 05_35 Q12. What would you need to ramp on quickly in this role?

Short Answer:
I would ramp first on the team's Databricks conventions, governance setup, and production workflow standards.

Expanded Answer:
My first ramp priorities would be how the team structures workspaces and workflows, their Delta and quality standards, and governance patterns such as catalog/permissions. Since my foundation in Python, AWS, SQL, and Spark-style ETL is strong, I can contribute quickly while deepening platform-specific practices like Unity Catalog and advanced Databricks operations.

Guardrail:
Avoid sounding uncertain. Frame ramping as targeted and fast.

## 11. Do Not Say List
Bad:
I have deep production Databricks administration experience.
Better:
My Databricks exposure is practical and growing, built on stronger Spark/Python/AWS pipeline foundations.

Bad:
I led large Databricks platform migrations.
Better:
I have focused study and practical exposure, and I map Databricks patterns to strong AWS/PySpark pipeline experience.

Bad:
I am an expert in heavy production Structured Streaming at scale.
Better:
I understand Structured Streaming concepts and operations, and I am continuing to build deeper production depth.

Bad:
I managed Unity Catalog governance in production enterprise environments.
Better:
I am familiar with Unity Catalog governance concepts and how they fit controlled access and lineage.

Bad:
Lambda is my deepest specialty.
Better:
I have practical Lambda usage in serverless pipeline patterns, with stronger overall depth in Python/SQL/AWS data engineering.

## 12. One-Hour Study Plan
- 10 min vocabulary: review workspace, notebook, cluster, serverless, Delta, medallion, Unity Catalog, Workflows.
- 15 min Delta/medallion: rehearse bronze/silver/gold and Delta reliability explanation.
- 15 min Structured Streaming: rehearse unbounded table, micro-batch, checkpointing, trigger, late data, monitoring.
- 10 min entity resolution pattern: rehearse deterministic then probabilistic matching flow.
- 10 min rehearse answers: practice section 10 Q1-Q12 out loud.

[Back to TOC](#toc)

