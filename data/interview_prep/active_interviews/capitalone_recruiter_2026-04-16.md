# Capital One — Lead Data Engineer
**Recruiter:** Sam Ali (Principal Recruiter, Card Tech)
**Call:** Wednesday April 16, 2026 — 10:00 AM
**Phone:** Sam will call you directly
**Format:** 15–30 min recruiter screen

---

## Table of Contents

- [The Role](#the-role)
- [Your Opening 2 Minutes](#your-opening-2-minutes)
- [Which Role To Target](#which-role-to-target)
- [Your 4 Key Stories](#your-4-key-stories-star-format)
  - [Story 1 — ETL Automation at Scale](#story-1--etl-automation-at-scale)
  - [Story 2 — ML Forecasting for Business Impact](#story-2--ml-forecasting-for-business-impact)
  - [Story 3 — Cost Savings From Data Mining](#story-3--cost-savings-from-data-mining)
  - [Story 4 — AWS Hybrid Data Platform](#story-4--aws-hybrid-data-platform)
- [Likely Questions Sam Will Ask](#likely-questions-sam-will-ask)
  - [Tell me about yourself](#tell-me-about-yourself)
  - [Why Capital One?](#why-capital-one)
  - [What are you looking for?](#what-are-you-looking-for-in-your-next-role)
  - [Streaming / Kafka experience?](#whats-your-experience-with-streaming--kafka)
  - [Are you interviewing elsewhere?](#are-you-interviewing-elsewhere)
  - [Salary expectation?](#whats-your-salary-expectation)
  - [When can you start?](#when-can-you-start)
  - [Tell me about a challenging project](#tell-me-about-a-challenging-project)
  - [How do you handle ambiguity?](#how-do-you-handle-ambiguity)
- [Things To Refresh Before The Call](#things-to-refresh-before-the-call)
  - [AWS Quick Review](#aws--quick-review)
  - [Kafka Basics](#kafka-basics)
  - [Python / Data Engineering](#python--data-engineering)
  - [Capital One Culture](#capital-one-culture)
- [Questions To Ask Sam](#questions-to-ask-sam)
- [Logistics Checklist](#logistics-checklist)
- [After The Call](#after-the-call)

---

## The Role

**Title:** Lead Data Engineer (Individual Contributor)
**Locations:** McLean VA / Richmond VA / Plano TX / Chicago IL
**Salary posted:** $197,300–$225,100 (McLean). Plano runs ~10–15% lower → ~$168k–$195k range.

**Your target number: $185,000 base**
> "Based on the role and my experience, I'm targeting around $185,000 base.
> I'm flexible depending on the full comp package including bonus and equity."

- Don't lead with salary — let her ask
- Don't give a range — they anchor to the bottom
- Don't say "whatever is fair"

[↑ Back to section](#the-role)

---

## Your Opening 2 Minutes

> "I'm in Plano — which is great for your Plano location. I'm actively looking,
> hands-on engineering is what I do, and the Lead Data Engineer role is the
> sweet spot for me. I've been doing Python pipelines, cloud data platforms,
> and ML forecasting at scale for most of my career — most recently 8 years
> at Citi in a Senior Capacity and Data Engineer role."

[↑ Back to section](#your-opening-2-minutes)

---

## Which Role To Target

**Lead Data Engineer** — not Lead SWE, not Senior Lead SWE.

- Lead DE maps directly to your background: Python, pipelines, Redshift, Glue, ML forecasting
- Lead SWE = Java/Scala microservices, more application-layer — not your strongest hand
- Senior Lead SWE = Senior Manager equivalent, heavy leadership loop — too early in this conversation

[↑ Back to section](#which-role-to-target)

---

## Your 4 Key Stories (STAR Format)

### Story 1 — ETL Automation at Scale
**Situation:** Citi had a manual capacity planning process across 6,000+ endpoints — Excel sheets, 10-day cycle, error-prone.
**Task:** Replace it with something automated and reliable.
**Action:** Built automated ETL pipelines in Python/Pandas, pulling P95 telemetry from BMC TrueSight/TSCO and other systems, ingesting into Oracle schemas optimized for historical retention.
**Result:** Replaced legacy manual processes entirely. Reports delivered in 2 days instead of 10. Unified disparate feeds into a single reporting platform with executive dashboards.

> *Use when asked: "Tell me about a complex pipeline you built" / "Describe a time you automated a manual process"*

[↑ Back to section](#your-4-key-stories-star-format)

---

### Story 2 — ML Forecasting for Business Impact
**Situation:** Infrastructure provisioning was reactive — problems were caught too late.
**Task:** Build a system that predicts bottlenecks before they hit.
**Action:** Developed ML forecasting models using Prophet and scikit-learn to predict capacity needs 3–6 months ahead. Fed historical time-series telemetry through the pipeline into the models. Accounted for seasonality and holidays. Back-tested multiple model types per server class.
**Result:** Improved provisioning accuracy significantly. Gave the business ample time to act before bottlenecks materialized. Reduced emergency capacity requests.

> *Use when asked: "Tell me about a time you used data to drive a business decision" / "Have you worked with ML in production?"*

[↑ Back to section](#your-4-key-stories-star-format)

---

### Story 3 — Cost Savings From Data Mining
**Situation:** Large enterprise infrastructure estate with no visibility into underutilization.
**Task:** Identify waste and drive consolidation.
**Action:** Applied statistical analysis and data mining on utilization patterns across the estate. Built Python scripts to flag underutilized servers alongside over-utilized ones in the same tier.
**Result:** Identified that bottlenecks were scheduling/allocation gaps, not capacity gaps. Drove hardware consolidation, delivered measurable cost savings. Avoided net-new hardware procurement.

> *Use when asked: "Tell me about a time you delivered business value" / "Cost optimization experience?"*

[↑ Back to section](#your-4-key-stories-star-format)

---

### Story 4 — AWS Hybrid Data Platform
**Situation:** Oracle on-prem for reporting, but ML forecasting workloads needed cloud scale.
**Task:** Extend the data platform into AWS without disrupting existing Oracle reporting.
**Action:** Built a hybrid platform — S3 as landing zone for raw telemetry, AWS Glue for ETL transformation, Redshift for forecasting workloads. Containerized Python ETL jobs on EC2/ECS for on-demand scaling.
**Result:** Existing Oracle reporting stayed intact. Heavy ML forecasting moved to Redshift — parallel runs at cloud scale, better performance, scalable on demand.

> *Use when asked: "Tell me about your AWS experience" / "Have you worked with cloud data warehousing?"*

[↑ Back to section](#your-4-key-stories-star-format)

---

## Likely Questions Sam Will Ask

---

### "Tell me about yourself"

> "Sure. I'm a Senior Data Engineer with over 20 years of enterprise experience,
> and most recently I spent 8 years at Citi as a Senior Capacity and Data Engineer —
> that was my longest and deepest role.
>
> At Citi I built and owned the data infrastructure for capacity planning across
> 6,000+ endpoints across 4 global regions. That meant automated ETL pipelines
> in Python pulling telemetry from BMC TrueSight, AppDynamics, and other enterprise
> monitoring systems — replacing what used to be a 10-day manual Excel process.
> We got reports out in 2 days with zero errors.
>
> I also built ML forecasting models using Prophet and scikit-learn to predict
> capacity 3 to 6 months ahead, accounting for seasonality and holidays. And I
> built a hybrid AWS platform — S3, Glue, Redshift, ECS — to scale the heavy
> forecasting workloads in the cloud while keeping existing reporting on-prem.
>
> My core is Python, SQL, cloud data platforms on AWS, and building pipelines
> that serve real business decisions — not just move data around.
>
> I'm based in Plano, actively looking, and the Lead Data Engineer role
> at Capital One is a strong fit."

*(Target: 90 seconds. Practice it out loud before the call.)*

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "Why Capital One?"

> "Capital One operates at a scale that's genuinely interesting from a data
> engineering perspective — millions of customers, real-time transactions,
> compliance requirements. That combination of scale, cloud-first culture,
> and hands-on technical work at the Lead level is exactly what I'm looking for."

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "What are you looking for in your next role?"

> "Hands-on technical work — I don't want to move into pure management.
> I want to be designing and building data systems, working with a strong team,
> and solving hard problems at scale. The Lead DE title at Capital One fits that."

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "What's your experience with streaming / Kafka?"

> "My background is stronger on the batch and warehouse side — Redshift,
> Spark for large-scale processing, Python ETL pipelines at enterprise scale.
> I've been actively studying Kafka concepts — topics, partitions, consumer groups,
> delivery semantics. I understand the architecture and can ramp quickly
> in a production context." *(Honest, not damaging)*

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "Are you interviewing elsewhere?"

> "I have a few conversations in progress — including with Toyota Financial Services
> and Samsung. Capital One is at the top of my list given the role fit,
> the Plano location, and the engineering culture."

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "What's your salary expectation?"

> "Based on the role and my experience, I'm targeting around $185,000 base.
> I'm flexible depending on the full comp package including bonus and equity."

**Say $185,000 once. Pause. Do not give a range.**

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "When can you start?"

> "I am available to start immediately and can align with your preferred onboarding timeline."

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "Tell me about a challenging project"

Use **Story 1** (ETL automation) or **Story 4** (AWS platform). Both show scale and complexity.

> Story 1 punch line: *"Replaced a 10-day manual Excel process with a fully automated
> pipeline — reports in 2 days, zero errors, consumed by multiple teams."*

> Story 4 punch line: *"Built a hybrid Oracle-to-AWS platform — preserved legacy
> reporting while moving ML forecasting workloads to cloud scale on Redshift."*

[↑ Back to section](#likely-questions-sam-will-ask)

---

### "How do you handle ambiguity?"

> "At Citi, capacity planning had no clear owner when I joined — just a manual
> process and a lot of tribal knowledge. I mapped out what data we had,
> what decisions depended on it, and built the system around that.
> I find that when there's ambiguity, the data usually tells you what to do next."

[↑ Back to section](#likely-questions-sam-will-ask)

---

## Things To Refresh Before The Call

### AWS — Quick Review
- [ ] S3 concepts: buckets, prefixes, partitioning for performance
- [ ] Glue: crawlers, ETL jobs, data catalog
- [ ] Redshift: distribution styles, sort keys, WLM (workload management)
- [ ] ECS vs EC2: when to use containers vs raw instances

[↑ Back to section](#things-to-refresh-before-the-call)

---

### Kafka Basics
- [ ] What it is: distributed log, topics, partitions, consumer groups
- [ ] Producer → topic → consumer mental model
- [ ] Why it's used: decoupling, real-time event streaming, at-least-once delivery
- [ ] How it differs from batch: push vs pull, latency vs throughput
- Key phrase: *"event-driven architecture"*

[↑ Back to section](#things-to-refresh-before-the-call)

---

### Python / Data Engineering
- [ ] Review your ETL code patterns — be ready to describe a pipeline end-to-end
- [ ] Know cold: pandas, scikit-learn, Prophet, PySpark

[↑ Back to section](#things-to-refresh-before-the-call)

---

### Capital One Culture
- [ ] They emphasize: hands-on, full-stack thinking, Agile, cloud-native
- [ ] Key phrase they use: *"full system design and architecture knowledge"*
- [ ] They value engineers who stay technical at senior levels — lean into that

[↑ Back to section](#things-to-refresh-before-the-call)

---

## Questions To Ask Sam

1. "What does the team structure look like for the Lead DE role in Plano?"
2. "Is this a backfill or a new headcount?"
3. "What's the biggest data engineering challenge the team is working through right now?"
4. "What does the interview process look like after this call?"
5. "Is the Plano role hybrid or on-site?"

[↑ Back to section](#questions-to-ask-sam)

---

## Logistics Checklist

- [ ] Confirm calendar invite received
- [ ] Phone charged and ready 10 min before
- [ ] Quiet room — Sam calls you directly
- [ ] Have this doc open on second screen
- [ ] Key numbers: 20+ years, 8 years Citi, 6,000+ endpoints, 4 global regions, $185K target
- [ ] Salary: $185,000 — single number, no range

[↑ Back to section](#logistics-checklist)

---

## After The Call

If it goes well Sam will schedule you for a technical screen. Typical Capital One loop:
1. Recruiter screen (this call)
2. Technical phone screen (Python, SQL, system design)
3. Virtual onsite (3–4 rounds: coding + system design + behavioral)

After the call — update `data/jobs/` metadata for Capital One with status `INTERVIEW` and add a history entry.

[↑ Back to section](#after-the-call)
