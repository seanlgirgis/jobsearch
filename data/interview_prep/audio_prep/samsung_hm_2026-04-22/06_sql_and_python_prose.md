# Samsung HM Interview — Audio 6: SQL and Python
## What This Audio Covers
SQL and Python as described in prose — no code syntax read aloud. Each concept is explained the way you would speak it in an interview, including the logic behind each query and the thinking behind each Python approach.

---

## SQL: Top 5 Bottleneck Tools Query

If asked to write or explain a query that identifies the top bottleneck tools, here is the approach:

The query selects tool ID and tool name from a telemetry table. It calculates two aggregate metrics: average utilization percentage and peak utilization percentage — using average and max functions. It also counts the number of readings per tool. It filters to only the last 30 days using a date comparison on the reading timestamp. It groups by tool ID and tool name so we get one row per tool. Then it orders by average utilization descending and limits to 5 results.

The logic: average utilization identifies tools that are consistently loaded — not just occasionally spiking. Peak catches the worst-case pressure. Together they distinguish a tool that is always near capacity from one that occasionally spikes.

---

## SQL: Consecutive Days Over Threshold — Gaps and Islands Pattern

If asked to find tools that have been over an 85 percent utilization threshold for 3 or more consecutive days, this is the gaps-and-islands pattern.

The approach uses three layers of logic:

**Layer 1:** Aggregate daily average utilization per tool — one row per tool per day.

**Layer 2:** Flag each day as over threshold or not — 1 if daily average is 85 percent or higher, 0 otherwise.

**Layer 3:** Identify consecutive runs using the double row-number trick. Assign a row number ordered by date across all rows for a tool. Assign a second row number ordered by date but only within rows sharing the same flag value. Subtract the second from the first. For a consecutive run of "over threshold" days, this difference stays constant — that constant is the group identifier for that streak.

Then group by tool and the group identifier, filter where the flag equals 1, count the days in each group, and keep only streaks of 3 or more. Order by consecutive days descending to see the worst offenders first.

Why this matters for capacity planning: a tool spiking once is noise. A tool above threshold for 5 straight days is a structural signal requiring action.

---

## SQL: Query Optimization Approach

If asked how you optimize a slow query:

Start with the execution plan — use EXPLAIN or EXPLAIN ANALYZE to see what the database is actually doing. Look for full table scans where an index scan should exist, hash joins on large unindexed tables, and row estimate errors that indicate stale statistics.

For analytical queries specifically: check whether partition pruning is working — filters on date partitions should eliminate large chunks of data before any aggregation. Use window functions to avoid self-joins, which are expensive. In Oracle specifically, watch for missing histogram statistics on skewed columns — bad cardinality estimates lead to wrong join order choices. Note that Common Table Expressions sometimes materialize and sometimes do not — verify which is happening.

General rules: push filters as early in the query as possible, avoid selecting all columns when you only need a few, and index the columns used in join conditions and high-cardinality filter predicates.

---

## SQL: Window Functions

Window functions compute aggregates over a sliding context without collapsing rows — the key distinction from GROUP BY.

**LAG and LEAD:** Access the previous or next row's value without a self-join. Use case: calculate day-over-day utilization change per tool.

**ROW_NUMBER and RANK:** Assign a sequential number within a partition. Use case: get the most recent reading per tool, or rank tools by utilization within a tier.

**Running SUM and AVG OVER:** Calculate a rolling total or average. Use case: 7-day or 30-day moving average to smooth telemetry noise so spikes do not hide the trend.

**NTILE:** Divide rows into equal-sized buckets. Use case: bucket all tools into utilization quartiles for tiered capacity reporting — top 25 percent, next 25 percent, and so on.

The key syntax pattern for a rolling 7-day average: average of utilization partitioned by tool ID, ordered by date, rows between 6 preceding and current row. This computes the average of the current day and the 6 days before it, independently for each tool.

---

## Python: Processing Large Time-Series Telemetry

For banking-scale telemetry at Citi — thousands of assets, years of history — you used PySpark. PySpark distributes the load across a cluster, handles partitioning automatically, and integrates natively with S3 and Redshift through AWS Glue.

For medium-scale datasets: Pandas with chunked reads and vectorized operations. The key is to avoid row-level Python loops — use NumPy-backed vectorized operations instead, which are orders of magnitude faster.

For HorizonScale specifically: a generator-based parallel pipeline. Each asset's time-series was fed through a generator — yielding one asset at a time rather than loading everything into memory. Assets were processed independently and parallelized using Python's multiprocessing Pool. This produced a 90 percent cycle time reduction compared to the original sequential design because forecasting models for different assets ran simultaneously rather than one at a time.

---

## Python: Forecasting Model Architecture — HorizonScale

The forecasting model used Prophet, Facebook's open-source time-series library, designed for data with seasonality and trend.

The function takes a dataframe of historical telemetry — dates and utilization percentages — and a forecast horizon defaulting to 180 days, which is 6 months ahead.

Inside the function: the dataframe is renamed to the column format Prophet expects — date column renamed to "ds" and utilization renamed to "y." A Prophet model is instantiated with yearly seasonality, weekly seasonality, and a changepoint prior scale of 0.05 — a low value that makes the model conservative about trend changes, reducing overfitting on volatile data. The model is fitted to the historical data, a future dataframe is generated for the forecast horizon, and the model predicts over that future window.

The output returns four columns: the date, the expected forecast value, the lower confidence bound, and the upper confidence bound.

The upper confidence bound — "yhat upper" — is the capacity risk signal. If it crosses the utilization threshold within the forecast window, that asset is flagged as at risk even though the expected value has not yet breached the threshold. You are planning for the worst plausible case, not just the median.

---

## Python: Data Analysis Stack

The core stack: Pandas and NumPy for data manipulation, SQLAlchemy for database connectivity to Oracle and Redshift.

Visualization: Matplotlib and Seaborn for static plots, Plotly for interactive charts, Streamlit for executive-facing dashboards that non-technical stakeholders can use directly.

Machine learning: scikit-learn for classification and regression models — specifically Random Forest and Gradient Boosting for the binary risk classifier in HorizonScale. Prophet for time-series forecasting.

Scale: PySpark on AWS Glue for distributed processing when the dataset exceeds what a single machine can handle.

Engineering discipline: type hints on all functions for clarity and IDE support, Pydantic for data model validation at pipeline boundaries, pytest for pipeline unit and integration testing, Black and ruff for consistent code formatting.
