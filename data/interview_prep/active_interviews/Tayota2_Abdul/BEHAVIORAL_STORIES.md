# Behavioral Stories — Abdul Interview
<a id="toc"></a>
## Table of Contents
1. [Story 1 — "Tell me about a time you solved a problem at a scale you hadn't seen before"](#sec-1)
2. [Story 2 — "Tell me about a time a system failed and how you handled it"](#sec-2)
3. [Story 3 — "Tell me about a time you delivered something that changed how a team operated"](#sec-3)
4. [Story 4 — "Tell me about a time you had to convince a team to change direction"](#sec-4)
5. [Story 5 — "Tell me about a time you improved a process that others had accepted as normal"](#sec-5)
6. [The One-Line Version (for when your brain is foggy)](#sec-6)
7. [The Opener — "Why Toyota?"](#sec-7)
8. [Virtual Interview Reminders (Teams over computer)](#sec-8)

**Toyota Way Values mapped to your real projects**
*Read once. Sleep on it. You already know these stories.*

---

<a id="sec-1"></a>
## Story 1 — "Tell me about a time you solved a problem at a scale you hadn't seen before"
**Toyota Value: Drive Curiosity + Get Better and Better**

**S:** At HorizonScale we had tens of thousands of servers and needed 180-day capacity forecasts. Nobody had built this before internally. The data was 65,000+ metrics — way too many to model manually.

**T:** I needed a forecasting system that could handle that volume, pick the right model per series, and actually be trusted by the ops team.

**A:** I got curious about the data first — spent time understanding how different server types behaved before writing a line of code. Then I built a model tournament: Prophet, ARIMA, Holt-Winters running head to head, with the winner selected automatically by error metric per series. Built observability in so the team could see which model won and why.

**R:** We went from manual one-off forecasts to a platform that ran across the full fleet. Ops team started making proactive capacity decisions instead of reactive ones. The curiosity paid off — if I'd just picked one model and shipped it, half the fleet would have had bad forecasts.

---
[Back to TOC](#toc)


<a id="sec-2"></a>
## Story 2 — "Tell me about a time a system failed and how you handled it"
**Toyota Value: Observe Thoroughly + Work with Integrity**

**S:** Early in my Citi pipeline work, a monthly capacity run completed "successfully," but part of the output was wrong because enrichment joins failed for a subset of endpoints.

**T:** I had to identify the root cause quickly, correct the report safely, and prevent silent bad output from happening again.

**A:** I traced the issue to an edge case in hostname normalization across source systems. I fixed the transformation logic, reran the pipeline, and added hard validation gates: row-count checks by stage, required-column checks, join-coverage thresholds, and explicit flags for unmatched endpoints instead of silent null propagation.

**R:** The corrected report was delivered, and future runs became much more reliable. The bigger result was process maturity: we moved from "pipeline ran" to "pipeline proved data correctness."

---
[Back to TOC](#toc)


<a id="sec-3"></a>
## Story 3 — "Tell me about a time you delivered something that changed how a team operated"
**Toyota Value: Act for Others + Create Room to Grow**

**S:** At G6 Hospitality, the operations team was flying blind. They had alerts, but the alerts were noise — firing constantly with no signal. Engineers were fatigued and ignoring them.

**T:** My job was to build an observability platform using Dynatrace that operations could actually trust and act on.

**A:** I started by sitting with the ops team — not the engineers. I asked what decisions they needed to make and when. Turned out they didn't need more data, they needed the right three signals at the right time. I redesigned the alerting around those three signals, added synthetic monitoring to catch issues before real users hit them, and built the FAST project dashboard so the morning standup had one source of truth.

**R:** Alert fatigue dropped dramatically. The ops team went from ignoring dashboards to running their morning standup off them. The shift was simple: I treated ops as the customer, not the endpoint.

---
[Back to TOC](#toc)


<a id="sec-4"></a>
## Story 4 — "Tell me about a time you had to convince a team to change direction"
**Toyota Value: Work with Integrity + Show Respect for People**

**S (Situation):** Midway through a pipeline build, the team leaned toward full hourly reloads because it was simpler to implement under timeline pressure.

**T (Task):** I needed to help the team choose a design that would still perform and stay cost-efficient as volume grew, without creating conflict.

**A (Action 1):** Instead of debating in the meeting, I built a simple projection using current table size, growth rate, and hourly reload frequency, then showed what the Q3 impact would look like in runtime and cost.

**A (Action 2):** I framed it as risk visibility, not "you are wrong," and I offered to own the incremental-load design so the added complexity was on me, not the rest of the team.

**R (Result):** The team switched to incremental processing. Months later, when volume had scaled significantly, the pipeline remained stable and cost-efficient. The key lesson: influence works best when you bring data, remove friction for others, and keep ego out of the room.


[Back to TOC](#toc)

<a id="sec-5"></a>
## Story 5 — "Tell me about a time you improved a process that others had accepted as normal"
**Toyota Value: Continue the Quest for Improvement**

**S (Situation):** When I joined Citi capacity planning, the monthly process was heavily manual: export telemetry, enrich in Excel, apply formulas, and publish reports. It took 5-10 business days and everyone saw it as normal.

**T (Task):** I needed to turn it into a reliable, repeatable pipeline so the team could spend time on decisions instead of spreadsheet mechanics.

**A (Action 1):** I mapped the workflow end to end and built a Python ETL pipeline to automate extraction, normalization, enrichment, calculations, and report generation.

**A (Action 2):** I added validation gates (row counts, required columns, join coverage) and idempotent reruns so quality was provable, not assumed.

**R (Result):** The process dropped from 5-10 days to about 1-2 hours, output consistency improved across 65,000+ endpoints, and the team shifted from manual report production to proactive capacity planning.


[Back to TOC](#toc)

<a id="sec-6"></a>
## The One-Line Version (for when your brain is foggy)

| Story | One Line |
|---|---|
| HorizonScale forecasting | "I got curious before I coded — ran a model tournament across 8,000 series" |
| Citi schema drift failure | "Green pipeline, wrong data — I traced it to silent schema drift and replayed from Bronze" |
| G6 ops dashboard | "I treated ops as the customer, not the endpoint — three signals beat 300 alerts" |
| Incremental vs full reload | "I put the numbers in front of the team, not the argument" |
| Process improvement | "5-10 days manual Excel -> 1-2 hours automated ETL with quality gates" |

---

*You know these stories. Sleep. Wednesday you sharpen. Thursday you show up.*

---

[Back to TOC](#toc)

<a id="sec-7"></a>
## The Opener — "Why Toyota?"

> "Toyota Financial Services is enabling people to own vehicles they couldn't otherwise — that's a real equity play. I want to build the data platform that makes that run reliably at scale."

30 seconds. Specific. Done.

**Wednesday morning — 10 minutes only:** Google "Toyota Financial Services Mobility for All 2026" so you have one real recent detail to drop in. One fact. That's it.

---

[Back to TOC](#toc)

<a id="sec-8"></a>
## Virtual Interview Reminders (Teams over computer)

- **Camera on. Business casual on top. Background clean. Lighting in front of you, not behind.**
- **The PDF said "computer skills."** For a Lead SE that's not about Excel. It means: can you communicate clearly without being in the room? Every answer you give is a demo of that. Structured. Not rushing. Eye contact with camera not screen.
- **Smile when you join.** Abdul sees your face before you speak. First impression is frame and energy, not words.
[Back to TOC](#toc)

