# HorizonScale Forecasting Story — Apple Cloud Capacity Interview Prep

## 30-second simple answer
```text
HorizonScale was a telemetry-driven capacity forecasting engine I built to replace
manual, reactive planning. It used signals like CPU, memory, P95 utilization,
and historical trend data from infrastructure monitoring sources.

I used SQL and Python for extraction, cleaning, aggregation, and feature prep,
with PySpark for larger telemetry volumes. For forecasting, I used Prophet and
scikit-learn depending on the pattern. The goal was to identify capacity risks
before they became incidents and support better planning decisions.
```

## 60-second deeper answer
```text
The business problem was that capacity planning was too manual and often
reactive, so teams found bottlenecks late.

The data came from telemetry across thousands of endpoints, including CPU,
memory, P95 utilization, trend history, and monitoring/capacity feeds.

The pipeline was practical: SQL extraction and historical aggregation,
Python/Pandas cleanup and validation, PySpark processing when scale demanded it,
then feature preparation and forecast output generation.

For models, I used Prophet when time-series trend and seasonality were important,
scikit-learn for feature-based prediction/risk scoring, and statistical
baselines/thresholds for explainable risk flags.

The outputs were forecasted bottlenecks, utilization insights,
underutilization detection, and planning recommendations delivered through
stakeholder dashboards and reporting.
```

## Model explanation in plain English

### A. Prophet
```text
I used Prophet for time-series forecasting. It works well when utilization has
clear trend and seasonal behavior (for example weekly/monthly patterns).

It helps answer: "When will this system cross a capacity threshold?"
```

### B. scikit-learn
```text
I used scikit-learn when the problem was more feature-driven than pure
seasonality.

Inputs could include utilization history, growth rate, historical peaks,
endpoint attributes, and threshold behavior. This helped identify risk patterns
and prioritize which systems needed action first.
```

### C. Statistical baselines / thresholds
```text
I used simple baselines for explainability: P95 utilization, growth trend,
headroom, and threshold-breach risk.

These are useful because capacity stakeholders trust clear threshold/headroom
logic and can act on it quickly.
```

### D. SQL/Python logic
```text
SQL prepared historical aggregates and core slices.

Python cleaned data, calculated trends, trained models, and generated outputs.
Pandas handled shaping and validation. PySpark helped when telemetry volume was
large.
```

## Best answer if Sarah asks: "What models did you use?"
```text
I used Prophet for time-series forecasting where trend and seasonality mattered,
scikit-learn for feature-based prediction and risk scoring, and simpler
statistical baselines for explainable threshold/headroom analysis.

I did not treat the model as the product by itself — the value was turning
telemetry into planning actions.
```

## Best answer if Sarah asks: "What did the input data look like?"
```text
Typical fields included:
- endpoint/server/application identifier
- timestamp/date
- CPU utilization
- memory utilization
- P95 metric
- historical peak/trend
- capacity threshold
- environment/application grouping (when available)
- monitoring/capacity source (for example TrueSight/TSCO, CA Wily, AppDynamics)
- optional cloud/platform mapping (when available)
```

## Best answer if Sarah asks: "How did you validate the forecasts?"
```text
I validated forecasts with practical checks:
- back-testing against historical windows
- comparing forecasted risk vs. later actual utilization
- checking output against known incidents/capacity reviews where available
- reviewing false positives/false negatives with SMEs

I preferred explainable forecasts because capacity decisions need trust.
```

## Best answer if Sarah asks: "How did this support cloud capacity or cost efficiency?"
```text
Forecasting reduced reactive over-provisioning. Underutilization detection
supported rightsizing and consolidation conversations. Trend forecasting helped
teams plan future demand.

The reporting gave stakeholders a basis for where to add capacity, tune
workloads, or reclaim unused resources. Even when telemetry originated in
enterprise infrastructure, the same method applies to cloud resources:
utilization, allocation, forecasted demand, rightsizing, and efficiency.
```

## STAR story
```text
Situation:
Manual capacity planning was slow and reactive.

Task:
Build a repeatable forecasting process from infrastructure telemetry.

Action:
Used SQL, Python/Pandas, PySpark, Prophet, scikit-learn, P95 utilization, and
historical telemetry feeds to generate forecasts and capacity-risk outputs.

Result:
Improved visibility into future bottlenecks, supported planning conversations,
surfaced underutilized resources, and gave leadership clearer capacity
reporting.
```

## Whiteboard-style architecture
```text
Telemetry Sources
  -> SQL extraction / historical store
  -> Python/Pandas cleanup
  -> PySpark processing for large telemetry sets
  -> Feature engineering: P95, trend, growth rate, headroom, thresholds
  -> Forecasting models: Prophet + scikit-learn + baselines
  -> Outputs: risk list, bottleneck forecast, underutilization report,
     dashboard/executive summary
```

## Words Sean should use
- telemetry-driven forecasting
- P95 utilization
- headroom
- demand trend
- seasonal pattern
- bottleneck prediction
- forecast horizon
- rightsizing candidate
- underutilized resource
- explainable threshold
- stakeholder reporting
- capacity risk score
- planning recommendation

## Words Sean should avoid
- "I built deep learning models"
- "I owned GCP production forecasting"
- "It was just a dashboard"
- "I only did physical servers"
- "The model was perfect"
- "Finance owned it so I did not touch cost"
- "I don't remember the details"

## Final memorized answer
```text
My forecasting work was telemetry-driven capacity planning. I used SQL and
Python to turn historical CPU, memory, and P95 utilization into clean
time-series datasets, then used Prophet, scikit-learn, and explainable
threshold logic to forecast bottlenecks and identify underutilized resources.

The purpose was not just prediction — it was to give infrastructure and
leadership teams enough lead time to plan capacity, improve utilization, and
make cost-aware decisions.
```

## Memorize this answer for the call
```text
My forecasting work was telemetry-driven capacity planning. I used SQL and
Python to turn historical CPU, memory, and P95 utilization into clean
time-series datasets, then used Prophet, scikit-learn, and explainable
threshold logic to forecast bottlenecks and identify underutilized resources.

Prophet was useful when the pattern had trend or seasonality. scikit-learn was
useful when I wanted to combine multiple features like growth rate, historical
peaks, headroom, and threshold behavior. I also kept simple baselines like P95
utilization and headroom because capacity planning needs to be explainable to
infrastructure and leadership teams.

The purpose was not just prediction — it was to give teams enough lead time to
plan capacity, improve utilization, and make cost-aware infrastructure
decisions.
```
