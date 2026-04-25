# Audio Script — G6 Hospitality: Application Performance Monitoring Platform
# Slug: g6-appmon
# HOST voice: nova | SEAN voice: onyx
# Chunk target: ~750 chars

---

**[HOST — voice: nova]**
Today we're looking at one of Sean's earlier projects — an application performance monitoring platform he built at G6 Hospitality, the parent company behind Motel 6 and Studio 6. Sean, give us the context. What was the problem?

**[SEAN — voice: onyx]**
G6 runs brand-dot-com, the direct booking website for hundreds of Motel 6 and Studio 6 locations. Direct bookings matter a lot — every second of latency on that website has a direct relationship to conversion and revenue. The company was using Dynatrace AppMon for performance monitoring, which is a solid enterprise tool, but what Dynatrace gives you out of the box are dashboards. What we needed was custom analytics — the ability to slice the data by geography, by device type, trend it over time, and surface actionable recommendations for the development team.

**[HOST — voice: nova]**
So the built-in Dynatrace dashboards weren't enough?

**[SEAN — voice: onyx]**
They captured the right data — AppMon instruments every web request and traces the full artifact chain — but the reporting layer was rigid. You couldn't easily ask "which page components are slowest for mobile users in the southeast?" or "how did response time change this week versus last week for a specific device class?" Those are the questions the business needed answered, and they required pulling the raw data out of AppMon and building a custom analytics layer on top of it.

**[HOST — voice: nova]**
Walk me through the extraction pipeline. How did you get the data out of AppMon?

**[SEAN — voice: onyx]**
AppMon exposes its data through a reporting and export interface. We built scripts that pulled the performance data programmatically — response times, error rates, and the full artifact chain breakdown for each monitored transaction. The artifact chain is the waterfall: the initial H-T-M-L response, then C-S-S, JavaScript, images, third-party scripts, A-P-I calls — each step in the chain has its own response time, and the full chain adds up to what the user actually experiences as page load time. We were capturing all of that, not just the top-level aggregate.

**[HOST — voice: nova]**
And you mentioned segmentation — by geography and device. How did that work?

**[SEAN — voice: onyx]**
Dynatrace tags each session with metadata about where the request came from and what kind of device initiated it. We extracted those tags as dimensions on the performance data. So instead of "the homepage loads in X seconds," you get "the homepage loads in X seconds for desktop users in California and Y seconds for mobile users in Texas." Those two numbers can be very different, and the root cause of each problem is often completely different — a heavy J-S bundle hits mobile harder, a regional C-D-N gap shows up geographically. You need the segmentation to know which problem you're actually solving.

**[HOST — voice: nova]**
Where did the data go once it was extracted?

**[SEAN — voice: onyx]**
Uploaded to a My-S-Q-L database. Each record captured the timestamp, the monitored application, the transaction type, the specific artifact being measured, the response time, the geography, and the device class. That structure let us run queries across time ranges and dimensions, aggregate by region or device, and compare before-and-after snapshots when changes were deployed. My-S-Q-L was the right choice here — the data volume was manageable, everyone on the team knew how to query it, and we didn't need a distributed system for this use case.

**[HOST — voice: nova]**
What did the reports look like?

**[SEAN — voice: onyx]**
We built reports that showed the artifact chain response times ranked by slowest to fastest, segmented by geography and device. The goal was to surface the highest-impact problem areas — not just "the site is slow" but "the checkout flow is slow specifically on mobile in the midwest, and this third-party script is the dominant contributor." That level of specificity is what turns a performance report into an action list for the development team. Without the segmentation, you're averaging out problems that have different causes and different fixes.

**[HOST — voice: nova]**
How did those findings translate into actual changes?

**[SEAN — voice: onyx]**
The reports fed directly into recommendations to the frontend team. When the data showed that certain J-S files were consistently the longest-running items in the artifact chain, we advised optimizations — deferred loading, minification, consolidating or removing third-party scripts that weren't worth their latency cost. When the data showed geographic gaps in C-D-N coverage, that informed infrastructure conversations. The data gave the team confidence in what to prioritize because the evidence was right there — not anecdote, not user complaints, but measured response times across thousands of real sessions, segmented by the exact dimensions that mattered.

**[HOST — voice: nova]**
What was the outcome?

**[SEAN — voice: onyx]**
Response times improved measurably across the monitored applications after the recommended changes were implemented. The bigger outcome, though, was that the team went from reactive to proactive. Before, performance issues were discovered by users or in Dynatrace alerts. After, the reporting pipeline gave the team a continuous view of where performance stood, which areas were trending worse, and where to focus next. That shift from alert-driven to data-driven performance management is the real value of building a layer like this on top of a monitoring tool.

**[HOST — voice: nova]**
Any lessons you'd carry forward from this project?

**[SEAN — voice: onyx]**
Two things stand out. First: monitoring tools give you data, not insight. Dynatrace AppMon was doing its job perfectly — it was capturing everything. The gap was the analytics layer that turned raw telemetry into prioritized, segmented, actionable information. Building that layer is an engineering problem, not a monitoring configuration problem. Second: segmentation is not optional when you have a geographically distributed user base on multiple device classes. A national hotel booking site has customers in every state on every device. Rolling everything up into a single average hides more than it reveals. The moment you add geography and device as dimensions, the data starts telling a completely different story.

**[HOST — voice: nova]**
Performance monitoring as a data engineering problem — extract the telemetry, model it, analyze it, surface recommendations. That framing applies well beyond hospitality.

**[SEAN — voice: onyx]**
It's the same pattern everywhere. The monitoring tool is the data source. The extraction pipeline, the data model, and the analytics layer are the engineering work. Whether you're doing it with Dynatrace and My-S-Q-L or Prometheus and ClickHouse, the problem is the same: turn raw telemetry into something the business can act on.

---
END OF SCRIPT
Voices: HOST (nova), SEAN (onyx)
Project: G6 Hospitality — Application Performance Monitoring Platform
Slug: g6-appmon
