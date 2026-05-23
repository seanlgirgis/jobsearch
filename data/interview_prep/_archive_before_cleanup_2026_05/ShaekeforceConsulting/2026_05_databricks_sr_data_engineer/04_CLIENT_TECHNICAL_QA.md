# 04 Client Technical QA

My safest technical positioning is: AWS/Python/PySpark-style data engineer with strong pipeline reliability, data quality, and operational monitoring experience, plus practical Databricks exposure built on those foundations.

## 1. Python / SQL / ETL Fundamentals

### Q01. Python Pipeline Design

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

### Q02. SQL Optimization Approach

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

### Q03. ETL vs ELT Decisioning

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

### Q04. Batch Pipeline Design

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

### Q05. Schema and Data Modeling

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

### Q06. Large Files and Partition Handling

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

### Q07. Troubleshooting Slow or Failing Pipelines

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

### Q08. S3 Landing Zone Design

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

### Q09. AWS Glue and PySpark Pattern

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

### Q10. Redshift Analytical Pattern

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

### Q11. Lambda in Data Pipelines

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

### Q12. CloudWatch and Monitoring

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

### Q13. IAM and Security Awareness

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

### Q14. What Is Databricks?

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

### Q15. Spark DataFrames in Practice

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

### Q16. Delta Lake and Delta Tables

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

### Q17. Medallion Architecture

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

### Q18. Jobs and Workflows

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

### Q19. Databricks vs AWS Glue

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

### Q20. Structured Streaming Basics

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

### Q21. Unity Catalog and Governance Basics

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

### Q22. Data Quality Framework

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

### Q23. Schema, Null, and Duplicate Checks

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

### Q24. Reconciliation and Row Counts

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

### Q25. Unit Testing for Python and Spark

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

### Q26. Monitoring and Alerting

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

### Q27. Incident Response and Operational Support

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

### Q28. Entity Resolution Approach

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

### Q29. Deterministic vs Probabilistic Matching

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

### Q30. False Positives and False Negatives

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

### Q31. Feature Engineering Support for ML

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

### Q32. Operationalizing ML Outputs

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

### Q33. Explaining Technical Concepts to Non-Technical Stakeholders

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

### Q34. Working with Data Scientists and Architects

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

### Q35. Agile Delivery, Jira, Confluence, and Production Mindset

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


### Q36. Supporting AI/ML Teams as a Data Engineer

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


### Q37. How would you connect Databricks with AWS S3?

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

### Q38. How would you implement data quality checks in Databricks?

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

### Top 10 questions to rehearse first
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

### Top 5 weak areas to defend carefully
1. Q14. What Is Databricks?
2. Q18. Jobs and Workflows
3. Q20. Structured Streaming Basics
4. Q21. Unity Catalog and Governance Basics
5. Q11. Lambda in Data Pipelines

### Top 5 stories to reuse
1. Citi telemetry pipeline (6,000+ endpoints)
2. AWS S3/Glue/Redshift migration pattern
3. Capacity forecasting support (Prophet and scikit-learn)
4. Data quality and validation framework
5. Operational monitoring and incident support background








