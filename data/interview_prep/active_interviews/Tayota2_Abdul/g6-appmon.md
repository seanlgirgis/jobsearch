# G6 Hospitality — Application Performance Monitoring Platform

---

## Project Context

G6 Hospitality is the parent company of Motel 6 and Studio 6. The brand.com
direct booking website is a primary revenue channel. In hospitality, website
performance is directly tied to conversion — a slow booking flow loses
customers to competitor sites. Every second of avoidable latency is a missed
booking.

G6 had invested in Dynatrace AppMon to instrument and monitor brand.com. AppMon
was capturing detailed telemetry, but the analytics and reporting that business
stakeholders and the dev team needed required a custom layer beyond what
Dynatrace's built-in dashboards provided.

---

## The Monitoring Gap

AppMon was doing its job — instrumented every transaction, captured response
times for every artifact in the request waterfall, surfaced alerts when
thresholds were breached. The gap was in the analytics layer above the raw data.
The built-in dashboards were rigid and didn't support the cross-dimensional
queries the team needed.

**Business questions that drove this project**

- Which pages and artifacts within them are consistently the slowest?
- Does performance vary by customer geography?
- Is mobile performance significantly different from desktop, and where in the artifact chain?
- How does performance trend over time — did a recent deployment improve or regress it?
- Where should the dev team focus next for maximum impact?

None of these required replacing Dynatrace. They required extracting its raw
data and building a custom analytics and reporting layer on top.

A monitoring tool that only generates alerts is reactive. The goal was to make
performance monitoring proactive — giving the team a continuous, segmented view
before users experienced problems.

---

## Dynatrace AppMon as Data Source

AppMon instruments web applications at the agent level — capturing every HTTP
request, tracing the full request lifecycle from browser initiation through
server processing and back, and recording timing data for every artifact in the
response chain. For brand.com this means every HTML page load, every CSS and JS
file request, every image, every third-party script, and every API call.

AppMon also captures session-level metadata: geographic origin, browser and
device type, user journey, and errors encountered. This metadata is what made
the segmentation approach possible — the raw data already contained the
geography and device dimensions. It just needed to be extracted and structured.

**AppMon capabilities and how they were used**

Full artifact chain timing — captured response times for every element in the page waterfall.
Session metadata — extracted geographic origin and device class for segmentation.
Transaction tracing — mapped customer interactions (search, select, checkout) as named transactions.
Error tracking — identified failed requests and their positions in the artifact chain.
Data export interface — used as the extraction point for the custom analytics pipeline.

---

## The Extraction Pipeline

Scripts pulled performance data out of AppMon through its data export interface
on a scheduled basis. Each extraction included the full set of dimensional
metadata: timestamp, application, transaction type, artifact identifier,
geography, and device class.

Extracted data was validated for completeness before loading into MySQL. Records
with missing dimensional data were flagged rather than silently dropped —
dropping incomplete records would have introduced geographic or device-class
bias into reports without any indication that data was missing.

```python
# Extraction pipeline (conceptual structure)
for each scheduled_run:
    raw_data = appmon.export_transactions(
        time_range   = last_period,
        applications = MONITORED_APPS,
        dimensions   = ["timestamp", "app", "transaction",
                        "artifact", "response_ms", "geo_region",
                        "device_class", "status"]
    )

    validated = validate_completeness(raw_data)
    flagged   = [r for r in raw_data if r not in validated]

    if flagged:
        log_incomplete_records(flagged)

    mysql.load(validated, table="performance_raw")
```

Scheduled extraction meant the MySQL database was continuously updated with
fresh performance data. Reports reflected current conditions, not a static
snapshot.

---

## Artifact Chain Analysis

The artifact chain is the waterfall of individual HTTP requests a browser makes
when loading a page. For brand.com, a single page load triggers a sequence:
HTML document, CSS stylesheets, JavaScript files, images, fonts, third-party
scripts (analytics, tracking pixels, chat widgets), and background API calls for
pricing and availability. Each step has its own response time. The chain's total
length is what the user experiences as page load time.

The key insight: different artifact types have different optimization paths. A
slow HTML response points to server-side rendering or database performance. Slow
JS points to bundle size or CDN delivery. Slow third-party scripts are often
outside direct control — but knowing which ones are the worst offenders gives
the team evidence to remove or defer them.

**Artifact types and optimization levers**

HTML — server render time, DB query latency. Fix: caching, query optimization, CDN.
CSS — file size, render-blocking delivery. Fix: minification, critical CSS inlining, deferred load.
JavaScript — bundle size, parse and execution time. Fix: minification, code splitting, async loading.
Images — file size, format, unoptimized delivery. Fix: compression, WebP, lazy loading, CDN.
Third-party scripts — external dependency latency, blocking behavior. Fix: audit and remove, defer, self-host.
API calls — backend response time, payload size. Fix: response caching, payload trimming, async loading.

---

## Geographical & Device Segmentation

A national hotel booking site serves customers across every US state on devices
ranging from high-end desktop browsers to older mobile phones on slower
connections. Rolling all of that into a single average hides more than it
reveals — two very different performance problems can cancel each other out in
an aggregate metric and appear as "acceptable" when neither individual
experience is acceptable.

Geographic segmentation revealed where CDN coverage gaps were creating elevated
response times in specific regions. Device segmentation revealed where large
JavaScript bundles were imposing disproportionate load times on mobile — the
parse-and-execute cost of a heavy JS bundle is significantly higher on a mobile
CPU than on a desktop, independent of network speed.

Together, these dimensions transformed reporting from "the site has a
performance problem" to "mobile users in the midwest have a specific problem in
the checkout flow driven by this script."

```sql
-- Artifact chain ranked by response time, mobile only
SELECT
    artifact_name,
    geo_region,
    device_class,
    AVG(response_ms)             AS avg_ms,
    PERCENTILE(response_ms, 95)  AS p95_ms,
    COUNT(*)                     AS sample_count
FROM performance_raw
WHERE
    device_class = 'mobile'
    AND transaction_name = 'checkout_flow'
    AND recorded_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY artifact_name, geo_region, device_class
ORDER BY p95_ms DESC
LIMIT 20;
```

P95 response time was a more useful reporting metric than average. Averages are
dragged down by fast responses and hide the tail of slow experiences. P95 shows
what the slowest 5% of users experience — where the real problems live.

---

## MySQL Data Layer

MySQL served as the aggregation and analytics database. The schema was built
around the dimensions needed for reporting: time, application, transaction,
artifact, response time, geography, and device. This structure supported both
high-granularity queries against individual artifact records and aggregated
trend queries across time ranges and segments.

```sql
-- Core performance data table (simplified)
CREATE TABLE performance_raw (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    recorded_at      DATETIME       NOT NULL,
    app_name         VARCHAR(100)   NOT NULL,
    transaction_name VARCHAR(200)   NOT NULL,
    artifact_name    VARCHAR(500)   NOT NULL,
    artifact_type    VARCHAR(50),           -- html, css, js, image, api, third_party
    response_ms      INT            NOT NULL,
    status_code      SMALLINT,
    geo_region       VARCHAR(100),
    device_class     VARCHAR(50),           -- desktop, mobile, tablet
    INDEX idx_app_tx   (app_name, transaction_name),
    INDEX idx_time     (recorded_at),
    INDEX idx_geo_dev  (geo_region, device_class)
);

-- Pre-aggregated summary table for fast dashboard queries
CREATE TABLE performance_summary (
    summary_date     DATE           NOT NULL,
    app_name         VARCHAR(100)   NOT NULL,
    transaction_name VARCHAR(200)   NOT NULL,
    artifact_name    VARCHAR(500)   NOT NULL,
    geo_region       VARCHAR(100),
    device_class     VARCHAR(50),
    avg_ms           DECIMAL(10,2),
    p95_ms           INT,
    p99_ms           INT,
    sample_count     INT,
    error_count      INT,
    PRIMARY KEY (summary_date, app_name, transaction_name,
                 artifact_name, geo_region, device_class)
);
```

Pre-aggregated summary tables were computed nightly from the raw data. Reports
ran against the summary tables for speed. The raw table was available for
drill-down investigation when a summary surfaced an anomaly worth investigating.

---

## Reporting & Analysis

Reports were structured around the questions the business actually needed
answered, not around the dimensions that happened to be easy to aggregate.

**Artifact Chain Slowdown Report** — dev team. Ranked list of slowest artifacts
by transaction — identifies specific files and API calls to optimize.

**Geographic Performance Map** — infra and dev. Response times by US region —
surfaces CDN gaps and regionally concentrated issues.

**Mobile vs Desktop Comparison** — dev team. Side-by-side response times by
device class — highlights where mobile experience diverges.

**Weekly Trend Report** — management and dev. Week-over-week performance trend —
shows whether deployments improved or regressed performance.

**Third-Party Script Audit** — dev and product. Response time and error rate for
all external scripts — evidence for remove/defer decisions.

**Transaction Flow Report** — product and dev. Per-step response times for
search to select to checkout — identifies conversion-critical bottlenecks.

The weekly trend report was the highest-value recurring output. Every deployment
was followed by a data-driven answer to "did this make things better or worse?"
rather than relying on anecdote or waiting for user complaints.

---

## Findings & Recommendations

**JavaScript bundle weight.**
Multiple JS files consistently appeared at the top of the artifact chain
slowdown report, particularly on mobile. Recommendations: audit the bundle for
unused code, defer non-critical scripts from initial page load, consolidate
multiple small JS files to reduce round-trip requests, minify uncompressed
scripts.

**Third-party script latency.**
Several third-party scripts — analytics tags, marketing pixels, embedded
widgets — were loading synchronously in the page head, blocking rendering until
their responses completed. These contributed disproportionately to
first-contentful-paint latency. Recommendation: load all non-critical
third-party scripts asynchronously or defer until after main content rendered.

**Regional CDN coverage.**
Geographic segmentation showed elevated response times in specific regions for
the same artifacts. This pattern is characteristic of CDN PoP gaps — the
nearest CDN node is farther away for users in those regions. Finding was
surfaced to the infrastructure team as evidence for CDN configuration review.

**Mobile-specific rendering paths.**
Mobile users experienced significantly higher JavaScript execution time on the
checkout flow compared to desktop. Recommendation: review whether the checkout
page was serving a mobile-optimized payload or a desktop-equivalent payload on
a device with less processing capacity.

---

## Impact & Outcomes

Following implementation of the recommended frontend changes, response times
improved measurably across monitored transactions on brand.com. The improvements
were visible in the weekly trend reports as a sustained shift in both average
and P95 response times — not a one-week anomaly but a durable improvement
tracked over multiple reporting cycles.

The structural outcome was the shift from reactive to proactive performance
management. Before the pipeline, performance issues were discovered through
Dynatrace alerts or user complaints. After, the dev team had a continuous,
segmented view of where performance stood and where it was trending.

The reports also created a shared language between the development team,
infrastructure team, and business stakeholders. A geographic performance map is
accessible to a VP in a way that a raw Dynatrace dashboard is not.

**Before vs after**

Performance visibility — Before: alert-driven, issues discovered reactively. After: continuous segmented reporting.
Dev prioritization — Before: based on anecdote and user complaints. After: driven by ranked artifact chain data.
Geographic insight — Before: aggregate metrics, regional issues hidden. After: per-region response times surfacing CDN gaps.
Mobile vs desktop — Before: single combined metric. After: device-class segmentation revealing mobile-specific issues.
Deployment validation — Before: manual spot-checks or waiting for alerts. After: weekly trend reports confirming improvement or regression.

---

## Lessons Learned

**Monitoring tools give you data, not insight.**
AppMon was capturing everything needed to answer the business questions. The gap
was not in the monitoring tool — it was in the analytics layer that turned raw
telemetry into prioritized, segmented, actionable information. Building that
layer is an engineering problem separate from the monitoring configuration
problem. Teams often conflate these two: assuming a better monitoring tool will
automatically produce better insight. It won't without the analytics layer on
top.

**Segmentation is not optional for distributed user bases.**
A national hospitality brand has customers in every state on every device.
Rolling all of that into a single average hides more than it reveals. The moment
geography and device class were added as dimensions, the data started telling a
completely different story. Problems that were averaging out became visible.
Root causes that looked identical in the aggregate turned out to require
completely different fixes once segmented.

**P95 is a better metric than average for user-facing performance.**
Averages are dominated by the fast majority and understate the slow tail. The
slowest 5% of user sessions are often the most impactful on conversion — these
are users who are already frustrated, and the average metric gives no visibility
into their experience.

The same pipeline pattern applies across industries and monitoring tools.
Whether the source is Dynatrace, Prometheus, Datadog, or a custom metrics API,
the engineering problem is the same: extract the raw data, store it in a
structure optimized for your analytical queries, add the dimensions that matter
for your business, and build reports that answer the questions stakeholders
actually need answered.

---

## Interview Q&A

**You had Dynatrace AppMon already — why build a custom pipeline on top of it?**

AppMon was capturing all the right data. The problem was the analytics and
reporting layer above it. The built-in dashboards were rigid — they didn't
support the cross-dimensional queries the team needed: "which artifacts are
slowest on mobile specifically in the midwest?" or "did this week's deployment
improve or regress checkout performance?" Answering those questions required
extracting AppMon's raw data, storing it in a structured database, and building
custom reports against it. The monitoring tool is the data source. The analytics
layer is the engineering work that turns raw telemetry into something the
business can act on. Those are two separate problems, and solving only the first
one leaves the insight gap open.

---

**Why did geographic and device segmentation matter so much for this project?**

A national hotel booking website serves customers across every US state on
devices ranging from high-end desktop to older mobile phones on slower
connections. Aggregate all of that into a single response time metric and very
different problems cancel each other out and appear as "acceptable."

Geographic segmentation revealed CDN PoP gaps — users in certain regions were
getting consistently higher latency because the nearest CDN node was farther
away. Device segmentation revealed that heavy JavaScript bundles were imposing
disproportionate load times on mobile, where CPU parse-and-execute cost is
significantly higher than on desktop. These two problems have completely
different fixes. Without segmentation you'd never know which one you were
actually dealing with.

---

**How did the artifact chain analysis work, and why was it more useful than top-level page timing?**

A page load is a waterfall of individual requests: HTML, CSS, JavaScript,
images, third-party scripts, API calls. Each step has its own response time,
and the chain total is what the user experiences. If you only measure the
top-level page load time, you know the page is slow but have no idea where to
fix it.

Analyzing the chain tells you which specific artifact is the bottleneck. Slow
HTML points to server-side or database issues. Slow JavaScript points to bundle
size or CDN delivery. Slow third-party scripts are sometimes outside direct
control — but knowing which ones are the worst offenders gives the team evidence
to defer, remove, or self-host them. The chain analysis turns "the page is slow"
into a ranked, actionable list of specific files and calls to address.

---

**Why MySQL for this use case rather than Redshift or a time-series database?**

MySQL was the right fit for the scale and access patterns of this project. The
data volume — scheduled extractions from one monitoring system covering a
handful of web applications — was well within what MySQL handles comfortably.
The team was already proficient with SQL, so no ramp-up cost. The queries
needed — aggregations by dimension, trend analysis over time windows, drill-down
from summaries to raw records — are exactly what a relational database is
designed for.

Pre-aggregated summary tables handled the performance requirements for recurring
reports. A distributed warehouse like Redshift or a time-series database like
InfluxDB would have been over-engineering — more operational complexity for no
additional analytical capability at that scale.

---

**How did the reports translate into actual frontend improvements?**

The reports created a prioritized, evidence-based action list for the dev team.
When the artifact chain report showed specific JavaScript files consistently at
the top of the slowdown ranking — particularly on mobile — the recommendation
was concrete: defer non-critical scripts, minify uncompressed bundles,
consolidate requests. When the data showed third-party scripts loading
synchronously in the page head and blocking rendering, the recommendation was
to switch those to async or deferred loading.

The key thing is that "advise" here meant presenting the data, the specific
files involved, and the measured impact — not a vague suggestion to "optimize
performance." The team could see exactly which artifact was costing how many
milliseconds, on which device class, in which region. That specificity is what
makes a recommendation actionable versus aspirational.

---

**What's the broader pattern here that applies beyond this specific project?**

Monitoring tools capture telemetry, but insight requires an analytics layer on
top. Whether you're working with Dynatrace, Prometheus, Datadog, or a custom
metrics API, the engineering problem is the same — extract the raw data, store
it in a structure optimized for your analytical queries, add the dimensions that
matter for your business, and build reports that answer the questions
stakeholders actually need answered.

The specific tools change. The pattern doesn't. I've applied the same thinking
across data engineering contexts well beyond web performance — any time a
business has a data-generating system and needs insight from it, the problem
structure is identical: source, extraction, modeling, analytics, reporting.
