## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: Apache Parquet for Data Engineers
Output filename: final_parquet.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\parquet\audio_script_parquet.md

---

**[HOST — voice: nova]**

Let’s start simple. What is Apache Parquet, and why does it matter so much for a Senior Data Engineer?

---

**[SEAN — voice: onyx]**

So... basically... Parquet is a columnar storage format designed for analytics workloads, especially on distributed systems like Pie-Spark or query engines over S-3. Instead of storing rows sequentially like C-S-V or J-S-O-N, it stores data column by column, which dramatically reduces how much data you actually read during queries. At scale, that means faster queries and significantly lower I-O costs, which is often the biggest bottleneck in data systems. For a Senior Data Engineer, it’s not optional — Parquet is the default format for any serious analytical pipeline.

---

**[HOST — voice: nova]**

Got it. So why is columnar storage such a big deal compared to row-based formats?

---

**[SEAN — voice: onyx]**

Here’s the key insight... row-based formats force you to read every column even if you only need one or two, which becomes incredibly wasteful for wide tables. Columnar formats like Parquet let you read only the columns referenced in the query, which is called column pruning. That reduces disk I-O by orders of magnitude when you’re working with hundreds of columns. At terabyte scale, that’s the difference between seconds and minutes — or between feasible and impossible.

---

**[HOST — voice: nova]**

Makes sense. Let’s go deeper — how is a Parquet file actually structured internally?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... Parquet has a three-level structure: row groups, column chunks, and pages. Row groups are horizontal slices of the dataset, which allows parallel processing across chunks of data. Inside each row group, each column is stored separately as a column chunk, which enables column pruning. And within those chunks, pages store the actual encoded data, which is where compression and encoding kick in. That layered design is what enables both efficient reads and smart skipping of data.

---

**[HOST — voice: nova]**

And that ties into compression, right? How does Parquet handle that?

---

**[SEAN — voice: onyx]**

Two things matter here... compression in Parquet happens at the column level, not the file level, which is critical because different columns compress differently. Snappy is the default — fast and good enough for most workloads, especially for real-time queries. Gzip gives you higher compression but slower reads, so it’s better for archival data. Zstd is the modern sweet spot — better compression than Snappy with decent speed, so it’s increasingly preferred for cold storage layers.

---

**[HOST — voice: nova]**

Interesting. What about encoding — how is data actually stored inside those columns?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... encoding is different from compression — it reduces redundancy before compression even starts. Dictionary encoding replaces repeated values with small integer IDs, which is perfect for low-cardinality columns like region or status. Run-length encoding handles repeated sequences efficiently, and delta encoding works well for ordered numeric data like timestamps or IDs. The engine chooses the best encoding automatically per column, which is why Parquet performs so well without manual tuning.

---

**[HOST — voice: nova]**

So how does the engine decide what data to skip when querying?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... Parquet stores statistics like min, max, and null counts for each column in every row group. When you run a filter like WHERE region equals US, the engine checks those stats before reading the data. If the max value in a row group is below US, that entire block gets skipped — ZERO I-O. That’s called predicate pushdown, and it’s one of the biggest performance wins in modern data systems.

---

**[HOST — voice: nova]**

And column pruning works alongside that?

---

**[SEAN — voice: onyx]**

Here’s the thing... column pruning and predicate pushdown are complementary. Column pruning limits which columns are read, and predicate pushdown limits which row groups are read. So if you SELECT only two columns with a filter, you’re reading a tiny fraction of the file. That combination is why Parquet scales so well for analytical queries.

---

**[HOST — voice: nova]**

Let’s talk schema evolution. What’s safe and what’s risky?

---

**[SEAN — voice: onyx]**

So... basically... adding new nullable columns is safe because older files simply won’t have those columns, and readers can handle that. But removing or renaming columns is dangerous — it breaks downstream readers that expect that schema. Changing data types can also cause compatibility issues depending on the engine. A Senior Data Engineer always treats schema changes as versioned contracts, not casual edits.

---

**[HOST — voice: nova]**

How does Parquet compare to formats like C-S-V, Avro, or O-R-C?

---

**[SEAN — voice: onyx]**

Here’s the key insight... C-S-V has ZERO structure — no types, no compression, no pushdown — so it forces full scans every time, which is unacceptable at scale. Avro is row-based and better for streaming systems like Kafka because it supports schema evolution cleanly. Parquet is optimized for analytics with columnar storage. O-R-C is similar to Parquet but more tightly integrated with Hive — in practice, Parquet dominates in most modern stacks.

---

**[HOST — voice: nova]**

What about partitioning strategies on S-3?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... partitioning is about skipping entire folders before even touching files. You typically use hive-style partitioning like year equals twenty twenty four slash month equals zero one. Query engines use partition pruning to eliminate whole directories based on filters. But the key rule is low cardinality — don’t partition on high-cardinality columns like user IDs, or you’ll create millions of tiny folders.

---

**[HOST — voice: nova]**

That leads into the small file problem, right?

---

**[SEAN — voice: onyx]**

Two things matter here... too many small files kill performance because S-3 listing becomes slow and engines can’t parallelize efficiently. Instead of processing large chunks, you’re managing thousands of tiny tasks, which adds overhead. The solution is compaction — merging small files into larger ones using OPTIMIZE or scheduled jobs. This is a classic scaling issue that separates junior pipelines from production-grade systems.

---

**[HOST — voice: nova]**

Quickly — how does Parquet fit into Python workflows?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... Python typically uses libraries like pyarrow or fastparquet to read and write Parquet files. Pyarrow is more feature-rich and aligns closely with modern engines, while fastparquet is lighter but less powerful. Pandas integrates directly with both through read_parquet and to_parquet. In distributed systems, Pie-Spark handles Parquet natively, so Python becomes more of a control layer.

---

**[HOST — voice: nova]**

Before we wrap — what are the most common mistakes engineers make with Parquet?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... the biggest mistake is treating Parquet like a file format instead of a system design decision. People ignore partitioning strategy, leading to either huge scans or millions of files. Another mistake is poor schema evolution — breaking downstream jobs by renaming fields casually. And finally, not running compaction — letting small files accumulate until performance degrades massively.

---

**[HOST — voice: nova]**

Let’s do a quick rapid-fire round.

---

**[SEAN — voice: onyx]**

Let’s go.

---

**[HOST — voice: nova]**

Why is Parquet faster than C-S-V?

---

**[SEAN — voice: onyx]**

Parquet reads only the columns needed instead of scanning entire rows, which reduces I-O significantly. It also uses compression and encoding, which shrink data size further. C-S-V has no schema, so everything is parsed at runtime, which adds overhead. At scale, Parquet is dramatically faster.

---

**[HOST — voice: nova]**

What’s predicate pushdown in one sentence?

---

**[SEAN — voice: onyx]**

It’s applying filters at the storage layer so irrelevant data is skipped before being read. The engine uses stored statistics to decide which blocks to ignore. This avoids unnecessary disk I-O. It’s one of the biggest performance optimizations in analytics systems.

---

**[HOST — voice: nova]**

When would you choose Avro over Parquet?

---

**[SEAN — voice: onyx]**

Avro is better for row-based streaming systems where records are processed one at a time. It supports schema evolution more flexibly for evolving event streams. Parquet is optimized for batch analytics instead. So it depends on access pattern — streaming versus querying.

---

**[HOST — voice: nova]**

What’s the small file problem?

---

**[SEAN — voice: onyx]**

It’s when you have too many tiny Parquet files, which slows down listing, scheduling, and execution. Distributed engines lose efficiency because tasks become too granular. It increases overhead instead of throughput. Compaction is the standard fix.

---

**[HOST — voice: nova]**

What’s the number one design decision with Parquet?

---

**[SEAN — voice: onyx]**

Partitioning strategy. It determines how much data gets scanned for every query. A bad partition strategy can destroy performance even if everything else is correct. A good one enables massive pruning and efficiency.

---

## END OF SCRIPT