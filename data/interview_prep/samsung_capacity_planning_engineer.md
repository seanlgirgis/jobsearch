# Samsung Austin Semiconductor — Capacity Planning Engineer
**Recruiter:** Robyn Wentworth (r.wentworth@samsung.com · 512.516.0181)
**Stage:** Phone screen → Hiring Manager interview
**Location:** Taylor, TX (on-site)
**Applied:** 2026-04-14 via LinkedIn | **Score:** 90%
**Job Folder:** `data/applied_jobs/00060_7c453502/`

---

## The Key Reframe: IT Capacity → FAB Capacity

Samsung does **semiconductor factory capacity planning**. You did **IT infrastructure capacity planning**. The domain differs. The analytical DNA is identical.

| Samsung FAB | Your CITI / HorizonScale |
|-------------|--------------------------|
| Wafer tools are bottlenecks | Servers/endpoints are bottlenecks |
| Tool utilization % | CPU/memory utilization P95 |
| Lot starts / WIP movement | Pipeline throughput / queue depth |
| Factory Physics (Little's Law) | Queuing theory in telemetry pipelines |
| Capacity gap analysis | Forecasting capacity shortfalls 6 months ahead |
| Long-range capacity planning | HorizonScale 6-month ML forecasting |
| Supply chain constraints | Resource availability forecasting |
| Engineering + Production coordination | Cross-team capacity reporting at Citi |

**Lead with the methodology and outcomes. Let them see the transfer.**

---

## Your Opening 2 Minutes (Samsung Version)

> "I'm a Senior Capacity and Data Engineer with 20+ years of experience,
> and the core of my work for the last 8 years at Citi was exactly what
> this role is about — capacity planning, bottleneck analysis, and
> forecasting at enterprise scale.
>
> I designed and operated capacity planning systems across 6,000+
> infrastructure endpoints using BMC TrueSight Capacity Optimization —
> that's the Helix platform — pulling P95 telemetry, identifying
> constraints, and forecasting demand 6 months ahead using ML models
> built with Prophet and scikit-learn.
>
> Most recently I built HorizonScale — an AI-driven capacity forecasting
> engine I designed from scratch. It replaced manual forecasting cycles,
> cut cycle time by 90%, and generated automated bottleneck risk reports
> that flag assets before they hit capacity thresholds.
>
> The Samsung role maps directly to that work — the tools in a fab are
> the bottlenecks, the methodology is the same: analyze utilization,
> forecast constraints, quantify risk, drive action. That's what I do."

*(Target: 90 seconds. Hits: BMC TrueSight, HorizonScale, 6-month forecasting, bottleneck analysis, 6,000+ endpoints)*

---

## Salary

Samsung posted range: **$70,480 – $179,090** (base + bonus, no RSU)
Austin/Taylor market for senior capacity planning with ML depth: **$145K–$160K**

**Your number: $145,000–$160,000 base**
> "I'm targeting a base in the range of $145,000 to $160,000.
> I understand Samsung structures comp as base plus bonus without RSUs,
> and I'm open to discussing the full package."

---

## Your 4 Key Stories (Samsung Framing)

### Story 1 — BMC TrueSight Capacity Optimization (Your Anchor Story)
**Situation:** Citi needed to manage capacity across 6,000+ infrastructure endpoints — servers, storage, network — feeding a live BMC TrueSight (Helix) environment.
**Task:** Build a scalable data pipeline to collect, clean, and analyze P95 telemetry from TSCO and surface capacity constraints before they impacted operations.
**Action:** Designed Python + Pandas pipelines ingesting TrueSight telemetry, integrated CMDB metadata, built Oracle data warehouse schemas for historical trending, and created dashboards for capacity review by leadership.
**Result:** Automated what was previously manual analysis. Capacity risk flagged weeks ahead of threshold breach. Reports consumed by both engineering teams and senior leadership at Citi.

> *Use when asked: "Tell me about your capacity planning experience" / "Have you worked with BMC TrueSight?"*

---

### Story 2 — HorizonScale: ML Forecasting Engine (Your Flagship)
**Situation:** Manual forecasting cycles at Citi were slow, reactive, and couldn't scale across thousands of endpoints. No predictive signal — teams were always behind the curve.
**Task:** Replace manual capacity forecasting with an automated, ML-driven system that predicted bottlenecks before they occurred.
**Action:** Built HorizonScale from scratch — PySpark telemetry pipeline ingesting time-series data at banking scale, Prophet time-series models for trend decomposition and 6-month forecasting, scikit-learn classifiers identifying assets at risk of capacity breach. Streamlit dashboard for real-time interactive capacity views. Generator-based parallel pipeline architecture that cut processing cycles 90%.
**Result:** 6-month ahead bottleneck prediction with 90%+ accuracy. Leadership could see capacity risk by resource class, region, and time horizon. Cycle time from data to insight dropped from days to minutes.

> *Use when asked: "Tell me about ML in capacity planning" / "Describe a forecasting project" / "Your most impactful project"*

---

### Story 3 — Bottleneck Investigation & Constraint Removal
**Situation:** Regular capacity reviews at Citi revealed recurring bottlenecks in specific server tiers — but root cause was unclear. Was it growth? Inefficiency? Bad allocation?
**Task:** Identify whether bottlenecks were structural (capacity gap) or operational (utilization inefficiency) and drive targeted action.
**Action:** Built SQL-heavy analytical queries over P95 utilization history to segment endpoints by utilization pattern — over-utilized, under-utilized, spiky vs. flat. Correlated with CMDB application/team metadata. Identified clusters of under-utilized servers alongside over-utilized ones in the same tier — a scheduling and allocation gap, not a capacity gap.
**Result:** Rebalancing recommendation quantified with data. Infrastructure spend avoided on net-new hardware. Engineering teams given actionable data instead of "buy more."

> *Use when asked: "Tell me about bottleneck analysis" / "How do you approach capacity gaps?" / "Supply chain or resource constraint examples"*

---

### Story 4 — Cross-Team Capacity Coordination
**Situation:** At Citi, capacity decisions required alignment between infrastructure engineering, application teams, finance, and procurement — each with different views of the same data.
**Task:** Create a shared capacity planning view that all stakeholders trusted and could act from.
**Action:** Built a unified capacity reporting layer pulling from TSCO, CMDB, and project intake data. Standardized definitions (what counts as "at capacity," what triggers a procurement cycle). Ran monthly capacity review sessions with engineering leads, presenting automated bottleneck reports with risk tiers and recommended actions.
**Result:** Forecasting became proactive across teams. Procurement cycles aligned to 6-month forecasting horizon. Eliminated surprises in hardware planning.

> *Use when asked: "Cross-functional coordination" / "Stakeholder management" / "How do you drive action from data?"*

---

## Capacity Planning — Deep Topic Q&A

### "Walk me through how you approach a capacity analysis."
> "I start by defining the resource and the constraint — what are we measuring, and
> what is the threshold that represents a problem? For infrastructure it's CPU/memory
> P95; for a fab it's tool utilization rate and WIP queue depth.
>
> Then I pull historical utilization data — ideally 12–24 months — and decompose the
> trend: is it growing linearly, seasonally, or spiking under specific conditions?
>
> From that I build a forecast — either statistical (moving average, regression) or
> ML-based (Prophet for time-series) depending on the volatility. The forecast gives
> me the expected crossover point where demand exceeds capacity.
>
> Then I calculate the gap: what's the delta between projected demand and available
> capacity at that horizon? Is it addressable through efficiency improvements or does
> it require net-new capacity?
>
> Finally I quantify the options and present risk-tiered recommendations — do nothing,
> optimize utilization, or procure — with cost and lead time for each."

---

### "What is Factory Physics and how do you apply it?"
> "Factory Physics is the study of how manufacturing systems behave under load —
> specifically the relationships between WIP, throughput, and cycle time.
>
> The foundational relationship is Little's Law: throughput equals WIP divided by
> cycle time. If you know any two of those, you know the third.
>
> In a fab context, this means you can calculate the maximum theoretical throughput
> of a bottleneck tool given its utilization rate, and then model what happens to
> cycle time as WIP builds up upstream. The closer a tool runs to 100% utilization,
> the exponentially worse cycle time gets — that's the nonlinear behavior Factory
> Physics captures.
>
> I applied the same principles in IT capacity — queuing theory tells you that a
> server at 90% utilization behaves very differently from one at 70%, even though
> the utilization gap looks small. The math translates directly."

---

### "How do you calculate resource capacity and utilization?"
> "Utilization = actual output / theoretical maximum capacity × 100%.
>
> For IT: a server's theoretical max is 100% CPU over a period. P95 utilization
> tells me what the realistic peak demand looks like — the 95th percentile cuts
> out noise and transient spikes.
>
> For available capacity headroom: headroom = threshold - current P95. If threshold
> is 80% and P95 is 72%, I have 8 points of headroom.
>
> For time-to-capacity: using the growth slope from historical trending, I project
> when P95 will cross the threshold. If it's growing 1.5 points per quarter and
> I have 8 points of headroom, that's roughly 5 quarters before breach — that's
> my planning horizon.
>
> I also calculate effective capacity after accounting for scheduled downtime,
> maintenance windows, and planned outages — raw theoretical capacity is rarely
> the real number to plan against."

---

### "How did you use BMC TrueSight / TSCO for capacity optimization?"
> "BMC TrueSight Capacity Optimization — now part of the Helix platform — was
> the primary telemetry source at Citi. It collected performance metrics across
> the entire infrastructure estate: CPU, memory, disk I/O, network — at P95
> granularity.
>
> I used the TSCO API and direct database feeds to extract time-series telemetry
> into my Python pipelines. From there, I enriched it with CMDB metadata
> (application, team, criticality tier) and loaded it into an Oracle data warehouse
> for historical trending.
>
> The Aperture Vista module within TSCO also provided built-in capacity forecasting
> views — I used those as a validation layer against my own ML-generated forecasts
> to catch model drift and sanity-check predictions.
>
> The key value of TSCO was breadth and consistency — it gave me a single unified
> telemetry source across heterogeneous infrastructure, which is what made
> cross-domain capacity comparisons possible."

---

### "Tell me about ML approaches for capacity forecasting."
> "I used a two-model architecture in HorizonScale.
>
> First: Prophet for time-series forecasting. Prophet handles seasonality and
> trend decomposition natively, which matters for capacity data that has weekly
> and monthly cyclical patterns. It generates a forecast with confidence intervals,
> so I can show not just the expected trajectory but the uncertainty band.
>
> Second: scikit-learn classifiers — specifically Random Forest and Gradient
> Boosting — trained to classify assets as 'at risk' or 'safe' based on features
> derived from the telemetry: growth rate, P95 trend slope, variance, days-to-threshold.
> This gave a binary risk signal that was easier for operational teams to act on
> than a continuous forecast curve.
>
> The pipeline ran on PySpark at banking scale — thousands of endpoints processed
> in parallel using a generator-based architecture that cut cycle time by 90%.
>
> For a FAB environment, the same architecture applies: replace server telemetry
> with tool utilization data, replace CMDB with equipment master data, and the
> pipeline and model structure transfers directly."

---

### "What's your experience with in-house vs. cloud capacity planning?"
> "Both. At Citi I operated a hybrid model.
>
> On-premises capacity: Oracle data warehouse, BMC TrueSight telemetry, traditional
> server/storage/network estate. Planning cycles were quarterly, with 12-month
> procurement horizons. The constraint was lead time — hardware takes months to
> arrive, so forecasting accuracy 6+ months ahead was critical.
>
> Cloud capacity: AWS S3, Glue, Redshift, ECS. Cloud changes the constraint model —
> you can provision in minutes, so the planning question shifts from 'do we have
> enough?' to 'are we spending appropriately?' Capacity management in cloud is
> partly a FinOps problem: right-sizing EC2 instances, auto-scaling policy design,
> Reserved vs. On-Demand allocation optimization.
>
> The key difference: on-prem capacity planning is a procurement and lead-time
> problem. Cloud capacity planning is a cost optimization and right-sizing problem.
> Both require the same analytical foundation — utilization data, trend analysis,
> forecasting — but the action levers are different."

---

### "What is containerized capacity planning?"
> "Containerized environments add a layer of abstraction that makes capacity
> planning more dynamic but also more complex.
>
> In a container environment — Docker/ECS or Kubernetes — individual containers
> request CPU and memory limits. Capacity planning shifts from physical machine
> utilization to:
> 1. Node-level: Is the underlying EC2/VM fleet sized correctly for the container
>    workloads running on it?
> 2. Cluster-level: Is the cluster auto-scaling policy configured to handle burst
>    demand without over-provisioning at baseline?
> 3. Workload-level: Are container resource requests and limits set correctly —
>    not over-requested (wasteful) or under-requested (causing throttling)?
>
> At Citi I containerized Python ETL workloads on ECS. Capacity planning there
> meant monitoring container task utilization, setting appropriate Fargate CPU/memory
> specs, and configuring ECS service auto-scaling policies based on queue depth
> and task throughput metrics."

---

## Aptitude / Logic / Estimation Questions

### "How would you estimate the capacity of a bottleneck tool in a fab?"
> "I'd start with the tool's theoretical throughput: how many wafer lots can it
> process per hour at rated speed? That's the ceiling.
>
> Then I'd factor in availability: scheduled maintenance, unplanned downtime,
> engineering qualifications. If the tool is up 85% of the time, effective
> capacity is 85% of theoretical.
>
> Then utilization within uptime: if the tool runs at 70% utilization while up,
> effective throughput is 70% × 85% = ~60% of theoretical max.
>
> To find headroom before constraint: if demand requires 75% of theoretical max
> and effective throughput is 60%, you have a 15-point gap — that's your
> bottleneck. Any upstream WIP growth will manifest as cycle time increase at
> that tool.
>
> I'd validate this against actual cycle time data — if cycle time at the tool
> is rising while utilization is also rising, that's the classic queuing nonlinearity
> that confirms it's the bottleneck."

---

### "If throughput dropped 10% this week, how do you find the cause?"
> "Systematic decomposition. I'd work from the top down:
>
> 1. Is it a tool availability issue? Check uptime/downtime logs — was the
>    bottleneck tool down for an extended period?
> 2. Is it a WIP starvation issue? Was there a shortage of lot starts feeding
>    the tool? Check upstream WIP levels.
> 3. Is it a process rate issue? Did the tool run slower — recipe change,
>    engineering intervention, or performance degradation?
> 4. Is it a scheduling issue? Were lots being misrouted or held in queue
>    for reasons outside normal flow?
>
> I'd pull time-series data for each dimension and correlate the timing of
> the throughput drop against each variable. The one that changes coincidentally
> with the drop is the lead indicator. Then I'd quantify impact and drive
> the corrective action."

---

### "Little's Law — explain it and give an example."
> "Little's Law: L = λW. The average number of items in a system equals
> the average arrival rate times the average time each item spends in the system.
>
> Fab example: If 100 wafer lots are in WIP (L = 100) and throughput is
> 20 lots per day (λ = 20), then average cycle time is 5 days (W = L/λ = 5).
>
> The power of this: if WIP doubles to 200 lots but throughput stays at 20/day,
> cycle time doubles to 10 days. You don't need to measure cycle time directly —
> you can calculate it from WIP and throughput, both of which are observable.
>
> It also tells you the lever: to reduce cycle time without reducing WIP,
> you must increase throughput. To reduce cycle time without increasing throughput,
> you must reduce WIP. There's no free lunch."

---

## SQL Questions

### "Write a query to find the top 5 bottleneck tools by average utilization over the last 30 days."
```sql
SELECT
    tool_id,
    tool_name,
    AVG(utilization_pct) AS avg_utilization,
    MAX(utilization_pct) AS peak_utilization,
    COUNT(*) AS reading_count
FROM tool_telemetry
WHERE reading_timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY tool_id, tool_name
ORDER BY avg_utilization DESC
LIMIT 5;
```

---

### "Find tools that exceeded 85% utilization for 3 or more consecutive days."
```sql
WITH daily_util AS (
    SELECT
        tool_id,
        DATE(reading_timestamp) AS day,
        AVG(utilization_pct) AS daily_avg
    FROM tool_telemetry
    GROUP BY tool_id, DATE(reading_timestamp)
),
flagged AS (
    SELECT
        tool_id,
        day,
        daily_avg,
        CASE WHEN daily_avg >= 85 THEN 1 ELSE 0 END AS over_threshold
    FROM daily_util
),
grouped AS (
    SELECT
        tool_id,
        day,
        daily_avg,
        over_threshold,
        ROW_NUMBER() OVER (PARTITION BY tool_id ORDER BY day) 
            - ROW_NUMBER() OVER (PARTITION BY tool_id, over_threshold ORDER BY day) AS grp
    FROM flagged
)
SELECT tool_id, MIN(day) AS streak_start, MAX(day) AS streak_end, COUNT(*) AS consecutive_days
FROM grouped
WHERE over_threshold = 1
GROUP BY tool_id, grp
HAVING COUNT(*) >= 3
ORDER BY consecutive_days DESC;
```

> "The gaps-and-islands pattern — I subtract two row numbers to identify consecutive runs."

---

### "What's your approach to query optimization?"
> "I start with the execution plan — EXPLAIN or EXPLAIN ANALYZE. I'm looking for:
> full table scans where index scans should exist, hash joins on large unindexed
> tables, and row estimate errors that indicate stale statistics.
>
> For large analytical queries, I look at partition pruning — is the query filtering
> on a partition key so it's only scanning relevant data? For aggregations, are
> window functions avoiding unnecessary self-joins?
>
> In Oracle specifically, I watch for missing histogram statistics on skewed columns
> and bad cardinality estimates that cause wrong join order selection. CTEs in Oracle
> are sometimes materialized — in performance-critical queries I verify whether
> that's helping or hurting.
>
> General rules: push filters early, avoid SELECT *, use CTEs for readability
> but know when the optimizer needs a subquery instead, and index your join keys
> and high-cardinality filter columns."

---

### "Window functions — when do you use them?"
> "Window functions let me compute aggregates over a sliding context without
> collapsing rows the way GROUP BY does. I use them constantly in capacity work.
>
> LAG/LEAD: calculate day-over-day or week-over-week change in utilization without a self-join.
> ROW_NUMBER / RANK: find the most recent record per tool, or rank tools by utilization within a class.
> SUM/AVG OVER: rolling 7-day or 30-day moving averages for smoothing telemetry noise.
> NTILE: bucket tools into utilization quartiles for tiered capacity review reporting.
>
> Example: rolling 7-day average utilization per tool:
> AVG(utilization_pct) OVER (PARTITION BY tool_id ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)"

---

## Python Questions

### "How do you process large time-series telemetry in Python?"
> "For banking-scale telemetry at Citi — thousands of endpoints, years of history —
> I used PySpark. It distributes the load across a cluster, handles the partitioning
> automatically, and integrates with S3 and Redshift natively via Glue.
>
> For medium-scale work or local analysis, Pandas with chunked reads and vectorized
> operations. The key is avoiding row-level Python loops — everything should be
> expressed as vectorized Pandas or NumPy operations where possible.
>
> For HorizonScale specifically, I built a generator-based parallel pipeline —
> each asset's time-series fed through a generator, processed independently,
> with multiprocessing.Pool for parallelism. This gave 90% cycle time reduction
> versus the original sequential design."

---

### "How would you build a capacity forecasting model in Python?"
```python
from prophet import Prophet
import pandas as pd

def forecast_capacity(telemetry_df: pd.DataFrame, periods: int = 180) -> pd.DataFrame:
    """Forecast utilization for the next `periods` days using Prophet."""
    df = telemetry_df.rename(columns={"date": "ds", "utilization_pct": "y"})
    
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        changepoint_prior_scale=0.05  # regularize to avoid overfitting
    )
    model.fit(df)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
```

> "Prophet handles trend + seasonality decomposition automatically. yhat_upper is
> what I use for capacity risk — it's the upper confidence bound. If yhat_upper
> crosses the threshold (e.g., 80% utilization) within the forecast window, that
> asset is flagged at risk."

---

### "What Python tools do you use for data analysis?"
> "Core stack: Pandas for tabular manipulation, NumPy for numerical operations,
> SQLAlchemy for Oracle/Redshift connectivity. For visualization: Matplotlib,
> Seaborn, and Plotly for interactive charts in Streamlit dashboards.
>
> For ML: scikit-learn for classification and regression models, Prophet for
> time-series. For scale: PySpark on AWS Glue for distributed processing.
>
> For development discipline: type hints everywhere, Pydantic for data model
> validation at pipeline boundaries, pytest for unit testing pipeline logic,
> Black and ruff for formatting and linting."

---

## Samsung-Specific Questions

### "Why Samsung / Why this role?"
> "Samsung operates at a scale of manufacturing complexity that's genuinely
> rare — advanced semiconductor fabrication at Austin is one of the most
> technically demanding manufacturing environments in the world.
>
> Capacity planning in a fab isn't just data work — it directly determines
> what gets built, when, and at what cost. The analytical rigor required —
> Factory Physics, bottleneck modeling, supply chain forecasting — is exactly
> the work I've been doing in infrastructure capacity, and I want to apply
> it in a domain where the stakes are higher and the problems are harder.
>
> The Taylor fab is also a strategic investment for Samsung's U.S. presence.
> Being part of building out the operational excellence layer of that facility
> is genuinely exciting."

---

### "What do you know about semiconductor capacity planning specifically?"
> "The core framework maps to Factory Physics principles: throughput, cycle time,
> and WIP are the three variables, governed by Little's Law. The bottleneck tool
> is the constraint — it sets the pace for the entire fab.
>
> Long-range capacity planning involves modeling tool availability (uptime, PM
> schedules), throughput rates, and incoming demand (lot starts) to identify
> where gaps will emerge over a 6–18 month horizon. Short-range is more about
> daily/weekly WIP movement, scheduling, and tool allocation to hit monthly
> output targets.
>
> Supply chain matters too — if a critical tool is down for repair and spares
> lead time is 8 weeks, that's a capacity event, not just a maintenance event.
> Capacity planning has to integrate equipment status, engineering roadmaps,
> and procurement realities together.
>
> My experience in IT capacity gave me the analytical foundation — the fab domain
> specifics I'm ready to learn fast."

---

## Questions To Ask The Hiring Manager

1. "What does the split look like between short-range capacity management (daily/weekly WIP) and long-range planning (6–18 months)?"
2. "What tools and data infrastructure are you currently using for capacity analysis — are you building on top of existing MES data, or pulling from separate analytics platforms?"
3. "Where are the biggest gaps today — is it analytical tooling, forecasting capability, or coordination between the engineering and production teams?"
4. "How mature is the use of ML or statistical forecasting in the current capacity process?"
5. "What does success look like in the first 90 days for this role?"

---

## Logistics

- **Recruiter screen:** Robyn Wentworth — r.wentworth@samsung.com
- **Format:** 30-min phone screen first, then hiring manager
- **Request:** 2 days' notice before interview to prepare
- **Start:** Available immediately
- **Salary anchor:** $145,000–$160,000 base
- **Key numbers:** 20+ years, 8 years Citi, 6,000+ endpoints, 90% forecast accuracy, 6-month prediction horizon, 90% cycle time reduction (HorizonScale)

---

## Pre-Interview 30-Minute Refresh

1. Re-read the 4 key stories out loud — time them at 60–90 seconds each
2. Rehearse the Opening 2 Minutes cold
3. Review Factory Physics / Little's Law — say it in plain language
4. Review BMC TrueSight story — it's the most direct credential match
5. Know your numbers cold: 6,000 endpoints, 90% accuracy, 6-month horizon, 90% cycle reduction
6. Have this doc open on a second screen

---

## After The Screen

Update `data/applied_jobs/00060_7c453502/metadata.yaml` status to `PHONE_SCREEN` or `INTERVIEW`.
