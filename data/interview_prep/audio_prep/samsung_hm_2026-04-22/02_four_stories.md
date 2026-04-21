# Samsung HM Interview — Audio 2: Your 4 Stories
## What This Audio Covers
Your four STAR-format stories in Samsung framing, plus the full scripted answer for "Tell me about yourself" and "Walk me through your capacity planning experience." These are the backbone of the interview.

---

## Story 1 — BMC TrueSight Capacity Optimization (Your Anchor Story)

**Situation:** Citi needed to manage capacity across 6,000 plus infrastructure assets — servers, storage, network — feeding a live BMC TrueSight Helix environment.

**Task:** Build a scalable pipeline to collect, clean, and analyze peak utilization telemetry and surface capacity constraints before they impacted operations.

**Action:** Designed Python and Pandas pipelines ingesting TrueSight telemetry, integrated CMDB metadata, built Oracle warehouse schemas for historical trending, created dashboards for leadership capacity review.

**Result:** Automated what was previously a 10-day manual process. Capacity risk flagged weeks ahead of threshold breach. Reports consumed by both engineering teams and senior leadership.

Use this story when asked: "Tell me about your capacity planning experience" or "Have you worked with BMC TrueSight?"

---

## Story 2 — HorizonScale: ML Forecasting Engine (Your Flagship)

**Situation:** Manual forecasting was slow, reactive, and could not scale across thousands of assets. No predictive signal — teams were always behind the curve.

**Task:** Replace manual forecasting with an automated ML-driven system that predicted bottlenecks before they occurred.

**Action:** Built HorizonScale from scratch — PySpark telemetry pipeline at banking scale, Prophet for time-series trend and seasonality decomposition, scikit-learn classifiers flagging assets at risk. Generator-based parallel pipeline cut processing cycles by 90 percent.

**Result:** 6-month ahead bottleneck prediction at 90 percent plus accuracy. Leadership saw capacity risk by resource class, region, and time horizon. Cycle time from data to insight dropped from days to minutes.

Use this story when asked: "Tell me about ML in capacity planning" or "Your most impactful project" or "Forecasting experience."

---

## Story 3 — Bottleneck Investigation and Constraint Removal

**Situation:** Recurring bottlenecks in specific server tiers at Citi — root cause unclear. Was it growth? Inefficiency? Bad allocation?

**Task:** Determine whether bottlenecks were structural — a capacity gap — or operational — a utilization inefficiency — and drive targeted action.

**Action:** Built SQL analytical queries over P95 utilization history to segment assets by pattern: over-utilized, under-utilized, spiky versus flat. Correlated with CMDB metadata. Found clusters of under-utilized assets alongside over-utilized ones in the same tier — a scheduling and allocation gap, not a capacity gap.

**Result:** Rebalancing recommendation quantified with data. Hardware procurement avoided. Engineering teams given actionable data instead of "buy more."

Use this story when asked: "Bottleneck analysis" or "How do you approach capacity gaps?" or "Constraint removal."

---

## Story 4 — Cross-Team Capacity Coordination

**Situation:** Capacity decisions at Citi required alignment between infrastructure engineering, application teams, finance, and procurement — all with different views of the same data.

**Task:** Create a shared capacity view all stakeholders trusted and could act from.

**Action:** Built unified reporting pulling from TSCO, CMDB, and project intake. Standardized definitions. Ran monthly capacity reviews presenting automated bottleneck reports with risk tiers and recommended actions.

**Result:** Forecasting became proactive. Procurement cycles aligned to the 6-month horizon. Eliminated surprises in hardware planning.

Use this story when asked: "Cross-functional coordination" or "Stakeholder management" or "How do you drive action from data?"

---

## "Tell me about yourself" — Full Scripted Answer

> "I'm a Senior Capacity and Data Engineer with over 20 years of experience. Most recently I spent 8 years at Citi leading capacity planning and data infrastructure across 4 global regions — monitoring tens of thousands of servers and infrastructure assets worldwide.
>
> I built the data pipelines and ML forecasting systems that replaced a 10-day manual Excel process — we got reports out in 2 days with zero errors. I designed forecasting models using Prophet and scikit-learn that predicted capacity 6 months ahead, accounting for seasonality and growth trends. That system — HorizonScale — reduced forecasting cycle time by 90 percent and predicted bottlenecks at 90 percent plus accuracy.
>
> My background is IT infrastructure capacity planning, and I understand the Samsung role is in semiconductor manufacturing. The analytical methodology is identical — bottleneck analysis, utilization modeling, Factory Physics, supply chain lead time forecasting. The domain is different, the discipline is the same.
>
> I'm excited about this role because it applies that methodology in a domain where the stakes are higher — capacity decisions in a fab directly determine output, revenue, and capital investment."

---

## "Walk me through your capacity planning experience" — Full Scripted Answer

> "At Citi I owned end-to-end capacity planning for the infrastructure estate — think of it as the fab capacity function, but for servers and storage instead of wafer tools.
>
> On the data side: I built automated ETL pipelines pulling peak utilization telemetry from BMC TrueSight Capacity Optimization across 6,000 plus assets. Data cleaned, enriched with asset metadata, loaded into Oracle for historical trending.
>
> On the analysis side: I performed bottleneck investigations identifying which asset classes were approaching capacity thresholds and whether the cause was structural growth or utilization inefficiency. I built the same short-range and long-range views the Samsung role describes — weekly operational reporting and 6-month planning horizon forecasting.
>
> On the forecasting side: Prophet and scikit-learn ML models predicting capacity breaches 6 months ahead. I ran sensitivity analysis — what does the picture look like if growth accelerates 20 percent? That gave leadership decision options, not just a status report.
>
> On the coordination side: monthly capacity reviews with engineering, application, finance, and procurement teams — translating utilization data into procurement decisions with quantified cost and lead time for each option."
