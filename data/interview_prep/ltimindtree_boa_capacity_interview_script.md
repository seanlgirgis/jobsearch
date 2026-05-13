# LTIMindtree / Bank of America Screening Interview Script

Role: IT Capacity Engineer / Performance and Capacity Engineer  
Core Positioning: Citi-scale capacity forecasting, telemetry pipelines, performance analytics, KPI reporting, executive decision support

## Table of Contents

1. [Opening / Tell me about yourself](#1-opening--tell-me-about-yourself)
2. [What attracted you to this role?](#2-what-attracted-you-to-this-role)
3. [What do you know about the client?](#3-what-do-you-know-about-the-client)
4. [Describe your Citi capacity work](#4-describe-your-citi-capacity-work)
5. [What tools did you use?](#5-what-tools-did-you-use)
6. [How did you forecast capacity?](#6-how-did-you-forecast-capacity)
7. [How do you explain capacity risk to leadership?](#7-how-do-you-explain-capacity-risk-to-leadership)
8. [How do you support capital planning or budgeting?](#8-how-do-you-support-capital-planning-or-budgeting)
9. [How do you handle bad or missing telemetry?](#9-how-do-you-handle-bad-or-missing-telemetry)
10. [How do you troubleshoot a performance bottleneck?](#10-how-do-you-troubleshoot-a-performance-bottleneck)
11. [Difference between performance engineering and capacity engineering](#11-what-is-the-difference-between-performance-engineering-and-capacity-engineering)
12. [How do you build KPI dashboards?](#12-how-do-you-build-kpi-dashboards)
13. [Tell me about operational playbooks](#13-tell-me-about-operational-playbooks)
14. [How do you work with application teams?](#14-how-do-you-work-with-application-teams)
15. [How do you work with executives?](#15-how-do-you-work-with-executives)
16. [What kind of infrastructure scale have you handled?](#16-what-kind-of-infrastructure-scale-have-you-handled)
17. [Do you have banking experience?](#17-do-you-have-banking-experience)
18. [Are you comfortable with onsite Plano?](#18-are-you-comfortable-with-onsite-plano)
19. [Why are you leaving / available?](#19-why-are-you-leaving--available)
20. [What is your strongest value for this role?](#20-what-is-your-strongest-value-for-this-role)
21. [What is your weakness or ramp-up area?](#21-what-is-your-weakness-or-ramp-up-area)
22. [Do you have cloud experience?](#22-do-you-have-cloud-experience)
23. [How do you handle conflicting stakeholder priorities?](#23-how-do-you-handle-conflicting-stakeholder-priorities)
24. [Describe a time you improved a process](#24-describe-a-time-you-improved-a-process)
25. [How do you handle RCA?](#25-how-do-you-handle-rca)
26. [What questions do you have for us?](#26-what-questions-do-you-have-for-us)
27. [Strong closing](#27-strong-closing)
28. [Emergency short version if your mind freezes](#28-emergency-short-version-if-your-mind-freezes)
29. [Things to avoid saying](#29-things-to-avoid-saying)

---

## 1. Opening / Tell me about yourself

```text
Thank you for speaking with me.

I am a Performance and Capacity Engineer / Senior Data Engineer with 20+ years of enterprise technology experience, including a strong recent background at Citi.

My main strength is turning large-scale infrastructure telemetry into capacity insights, forecasting models, KPI reports, and executive-ready recommendations. At Citi, I built Python, Pandas, PySpark, and SQL workflows that processed telemetry from more than 6,000 infrastructure endpoints into validated reporting and forecasting datasets.

I worked with tools and platforms such as BMC TrueSight / TSCO, CA APM / Wily, AppDynamics, Oracle, SQL, Python, Pandas, PySpark, and AWS-oriented data workflows.

The value I bring is not only technical pipeline work. It is helping infrastructure, application, and leadership teams understand utilization, bottleneck risk, growth trends, timing of capacity needs, and where investment or remediation is needed.
```

[Back to TOC](#table-of-contents)

## 2. What attracted you to this role?

```text
This role is very close to the work I did at Citi.

The description mentions large-scale infrastructure optimization, automated forecasting models, capital planning, KPI-based decision frameworks, operational playbooks, and communication with leadership and product teams. That maps directly to my background.

I like roles where capacity engineering is treated as a business decision-support function, not just a monitoring activity. The goal is to help leadership make better decisions about performance risk, infrastructure investment, resource allocation, and service stability.
```

[Back to TOC](#table-of-contents)

## 3. What do you know about the client?

```text
I understand the client is Bank of America, so I would expect a large, regulated banking environment with complex infrastructure, high reliability expectations, strong controls, and a need for clear communication across application, infrastructure, operations, and leadership teams.

That type of environment is familiar to me from Citi. In banking, capacity work has to be accurate, explainable, and tied to service risk and business impact.
```

[Back to TOC](#table-of-contents)

## 4. Describe your Citi capacity work

```text
At Citi, I supported capacity and performance analytics for large-scale banking infrastructure.

I worked with telemetry from more than 6,000 endpoints. My work involved ingesting data from monitoring and capacity platforms, validating the data, transforming it with Python, Pandas, PySpark, and SQL, then producing reporting and forecasting outputs for infrastructure and leadership teams.

The focus was to identify utilization patterns, bottleneck risks, growth trends, underused infrastructure, and areas where resource planning or remediation was needed.

I also created runbooks, metric definitions, validation checkpoints, and operational documentation so the process was repeatable and easier for teams to trust.
```

[Back to TOC](#table-of-contents)

## 5. What tools did you use?

```text
For capacity and performance work, I used BMC TrueSight / TSCO, CA APM / Wily, AppDynamics, Oracle, SQL, Python, Pandas, PySpark, and reporting/dashboard workflows.

I also worked with AWS-oriented data patterns including S3, Glue, Athena, and Redshift in support of cloud data workflows and forecasting workloads.

For scripting and automation, I used Python, Perl, KornShell, SQL, and Unix/Linux scripting depending on the environment.
```

[Back to TOC](#table-of-contents)

## 6. How did you forecast capacity?

```text
My process starts with data quality.

Before forecasting, I validate the telemetry: row counts, missing data, freshness, abnormal spikes, duplicates, and whether the metric is actually meaningful for the service.

Then I build historical datasets by server, application, metric, or service group. I look at utilization trends, seasonality, growth patterns, abnormal deltas, and known business events.

For forecasting, I have used Python workflows with Prophet and scikit-learn-style models. But I always explain forecasting as decision support, not a magic answer. The forecast helps identify risk windows, possible saturation points, and when teams may need to scale, tune, consolidate, or investigate.
```

[Back to TOC](#table-of-contents)

## 7. How do you explain capacity risk to leadership?

```text
I avoid overwhelming leadership with raw technical metrics.

I translate the data into four things:

What is constrained?
When could it become a problem?
What service or business function could be affected?
What decision or action is needed?

For example, instead of saying CPU is trending upward, I would explain whether the trend creates a capacity risk within the planning window, whether it affects a critical application, and whether the right action is add capacity, tune the application, rebalance workload, or continue monitoring.
```

[Back to TOC](#table-of-contents)

## 8. How do you support capital planning or budgeting?

```text
Capacity data supports capital planning by showing where infrastructure investment is justified and where it is not.

At Citi, I analyzed utilization patterns, growth trends, underused infrastructure, seasonal peaks, and bottleneck risks. That helps leadership avoid both under-provisioning and over-provisioning.

The goal is to support decisions like:
Do we need more capacity?
Can we reclaim or consolidate unused capacity?
Is the issue hardware, application behavior, query performance, or workload distribution?
When should investment happen to avoid service risk?
```

[Back to TOC](#table-of-contents)

## 9. How do you handle bad or missing telemetry?

```text
I treat telemetry quality as part of capacity engineering.

If data is missing or suspicious, I do not blindly forecast from it. I check freshness, source feeds, row counts, nulls, duplicates, metric definitions, collection gaps, and changes in upstream systems.

I also compare current outputs to prior trusted runs. If there is a sudden abnormal change, I investigate whether it is a real infrastructure event or a data issue.

Bad telemetry can lead to bad investment decisions, so validation is critical.
```

[Back to TOC](#table-of-contents)

## 10. How do you troubleshoot a performance bottleneck?

```text
I start by separating symptom from cause.

First, I identify the symptom: latency, throughput drop, CPU saturation, memory pressure, thread contention, database waits, garbage collection, network, or storage.

Then I correlate multiple signals:
Infrastructure metrics
APM transaction behavior
Application timing
Database or SQL behavior
Recent changes
Workload volume
Historical baseline

At AT&T, for example, I analyzed J2EE applications under load and looked at JDBC bottlenecks, threads, heap memory, CPU, and garbage collection. At Citi, I used telemetry and reporting patterns to identify capacity and reliability risks.
```

[Back to TOC](#table-of-contents)

## 11. What is the difference between performance engineering and capacity engineering?

```text
Performance engineering focuses on how a system behaves under workload: response time, throughput, bottlenecks, and efficiency.

Capacity engineering focuses on whether the environment has enough resources now and in the future: CPU, memory, storage, infrastructure growth, utilization trends, and forecasted demand.

They overlap. Performance issues can create capacity symptoms, and capacity limits can create performance issues. A good capacity engineer needs to understand both.
```

[Back to TOC](#table-of-contents)

## 12. How do you build KPI dashboards?

```text
I start by defining the audience and decision.

For engineering teams, the dashboard may show detailed metrics like utilization, saturation, latency, errors, or feed health.

For leadership, the dashboard should show risk, trend, confidence, and action. For example:
Capacity risk by service
Growth trend
Forecasted saturation date
Criticality
Recommended action
Data confidence

I also define the metric clearly so people understand what it means and what it does not mean.
```

[Back to TOC](#table-of-contents)

## 13. Tell me about operational playbooks

```text
A playbook makes repeated work consistent.

For capacity and performance work, a playbook may include:
What metrics to check
Where the data comes from
How to validate freshness
What thresholds matter
How to investigate anomalies
Who to contact
How to document RCA
How to communicate status

At Citi and in previous APM roles, I created runbooks, metric definitions, dashboard notes, validation checkpoints, and troubleshooting documentation to improve repeatability and knowledge sharing.
```

[Back to TOC](#table-of-contents)

## 14. How do you work with application teams?

```text
I try to make capacity data useful to application teams, not just report numbers.

I ask what service they own, what the expected workload is, what changed recently, and what business events may affect demand.

Then I translate telemetry into practical findings:
Is there a real bottleneck?
Is the issue capacity, code, SQL, configuration, or workload distribution?
Is this urgent or a planning item?
What should be monitored next?

The best result is when application teams trust the data and use it for planning.
```

[Back to TOC](#table-of-contents)

## 15. How do you work with executives?

```text
Executives need clarity, not metric overload.

I summarize the situation in business terms:
Current state
Risk
Timing
Impact
Options
Recommendation

I also explain confidence level. If the data is clean and the trend is stable, confidence is higher. If there are gaps or recent changes, I say that clearly.
```

[Back to TOC](#table-of-contents)

## 16. What kind of infrastructure scale have you handled?

```text
At Citi, I worked with telemetry from more than 6,000 infrastructure endpoints.

At CA Technologies / TIAA-CREF, I supported a large CA APM environment with 50+ Enterprise Managers and 4,000 to 6,000 instrumented agents.

So I am comfortable with enterprise-scale telemetry, monitoring, performance data, and the challenge of making that data useful for operations and leadership.
```

[Back to TOC](#table-of-contents)

## 17. Do you have banking experience?

```text
Yes. My strongest recent experience is in banking and financial-services environments.

At Citi, I supported capacity, performance, telemetry, reporting, forecasting, and operational insight workflows for banking infrastructure.

Earlier, at CA Technologies / TIAA-CREF, I supported enterprise APM and performance monitoring in a financial-services environment.

I understand that banking environments require reliability, documentation, controls, communication, and careful handling of operational risk.
```

[Back to TOC](#table-of-contents)

## 18. Are you comfortable with onsite Plano?

```text
Yes. I am local to the Plano area, and I am comfortable with the onsite requirement.
```

[Back to TOC](#table-of-contents)

## 19. Why are you leaving / available?

```text
I am looking for the right next role where I can apply my performance, capacity, forecasting, and infrastructure analytics background.

This LTIMindtree / Bank of America opportunity is interesting because it is close to my strongest Citi experience: large-scale infrastructure, capacity forecasting, KPI reporting, operational playbooks, and executive decision support.
```

[Back to TOC](#table-of-contents)

## 20. What is your strongest value for this role?

```text
My strongest value is the combination of capacity engineering, data engineering, and performance analysis.

I can work with raw infrastructure telemetry, validate it, transform it, forecast from it, and explain it to both technical teams and leadership.

Many people can create dashboards. My strength is making sure the data is trustworthy and tied to real capacity decisions.
```

[Back to TOC](#table-of-contents)

## 21. What is your weakness or ramp-up area?

```text
I am strongest in Citi-scale performance and capacity engineering, telemetry pipelines, forecasting, and reporting.

Depending on the exact Bank of America environment, I may need to ramp up on their specific internal tools, naming conventions, reporting standards, and governance processes.

But the core capacity engineering pattern is familiar to me: understand the telemetry, validate the data, identify trends and bottlenecks, communicate risk, and support decisions.
```

[Back to TOC](#table-of-contents)

## 22. Do you have cloud experience?

```text
Yes. My strongest cloud-related work is AWS-oriented data and capacity workflows.

At Citi, I worked with AWS S3, Glue, Athena, Redshift, EC2/ECS concepts, and cloud-oriented reporting patterns. I used these to support scalable data processing, forecasting, and analytics workflows.

I would describe myself as strongest in AWS data/platform workflows and hybrid infrastructure analytics, not as a pure cloud infrastructure architect.
```

[Back to TOC](#table-of-contents)

## 23. How do you handle conflicting stakeholder priorities?

```text
I bring the conversation back to risk, impact, and evidence.

If two teams want different actions, I compare:
Business criticality
Current utilization
Forecasted risk window
Customer or service impact
Cost
Confidence in the data
Operational effort

Then I present options clearly. Capacity engineering is often about helping leaders make tradeoffs.
```

[Back to TOC](#table-of-contents)

## 24. Describe a time you improved a process

```text
At Citi, a lot of capacity and telemetry reporting depended on raw monitoring feeds and manual interpretation.

I helped improve the process by building Python/Pandas/PySpark and SQL workflows that turned telemetry into validated reporting and forecasting datasets. I added checks for freshness, missing data, abnormal movement, and consistency with prior runs.

That improved trust in the reports and made the process more repeatable for operational and leadership use.
```

[Back to TOC](#table-of-contents)

## 25. How do you handle RCA?

```text
For RCA, I start with the timeline.

What changed?
When did the symptom start?
Which metrics moved?
Which service or infrastructure layer was affected?
Was the issue real capacity pressure, application behavior, database behavior, missing telemetry, or reporting error?

Then I document:
Root cause
Impact
Detection method
Resolution
Prevention
Follow-up monitoring

I try to make the RCA useful, not just formal.
```

[Back to TOC](#table-of-contents)

## 26. What questions do you have for us?

Use two or three only:

```text
What capacity tools and telemetry platforms does the Bank of America team use today?
```

```text
Is the role more focused on forecasting and executive reporting, or more hands-on performance troubleshooting?
```

```text
What are the biggest capacity challenges right now: growth forecasting, cost optimization, risk reporting, or application bottlenecks?
```

```text
How does the team currently connect capacity insights to budgeting or capital planning?
```

```text
What would success look like in the first 90 days?
```

[Back to TOC](#table-of-contents)

## 27. Strong closing

```text
This role sounds very close to my strongest Citi experience.

I bring large-scale banking infrastructure experience, capacity forecasting, telemetry pipelines, KPI reporting, performance analysis, and executive communication.

I am local to Plano, comfortable with the onsite requirement, and I believe I can contribute quickly because the core problem is familiar: turn complex infrastructure telemetry into reliable capacity decisions.
```

[Back to TOC](#table-of-contents)

## 28. Emergency short version if your mind freezes

```text
At Citi, I worked on capacity and performance analytics for large-scale banking infrastructure. I processed telemetry from more than 6,000 endpoints using Python, Pandas, PySpark, SQL, and tools like BMC TrueSight/TSCO, CA APM, and AppDynamics. My work helped teams understand utilization, bottleneck risk, forecasting, resource planning, and executive reporting. That is why this LTIMindtree / Bank of America role feels very aligned with my background.
```

[Back to TOC](#table-of-contents)

## 29. Things to avoid saying

```text
Avoid: I am mainly a data engineer.
Say: I am a performance and capacity engineer with strong data engineering skills.
```

```text
Avoid: I just built reports.
Say: I built validated telemetry and forecasting workflows used for capacity decisions.
```

```text
Avoid: I only used tools.
Say: I used tools plus Python/SQL pipelines to convert telemetry into decision-ready insights.
```

```text
Avoid: ML solves capacity.
Say: Forecasting supports capacity decisions, but data validation and business context are critical.
```

Your resume for this role is already strongly aligned around capacity planning, forecasting, telemetry/APM, Python/PySpark/SQL, executive reporting, and operational playbooks.

[Back to TOC](#table-of-contents)
