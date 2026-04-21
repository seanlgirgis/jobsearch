# Samsung HM Interview — Audio 4: Technical Depth
## What This Audio Covers
The deep technical questions David Rojas is most likely to probe if he goes past the surface: bottleneck investigation methodology, full capacity analysis walkthrough, BMC TrueSight, ML forecasting architecture, how to estimate bottleneck capacity, and diagnosing a sudden throughput drop.

---

## How to Approach a Bottleneck Investigation

Systematic decomposition — work from the top down.

**Step 1: Is it a capacity issue or a utilization issue?**
If peak utilization is high AND growing, that is a structural capacity gap. If peak utilization is high but adjacent assets are under-utilized, that is a scheduling or allocation gap. These have completely different solutions — one requires procurement, the other requires rebalancing.

**Step 2: What is the timing signature?**
A sudden spike points to a discrete event — a tool going down, a process change, a demand surge. A gradual trend points to organic growth approaching the ceiling.

**Step 3: Is it the actual bottleneck or a downstream effect?**
In fab terms — is the WIP building up because that tool is slow, or because the tool feeding it is starving it? Correlate queue depth, move rate, and upstream WIP to separate cause from symptom.

At Citi you built SQL queries that segmented assets by utilization pattern — over-utilized, under-utilized, spiky versus flat — and correlated with metadata to find the root cause. The output was not just "this is bottlenecked" — it was "here is why, here is the quantified impact, here is the recommended action."

---

## Walk Through a Full Capacity Analysis

Start by defining the resource and the constraint — what are we measuring and what threshold represents a problem? In IT: CPU and memory peak utilization. In a fab: tool utilization rate and WIP queue depth.

Then pull 12 to 24 months of historical utilization data and decompose the trend: linear growth, seasonal pattern, or event-driven spikes?

From that build a forecast — statistical for stable trends, ML-based using Prophet for volatile or seasonal data. The forecast gives the expected crossover point where demand exceeds available capacity.

Then calculate the gap: projected demand minus available capacity at each planning horizon — 3 months, 6 months, 12 months. Is the gap addressable through efficiency improvements or does it require net-new capacity?

Finally present risk-tiered options: do nothing — cost of miss; optimize utilization — investment plus lead time; procure — cost plus lead time. Leadership decides with full information, not just a status update.

---

## How You Used BMC TrueSight / TSCO for Capacity Optimization

BMC TrueSight Capacity Optimization — now the Helix platform — was your primary telemetry source at Citi. It collected performance metrics across the entire infrastructure estate: CPU, memory, disk I/O, network — at peak utilization granularity.

You used the TSCO API and direct database feeds to extract time-series telemetry into Python pipelines. Enriched with CMDB metadata — application, team, criticality tier — and loaded into Oracle for historical trending.

The Aperture Vista module provided built-in capacity forecasting views — you used those as a validation layer against your ML-generated forecasts to catch model drift and sanity-check predictions.

The key value of TSCO was breadth and consistency — a single unified telemetry source across heterogeneous infrastructure. That is the same value a MES provides in a fab: one source of truth for equipment state, lot movement, and process data.

---

## ML Approaches for Capacity Forecasting — HorizonScale Architecture

You used a two-model architecture in HorizonScale.

**First model: Prophet for time-series forecasting.** It handles seasonality and trend decomposition natively — weekly patterns, monthly cycles, holiday effects. Generates a forecast with confidence intervals, so you can show the uncertainty band, not just the expected trajectory.

**Second model: scikit-learn classifiers — Random Forest and Gradient Boosting** — trained to classify assets as at-risk or safe based on derived features: growth rate, utilization trend slope, variance, days to threshold. This gave a binary risk signal easier for operational teams to act on than a curve.

The pipeline ran on PySpark at banking scale — thousands of assets processed in parallel, generator-based architecture. 90 percent cycle time reduction versus the original sequential design.

For a fab environment: replace server telemetry with tool utilization data, replace CMDB with equipment master data. The pipeline architecture and model structure transfer directly.

---

## MES — What It Is and How Capacity Planning Interacts With It

MES — Manufacturing Execution System — runs the fab floor in real time. Tracks every lot at every step: location, tool used, step duration, holds, excursions.

For capacity planning, MES is the primary data source: lot tracking — actual cycle time, move rates, WIP by step; equipment history — uptime and downtime, SEMI E10 states; and process data — tool, recipe, process time.

Capacity planning queries MES to calculate actual OEE, actual versus standard cycle time, and WIP movement rates — then feeds those into forecasting models.

You have not worked directly with fab MES, but the data extraction pattern is identical to what you built against BMC TrueSight — connect to the source, extract time-series telemetry, enrich with reference data, build analytical models.

---

## How to Estimate the Capacity of a Bottleneck Tool

Start with theoretical throughput: lots per hour at rated speed — that is the ceiling.

Factor in availability: if the tool is up 85 percent of the time, effective capacity is 85 percent of theoretical.

Factor in utilization within uptime: 70 percent utilization times 85 percent availability equals approximately 60 percent effective capacity.

Calculate the gap: if demand requires 75 percent of theoretical max and effective capacity is 60 percent, you have a 15-point gap — that is your bottleneck.

Validate against cycle time data: cycle time rising alongside utilization is the classic queuing nonlinearity that confirms the bottleneck.

---

## How Do You Calculate Resource Capacity and Utilization?

Utilization equals actual output divided by theoretical maximum capacity times 100 percent.

Headroom equals threshold minus current peak utilization. If threshold is 80 percent and peak is 72 percent, you have 8 points of headroom.

Time-to-capacity: growth slope from historical trending projects when peak utilization crosses the threshold. Growing 1.5 points per quarter with 8 points of headroom equals approximately 5 quarters to breach.

Effective capacity equals theoretical times availability — raw theoretical capacity is never the real planning number.

---

## If Throughput Dropped 10% This Week — How Do You Find the Cause?

Systematic decomposition, top down:

1. **Tool availability** — was the bottleneck tool down?
2. **WIP starvation** — was there a shortage of lot starts feeding the tool?
3. **Process rate** — did the tool run slower due to a recipe change or degradation?
4. **Scheduling** — were lots misrouted or held in queue?

Pull time-series data for each dimension, correlate timing with the drop. The variable that changes coincidentally with the throughput drop is the lead indicator. Quantify the impact and drive the corrective action.

---

## In-House vs. Cloud Capacity Planning

Both — Citi was a hybrid model.

**On-premises:** Oracle warehouse, BMC TrueSight, server, storage, and network estate. Quarterly planning cycles, 12-month procurement horizons. The constraint is lead time — hardware takes months, so 6-month plus forecasting accuracy is critical.

**Cloud on AWS:** S3, Glue, Redshift, ECS. Cloud changes the constraint model — you provision in minutes. Planning shifts from "do we have enough?" to "are we spending appropriately?" It becomes partly a FinOps problem: right-sizing, auto-scaling, Reserved versus On-Demand.

On-premises is a procurement and lead-time problem. Cloud is a cost optimization and right-sizing problem. Same analytical foundation, different action levers.
