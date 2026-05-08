# HorizonStudy vs AWS-CapacityForecaster — Comparison and Talk Track

## 1. Simple Difference
- HorizonStudy: strongest for telemetry pipeline depth, high-volume time-series processing, and model competition flow with Python + DuckDB/Parquet + parallel processing.
- AWS-CapacityForecaster: strongest for AWS-first implementation angle, modular cloud-capacity workflow, and S3/SageMaker-compatible execution patterns.

## 2. How They Fit Together
Together they support one end-to-end interview story:
telemetry ingestion -> processing/normalization -> feature engineering -> forecasting -> risk/cost-oriented outputs -> planning recommendations.

HorizonStudy strengthens the processing/forecast workflow narrative.
AWS-CapacityForecaster strengthens AWS/cloud implementation and automation narrative.

## 3. Best Combined Interview Answer
I usually explain these as two complementary projects. HorizonStudy is where I focused on telemetry pipeline engineering and forecasting workflow depth: preparing model-ready time-series data, scaling forecast runs, and producing risk-oriented outputs. AWS-CapacityForecaster is where I emphasize cloud implementation, using a modular pipeline with ETL, feature engineering, model training, and risk analysis that aligns with AWS patterns like S3 artifact flow and SageMaker-compatible execution.

Across both, the common method is telemetry-driven capacity planning: calculate utilization pressure, use measures like P95/headroom/forecast variance, identify likely risk or waste, and produce practical outputs that teams can act on. I position this as applied forecasting and capacity engineering, not deep research ML.

## 4. Which Project To Mention For Which Question
| Question Type | Best Project To Mention | Why |
|---|---|---|
| PySpark / big data processing | HorizonStudy | Strong telemetry pipeline and scale-oriented processing narrative (plus modernization docs). |
| AWS cloud capacity | AWS-CapacityForecaster | Clear AWS utils, S3 and SageMaker integration paths. |
| cost efficiency | AWS-CapacityForecaster | Risk/optimization module and cloud execution framing. |
| forecasting | Both | HorizonStudy for workflow depth; AWS project for cloud-aligned implementation. |
| automation | AWS-CapacityForecaster | Modular runner and script-driven cloud/local execution patterns. |
| telemetry feature engineering | AWS-CapacityForecaster | Explicit ETL feature engineering module. |
| stakeholder reporting | Both | HorizonStudy risk outputs + AWS project report/analysis outputs. |
| SQL/Python coding | Both | Python-heavy modular code with data processing and analysis logic. |
| model validation | Both | HorizonStudy model competition; AWS project metrics/backtest-style evaluation paths. |

## 5. Safe Claims
- HorizonStudy contains a multi-stage forecasting pipeline with synthetic data, processing, model runs, competition, and risk reporting.
- AWS-CapacityForecaster contains modular ETL/ML/risk modules and AWS integration utilities (S3/SageMaker paths).
- Both projects support telemetry-driven capacity analysis and practical forecasting discussion.
- AWS is the stronger hands-on cloud angle based on repository evidence.

## 6. Claims To Avoid
- Avoid claiming broad enterprise production deployment unless Sean confirms.
- Avoid claiming deep GCP ownership.
- Avoid claiming deep Kubernetes platform administration ownership.
- Avoid claiming perfect model accuracy.
- Avoid claiming direct ownership of enterprise billing/procurement systems unless Sean confirms.

## 7. Bridge To Apple Role
These projects map well to Apple Cloud Capacity & Efficiency themes:
- cloud capacity: telemetry-to-risk forecasting pattern
- telemetry automation: repeatable ETL, feature pipelines, and modular execution
- cost efficiency: risk and optimization logic tied to utilization and planning
- EKS/Kubernetes concepts: transferable analysis method (requests/limits/usage/headroom), without overclaiming deep platform ownership
- S3/storage concepts: explicit S3 artifact handling and cloud data paths
- AWS-first positioning: AWS-CapacityForecaster provides strongest hands-on cloud discussion
