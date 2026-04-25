## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: Amazon Athena
Output filename: final_aws-athena.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md

---

**[HOST — voice: nova]**

Let's start from the top. What is Amazon Athena, and why would a data engineer reach for it?

---

**[SEAN — voice: onyx]**

So... basically... Athena is a serverless interactive S-Q-L service that lets you query data directly in S-3 without provisioning clusters. Under the hood it's a Presto and Trino style distributed engine, but operationally you just submit queries and read results. It's compelling because there's no server patching, no node sizing, and no idle compute cost when nobody is querying. You pay for data scanned, so it's excellent for ad-hoc analytics and exploration on a data lake. It's not a replacement for every warehouse workload, but for flexible discovery it's a strong default.

---

**[HOST — voice: nova]**

Got it. So when I click run on a query, what actually happens behind the scenes?

---

**[SEAN — voice: onyx]**

Here's the thing... the engine reads table metadata from the Glue catalog first, including schema and S-3 object locations. Then a distributed execution plan is built, workers read relevant files, apply filters and projections, and aggregate results in parallel. You don't manage those workers, A-W-S does, which is why the service feels instant to start. Query outputs are written to an S-3 results location, and that output path becomes part of your operational audit trail. Workgroup settings can also enforce limits, encryption, and output controls before a query even executes. So the flow is metadata lookup, distributed scan, governed execution, and persisted result.

---

**[HOST — voice: nova]**

Makes sense. Everyone mentions file format, so why is that such a big deal for Athena?

---

**[SEAN — voice: onyx]**

Here's the key insight... Athena cost and speed are dominated by bytes scanned, so storage format is your biggest lever. Row formats like C-S-V and raw J-S-O-N force broad scans, even when you only need a few columns. Columnar formats like Parquet and O-R-C let the engine read only needed columns and skip large sections of data. In practice, teams often see SIXTY to EIGHTY percent scan reduction after converting ingestion outputs to columnar compressed files. That means faster queries and materially lower spend with no change to business logic. If your lake is still mostly C-S-V, that's usually the first optimization to do.

---

**[HOST — voice: nova]**

And partitioning is the second big lever, right? How should teams design it?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... partitioning should mirror how analysts filter in real queries, usually by date and sometimes by region or tenant. If the predicate includes the partition key, Athena prunes entire folder ranges before scanning files, which can cut scan volume dramatically. If the query forgets the partition filter, partitioning gives almost no benefit and cost spikes back up. Partition projection can help at scale by avoiding heavy catalog partition registration overhead for predictable key ranges. The practical rule is simple: choose partitions you will filter on, enforce those filters in query patterns, and monitor for full-scan regressions.

---

**[HOST — voice: nova]**

Let's talk money directly. Five dollars per terabyte sounds cheap, but where do teams still get burned?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... a team runs exploratory SELECT star queries on raw event C-S-V and accidentally scans one terabyte per query, so each run costs about five dollars. Do that a few hundred times during investigation week and costs jump fast with little business value. The winning playbook is first convert to Parquet, second partition correctly, third avoid SELECT star, and fourth materialize heavy logic with C-T-A-S for repeated use. Also set workgroup scan limits and alerts so runaway analyst queries fail early instead of burning budget silently. Even small query hygiene changes can produce NINETY percent scan reduction in active environments. Athena is cheap when used intentionally, expensive when query discipline is weak.

---

**[HOST — voice: nova]**

I hear C-T-A-S constantly. Where does it fit versus regular inserts?

---

**[SEAN — voice: onyx]**

Two things matter here... C-T-A-S is the fastest way to create a new optimized table from an existing query result, especially for converting raw data to Parquet. You define format and partitioning in the WITH clause, then write a single select statement to materialize output. INSERT INTO is better when appending to an existing table structure and lifecycle. Many pipelines use C-T-A-S for initial shaping, then INSERT INTO for incremental loads. Just remember to set partitioning explicitly during C-T-A-S, because defaults may not match your query strategy.

---

**[HOST — voice: nova]**

Where does the Glue Data Catalog fit operationally, and what should we be careful about?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... the catalog is shared metadata infrastructure, not just a convenience feature for one query tool. Athena depends on it for schema and table location, and other services like E-M-R and some warehouse integrations can depend on those same definitions. Crawlers are useful to bootstrap quickly, but production teams usually move to explicit D-D-L in code so schema changes are reviewable and reproducible. It's smart to version table definitions in source control and promote them through environments the same way you promote application code. Schema evolution is easiest for additive columns, while type rewrites often require data rewrite plans. Treat catalog changes like contract changes, because downstream consumers can break if they are unmanaged.

---

**[HOST — voice: nova]**

Federated queries sound powerful. When are they useful, and when are they risky?

---

**[SEAN — voice: onyx]**

So... basically... federated queries let Athena reach external systems through connector functions, commonly implemented with Lambda, so you can join lake data with operational sources. That's useful for one-off enrichment or investigative analysis when building a full E-T-L pipeline would be overkill. The risk is accidental broad pulls from source systems when predicates aren't pushed down effectively. That can hurt both query latency and source database performance. Use federated mode with tight filters, explicit limits, and a clear decision point for when repeated access should become a modeled ingestion pipeline instead.

---

**[HOST — voice: nova]**

Rapid-fire round. What's the single biggest thing you can do to reduce Athena costs?

---

**[SEAN — voice: onyx]**

Here's the thing... convert source datasets to columnar Parquet with compression before heavy analysis. That one move usually cuts scanned bytes more than any other single tactic. Then pair it with partition filters so the engine reads only relevant slices. Cost follows scan volume, so structural storage decisions are the highest-impact optimization.

---

**[HOST — voice: nova]**

What's the difference between Athena and Redshift Spectrum?

---

**[SEAN — voice: onyx]**

Here's the key insight... Athena is a fully serverless query service where you submit S-Q-L and pay per scan with no cluster ownership. Redshift Spectrum is an extension of Redshift that queries external S-3 data from within a Redshift environment, typically alongside warehouse tables. If your center of gravity is ad-hoc lake querying, Athena is often simpler. If your center of gravity is a managed warehouse with high-concurrency dashboards plus external lake joins, Spectrum can be the better fit.

---

**[HOST — voice: nova]**

You have a date-partitioned table, but your query still scans ten terabytes. What's probably wrong?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... either the query missed the partition predicate, or the predicate wasn't written in a form the optimizer can use for pruning. Another common issue is partition metadata drift where newly arrived folders were not registered or projected correctly. I would first inspect query text, then bytes-scanned metrics, then partition state in catalog metadata. Most of the time it's a filter-shape issue, not an engine failure.

---

**[HOST — voice: nova]**

How do you add new columns safely without breaking existing Athena users?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... add columns at the end of schema definitions, keep existing column order stable, and communicate changes as versioned contracts. Existing queries that select known columns continue working, while new consumers can adopt additional fields when ready. For risky type changes, create a new table version rather than mutating in place. Controlled additive evolution is the safest path in shared analytics environments.

---

**[HOST — voice: nova]**

Last one. For a nightly four-hour pipeline, when would you pick C-T-A-S over INSERT INTO?

---

**[SEAN — voice: onyx]**

Two things matter here... use C-T-A-S when you need to reshape and optimize large data in one pass, especially format conversion and fresh partition layout. Use INSERT INTO when your target table is already modeled and you're appending incremental slices. In nightly workflows, a common pattern is C-T-A-S for periodic compaction and model resets, with INSERT INTO for daily deltas. Choosing correctly keeps query speed stable and prevents storage fragmentation over time.

---

## END OF SCRIPT
