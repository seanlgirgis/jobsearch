# Interview Master — Sean Girgis

---

## The Elevator Pitch

**30 Seconds — Phone Screen / Opening**

I'm Sean Girgis — a Senior Data Engineer with 20-plus years of enterprise
experience. Most recently I spent eight years at Citigroup building
production-grade data pipelines: ETL at scale, ML-driven capacity
forecasting, and a hybrid AWS and Oracle data platform. I'm based in the
Dallas–Fort Worth area, U.S. citizen, no sponsorship required. I'm looking
for a senior data engineering or cloud data platform role where I can bring
the full stack — Python, PySpark, AWS, and the AI/ML capabilities I've been
building alongside my core engineering work.

---

**2 Minutes — First Round / Hiring Manager**

I started in software development in 1999 — C++, multithreaded systems,
Oracle databases — and my career evolved from low-level systems work toward
data engineering and infrastructure intelligence.

The anchor of my recent experience is eight years at Citigroup. I built
Python and PySpark ETL pipelines ingesting P95 telemetry from thousands of
endpoints through BMC TrueSight. I designed an ML forecasting layer —
Prophet and scikit-learn — that predicted capacity bottlenecks six months
ahead. I built a hybrid AWS and Oracle data platform: S3 as the raw landing
zone, Glue for ETL, Redshift for ML workloads, and ECS for containerized
pipeline jobs. I also built the analytics layer on top — Streamlit and
Plotly dashboards used by senior stakeholders for infrastructure decisions.

In parallel, I've been building my own practice projects — HorizonScale, a
time-series ML forecasting engine that runs 8,000-plus series through a
model tournament on Spark, and an AI-powered job search pipeline using
Grok, RAG, and FAISS to automate the entire application workflow. Both are
public on GitHub.

What I'm looking for: a role where data engineering is the primary function,
modern lakehouse or cloud-native architecture, and room to bring in AI and ML
as part of the craft — not a separate team. I'm actively studying Databricks
and dbt and I'm ready to contribute from day one on Python, PySpark, and AWS.

---

## Full Career Story

**Tell me about yourself — walk me through your background.**

I'll take you through the arc rather than the job titles — the thread is
the same throughout: making complex systems visible, measurable, and
improvable through data.

I started in software development — C++, Oracle, multithreaded systems.
Six years at Corpus Inc. supporting Sprint's billing infrastructure, where
I learned to care about performance at VISA-scale transaction volumes. After
that, Sabre — migration of a high-throughput shopping engine from 200-plus
MySQL nodes to a 6-node Oracle RAC cluster, 95% hardware footprint reduction
while maintaining sub-second query latency.

From there, my career shifted toward application performance monitoring and
data. Five years at CA Technologies as SME for CA APM at TIAA-CREF — 50-plus
Enterprise Managers, 4,000-to-6,000 instrumented agents, performance
dashboards, and automated reporting. Then G6 Hospitality — built the
extraction pipeline from Dynatrace AppMon, segmented performance by geography
and device, and produced analytics that drove frontend optimization
recommendations for brand.com.

Then eight years at Citigroup. Built the Python and Pandas ETL pipeline for
P95 telemetry across thousands of endpoints, the ML forecasting layer, the
hybrid AWS and Oracle platform, and the analytics and reporting layer on top.
Left at end of 2025 with everything I set out to build there delivered.

Now looking for the next chapter — a dedicated data engineering or cloud data
platform role with modern tooling and the full stack I've built.

---

## Why Now & What I'm Looking For

**Why did you leave Citi? Why are you looking now?**

Eight years is a long run and I'm proud of what I built there. The honest
answer is the role reached its natural ceiling within the capacity planning
function. I'd built the ETL pipeline, the ML forecasting layer, the AWS
migration, the dashboards — and the team's mandate didn't have room to go
further into the modern data stack. No path to Databricks, dbt, event-driven
architectures, or the lakehouse design I want to be doing next.

I left on my own terms at end of 2025 and immediately started building:
HorizonScale for ML and PySpark depth, the AI job search pipeline for hands-on
LLM and agentic patterns, and self-study on Databricks, Delta Lake, and dbt.
I'm looking for a role where data engineering is first-class — not a support
function embedded in infrastructure — and where I can contribute from day one
on Python, PySpark, and AWS while building toward the modern lakehouse stack.

---

**What are you looking for in your next role?**

Three things. Engineering craft — a team that takes pipeline design, data
modeling, and platform architecture seriously. Modern tooling — cloud-native,
Spark or Databricks, dbt, event streaming. And AI and data together — I'm
genuinely excited about the intersection, whether that's inference pipelines,
LLM capabilities in data products, or the data infrastructure that AI systems
run on. I want to be where those two fields are converging.

---

**What's your ideal company size / type?**

I've spent most of my career in large enterprises and know how to operate
in regulated, high-stakes environments. I'm genuinely open to that again if
the engineering ambition is there. But I'm also attracted to mid-size
companies — Series B to D, or established companies with strong engineering
culture — where data engineering is closer to the core product and the
feedback loop is shorter. What matters more than size is whether the team
takes data engineering seriously as a discipline.

---

## Behavioral: Impact & Automation

**Tell me about a time you turned a slow manual process into an automated system.**

**S** — At Citi, the monthly capacity planning report was entirely manual in
Excel. Extract P95 telemetry from 65,000-plus endpoints, manually enrich with
CMDB and AppDynamics data, apply safety factors in spreadsheet formulas,
publish. That process took five to ten business days every month.

**T** — I identified this as the highest-friction and highest-leverage
problem on the team. My goal was to replace the entire manual workflow with
a pipeline that produced the same deliverables automatically and reliably.

**A** — Built a Python ETL pipeline end to end. SQLAlchemy and cx_Oracle
for direct Oracle extraction. Pandas for transformations, NumPy for
vectorized safety and ceiling calculations across 65,000-plus rows.
SQLAlchemy plus pyodbc for SQL Server CMDB joins. The hardest part was
identifier normalization — three source systems with different naming
conventions for the same endpoints. Dual SQLite architecture: monthly
databases for per-period detail, master database for multi-month
progression. openpyxl for Excel output. Streamlit for internal dashboard.
Version-controlled in GitLab with required merge requests for logic changes.

**R** — Reports that previously took five to ten days were produced in the
first or second hour after monthly data was available. Same deliverables,
same format — but generated deterministically and consistently across all
65,000-plus endpoints. The team went from spending most of the month
producing data to actually doing capacity planning work.

---

**Tell me about a project you built from scratch that had real business impact.**

**S** — The capacity forecasting ML system at Citi. The team had good
historical data but no way to look forward. Teams only found out about
capacity problems when they were already close to the limit — at a bank,
that has regulatory implications.

**T** — Build a forecasting system that predicted infrastructure capacity
six months ahead with enough reliability to drive procurement and architecture
decisions.

**A** — Built the ML layer in Python using Prophet with logistic growth
mode — constrains forecasts between 0% and 100% utilization, which matters
because a linear model will forecast 110% CPU, which is meaningless. Added
scikit-learn for ensemble validation. Applied safety factors and ceiling
thresholds to produce conservative adjusted utilization numbers. Built output
into Streamlit so teams could see projected trajectories months ahead. Then
migrated the ML workloads from on-premises Oracle to Redshift to enable
parallel forecasting at cloud scale.

**R** — 90-plus percent forecast accuracy over the six-month window. Teams
received proactive warnings weeks to months before systems approached the
ceiling. In one important case, a memory utilization trend that looked like
a capacity problem turned out to be a memory leak — the early warning created
time to fix it properly rather than just provisioning more RAM.

---

**Give me an example of a time you identified a cost-saving opportunity through data.**

**S** — In the Citi capacity pipeline, the same system that flagged near-
capacity servers also surfaced the opposite: systems with consistently low
adjusted utilization that were over-provisioned.

**A** — The risk report generated two ranked lists — systems approaching the
ceiling and the most under-utilized systems in the fleet. Each entry had the
owner, department, region, and system type attached from the enrichment joins.
Recommendations ranged from downsizing VM resource allocation, to consolidating
workloads onto fewer hosts, to promoting from physical on-premises to virtual
or cloud where the workload profile supported it.

**R** — The capacity team published findings to owning teams across the
enterprise. Hardware consolidation decisions followed from the data. In a bank
running tens of thousands of physical and virtual servers, over-provisioned
infrastructure adds up fast. The data-driven ranked list with owner attribution
made the conversations actionable — teams couldn't push back on anecdotal
suggestions, but a specific system showing 12% average adjusted utilization
over twelve months is hard to argue with.

---

## Behavioral: Leadership & Influence

**Tell me about a time you influenced a technical decision without direct authority.**

**S** — At Citi, the capacity planning team operated on a manual Excel
workflow. There was no mandate to change it — it worked, it was familiar,
people had processes built around it. I had to build the case.

**A** — I built the pipeline as a proof of concept, ran it in parallel with
the manual process for one monthly cycle, then presented the comparison side
by side: manual output took nine days, pipeline output took two hours. More
importantly, I ran a diff between the two outputs and showed where they
diverged — places where the manual process had applied factors inconsistently
or missed enrichment data. The quality argument was as strong as the speed
argument. I made the case in terms of what the team cared about: reliability
of the reports they were putting in front of senior stakeholders.

**R** — The pipeline replaced the manual process. The approach also
established a pattern for how the team thought about data work — repeatable
validated pipelines rather than repeatable manual workflows. That shift
opened the door for the ML forecasting work that came after.

---

**Tell me about a time you explained a complex technical concept to a non-technical audience.**

**S** — The ML capacity forecasting system produced outputs that senior
infrastructure stakeholders needed to act on. "The Prophet model with logistic
growth and a 1.15 safety factor predicts 90% adjusted utilization in 11 weeks"
doesn't land with a VP who manages a budget, not a model.

**A** — I built the Streamlit dashboard around the business question, not
the model output. The dashboard showed utilization trend over the past two
years with a shaded forward window and a clear red line at the 90% ceiling.
The risk report used plain English — "this system needs attention before end
of Q2" with owner name, region, and a color-coded priority flag. Under-
utilization findings were savings recommendations, not statistical summaries.

**R** — Stakeholders engaged with the forecasts and acted on the
recommendations — the only real measure of success. A technically perfect
model nobody acts on has no business value. Same philosophy at G6:
P95 response time data turned into a map a VP could look at and immediately
understand which regions needed attention.

---

**Tell me about a time you mentored or helped a colleague grow technically.**

**S** — At CA Technologies, I was the SME for CA APM at TIAA-CREF. Part of
that role was training the client's internal IT team and junior CA consultants.

**A** — Rather than delivering knowledge as lectures, I structured learning
around real problems in the client environment. When I built custom management
modules — dashboards, alert thresholds, SLA monitoring — I walked team members
through why each design choice was made, not just what the configuration was.
I documented the patterns in a reusable way that was adopted as standards by
both the CA team and the client's internal team.

**R** — The training programs were adopted by CA internally for other client
engagements. The client team became capable of extending and maintaining the
APM configuration independently rather than remaining dependent on external
consultants. That's the right measure of successful knowledge transfer — when
you've worked yourself out of being the only person who knows how something
works.

---

## Behavioral: Challenge & Growth

**Tell me about the hardest technical problem you've ever solved.**

**S** — At Sabre, I was the lead on migrating a high-throughput shopping
engine from 200-plus MySQL nodes to a 6-node Oracle RAC cluster. Transaction
volume comparable to VISA. The constraint: zero data loss, sub-second query
latency maintained throughout the phased cutover.

**A** — The core engineering problem: how do you validate that 200-plus MySQL
nodes' worth of data arrived intact when transaction volumes are in the
billions? I built a CPPUNIT testing framework in C++ with OCCI/OCI that ran
automated validation across millions of transaction records — row counts,
hash-based checksums on key fields, spot-check queries on high-value
transactions. Schema conversion was automated; manually converting MySQL
schemas to Oracle at that scale isn't tractable. C++ transaction processing
code was optimized for the Oracle environment: OCCI query patterns, connection
pooling, batch commit sizing.

**R** — Migration completed successfully. No data loss, no SLA breach during
cutover. 95% hardware footprint reduction. The deeper lesson: at that scale,
you can't test migration correctness manually. You need automated validation
running at machine speed across the full dataset. That thinking shows up in
everything I've built since — quality gates, validation pipelines, automated
correctness checks before marking a process complete.

---

**Tell me about a failure and what you learned from it.**

**S** — Early in my data engineering work at Citi, I built a reporting
pipeline that was producing outputs quickly. What I hadn't built was a robust
validation layer. The pipeline completed successfully but silently produced
incorrect output — the enrichment join had failed for a subset of records
in a way that didn't raise an error. Reports went out with those records
showing as unowned rather than flagged.

**A** — When the gap was discovered, I investigated the root cause — an edge
case in the hostname normalization logic not covered by my test data. I rebuilt
the validation layer completely: explicit row count checks at each stage,
enrichment coverage rate tracking, a flag for any records with no join match
rather than silently including them with nulls, and an exit criteria check the
pipeline had to pass before marking the run complete. Added structured logging
that recorded coverage rates per run so any degradation would be visible over
time.

**R** — The validation layer caught several subsequent edge cases before they
reached the output. More importantly, it changed my design philosophy: a
pipeline that completes without errors but produces wrong output is more
dangerous than one that fails loudly. Silent success is not success.

---

**Tell me about a time you had to learn a new technology quickly under pressure.**

**S** — When Citi started the AWS migration of the ML forecasting workloads,
I had to get productive on AWS Glue and PySpark quickly — the infrastructure
team was moving on a timeline and the data engineering layer had to be ready.

**A** — My approach was to map what I already knew onto the new environment
rather than treating it as starting from zero. I understood Python, Pandas,
and ETL patterns deeply. PySpark is a distributed execution layer over the
same conceptual model. Glue is managed Spark with an AWS-native job scheduler.
I built a small end-to-end Glue job quickly to validate my understanding, then
extended it to the real workload. The PySpark Grouped Map UDF pattern for
distributing Python ML models was the key new concept — I spent focused time
understanding exactly why it works before applying it to the Prophet jobs.

**R** — AWS migration delivered on schedule. The Glue-based forecasting
pipeline ran the full fleet in a fraction of the time the on-premises Oracle
approach did. The lesson: when learning under pressure, map first. Understand
what transfers, then fill in the specific gaps. Faster than treating everything
as new.

---

**Tell me about a time you disagreed with a technical approach.**

**S** — At Citi, there was a proposal to continue storing capacity analysis
outputs in a monolithic Excel-based system even after the pipeline was built.

**A** — I agreed that the Excel output format should stay — right call for
the enterprise audience. But I disagreed that Excel files should be the
persistence layer for historical data we needed to query and trend. I proposed
the dual SQLite architecture — monthly databases for per-period detail, master
database for longitudinal querying — as a solution that kept Excel output for
stakeholders while giving the team a proper query interface. I presented the
trade-offs explicitly: zero infrastructure overhead, familiar SQL interface,
running the same day.

**R** — Dual database architecture was adopted. Streamlit dashboard queried
directly from SQLite, enabling month-over-month trend analysis. Excel outputs
for enterprise distribution continued unchanged. Both audiences got what they
needed.

---

## Technical: Data Pipeline Design

**How do you approach designing a data pipeline from scratch?**

I start with the output — what decision or product does this pipeline serve,
and what does the consumer actually need? That drives everything backward:
schema at the end, transformations that produce it, source inputs, acceptable
latency (batch vs streaming), and what failure looks like at each stage.

Then I define the data contract between stages. Each stage has an input schema
and an output schema — documented explicitly before writing any transformation
logic. This makes the pipeline modular: each stage can be tested, replaced,
or rerun independently.

Quality gates are non-negotiable. Every stage has entrance criteria (validate
input before processing) and exit criteria (validate output before passing
downstream). Silent success — completing without errors but producing wrong
output — is the worst failure mode. A loud failure at stage 3 is far better
than wrong data arriving at stage 10.

Finally, idempotency: every stage should be safe to rerun. Drop and recreate
tables, overwrite Parquet files. Same result every time from the same input.
Rerun any stage from the last known-good checkpoint without worrying about
duplicates or state corruption.

---

**How do you handle data quality in production pipelines?**

In layers.

First layer — structural validation at ingestion: expected schema, required
columns, row counts above minimum threshold, non-null join keys. Failure halts
the pipeline immediately with a descriptive error. Don't process corrupt input.

Second layer — semantic validation after transformation: are utilization values
between 0 and 100? Are there no negative response times? Are join coverage
rates above the expected floor? I track coverage rates over time because
degrading coverage is itself a signal — reference data going stale or a source
system changing format.

Third layer — trend monitoring: is today's output consistent with historical
patterns? A sudden 50% drop in row count after extraction is worth
investigating even if structural checks pass. I've seen cases where a source
system silently stopped writing certain record types and the pipeline processed
successfully with half the data it should have had.

The key principle: fail loudly and early. The cost of a delayed pipeline run
is far lower than the cost of wrong data reaching downstream consumers.

---

**Batch vs streaming — how do you choose?**

Start with the business latency requirement. If decisions need to be made on
data that's seconds old — fraud detection, real-time pricing, operational
alerting — streaming is required. If the decision horizon is hours or days —
monthly capacity reports, daily business analytics, weekly ML model refresh —
batch is simpler, cheaper, and more reliable.

Most of my production work has been batch. The Citi capacity pipeline was
monthly. HorizonScale is a monthly forecast cycle. G6 performance analysis
was weekly. In all of those cases, streaming would have added significant
infrastructure and operational complexity with no business benefit.

Where I'd choose streaming: data whose value decays in minutes, downstream
systems that need to react immediately, or data volume that makes periodic
large batch loads impractical. For most analytics and reporting use cases,
well-designed micro-batch or scheduled batch with tight SLAs covers the need.

---

**What does idempotency mean in a data pipeline and why does it matter?**

An idempotent pipeline stage produces the same output every time it's run
against the same input, regardless of how many times it's been run. Run stage
4 twice on the same input — you get exactly the same output both times. No
duplicates, no corrupted state.

Why it matters: pipelines fail. Source data arrives late. Bugs get fixed and
historical data needs reprocessing. Deployments break and need to be rolled
back. In all of these cases, being able to rerun a stage without manual cleanup
is the difference between a manageable recovery and a data archaeology project.

How I implement it: for database tables, drop-and-recreate rather than
appending unless the design explicitly requires append-only with deduplication.
For master/history tables, upsert on a natural key. For Parquet outputs,
overwrite. Never append to an output that might already contain the same data.

---

**How do you think about data modeling — when do you use star schema vs something else?**

Star schema is my default for analytical workloads where the query pattern is
"give me a measure filtered and grouped by multiple dimensions." Fact table
with foreign keys to dimension tables. Queries are simple, optimizer-friendly,
and easy to explain to stakeholders. That's what I used for the Citi capacity
planning analytics — utilization metrics as the fact, server metadata and time
as dimensions.

I use a flattened wide table when the query patterns are dominated by a single
analytical workflow and join performance matters more than flexibility. The
HorizonScale forecast outputs are always consumed with host metadata joined to
forecast data — denormalizing into a single table eliminates runtime joins and
simplifies the query layer.

For operational data stores where writes are frequent and data integrity is
critical: normalized relational design. For event logs and time-series data:
columnar Parquet with time partitioning — star schema joins get expensive at
millions of rows; column pruning and partition pushdown on Parquet are the
right tools.

The modeling choice should follow the access pattern, not the other way around.

---

## Technical: AWS Architecture

**Walk me through how you'd design an AWS data lake for a large enterprise.**

Start with S3 as the storage foundation — cheap, durable, decoupled from
compute. Structure with a medallion-style layered prefix:

Raw/bronze — data exactly as it arrived from the source. Never transform in
place. Silver — cleaned, validated, enriched Parquet with Snappy compression.
Gold — business-ready aggregates and analytical views. Keep layers separate
so any layer can be reprocessed from above without touching source data.

AWS Glue Data Catalog as the metastore — register all table schemas,
partition information, and data lineage. Makes data discoverable to Athena
for ad-hoc queries without loading anything into a warehouse. Glue PySpark
jobs for heavy transformation; Glue Python Shell for lightweight orchestration
and data quality checks. Step Functions or Airflow via MWAA for orchestration
with dependency management.

For serving: Athena for ad-hoc SQL over S3 — serverless, pay per query.
Redshift for workloads needing consistent sub-second response — executive
dashboards, ML feature stores. IAM roles with least privilege at every layer.
No long-lived credentials anywhere.

Keys at scale: partition strategy (Parquet partitioned by date or region
eliminates full-table scans), small file consolidation (periodic compaction
jobs to prevent the small-file performance problem), and data catalog
governance so teams can discover what exists without asking someone.

---

**When would you use Glue vs EMR vs Lambda for a data processing job?**

Glue for managed ETL where I don't want to manage cluster lifecycle — the
right default for Spark workloads on a schedule that don't need persistent
cluster configuration. Used Glue for HorizonScale's distributed Prophet
forecasting: 10 G.2X workers, Glue 4.0, PySpark Grouped Map UDF. Works well
for batch ETL measured in minutes to hours.

EMR when I need more control — specific Spark version, custom libraries,
long-running clusters, spot instance fleets for cost optimization, or
workloads Glue's managed environment can't accommodate. For massive-scale
jobs where tuning YARN memory settings, executor configuration, and cluster
topology matters, EMR gives that control at the cost of more operational
responsibility.

Lambda for event-driven lightweight processing: S3 trigger on new file
arrival, DynamoDB Streams, API Gateway integration. Lambda's constraints —
15-minute timeout, 10GB memory max, cold start latency — make it wrong for
heavy ETL. But for "a file arrived, validate it and write a notification" or
"an API call arrived, look up a value and return it," Lambda is the right
tool. I use Lambda as orchestration glue between services, not as the
processing engine for large data.

---

**How does IAM work and why does it matter for data engineering?**

IAM is the authorization layer for every AWS API call. Every action — reading
from S3, running a Glue job, writing to Redshift — is evaluated against the
attached policies of the calling principal. Default is deny; explicit allow
must exist, and any explicit deny overrides all allows.

For data engineering it matters three specific ways.

First, least privilege for service roles: a Glue job should have S3 read
access on the source prefix and S3 write access on the destination prefix,
nothing else. Not S3 full access on the entire account. If a job gets
compromised or misconfigured, the blast radius is contained to exactly the
data it legitimately touches. I auto-provision scoped IAM roles for every
Glue job rather than reusing a single broad role.

Second, cross-account access: in enterprise environments, data commonly lives
in one account and consuming teams are in others. The assume-role-with-STS
pattern scoped to the target account is how you do this securely without
sharing credentials.

Third, audit trail: IAM events flow into CloudTrail — a complete log of who
accessed what data when. In regulated environments like financial services,
that's a compliance requirement, not a nice-to-have.

---

## Technical: PySpark & Scale

**How does Spark's execution model work? What's the difference between a transformation and an action?**

Spark uses lazy evaluation. Transformations — map, filter, join, groupBy —
build a logical execution plan (a DAG) but don't execute anything. Nothing
runs until an action is called: collect, count, write, show. This lets Spark
optimize the entire computation graph before executing: filter pushdown,
predicate pushdown to Parquet readers, join reordering.

Wide transformations — joins, groupBy, distinct — require a shuffle: data
moves across partitions and nodes. Shuffles are expensive. Narrow
transformations — map, filter, select — don't shuffle; each partition is
processed independently.

Performance tuning in Spark is largely about minimizing shuffles: broadcast
joins for small tables, partition by the join key before joining large tables,
avoid unnecessary wide transformations.

In the HorizonScale context: the Grouped Map UDF pattern is deliberately
narrow — each partition (one host-resource pair) is processed independently
with no cross-partition communication. Zero shuffles in the forecasting stage.

---

**You have 8,000+ time-series models to run. How do you parallelize that in Spark?**

The PySpark Grouped Map UDF pattern. This is the right approach when you have
a Python ML function like Prophet that can't natively distribute across a Spark
cluster but needs to run independently on each logical group in the data.

Structure: group the data by (host_id, resource) so each partition contains
the complete time series for one host-resource pair. Define a Pandas UDF that
receives a Pandas DataFrame for one partition, runs the complete model fit,
generates the forecast, and returns the results. Spark automatically
distributes partitions across the worker fleet. No cross-partition
communication, no shared state, no coordination overhead — embarrassingly
parallel. With 10 Glue G.2X workers processing 8,000-plus partitions, the
throughput difference over sequential or local multiprocessing is dramatic.

Key operational detail: reduce Prophet's uncertainty_samples from 1,000 to 100
in the distributed version. Confidence interval accuracy degradation at fleet
scale is negligible — the throughput gain is 10x. That single change is what
makes the fleet-scale run tractable within a reasonable job window.

---

## Technical: ML & Forecasting

**How does Facebook Prophet work and when would you choose it over SARIMA?**

Prophet is a decomposable model: it separates the time series into a trend
component, seasonality at multiple frequencies (daily, weekly, annual via
Fourier series), and holiday effects. It fits these components independently
via Stan's Bayesian inference, then combines them for the forecast.
Because it's decomposable, it handles missing data gracefully, it's robust
to outliers, and the components are interpretable.

Choose Prophet when: the series has strong multi-frequency seasonality, you
need to incorporate known future events (holidays, planned maintenance
windows), you need well-calibrated uncertainty intervals for decision-making,
or you're running a model tournament across heterogeneous series and want a
robust default.

SARIMA is better when: the series has a single dominant seasonal period, the
data is regular with no missing values, and you want a classical statistical
model with auditable behavior. SARIMA with seasonal order (1,1,1,7) is very
precise on a server with a clean weekly business cycle and low noise — it'll
often beat Prophet on MAPE on those specific series.

The model tournament selects between them per series, which is exactly the
right approach.

---

**What's the champion-challenger framework and why use it for forecasting?**

The champion-challenger framework evaluates multiple models on a held-out
backtest window and selects the best-performing one as the champion for
deployment.

In HorizonScale: I use the first 32 months of data for training, hold out the
most recent 4 months as a backtest window that no model sees during training,
then compare Prophet, SARIMA, and XGBoost on MAPE against those real held-out
values. Lowest MAPE wins for that specific host-resource pair.

Why use it rather than picking a single model: no single model fits all
behavioral patterns equally well. Prophet wins on seasonal series. SARIMA wins
on clean weekly-cycle series with low noise. XGBoost wins on trend-dominated
series. Using a single global model means accepting poor forecast quality on
the series where it doesn't fit — and those are often the CAPACITY_BREACH
scenarios where accuracy matters most.

---

## Technical: AI / LLM / Agentic

**What is RAG and how does it work in a production pipeline?**

RAG — Retrieval-Augmented Generation — grounds an LLM's response in retrieved
documents rather than relying solely on the model's training knowledge.

The pattern: embed a query and a document corpus using the same embedding
model, retrieve the most semantically similar documents to the query, inject
those documents into the prompt context, and ask the LLM to answer using that
context. This lets you use a general-purpose LLM on proprietary or current
data without fine-tuning.

In my job search pipeline, RAG drives the job scoring stage. The master career
profile — a structured YAML with all skills, roles, and experience summaries —
is the retrieval corpus. The incoming job description is the query. The pipeline
retrieves relevant profile sections, injects them alongside the job description
into a structured prompt, and asks Grok to return a match score, skill gap
analysis, and recommendation. The career profile is the hard boundary for what
the LLM can say about experience — it can't invent accomplishments that aren't
in the profile YAML. The retrieval grounds the generation.

---

**How does FAISS work for semantic similarity and why use it locally?**

FAISS — Facebook AI Similarity Search — is a library for efficient
nearest-neighbor search in high-dimensional vector spaces.

Workflow: embed documents using a sentence transformer model to produce
fixed-dimension vectors. Store those vectors in a FAISS index. At query time,
embed the query, search the index for the nearest vectors by cosine similarity,
return the top-k matches with their similarity scores.

In my job search pipeline, I use FAISS for the duplicate detection gate at
stage zero. Every previously processed job description is embedded and stored
in the index. When a new posting arrives, it's embedded and compared against
all previous entries. If cosine similarity exceeds the threshold, the pipeline
blocks — the job has likely been processed before under a different URL.

I run this locally with all-MiniLM-L6-v2 from sentence-transformers for three
reasons: speed (milliseconds, no network call), cost (no API charge on every
intake), and privacy (job descriptions contain detailed information that
doesn't need to leave the machine for an embedding operation). The index
persists to disk and rebuilds in seconds when a new job is accepted.

---

## Project Deep-Dives

### AI-Powered Job Search Pipeline

**Walk me through the job search pipeline you built.**

Ten-stage sequential pipeline. Input is a raw job posting. Output is a
production-ready application package — tailored resume, cover letter, company
research — tracked in a structured system.

Stage 0: FAISS semantic duplicate check so I don't waste API credits on jobs
already processed. Stage 1: RAG scoring against my career profile — match
score and skill gap analysis (first live run scored 85% on a Collective Health
role). If accepted, stages 3-5 extract structured job data, generate a tailored
JSON resume grounded in the master profile, and render it to ATS-safe DOCX.
Stages 6-8 run company research and generate a cover letter referencing
specific things about the company — the generator classifies the target as
agency vs direct employer and adjusts tone automatically. Stage 9 is a
blocking quality gate before anything is marked as applied.

Primary LLM is Grok via its OpenAI-compatible API — grok-3-mini for light tasks
(scoring, parsing), grok-3 for heavy generation that goes in front of a
hiring manager.

---

### HorizonScale — ML Forecasting at Scale

**How did you approach the forecasting problem at 8,000+ series?**

Two phases. Phase one was local: DuckDB and Polars for data processing, Prophet
with logistic growth as the primary model, SARIMA and ETS as alternatives, a
model tournament using a 32-month train / 4-month MAPE backtest split to select
the champion per series, and Streamlit for internal dashboarding. I validated
the approach completely before committing to cloud infrastructure.

Phase two migrated to AWS: S3 data lake for all inputs and outputs, AWS Glue
with 10 G.2X workers running Spark 3.3, and a PySpark Grouped Map UDF to
distribute Prophet across the worker fleet — one partition per host-resource
pair, one complete independent Prophet fit per UDF call. Gating on yhat_upper
at 95% for breach detection. MLflow for experiment tracking.

Two confidence tiers — three months high-confidence with tight intervals,
six months directional — are explicit in the output design so teams know what
they're acting on versus planning around.

---

### Citi High-Scale Telemetry Pipeline

**What was the scale of the Citi pipeline and what were the key engineering decisions?**

65,000 to 70,000 endpoints worldwide across four regions and dozens of
departments. Four KPIs: CPU, memory, disk, and network — all at P95. Three
data sources: BMC TrueSight (Oracle DB via SQLAlchemy and cx_Oracle), the
Change Management Database on SQL Server (via pyodbc), and AppDynamics for
supplementary server metadata.

The hardest engineering problem: cross-system identifier normalization. Three
sources with independent naming conventions for the same endpoints. I built
normalization rules to produce a canonical hostname key, then used a
priority-order join strategy with enrichment fallback.

Safety factor of 1.15 applied to raw P95, against a 90% ceiling threshold.
Dual SQLite design: monthly databases for per-period detail, master database
for multi-month progression tracking. Process went from 5-10 business days
manually to 1-2 hours automatically. Version-controlled in GitLab,
openpyxl for Excel output, Streamlit for the internal team dashboard.

---

### G6 Hospitality AppMon

**What was the engineering insight on the G6 performance project?**

Dynatrace AppMon was capturing all the right data but the built-in dashboards
couldn't answer the questions the business needed answered. The artifact chain
— HTML, CSS, JavaScript, images, third-party scripts, API calls — was all
instrumented. But "the site is slow" is not actionable. "The checkout flow is
slow specifically on mobile in the midwest and this third-party script is the
dominant contributor" is actionable.

The engineering work was building the extraction pipeline from AppMon,
structuring the data in MySQL with geography and device class as dimensions,
and generating reports that ranked the artifact chain by response time
segmented by those dimensions. P95 rather than average as the reporting metric
— averages hide the tail of slow experiences that matter most for conversion.

The findings drove specific frontend recommendations: deferred loading of
non-critical JS, async loading of third-party head scripts, CDN configuration
review for regional gaps. Response times improved measurably after
implementation.

---

## Career & Motivation

**Why data engineering? What draws you to this field specifically?**

I backed into it from performance engineering and systems work, and what I
found was that the problems I cared most about — how do you make a complex
system visible, how do you turn raw telemetry into a decision, how do you
build something that reliably produces correct output at scale — are exactly
what data engineering is.

The craft of it: designing a pipeline that's idempotent, that fails loudly
rather than silently, that has validated contracts between stages, that scales
horizontally when data grows — that's genuinely interesting engineering. Done
well, it's platform engineering that determines what a business can know about
itself.

What's exciting now is the AI layer on top. Text-to-SQL agents, AI-assisted
data quality, inference pipelines that serve ML models at scale — that's where
I want to be. I've been building at that intersection for two years and it's
where I see the field going.

---

**Where do you see yourself in three to five years?**

In three years: deeply proficient with the modern lakehouse stack —
Databricks, Delta Lake, dbt — in a production environment. Having shipped data
platform work a business relies on, contributed to data contracts and
governance at an organizational level, and built something at the AI-data
intersection I'm genuinely proud of.

In five years: a staff or principal role where I'm influencing platform
architecture decisions, not just executing them, and where my combination of
deep systems background, data engineering experience, and AI/ML work is being
applied to hard problems at real scale. I've been in the room for large-scale
migrations, high-stakes architecture decisions, and performance-critical
systems across a 25-year career. There's a version of the next five years
where that experience becomes an asset for a broader team.

---

**What are you self-studying right now and why?**

Three areas.

Databricks and the lakehouse stack — Delta Lake, Delta Live Tables, Unity
Catalog, Workflows. My core Spark and PySpark work is solid; I'm learning
the Databricks operational layer and the governance model. I know enough to
be productive quickly and I'm honest that the depth comes from production use.

dbt — the SQL transformation layer. I built similar transformations manually
at Citi: multi-stage SQL that cleaned, validated, and aggregated data. dbt
formalizes exactly that pattern with dependency resolution, testing, lineage
documentation, and incremental materialization. I've been practicing with
dbt-duckdb locally. The concepts aren't new — the tooling is.

AI patterns for data engineering: RAG, vector search, LLM integration in data
pipelines, Text-to-SQL. I built a Text-to-SQL agent at Citi using Claude 3
Sonnet and Bedrock. I'm building the job search pipeline with Grok. This isn't
theoretical — I'm writing production code at this intersection.

---

## Strengths & Self-Awareness

**What are your strongest technical areas?**

Three genuine ones, not just claimed.

Production pipeline engineering. Twenty years building systems that can't fail
— telecom billing at Sprint, migration at Sabre, capacity intelligence at Citi.
I think in terms of failure modes first, then correctness, then performance.
Quality gates, idempotency, validation at every stage boundary — deeply
ingrained.

Cross-system data integration. Most of my interesting work has involved joining
data from multiple sources with incompatible identifiers, different update
cadences, and inconsistent data quality. The Citi enrichment join across three
enterprise systems. The G6 analysis across AppMon, geography, and device data.
Making disparate systems speak to each other cleanly is where I've done some
of my best work.

Translating data into decisions. I think carefully about who consumes the
output and what they actually need. The Streamlit dashboards I build look the
way they do because I've thought about the VP who needs to act on this, not
the data engineer who produced it.

---

**What's a genuine weakness or area you're actively working on?**

The modern lakehouse tooling gap is real and I'm honest about it. Databricks
in production, dbt at enterprise scale, event streaming with Kafka or Kinesis —
strong conceptual understanding and active study, but I haven't shipped
production systems with them yet. That's the honest assessment.

What I'd push back on is treating that as disqualifying. I have 20-plus years
of the underlying skills — Python, PySpark, SQL, distributed systems, data
modeling — and I've demonstrated across my career that I ramp quickly on new
tooling by mapping it to what I already know. Glue and PySpark at Citi,
Prophet and FAISS for HorizonScale, Grok and LangChain for the job search
pipeline — each was new and I shipped production work on all of them. The
Databricks and dbt gap is a 3-to-6 month gap with production access, not a
foundational one.

---

**How do you handle ambiguity — when requirements aren't clear?**

I start by identifying which kind of ambiguity it is. If it's unclear what
the business outcome should be, I ask one specific question: what decision
will this output drive, and who makes it? That single answer usually unlocks
the right design direction more than any technical discussion.

If the requirements are clear at the business level but unclear at the
technical level, I build the MVP that validates the approach rather than
designing the full system up front. Phase one of HorizonScale was exactly this:
build locally, prove the tournament works, prove the confidence tiers are
calibrated correctly. Commit to cloud infrastructure only once the approach is
validated.

What I don't do is wait for perfect requirements before starting. Clarify the
most important uncertainty, build to the decision boundary, learn from the
output. Iteration over analysis paralysis.

---

## Questions I Ask Back

Ask at least three. They signal genuine interest, senior thinking, and respect
for the interviewer's knowledge. Never ask about salary or PTO in technical rounds.

1. What does the data engineering team own end-to-end — from raw ingestion to
   serving — and where does the boundary with data science or analytics
   engineering sit?

2. What's the biggest data reliability or quality challenge you're dealing
   with right now?

3. How do you currently handle pipeline observability — what does a data
   engineer know about whether their pipelines ran correctly last night?

4. Is the data platform on a modern lakehouse stack or is there active
   migration work underway? Where are you on that journey?

5. How are data contracts and schema evolution handled between teams — is
   there a formal process or is it coordinated informally?

6. What does the on-call or incident rotation look like for the data team?
   How do data pipeline failures get detected and escalated?

7. What would a successful first 90 days look like for someone in this role —
   what would they have shipped, what would they have learned?

8. How does AI or ML fit into the data team's roadmap — is it a separate team,
   integrated, or somewhere in between?

9. What's the most recent hard technical decision the team made, and how did
   you evaluate the options?

10. What's the thing that would make someone in this role unusually successful —
    beyond the job description?
