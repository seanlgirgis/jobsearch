# SAMSUNG HM INTERVIEW — AUDIO PLAY SCRIPT 4
# SQL and Python

## STRICT INSTRUCTIONS FOR NOTEBOOKLM

This is a word-for-word audio interview script. You are not summarizing. You are not discussing. You are performing a live job interview as two characters.

- **Host 1** is DAVID — the Hiring Manager at Samsung Austin Semiconductor. David is testing analytical and coding depth.
- **Host 2** is SEAN — the candidate. Sean explains clearly and answers exactly as written.
- Read every line exactly as written. Do not paraphrase. Do not add commentary. Do not break character.

---

DAVID: Let's talk SQL. If I asked you to write a query to identify the top five bottleneck tools by average utilization over the last thirty days, how would you approach it?

SEAN: Straightforward query. I would select tool ID and tool name from the telemetry table, calculate average utilization and peak utilization as aggregates, and count the number of readings per tool. I would filter to only the last thirty days using a date comparison on the reading timestamp. Group by tool ID and tool name so I get one row per tool. Order by average utilization descending. Limit to five results. The reason I use average rather than just peak is that average identifies tools that are consistently loaded — a tool that spikes once is noise, a tool that averages eighty-five percent for thirty days is a structural bottleneck. Peak catches the worst-case pressure. Together they distinguish chronic overload from occasional spikes.

DAVID: Good. What if I need to find tools that have been above eighty-five percent utilization for three or more consecutive days?

SEAN: That is the gaps-and-islands pattern in SQL. I would use three layers. First, aggregate to one row per tool per day — daily average utilization. Second, flag each day as over threshold or not. Third, use the double row-number trick to identify consecutive runs: assign a row number ordered by date across all rows for a tool, then assign a second row number ordered by date but only within rows sharing the same flag value. Subtract the second from the first. For a consecutive run of over-threshold days, that difference stays constant — that constant becomes the group identifier for the streak. Then I group by tool and group identifier, filter where the flag equals one, count the days in each group, and keep only streaks of three or more days, ordered by streak length descending. The result is every tool with a sustained utilization problem, ranked by severity.

DAVID: How do you approach optimizing a slow query?

SEAN: I start with the execution plan — EXPLAIN or EXPLAIN ANALYZE to see what the database is actually doing. I look for three things: full table scans where an index scan should exist, hash joins on large unindexed tables, and row estimate errors that indicate stale statistics. For analytical queries specifically: I verify partition pruning is working — date filters should eliminate large chunks of data before any aggregation. I use window functions to avoid self-joins, which are expensive. In Oracle specifically I watch for missing histogram statistics on skewed columns, which cause bad cardinality estimates and wrong join order. General rules: push filters as early as possible, avoid selecting all columns when you only need a few, and index the columns used in join conditions and high-cardinality filter predicates.

DAVID: Tell me about window functions — when and how do you use them?

SEAN: Window functions compute aggregates over a sliding context without collapsing rows — that is the key distinction from GROUP BY. I use LAG and LEAD to access the previous or next row's value without a self-join — for example, calculating day-over-day utilization change per tool. I use ROW_NUMBER to get the most recent record per tool, or RANK to rank tools by utilization within a tier. I use running average over a window to compute a seven-day or thirty-day moving average — smoothing telemetry noise so spikes do not hide the underlying trend. The syntax for a rolling seven-day average per tool is: average of utilization partitioned by tool ID, ordered by date, rows between six preceding and current row. That computes the average of today and the six days before it, independently for each tool. I also use NTILE to bucket tools into utilization quartiles for tiered capacity reporting.

DAVID: How do you handle large-scale time-series telemetry processing in Python?

SEAN: For banking-scale telemetry — thousands of assets, years of history — I use PySpark. It distributes the load across a cluster, handles partitioning automatically, and integrates natively with S3 and Redshift through AWS Glue. For medium-scale datasets: Pandas with chunked reads and vectorized operations. The key discipline is avoiding row-level Python loops — use NumPy-backed vectorized operations instead, which are orders of magnitude faster. For HorizonScale specifically I used a generator-based parallel pipeline — each asset's time-series fed through a generator yielding one asset at a time rather than loading everything into memory. Assets processed independently and parallelized using Python's multiprocessing Pool. This produced a ninety percent cycle time reduction compared to the original sequential design because forecasting models for different assets ran simultaneously.

DAVID: Walk me through how you would build a capacity forecasting model in Python.

SEAN: I use Prophet from Facebook's open-source library — it is designed for time-series data with seasonality and trend. The function takes a dataframe of historical telemetry — dates and utilization percentages — and a forecast horizon, defaulting to one hundred eighty days, which is six months ahead. Inside the function: rename the columns to the format Prophet expects — date column to DS and utilization to Y. Instantiate a Prophet model with yearly seasonality, weekly seasonality, and a changepoint prior scale of point zero five — a conservative value that prevents the model from overfitting to short-term volatility. Fit the model to historical data. Generate a future dataframe for the forecast horizon. Predict over that window. The output returns the date, the expected forecast value, and the upper and lower confidence bounds. The upper confidence bound is the capacity risk signal — if it crosses the utilization threshold within the forecast window, that asset is flagged at risk even though the expected value has not yet breached the threshold. You plan for the worst plausible case, not just the median outcome.

DAVID: What does your standard Python data analysis stack look like?

SEAN: Core: Pandas and NumPy for data manipulation, SQLAlchemy for database connectivity to Oracle and Redshift. Visualization: Matplotlib and Seaborn for static plots, Plotly for interactive charts, Streamlit for executive-facing dashboards that non-technical stakeholders can navigate directly. Machine learning: scikit-learn for classification and regression — specifically Random Forest and Gradient Boosting for binary risk classification. Prophet for time-series forecasting. Scale: PySpark on AWS Glue for distributed processing when the dataset exceeds what a single machine can handle. Engineering discipline: type hints on all functions, Pydantic for data model validation at pipeline boundaries, pytest for unit and integration testing, and Black with ruff for consistent code formatting.

DAVID: Good — that gives me a solid picture of your technical depth. Thank you Sean.

SEAN: Thank you David. I appreciate the thorough conversation and I look forward to hearing about next steps.

---

## END OF SCRIPT 4
