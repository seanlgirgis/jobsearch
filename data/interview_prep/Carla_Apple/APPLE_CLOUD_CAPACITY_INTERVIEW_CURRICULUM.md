# Apple Cloud Capacity Interview Curriculum

## 1. Interview Target

This is not just a SQL role and not just a Python role. It is a capacity,
efficiency, telemetry, automation, and cloud-cost role.

Sean's safest positioning:
Senior capacity/data engineer who automates telemetry analysis into capacity and
cost decisions.

## 2. Core Identity Statement

I am strongest where capacity engineering meets data engineering. I use Python,
SQL, telemetry, and forecasting to turn infrastructure metrics into capacity
risk, rightsizing opportunities, and stakeholder-ready reports. My deepest
hands-on cloud is AWS, and I understand how the same capacity principles apply
to Kubernetes, EKS, S3, and multi-cloud environments.

## 3. Automation — What Carla May Mean

1. Data automation
- ingest telemetry
- clean data
- normalize schema
- aggregate by service/team/workload

2. Capacity automation
- P95/headroom calculation
- threshold breach detection
- forecast variance
- risk classification
- rightsizing candidates

3. Cloud/platform automation
- EKS/Kubernetes requests/limits/utilization checks
- S3 storage growth/lifecycle opportunity
- cost and allocation reporting
- tagging/ownership metadata

4. Operational automation
- repeatable scripts
- scheduled reports
- runbooks
- validation checks
- reducing manual spreadsheet work

When I say automation, I mean reducing manual capacity analysis. Instead of
manually pulling telemetry and building one-off reports, I build repeatable
pipelines and scripts that collect metrics, clean them, calculate P95,
headroom, forecast variance, classify risk, and export stakeholder-ready
reports. That same pattern can apply to EC2, ECS, EKS, S3, or Kubernetes
capacity data.

## Automation in Cloud Capacity Work

Automation in this role does not mean only one thing. It can mean data
automation, capacity-risk automation, cloud/platform collection automation, and
reporting/operational automation. The common goal is reducing manual capacity
analysis and turning telemetry into repeatable decisions.

### 1. Data Automation

- collect telemetry
- ingest CSV/Excel exports
- pull from databases or APIs
- normalize column names
- convert dates and numeric fields
- join service ownership, tags, environment, team, account, region, namespace,
  or workload metadata
- produce reusable clean datasets

Interview answer:
Data automation means I do not want analysts manually cleaning the same
telemetry export every time. I would automate the ingestion, cleaning, schema
normalization, ownership tagging, and validation so downstream capacity
calculations are repeatable.

### 2. Capacity-Risk Automation

- calculate AVG / MAX / P95
- calculate headroom
- compare allocated/requested capacity vs actual usage
- detect threshold breaches
- calculate forecast variance
- classify services/workloads as high_capacity_risk, latency_watch,
  rightsizing_candidate, or normal
- generate top-risk or top-waste lists

Interview answer:
Capacity automation means turning raw metrics into decision flags. For example,
the workflow can automatically calculate P95 utilization, headroom, forecast
variance, and cost impact, then classify services or workloads into risk or
rightsizing categories.

### 3. Cloud / Platform Collection Automation

AWS-native or platform sources may include:
- CloudWatch / Container Insights for compute, container, EKS/ECS, pod, node,
  and cluster metrics
- AWS Cost and Usage Report for cost and usage data delivered to S3
- S3 Inventory for bucket/object/storage metadata
- tags and ownership metadata
- centralized collectors such as BMC TrueSight, TSCO, Helix, or similar
  observability/capacity platforms

At Citi, centralized tools such as BMC TrueSight/TSCO/Helix could discover
resources and populate metrics after configuration. Once the resources were
onboarded, the analytics problem became similar to other endpoints: different
columns and rules, but the same pattern of collect, normalize, analyze, and
report.

Interview answer:
If a company already has a centralized platform like BMC/Helix or
CloudWatch/Container Insights, I would use that as the telemetry source where
appropriate. If not, I would use scheduled jobs or native exports. The analysis
pattern is the same: collect the data, normalize it, join ownership metadata,
calculate risk or waste, and report.

### 4. Reporting / Operational Automation

- scheduled scripts
- scheduled Lambda
- scheduled container jobs
- Airflow / Step Functions / batch orchestration
- CSV / Markdown / dashboard exports
- validation checks
- runbook updates
- reducing manual spreadsheet/reporting work

Interview answer:
Reporting automation means the output is not a one-time spreadsheet. The
workflow should create repeatable CSV, Markdown, dashboard, or table outputs
that stakeholders can review consistently.

### 5. Batch First, Streaming Only If Needed

For capacity and cost analytics, batch is usually the default. Streaming is
useful for real-time alerting, but most capacity planning, rightsizing,
forecasting, and cost analysis works from periodic snapshots.

Frequency guidance:
- 1–5 minutes: operational monitoring or alerting
- 5–15 minutes: infrastructure or service telemetry samples
- hourly: capacity rollups and workload pressure trends
- daily: cost usage, rightsizing candidates, S3 inventory, stakeholder reports
- weekly/monthly: forecasting, budget planning, commitment planning, executive
  review

Interview answer:
For capacity and cost analytics, I usually think batch first. We normally do
not need streaming unless the use case is real-time alerting. For planning and
efficiency, periodic snapshots are enough: 5-minute or hourly telemetry, daily
cost files, and scheduled inventory exports.

### 6. Lambda vs Container vs Orchestrator

- Lambda is good for lightweight scheduled pulls or small enrichment jobs.
- A scheduled container job is better for heavier dependencies, larger
  extracts, or longer processing.
- Airflow / Step Functions / batch orchestration is better for multi-step
  workflows: extract, validate, load, transform, report.
- Centralized tools like BMC/Helix/CloudWatch may already handle collection, so
  the automation focus becomes downstream processing and reporting.

Interview answer:
I would choose the automation mechanism based on the workload. Lambda is good
for lightweight scheduled pulls. A container job is better for heavier
dependencies or larger extracts. An orchestrator is better when the workflow
has multiple stages. If a centralized collector already exists, I would use it
and focus automation on validation, transformation, risk classification, and
reporting.

### 7. How Automation Maps to Current Code Lab

- src\db.py handles database connection and query execution
- src	elemetry_queries.py centralizes reusable SELECT queries
- src\capacity_analysis.py calculates flags, summaries, and capacity status
- srceporting.py exports CSV/Markdown outputs
- scripts_export_capacity_summary.py runs the end-to-end workflow
- tests validate connection, SELECT-only safety, and Pandas logic

Answer:
In my lab, the Python side demonstrates the automation pattern. It connects to
PostgreSQL, runs SELECT-only telemetry queries, loads results into Pandas,
calculates capacity summaries and status labels, exports CSV/Markdown reports,
and validates the logic with pytest. In a real environment, the input source
could be BMC/Helix, CloudWatch, CUR, S3 Inventory, or a staging table.

### 8. Fire Drill Q&A

Q: What do you mean by automation?
A: Reducing manual capacity analysis. Automating data collection, cleaning,
P95/headroom/forecast variance calculations, risk classification, and
stakeholder-ready reporting.

Q: Do you need streaming for capacity and cost analytics?
A: Usually no. Capacity planning and cost efficiency usually work from periodic
snapshots, hourly/daily rollups, and historical trends. Streaming is more
useful for alerting.

Q: How would you collect AWS cost data?
A: I would start with AWS Cost and Usage Reports delivered to S3, then process
them with SQL, Python, or Spark and join to tags, accounts, services, and
ownership metadata.

Q: How would you collect EKS metrics?
A: I would use CloudWatch Container Insights or an existing
observability/capacity platform. I would focus on namespace, workload, pod,
node, requests, limits, actual usage, and cost allocation.

Q: How would you collect S3 capacity data?
A: I would use S3 Inventory, cost/usage data, and bucket metadata to analyze
storage growth, object count, storage class, lifecycle opportunity, access
pattern, and cost trend.

Q: Lambda or container for collection?
A: Lambda is good for lightweight scheduled pulls. A container job is better
for heavier dependencies, larger extracts, or longer runtime. An orchestrator
is better for multi-step workflows.

Q: What if the company already has BMC/Helix?
A: Then I would use it as the central telemetry source when appropriate. Once
resources and metrics are onboarded, the analytics pattern is similar to other
endpoints: extract, normalize, join ownership, calculate risk/waste, and
report.

Q: How does this connect to your older physical/virtualization background?
A: The resource model changes, but the capacity method is the same. Physical/VM
work uses servers, VMs, CPU, memory, disk, and endpoint telemetry. Cloud adds
account, region, tags, resource type, requests/limits, storage class, and cost.
The pipeline remains collect, normalize, calculate, classify, and report.

## Cloud Telemetry Collection — Batch First

For capacity and cost analytics, batch is usually the default. We normally do
not need streaming for capacity planning unless there is an operational
alerting use case. Capacity analysis usually works from periodic snapshots:
5-minute samples, hourly rollups, daily cost files, monthly trends, or
scheduled inventory exports.

### AWS Native Sources

- CloudWatch / Container Insights:
  collects compute, ECS, EKS, Kubernetes, container, pod, node, and cluster
  metrics depending on setup.

- AWS Cost and Usage Report:
  publishes detailed cost and usage data to S3, usually used for cost
  allocation, showback, rightsizing analysis, forecasting, and tag-based
  reporting.

- S3 Inventory:
  produces scheduled reports about S3 objects and metadata, useful for storage
  growth, lifecycle policy analysis, storage class review, and cold-data
  identification.

- Tags / ownership metadata:
  account, region, environment, team, application, service, namespace,
  workload.

### Collector Patterns

1. Centralized platform collector:
Examples: BMC TrueSight, TSCO, Helix, CloudWatch, Container Insights.
Once configured, resources are discovered and metrics are populated centrally.
The analytics code consumes these resources like any other endpoint.

2. Scheduled Lambda:
Good for small periodic API pulls or lightweight enrichment.
Could run hourly or daily depending on need.

3. Scheduled container job:
Good for heavier collectors, more dependencies, larger extracts, or jobs that
need more runtime than Lambda.

4. Airflow / Step Functions / batch orchestration:
Good when the process has multiple stages: extract, validate, load, transform,
report.

5. Direct export files:
CSV/Excel exports from BMC/Helix/TSCO or AWS reports. Read with Pandas for
quick analysis, or load to staging tables for repeatable pipelines.

### Frequency Guidance

- 1–5 minutes:
  alerting or operational monitoring, not usually required for planning reports.

- 5–15 minutes:
  service or infrastructure telemetry sampling.

- Hourly:
  capacity rollups, trend tracking, workload pressure checks.

- Daily:
  cost and usage analysis, S3 inventory, rightsizing candidates, stakeholder
  reports.

- Weekly/monthly:
  forecasting, budget planning, commitment planning, executive review.

### Code Impact

The code pattern does not radically change when moving from physical/VM
telemetry to cloud telemetry. The input schema changes.

Physical/VM columns:
server_id, hostname, cpu_utilization_pct, memory_utilization_pct,
disk_utilization_pct, sampled_at.

Cloud columns:
account_id, region, resource_id, resource_type, service_name, tag_team,
tag_env, cost_usd, usage_quantity.

EKS/Kubernetes columns:
cluster_name, namespace, workload_name, pod_name, container_name, cpu_request,
cpu_limit, cpu_usage, memory_request, memory_limit, memory_usage.

S3 columns:
bucket_name, storage_class, object_count, storage_gb, last_accessed_days,
monthly_cost_usd, lifecycle_policy_status.

The same code idea remains:
read data -> normalize columns -> join ownership/tags -> calculate
utilization/headroom/P95/variance/cost -> classify risk or waste -> export
report.

### Interview Answer

For capacity and cost analytics, I usually think batch first. We normally do not need streaming unless the use case is real-time alerting. For planning and efficiency, periodic snapshots are enough: 5-minute or hourly telemetry, daily cost files, and scheduled inventory exports.

In AWS, I would use native sources where possible: CloudWatch and Container Insights for compute/container metrics, Cost and Usage Reports for cost and usage data in S3, and S3 Inventory for storage/object metadata. If enrichment is needed, I would use a scheduled Lambda for lightweight jobs, a scheduled container for heavier collectors, or an orchestrated batch workflow for multi-step pipelines.

At Citi, the same pattern existed through centralized tools like BMC TrueSight/TSCO and later Helix. Once configured, the system discovered resources and populated metrics. From the analytics side, it became the same problem: different columns and rules, but the same decision loop — collect, normalize, calculate headroom/P95/variance/cost, classify risk or waste, and report.

### Fire Drill Questions To Add

Q: Do you need streaming for cloud capacity analysis?
A: Usually no. Capacity planning is normally batch-oriented. Streaming is useful
for alerting, but planning and efficiency usually work from periodic snapshots,
hourly/daily rollups, and historical trends.

Q: How would you collect AWS cost data?
A: I would start with AWS Cost and Usage Reports delivered to S3, then process
them with SQL/Python/Spark depending on scale. I would join cost data to tags,
accounts, services, and ownership metadata.

Q: How would you collect EKS metrics?
A: I would use CloudWatch Container Insights or an existing observability
platform if already configured. I would focus on namespace, workload, pod,
node, requests, limits, actual usage, and cost allocation.

Q: How would you collect S3 capacity data?
A: I would use S3 Inventory or cost/usage exports to analyze bucket growth,
object count, storage class, lifecycle opportunity, and cost trend.

Q: What if the company already has BMC/Helix?
A: Then I would use it as the central telemetry source when appropriate. Once
resources and metrics are onboarded, the analytics pattern is similar to other
endpoints: extract the data, normalize it, join ownership, calculate risk or
waste, and report.

Q: Lambda or container for collection?
A: Lambda is good for lightweight scheduled pulls. A container job is better for
heavier dependencies, longer runtime, larger data extracts, or more complex
processing.

## 4. HorizonScale — Code Walkthrough

- Inputs:
  CPU, memory, P95 latency/utilization, requests, forecast, allocated capacity,
  actual usage, cost, ownership/service metadata.

- Code flow:
  1. read telemetry
  2. clean/normalize
  3. convert date/numeric fields
  4. calculate headroom
  5. calculate P95
  6. calculate forecast variance
  7. group by service/workload
  8. classify status
  9. export report/action list

- Outputs:
  capacity risk list
  rightsizing candidates
  forecast misses
  cost/efficiency report
  stakeholder summary

The code side of HorizonScale was a telemetry-to-decision pipeline. I pulled
infrastructure metrics, cleaned and normalized the data, calculated features
like P95 utilization, headroom, forecast variance, and utilization trends, then
grouped by service or workload to classify capacity risk and rightsizing
opportunities. The value was the repeatable decision loop, not just one
dashboard.

## 5. SQL Coverage

- 01 basic selects:
  table inspection, filtering, simple joins
- 02 joins/group by:
  service/host readable telemetry, grouped summaries
- 03 capacity aggregation:
  AVG, MAX, P95, DATE_TRUNC, cost and risk rollups
- 04 window functions:
  ROW_NUMBER, RANK, LAG, LEAD, moving averages
- 05 interview questions:
  mixed SQL problem solving
- 06 server rollup:
  5-minute samples to hourly capacity rollups, CTEs, JSONB, P95, LAG/RANK

In SQL, I can move from raw telemetry samples to service-level capacity views
using JOIN, GROUP BY, DATE_TRUNC, P95 calculations, CTEs, and window functions.

## 6. Python Coverage

- db connection helper
- SELECT-only query layer
- Pandas capacity analysis
- status classification
- CSV/Markdown report export
- pytest validation

In Python, I built a small layer over PostgreSQL that runs telemetry queries,
loads results into Pandas, calculates flags and service summaries, classifies
capacity status, exports reports, and validates the logic with pytest.

## 7. Kubernetes / EKS Capacity Concepts

Conceptually prepared, without claiming deep production platform ownership:
- pods
- nodes
- namespaces
- requests
- limits
- actual usage
- over-requesting
- underutilization
- autoscaling
- bin packing
- cluster headroom
- noisy workload
- cost allocation by namespace/team

### Kubernetes Capacity Granularity

Kubernetes capacity should not be analyzed only at the cluster level. It should
be analyzed at multiple grains, because each grain answers a different
question.

Container level:
Best for exact rightsizing.
Question: Is this container requesting too much or too little CPU/memory?

Pod/workload level:
Best for application capacity.
Question: Is this deployment, job, or service sized correctly?

Namespace/team level:
Best for ownership, showback, and cost allocation.
Question: Which team or namespace is consuming or wasting capacity?

Node/cluster level:
Best for infrastructure capacity.
Question: Does the cluster have enough headroom? Are nodes underused or
saturated? Is autoscaling pressure caused by real usage or inflated requests?

Kubernetes is elastic, but elasticity does not remove the need for rightsizing.
Inflated requests can waste money and reduce bin-packing efficiency.
Underestimated requests or usage close to limits can create throttling, OOM
risk, or reliability issues.

CPU request utilization = cpu_usage_cores / cpu_request_cores * 100
Memory request utilization = memory_usage_gb / memory_request_gb * 100
CPU request waste = cpu_request_cores - cpu_usage_cores
Memory request waste = memory_request_gb - memory_usage_gb

I would not calculate Kubernetes capacity only at the cluster level. I would
look at multiple grains. Container and workload level are best for rightsizing
because that is where requests, limits, and actual usage can be compared.
Namespace and team level are best for ownership and cost reporting. Cluster
level is best for total headroom, node utilization, autoscaling pressure, and
bin-packing efficiency. Kubernetes is elastic, but inflated requests can still
waste money and hurt bin packing, while usage close to limits can create
reliability risk.

For EKS or Kubernetes capacity, I would look at requested CPU/memory versus
actual usage, namespace and workload ownership, pod and node utilization,
autoscaling behavior, and cluster headroom. The same data method applies:
collect metrics, group by workload or namespace, calculate P95 and headroom,
identify over-requesting or saturation, and turn it into scaling or rightsizing
recommendations.

## 8. S3 Capacity / Cost Concepts

- storage growth
- bucket/object count
- storage class
- lifecycle policies
- access patterns
- old/cold data
- replication
- data transfer
- cost trend

For S3, capacity and efficiency are less about CPU and more about storage
growth, access pattern, lifecycle opportunity, storage class, replication, and
data transfer cost. I would look for fast-growing buckets, rarely accessed
objects, missing lifecycle policies, and ownership/tagging gaps so teams can
reduce waste without risking availability.

## 9. Cost Savings / Efficiency Playbook

1. Find waste
2. Validate with telemetry
3. Attach ownership
4. Estimate impact
5. Recommend action
6. Track result

Examples:
- underutilized compute
- over-requested Kubernetes workloads
- oversized memory allocation
- cold S3 data without lifecycle
- idle or low-traffic services
- high-cost services with low usage
- forecast over-allocation

I do not start by randomly cutting resources. I start with telemetry and
ownership. I look for low utilization, low headroom risk, over-allocation, or
storage lifecycle opportunities. Then I validate with service owners and turn
the finding into a safe action: rightsize, scale down, add lifecycle policy,
rebalance, or monitor.

## 10. Interview Runbook — 45 Minutes

- 0-5 minutes: opening and background
- 5-15 minutes: capacity/telemetry story
- 15-25 minutes: automation and HorizonScale code
- 25-35 minutes: SQL/Python/cloud capacity discussion
- 35-42 minutes: Kubernetes/EKS/S3/cost efficiency questions
- 42-45 minutes: questions for them and close

## 11. Interview Runbook — 30 Minutes

- 0-3 opening
- 3-10 strongest capacity story
- 10-18 technical drill
- 18-25 cloud/cost/automation discussion
- 25-30 questions and close

## 12. Fire Drill Questions

1. What do you mean by automation?
- I mean replacing manual telemetry pulls and one-off spreadsheets with
  repeatable scripts/pipelines that generate decision-ready outputs.

2. How did HorizonScale work in code?
- Pull telemetry, clean/normalize, compute P95/headroom/variance, classify risk,
  group by service/workload, export recommendations.

3. How do you calculate capacity risk?
- Combine utilization, latency, error rates, headroom, and forecast variance;
  then rank by severity and ownership.

4. Why P95 instead of average?
- Average hides stress behavior. P95 better reflects sustained high pressure and
  user-impact risk.

5. How would you analyze EKS cost?
- Compare requested vs actual CPU/memory by namespace/workload, evaluate
  over-requesting, autoscaling behavior, and ownership mapping.

6. How would you analyze S3 cost?
- Track growth, access pattern, storage class, lifecycle gaps, replication, and
  transfer costs; then prioritize safe optimization actions.

7. How do you find rightsizing candidates?
- Identify sustained low utilization with safe headroom, validate with owners,
  and recommend phased changes.

8. What did you actually build in Python?
- A DB query layer, pandas analysis/flags, service summarization, status
  classification, CSV/Markdown exports, and pytest validation.

9. What SQL would you use for telemetry rollups?
- JOIN + GROUP BY + DATE_TRUNC + percentile functions + CTEs/window functions
  when needed for ranking or trend comparison.

10. What if you do not have deep GCP?
- My hands-on depth is strongest in AWS. I apply transferable capacity methods
  across cloud platforms without over-claiming ownership.

11. How do you validate forecasts?
- Back-testing, forecast-vs-actual comparison, variance analysis, and SME review
  of false positives/negatives.

12. How do you communicate risk to stakeholders?
- Translate metrics into risk, impact, owner, recommended action, and expected
  timeline.

13. What would you automate first in this role?
- A repeatable telemetry-to-risk pipeline with ownership tagging and recurring
  service-level rollups.

14. How do you avoid unsafe cost cuts?
- Require utilization/headroom evidence, owner signoff, phased rollout, and
  post-change validation.

15. How do you handle missing or messy telemetry?
- Document gaps, normalize what is available, add validation checks, and build
  a prioritized telemetry quality backlog.


Q: Do you calculate Kubernetes capacity only at the cluster level?
A: No. I look at multiple grains. Container/workload level is best for
rightsizing, namespace/team level is best for ownership and cost, and cluster
level is best for headroom, autoscaling pressure, and bin-packing efficiency.

Q: Why does container-level data matter if Kubernetes is elastic?
A: Because autoscaling still depends on requests, limits, and actual usage. If
requests are inflated, the cluster may scale unnecessarily or pack workloads
inefficiently. If usage is close to limits, the workload may throttle or become
unstable.
## 13. Questions To Ask Them

- What are the main capacity signals your team trusts today?
- Are the biggest efficiency opportunities in compute, Kubernetes, storage, or
  data transfer?
- How do you currently connect telemetry to ownership and cost?
- What automation exists today, and where is the manual pain?
- How do you measure success for this role in the first 90 days?

## 14. Things To Avoid

- Do not claim deep Kubernetes production ownership.
- Do not claim deep GCP production ownership.
- Do not say it was only physical infrastructure.
- Do not say HorizonScale was just a dashboard.
- Do not imply finance ownership of billing systems.
- Do not over-focus on old APM unless tying it to telemetry/capacity.

## 15. Final 60-Second Close

My strongest match is capacity planning at scale with automation. I have worked
with large infrastructure telemetry, Python, SQL, forecasting, and cloud-style
data pipelines to turn raw metrics into risk, rightsizing, and planning
recommendations. My deepest hands-on cloud is AWS, and I am careful to separate
platform ownership from transferable capacity principles. What I bring is the
ability to automate the decision loop: collect telemetry, calculate utilization
and headroom, identify risk or waste, and produce recommendations that
engineering and leadership can act on.
