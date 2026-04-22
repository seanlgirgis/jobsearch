# Samsung Austin Semiconductor — Capacity Planning Engineer
**Hiring Manager:** David Rojas
**Recruiter:** Robyn Wentworth (r.wentworth@samsung.com · 512.516.0181)
**Call:** Wednesday April 22, 2026 — 9:00 AM CT (David calls you)
**Phone:** 214-315-2190
**Format:** Hiring Manager phone interview — technical + behavioral, no live coding
**Location:** Taylor, TX (on-site) | **Score:** 90% | **Job Folder:** `data/applied_jobs/00060_7c453502/`

---

## Table of Contents

- [The Pivot Strategy](#the-pivot-strategy)
  - [Move 1 — Reframe Before They Do](#move-1--reframe-before-they-do)
  - [Move 2 — Speak Fab Language From Word One](#move-2--speak-fab-language-from-word-one)
  - [Move 3 — The Direct Challenge Answer](#move-3--the-direct-challenge-answer)
  - [The Underlying Logic](#the-underlying-logic-to-internalize)
- [IT Capacity → FAB Capacity Reframe Table](#the-key-reframe-it-capacity--fab-capacity)
- [Your Opening 2 Minutes](#your-opening-2-minutes-samsung-version)
- [Salary](#salary)
- [Your 4 Key Stories](#your-4-key-stories-samsung-framing)
  - [Story 1 — BMC TrueSight Capacity Optimization](#story-1--bmc-truesight-capacity-optimization-your-anchor-story)
  - [Story 2 — HorizonScale ML Forecasting Engine](#story-2--horizonscale-ml-forecasting-engine-your-flagship)
  - [Story 3 — Bottleneck Investigation & Constraint Removal](#story-3--bottleneck-investigation--constraint-removal)
  - [Story 4 — Cross-Team Capacity Coordination](#story-4--cross-team-capacity-coordination)
- [Questions — Ordered By Likelihood](#questions--ordered-by-likelihood)
  - [Tell me about yourself](#tell-me-about-yourself)
  - [Walk me through your capacity planning experience](#walk-me-through-your-capacity-planning-experience)
  - [Do you have manufacturing / fab experience?](#do-you-have-manufacturing--fab-experience)
  - [How do you approach a bottleneck investigation?](#how-do-you-approach-a-bottleneck-investigation)
  - [What is Factory Physics and how do you apply it?](#what-is-factory-physics-and-how-do-you-apply-it)
  - [Walk me through a full capacity analysis](#walk-me-through-how-you-approach-a-capacity-analysis)
  - [How did you use BMC TrueSight / TSCO?](#how-did-you-use-bmc-truesight--tsco-for-capacity-optimization)
  - [Tell me about your ML forecasting experience](#tell-me-about-ml-approaches-for-capacity-forecasting)
  - [What is OEE?](#what-is-oee-and-how-do-you-use-it-for-capacity-planning)
  - [What is supply chain management in a fab context?](#what-is-supply-chain-management-in-a-fab-context)
  - [How do you perform line analysis?](#how-do-you-perform-line-analysis-and-identify-line-movement-constraints)
  - [How do you coordinate Production and Engineering?](#how-do-you-coordinate-between-production-and-fab-engineering-teams)
  - [How do you present capacity risk to leadership?](#how-do-you-present-capacity-risk-to-leadership)
  - [How do you quantify throughput improvement impact?](#how-do-you-quantify-the-impact-of-a-throughput-improvement)
  - [What is takt time?](#what-is-takt-time-and-how-does-it-connect-to-capacity-planning)
  - [How do lot starts connect to output planning?](#how-do-lot-starts-connect-to-output-planning)
  - [How does yield impact capacity planning?](#how-does-yield-impact-capacity-planning)
  - [Why Samsung / Why this role?](#why-samsung--why-this-role)
  - [Why are you leaving Citi?](#why-are-you-leaving--what-happened-at-citi)
  - [Are you interviewing elsewhere?](#are-you-interviewing-elsewhere)
  - [Salary expectation](#whats-your-salary-expectation)
  - [When can you start?](#when-can-you-start)
  - [U.S. Export Control / On-site comfort](#us-export-control--on-site-comfort)
- [Deep Technical Topics](#deep-technical-topics-if-david-goes-there)
  - [SEMI E10 Equipment States](#what-are-the-semi-e10-equipment-states)
  - [MES Systems](#what-is-mes-and-how-does-capacity-planning-interact-with-it)
  - [Little's Law](#littles-law--explain-it-and-give-an-example)
  - [How to calculate resource capacity](#how-do-you-calculate-resource-capacity-and-utilization)
  - [In-house vs cloud capacity](#whats-your-experience-with-in-house-vs-cloud-capacity-planning)
  - [Estimate bottleneck tool capacity](#how-would-you-estimate-the-capacity-of-a-bottleneck-tool)
  - [Throughput dropped 10% — root cause](#if-throughput-dropped-10-this-week-how-do-you-find-the-cause)
- [SQL Questions](#sql-questions)
  - [Top 5 bottleneck tools query](#top-5-bottleneck-tools-query)
  - [Consecutive days over threshold](#consecutive-days-over-threshold-gaps-and-islands)
  - [Query optimization approach](#query-optimization-approach)
  - [Window functions](#window-functions)
- [Python Questions](#python-questions)
  - [Processing large time-series telemetry](#processing-large-time-series-telemetry)
  - [Build a forecasting model in Python](#build-a-capacity-forecasting-model-in-python)
  - [Python data analysis stack](#python-data-analysis-stack)
- [Questions To Ask David](#questions-to-ask-david-rojas)
- [Logistics & Pre-Interview Refresh](#logistics--pre-interview-refresh)
- [Job Requirements Coverage Check](#job-requirements-coverage-check)

---

## The Pivot Strategy

This is a Hiring Manager interview. David Rojas owns the capacity planning function.
He will probe domain knowledge. Use all three moves throughout.

---

### Move 1 — Reframe Before They Do

Address the domain gap in your **opening 2 minutes** — don't wait for them to raise it:

> "My background is IT infrastructure capacity planning — not fab — but the
> methodology is the same discipline. Bottleneck identification, utilization
> analysis, Little's Law, forecasting demand against constrained resources —
> I've been doing that for 8 years at enterprise scale. The domain changes.
> The analytical framework doesn't."

You own the gap before they raise it. That reads as confidence, not defensiveness.

[↑ Back to section](#the-pivot-strategy)

---

### Move 2 — Speak Fab Language From Word One

Every time you describe your Citi work, use **fab vocabulary**.

| Don't say | Say instead |
|-----------|------------|
| "servers hitting CPU limits" | "endpoints hitting capacity thresholds — same as tools approaching utilization ceiling" |
| "6,000 endpoints" | "6,000 assets across the estate — comparable scale to a large tool set" |
| "pipeline queue depth" | "WIP buildup upstream of the constraint" |
| "P95 utilization" | "peak utilization — equivalent to tool utilization rate in a fab" |
| "procurement lead time" | "capacity acquisition lead time — same 6–18 month horizon problem" |
| "server tier bottleneck" | "constraint step in the process flow" |

If you translate your own work into their language, they do the mapping for you.

**Quick definitions to use in the interview:**
- **MES (Manufacturing Execution System):** The real-time system that tracks every lot, step, tool state, and cycle time on the fab floor; it is the core data source for capacity analysis.
- **Factory Physics:** The operating math of manufacturing flow (WIP, throughput, cycle time, bottlenecks), including Little's Law, used to predict where constraints will appear.
- **Little's Law:** `WIP = Throughput × Cycle Time`; if two are known, the third can be calculated to diagnose flow constraints.
- **Takt time:** The pace required to meet demand (available production time divided by required output); if process cycle time is slower than takt, a gap exists.
- **OEE (Overall Equipment Effectiveness):** `Availability × Performance × Quality`; converts theoretical tool capacity into realistic effective capacity.

[↑ Back to section](#the-pivot-strategy)

---

### Move 3 — The Direct Challenge Answer

**"Do you have manufacturing experience?"** or **"Why you over someone with fab experience?"**

> "I don't have direct fab experience — I'll be straight about that.
> What I have is deep mastery of the analytical methodology that sits under
> all capacity planning regardless of domain: utilization modeling, bottleneck
> forecasting, Factory Physics, supply chain lead time analysis.
>
> Those skills take years to build. Semiconductor domain knowledge — process
> steps, MES systems, fab-specific terminology — I can learn in months.
> I've done exactly that before: I entered financial services IT with no
> banking background and was running the capacity planning system for Citi
> within my first year.
>
> The question isn't whether I know wafer fabs today. It's whether I can
> apply rigorous capacity planning methodology in a new domain — and I have
> a strong track record of doing exactly that."

[↑ Back to section](#the-pivot-strategy)

---

### The Underlying Logic To Internalize

Manufacturing capacity planning is the **origin** of the discipline. Factory Physics, Little's Law, takt time, OEE — all invented for factories. IT borrowed them. You're going from the application back to the source. That's not a stretch — it's the natural direction.

If you believe that framing, it comes through. If you're apologizing for it, it doesn't.

[↑ Back to section](#the-pivot-strategy)

---

## The Key Reframe: IT Capacity → FAB Capacity

| Samsung FAB | Your CITI / HorizonScale |
|-------------|--------------------------|
| Wafer tools are bottlenecks | Servers/endpoints are bottlenecks |
| Tool utilization % | CPU/memory utilization P95 |
| Lot starts / WIP movement | Pipeline throughput / queue depth |
| Factory Physics (Little's Law) | Queuing theory in telemetry pipelines |
| Capacity gap analysis | Forecasting capacity shortfalls 6 months ahead |
| Long-range capacity planning | HorizonScale 6-month ML forecasting |
| Supply chain constraints | Resource availability / procurement forecasting |
| Engineering + Production coordination | Infrastructure vs application team coordination at Citi |
| OEE (Availability × Performance × Quality) | Effective capacity = theoretical × uptime × efficiency |
| SEMI E10 equipment states | Server uptime / downtime / maintenance window states |

**Lead with the methodology and outcomes. Let David see the transfer.**

[↑ Back to section](#the-key-reframe-it-capacity--fab-capacity)

---

## Your Opening 2 Minutes (Samsung Version)

> "I'm a Senior Capacity and Data Engineer with 20+ years of experience —
> and the core of my work for the last 8 years at Citi was exactly this role:
> capacity planning, bottleneck analysis, and forecasting at enterprise scale.
>
> My background is IT infrastructure capacity — not fab — but the methodology
> is identical. I managed capacity across 6,000+ infrastructure assets using
> BMC TrueSight Capacity Optimization, pulling peak utilization telemetry,
> identifying constraints, and forecasting demand 6 months ahead using ML models
> built with Prophet and scikit-learn.
>
> I replaced a 10-day manual Excel process with a fully automated pipeline —
> reports in 2 days, zero errors. I built HorizonScale, an AI-driven forecasting
> engine from scratch that predicted bottlenecks 6 months ahead at 90%+ accuracy
> and cut forecasting cycle time by 90%.
>
> The tools in a fab are the bottlenecks. The methodology is the same: analyze
> utilization, forecast constraints, quantify risk, drive action. The domain
> specifics I'm ready to learn fast — the analytical foundation is already there."

*(Target: 90 seconds. Hits: pivot owned, BMC TrueSight, HorizonScale, 10→2 days, 6-month forecast)*

[↑ Back to section](#your-opening-2-minutes-samsung-version)

---

## Salary

**Samsung posted range:** $70,480 – $179,090 (base + bonus, no RSU)
**Austin/Taylor market for senior capacity planning + ML depth:** $145K–$160K

> "I'm targeting a base in the range of $145,000 to $160,000.
> I understand Samsung structures comp as base plus bonus without RSUs,
> and I'm open to discussing the full package."

[↑ Back to section](#salary)

---

## Your 4 Key Stories (Samsung Framing)

### Story 1 — BMC TrueSight Capacity Optimization (Your Anchor Story)
**Situation:** Citi needed to manage capacity across 6,000+ infrastructure assets — servers, storage, network — feeding a live BMC TrueSight Helix environment.
**Task:** Build a scalable pipeline to collect, clean, and analyze peak utilization telemetry and surface capacity constraints before they impacted operations.
**Action:** Designed Python + Pandas pipelines ingesting TrueSight telemetry, integrated CMDB metadata, built Oracle warehouse schemas for historical trending, created dashboards for leadership capacity review.
**Result:** Automated what was previously a 10-day manual process. Capacity risk flagged weeks ahead of threshold breach. Reports consumed by both engineering teams and senior leadership.

> *Use when asked: "Tell me about your capacity planning experience" / "Have you worked with BMC TrueSight?"*

[↑ Back to section](#your-4-key-stories-samsung-framing)

---

### Story 2 — HorizonScale: ML Forecasting Engine (Your Flagship)
**Situation:** Manual forecasting was slow, reactive, and couldn't scale across thousands of assets. No predictive signal — teams were always behind the curve.
**Task:** Replace manual forecasting with an automated ML-driven system that predicted bottlenecks before they occurred.
**Action:** Built HorizonScale from scratch — PySpark telemetry pipeline at banking scale, Prophet for time-series trend + seasonality decomposition, scikit-learn classifiers flagging assets at risk. Generator-based parallel pipeline cut processing cycles 90%.
**Result:** 6-month ahead bottleneck prediction at 90%+ accuracy. Leadership saw capacity risk by resource class, region, and time horizon. Cycle time from data to insight: days to minutes.

> *Use when asked: "Tell me about ML in capacity planning" / "Your most impactful project" / "Forecasting experience"*

[↑ Back to section](#your-4-key-stories-samsung-framing)

---

### Story 3 — Bottleneck Investigation & Constraint Removal
**Situation:** Recurring bottlenecks in specific server tiers at Citi — root cause unclear. Growth? Inefficiency? Bad allocation?
**Task:** Determine whether bottlenecks were structural (capacity gap) or operational (utilization inefficiency) and drive targeted action.
**Action:** Built SQL analytical queries over P95 utilization history to segment assets by pattern — over-utilized, under-utilized, spiky vs. flat. Correlated with CMDB metadata. Found clusters of under-utilized assets alongside over-utilized ones in the same tier — a scheduling and allocation gap, not a capacity gap.
**Result:** Rebalancing recommendation quantified with data. Hardware procurement avoided. Engineering teams given actionable data instead of "buy more."

> *Use when asked: "Bottleneck analysis" / "How do you approach capacity gaps?" / "Constraint removal"*

[↑ Back to section](#your-4-key-stories-samsung-framing)

---

### Story 4 — Cross-Team Capacity Coordination
**Situation:** Capacity decisions at Citi required alignment between infrastructure engineering, application teams, finance, and procurement — all with different views of the same data.
**Task:** Create a shared capacity view all stakeholders trusted and could act from.
**Action:** Built unified reporting pulling from TSCO, CMDB, and project intake. Standardized definitions. Ran monthly capacity reviews presenting automated bottleneck reports with risk tiers and recommended actions.
**Result:** Forecasting became proactive. Procurement cycles aligned to 6-month horizon. Eliminated surprises in hardware planning.

> *Use when asked: "Cross-functional coordination" / "Stakeholder management" / "How do you drive action from data?"*

[↑ Back to section](#your-4-key-stories-samsung-framing)

---

## Questions — Ordered By Likelihood

---

### "Tell me about yourself"

> "I'm a Senior Capacity and Data Engineer with over 20 years of experience.
> Most recently I spent 8 years at Citi leading capacity planning and data
> infrastructure across 4 global regions — monitoring tens of thousands of
> servers and infrastructure assets worldwide.
>
> I built the data pipelines and ML forecasting systems that replaced a
> 10-day manual Excel process — we got reports out in 2 days with zero errors.
> I designed forecasting models using Prophet and scikit-learn that predicted
> capacity 6 months ahead, accounting for seasonality and growth trends.
> That system — HorizonScale — reduced forecasting cycle time by 90% and
> predicted bottlenecks at 90%+ accuracy.
>
> My background is IT infrastructure capacity planning, and I understand the
> Samsung role is in semiconductor manufacturing. The analytical methodology
> is identical — bottleneck analysis, utilization modeling, Factory Physics,
> supply chain lead time forecasting. The domain is different, the discipline
> is the same.
>
> I'm excited about this role because it applies that methodology in a domain
> where the stakes are higher — capacity decisions in a fab directly determine
> output, revenue, and capital investment."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "Walk me through your capacity planning experience"

> "At Citi I owned end-to-end capacity planning for the infrastructure estate —
> think of it as the fab capacity function, but for servers and storage instead
> of wafer tools.
>
> On the data side: I built automated ETL pipelines pulling peak utilization
> telemetry from BMC TrueSight Capacity Optimization across 6,000+ assets.
> Data cleaned, enriched with asset metadata, loaded into Oracle for historical trending.
>
> On the analysis side: I performed bottleneck investigations identifying which
> asset classes were approaching capacity thresholds and whether the cause was
> structural growth or utilization inefficiency. I built the same short-range
> and long-range views the Samsung role describes — weekly operational reporting
> and 6-month planning horizon forecasting.
>
> On the forecasting side: Prophet and scikit-learn ML models predicting
> capacity breaches 6 months ahead. I ran sensitivity analysis — what does the
> picture look like if growth accelerates 20%? That gave leadership decision
> options, not just a status report.
>
> On the coordination side: monthly capacity reviews with engineering, application,
> finance, and procurement teams — translating utilization data into procurement
> decisions with quantified cost and lead time for each option."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "Do you have manufacturing / fab experience?"

Use **Move 3** from the Pivot Strategy above — have it cold.

> "I don't have direct fab experience — I'll be straight about that.
> What I have is deep mastery of the analytical methodology that sits under
> all capacity planning regardless of domain: utilization modeling, bottleneck
> forecasting, Factory Physics, supply chain lead time analysis.
>
> Those skills take years to build. Semiconductor domain knowledge — process
> steps, MES systems, fab-specific terminology — I can learn in months.
> I've done exactly that before: I entered financial services IT with no
> banking background and was running the capacity planning system for Citi
> within my first year.
>
> The question isn't whether I know wafer fabs today. It's whether I can
> apply rigorous capacity planning methodology in a new domain — and I have
> a strong track record of doing exactly that."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How do you approach a bottleneck investigation?"

> "Systematic decomposition — I work from the top down.
>
> First: Is it a capacity issue or a utilization issue? If peak utilization
> is high AND growing, that's a structural capacity gap. If peak utilization
> is high but adjacent assets are under-utilized, that's a scheduling or
> allocation gap. These have completely different solutions — one requires
> procurement, the other requires rebalancing.
>
> Second: What's the timing signature? A sudden spike points to a discrete
> event — a tool going down, a process change, a demand surge. A gradual
> trend points to organic growth approaching the ceiling.
>
> Third: Is it the actual bottleneck or a downstream effect? In fab terms —
> is the WIP building up because that tool is slow, or because the tool
> feeding it is starving it? I correlate queue depth, move rate, and
> upstream WIP to separate cause from symptom.
>
> At Citi I built SQL queries that segmented assets by utilization pattern —
> over-utilized, under-utilized, spiky vs. flat — and correlated with metadata
> to find the root cause. The output wasn't just 'this is bottlenecked' —
> it was 'here's why, here's the quantified impact, here's the recommended action.'"

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "What is Factory Physics and how do you apply it?"

> "Factory Physics is the study of how manufacturing systems behave under load —
> specifically the relationships between WIP, throughput, and cycle time.
>
> The foundational relationship is Little's Law: L = λW.
> Average WIP = throughput rate × average cycle time. Know two, you know the third.
>
> In a fab: if 100 lots are in WIP and throughput is 20 lots/day, average
> cycle time is 5 days. If WIP doubles to 200 lots but throughput stays at 20/day,
> cycle time doubles to 10 days. That's the lever — you can't improve cycle time
> without either increasing throughput or reducing WIP.
>
> The other critical behavior: as tool utilization approaches 100%, cycle time
> increases exponentially — not linearly. A tool at 95% utilization has dramatically
> worse cycle time than one at 80%, even though the utilization gap looks small.
> That nonlinear behavior is what Factory Physics captures — and it's why capacity
> planning can't just chase utilization to 100%.
>
> I applied the same queuing theory in IT capacity — a server at 90% utilization
> behaves very differently from one at 70%. The math translates directly."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "Walk me through how you approach a capacity analysis"

> "I start by defining the resource and the constraint — what are we measuring
> and what threshold represents a problem? In IT: CPU/memory peak utilization.
> In a fab: tool utilization rate and WIP queue depth.
>
> Then I pull 12–24 months of historical utilization data and decompose the trend:
> linear growth, seasonal pattern, or event-driven spikes?
>
> From that I build a forecast — statistical for stable trends, ML-based
> (Prophet) for volatile or seasonal data. The forecast gives me the expected
> crossover point where demand exceeds available capacity.
>
> Then I calculate the gap: projected demand minus available capacity at each
> planning horizon — 3 months, 6 months, 12 months. Is the gap addressable
> through efficiency improvements or does it require net-new capacity?
>
> Finally I present risk-tiered options: do nothing (cost of miss), optimize
> utilization (investment + lead time), or procure (cost + lead time).
> Leadership decides with full information, not just a status update."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How did you use BMC TrueSight / TSCO for capacity optimization?"

> "BMC TrueSight Capacity Optimization — now the Helix platform — was my
> primary telemetry source at Citi. It collected performance metrics across
> the entire infrastructure estate: CPU, memory, disk I/O, network — at
> peak utilization granularity.
>
> I used the TSCO API and direct database feeds to extract time-series
> telemetry into Python pipelines. Enriched with CMDB metadata — application,
> team, criticality tier — and loaded into Oracle for historical trending.
>
> The Aperture Vista module provided built-in capacity forecasting views —
> I used those as a validation layer against my ML-generated forecasts
> to catch model drift and sanity-check predictions.
>
> The key value of TSCO was breadth and consistency — a single unified
> telemetry source across heterogeneous infrastructure. That's the same
> value a MES provides in a fab: one source of truth for equipment state,
> lot movement, and process data."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "Tell me about ML approaches for capacity forecasting"

> "I used a two-model architecture in HorizonScale.
>
> First: Prophet for time-series forecasting. It handles seasonality and
> trend decomposition natively — weekly patterns, monthly cycles, holiday
> effects. Generates a forecast with confidence intervals, so I can show
> the uncertainty band, not just the expected trajectory.
>
> Second: scikit-learn classifiers — Random Forest and Gradient Boosting —
> trained to classify assets as 'at risk' or 'safe' based on derived features:
> growth rate, utilization trend slope, variance, days-to-threshold. This gave
> a binary risk signal easier for operational teams to act on than a curve.
>
> The pipeline ran on PySpark at banking scale — thousands of assets processed
> in parallel, generator-based architecture. 90% cycle time reduction vs.
> the original sequential design.
>
> For a FAB environment: replace server telemetry with tool utilization data,
> replace CMDB with equipment master data. The pipeline architecture and
> model structure transfer directly."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "What is OEE and how do you use it for capacity planning?"

> "OEE — Overall Equipment Effectiveness — is the standard manufacturing KPI
> measuring actual equipment performance vs. theoretical maximum.
>
> **OEE = Availability × Performance × Quality**
>
> - **Availability:** Actual uptime ÷ planned production time — captures downtime
> - **Performance:** Actual throughput rate ÷ ideal rate — captures slow cycles
> - **Quality:** Good units ÷ total units — captures yield loss
>
> Example: 90% availability × 80% performance × 95% quality = **68.4% OEE**.
> World-class targets 85%+.
>
> For capacity planning, OEE is the bridge from theoretical to real capacity.
> A tool rated at 100 lots/week at 68% OEE delivers 68 lots/week effective.
> Plan against theoretical and you'll consistently miss output.
>
> I used identical logic in IT — effective capacity = theoretical × availability
> × performance efficiency. Raw CPU capacity is never real capacity.
> The math is the same, the terminology shifts."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "What is supply chain management in a fab context?"

> "Two dimensions in semiconductor manufacturing:
>
> **Equipment supply chain:** Leading-edge fab tools have 18–24 month lead times.
> A capacity gap identified today can't be filled for 2 years. Capacity planning
> must look 24+ months out and signal equipment needs well ahead of demand.
> Spare parts are critical too — a tool down waiting for a part for 3 weeks
> is a massive capacity loss. Stocking decisions for critical spares are a
> supply chain optimization problem.
>
> **Materials and consumables:** Wafers, gases, chemicals, photomasks.
> Demand forecasting feeds procurement cycles. A sudden lot start ramp requires
> more raw wafers — if procurement didn't anticipate it, the capacity plan
> is impossible to execute regardless of tool availability.
>
> The capacity planner sits at the intersection of both: forecast demand accurately,
> communicate constraints to production, give procurement enough lead time
> to support the plan. I did the same at Citi — 6-month forecasting horizon
> aligned directly to the hardware procurement cycle."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How do you perform line analysis and identify line movement constraints?"

> "Line analysis is about understanding how product flows across all process
> steps — not just one tool — and finding where it accumulates, slows, or starves.
>
> I start by mapping the process flow: all steps, tools per step, throughput rate
> at each tool. Then I overlay WIP data — where are queues building? WIP
> accumulates upstream of a bottleneck.
>
> Key metrics per step: queue depth, move rate, cycle time vs. standard, utilization.
>
> A healthy line has WIP distributed evenly. An unhealthy line has WIP
> piling at one or two steps — those are your constraints.
>
> Line balance is the goal: matching throughput at every step to the pace set
> by the bottleneck so WIP flows smoothly. Imbalance wastes capacity on fast
> tools while the bottleneck is overloaded.
>
> At Citi I did the same across server tiers — mapping utilization flow
> to find where processing was accumulating and which tier was the constraint."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How do you coordinate between Production and Fab Engineering teams?"

> "These teams have natural tension: Production wants output now — minimize
> downtime. Engineering wants stability — experiments, PMs, qualifications.
>
> The capacity planner's job is to quantify that tension with data, not
> referee it politically.
>
> I build a shared model that shows: if Engineering takes Tool X offline
> 8 hours this week, it costs Y lots of output. That forces an explicit
> decision — is the engineering run worth Y lots? Both sides use the same
> numbers. The conversation shifts from 'my team's priority' to
> 'what's the right tradeoff for the business.'
>
> At Citi: infrastructure engineering wanted maintenance windows,
> application teams wanted 100% availability. Same dynamic. A shared
> data model that quantified the tradeoff — maintenance now vs. risk of
> unplanned outage later — turned arguments into decisions."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How do you present capacity risk to leadership?"

> "Risk-tiered format with clear action items. Leadership doesn't need
> queuing theory — they need: what's at risk, by when, what does it cost,
> what's the recommended action.
>
> My standard structure:
> 1. **Current state:** OEE / utilization vs. threshold / WIP levels —
>    one view, traffic-light format
> 2. **Risk horizon:** Which resources breach capacity at 3 / 6 / 12 months —
>    ranked by severity (impact × probability)
> 3. **Options and cost:** For each at-risk item — do nothing (cost of miss),
>    efficiency improvement (investment + lead time), procure (cost + lead time)
> 4. **Decision deadline:** By when does leadership need to act to stay on track?
>    That's the forcing function.
>
> At Citi I automated this from HorizonScale — same format every month,
> which built trust in the numbers. Consistency in reporting is as important
> as accuracy."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How do you quantify the impact of a throughput improvement?"

> "Three dimensions: output, revenue, and cost avoidance.
>
> **Output:** If the bottleneck tool throughput increases 5% and it's the
> line constraint, total fab output increases 5%. Convert to wafer starts or die count.
>
> **Revenue:** Incremental output × average selling price. 1,000 more
> wafers/month at $5,000/wafer = $5M/month additional revenue.
>
> **Cost avoidance:** If the improvement delays a $20M tool procurement by
> 18 months, that's quantifiable capital deferral — NPV of deferred spend.
>
> At Citi: throughput improvements that reduced forecasted server procurement
> were quantified as $ of CapEx avoided over the planning horizon.
> That's how you get engineering work approved — translate utilization
> percentages into dollar impact."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "What is takt time and how does it connect to capacity planning?"

> "Takt time is the pace at which you must produce to meet customer demand.
> **Available production time ÷ customer demand rate.**
>
> Example: 168 hours/week available, customers need 200 lots/week →
> takt time = 0.84 hours/lot. The factory must complete one lot every 50 minutes.
>
> For capacity planning: takt time sets the floor for required throughput.
> If the bottleneck tool completes one lot every 70 minutes, you have a gap —
> add capacity, reduce demand, or accept a miss.
>
> Takt time also drives lot start planning: if cycle time is 45 days and you
> need 200 lots out in week 10, lot starts must begin in week 3."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How do lot starts connect to output planning?"

> "Lot starts are the input lever for controlling output:
> **Output = Lot Starts × Yield × (cycle time and WIP adjusted)**
>
> You can't pull product on demand — everything has a multi-week cycle time.
> The question is: given what we need to ship 6-8 weeks from now, what do
> we need to start today?
>
> Lot start planning requires: demand signal, yield estimate per product,
> cycle time by product, current WIP in the line, and bottleneck tool capacity.
>
> Same logic in IT: to hit a future capacity target you start procurement now
> because hardware lead times are 3-6 months. Forward-planning horizon and
> yield/attrition accounting are identical concepts."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "How does yield impact capacity planning?"

> "Yield is critical and often underweighted. If a step has 95% yield —
> 5% of lots fail or need rework — to produce 100 good lots you start 105.
> That overhead is built into the lot start plan and tool capacity model.
>
> Yield loss at the bottleneck is doubly expensive: you consumed bottleneck
> capacity on a lot that didn't contribute to output. 5% yield loss at the
> bottleneck = 5% effective capacity loss.
>
> For long-range modeling: build yield assumptions per product and step,
> with sensitivity analysis — what does the capacity picture look like if
> yield drops from 95% to 90%? That drives both the lot start buffer
> and the equipment investment decision."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "Why Samsung / Why this role?"

> "Samsung operates at a manufacturing scale that's genuinely rare —
> advanced semiconductor fabrication at the Taylor fab is one of the most
> technically demanding manufacturing environments in the world.
>
> Capacity planning in a fab isn't just data work — it directly determines
> what gets built, when, and at what cost. The analytical rigor required —
> Factory Physics, bottleneck modeling, supply chain forecasting — is exactly
> what I've been doing in infrastructure capacity, and I want to apply it
> in a domain where the stakes are higher and the problems are harder.
>
> The Taylor fab is a strategic U.S. investment for Samsung. Being part of
> building out the operational excellence layer of that facility is
> genuinely exciting — it's a generational project."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "Why are you leaving / what happened at Citi?"

> "I was at Citi for 8 years and delivered strong results. My role was
> eliminated as part of a broader organizational restructuring —
> not performance related. I've used the time to sharpen my skills and
> I'm actively looking for the right long-term fit.
> The Samsung role is at the top of my list."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "Are you interviewing elsewhere?"

> "Yes, I have a few conversations in progress — including with Toyota Financial
> Services and Capital One. Samsung is my top priority given the capacity planning
> focus, the analytical depth the role requires, and the scale of what's being
> built at the Taylor facility."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "What's your salary expectation?"

> "I'm targeting a base in the range of $145,000 to $160,000.
> I understand Samsung structures comp as base plus bonus without RSUs,
> and I'm open to discussing the full package."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "When can you start?"

> "I'm available to start immediately and can align with your preferred onboarding timeline."

[↑ Back to section](#questions--ordered-by-likelihood)

---

### "U.S. Export Control / On-site comfort"

**Export Control:**
> "Yes — I understand this role has U.S. Export Control compliance requirements and I can complete any required verification promptly."

**On-site:**
> "Yes, fully on-site in Taylor works for me and I can support whatever schedule the team needs."

[↑ Back to section](#questions--ordered-by-likelihood)

---

## Deep Technical Topics (If David Goes There)

---

### "What are the SEMI E10 equipment states?"

> "SEMI E10 is the industry standard classifying every minute of equipment time:
> - **Productive:** Processing wafer lots
> - **Standby:** Ready but no product in queue
> - **Engineering:** Experiments, qualifications, process development
> - **Scheduled Downtime:** Planned PMs, calibrations
> - **Unscheduled Downtime:** Unexpected failures, waiting for parts
> - **Off:** Not available
>
> These matter because they define what actually happened to your capacity budget.
> A tool with 15% engineering and 12% unscheduled downtime has far less productive
> window than the calendar suggests. Rising unscheduled downtime is an early warning
> signal of equipment reliability issues before you see the output miss."

[↑ Back to section](#deep-technical-topics-if-david-goes-there)

---

### "What is MES and how does capacity planning interact with it?"

> "MES — Manufacturing Execution System — runs the fab floor in real time.
> Tracks every lot at every step: location, tool used, step duration, holds, excursions.
>
> For capacity planning, MES is the primary data source: lot tracking (actual cycle
> time, move rates, WIP by step), equipment history (uptime/downtime, SEMI E10 states),
> and process data (tool, recipe, process time).
>
> Capacity planning queries MES to calculate actual OEE, actual vs. standard cycle
> time, and WIP movement rates — then feeds those into forecasting models.
>
> I haven't worked directly with fab MES, but the data extraction pattern is identical
> to what I built against BMC TrueSight — connect to the source, extract time-series
> telemetry, enrich with reference data, build analytical models."

[↑ Back to section](#deep-technical-topics-if-david-goes-there)

---

### "Little's Law — explain it and give an example"

> "Little's Law: L = λW.
> Average WIP = throughput rate × average cycle time.
>
> Fab example: 100 lots in WIP, throughput 20 lots/day → cycle time = 5 days.
> WIP doubles to 200, throughput stays at 20/day → cycle time doubles to 10 days.
>
> The power: you don't need to measure cycle time directly. Calculate it from
> WIP and throughput, both observable.
>
> The lever: to reduce cycle time without reducing WIP, increase throughput.
> To reduce cycle time without increasing throughput, reduce WIP. No free lunch."

[↑ Back to section](#deep-technical-topics-if-david-goes-there)

---

### "How do you calculate resource capacity and utilization?"

> "Utilization = actual output ÷ theoretical maximum capacity × 100%.
>
> Headroom = threshold − current peak utilization.
> If threshold is 80% and peak is 72%, I have 8 points of headroom.
>
> Time-to-capacity: growth slope from historical trending projects when
> peak utilization crosses the threshold.
> Growing 1.5 points/quarter with 8 points of headroom = ~5 quarters to breach.
>
> Effective capacity = theoretical × availability — raw theoretical capacity
> is never the real planning number."

[↑ Back to section](#deep-technical-topics-if-david-goes-there)

---

### "What's your experience with in-house vs. cloud capacity planning?"

> "Both — Citi was a hybrid model.
>
> On-prem: Oracle warehouse, BMC TrueSight, server/storage/network estate.
> Quarterly planning cycles, 12-month procurement horizons. The constraint
> is lead time — hardware takes months, so 6-month+ forecasting accuracy is critical.
>
> Cloud (AWS): S3, Glue, Redshift, ECS. Cloud changes the constraint model —
> you provision in minutes. Planning shifts from 'do we have enough?' to
> 'are we spending appropriately?' It's partly a FinOps problem: right-sizing,
> auto-scaling, Reserved vs. On-Demand.
>
> On-prem = procurement and lead-time problem.
> Cloud = cost optimization and right-sizing problem.
> Same analytical foundation, different action levers."

[↑ Back to section](#deep-technical-topics-if-david-goes-there)

---

### "How would you estimate the capacity of a bottleneck tool?"

> "Theoretical throughput: lots per hour at rated speed — that's the ceiling.
> Factor in availability: if the tool is up 85% of the time, effective capacity
> is 85% of theoretical.
> Factor in utilization within uptime: 70% utilization × 85% availability = ~60% effective.
>
> Headroom: if demand requires 75% of theoretical max and effective is 60%,
> you have a 15-point gap — that's your bottleneck.
>
> Validate against cycle time data: cycle time rising alongside utilization
> is the classic queuing nonlinearity that confirms the bottleneck."

[↑ Back to section](#deep-technical-topics-if-david-goes-there)

---

### "If throughput dropped 10% this week, how do you find the cause?"

> "Systematic decomposition, top down:
> 1. Tool availability — was the bottleneck tool down?
> 2. WIP starvation — shortage of lot starts feeding the tool?
> 3. Process rate — did the tool run slower (recipe change, degradation)?
> 4. Scheduling — lots misrouted or held in queue?
>
> Pull time-series data for each dimension, correlate timing with the drop.
> The variable that changes coincidentally with the throughput drop is the
> lead indicator. Quantify impact and drive the corrective action."

[↑ Back to section](#deep-technical-topics-if-david-goes-there)

---

## SQL Questions

---

### Top 5 Bottleneck Tools Query

```sql
SELECT
    tool_id,
    tool_name,
    AVG(utilization_pct)  AS avg_utilization,
    MAX(utilization_pct)  AS peak_utilization,
    COUNT(*)              AS reading_count
FROM tool_telemetry
WHERE reading_timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY tool_id, tool_name
ORDER BY avg_utilization DESC
LIMIT 5;
```

[↑ Back to section](#sql-questions)

---

### Consecutive Days Over Threshold (Gaps and Islands)

```sql
WITH daily_util AS (
    SELECT tool_id,
           DATE(reading_timestamp) AS day,
           AVG(utilization_pct)    AS daily_avg
    FROM tool_telemetry
    GROUP BY tool_id, DATE(reading_timestamp)
),
flagged AS (
    SELECT tool_id, day, daily_avg,
           CASE WHEN daily_avg >= 85 THEN 1 ELSE 0 END AS over_threshold
    FROM daily_util
),
grouped AS (
    SELECT tool_id, day, daily_avg, over_threshold,
           ROW_NUMBER() OVER (PARTITION BY tool_id ORDER BY day)
               - ROW_NUMBER() OVER (PARTITION BY tool_id, over_threshold ORDER BY day) AS grp
    FROM flagged
)
SELECT tool_id,
       MIN(day)   AS streak_start,
       MAX(day)   AS streak_end,
       COUNT(*)   AS consecutive_days
FROM grouped
WHERE over_threshold = 1
GROUP BY tool_id, grp
HAVING COUNT(*) >= 3
ORDER BY consecutive_days DESC;
```

> "The gaps-and-islands pattern — subtract two row numbers to identify consecutive runs."

[↑ Back to section](#sql-questions)

---

### Query Optimization Approach

> "Start with the execution plan — EXPLAIN or EXPLAIN ANALYZE. Look for full table
> scans where index scans should exist, hash joins on large unindexed tables,
> and row estimate errors indicating stale statistics.
>
> For analytical queries: partition pruning, window functions to avoid self-joins.
> In Oracle: watch for missing histogram stats on skewed columns and bad cardinality
> estimates causing wrong join order. CTEs sometimes materialize — verify.
>
> General rules: push filters early, avoid SELECT *, index join keys and
> high-cardinality filter columns."

[↑ Back to section](#sql-questions)

---

### Window Functions

> "Window functions compute aggregates over a sliding context without collapsing rows.
>
> LAG/LEAD: day-over-day utilization change without a self-join.
> ROW_NUMBER/RANK: most recent record per tool, or rank by utilization within a class.
> SUM/AVG OVER: rolling 7-day or 30-day moving average for smoothing telemetry noise.
> NTILE: bucket tools into utilization quartiles for tiered capacity reporting.
>
> Rolling 7-day average per tool:
> `AVG(utilization_pct) OVER (PARTITION BY tool_id ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`"

[↑ Back to section](#sql-questions)

---

## Python Questions

---

### Processing Large Time-Series Telemetry

> "For banking-scale telemetry at Citi — thousands of assets, years of history —
> I used PySpark. Distributes the load, handles partitioning, integrates
> natively with S3 and Redshift via Glue.
>
> For medium-scale: Pandas with chunked reads and vectorized operations —
> avoid row-level Python loops, use NumPy-backed operations.
>
> For HorizonScale: generator-based parallel pipeline — each asset's time-series
> fed through a generator, processed independently, parallelized with
> multiprocessing.Pool. 90% cycle time reduction vs. sequential design."

[↑ Back to section](#python-questions)

---

### Build a Capacity Forecasting Model in Python

```python
from prophet import Prophet
import pandas as pd

def forecast_capacity(telemetry_df: pd.DataFrame, periods: int = 180) -> pd.DataFrame:
    df = telemetry_df.rename(columns={"date": "ds", "utilization_pct": "y"})
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        changepoint_prior_scale=0.05
    )
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
```

> "yhat_upper is the capacity risk signal — the upper confidence bound.
> If yhat_upper crosses the threshold within the forecast window,
> that asset is flagged at risk."

[↑ Back to section](#python-questions)

---

### Python Data Analysis Stack

> "Core: Pandas, NumPy, SQLAlchemy for Oracle/Redshift connectivity.
> Visualization: Matplotlib, Seaborn, Plotly for interactive Streamlit dashboards.
> ML: scikit-learn for classification/regression, Prophet for time-series.
> Scale: PySpark on AWS Glue for distributed processing.
> Discipline: type hints everywhere, Pydantic for data model validation,
> pytest for pipeline testing, Black and ruff for formatting."

[↑ Back to section](#python-questions)

---

## Questions To Ask David Rojas

1. "What does the split look like between short-range capacity management — daily/weekly WIP — and long-range planning at the 6–18 month horizon?"
2. "What tools and data infrastructure is the team currently using — are you pulling from MES data directly or through separate analytics platforms?"
3. "Where are the biggest gaps today — analytical tooling, forecasting maturity, or coordination between the engineering and production teams?"
4. "How mature is the use of statistical or ML forecasting in the current capacity process?"
5. "What does success look like in the first 90 days for this role?"

[↑ Back to section](#questions-to-ask-david-rojas)

---

## Logistics & Pre-Interview Refresh

**Call details:**
- David Rojas calls you at **214-315-2190** at **9:00 AM CT Wednesday April 22**
- Have this doc open on second screen

**Key numbers to know cold:**
20+ years · 8 years Citi · 4 global regions · 6,000+ assets · 10 days → 2 days · 90% forecast accuracy · 6-month horizon · 90% cycle reduction

**Salary:** $145,000–$160,000 base

**30-minute pre-interview refresh:**
1. Opening 2 minutes — say it out loud cold
2. The 3 Pivot Moves — internalize the framing, especially Move 3
3. Factory Physics / Little's Law — plain language, no hesitation
4. OEE formula — Availability × Performance × Quality = OEE
5. BMC TrueSight story — most direct credential match
6. Story 3 (Bottleneck Investigation) — most likely deep follow-up

[↑ Back to section](#logistics--pre-interview-refresh)

---

## Job Requirements Coverage Check

| Job Bullet | Covered By | Status |
|-----------|-----------|--------|
| Capacity analysis — long/short term | Stories 1 & 3, Capacity analysis Q&A | ✓ |
| Identify actions to reduce gaps, drive to completion | Story 3, Bottleneck investigation Q&A | ✓ |
| Line analysis, supply chain forecasting, line balance | Line analysis Q&A, Supply chain Q&A, Takt time Q&A | ✓ |
| Bottleneck investigations using production plans + tool metrics | Bottleneck Q&A, Throughput drop Q&A, Little's Law | ✓ |
| Summarize risk to leadership | Risk presentation Q&A | ✓ |
| Coordinate manufacturing + engineering, quantify impact | Story 4, Coordination Q&A, Throughput impact Q&A | ✓ |
| Equipment efficiency analysis | OEE Q&A, SEMI E10 Q&A | ✓ |
| Factory Physics proficiency | Factory Physics Q&A, Little's Law Q&A, Takt time | ✓ |
| SQL / Python for analytics | Full SQL and Python sections | ✓ |
| Supply chain management | Supply chain Q&A, Lot starts Q&A, Yield Q&A | ✓ |

**Honest gaps if asked:**
- Direct fab / semiconductor experience: None — own it with Move 3
- MES systems (Opcenter, WorkStream): No direct experience — frame as same pattern as BMC TrueSight
- Physical shop floor: Acknowledge and redirect to analytical depth

[↑ Back to section](#job-requirements-coverage-check)
