# HorizonScale — Time-Series ML Forecasting at Scale

<a id="toc"></a>
## Table of Contents
1. [Facebook Prophet](#sec-1)
2. [SARIMA](#sec-2)
3. [Exponential Smoothing (ETS)](#sec-3)
4. [XGBoost Challenger](#sec-4)

GitHub: [seanlgirgis/horizonscale](https://github.com/seanlgirgis/horizonscale)

---

## Project Overview

HorizonScale is a two-phase infrastructure capacity forecasting platform.
Input: two years of P95 utilization telemetry across tens of thousands of servers and four
KPIs — CPU, memory, disk, and network. Output: a six-month rolling forecast
per server per KPI, with a model tournament selecting the best-performing
algorithm for each of the 65,000+ metrics, and a risk report
surfacing every system projected to breach capacity thresholds within the
forecast window.

**Phase 1** — built and validated the entire forecasting pipeline on a local
Apache open-source stack: DuckDB, Parquet, Polars, Prophet, SARIMA, ETS.
Prove the approach works before committing to cloud infrastructure.

**Phase 2** — migrated to AWS: S3 data lake, AWS Glue with PySpark Grouped
Map UDFs for distributed Prophet execution across the full fleet, and Amazon
Athena for ad-hoc querying of forecast outputs.

Scale: tens of thousands of servers · 4 KPIs · 65,000+ metrics · 180-day forecast
horizon · Champion model selected per series via backtest tournament.

---

## The Dataset — 2 Years of P95 Telemetry

Two years of daily P95 utilization measurements — the 95th percentile across
intra-day readings — for every monitored endpoint across four resource types.
P95 rather than average is the right metric for capacity planning: it captures
what the system experiences at high load, not what it averages across quiet
periods. An average CPU utilization of 45% can coexist with a P95 of 88% if
workloads are bursty — and it's the 88% that drives capacity decisions.

Data is stored in Parquet format partitioned by resource type. DuckDB provides
SQL query capability directly against the Parquet files without loading them
fully into memory — critical when the dataset spans 2,000 hosts × 4 resources
× 730 days.

```
# Master Parquet schema
date        DATE      -- daily timestamp
node_name   VARCHAR   -- server UUID (e.g. server-a3f2b1c4)
resource    VARCHAR   -- cpu | memory | disk | network
p95_util    DOUBLE    -- P95 utilization 0–100 (percentage)
capacity    DOUBLE    -- max_cores / memory_gb / storage_mb (null for network)

# Scale: 2,000 hosts × 4 resources × ~730 days ≈ 5.8M rows
```

**Resource characteristics**

CPU — max_cores, 4–128 cores. Noise std ±3%. Most time-structured signal.
Memory — memory_gb, 16–512 GB. Noise std ±4%. Growth trends often software-driven.
Disk — storage_capacity_mb, 500GB–10TB. Noise std ±6%. Monotonic growth common.
Network — relative %, 0–100%. Noise std ±5%. Burst-heavy patterns.

---

## Confidence Tiers: 3-Month vs 6-Month

The forecast window is structured into two explicit confidence tiers rather
than a single 180-day output. Uncertainty accumulates with horizon — treating
a 5-month forecast with the same confidence as a 5-week forecast leads to poor
planning decisions.

**High-confidence tier — months 1–3**
Tight prediction intervals. Use for: procurement decisions, infrastructure
change requests, immediate scaling actions.

**Directional tier — months 4–6**
Wider intervals, trajectory signal only. Use for: planning horizon
conversations, budget requests, architecture review scheduling.

Prophet's Bayesian uncertainty quantification produces `yhat_lower` and
`yhat_upper` columns representing the 80% prediction interval at each
forecast point. The interval width naturally widens with distance from the
training data.

Risk breach detection uses `yhat_upper >= 95%` as the threshold — if the
upper confidence bound reaches 95% within the window, the system is flagged.
This ensures teams are warned before the forecast's central estimate hits the
ceiling, not after.

---

## Seasonality & Business Cycles

Infrastructure utilization carries layered periodicity. Ignoring any layer
produces systematic forecast errors precisely on the high-load days that
capacity planning cares most about.

**Weekly** — 7 days. Weekday workloads vs. weekend; batch jobs run on specific
days. Handled by: SARIMA seasonal order (1,1,1,7); Prophet weekly seasonality.

**Monthly** — ~30 days. Month-end billing runs, reporting jobs, payroll cycles.
Handled by: Prophet monthly seasonality component; ETS additive seasonal.

**Quarterly** — ~90 days. Business planning cycles, quarterly reporting,
compliance runs. Handled by: captured in Prophet's annual Fourier terms.

**Annual** — 365 days. Year-end processing, holiday traffic surges, annual
batch jobs. Handled by: Prophet yearly seasonality; logistic growth cap
constrains peak behavior.

**Holiday effects** — irregular. Traffic surges or drops around public
holidays. Handled by: Prophet holiday regressor; explicit calendar features
in XGBoost.

Models that ignore weekly seasonality will systematically underforecast on
Mondays and Fridays — the peak business days for many financial and enterprise
workloads. The SARIMA seasonal order of (1,1,1,7) was chosen specifically to
capture the weekly business cycle across the fleet.

The fleet behavioral classification ensures that seasonal models are applied
to series where they add value. Fitting a strong seasonal model to a LOW_IDLE
server that barely moves adds noise rather than signal.

---

## Fleet Behavioral Classification

Before modeling, every server-resource series is classified into one of five
behavioral scenarios based on its historical pattern. This drives model
selection hints, alert thresholds, and reporting priority. It also makes the
fleet analytically tractable — instead of treating 65,000+ metrics as
individually unique, the classification creates groups with shared
characteristics that can be analyzed and validated as cohorts.

```python
# Scenario distribution in fleet initialization
SCENARIO_DISTRIBUTION = {
    Scenario.STEADY_GROWTH:    0.35,
    Scenario.LOW_IDLE:         0.25,
    Scenario.SEASONAL:         0.20,
    Scenario.BURST:            0.15,
    Scenario.CAPACITY_BREACH:  0.05,   # 5% at-risk — highest priority
}

# Each scenario has common and rare variants (80/20 split)
VARIANT_WEIGHTS = {'common': 0.80, 'rare': 0.20}
```

**STEADY_GROWTH** (~35%) — gradual linear increase from 35–55% baseline.
Predictable procurement timeline; forecast confidence is high.

**LOW_IDLE** (~25%) — consistently low utilization, 10–12% baseline.
Under-utilization candidates; downsizing or consolidation opportunity.

**SEASONAL** (~20%) — periodic cycles ±20–30% amplitude around baseline.
Seasonal peak must be the planning ceiling, not the average.

**BURST** (~15%) — low baseline with irregular high-intensity spikes.
Wide prediction intervals; P95 is the right metric; hard to model precisely.

**CAPACITY_BREACH** (~5%) — rapid growth trajectory toward 95–100% ceiling.
Immediate action required; flagged as highest priority in risk report.

---

## Phase 1 — Apache Stack Architecture

The first phase built and validated the entire forecasting pipeline on a local
open-source stack. The principle: prove the approach works before investing in
cloud infrastructure. All core design decisions — model tournament, confidence
tiers, risk detection thresholds, behavioral classification — were validated
in Phase 1 before Phase 2 migrated them to AWS.

```
# Phase 1 pipeline stages
00_init_db.py              # Initialize DuckDB schema
01_generate_master_parquet # Generate 2-year daily P95 telemetry → master_daily.parquet
02_export_monthly_csvs     # CSV export for downstream compatibility
03_data_pipeline.py        # Aggregate raw Parquet → DuckDB tables
                           # Prophet-compatible format: ds (TIMESTAMP), y (DOUBLE)
                           # Rolling features: rolling_mean_7, rolling_std_7
04_eda_synthetic.py        # Exploratory analysis — distributions, correlations, volatility
05_eda_processed.py        # EDA on processed Prophet-ready data
06_baseline_prophet.py     # Facebook Prophet — 180-day forecast with logistic growth
07_baseline_sarima_ets.py  # SARIMA(1,1,1)(1,1,1,7) + ETS — 180-day forecasts
08_baseline_comparison.py  # Model tournament — MAPE comparison, champion selection
09_advanced_tft.py         # Temporal Fusion Transformer (attention-based deep learning)
10_advanced_hybrid.py      # Ensemble hybrid models
11_anomaly_recs.py         # Anomaly detection (Isolation Forest) + recommendations
12_dashboard.py            # Streamlit internal dashboard
```

**Phase 1 tech stack**

Storage — Parquet (Snappy compression). Columnar time-series; efficient range scans and resource-type filters.
Query engine — DuckDB. In-process SQL over Parquet; no server, sub-second aggregation on millions of rows.
DataFrame ops — Polars. High-speed transformations and feature engineering; faster than Pandas at this scale.
Forecasting — Prophet, SARIMA, ETS, XGBoost. Multi-model tournament; champion selected per series via 4-month backtest MAPE.
Experiment tracking — MLflow. Model parameters, MAPE scores, and forecast artifacts logged per run.
Dashboard — Streamlit. Interactive drill-down; fleet overview, per-host forecast viewer, risk rankings.

---

## Forecasting Models

<a id="sec-1"></a>
### Facebook Prophet

Prophet is the primary model across the fleet. It decomposes the time series
into trend, seasonality (daily, weekly, annual), and holiday components,
fitting each independently via Stan's Bayesian inference.

Logistic growth mode is critical — it constrains the forecast to be physically
bounded between 0% and 100% utilization. A linear trend model will forecast
110% CPU, which is meaningless. Logistic growth recognizes that utilization
growth must slow as it approaches the physical ceiling, producing more
realistic long-horizon forecasts for high-utilization systems.

```python
# Prophet configuration (Phase 1)
from prophet import Prophet

model = Prophet(
    growth='logistic',          # Bounded — respects physical capacity ceiling
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=True,
    uncertainty_samples=1000,   # Reduced to 100 in Phase 2 for throughput
)

# Logistic growth requires cap and floor
df['cap']   = 100.0   # Physical maximum: 100% utilization
df['floor'] = 0.0     # Physical minimum

model.fit(df)
future          = model.make_future_dataframe(periods=180)
future['cap']   = 100.0
future['floor'] = 0.0
forecast = model.predict(future)
# Outputs: ds, yhat, yhat_lower, yhat_upper
```
[Back to TOC](#toc)


<a id="sec-2"></a>
### SARIMA

SARIMA — Seasonal AutoRegressive Integrated Moving Average. Configuration
`order=(1,1,1)` with `seasonal_order=(1,1,1,7)` captures first-order trend
differencing and a weekly seasonal period of 7 days. SARIMA wins the
tournament on series with strong regular weekly patterns and relatively low
noise, where the statistical structure is well-defined and doesn't require
Prophet's flexibility.

[Back to TOC](#toc)

<a id="sec-3"></a>
### Exponential Smoothing (ETS)

ETS models are selected automatically via AIC minimization — the framework
tries additive and multiplicative error, trend, and seasonal variants and
selects the best-fitting specification for each series. Computationally fast,
robust on shorter series, performs well on LOW_IDLE and STEADY_GROWTH
scenarios where behavior is smooth and trend-dominated.

[Back to TOC](#toc)

<a id="sec-4"></a>
### XGBoost Challenger

XGBoost takes a supervised ML approach rather than time-series decomposition.
Features are engineered from the time index: an ordinal trend variable
capturing overall growth direction, and month-of-year capturing annual
seasonality. GPU acceleration via CUDA (`device='cuda'`) enables the 65,000+
series to process rapidly. XGBoost wins the tournament on series with strong
trend and weak periodicity — particularly STEADY_GROWTH and CAPACITY_BREACH
scenarios — where its gradient boosting on simple features outperforms
Prophet's flexible seasonality components on series that don't actually have
strong seasonal structure.

---

## Model Tournament — Champion Selection

No single forecasting algorithm performs best across all behavioral scenarios
at fleet scale. The champion-challenger tournament selects the best model per
series rather than committing the entire fleet to one algorithm.

```python
# Tournament logic (per host-resource pair)
TRAIN_MONTHS    = 32   # ~2.7 years of training data
BACKTEST_MONTHS = 4    # Held-out window — no model sees this during training
FUTURE_MONTHS   = 6    # Forecast horizon

# For each host-resource series:
train_df    = history[: -BACKTEST_MONTHS_ROWS]
backtest_df = history[-BACKTEST_MONTHS_ROWS :]

# Train all models on train_df
prophet_forecast = fit_prophet(train_df).predict(backtest_period)
sarima_forecast  = fit_sarima(train_df).forecast(BACKTEST_MONTHS_ROWS)
xgb_forecast     = fit_xgboost(train_df).predict(backtest_features)

# Score each model on backtest
def mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

scores = {
    'prophet':  mape(backtest_df['y'], prophet_forecast['yhat']),
    'sarima':   mape(backtest_df['y'], sarima_forecast),
    'xgboost':  mape(backtest_df['y'], xgb_forecast),
}

champion = min(scores, key=scores.get)   # Lowest MAPE wins
# Champion retrained on full history, generates 6-month future forecast
```

The champion model is selected independently for every host-resource pair.
In a fleet of 2,000 servers × 4 resources, the winning model distribution
reflects the actual mix of behavioral patterns — Prophet dominates on seasonal
series, XGBoost on trend-dominated ones, SARIMA on clean weekly-cycle series.

Using a single global model is a common shortcut that degrades forecast quality
on the series where it doesn't fit. The tournament adds engineering complexity
but produces meaningfully better accuracy across the fleet, which directly
improves the reliability of the capacity risk report.

---

## Phase 2 — AWS Migration

With the forecasting approach validated in Phase 1, Phase 2 migrated to AWS
for production-scale throughput. Running 65,000+ metrics sequentially
hits a throughput ceiling. AWS Glue with 10 G.2X worker nodes running Spark
3.3 distributes the workload across the fleet in parallel, dramatically
reducing wall-clock time for a full fleet forecast run.

**AWS services**

S3 — data lake for all input and output data. Bucket: `horizonscale-datalake-v1` with structured prefixes.
AWS Glue — distributed PySpark forecasting engine. 10 G.2X workers, Glue 4.0 (Spark 3.3), Prophet and Polars dependencies packaged.
Amazon Athena — ad-hoc SQL over forecast Parquet outputs. Results prefix: `s3://horizonscale-datalake-v1/athena-results/`.
IAM — service roles for Glue and S3 access. Auto-provisioned Glue service role with S3 full access on data lake bucket.

**S3 data lake structure**

```
s3://horizonscale-datalake-v1/
├── raw/telemetry/              # Master Parquet — input time-series
│   └── master_daily.parquet
├── scripts/                    # Glue job Python scripts
│   └── glue_horizon_prophet.py
├── forecasts/                  # Turbo Prophet output Parquet
│   └── prophet_turbo_master.parquet
└── athena-results/             # Athena query output CSVs
```

---

## AWS Glue: Distributed PySpark Forecasting

Prophet is single-threaded Python — it cannot natively parallelize across a
Spark cluster. The PySpark Grouped Map UDF pattern works around this by
treating each host-resource pair as an independent group. The data is
structured so each partition contains one complete time series. Spark
automatically distributes partitions across worker nodes. Each worker runs a
complete, independent Prophet fitting inside the UDF function. No
cross-partition communication. No shared state.

```python
# glue_horizon_prophet.py — PySpark Grouped Map UDF pattern
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
from prophet import Prophet
import pandas as pd

OUTPUT_SCHEMA = StructType([
    StructField("node_name",  StringType()),
    StructField("resource",   StringType()),
    StructField("ds",         DateType()),
    StructField("yhat",       DoubleType()),
    StructField("yhat_lower", DoubleType()),
    StructField("yhat_upper", DoubleType()),
    StructField("data_type",  StringType()),   # 'history' or 'forecast'
])

@pandas_udf(OUTPUT_SCHEMA, PandasUDFType.GROUPED_MAP)
def forecast_one_series(pdf: pd.DataFrame) -> pd.DataFrame:
    """Fits Prophet on one host-resource partition and returns forecast."""
    node = pdf["node_name"].iloc[0]
    res  = pdf["resource"].iloc[0]

    df          = pdf[["ds", "y"]].copy()
    df["cap"]   = 100.0
    df["floor"] = 0.0

    model = Prophet(
        growth='logistic',
        uncertainty_samples=100,   # Reduced from 1000 for throughput
        daily_seasonality=True,
        weekly_seasonality=True,
    )
    model.fit(df)

    future          = model.make_future_dataframe(periods=180)
    future["cap"]   = 100.0
    future["floor"] = 0.0
    forecast        = model.predict(future)

    cutoff = df["ds"].max()
    forecast["data_type"] = forecast["ds"].apply(
        lambda d: "history" if d <= cutoff else "forecast"
    )
    forecast["node_name"] = node
    forecast["resource"]  = res
    return forecast[["node_name","resource","ds","yhat","yhat_lower","yhat_upper","data_type"]]

# Apply UDF: Spark groups by (node_name, resource) — one partition per series
result_df = (
    spark_df
    .groupBy("node_name", "resource")
    .apply(forecast_one_series)
)
result_df.write.parquet("s3://horizonscale-datalake-v1/forecasts/prophet_turbo_master.parquet")
```

The throughput trick: `uncertainty_samples` reduced from 1,000 to 100 in
Phase 2. The confidence interval accuracy degradation at fleet scale is
negligible — the throughput gain is 10x. That single change is what makes the
fleet-scale run tractable within a reasonable job window.

---

## Risk Detection & Reporting

The forecast output is only useful if it surfaces the right signals for the
right teams. The risk detection layer scans the champion forecast for every
host-resource pair and classifies against two criteria.

**Capacity breach** — `yhat_upper >= 95%` within 6-month window. Upper
confidence bound projects the system at or above the operational ceiling.
Action required.

**High priority** — forecast StdDev > 2 OR projected peak > 105%. High
volatility or extreme projected overage. Elevated urgency — most likely needs
immediate consultation.

```python
# Risk detection (09_risk_reporting.py — simplified)
import duckdb

risks = duckdb.sql("""
    SELECT
        node_name,
        resource,
        MAX(yhat_upper)                         AS projected_peak,
        MIN(ds) FILTER (WHERE yhat_upper >= 95) AS earliest_breach_date,
        STDDEV(yhat)                            AS forecast_volatility,
        CASE
            WHEN STDDEV(yhat) > 2 OR MAX(yhat_upper) > 105
            THEN 'HIGH PRIORITY'
            ELSE 'MONITOR'
        END                                     AS priority_flag
    FROM champion_forecasts
    WHERE data_type = 'forecast'
    GROUP BY node_name, resource
    HAVING MAX(yhat_upper) >= 95
    ORDER BY projected_peak DESC
""").df()

risks.to_csv("capacity_risk_report.csv", index=False)
```

The report is supplemented by a visual gallery of 400+ individual forecast
plots — one PNG per host-resource pair showing two years of history, the
champion model forecast line, and the 80% prediction interval shaded. Teams
can drill from a row in the risk report directly to the visual evidence for
that system.

---

## Streamlit Risk Dashboard

The Streamlit dashboard is the primary interface for capacity teams reviewing
the monthly forecast cycle. Reads directly from the DuckDB champion forecast
database and the risk report CSV.

**Dashboard views**

Executive metrics bar — total capacity risks, high-priority count, fleet-wide
average utilization across all 4 KPIs.

Risk inventory table — all breach-flagged systems with earliest breach date,
projected peak, priority — high-priority rows highlighted.

Forecast viewer — per-host, per-resource drill-down — history, champion model
forecast, and confidence bands.

Fleet scenario summary — distribution of behavioral classifications; how many
systems in each scenario this month.

Model tournament results — champion model distribution across fleet; which
model won on how many series.

---

## Engineering Practices

**Idempotency** — DuckDB tables are dropped and recreated at each pipeline run.
Parquet outputs are overwritten. Re-running on the same input always produces
the same output. Safe to rerun without manual cleanup.

**Validation gates** — entrance criteria checked before each stage: minimum
row counts, required column presence, behavioral variety coverage. Exit
criteria verified after: output row counts, schema conformance, breach
detection sanity checks.

**Structured logging** — per-stage execution timer context manager logs start
time, duration, row counts in/out, and PASS/FAIL status. Logs written to
`/logs/` directory with timestamped filenames.

**Failure isolation** — each host-resource series is forecasted in a
try/except block. A single series failure (e.g., insufficient data for SARIMA)
logs the error and skips that series rather than aborting the entire fleet run.

**MLflow experiment tracking** — model parameters, MAPE scores, training data
stats, and forecast artifact paths logged per run. Enables comparison across
forecast cycles and detection of model drift over time.

**Parallelization** — Phase 1: ProcessPoolExecutor (multiprocessing) to bypass
the Python GIL. Phase 2: Spark Grouped Map UDF distributes across 10 G.2X
Glue workers.

**Throughput optimization** — Prophet `uncertainty_samples` reduced from 1,000
to 100 in Phase 2 turbo mode. 10x throughput gain with negligible interval
accuracy degradation at fleet scale.

---

## Lessons Learned

**Validate locally before migrating to cloud.**
Phase 1 proved that the tournament framework worked, that logistic growth was
the right Prophet configuration, that the 95% breach threshold was calibrated
correctly, and that the behavioral classification was meaningful. By the time
the AWS migration happened, every design decision had been tested. The cloud
investment landed on a proven foundation rather than an untested hypothesis.
The cloud doesn't fix a broken model — it just scales the broken output faster.

**No single model wins across a heterogeneous fleet.**
The tournament framework adds engineering complexity, but it materially
improves forecast quality across the fleet. A STEADY_GROWTH server and a BURST
server should not be modeled identically. The effort of building champion
selection pays back in a risk report that is more trustworthy — teams can act
on it rather than discounting it because "the model doesn't fit our workloads."

**Logistic growth is not optional for utilization forecasting.**
Linear trend Prophet will forecast utilization above 100% on high-growth
series. That number is nonsensical — you can't use 110% of CPU. Logistic
growth with `cap=100` forces the model to recognize the physical ceiling,
producing forecasts that slow their growth rate as utilization approaches the
limit. This is both more accurate and more interpretable for the infrastructure
teams consuming the output.

**The Grouped Map UDF pattern is the right way to scale Python ML on Spark.**
Trying to run Prophet natively distributed inside Spark is the wrong
abstraction. The pattern — one partition per series, one complete independent
model fit per UDF call, Spark handles distribution — is clean, debuggable, and
scales linearly with the number of workers.

---

## Interview Q&A

**Why did you choose a model tournament rather than a single forecasting algorithm?**

A fleet of tens of thousands of servers has behavioral heterogeneity that no single model
fits well across all series. Prophet is excellent on seasonal systems with
structured weekly and annual cycles. SARIMA is precise on series with clean
weekly periodicity and low noise. XGBoost wins on trend-dominated series where
gradient boosting on simple time features outperforms Prophet's flexible
seasonality components on series that don't actually have strong seasonal
structure.

Picking one model for everything means accepting poor forecast quality on the
series where it doesn't fit — and those are often the BURST or CAPACITY_BREACH
scenarios where forecast accuracy matters most. The tournament adds engineering
complexity but produces a risk report that's meaningfully more trustworthy,
which directly determines whether infrastructure teams act on it or discount it.

---

**Why did you use logistic growth mode in Prophet rather than the default linear mode?**

Utilization is bounded between 0% and 100%. A linear trend model doesn't know
that — it will happily forecast 115% CPU on a high-growth system, which is a
physically meaningless number. Logistic growth with `cap=100` and `floor=0`
forces Prophet to recognize the physical ceiling. As utilization approaches
the cap, the model's growth rate naturally slows to reflect that the system
cannot grow past its physical maximum.

This produces realistic long-horizon forecasts for high-utilization systems —
the ones that matter most for capacity planning. It also makes the upper
confidence interval more meaningful for breach detection: when `yhat_upper`
approaches 95%, you can act on that number knowing it's bounded by physical
reality.

---

**How does the PySpark Grouped Map UDF pattern work for distributing Prophet across Glue workers?**

Prophet is single-threaded Python — it can't natively parallelize across a
Spark cluster. The Grouped Map UDF pattern works around this by treating each
host-resource pair as an independent group. The data is structured so each
partition contains one complete time series. Spark automatically distributes
partitions across worker nodes. Each worker calls the UDF function with a
Pandas DataFrame for one series, fits a complete independent Prophet model,
generates the 180-day forecast, and returns the result. Spark collects all
results into a distributed DataFrame that's then written to S3 as Parquet.

No cross-partition communication, no shared state, no coordination overhead.
With 10 G.2X workers, 65,000+ metrics are processed in parallel — the wall-clock
time is a fraction of sequential execution.

---

**How did you handle the seasonality and holiday effects in the forecast?**

Infrastructure utilization has layered periodicity: weekly business cycles
where weekday loads differ from weekends, monthly cycles driven by batch jobs
and billing runs at month-end, quarterly patterns from business planning
cycles, and annual effects from year-end processing and holiday traffic.
Prophet handles all of these natively through its decomposable model structure
— weekly and yearly Fourier seasonality terms, plus an explicit holiday
regressor for known calendar events. SARIMA's `seasonal_order=(1,1,1,7)`
captures the weekly period. XGBoost uses month-of-year as an explicit feature
for annual seasonality.

The behavioral classification layer ensures that heavy seasonal models are
applied to series with actual seasonal structure — fitting a seasonal model
to a LOW_IDLE server that barely moves adds noise rather than signal.

---

**Why two confidence tiers — three months high-confidence and six months directional?**

Forecast uncertainty accumulates with horizon. Treating a five-month forecast
with the same confidence as a five-week forecast leads to either
under-reaction or over-reaction, depending on which horizon you calibrate for.

Prophet's Bayesian uncertainty quantification naturally produces wider
prediction intervals as the horizon extends — the three-month near-term
intervals are tight enough to make concrete procurement and scaling decisions.
The four-to-six month window has wider intervals, but still carries a
meaningful trajectory signal for planning conversations, budget requests, and
architecture review scheduling.

Separating these two tiers explicitly in the output ensures teams understand
what they're looking at — they're not comparing a three-month number to a
five-month number as if they had the same reliability.

---

**What was the key engineering lesson from the Phase 1 to Phase 2 migration?**

Validate the approach locally before spending on infrastructure. Phase 1 proved
that the tournament framework worked, that logistic growth was calibrated
correctly, that the 95% breach threshold was producing the right risk
classifications, and that behavioral scenario labeling was meaningful. By the
time the AWS migration happened, every design decision had been tested on real
data with real model fits. The migration was a well-defined engineering
problem: move data to S3, wrap the proven Prophet logic in a Grouped Map UDF,
deploy to Glue. We weren't figuring out whether the forecasting approach was
right at the same time as figuring out the cloud architecture.

Sequencing validation before scaling is a discipline that applies to any ML
pipeline — the cloud doesn't fix a broken model, it just scales the broken
output faster.

[Back to TOC](#toc)

