## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: dbt for Data Engineers
Output filename: final_dbt.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\dbt\audio_script_dbt.md

---

**[HOST — voice: nova]**

Let’s start simple. What exactly is dbt, and why does it matter for a Senior Data Engineer?

---

**[SEAN — voice: onyx]**

So... basically... dbt is a transformation layer that runs inside your warehouse — it’s NOT an orchestrator, and it doesn’t do ingestion. It takes raw data that’s already landed — say from an E-T-L or E-L-T pipeline — and turns it into clean, analytics-ready models using S-Q-L. The key idea is pushing compute down to the warehouse, instead of pulling data out into external engines. For a senior engineer, this matters because it standardizes transformations, enforces lineage, and keeps logic version-controlled and testable. It’s really about making your warehouse the single source of truth, not your Python scripts.

---

**[HOST — voice: nova]**

Got it. So at the core, everything revolves around models — what are those in dbt?

---

**[SEAN — voice: onyx]**

Here’s the thing... a dbt model is just a S-Q-L SELECT statement saved as a file, and dbt turns that into a table or view in your warehouse. The magic comes from the ref function — it automatically builds dependencies between models, so you don’t hardcode table names. That gives you a DAG without writing orchestration logic. At scale, this is huge because ref ensures correct build order and enables lineage tracking. You’re essentially declaring transformations, not scripting them step by step.

---

**[HOST — voice: nova]**

And how does dbt decide whether something becomes a table or a view?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... that’s controlled by materializations. Views are the default — no storage, always recomputed. Tables are full rebuilds, which are expensive but stable. Incremental models only process new or changed data, which is where dbt really shines at scale. And ephemeral models don’t exist physically at all — they compile into C-T-Es inside downstream queries. Choosing the right materialization is a performance and cost decision — not just a convenience setting.

---

**[HOST — voice: nova]**

Let’s dig into incremental models — that’s where things get interesting, right?

---

**[SEAN — voice: onyx]**

Here’s the key insight... incremental models are how you avoid full table rebuilds on large datasets. You use an is_incremental filter to only process new rows — typically based on a timestamp or surrogate key. Then you define a unique_key so dbt can perform idempotent MERGE operations instead of blind inserts. There are strategies — append, merge, delete plus insert — and each has tradeoffs depending on update patterns. If you get this wrong, you either duplicate data or blow up compute costs.

---

**[HOST — voice: nova]**

Makes sense. What about sources and seeds — how do those fit in?

---

**[SEAN — voice: onyx]**

Two things matter here... sources define your upstream raw tables, and they let you add freshness checks — so you know if ingestion is lagging. Seeds are small static C-S-V files you load directly into the warehouse — think lookup tables or mappings. Together, they formalize both dynamic and static inputs into your transformation layer. For a senior engineer, the key is that everything is declared and versioned — no hidden dependencies. That’s what makes pipelines observable and reliable.

---

**[HOST — voice: nova]**

And testing — dbt has built-in tests, right?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... dbt tests are just S-Q-L assertions that run against your data. Built-ins like not_null, unique, accepted_values, and relationships catch common data quality issues. They run as part of your pipeline, so failures break the build — which is exactly what you want. You can also write custom tests — either one-off queries or reusable macros. This shifts data quality from dashboards into the pipeline itself, which is a very senior-level mindset.

---

**[HOST — voice: nova]**

Speaking of macros — what role do they play?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... macros are reusable Jinja-based S-Q-L snippets, so you don’t repeat logic across models. Think dynamic column generation, standardized filters, or reusable joins. You can also pull in community packages from dbt Hub to accelerate development. The real value is consistency — every model follows the same patterns without copy-paste drift. That’s critical when you’re managing hundreds of models across teams.

---

**[HOST — voice: nova]**

What about documentation and lineage — how does dbt help there?

---

**[SEAN — voice: onyx]**

Here’s the key insight... dbt automatically generates a DAG and documentation site from your models and metadata. You can describe tables and columns, and dbt docs serve gives you a browsable lineage graph. That means anyone can trace data from raw source to final metric. For large organizations, this is HUGE — it eliminates tribal knowledge. You’re essentially turning your warehouse into a self-documented system.

---

**[HOST — voice: nova]**

And how do teams typically run dbt — Core versus Cloud?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... dbt Core is just a C-L-I tool — you run it locally or in your own orchestration like Airflow. dbt Cloud is the managed version — it adds scheduling, C-I-C-D, and a UI. The tradeoff is control versus convenience. Senior engineers often start with Core for flexibility, then move to Cloud when governance and collaboration become pain points.

---

**[HOST — voice: nova]**

Let’s talk snapshots — especially S-C-D Type two patterns.

---

**[SEAN — voice: onyx]**

Here’s the thing... dbt snapshots handle S-C-D Type two by tracking changes over time. They create columns like dbt_valid_from and dbt_valid_to to represent record history. You define how changes are detected — either timestamp or check columns. This gives you historical tracking without writing complex merge logic yourself. It’s clean, declarative, and production-ready out of the box.

---

**[HOST — voice: nova]**

And orchestration — how does dbt fit with something like Airflow?

---

**[SEAN — voice: onyx]**

Two things matter here... dbt doesn’t orchestrate, so you plug it into tools like Airflow. You can trigger dbt runs using a Bash operator, or use something like Cosmos for tighter integration. In practice, Airflow handles scheduling and dependencies across systems, while dbt handles transformations inside the warehouse. Keeping those responsibilities separate is what scales cleanly.

---

**[HOST — voice: nova]**

Before we wrap — what are the most common mistakes you see?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... most issues come from misuse of incremental models. People forget partitioning or omit unique keys — which leads to duplicates or full scans. Another big one is overusing ephemeral models, which can create massive compiled queries. And teams sometimes treat dbt like an orchestrator, which it isn’t. At scale, these mistakes translate directly into cost and performance problems.

---

**[HOST — voice: nova]**

Let’s do a quick rapid-fire round.

---

**[SEAN — voice: onyx]**

Let’s go.

---

**[HOST — voice: nova]**

What does ref actually solve?

---

**[SEAN — voice: onyx]**

It handles dependency resolution and prevents hardcoding table names. It builds the DAG automatically based on model references. That ensures correct execution order every time. It also enables lineage tracking in documentation.

---

**[HOST — voice: nova]**

When should you use incremental over table?

---

**[SEAN — voice: onyx]**

Use incremental when data volume is large and only a subset changes each run. It reduces compute and runtime significantly. But it requires a reliable key or timestamp. Without that, correctness breaks.

---

**[HOST — voice: nova]**

What’s the risk of missing unique_key?

---

**[SEAN — voice: onyx]**

You’ll get duplicate records because merges can’t match existing rows. Over time, that corrupts your dataset. It’s one of the most common production bugs. Always define it for incremental models.

---

**[HOST — voice: nova]**

dbt versus Airflow — one line?

---

**[SEAN — voice: onyx]**

dbt transforms data, Airflow orchestrates workflows. They solve different layers of the pipeline. You almost always use them together. Mixing their responsibilities leads to poor design.

---

**[HOST — voice: nova]**

What separates a junior from a senior dbt user?

---

**[SEAN — voice: onyx]**

Seniors think in terms of data contracts, lineage, and cost — not just writing S-Q-L. They design incremental strategies carefully. They enforce testing and documentation. And they treat dbt as part of a larger system, not a standalone tool.

---

## END OF SCRIPT