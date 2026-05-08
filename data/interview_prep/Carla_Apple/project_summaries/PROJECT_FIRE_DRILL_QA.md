# Project Fire Drill Q&A

1. **Q: What was HorizonStudy?**  
**A:** Based on the files inspected, I would position it as a telemetry-processing and forecasting pipeline workspace that goes from data prep to model outputs and risk reporting.

2. **Q: What was AWS-CapacityForecaster?**  
**A:** An AWS-oriented modular capacity forecasting project with ETL, model training, risk analysis, and S3/SageMaker-compatible execution paths.

3. **Q: What is the difference between the two?**  
**A:** HorizonStudy emphasizes forecasting workflow depth and pipeline processing; AWS-CapacityForecaster emphasizes AWS cloud implementation and modular automation.

4. **Q: What data did you process?**  
**A:** Telemetry-style time-series capacity data (utilization/forecast/risk-oriented fields), including synthetic and processed datasets based on inspected files.

5. **Q: What features did you calculate?**  
**A:** Based on inspected modules: lag and rolling features, seasonal/calendar indicators, and risk-oriented derived fields.

6. **Q: What models did you use?**  
**A:** Prophet and scikit-learn family models are clearly present; HorizonStudy also references challenger competition paths.

7. **Q: Why Prophet?**  
**A:** It is practical for trend/seasonality forecasting and gives interpretable forecast outputs for capacity planning.

8. **Q: Why scikit-learn?**  
**A:** For feature-driven predictive modeling and complementary baselines/challengers next to time-series models.

9. **Q: Why PySpark?**  
**A:** Based on files inspected, I would position large-scale distributed processing as part of the broader telemetry-at-scale story; use this carefully unless Sean confirms direct PySpark-heavy execution in these exact repos.

10. **Q: Why SQL?**  
**A:** SQL is key for aggregation, rollups, and validation queries in telemetry and capacity workflows.

11. **Q: How did you validate forecasts?**  
**A:** I would cite backtest-style evaluation, metrics comparison, and practical review against threshold/risk behavior.

12. **Q: How did you avoid overclaiming model accuracy?**  
**A:** I describe relative improvement and decision usefulness, not perfection; I avoid claiming universal accuracy guarantees.

13. **Q: How did this support cost savings?**  
**A:** By surfacing risk and underutilization patterns that support rightsizing and better capacity allocation decisions.

14. **Q: How does this map to AWS?**  
**A:** The AWS-CapacityForecaster repo shows S3 data paths, AWS utilities, and SageMaker-compatible execution flows.

15. **Q: How would this map to EKS/Kubernetes?**  
**A:** Transferable method: compare requested vs actual usage, calculate P95/headroom, and classify risk/waste by workload/namespace.

16. **Q: How would this map to S3?**  
**A:** Use S3 for pipeline artifacts and storage analytics inputs; monitor growth and ownership tags for efficiency decisions.

17. **Q: What would you automate first?**  
**A:** Data ingestion/cleanup, repeatable feature generation, risk flagging, and scheduled stakeholder-ready report exports.

18. **Q: Batch or streaming?**  
**A:** Usually batch-first for planning and cost analysis; streaming is mainly for near-real-time alerting scenarios.

19. **Q: How often would you collect metrics?**  
**A:** Typical practical cadence: 5-15 minute telemetry samples, hourly rollups, daily cost/efficiency reports.

20. **Q: What did you actually code?**  
**A:** Pipeline modules for ETL/feature engineering, model training orchestration, risk analysis logic, and AWS utility flows.

21. **Q: What was hard?**  
**A:** Data consistency, schema alignment across stages, and keeping model outputs explainable for planning decisions.

22. **Q: What would you improve?**  
**A:** Stronger data contracts, drift monitoring, tighter validation dashboards, and clearer production runbooks.

23. **Q: How does this relate to BMC/TrueSight/Helix?**  
**A:** Similar analytics pattern: once telemetry is available, normalize fields, compute risk/waste indicators, and report actions.

24. **Q: How would you explain this to a manager?**  
**A:** I built repeatable telemetry-to-decision workflows that improve lead time for capacity planning and reduce reactive firefighting.

25. **Q: How would you explain this to a senior engineer?**  
**A:** Modular pipeline with explicit ETL, feature store logic, model training/evaluation, and risk classification outputs with clear handoffs.

26. **Q: Was this enterprise production at scale?**  
**A:** I would avoid claiming broad production ownership unless Sean confirms exact deployment scope.

27. **Q: Did you own AWS billing systems?**  
**A:** I would avoid claiming billing system ownership unless Sean confirms; I position this as technical capacity/risk analytics that informs cost decisions.

28. **Q: Did you deeply administer Kubernetes platforms?**  
**A:** I would avoid claiming deep platform-admin ownership unless Sean confirms; I frame Kubernetes as transferable capacity concepts.

29. **Q: Did you do deep ML research?**  
**A:** I position this as applied forecasting and capacity engineering, not research-level ML.

30. **Q: What is the one-line combined story?**  
**A:** I built telemetry-driven forecasting workflows and AWS-aligned capacity analytics that turn raw metrics into practical risk and efficiency decisions.
