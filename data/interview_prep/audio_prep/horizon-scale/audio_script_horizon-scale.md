# Audio Script — HorizonScale: Time-Series ML Forecasting at Scale
# Slug: horizon-scale
# HOST voice: nova | SEAN voice: onyx
# Chunk target: ~750 chars

---

**[HOST — voice: nova]**
Today we're covering HorizonScale — a time-series machine learning platform Sean built to forecast infrastructure capacity across thousands of servers. Sean, start with the problem. What were you trying to predict, and at what scale?

**[SEAN — voice: onyx]**
The same four K-P-Is from capacity planning work — C-P-U, memory, disk, and network utilization — but this time the goal was forecasting, not just reporting current state. The question we needed to answer was: given two years of P-ninety-five telemetry history, where will each system's utilization be in three to six months? Multiplied across two thousand-plus servers, that's more than eight thousand individual time series to model. You can't do that manually. You need a pipeline that trains models, selects the best one per series, detects emerging capacity risks, and surfaces the findings in a way that's actionable for infrastructure teams.

**[HOST — voice: nova]**
Why the two-tier confidence window — three months and six months?

**[SEAN — voice: onyx]**
Forecasting reliability degrades with horizon. Three months out, you have enough signal from the recent trend, the weekly cycle, the monthly business rhythm, and seasonal patterns that your confidence intervals are tight enough to act on. That's what we call the high-confidence window — teams can make procurement and architecture decisions based on those numbers. Six months is directional — it gives a meaningful signal about trajectory, but the uncertainty bands are wider. The design explicitly separates these two windows in the output so teams understand what they're looking at. A three-month near-capacity warning drives immediate action. A six-month signal starts a planning conversation.

**[HOST — voice: nova]**
Seasonality and business cycles are a big part of this. What did that look like in the data?

**[SEAN — voice: onyx]**
Infrastructure utilization has layered periodicity. Weekly cycles are the most obvious — weekday workloads look very different from weekend. Monthly cycles reflect billing runs, batch jobs, reporting cycles that fire at month-end. Quarterly and annual patterns reflect business planning cycles, end-of-year processing, and the kind of traffic surge that happens around holidays. A model that doesn't account for all of these will systematically mis-forecast on the days that matter most — the ones where systems are under the most load. The fleet was classified into behavioral scenarios to make this tractable: steady growth, seasonal, burst, low-idle, and capacity-breach. Each scenario has distinct patterns that the models needed to capture appropriately.

**[HOST — voice: nova]**
Walk me through the two phases of the project. What was Phase One?

**[SEAN — voice: onyx]**
Phase One was the local Apache stack — building the pipeline end to end using open-source tools. Data stored as Parquet files, queried and processed through DuckDB using Polars for high-speed dataframe operations. The forecasting layer ran three model families: Facebook Prophet, which handles trend and multi-frequency seasonality natively; SARIMA with a weekly seasonal period; and Exponential Smoothing, which is robust and fast. Each model produced a hundred-eighty-day forecast with confidence intervals. Streamlit provided the internal dashboard for reviewing results and drilling into individual hosts.

**[HOST — voice: nova]**
How did you choose which model to use for each series?

**[SEAN — voice: onyx]**
A model tournament — sometimes called a champion-challenger framework. The pipeline uses the first thirty-two months of data for training, then holds out the most recent four months as a backtest window that none of the models saw during training. Prophet, SARIMA, and later X-G-Boost compete on M-A-P-E — mean absolute percentage error — against those four held-out months of real data. The model with the lowest M-A-P-E on the backtest is selected as champion for that host and resource combination. So different models can win on different series. Prophet might be champion for a server with strong seasonal patterns, while SARIMA wins on a server with a simple trend and weekly cycle. The selection is per-series, not per-project.

**[HOST — voice: nova]**
Prophet is doing more than just fitting a trend line — how does it handle seasonality and capacity constraints?

**[SEAN — voice: onyx]**
Prophet is a decomposable model — it separates the signal into a trend component, seasonality components at multiple frequencies, and holiday effects. For this use case, we used logistic growth mode rather than linear, which is important: it constrains the forecast to be physically bounded between zero and a hundred percent utilization. A linear trend model will happily forecast a hundred and twenty percent C-P-U, which is meaningless. Logistic growth with cap set to a hundred forces the model to recognize that the rate of increase must slow as utilization approaches the ceiling. Combined with daily seasonality for within-day patterns and weekly seasonality for the business cycle, Prophet produced well-calibrated forecasts for systems with structured periodic behavior.

**[HOST — voice: nova]**
What was Phase Two?

**[SEAN — voice: onyx]**
Phase Two was the A-W-S migration. The local pipeline proved the approach worked, but running eight thousand-plus time-series models sequentially — even parallelized across local C-P-U cores — hits a wall. Phase Two moved the data layer to an S-3 data lake with a structured partition layout: raw telemetry in Parquet, forecast outputs, and Athena result sets. The forecasting layer moved to A-W-S Glue with ten G-dot-two-X workers running Spark three-dot-three. The key pattern is a Py-Spark Grouped Map U-D-F — one partition per host and resource pair, Prophet fitting entirely inside the U-D-F function. Glue distributes the eight-thousand-plus partitions across the worker fleet automatically.

**[HOST — voice: nova]**
So Prophet is running inside Spark — one host per partition?

**[SEAN — voice: onyx]**
Exactly. The Grouped Map U-D-F is the right pattern for this problem because Prophet is single-threaded Python — it can't natively parallelize across a Spark cluster. But if you structure your data so each group is one host-resource pair, Spark distributes the groups across workers and each worker runs Prophet independently. The U-D-F receives a Pandas dataframe for one series, fits Prophet, generates the hundred-eighty-day forecast, and returns the result. Spark collects all results back into a distributed dataframe. The throughput difference between local multiprocessing and Glue at ten workers is dramatic.

**[HOST — voice: nova]**
And the X-G-Boost challenger — how does that fit in?

**[SEAN — voice: onyx]**
X-G-Boost is the challenger model — it uses a different approach from Prophet. Rather than decomposing the time series into trend and seasonality components, it learns the relationship between engineered features and the target. The features are simple but effective: an ordinal time index capturing the trend, and month-of-year capturing annual seasonality. X-G-Boost with CUDA acceleration runs on the same thirty-two-month training and four-month backtest split as Prophet. On some series — particularly the ones with strong trend and weak periodicity — X-G-Boost wins the tournament over Prophet. The ensemble selection gives you the best model per series rather than committing the entire fleet to one algorithm.

**[HOST — voice: nova]**
What does the risk output look like?

**[SEAN — voice: onyx]**
Two layers. First, a capacity risk report that flags every host-resource pair where the upper confidence interval of the forecast reaches or exceeds ninety-five percent utilization within the six-month window — that's the breach threshold. Priority flags go on systems where the forecast shows high volatility, measured as standard deviation greater than two percentage points, or where projected peaks exceed a hundred and five percent — which in a logistic-bounded model indicates the system is being pushed hard against its ceiling. The second layer is the visual gallery — four hundred-plus individual forecast plots, one per host per resource, showing history, the champion model forecast, and confidence bands. Teams can drill directly from the risk report into the evidence for any flagged system.

**[HOST — voice: nova]**
What was the hardest engineering problem across both phases?

**[SEAN — voice: onyx]**
Scale and heterogeneity. Eight thousand-plus series, each with a different behavioral pattern, different noise level, different seasonality signature. No single model configuration works for all of them. A Prophet configuration tuned for a server with strong weekly seasonality will produce poorly calibrated forecasts for a server in the LOW-IDLE scenario that barely moves. The model tournament solves the selection problem, but building infrastructure that trains, backtests, and selects champion models at that scale — reliably, with structured logging, idempotent reruns, and failure isolation so one bad series doesn't abort the entire fleet — required serious pipeline engineering on top of the modeling work.

**[HOST — voice: nova]**
Local open-source stack first, then A-W-S — that's a deliberate sequencing.

**[SEAN — voice: onyx]**
Always validate the approach before spending on infrastructure. The local phase proved that the tournament framework worked, that the models were producing calibrated forecasts, that the risk detection logic was flagging the right systems. Once that was proven, the A-W-S migration was a well-understood engineering problem: move data to S-3, wrap the proven Prophet logic in a Py-Spark U-D-F, deploy to Glue. You're not figuring out whether the approach is right at the same time as you're figuring out the infrastructure. Sequencing it this way means the cloud investment lands on a validated foundation.

---
END OF SCRIPT
Voices: HOST (nova), SEAN (onyx)
Project: HorizonScale — Time-Series ML Forecasting at Scale
Slug: horizon-scale
