## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: Data Modeling for Data Engineers
Output filename: final_data-modeling.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\data-modeling\audio_script_data-modeling.md

---

**[HOST — voice: nova]**

Let’s start simple. What is data modeling, and why does it matter so much for a Senior Data Engineer?

---

**[SEAN — voice: onyx]**

So... basically... data modeling is the way you structure your data so it can be stored, queried, and trusted at scale. It’s not cosmetic — the wrong model makes EVERY query slow and EVERY report wrong. You’re encoding business logic into tables, relationships, and keys. If you get that wrong, no amount of tuning or indexing will save you later. At senior level, this is about making decisions that last years, not just getting a query to run today.

---

**[HOST — voice: nova]**

Got it. Let’s talk about the most common pattern — the star schema. What’s going on there?

---

**[SEAN — voice: onyx]**

Here’s the key insight... a star schema separates facts from dimensions. Fact tables store measurable events — like orders or clicks — and dimension tables store descriptive context like customer, product, or time. You connect them with foreign keys, and that gives you clean, predictable joins. It’s intentionally denormalized, so queries are simpler and faster — you trade some storage duplication for performance and clarity.

---

**[HOST — voice: nova]**

And how does that compare to a snowflake schema?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... snowflake schema normalizes the dimensions further. Instead of one wide dimension table, you break it into smaller related tables — like splitting customer into customer, geography, and segment. That reduces storage and enforces consistency, but it adds more joins. At scale, those extra joins can hurt performance, so you only snowflake when the normalization benefit is worth the complexity.

---

**[HOST — voice: nova]**

Makes sense. Let’s zoom into fact tables — there are different types, right?

---

**[SEAN — voice: onyx]**

Two things matter here... the type of fact table defines how you capture time and change. Transaction facts are one row per event — like one order per row. Periodic snapshots are one row per interval — like daily account balances. Accumulating snapshots track a process lifecycle — like order placed, shipped, delivered in a single row. Picking the wrong type leads to awkward queries and incorrect aggregations later.

---

**[HOST — voice: nova]**

You mentioned earlier that grain is critical. Why is that such a big deal?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... grain is the exact meaning of one row in your fact table. If you don’t define it explicitly, your data becomes ambiguous. For example, is a row one order, one order line, or one customer-day? That decision drives everything — joins, aggregations, even business metrics. Get the grain wrong, and you permanently break downstream reporting.

---

**[HOST — voice: nova]**

Let’s move to dimensions. What are the key design choices there?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... dimensions should almost always use surrogate keys — artificial IDs — instead of natural keys from source systems. That gives you stability even when source systems change. You also want conformed dimensions — shared dimensions like customer or date used across multiple fact tables. That’s what allows consistent reporting across the business. Without conformed dimensions, every team ends up with different numbers for the same metric.

---

**[HOST — voice: nova]**

And that ties into slowly changing dimensions, right?

---

**[SEAN — voice: onyx]**

Here’s the thing... slowly changing dimensions control how you track history. Type one overwrites data — no history. Type two creates a new row for every change with valid-from and valid-to timestamps. Type three keeps only current and previous values. The choice depends on whether historical accuracy matters — and in analytics, it usually does.

---

**[HOST — voice: nova]**

How does Type two actually work in practice?

---

**[SEAN — voice: onyx]**

So... basically... Type two uses surrogate keys plus versioning fields. When a change is detected, you expire the old row and insert a new one with updated values. You track an is-current flag and date ranges to know which version applies at a given time. This is usually implemented with a MERGE pattern to detect changes and apply inserts and updates. It’s more complex, but it preserves historical truth.

---

**[HOST — voice: nova]**

Let’s switch gears — when would you use a one big table instead?

---

**[SEAN — voice: onyx]**

Here’s the key insight... one big table is full denormalization — everything flattened into a single wide table. It’s great for BI tools and fast queries because there are ZERO joins. But you lose flexibility, and updates become harder. It’s a tradeoff — performance versus maintainability. At scale, you often build OBTs on top of a well-modeled warehouse.

---

**[HOST — voice: nova]**

And where does data vault fit into all of this?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... data vault is designed for flexibility and auditability, not query simplicity. You split data into hubs for business keys, links for relationships, and satellites for attributes. It’s great for ingesting messy, changing source systems without breaking history. But it’s not analyst-friendly — you usually transform it into star schemas for consumption. Think of it as a staging architecture, not a reporting one.

---

**[HOST — voice: nova]**

What about modeling for streaming systems?

---

**[SEAN — voice: onyx]**

Two things matter here... streaming forces you to think in events versus state. Event tables are append-only — every action is a new row. State tables represent the latest view — often updated or compacted. At scale, you usually keep both — events for history and replay, state for fast queries. Designing this wrong leads to duplicate processing or inconsistent state.

---

**[HOST — voice: nova]**

Before we wrap, what are the biggest mistakes you see?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... the biggest mistake is joining fact to fact — that almost always creates duplication and wrong metrics. Second, not defining grain clearly — that breaks everything downstream. Third, misusing surrogate keys or not handling late-arriving dimensions correctly. And finally, over-normalizing or over-denormalizing without understanding the tradeoffs. At senior level, you’re expected to avoid these by design, not fix them later.

---

**[HOST — voice: nova]**

Let’s do a quick rapid-fire round.

---

**[SEAN — voice: onyx]**

Let’s go.

---

**[HOST — voice: nova]**

When would you choose star over snowflake?

---

**[SEAN — voice: onyx]**

Choose star when query performance and simplicity matter most, especially for analytics and dashboards. It reduces joins and is easier for analysts to understand. Snowflake only makes sense when dimension normalization significantly reduces redundancy or enforces critical consistency. In most modern warehouses, storage is cheap, so star wins more often.

---

**[HOST — voice: nova]**

What’s the most important question to ask before creating a fact table?

---

**[SEAN — voice: onyx]**

Define the grain clearly before anything else. Ask what one row represents in exact business terms. Then validate how that grain supports downstream queries. If the grain is wrong, everything built on top will be wrong. This is the foundation of the model.

---

**[HOST — voice: nova]**

When is Type one SCD acceptable?

---

**[SEAN — voice: onyx]**

Type one is acceptable when historical changes don’t matter — like correcting typos or non-analytical attributes. It simplifies storage and queries because there’s only one version of the data. But you lose history completely. Use it carefully and intentionally.

---

**[HOST — voice: nova]**

Why are fact-to-fact joins dangerous?

---

**[SEAN — voice: onyx]**

Fact-to-fact joins multiply rows because both sides contain many-to-many relationships. That leads to inflated metrics and incorrect aggregations. You lose control of the grain. Instead, join facts through shared dimensions to maintain consistency. This is a fundamental modeling rule.

---

**[HOST — voice: nova]**

When would you use a one big table?

---

**[SEAN — voice: onyx]**

Use a one big table when you need fast, simple queries for BI tools and can tolerate redundancy. It’s ideal for dashboards and reporting layers. But it shouldn’t be your source of truth. Build it from a well-modeled warehouse to avoid losing flexibility.

---

## END OF SCRIPT