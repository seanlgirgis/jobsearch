## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: SQL Patterns for Data Engineers
Output filename: final_sql-patterns.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\sql-patterns\audio_script_sql-patterns.md

---

**[HOST — voice: nova]**

Let's talk about S-Q-L patterns for data engineers. At senior level, this isn't about memorizing syntax, it's about using S-Q-L to make pipelines correct, explainable, and scalable. Why does this topic matter so much in interviews?

---

**[SEAN — voice: onyx]**

So... basically... S-Q-L is where a lot of data engineering truth gets exposed. A pipeline can look clean in Python or orchestration code, but the joins, deduping, history logic, and reconciliation usually land in S-Q-L. Interviewers use it to test whether you understand data shape, grain, correctness, and performance under volume. A senior answer explains the pattern, the tradeoff, and what can break when the table gets large.

---

**[HOST — voice: nova]**

Let's start with window functions. People know names like row number, rank, dense rank, lag, lead, and first value, but what are the real use cases?

---

**[SEAN — voice: onyx]**

Here's the thing... window functions let you compare a row to its neighbors without collapsing the result like a group by does. Row number is the classic dedupe pattern: keep the latest record per business key. Rank and dense rank are useful when ties matter, like finding top products per region where two products can share the same score. Lag and lead are for change detection, like comparing today's status to yesterday's status, while first value can pull the opening event in a customer journey or the first known state in a version chain.

---

**[HOST — voice: nova]**

Got it. What about partitioned frames like rows between and range between? That's where people often get fuzzy.

---

**[SEAN — voice: onyx]**

Here's the key insight... partitioning defines the group of rows, but the frame defines the subset inside that group used for each calculation. Rows between is physical row-based movement, so it's predictable for moving averages like the prior seven events. Range between is value-based, so it matters when the order column has meaning, like all events within a time or price range. The trap is that range can include multiple tied rows, so the result may surprise people if the ordering column isn't unique.

---

**[HOST — voice: nova]**

And that leads naturally to running totals and moving averages. How should a data engineer explain those cleanly?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... running totals answer, what have we accumulated up to this row, at this grain. Moving averages answer, what does the recent window look like around this row. For revenue by customer, a running sum over order date gives lifetime value progression; for telemetry, an average over the prior several readings smooths noisy metrics. The senior point is to order deterministically, define the frame explicitly, and make sure the partition matches the business question.

---

**[HOST — voice: nova]**

Let's shift to query structure. C-T-Es, subqueries, and temp tables can all express similar logic, so when do you use each?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... a C-T-E is great when I'm naming a logical step, like filtered orders, ranked customers, then final selection. A subquery is fine for compact logic, especially when it stays local to one join or filter. A temp table is better when the intermediate result is reused, expensive, or needs indexing and inspection during a batch process. The mistake is treating C-T-Es as automatically faster; depending on the engine, they may inline, materialize, or block optimization.

---

**[HOST — voice: nova]**

What about recursive C-T-Es? They sound academic, but where do they show up in real data work?

---

**[SEAN — voice: onyx]**

Two things matter here... recursive C-T-Es are for walking relationships where each row points to another row. Org charts, category trees, folder paths, and bill-of-material structures are common examples. The anchor query starts the tree, and the recursive query keeps joining child rows until there are no more. In production, I watch for cycles, depth limits, and whether the recursive query should be replaced by a precomputed hierarchy table.

---

**[HOST — voice: nova]**

Let's cover slowly changing dimensions. Can you compare Type one, Type two, and Type three without turning it into a warehouse lecture?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... each type answers a different history question. Type one overwrites the old value, so it gives you the current truth but loses history. Type two creates a new row with effective dates, current flag, and versioning, so facts can join to the correct historical dimension row. Type three stores current and previous values in the same row, which is simple but only preserves limited history.

---

**[HOST — voice: nova]**

Let's zoom into S-C-D Type two. What does the full M-E-R-G-E pattern need to do?

---

**[SEAN — voice: onyx]**

So... basically... Type two is not just an update, it's a controlled versioning workflow. You detect changed business attributes for the natural key, expire the current row by setting an end date and current flag to false, then insert a new row with a new surrogate key and a fresh effective start date. The fact table should join through the surrogate key or through the natural key plus effective date range, depending on the model. The senior gotcha is making the load idempotent, because rerunning the same batch should not create duplicate history rows.

---

**[HOST — voice: nova]**

Makes sense. Now compare incremental loads using M-E-R-G-E, upsert, and insert on conflict.

---

**[SEAN — voice: onyx]**

Here's the thing... incremental loading is about applying only what changed while preserving correctness. M-E-R-G-E is the general pattern: match existing rows, update changed rows, insert new rows, and sometimes delete or deactivate missing rows. Insert on conflict is a simpler upsert pattern, common in Postgre-S-Q-L, where a unique constraint decides whether to insert or update. The interview answer should mention keys, idempotency, late-arriving data, and audit columns like load timestamp and source batch id.

---

**[HOST — voice: nova]**

Deduplication is another classic. How do you describe the row number pattern?

---

**[SEAN — voice: onyx]**

Here's the key insight... dedupe only makes sense after you define the business key and the rule for which row wins. The pattern is row number over partition by the duplicate key, ordered by freshness, source priority, or ingestion timestamp. Then you keep row number equals one and quarantine or inspect the rest. A junior answer says remove duplicates; a senior answer asks, duplicate by what grain, and which record is authoritative?

---

**[HOST — voice: nova]**

Let's talk anti-joins. When you're finding rows in A that don't exist in B, do you prefer left join is null or not exists?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... both can express the same anti-join, but not exists is often clearer and safer around null behavior. Left join is null is common and readable when you're checking absence after a join, but you must make sure the null check is on the joined key from the right table. Performance depends on the optimizer, indexes, and data distribution. In interviews, I also call out not in as risky when the subquery can return nulls.

---

**[HOST — voice: nova]**

How about set operations: union, union all, intersect, and except?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... union all stacks datasets and keeps every row, so it's usually right for appending daily files or combining partitions. Union removes duplicates, which can be correct for a distinct business set, but it adds sorting or hashing cost. Intersect finds overlap, useful for reconciliation, and except finds records in one result that aren't in another. The senior move is choosing based on data meaning first, then understanding the performance cost of duplicate elimination.

---

**[HOST — voice: nova]**

Now performance. What should a data engineer look for when reading an explain plan?

---

**[SEAN — voice: onyx]**

Two things matter here... access path and join strategy. A sequential scan can be fine on a small table or when most rows qualify, but it can be painful when the filter is selective and an index exists. Index scans help selective lookups, hash joins are common for larger equality joins, and nested loops can be great for small outer inputs but dangerous when both sides are large. I also look at estimated versus actual row counts, because bad estimates often explain bad plans.

---

**[HOST — voice: nova]**

Let's bring in analytical functions for data engineering: percentiles, histograms, and cohort analysis. Where do those fit?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... analytics S-Q-L is often used to understand distributions, not just totals. Percentiles help with latency, spend, and metric outliers where averages hide the truth. Histograms bucket values so you can see shape, skew, and concentration. Cohort analysis groups users or entities by start period, then measures behavior over later periods, which is useful for retention, adoption, and pipeline quality trends.

---

**[HOST — voice: nova]**

What S-Q-L patterns do you use for data quality checks?

---

**[SEAN — voice: onyx]**

So... basically... data quality S-Q-L is about proving the load behaved the way you expected. I use reconciliation queries to compare source counts, target counts, sums, and key coverage. Null counts show required-field failures, duplicate detection validates grain, and anti-joins find missing relationships between tables. The senior habit is saving these checks as repeatable controls, not one-off queries pasted into a notebook.

---

**[HOST — voice: nova]**

Before rapid-fire, what are the common S-Q-L interview traps?

---

**[SEAN — voice: onyx]**

Here's the thing... nulls are the classic trap because they change comparisons, joins, and aggregations. Count star counts rows, while count column ignores nulls. Group by mistakes happen when people select columns that don't match the intended grain, or accidentally aggregate after a many-to-many join. I also watch for candidates who use distinct to hide join bugs instead of fixing the data model.

---

**[HOST — voice: nova]**

Let's do a quick rapid-fire round.

---

**[SEAN — voice: onyx]**

Let's go.

---

**[HOST — voice: nova]**

First question: when would you use rank instead of row number?

---

**[SEAN — voice: onyx]**

Use rank when ties are meaningful and should receive the same position. For example, if two products have the same sales amount, they can both be ranked first. Row number forces a single winner, which is better for dedupe. Dense rank is similar to rank, but it doesn't leave gaps after ties.

---

**[HOST — voice: nova]**

Second question: what's the safest dedupe pattern for a pipeline?

---

**[SEAN — voice: onyx]**

Define the business key first, then use row number over that key with a deterministic order. The order should include source priority, event timestamp, ingestion timestamp, and a tie-breaker if needed. Keep the winning row and persist rejected duplicates somewhere visible. Silent dedupe is dangerous because it can hide source system problems.

---

**[HOST — voice: nova]**

Third question: when is a temp table better than a C-T-E?

---

**[SEAN — voice: onyx]**

A temp table is better when the intermediate result is reused multiple times or expensive to compute. It's also useful when you need indexes, statistics, or debug visibility during a batch. A C-T-E is cleaner for readable, one-pass logical steps. The choice depends on engine behavior and workload shape.

---

**[HOST — voice: nova]**

Fourth question: why is not in risky for anti-joins?

---

**[SEAN — voice: onyx]**

Not in can behave unexpectedly when the subquery returns null. A single null can make the comparison unknown and cause results to disappear. Not exists avoids that trap and usually expresses the intent more clearly. Left join is null is also fine when written carefully.

---

**[HOST — voice: nova]**

Final question: what's the senior-level answer to count star versus count column?

---

**[SEAN — voice: onyx]**

Count star counts rows, regardless of nulls. Count column counts only rows where that column isn't null. For data quality, that difference is extremely useful because it tells you whether required fields are missing. In an interview, I tie it back to grain, null handling, and reconciliation.

---

## END OF SCRIPT
