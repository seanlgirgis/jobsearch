# Interview Cram - Personal + Projects (Combined)

<a id="toc"></a>
## Table of Contents
1. [Q1) What was the business problem, and why wasn't AppMon alone enough?](#sec-1)
2. [Q2) Walk through the pipeline in 5 steps.](#sec-2)
3. [Q3) Why did geography/device segmentation matter?](#sec-3)
4. [Q4) Why P95 (and P99) vs average?](#sec-4)
5. [Q5) Give one optimization and business effect.](#sec-5)
6. [Q6) Biggest leadership contribution?](#sec-6)
7. [Q1) What problem did it solve and what value did it create?](#sec-7)
8. [Q2) Architecture in 5 steps.](#sec-8)
9. [Q3) Why local FAISS before LLM?](#sec-9)
10. [Q4) Why two-tier model strategy?](#sec-10)
11. [Q5) What is the quality gate and why blocking?](#sec-11)
12. [Q6) What would you change if rebuilding?](#sec-12)
13. [Q1) Core problem and risk?](#sec-13)
14. [Q2) Pipeline architecture in 5 steps.](#sec-14)
15. [Q3) Why enrichment mattered as much as telemetry?](#sec-15)
16. [Q4) Why 1.15 safety factor and 90% ceiling?](#sec-16)
17. [Q5) Hardest technical challenge and solution?](#sec-17)
18. [Q6) Measurable impact beyond speed?](#sec-18)
19. [Q1) What problem did HorizonScale solve and why forecasting over threshold alerts?](#sec-19)
20. [Q2) Why model tournament instead of one global model?](#sec-20)
21. [Q3) Why Prophet logistic growth?](#sec-21)
22. [Q4) Why 3-month high-confidence and 6-month directional tiers?](#sec-22)
23. [Q5) How did you scale Prophet in AWS Glue?](#sec-23)
24. [Q6) Key migration lesson (Phase 1 to Phase 2)?](#sec-24)
25. [Q1) Tell me about yourself (60 sec)](#sec-25)
26. [Q2) Why did you leave Citi and why now?](#sec-26)
27. [Q3) Why Toyota Financial Services specifically?](#sec-27)
28. [Q4) Biggest weakness?](#sec-28)
29. [Q5) Top strengths for this role](#sec-29)
30. [Q6) Dynatrace/AppMon experience (45 sec)](#sec-30)
31. [Story 1) Solved a problem at unfamiliar scale (HorizonScale)](#sec-31)
32. [Story 2) System failed and response (Citi schema drift)](#sec-32)
33. [Story 3) Delivered change in team operations (G6 observability)](#sec-33)
34. [Story 4) Convinced team to change direction (incremental vs full reload)](#sec-34)
35. [Story 5) Improved accepted process (manual telemetry reporting -> automated ETL)](#sec-35)
36. [Toyota opener (Why Toyota?)](#sec-36)
37. [One-line memory hooks](#sec-37)

## Topic 1: G6 Hospitality (Dynatrace AppMon)

<a id="sec-1"></a>
### Q1) What was the business problem, and why wasn't AppMon alone enough?
G6's direct-booking site had conversion impact from performance issues, but pain varied by region, device, and transaction step. AppMon captured rich telemetry, but built-in dashboards were too rigid for cross-dimensional analysis. We built a custom analytics layer on top of AppMon exports to produce segmented, actionable insights.
[Back to TOC](#toc)





<a id="sec-2"></a>
### Q2) Walk through the pipeline in 5 steps.
1. Extract AppMon telemetry on schedule with dimensions: timestamp, transaction, artifact, geo, device, status.
2. Validate completeness and flag incomplete records.
3. Load validated records into MySQL raw tables.
4. Build summary tables with P95/P99, error rates, and segmentation.
5. Publish targeted reports (artifact slowdown, geo map, mobile-vs-desktop, weekly trend).


[Back to TOC](#toc)


<a id="sec-3"></a>
### Q3) Why did geography/device segmentation matter?
Global averages hid real issues. Device segmentation exposed mobile-specific JS/rendering pain; geography exposed regional latency/CDN gaps. Different causes required different fixes.



[Back to TOC](#toc)

<a id="sec-4"></a>
### Q4) Why P95 (and P99) vs average?
Average hides user pain because fast requests dilute slow ones. P95 captures the slow tail that affects user experience and conversion. P99 helps deeper investigation of extreme latency.


[Back to TOC](#toc)


<a id="sec-5"></a>
### Q5) Give one optimization and business effect.
Heavy JavaScript bundles were major bottlenecks, especially on mobile. The team reduced bundle weight, deferred non-critical scripts, and optimized delivery paths. Result: sustained improvement in performance metrics and booking flow experience.



[Back to TOC](#toc)

<a id="sec-6"></a>
### Q6) Biggest leadership contribution?
I reframed the effort from ad hoc reporting to a scalable analytics capability, scoped the pipeline and reporting model, aligned stakeholders, and got approval for implementation.

---

## Topic 2: AI-Powered Job Search Pipeline


[Back to TOC](#toc)


<a id="sec-7"></a>
### Q1) What problem did it solve and what value did it create?
Senior job search is operationally expensive: role triage, tailoring, research, and tracking duplicates. I built an AI-assisted pipeline to reduce cycle time and decision fatigue while keeping human review in control. Value: speed, consistency, and better decision quality.


[Back to TOC](#toc)


<a id="sec-8"></a>
### Q2) Architecture in 5 steps.
1. Intake + local FAISS duplicate gate.
2. RAG fit scoring against career profile (accept/pass).
3. Structured tailoring to job YAML + tailored resume JSON.
4. Company research + cover letter JSON + DOCX rendering.
5. Blocking quality gate before status is set to applied.


[Back to TOC](#toc)


<a id="sec-9"></a>
### Q3) Why local FAISS before LLM?
It blocks reposted roles early, saves cost/time, and protects privacy. No external API call is needed to make duplicate decisions.



[Back to TOC](#toc)

<a id="sec-10"></a>
### Q4) Why two-tier model strategy?
Use smaller model for structured/light tasks and full model for high-stakes generation. This preserves quality where needed while reducing per-job cost.


[Back to TOC](#toc)


<a id="sec-11"></a>
### Q5) What is the quality gate and why blocking?
It verifies required files exist, are not truncated, and pass baseline checks before marking applied. Blocking prevents silent bad output. Human review remains final control.



[Back to TOC](#toc)

<a id="sec-12"></a>
### Q6) What would you change if rebuilding?
Use SQLite from day one for queryability, and formal stage contracts (Pydantic/JSON Schema) to catch schema drift early.

---

## Topic 3: Citi High-Scale Telemetry Pipeline


[Back to TOC](#toc)


<a id="sec-13"></a>
### Q1) Core problem and risk?
Manual monthly capacity reporting for 65K+ endpoints across four regions took 5-10 days using Excel-heavy workflows. In a banking environment, delayed/inconsistent capacity signals create operational and compliance risk.



[Back to TOC](#toc)

<a id="sec-14"></a>
### Q2) Pipeline architecture in 5 steps.
1. Validate + ingest from TrueSight (Oracle), CMDB (SQL Server), AppDynamics.
2. Normalize identifiers to canonical hostname key.
3. Join + enrich (CMDB primary, AppDynamics fallback, flag unmatched).
4. Calculate adjusted utilization (P95 x 1.15) vs 90% ceiling; classify endpoint health.
5. Load idempotently into monthly + master SQLite and publish Excel + Streamlit outputs.


[Back to TOC](#toc)


<a id="sec-15"></a>
### Q3) Why enrichment mattered as much as telemetry?
Telemetry shows what is hot/idle; enrichment shows who owns it and where. Without ownership context, alerts are not actionable.



[Back to TOC](#toc)

<a id="sec-16"></a>
### Q4) Why 1.15 safety factor and 90% ceiling?
They create conservative early warning and preserve response lead time. Teams act before systems hit hard limits.


[Back to TOC](#toc)


<a id="sec-17"></a>
### Q5) Hardest technical challenge and solution?
Cross-system identifier normalization. I cataloged naming patterns, built canonical rules, collaborated with source teams, and tracked join coverage as a quality metric.



[Back to TOC](#toc)

<a id="sec-18"></a>
### Q6) Measurable impact beyond speed?
Beyond 5-10 days to 1-2 hours, outputs became deterministic and more trusted. Teams acted earlier on risk and identified under-utilization savings more confidently.

---

## Topic 4: HorizonScale (Time-Series Forecasting at Scale)

[Back to TOC](#toc)



<a id="sec-19"></a>
### Q1) What problem did HorizonScale solve and why forecasting over threshold alerts?
Threshold alerts are reactive and often too late. HorizonScale forecasted six months ahead across 65,000+ host-resource series so teams had lead time for procurement, scaling, and architecture actions before incidents.
[Back to TOC](#toc)




<a id="sec-20"></a>
### Q2) Why model tournament instead of one global model?
Fleet behavior is heterogeneous. Prophet, SARIMA, ETS, and XGBoost each fit different series patterns. We backtested per series and selected a champion model (lowest MAPE), improving trust and risk-signal quality.


[Back to TOC](#toc)


<a id="sec-21"></a>
### Q3) Why Prophet logistic growth?
Utilization is physically bounded (0 to 100%). Linear trends can forecast impossible values (for example 110% CPU). Logistic mode with cap/floor produced realistic forecasts and meaningful breach intervals.



[Back to TOC](#toc)

<a id="sec-22"></a>
### Q4) Why 3-month high-confidence and 6-month directional tiers?
Uncertainty grows with horizon. Months 1-3 supported concrete actions; months 4-6 supported planning and budgeting. This prevented overconfidence in long-range point estimates.


[Back to TOC](#toc)


<a id="sec-23"></a>
### Q5) How did you scale Prophet in AWS Glue?
Used Spark Grouped Map UDF by (node_name, resource). Each worker fit one independent series in parallel, no shared state. Results were written to S3 Parquet for Athena and dashboard consumption.


[Back to TOC](#toc)


<a id="sec-24"></a>
### Q6) Key migration lesson (Phase 1 to Phase 2)?
Validate model design locally first, then scale in cloud. Phase 1 proved tournament logic and thresholds; Phase 2 focused on throughput and operations.

---

## Topic 5: General Interview (Interview Master)



[Back to TOC](#toc)

<a id="sec-25"></a>
### Q1) Tell me about yourself (60 sec)
I'm Sean Girgis, a Senior Data Engineer and Python platform engineer with 20+ years in enterprise systems, including eight years at Citi. I specialize in reliable data pipelines, forecasting platforms, and cloud-native automation at scale. I replaced a 5-10 day manual capacity process with a deterministic pipeline across 65,000+ endpoints, built ML forecasting with Prophet/PySpark/AWS, and developed HorizonScale for 65,000+ series forecasting. I'm now looking for a role where I can bring that same Python + AWS + platform engineering depth in a modern data environment.



[Back to TOC](#toc)

<a id="sec-26"></a>
### Q2) Why did you leave Citi and why now?
I had a strong eight-year run and delivered the major goals of the role. The position reached a natural ceiling, and I wanted to move closer to modern cloud-native data platform work and reusable engineering frameworks.

[Back to TOC](#toc)



<a id="sec-27"></a>
### Q3) Why Toyota Financial Services specifically?
TFS combines enterprise-scale engineering with long-term, disciplined operating culture. The role aligns with my strengths in Python platforms, ETL quality systems, AWS architecture, and enabling teams with reliable tooling.
[Back to TOC](#toc)




<a id="sec-28"></a>
### Q4) Biggest weakness?
Deep production experience with certain modern lakehouse tools (Databricks/dbt/Snowflake) is still growing. I have strong foundations (PySpark, SQL, AWS) and I close gaps by building hands-on projects quickly and systematically.


[Back to TOC](#toc)


<a id="sec-29"></a>
### Q5) Top strengths for this role
1. Reliable Python data platform engineering at large scale (Citi 65,000+ endpoints).
2. Cross-system enterprise integration (Oracle, SQL Server, AppDynamics, AWS).
3. Dynatrace observability depth: built AppMon analytics pipeline at G6 for geo/device/flow-level bottleneck detection and optimization guidance.


[Back to TOC](#toc)


<a id="sec-30"></a>
### Q6) Dynatrace/AppMon experience (45 sec)
At G6, Dynatrace AppMon captured strong telemetry, but built-in dashboards were not enough for cross-dimensional decisions. I built an extraction and analytics layer that segmented performance by geography, device type, and transaction/artifact chain, then surfaced P95 bottlenecks and trends. That produced actionable optimization priorities like deferring non-critical JavaScript, async third-party scripts, and regional delivery/CDN improvements.

---

## Topic 6: Behavioral Stories (Toyota HM)


[Back to TOC](#toc)


<a id="sec-31"></a>
### Story 1) Solved a problem at unfamiliar scale (HorizonScale)
- Situation: Needed 180-day forecasting across tens of thousands of servers / 65,000+ time series.
- Task: Build a trusted forecasting system at fleet scale.
- Action: Built model tournament (Prophet, SARIMA, Holt-Winters/XGBoost path), selected champion per series by backtest metric, added observability for model selection transparency.
- Result: Shifted from reactive/manual forecasting to proactive capacity planning at fleet scale.



[Back to TOC](#toc)

<a id="sec-32"></a>
### Story 2) System failed and response (Citi schema drift)
- Situation: A monthly capacity run completed successfully, but enrichment joins failed for a subset of endpoints and part of the output was wrong.
- Task: Identify root cause fast, correct report safely, and prevent silent bad output.
- Action: Traced issue to an edge case in hostname normalization across source systems; fixed transform logic, reran pipeline, added row-count checks, required-column checks, join-coverage thresholds, and explicit unmatched-endpoint flags.
- Result: Corrected report delivered quickly; future runs became more reliable; team shifted from "pipeline ran" to "pipeline proved data correctness."


[Back to TOC](#toc)


<a id="sec-33"></a>
### Story 3) Delivered change in team operations (G6 observability)
- Situation: Alert fatigue; ops ignored noisy alerts.
- Task: Build an observability output the ops team could trust.
- Action: Designed around ops decisions (not raw telemetry), reduced to high-signal alerts, added synthetic monitoring, created single source dashboard for standups.
- Result: Alert fatigue dropped; team adopted dashboard as daily operating system.


[Back to TOC](#toc)


<a id="sec-34"></a>
### Story 4) Convinced team to change direction (incremental vs full reload)
- S (Situation): Team leaned toward hourly full reload for simplicity under deadline pressure.
- T (Task): Prevent future cost/performance failure while keeping team alignment.
- A1 (Action): Built a growth/cost projection and showed likely Q3 runtime and spend impact.
- A2 (Action): Framed it as risk visibility and offered to own incremental design complexity.
- R (Result): Team switched to incremental; later handled major volume growth at much lower cost.


[Back to TOC](#toc)


<a id="sec-35"></a>
### Story 5) Improved accepted process (manual telemetry reporting -> automated ETL)
- S (Situation): Monthly capacity reporting at Citi was manual and Excel-heavy, taking 5-10 business days.
- T (Task): Convert it into a reliable, repeatable process and free team time for analysis.
- A1 (Action): Built Python ETL for extraction, normalization, enrichment, calculation, and report generation.
- A2 (Action): Added validation gates and idempotent reruns to make data quality provable.
- R (Result): Reduced cycle time to ~1-2 hours; improved consistency across 65,000+ endpoints; shifted team to proactive planning.


[Back to TOC](#toc)


<a id="sec-36"></a>
### Toyota opener (Why Toyota?)
"Toyota Financial Services enables mobility access at scale, and I want to build reliable data/platform systems that make that mission execute safely, quickly, and consistently."



[Back to TOC](#toc)

<a id="sec-37"></a>
### One-line memory hooks
- HorizonScale: "Curiosity before code; tournament across 65,000+ series."
- Citi failure: "Run completed, output was wrong; fixed join edge case and added hard validation gates."
- G6: "Three high-signal alerts beat 300 noisy alerts."
- Incremental design: "I showed the numbers, not an argument."
- Process improvement: "5-10 days manual Excel to 1-2 hours automated ETL."



[Back to TOC](#toc)

