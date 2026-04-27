# Citi Telemetry Platform — Technologies Interview Narrative

## 1) Header + System Overview

I designed and operated a Citi telemetry platform that monitored **6,000+ API endpoints** generating about **60,000 events per second** across latency, error-rate, and throughput signals. The purpose of the platform was to provide real-time operational visibility for regulated API services while also preserving replayable history for audit, trend analysis, and incident investigation. At a high level, the platform flowed through **Kafka → Spark → dbt → Airflow → Splunk**, with cloud analytics, ML experimentation, and CI/CD controls layered around it.

---

## 2) The Citi Architecture

```text
                           CITI TELEMETRY PLATFORM
        6,000+ endpoints | ~60,000 events/sec | regulated API monitoring

  [Endpoint APIs / Services]
        |  latency, errors, throughput, logs
        |  ~60,000 events/sec
        v
  +-------------------+
  | Kafka / Streaming |
  | ordered by key    |
  | replay + retention|
  +-------------------+
        |  hot stream
        |  ~5.1B events/day logical flow
        v
  +-------------------+          +--------------------------+
  | Spark Streaming   |--------->| Splunk / Observability   |
  | near-real-time    | alerts    | correlation + dashboards |
  +-------------------+          | 7-year audit retention   |
        |                         +--------------------------+
        | aggregates / curated stream
        v
  +-------------------+
  | Lakehouse / Bronze|
  | Silver / Gold     |
  | Databricks / S3   |
  +-------------------+
        |  batch + replay
        |  500K metrics rows/day
        v
  +-------------------+      +-------------------+
  | dbt Models        |----->| Airflow           |
  | lineage + tests   |      | 8-step orchestration
  +-------------------+      | SLA by 6 AM       |
        |                    +-------------------+
        v
  +-------------------+
  | Analytics Serving |
  | Postgres / Athena |
  | BigQuery / Azure  |
  +-------------------+
        |
        +--------------------+
        |                    |
        v                    v
  +-------------------+  +----------------------+
  | ML Platform       |  | CI/CD for Data       |
  | MLflow registry   |  | GitHub Actions + GE  |
  | anomaly models    |  | contract + quality   |
  +-------------------+  +----------------------+

Infrastructure / IaC spans everything above:
Terraform across AWS + GCP + Azure with policy, repeatability, and drift control.
```

---

## 3) Category A — Kafka / Streaming

### The problem Kafka solved at Citi
Kafka solved the ingestion problem for a platform receiving **60,000 events per second** from **6,000+ monitored endpoints**, where ordering per endpoint mattered and replay mattered even more. We needed a streaming backbone that could absorb regional spikes, decouple producers from consumers, and allow us to replay event ranges during incident reviews and regulatory investigations.

### The architecture decision
We chose self-managed Kafka instead of Kinesis because the environment had on-prem compliance constraints, cross-data-center replication requirements, and a retention model that supported long-lived replay and audit. The key architectural reason was control: we needed deterministic partitioning by endpoint, predictable replication behavior, and an operational model aligned with Citi infrastructure standards.

### Interview story (STAR)

**Situation:** Citi had thousands of regulated API endpoints generating telemetry continuously across regions and severity levels. The existing ingestion model could not guarantee ordered processing per endpoint, and replay during root-cause analysis was inconsistent. Incident teams were spending too much time arguing about missing telemetry instead of diagnosing failures.

**Task:** My task was to design a streaming layer that could ingest high-volume telemetry reliably and preserve ordered event history. I also needed to make sure the solution supported audit replay without forcing application teams to change how they emitted metrics.

**Action:** I introduced Kafka as the central event bus and standardized partitioning by endpoint identifier so per-endpoint ordering stayed stable during normal processing and replay. I designed consumer groups for real-time alerting and downstream enrichment separately, which let us scale independent workloads without coupling them. I also defined retention and replication policies so operations teams could replay incident windows instead of reconstructing data from fragmented logs.

**Result:** The platform handled sustained streaming load while giving incident teams a reliable replay mechanism for regulated investigations. The biggest win was operational trust: once engineers knew the stream could be replayed deterministically, mean-time-to-diagnosis dropped and debates about data completeness largely disappeared. **Number:** ~60,000 events/sec.

### 2 numbers to memorize
- **60,000 events/sec**
- **7-year retention**

---

## 4) Category B — Spark / Compute

### The problem Spark solved
Spark solved the compute problem for a platform that needed both streaming alert pipelines and batch analytics over telemetry history. We had daily metric processing, rolling regional percentiles, and anomaly-oriented enrichments, and we wanted one engineering team using one compute model rather than splitting logic across separate tools.

### The architecture decision
We chose Spark over Flink because batch and streaming unification mattered more than ultra-specialized event-time sophistication. The team already had strong PySpark experience, which meant we could move faster operationally and keep both historical and near-real-time logic in a consistent codebase.

### Interview story (STAR)

**Situation:** Citi needed to process around **500,000 metric rows per day** for curated batch views while also reacting to streaming alert conditions in near real time. Before consolidation, different jobs were written in inconsistent styles and owned by different teams. That made debugging difficult because the batch truth and streaming truth were implemented differently.

**Task:** My task was to unify the compute layer so batch and stream processing could share transformation logic and team ownership. I also needed to keep the solution approachable for Python-heavy engineers so the operational burden stayed low.

**Action:** I standardized compute on Spark and used PySpark for both historical transformations and structured streaming jobs. I defined common schemas and aggregation patterns so the same business logic could be adapted across hourly batch views and real-time detection paths. I also pushed the team to treat streaming as incremental table-building instead of as a separate engineering universe.

**Result:** We reduced fragmentation in the pipeline and made operational support much easier because one team could reason about both modes of processing. It also improved onboarding, since engineers only needed one core compute framework to contribute across ingestion, aggregation, and replay scenarios. **Number:** 500,000 metrics rows/day.

### 2 numbers to memorize
- **500,000 metrics rows/day**
- **1 team using batch + streaming in PySpark**

---

## 5) Category C — Airflow / Orchestration

### The problem Airflow solved
Airflow solved the coordination problem for a nightly telemetry pipeline with **8 dependent steps** that had to finish before **6:00 AM**. Data extraction, staging, model builds, tests, and publishing needed explicit dependency control and rerun visibility.

### The architecture decision
We chose Airflow over Prefect because we needed an enterprise-standard scheduler with a stronger compliance and audit footprint already familiar inside Citi. The decision was less about novelty and more about operational fit: existing support knowledge, auditability, and platform acceptance mattered.

### Interview story (STAR)

**Situation:** The nightly telemetry batch had multiple dependent stages, and when one step failed, reruns were inconsistent and hard to track. Teams often had to manually inspect which downstream steps had partially completed, which created risk around duplicate outputs. That was a bad fit for a regulated environment where pipeline state needed to be explainable.

**Task:** My task was to orchestrate the nightly chain so failures were visible, retries were controlled, and the platform could still meet its morning reporting SLA. I also needed to make the state of each run reviewable for auditors and support teams.

**Action:** I modeled the pipeline in Airflow as a directed workflow with explicit dependencies, retry policies, and operator-level ownership. I separated extraction, transformation, validation, and publish steps so reruns could be targeted instead of blunt-force. I also standardized logging and SLA monitoring so operations teams knew whether a delay came from source data, compute, or publishing.

**Result:** The batch pipeline became far easier to operate because every stage had a clear state, retry history, and upstream/downstream dependency trail. Most importantly, we could explain failures precisely and still protect the **6:00 AM** SLA with controlled reruns instead of manual guesswork. **Number:** 8 dependent steps.

### 2 numbers to memorize
- **8 dependent steps**
- **6:00 AM SLA**

---

## 6) Category D — dbt / Transformation

### The problem dbt solved
dbt solved the SQL chaos problem created by **15 analysts** writing transformations with weak lineage and inconsistent deployment habits. The data itself was useful, but the transformation layer was brittle because business logic lived in disconnected scripts and tribal knowledge.

### The architecture decision
We chose dbt because it gave us version-controlled SQL, lineage graphs, modular models, and a natural CI/CD path for transformation logic. The decision was about making SQL engineering behave like software engineering without forcing analysts to abandon SQL.

### Interview story (STAR)

**Situation:** The telemetry platform had useful raw and staged data, but the reporting layer was fragile because analysts were editing SQL in disconnected ways. When one team changed a logic rule for latency bands or severity rollups, another team’s dashboard could break without warning. That slowed delivery and made trust in the data model uneven.

**Task:** My task was to standardize transformation development so lineage was visible, changes were reviewable, and downstream breakage was reduced. I also needed to keep the tool approachable for SQL-heavy contributors rather than forcing everyone into custom Python pipelines.

**Action:** I introduced dbt to structure the transformation layer into staged, intermediate, and business-facing models with explicit dependencies. I required model code to live in version control and aligned testing with pull-request review so logic changes were visible before deployment. I also used dbt documentation and lineage artifacts to make impact analysis much easier for both engineers and analysts.

**Result:** Transformation work became collaborative instead of collision-prone, and teams could see exactly what a model change would affect before it hit production. That reduced dashboard breakage and improved confidence because lineage was no longer buried in individual notebooks or ad hoc scripts. **Number:** 15 analysts.

### 2 numbers to memorize
- **15 analysts**
- **3 downstream dashboards once broken by one bad model change**

---

## 7) Category E — Databricks / Lakehouse

### The problem Databricks solved
Databricks solved the problem of on-prem Spark cluster management overhead and the need for a more flexible notebook environment for analytics and ML experimentation. We wanted engineers and data scientists to use Spark without spending too much time on cluster babysitting.

### The architecture decision
We chose Databricks Serverless because it reduced cluster-management friction and gave us governance leverage through Unity Catalog. The key business reason was to let teams move faster on analytics and experimentation while still staying inside controlled enterprise patterns.

### Interview story (STAR)

**Situation:** The team had growing Spark needs for telemetry enrichment, historical analysis, and ML-adjacent experiments, but on-prem cluster operations were consuming too much engineering time. Developers were waiting on infrastructure issues instead of working on use cases. That slowed iteration on both performance analysis and anomaly-detection exploration.

**Task:** My task was to reduce operational overhead while preserving a governed analytics environment. I also needed to support ad hoc notebook workflows without turning the platform into an unmanaged sandbox.

**Action:** I moved suitable workloads to Databricks and used the lakehouse model to organize raw, refined, and curated telemetry data. I leaned on the managed environment to eliminate much of the manual cluster handling that had distracted the team. I also aligned governance patterns so experimentation could happen without bypassing data ownership and access controls.

**Result:** Engineers spent more time building transformations and analysis workflows and less time fixing cluster-level issues. The biggest cultural shift was that experimentation became faster without losing governance, which helped the platform serve both operational reporting and ML discovery use cases. **Number:** 0 user-managed clusters for serverless workloads.

### 2 numbers to memorize
- **0 user-managed clusters for serverless workloads**
- **3 lakehouse tiers: bronze, silver, gold**

---

## 8) Category F — Infrastructure / IaC

### The problem Terraform solved
Terraform solved the environment consistency problem when **12 engineers** were provisioning cloud resources manually across multiple providers. Without IaC, drift accumulated quietly and it became hard to tell whether an issue came from code, configuration, or undocumented manual changes.

### The architecture decision
We chose Terraform over CDK because the platform was explicitly multi-cloud across AWS, GCP, and Azure. Provider-agnostic state handling and one consistent workflow mattered more than deep specialization in a single cloud SDK.

### Interview story (STAR)

**Situation:** Platform teams were creating buckets, service accounts, network rules, and compute resources manually, and small environment differences kept surfacing as hard-to-debug production issues. The same pipeline could behave differently in dev and prod simply because resources had drifted over time. That made infrastructure part of the incident surface in a way leadership could not tolerate.

**Task:** My task was to standardize provisioning and reduce configuration drift across cloud environments. I also needed to make infrastructure changes reviewable and repeatable so platform evolution did not depend on tribal memory.

**Action:** I introduced Terraform modules for common patterns and aligned teams on pull-request-based changes instead of console-driven provisioning. I used remote state and environment-specific variables so changes were traceable and reproducible. I also pushed drift detection and plan review as normal operating discipline rather than as emergency-only practice.

**Result:** Infrastructure became far more predictable because resource creation and updates followed reviewed code paths instead of human memory. That reduced environment-specific surprises and made cloud changes auditable in the same way as application and data changes. **Number:** 12 engineers moved off manual provisioning.

### 2 numbers to memorize
- **12 engineers**
- **3 clouds: AWS, GCP, Azure**

---

## 9) Category G — Splunk / Observability

### The problem Splunk solved
Splunk solved the operational visibility problem for **6,000 endpoints** with real-time alert correlation and long-retention searchability. We needed one place to correlate streaming anomalies, infrastructure events, and service-level symptoms during incidents.

### The architecture decision
We chose Splunk over ELK because regulatory auditability, enterprise support, and existing licensing mattered more than cost-optimized open-source flexibility. This was a business-driven observability choice: the platform needed strong enterprise fit and defensible retention behavior.

### Interview story (STAR)

**Situation:** Endpoint failures were not isolated to one signal, so engineers needed to correlate latency spikes, error bursts, infrastructure events, and alert escalations quickly. Without a strong observability layer, too much time was spent pivoting across disconnected tools. That increased incident duration and made historical investigations harder than they should have been.

**Task:** My task was to ensure the telemetry platform could support both real-time triage and audit-friendly historical analysis. I also needed to make sure alert correlation worked across operational signals, not just inside one dashboard.

**Action:** I integrated streaming and batch-derived telemetry into Splunk with consistent fielding and severity context. I aligned dashboarding and search patterns around endpoint, region, and severity so incident teams could move from symptom to scope fast. I also treated retention and searchability as platform features, not as afterthoughts, because regulated investigations depended on them.

**Result:** Splunk became the operational front door for incident response and trend analysis, reducing the time needed to correlate symptoms across services. It also strengthened the audit posture because teams could search long-lived telemetry and alert history without rebuilding the story from raw fragments. **Number:** 7-year retention.

### 2 numbers to memorize
- **6,000 endpoints**
- **7-year retention**

---

## 10) Category H — AWS DE

### The problem AWS Glue/Athena solved
AWS Glue and Athena solved the historical analytics problem over roughly **500 million archived metric rows** without standing up a dedicated always-on warehouse for cold data. We needed low-friction access to deep history for investigations, trend analysis, and low-frequency analytical questions.

### The architecture decision
We chose Athena over Redshift for cold telemetry because the workload was sparse, serverless access mattered, and the data already fit naturally in object storage. The economics worked better when we paid for scans and optimization discipline rather than for a standing cluster.

### Interview story (STAR)

**Situation:** Historical telemetry accumulated quickly, but most of it was not queried often enough to justify loading everything into a traditional always-on analytical cluster. Investigators still needed deep history when they were looking at seasonal trends or long-tail incident patterns. That created a classic hot-versus-cold data problem.

**Task:** My task was to give teams a practical way to query archived telemetry without adding a heavyweight warehouse footprint. I also needed to preserve enough performance discipline that query costs stayed explainable.

**Action:** I organized archived telemetry in cloud storage with partition-aware layouts and exposed it through Athena for ad hoc querying. I used Glue metadata management so datasets were discoverable and queryable without manual table bookkeeping. I also coached teams on predicate discipline and partition alignment so serverless querying stayed efficient.

**Result:** We gave analysts and incident responders access to deep telemetry history without paying for idle cluster capacity. The pattern worked especially well for exploratory and infrequent investigations, where fast setup mattered more than sub-second response times. **Number:** 500 million archived metric rows.

### 2 numbers to memorize
- **500 million archived metric rows**
- **0 standing analytics clusters for cold data**

---

## 11) Category I — GCP + Azure DE

### The problem GCP/Azure solved
GCP and Azure solved the cross-cloud analytics problem for business units operating under different cloud contracts and governance models. The telemetry platform had to be portable enough to support multiple analytical consumers without forcing one-cloud-only decisions everywhere.

### The architecture decision
We used BigQuery as the primary example for serverless analytics because columnar execution, elastic performance, and low DBA overhead fit the analytics need well. The broader architectural point was that the platform design stayed portable, with Terraform and open data patterns limiting deep lock-in.

### Interview story (STAR)

**Situation:** Different groups needed telemetry insights, but they did not all sit on the same cloud or procurement path. A one-cloud-only analytics strategy would have created friction with partner teams and slowed broader adoption. The platform needed to support federation without fragmenting data meaning.

**Task:** My task was to make telemetry analytics available across cloud boundaries while preserving a consistent data model. I also needed to keep operational overhead low so analytics teams could focus on use cases instead of infrastructure administration.

**Action:** I designed the data contracts and transformation layers so curated telemetry datasets could be served into cloud-native analytics environments without semantic drift. I used infrastructure-as-code and schema discipline to keep environments aligned even when the execution engines differed. I also favored serverless analytics patterns where possible so teams did not need dedicated database operations support.

**Result:** Cross-cloud consumers could work with the same telemetry story without forcing the platform into a one-size-fits-all operational model. That increased adoption while preserving architectural coherence, which is exactly the kind of tradeoff Staff-level platform design should optimize for. **Number:** 3 cloud platforms supported.

### 2 numbers to memorize
- **3 cloud platforms**
- **0 dedicated DBAs required for serverless analytics consumers**

---

## 12) Category J — ML Platform

### The problem MLflow solved
MLflow solved the experiment management problem for data scientists running anomaly-detection models such as IsolationForest without reproducibility or a shared registry. Model artifacts existed, but it was hard to say which code, parameters, and data slice produced which result.

### The architecture decision
We chose MLflow over SageMaker for experiment tracking because we wanted a cloud-agnostic, open source solution that worked both locally and in hosted environments. The decision fit the platform’s broader theme: keep the experimentation layer portable and avoid unnecessary vendor lock-in where open tooling was sufficient.

### Interview story (STAR)

**Situation:** The team wanted to move beyond threshold alerts and test anomaly-detection models against telemetry patterns, but experiment tracking was inconsistent. People were saving notebooks and artifacts manually, which made comparison and reproducibility weak. That meant model discussions often became debates about which run was actually being referenced.

**Task:** My task was to make experimentation reproducible and to create a path from experiments to governed candidate models. I also needed a solution that would not force the team into one cloud-specific ML platform prematurely.

**Action:** I introduced MLflow for tracking parameters, metrics, artifacts, and candidate models tied to telemetry experiments. I standardized the way runs were logged so comparisons between anomaly-detection approaches were reviewable and reproducible. I also used the registry concept to separate “interesting experiment” from “approved model candidate,” which improved governance.

**Result:** Model development became more disciplined because every experiment had a clear record of inputs, outputs, and results. That reduced confusion in review discussions and created a cleaner bridge from exploratory analysis to operationalized ML. **Number:** 1 registry for model candidates.

### 2 numbers to memorize
- **1 shared model registry**
- **2 classes of artifacts tracked: experiment runs and promoted candidates**

---

## 13) Category K — CI/CD for Data

### The problem GitHub Actions + Great Expectations solved
GitHub Actions and Great Expectations solved the deployment-safety problem after a dbt model change once broke **3 downstream dashboards** because there was no enforced quality check before merge. The lesson was simple: data quality checks that happen after deployment are too late for platform trust.

### The architecture decision
We chose Great Expectations in CI because contract-style validation before merge is far safer than relying on downstream users to notice bad outputs. GitHub Actions fit naturally because it gave us an auditable, automated path from change proposal to validation to deployment.

### Interview story (STAR)

**Situation:** A transformation change merged successfully from a code perspective but introduced bad data semantics that propagated into downstream dashboards. Because checks were weak and late, the issue was discovered by consumers rather than by the platform. That damaged trust far more than the technical bug itself.

**Task:** My task was to move quality enforcement earlier in the lifecycle so data model changes could not merge without passing defined checks. I also needed to make the process lightweight enough that teams would adopt it instead of working around it.

**Action:** I added CI workflows that ran transformation validation and Great Expectations-style checks before deployment decisions were finalized. I separated syntax success from data-contract success so a green build did not automatically mean “safe to ship.” I also made failures visible in pull requests so reviewers could discuss data impact before merge, not after production fallout.

**Result:** The platform became safer because bad changes were more likely to fail in review than in front of users. Just as important, teams started treating data contracts as deployable software quality gates rather than as optional documentation. **Number:** 3 downstream dashboards protected by pre-merge checks.

### 2 numbers to memorize
- **3 downstream dashboards**
- **1 pre-merge quality gate per data change**

---

## 14) The Master Interview Answer

If I were describing a data platform I designed at scale, I’d say this: at Citi we operated a telemetry platform for **6,000+ API endpoints** generating roughly **60,000 events per second** across latency, error-rate, and throughput signals for regulated services. Kafka was the streaming backbone because we needed ordered ingestion per endpoint and reliable replay for audit and incident review. Spark handled both near-real-time and historical compute so the same team could build streaming enrichments and batch aggregates without splitting logic across different engines.

From there, we used dbt to turn raw and staged telemetry into governed analytical models with lineage and reviewable SQL, and Airflow orchestrated the nightly dependency chain so the reporting layer hit its **6:00 AM** SLA. Splunk sat on the observability side for real-time alert correlation and long-retention search, while Athena and other cloud analytics patterns handled colder historical questions without forcing us to run standing infrastructure everywhere. We also supported experimentation through MLflow for anomaly-detection use cases and locked down delivery with GitHub Actions plus data-quality checks so model and transformation changes were validated before merge.

The result was a platform that balanced streaming speed, analytical depth, governance, and auditability. It was not just a pipeline; it was an operating model where streaming, batch, observability, and deployment discipline all reinforced each other. That is the kind of design I usually aim for at Staff level: strong business alignment, clear operational tradeoffs, and enough modularity that the platform can evolve without losing trust.
