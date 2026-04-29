# Citi High-Scale Telemetry Pipeline

---

## Team Context & Problem

The Capacity and Planning team at Citigroup sat at the center of a global
infrastructure operation. The mandate: help technology and business teams
across the enterprise understand their infrastructure position — where they
had headroom, where they were approaching limits, and what actions they
needed to take.

Scope: 65,000 to 70,000 monitored endpoints worldwide, four global regions,
dozens of departments, across every system type the bank ran: physical servers,
virtual machines, databases, and containers.

Capacity planning in financial services is not optional — it is a compliance
and operational continuity function. A trading system, a payments platform, or
a risk calculation engine that runs out of capacity during peak hours creates
regulatory exposure, customer impact, and potential financial loss. The
analysis had to be timely, accurate, and actionable enough for enterprise teams
to plan months ahead.

---

## The Manual Process

When the pipeline was designed, the entire monthly analysis was done manually
in Excel. The workflow had every characteristic of a process that had grown
organically to fill a need without ever being engineered.

**Steps and tools**

1. Extract — pull P95 telemetry from BMC TrueSight for all monitored endpoints. Tool: BMC TrueSight export.
2. Divide — manually split data into spreadsheets by region and system type. Tool: Excel.
3. Enrich — pull ownership, location, department data from CMDB and AppDynamics; manually join. Tool: SQL Server + Excel.
4. Clean — handle missing values, fix naming inconsistencies, remove invalid records. Tool: Excel (manual).
5. Calculate — apply safety and ceiling factors; compute adjusted utilization for each KPI. Tool: Excel formulas.
6. Sort & rank — order systems by utilization; surface top under-utilized and near-capacity. Tool: Excel.
7. Publish — distribute reports to enterprise teams; brief stakeholders. Tool: email and meetings.

End to end: 5 to 10 days every month.

Manual processes over five to ten days introduce drift: factors applied
inconsistently, enrichment data missed for some regions, judgment calls made
differently by different team members. The reports were produced, but their
consistency and reliability were bounded by the manual process that produced
them.

---

## Data Sources

Three sources. One primary telemetry source, two enrichment sources. No single
source was sufficient on its own.

**BMC TrueSight** (Oracle DB backend) — P95 time-series for CPU, Memory, Disk,
and Network across all 65–70K monitored endpoints. Extracted directly via
Oracle DB queries. Answered: what is happening.

**CMDB** (SQL Server, Change Management Database) — asset inventory: system
name, owner, region, department, tier, classification, environment. Answered:
who owns it and where it is.

**AppDynamics** — supplementary server metadata: ownership, location,
departmental assignment, application context not always present in CMDB.
Especially useful for systems that had been reassigned or were running workloads
not yet reflected in CMDB records.

Raw telemetry without enrichment context produces an unaddressed list of
numbers. With enrichment, every row in the report is associated with a
responsible team and a geography, making it immediately actionable.

---

## The Four KPIs & System Types

Every monitored endpoint was analyzed across four KPIs. Together they give a
complete picture of infrastructure health — a system can be under-utilized on
CPU but saturated on disk, or healthy across all KPIs but trending toward
memory exhaustion over the next quarter.

**CPU** — processing utilization at P95. Consistent high P95 signals compute
saturation; spikes suggest batch or peak-load problems.

**Memory** — RAM utilization at P95. Memory pressure causes swapping and
performance degradation before hard failures; often has a software root cause.

**Disk** — storage I/O and capacity utilization. Disk fills silently —
applications fail when storage is exhausted, often without warning to the
owning team.

**Network** — throughput and bandwidth utilization. Network saturation can be
invisible in CPU and memory metrics while causing severe latency for connected
systems.

**System types**

Physical — bare-metal servers. Fixed capacity, no elasticity, highest cost to
right-size up or down.

Virtual — VMs on shared hypervisor pools. More flexible, but still
capacity-bounded at the pool level.

Databases — disk and memory utilization patterns differ significantly from
compute workloads.

Containers — typically more dynamic, but resource limits still require planning.

---

## Safety & Ceiling Factors

Raw P95 telemetry tells you the 95th percentile utilization for the measurement
period. That number alone is not sufficient for capacity planning decisions —
it doesn't account for measurement uncertainty, and it doesn't define what
"too high" means operationally.

**Ceiling factor — the operational maximum**
The ceiling was set at 90%. A system running at 90% P95 CPU is at capacity —
no meaningful headroom for load spikes, batch jobs, or unexpected demand. The
ceiling defines the boundary between "operating normally" and "needs action."

**Safety factor — accounting for measurement confidence**
A single month's P95 doesn't capture every possible spike. The safety
multiplier of 1.15 was applied to the raw P95 to produce a conservative
adjusted utilization — effectively assuming real peak exposure is 15% higher
than measured, accounting for variance at approximately 85% measurement
confidence.

```python
# Utilization calculation (per KPI, per endpoint)
RAW_P95        = telemetry value from BMC TrueSight
SAFETY_FACTOR  = 1.15    # conservative buffer for measurement uncertainty
CEILING_PCT    = 0.90    # operational maximum threshold (90%)

adjusted_util  = RAW_P95 * SAFETY_FACTOR

# Flags
near_capacity  = adjusted_util >= CEILING_PCT
under_utilized = adjusted_util < UNDER_UTIL_THRESHOLD

# Headroom: how far below ceiling is the adjusted utilization?
headroom_pct   = (CEILING_PCT - adjusted_util) / CEILING_PCT
```

Applying the safety factor before comparing to the ceiling means the pipeline
is conservative by design — it flags systems as near-capacity before they
actually hit the limit, giving teams lead time to act.

Without the safety factor, the pipeline would only flag systems already at the
ceiling. In financial services infrastructure, no response time is not an
acceptable operational state.

---

## Pipeline Architecture

Classic ETL pattern: Extract from Oracle and SQL Server, Transform with Pandas
and NumPy, Load into SQLite — extended with a validation gate before
transformation and a publish step after load.

Database connections managed through SQLAlchemy, providing a consistent
abstraction layer over the Oracle backend (via cx_Oracle) for TrueSight
extraction and the SQL Server CMDB (via pyodbc). Excel output generated
programmatically using openpyxl. Version-controlled in GitLab with merge
requests required for any changes to transformation logic or calculation
parameters.

```
# Pipeline flow (high level)
0. VALIDATE (pre-run)
   ├── Assert source row counts above minimum expected threshold
   ├── Confirm all four KPI columns present in TrueSight extract
   ├── Check for null endpoint identifiers (join key integrity)
   └── Log extraction metadata: row count, timestamp, source version

1. INGEST
   ├── Extract TrueSight P95 data — SQLAlchemy + cx_Oracle → Oracle DB
   ├── Query CMDB reference data — SQLAlchemy + pyodbc → SQL Server
   └── Load AppDynamics server metadata export

2. NORMALIZE
   ├── Standardize endpoint identifiers across all three sources
   ├── Resolve hostname aliases and naming convention differences
   └── Handle missing values and invalid records

3. JOIN & ENRICH
   ├── Left join TrueSight data → CMDB on normalized hostname
   ├── Fill gaps with AppDynamics metadata where CMDB join fails
   └── Flag records with no enrichment match for manual review

4. CALCULATE
   ├── Apply safety factor (×1.15) to raw P95 for each KPI
   ├── Compute adjusted utilization vs ceiling threshold (90%)
   ├── Derive headroom percentage and capacity flag per KPI
   └── Classify each endpoint: near_capacity / healthy / under_utilized

5. LOAD → SQLite (idempotent)
   ├── Monthly database: drop-and-recreate for this period
   └── Master database: upsert on (endpoint_id, report_month)

6. PUBLISH
   ├── Generate Excel workbooks via openpyxl (by region, type, department)
   └── Streamlit dashboard refresh with new monthly data
```

The pipeline is idempotent by design. If it fails mid-run or needs to be rerun
with corrected source data, the monthly SQLite database is dropped and recreated
from scratch. The master database uses upsert logic on `(endpoint_id,
report_month)` so re-running a month produces the same result rather than
duplicating records.

---

## Data Transformation & Enrichment

The transformation stage was the most labor-intensive part of the initial build
and the stage that, in the manual process, consumed the most time and introduced
the most inconsistency.

**Identifier normalization**

Server names in BMC TrueSight, hostnames in the CMDB, and identifiers in
AppDynamics followed different conventions. A single server might appear as
`NYDB-PROD-042` in TrueSight, `nydb-prod-042.citi.com` in the CMDB, and
`NY_DB_PROD_042` in AppDynamics. Normalizing these to a canonical key —
lowercase, stripped of domain suffixes, with separator characters standardized —
was a prerequisite for any reliable join.

**Enrichment fallback strategy**

Priority order: CMDB as the primary reference source, AppDynamics as a fallback
for endpoints where the CMDB join failed or returned incomplete data, and a
"no enrichment" flag for endpoints that couldn't be matched to either.
Unmatched endpoints were reported separately rather than silently dropped.

```python
# Enrichment join with fallback (Pandas)
df = (
    trusight_df
    .merge(cmdb_df, on="hostname_normalized", how="left", suffixes=("", "_cmdb"))
    .merge(appdyn_df, on="hostname_normalized", how="left", suffixes=("", "_appdyn"))
)

# Fill CMDB gaps with AppDynamics data
for col in ["owner", "department", "region", "tier"]:
    df[col] = df[col].fillna(df[f"{col}_appdyn"])

# Flag records with no enrichment coverage
df["enrichment_status"] = df["owner"].apply(
    lambda x: "enriched" if pd.notna(x) else "no_match"
)
```

---

## SQLite Data Model

Two SQLite databases. The design was driven by specific reporting requirements:
fast queries against a single month's data, and longitudinal trend analysis
across months without querying every monthly database separately.

**Monthly database**
One SQLite file per reporting period. Full enriched and calculated dataset for
that month. Used for detailed drill-down, export, or comparison against another
specific month.

**Master progression database**
One record per endpoint per month — a longitudinal table that made
"system X has been trending from 60% to 75% to 88% CPU over three months" a
queryable fact rather than a manually compiled observation.

```sql
-- Master progression table (simplified)
CREATE TABLE endpoint_progression (
    endpoint_id      TEXT    NOT NULL,
    hostname         TEXT    NOT NULL,
    report_month     TEXT    NOT NULL,   -- YYYY-MM
    system_type      TEXT,               -- physical / virtual / database / container
    region           TEXT,
    department       TEXT,
    owner            TEXT,
    tier             TEXT,
    -- Raw P95 values
    cpu_p95          REAL,
    mem_p95          REAL,
    disk_p95         REAL,
    net_p95          REAL,
    -- Adjusted utilization (P95 × 1.15)
    cpu_adjusted     REAL,
    mem_adjusted     REAL,
    disk_adjusted    REAL,
    net_adjusted     REAL,
    -- Capacity flags
    cpu_flag         TEXT,   -- near_capacity / healthy / under_utilized
    mem_flag         TEXT,
    disk_flag        TEXT,
    net_flag         TEXT,
    enrichment_status TEXT,
    PRIMARY KEY (endpoint_id, report_month)
);

-- Query: systems trending toward capacity over last 3 months
SELECT hostname, department, region,
       cpu_adjusted,
       LAG(cpu_adjusted, 1) OVER w AS prev_month,
       LAG(cpu_adjusted, 2) OVER w AS two_months_ago
FROM endpoint_progression
WHERE cpu_flag = 'near_capacity'
WINDOW w AS (PARTITION BY endpoint_id ORDER BY report_month)
ORDER BY cpu_adjusted DESC;
```

---

## Two Output Directions

Every endpoint resolved into one of two actionable directions based on its
adjusted utilization relative to the ceiling threshold.

**Under-utilized — the savings opportunity**
Systems with consistently low adjusted utilization represented resource
allocation not earning its cost. In a global bank running tens of thousands of
physical and virtual servers, over-provisioned infrastructure adds up to
significant recurring spend. The pipeline surfaced the top under-utilized
systems ranked by severity, with enrichment data identifying the owning
department. Recommendations ranged from downsizing resource allocation, to
consolidating workloads onto fewer physical hosts, to promoting from physical
to virtual or on-premises to cloud where the workload profile supported it.

**Near-capacity — the proactive warning**
Systems trending toward or already at the 90% ceiling on any KPI were surfaced
for proactive outreach to the owning team. The critical design principle was
lead time. Infrastructure procurement, change management, and architecture
decisions at Citi operate on timelines of weeks to months. A warning with
enough lead time allows the team to engage capacity planning consultation and
develop a real response. A warning after the system is already at capacity means
the options are limited and the response is reactive.

The recommended action was not always "add hardware." Some capacity problems had
software root causes: memory leaks, inefficient query patterns consuming disk
I/O, batch jobs not sized correctly. The early warning created time to
investigate the root cause rather than defaulting to hardware remediation.

**Directions summary**

Under-utilized — adjusted utilization well below operational floor. Actions: downsize, consolidate, promote to virtual/cloud.
Near-capacity — adjusted utilization approaching or above 90% ceiling on any KPI. Actions: scale hardware, optimize software, architecture consultation, bug investigation.
Healthy + trending up — currently healthy but month-over-month utilization increasing. Actions: monitor closely, begin planning cycle before threshold is reached.

---

## Streamlit Internal Dashboard

The Excel reports remained the external deliverable — enterprise teams across
Citi consumed the output in that format. But internally, the capacity planning
team needed something more dynamic: the ability to browse the full dataset,
filter by region or department, drill into individual systems, and compare
month-over-month progression without opening multiple Excel files.

The Streamlit dashboard provided that internal interface, built on top of the
SQLite master database.

**Dashboard views**

Monthly Summary — top-level counts: near-capacity, under-utilized, healthy per region and system type.
Near-Capacity List — filtered, sortable list of systems at or approaching ceiling, by KPI, region, department.
Under-Utilization Ranking — ranked savings opportunities with estimated reallocation potential.
System Progression View — month-over-month utilization trend for a specific endpoint or department.
Department Health Summary — aggregate capacity health score per department for executive-level reporting.

---

## Impact: 5–10 Days to 1–2 Hours

The headline impact was the time reduction: the monthly analysis that previously
required five to ten days of manual work was produced in the first or second
hour after the BMC TrueSight export was ready. Same deliverables — Excel
reports by region and system type, enriched with ownership and department data,
with utilization calculations and capacity flags applied — generated
automatically, consistently, and without manual intervention.

The secondary impact was quality consistency. The pipeline applied identical
logic to every one of the 65,000+ endpoints, every month. The reports became
more trustworthy, which made the enterprise teams more willing to act on
near-capacity warnings and more confident in the savings recommendations.

The tertiary impact was team capacity. The five to ten days previously spent
producing data became available for the analysis and consultation work that was
the actual value the team delivered.

**Before vs after**

Monthly report production time — Before: 5–10 business days. After: 1–2 hours.
Data consistency — Before: variable, manual calculation and human judgment. After: deterministic, same logic applied to every endpoint.
Enrichment coverage — Before: dependent on analyst diligence per region. After: automated join across CMDB and AppDynamics with flagging.
Month-over-month trend visibility — Before: manual comparison across previous Excel files. After: queryable master SQLite database and Streamlit dashboard.
Team capacity for planning work — Before: limited, majority of month on data production. After: significant, pipeline frees team for analysis and consultation.

---

## Engineering Practices

```python
# Data validation gate (pre-transform)
def validate_extract(df: pd.DataFrame, source: str, min_rows: int) -> None:
    """Halt pipeline if source data fails quality checks."""
    if len(df) < min_rows:
        raise DataValidationError(
            f"{source}: {len(df)} rows — below minimum threshold {min_rows}"
        )
    required_cols = ["endpoint_id", "cpu_p95", "mem_p95", "disk_p95", "net_p95"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise DataValidationError(f"{source}: missing columns {missing}")
    null_keys = df["endpoint_id"].isna().sum()
    if null_keys > 0:
        raise DataValidationError(
            f"{source}: {null_keys} records with null endpoint_id (join key)"
        )
    logger.info(f"{source} validated: {len(df):,} rows, all checks passed")
```

**ETL pattern** — clear separation of Extract, Transform, and Load stages. Each independently testable and re-runnable.

**Data validation** — pre-transformation checks: row count thresholds, KPI column completeness, null join key detection. Pipeline halts on validation failure rather than processing corrupt input.

**Idempotency** — monthly databases are drop-and-recreate; master database uses upsert on `(endpoint_id, report_month)`. Safe to rerun on corrected source data without duplication or manual cleanup.

**Logging** — structured logging at each pipeline stage: extraction row counts, join coverage rates, validation pass/fail, enrichment match percentages, execution time per stage. Execution metadata written to an audit table in SQLite.

**Configuration management** — database credentials, safety factor, ceiling threshold, and region/department mappings held in config files. Threshold changes reviewed via GitLab merge request before deployment.

**Version control** — GitLab repository for all pipeline code. Merge request workflow for transformation logic changes, calculation parameter updates, and schema changes — full audit trail of what changed and when.

**Error handling** — each stage wrapped in explicit error handling. Failures surface a descriptive message identifying the stage and cause. Partial failures do not silently produce incomplete output.

**Enrichment coverage reporting** — unmatched endpoints counted and reported separately. Coverage rate tracked month-over-month — degrading coverage is a signal that CMDB records are going stale.

---

## Engineering Challenges

**Cross-system identifier normalization**
The hardest technical problem. Three enterprise systems — BMC TrueSight, the
CMDB, and AppDynamics — each used independent naming conventions for the same
endpoints. A server might have a short hostname in TrueSight, a fully qualified
domain name in the CMDB, and a different separator character in AppDynamics.
Normalizing these to a reliable join key required extensive data investigation:
cataloging the naming patterns in each source, building transformation rules,
and testing join coverage across the full 65K endpoint set. Poor join coverage
meant enrichment gaps; enrichment gaps meant reports delivered without owner
information — defeating a significant part of the pipeline's value.

**Scale with Pandas**
Operating on 65,000+ endpoints across four KPIs per month required attention to
Pandas memory management. Vectorized operations via NumPy rather than
row-by-row Python loops were essential for the calculation stage. Pre-filtering
DataFrames before joins — removing records already known to be invalid before
the merge step — significantly reduced peak memory usage during the enrichment
phase.

**SQLite concurrency and file management**
The dual-database design required careful file path management as the number of
monthly archives grew. A lightweight catalog file tracked available monthly
databases and their date ranges, so the Streamlit dashboard could dynamically
discover available history without hardcoded paths.

---

## Lessons Learned

**The most valuable part of a data pipeline is often the enrichment join.**
Raw telemetry has no action value without context. An endpoint at 88% CPU is a
number. An endpoint at 88% CPU owned by the Fixed Income trading platform in
the EMEA region, managed by a specific infrastructure team, is an actionable
alert. The work of connecting telemetry to ownership and context — through CMDB
joins, reference data enrichment, identifier normalization — is unglamorous
engineering, but it's what makes the output usable.

**Conservative calculations earn trust.**
The 1.15 safety factor was occasionally questioned by teams who received a
near-capacity warning and felt their system was "fine." The consistent response:
the pipeline is designed to give you lead time, not to tell you your system is
on fire right now. Systems flagged early with headroom to act are the goal. The
alternative — flagging only when systems are already at 90% — eliminates the
response window. Conservative thresholds, consistently applied and clearly
explained, build more trust than aggressive thresholds that produce false
urgency.

**Determinism is a quality argument, not just an efficiency argument.**
Reducing the report production time from ten days to two hours was visible and
immediately valued. The less visible but equally important improvement was that
the pipeline applied identical logic to every endpoint every month. In the
manual process, the 80,000th row of a spreadsheet was handled by a tired
analyst on day nine. In the pipeline, the 80,000th row gets the same
calculation as the first. That consistency is what makes the reports trustworthy
at scale.

---

## Interview Q&A

**Walk me through the architecture of this pipeline at a high level.**

The pipeline ingests P95 telemetry exports from BMC TrueSight covering 65,000
to 70,000 monitored endpoints across four KPIs: CPU, memory, disk, and network.
It normalizes endpoint identifiers across three source systems — TrueSight, the
CMDB on SQL Server, and AppDynamics — and joins the telemetry to enrichment
data to attach ownership, region, department, and tier to every row. The
enriched dataset is then transformed: a safety factor of 1.15 is applied to
produce a conservative adjusted utilization, which is compared to the 90%
ceiling threshold to classify every endpoint as near-capacity, healthy, or
under-utilized. Results load into SQLite — one monthly database per reporting
period and a master database for multi-month progression tracking. The pipeline
then generates Excel reports by region and system type and refreshes the
internal Streamlit dashboard. What used to take five to ten days runs in one to
two hours.

---

**Why did you choose SQLite for a dataset of this scale?**

The scale fit SQLite comfortably. 65,000 endpoints, four KPIs, monthly cadence,
a couple of years of history — that's a large dataset for Excel, but it's not
a distributed system problem. SQLite handles tens of millions of rows on a
single file with fast indexed queries, and it has zero operational overhead: no
server to manage, no connection pooling, no licensing.

The specific design — separate monthly files plus a master progression database
— mapped naturally to SQLite's file-per-database model. Each monthly database
is an isolated, portable artifact. The master database provides longitudinal
queryability without requiring joins across multiple files at query time.
A proper database server like PostgreSQL would have worked too, but would have
added infrastructure complexity for no additional analytical capability at this
scale.

---

**How did the safety and ceiling factors work, and why were those specific values chosen?**

The ceiling of 90% defines the operational maximum — a system consistently
hitting 90% utilization is at capacity with no headroom for demand spikes or
unexpected load. The 1.15 safety multiplier accounts for measurement
uncertainty: a single month's P95 doesn't capture every possible spike, and
the confidence in any sampled metric isn't 100%. Multiplying by 1.15 —
assuming the real peak exposure is 15% higher than measured — builds a
conservative buffer reflecting roughly 85% measurement confidence.

Together, these mean a system is flagged as near-capacity when its conservative
estimate approaches the operational ceiling, giving teams lead time before they
actually hit it. The alternative — flagging only when systems are already at 90%
— eliminates the response window. In financial services infrastructure, you want
weeks of lead time, not a same-day alert.

---

**What was the hardest technical problem to solve?**

Cross-system identifier normalization. Three enterprise systems — BMC TrueSight,
the CMDB, and AppDynamics — each used independent naming conventions for the
same endpoints. A server might have a short hostname in TrueSight, a fully
qualified domain name in the CMDB, and a different separator character in
AppDynamics. Getting reliable join coverage across 65,000 endpoints required
extensive data investigation: cataloging the naming patterns in each source,
building normalization rules to produce a canonical key, and iterating until
join coverage was high enough that the enrichment gaps weren't distorting the
reports. Poor join coverage meant some endpoints had no owner or department
assigned — which defeats the purpose of the enrichment step, because an
unaddressed near-capacity warning helps no one.

---

**What was the business impact beyond the time reduction?**

The time reduction from ten days to two hours was the visible impact. The less
visible but equally important impacts were quality consistency and team
capacity.

On quality: the manual process applied factors inconsistently, missed enrichment
data for some regions on some months, and depended on analyst judgment calls
made under time pressure on day nine. The pipeline applied identical logic to
every one of the 65,000 endpoints, every month — deterministically. That
consistency made the reports more trustworthy, which made enterprise teams more
willing to act on near-capacity warnings rather than treating them as advisory.

On team capacity: the days previously spent producing data became available for
the analysis and consultation work that was the actual value the team delivered.
The pipeline didn't replace the capacity planning expertise — it removed the
manual data work that was blocking the expertise from being applied.

---

**You mentioned near-capacity warnings sometimes led to bug fixes rather than hardware. Can you explain that?**

Capacity problems often have software root causes that look like infrastructure
problems in the telemetry. A memory utilization trending steadily upward month
over month might be a memory leak — not a workload that genuinely requires more
RAM, but a bug slowly consuming available memory until the system fails. A disk
utilization climbing toward the ceiling might be unrotated logs, uncleaned
temporary files, or a batch process writing data it never cleans up.

If the near-capacity warning arrives when the system is already at 88% and the
team orders more disk, they've fixed the symptom for a few months. If the
warning arrives at 70%, there's time to investigate whether the root cause is a
software issue that can be fixed permanently. The lead time the pipeline created
— by flagging systems conservatively before they hit the ceiling — was what made
the difference between reactive hardware remediation and proactive root cause
resolution.
