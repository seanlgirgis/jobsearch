# Capital One — Lead Data Engineer
**Recruiter:** Sam Ali (Principal Recruiter, Card Tech)
**Call:** Wednesday April 16, 2026 — 10:00 AM
**Phone:** Sam will call you directly
**Format:** 15–30 min recruiter screen

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

---

## Your Opening 2 Minutes

> "I'm in Plano — which is great for your Plano location. I'm actively looking,
> hands-on engineering is what I do, and the Lead Data Engineer role is the
> sweet spot for me. I've been doing Python pipelines, cloud data platforms,
> and ML forecasting at scale for most of my career — most recently 8 years
> at Citi in a Senior Capacity and Data Engineer role."

---

## Which Role To Target

**Lead Data Engineer** — not Lead SWE, not Senior Lead SWE.

- Lead DE maps directly to your background: Python, pipelines, Redshift, Glue, ML forecasting
- Lead SWE = Java/Scala microservices, more application-layer — not your strongest hand
- Senior Lead SWE = Senior Manager equivalent, heavy leadership loop — too early in this conversation

---

## Your 4 Key Stories (STAR Format)

### Story 1 — ETL Automation at Scale
**Situation:** Citi had a manual capacity planning process across 6,000+ endpoints.
**Task:** Replace it with something automated and reliable.
**Action:** Built automated ETL pipelines in Python/Pandas, pulling P95 telemetry from BMC TrueSight/TSCO, ingesting into Oracle schemas optimized for historical retention.
**Result:** Replaced legacy manual processes entirely. Unified disparate feeds into a single reporting platform with executive dashboards.

> *Use when asked: "Tell me about a complex pipeline you built" / "Describe a time you automated a manual process"*

---

### Story 2 — ML Forecasting for Business Impact
**Situation:** Infrastructure provisioning was reactive — problems were caught too late.
**Task:** Build a system that predicts bottlenecks before they hit.
**Action:** Developed ML forecasting models using Prophet and scikit-learn to predict capacity needs 3–6 months ahead. Fed historical telemetry data through the pipeline into the models.
**Result:** Improved provisioning accuracy, gave the business time to act before bottlenecks materialized. Reduced emergency capacity requests.

> *Use when asked: "Tell me about a time you used data to drive a business decision" / "Have you worked with ML in production?"*

---

### Story 3 — Cost Savings From Data Mining
**Situation:** Large enterprise infrastructure estate with no visibility into underutilization.
**Task:** Identify waste and drive consolidation.
**Action:** Applied statistical analysis and data mining on utilization patterns across the estate. Built Python scripts to flag underutilized servers.
**Result:** Identified underutilized infrastructure, drove hardware consolidation, delivered measurable cost savings. [Add $ number if you remember one]

> *Use when asked: "Tell me about a time you delivered business value" / "Cost optimization experience?"*

---

### Story 4 — AWS Hybrid Data Platform
**Situation:** Oracle on-prem for reporting, but ML forecasting workloads needed cloud scale.
**Task:** Extend the data platform into AWS without disrupting existing Oracle reporting.
**Action:** Built a hybrid platform — S3 as landing zone for raw telemetry, AWS Glue for ETL transformation, Redshift for forecasting workloads. Containerized Python ETL jobs on EC2/ECS for on-demand scaling.
**Result:** Existing Oracle reporting stayed intact. Heavy ML forecasting moved to Redshift — parallel runs at cloud scale, better performance, scalable on demand.

> *Use when asked: "Tell me about your AWS experience" / "Have you worked with cloud data warehousing?"*

---

## Likely Questions Sam Will Ask + Your Answers

### "Tell me about yourself"
> Use your opening 2 minutes above. Keep it under 90 seconds.
> End with: "I'm actively looking and the Lead DE role at Capital One is a strong fit."

### "Why Capital One?"
> "Capital One operates at a scale that's genuinely interesting from a data
> engineering perspective — millions of customers, real-time transactions,
> compliance requirements. That combination of scale, cloud-first culture,
> and hands-on technical work at the Lead level is exactly what I'm looking for."

### "What are you looking for in your next role?"
> "Hands-on technical work — I don't want to move into pure management.
> I want to be designing and building data systems, working with a strong team,
> and solving hard problems at scale. The Lead DE title at Capital One fits that."

### "What's your experience with streaming / Kafka?"
> "My background is stronger on the batch and warehouse side — Redshift,
> Snowflake, Spark for large-scale processing. I've worked adjacent to
> streaming architectures and I'm actively building in that space.
> It's an area I'm ramping on." *(Honest, not damaging)*

### "Are you interviewing elsewhere?"
> "I have a few conversations in progress. Capital One is at the top of my
> list given the role fit and the Plano location."

### "What's your salary expectation?"
> "Based on the role and my experience, I'm targeting around $185,000 base.
> I'm flexible depending on the full comp package including bonus and equity."

### "When can you start?"
> "I can be flexible — ideally I'd like 2–3 weeks to wrap up properly,
> but I can discuss if there's urgency on your end."

### "Tell me about a challenging project"
> Use Story 1 (ETL automation) or Story 4 (AWS platform). Both show scale and complexity.

### "How do you handle ambiguity?"
> "At Citi, capacity planning had no clear owner when I joined — just a manual
> process and a lot of tribal knowledge. I mapped out what data we had,
> what decisions depended on it, and built the system around that.
> I find that when there's ambiguity, the data usually tells you what to do next."

---

## Things To Refresh Before Wednesday

### AWS — quick review (30 min)
- [ ] S3 concepts: buckets, prefixes, partitioning for performance
- [ ] Glue: crawlers, ETL jobs, data catalog
- [ ] Redshift: distribution styles, sort keys, WLM (workload management)
- [ ] ECS vs EC2: when to use containers vs raw instances

### Kafka Basics — just enough to not be cold (1 hour)
- [ ] What it is: distributed log, topics, partitions, consumer groups
- [ ] Producer → topic → consumer mental model
- [ ] Why it's used: decoupling, real-time event streaming, at-least-once delivery
- [ ] How it differs from batch: push vs pull, latency vs throughput
- Key phrase to use: *"event-driven architecture"*

### Python / Data Engineering
- [ ] Review your ETL code patterns — be ready to describe a pipeline end-to-end
- [ ] Know: pandas, scikit-learn, Prophet (you've used all of these)

### Capital One Culture
- [ ] They emphasize: hands-on, full-stack thinking, Agile, cloud-native
- [ ] Key phrase they use: *"full system design and architecture knowledge"*
- [ ] They value engineers who stay technical at senior levels — lean into that

---

## Questions To Ask Sam

1. "What does the team structure look like for the Lead DE role in Plano?"
2. "Is this a backfill or a new headcount?"
3. "What's the biggest data engineering challenge the team is working through right now?"
4. "What does the interview process look like after this call?"
5. "Is the Plano role hybrid or on-site?"

---

## Logistics Checklist

- [ ] Confirm calendar invite received
- [ ] Phone charged and ready 10 min before
- [ ] Quiet room — Sam calls you directly
- [ ] Have this doc open on second screen
- [ ] Know your numbers: 20+ years exp, 8 years at Citi, 6,000+ endpoints, $185k target

---

## After The Call

If it goes well Sam will schedule you for a technical screen. Typical Capital One loop:
1. Recruiter screen (this call)
2. Technical phone screen (Python, SQL, system design)
3. Virtual onsite (3–4 rounds: coding + system design + behavioral)

After the call — update `data/jobs/` metadata for Capital One with status `INTERVIEW` and add a history entry.
