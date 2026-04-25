# Audio Script — Data Pipeline Architecture & Design
# Slug: pipeline-design
# HOST voice: nova | SEAN voice: onyx
# Chunk target: ~750 chars

---

**[HOST — voice: nova]**
Today we're going deep on something that separates senior data engineers from everyone else — how you actually think about designing a pipeline. Not which tools you pick, but the reasoning process behind the architecture. We're covering how to design from scratch, how to draw microservice boundaries, how to test properly, and a lot more. Sean, ready?

**[SEAN — voice: onyx]**
Ready. And honestly, this is the topic I wish someone had laid out clearly when I was coming up. The tendency is to jump straight to tools, and that's where most bad architectures start.

**[HOST — voice: nova]**
Let's start with the biggest mistake. Why is starting with a tool the wrong move?

**[SEAN — voice: onyx]**
Here's the thing — when you start with a tool, you're anchoring the design to a solution before you understand the problem. You end up with a Kafka pipeline serving a dashboard that only refreshes once a day, or a full Spark cluster for a job that could've been a Lambda function. The tool should be the last decision, not the first.

**[HOST — voice: nova]**
So what's the first question?

**[SEAN — voice: onyx]**
The consumer. Always. What does the downstream system actually need — how fresh does the data need to be, what format, what's the access pattern? That single question determines whether you need real-time streaming, micro-batch, or a nightly batch job. Everything upstream flows from that answer.

**[HOST — voice: nova]**
Walk me through the full process when you're designing a new pipeline from scratch.

**[SEAN — voice: onyx]**
The mental model I use is five steps. First, define the consumer contract — freshness, format, access pattern, and what happens to the business if data is wrong or late. Second, characterize the source — volume, velocity, does it emit deletes and updates, can it be replayed. Third, sketch the data model at each stage explicitly. Fourth — and this is the one most engineers skip — design for failure before the happy path. What retries when, where does bad data go, how does replay work. Fifth, only then do you choose compute.

**[HOST — voice: nova]**
That fourth step is interesting. Why design for failure first?

**[SEAN — voice: onyx]**
Because every pipeline will fail. Networks time out, instances get terminated, jobs hit memory limits. If you haven't designed the failure path upfront, you end up bolting on retry logic and dead letter queues after the fact — and it's always messier and less reliable than designing it in from the start. Failure handling isn't a feature, it's a constraint.

**[HOST — voice: nova]**
Let's talk about the batch versus streaming decision. How do you make that call?

**[SEAN — voice: onyx]**
The question I ask is — what is the actual business impact of data being five minutes stale versus fifteen minutes stale versus an hour stale? If the honest answer is "no real difference," then batch or micro-batch is the correct architecture. Streaming is a cost and complexity premium you pay for a latency requirement. And most pipelines that feel like they need real-time actually need near-real-time, which micro-batch handles just fine.

**[HOST — voice: nova]**
What makes streaming worth the cost when it actually is the right call?

**[SEAN — voice: onyx]**
Three situations. One — the consumer has a hard sub-minute freshness requirement that a business outcome depends on, like fraud detection or live inventory. Two — the source emits such high-volume events that you need to process per-event rather than batching. Three — you need stateful windowed aggregations over event-time streams. Outside those three, the operational overhead of streaming rarely justifies itself.

**[HOST — voice: nova]**
And the operational overhead is real?

**[SEAN — voice: onyx]**
Very real. Streaming architectures are harder to test, harder to debug, harder to backfill, and harder to replay than batch. When something goes wrong at two in the morning, a batch job is straightforward to reason about and rerun. A streaming pipeline with stateful operators and watermarks is a much more complex incident. That complexity needs to be earning its keep.

**[HOST — voice: nova]**
Let's go to idempotency. Why is it the first design constraint and not an afterthought?

**[SEAN — voice: onyx]**
What I've found in practice is that retrofitting idempotency is painful in a way that's hard to appreciate until you've done it. If you design a pipeline assuming it runs exactly once, and then it runs twice because of a retry, you get duplicated rows, inflated metrics, double-charged transactions. The damage can be invisible for days. Designing for idempotency upfront means any retry or rerun produces exactly the same correct output, no cleanup required.

**[HOST — voice: nova]**
What are the practical patterns for achieving it?

**[SEAN — voice: onyx]**
Four main patterns. The simplest for S3 batch jobs is overwrite partitioning — you always write to a deterministic prefix and overwrite it on rerun, so running it twice is the same as running it once. For databases you use MERGE or UPSERT on a primary key. For event processors you track an idempotency key — a hash of the input — and skip records you've already processed. And for streaming you use offset-based checkpointing so you always resume from exactly where you left off.

**[HOST — voice: nova]**
How do you actually test that a pipeline is idempotent?

**[SEAN — voice: onyx]**
The test is simple and should be in every test suite. Run the job, record the row count and a checksum of the output. Run the exact same job again with identical input. Assert that both numbers match. If they don't, the pipeline is not idempotent and you have a data correctness problem waiting to surface in production.

**[HOST — voice: nova]**
Now microservice boundaries. How do you decide where one service ends and another begins?

**[SEAN — voice: onyx]**
Three principles. Separate by rate of change — if ingestion logic and transformation logic evolve at different speeds, coupling them means every change to one triggers a joint deployment with the other. Separate by failure domain — a failure in an enrichment lookup shouldn't take down the core ingestion path. And separate by scale requirement — ingestion of high-volume events and query serving of low-volume results have completely different scaling characteristics and should scale independently.

**[HOST — voice: nova]**
Give me a concrete example of what a well-bounded data platform looks like.

**[SEAN — voice: onyx]**
The way I think about it, most data platforms need five distinct services. An ingestion service that reads from the source, validates, and writes raw data to S3 or a Kafka topic. A transformation service that applies business logic and produces processed output. A quality gate service that validates the output before it reaches consumers. A serving layer that exposes data via S-Q-L, A-P-I, or scheduled delivery. And an orchestrator that sequences and monitors — but contains zero business logic. Business logic in the orchestrator is one of the most common architectural mistakes I see.

**[HOST — voice: nova]**
What about the other extreme — too many services?

**[SEAN — voice: onyx]**
That's real too. Fine-grained micro-services create distributed system complexity without benefit. You end up with network hops, distributed tracing requirements, and coordination overhead for no gain. A monolithic pipeline that deploys as one unit is often the right answer for a small team or an early-stage data product. The goal is the right granularity, not the most services.

**[HOST — voice: nova]**
Let's talk about how services communicate. Sync versus async — when do you use each?

**[SEAN — voice: onyx]**
And that's actually one of the more nuanced decisions. Synchronous — REST, gRPC — is right when you need an immediate answer. Lookups, real-time validations, user-facing A-P-Is. The caller waits, and the design assumes the callee is available. Asynchronous — queues, event streams — is right when you need durability, fan-out, or independence between stages. The source doesn't need to wait for the transformation to finish, and the transformation doesn't need the serving layer to be healthy to write its output.

**[HOST — voice: nova]**
What's the hidden cost of going async everywhere?

**[SEAN — voice: onyx]**
Async patterns shift errors from immediate failures to deferred failures. With synchronous communication, if something breaks, you know right now. With async, a failure shows up in a dead letter queue or as rising consumer lag — and only if you're monitoring those things. The more asynchronous your architecture, the more you need to invest in observability. The two go together.

**[HOST — voice: nova]**
Data contracts. What is a data contract and why does it matter?

**[SEAN — voice: onyx]**
Here's what I've learned — most pipeline breakages don't come from hardware failures or bugs in the compute layer. They come from an upstream team changing a field name, removing a column, or changing what a timestamp means, and every downstream consumer breaks silently on the next run. A data contract is an explicit agreement between producer and consumers about schema, semantics, freshness, completeness, and uniqueness. Making it explicit is how you catch that field rename before it causes a production incident.

**[HOST — voice: nova]**
And schema evolution — backward versus forward compatibility?

**[SEAN — voice: onyx]**
Backward compatible means the new schema can still read data written with the old schema. Forward compatible means the old schema can still read data written with the new schema. The only change that's safe in both directions is adding an optional field with a default. Everything else — renaming a field, changing a type, making an optional field required — is a breaking change that requires consumer migration before the producer deploys. The expand-and-contract pattern is how you handle it safely: add the new field first, migrate consumers to use it, then remove the old one.

**[HOST — voice: nova]**
Testing. Walk me through how you test a data pipeline end to end.

**[SEAN — voice: onyx]**
The framework I use has five layers. Unit tests on pure transformation functions — no Spark dependency, runs in milliseconds on small DataFrames, catches logic bugs. Integration tests using mocked A-W-S services to validate that the job reads from source and writes correct output. Contract tests that validate the output schema and semantics match what consumers declared they need. End-to-end tests in a staging environment with a representative sample. And data quality tests that run in production after every single job.

**[HOST — voice: nova]**
How do you test something that runs on five hundred gigabytes of data?

**[SEAN — voice: onyx]**
The key insight is that you separate transformation logic from the Spark scaffolding. Transformation functions are pure functions — they take a DataFrame in and return a DataFrame out. You can test those against a hundred rows in a unit test with no cluster. What you're validating is correctness of business logic, handling of nulls, edge cases, type coercions. The scale-specific behavior — partition skew, shuffle correctness — you test in a staging environment with a sampled dataset, not in C-I.

**[HOST — voice: nova]**
What's the most dangerous kind of test failure?

**[SEAN — voice: onyx]**
The test that doesn't fail when it should. A pipeline that runs to completion and returns exit code zero, but the output data is wrong. This happens all the time — a source schema changed silently, a JOIN was on the wrong key, an idempotency failure doubled rows. The job looks healthy, the C-I pipeline is green, and bad data propagates to consumers for days. The only defense is data quality checks that run after every job and actually inspect the data — row counts, uniqueness, freshness, value ranges.

**[HOST — voice: nova]**
Let's cover observability and S-L-As. How do you know a pipeline is healthy?

**[SEAN — voice: onyx]**
Three signals. Metrics — records processed per minute, job duration, error rate, row count per partition. These tell you the pipeline is running. Consumer lag — for streaming pipelines, rising lag is a leading indicator of freshness S-L-O breach. It tells you the consumer is falling behind before the freshness target is actually missed. And data quality test results after each run — these tell you the output is correct, not just that the job ran. You need all three, because each catches a different failure mode.

**[HOST — voice: nova]**
What does a pipeline S-L-O actually look like?

**[SEAN — voice: onyx]**
Concrete and measurable. Something like: data in the serving layer is no more than fifteen minutes behind source. Row count for any partition is within two percent of the source count. The pipeline completes successfully ninety-nine point five percent of scheduled executions. For streaming: P ninety-nine processing time per event is under thirty seconds. The point is defining these before you build, not after. S-L-Os drive your monitoring thresholds, your retry design, and your alerting sensitivity.

**[HOST — voice: nova]**
Late-arriving data. How do you handle it in streaming?

**[SEAN — voice: onyx]**
The mechanism is watermarking. A watermark is a declaration that you've seen all events up to timestamp T. As new events arrive with later timestamps, the watermark advances. Events that arrive after the watermark for their window are considered late. You configure a grace period — say ten minutes — within which late events are still included in the correct window. Events later than the grace period are dropped or routed to a separate late-data sink for offline reconciliation.

**[HOST — voice: nova]**
And in batch?

**[SEAN — voice: onyx]**
Batch makes it simpler. The standard pattern is a lookback window — on every run, you reprocess the last N days rather than just today. Late-arriving records from three days ago get picked up on the next run automatically. The tradeoff is compute cost — you process N days of data instead of one — but the pipeline stays simple, correct, and easy to reason about. For most analytical workloads, this is the right tradeoff.

**[HOST — voice: nova]**
Backfill strategy. You need to reprocess two years of historical data. Walk me through how you do it without disrupting production.

**[SEAN — voice: onyx]**
The prerequisites first. Immutable raw source — the original data must still exist and be replayable. Idempotent writes — reprocessing any partition must overwrite cleanly without duplicates. Parameterized date range — the job must accept any arbitrary window, not just "today." Then the execution: I split it into monthly batches, not one two-year run. Each month writes to a staging prefix, runs the standard quality gate, and only after all months pass does an atomic swap promote the backfill to the production path.

**[HOST — voice: nova]**
Why monthly batches instead of one big job?

**[SEAN — voice: onyx]**
Two reasons. If a single month fails, I haven't lost all progress — I rerun that month and continue. And progress is concrete and trackable — I can tell stakeholders "we're through fourteen of twenty-four months" rather than watching a two-year job run for twelve hours with no visibility. The atomic swap at the end is critical — production stays untouched by the backfill until every partition has been validated.

**[HOST — voice: nova]**
Failure modes. How do you classify a failure and decide what to do with it?

**[SEAN — voice: onyx]**
The critical distinction is transient versus fatal. A transient failure is one that might succeed if you try again — network timeout, throttling, temporary service unavailability. The right response is exponential backoff with jitter, up to a maximum retry count. A fatal failure is one where retrying won't help — schema mismatch, permission denied, malformed record, source data missing. The right response is move it to a dead letter queue, alert, and do not retry. Retrying a fatal error wastes compute and delays the alert that should be waking someone up.

**[HOST — voice: nova]**
What about partial failures — some records succeed, some fail?

**[SEAN — voice: onyx]**
Route the failures to the D-L-Q and complete the successful batch. Don't block the whole batch on a few bad records. Then alert on D-L-Q depth — the threshold should be zero. Every record in the D-L-Q is a failure that needs investigation. And critically, have a replay mechanism ready. The D-L-Q is not a graveyard, it's a holding area for records you intend to fix and reprocess.

**[HOST — voice: nova]**
Build versus buy. How do you make that call?

**[SEAN — voice: onyx]**
The way I think about it is total cost of ownership over three years, not the sprint estimate. Building includes initial development time, operational runbooks, on-call burden, security patching, scaling incidents, and the opportunity cost of not building product features. Managed services shift that burden to the vendor at a cost premium. My default is: managed for undifferentiated infrastructure — queues, orchestrators, catalogs, monitoring — and custom for business logic that is genuinely ours. The closer a component is to raw infrastructure, the less likely building it yourself creates any competitive advantage.

**[HOST — voice: nova]**
When does build actually win?

**[SEAN — voice: onyx]**
A few real cases. Self-managed Kafka on E-C-2 when you need specific Kafka features that M-S-K doesn't expose, or when the cost math at extreme scale genuinely favors it. Custom P-y-Spark on E-M-R when Glue's worker types and D-P-U pricing becomes expensive relative to your compute needs. But even in those cases I've seen teams underestimate the ongoing operational cost. The question I always ask is — is this the kind of thing we want to be woken up at two in the morning to fix? If the answer is no, that's a strong signal toward managed.

**[HOST — voice: nova]**
Alright — rapid fire. I'll give you the interview questions. Keep your answers tight. Ready?

**[SEAN — voice: onyx]**
Let's go.

**[HOST — voice: nova]**
How do you start designing a new pipeline?

**[SEAN — voice: onyx]**
Consumer first. What S-L-A does the downstream system need, what format, what access pattern. Every upstream decision flows from that answer. Tool selection is last.

**[HOST — voice: nova]**
Batch or streaming?

**[SEAN — voice: onyx]**
Ask what the business impact of fifteen-minute stale data is versus one-hour stale. If there's no real difference, batch. Streaming is a cost you pay for a latency requirement. Most "real-time" needs are actually near-real-time, which micro-batch covers.

**[HOST — voice: nova]**
How do you test idempotency?

**[SEAN — voice: onyx]**
Run the job, checksum the output, run it again with identical input, assert the checksums match. If they differ, the pipeline is not idempotent.

**[HOST — voice: nova]**
A job completed successfully but data is wrong. How?

**[SEAN — voice: onyx]**
Silent schema change, wrong JOIN key, idempotency failure doubling rows, logic bug producing plausible but incorrect output. Exit code zero only proves the job ran. Data quality checks after every run are the only defense.

**[HOST — voice: nova]**
How do you draw a service boundary?

**[SEAN — voice: onyx]**
Separate by rate of change, failure domain, and scale requirement. A service should be independently deployable. If you can't deploy one without touching another, the boundary is in the wrong place.

**[HOST — voice: nova]**
How do you handle a breaking schema change?

**[SEAN — voice: onyx]**
Expand and contract. Add the new field while keeping the old one. Migrate consumers to the new field. Remove the old field only after all consumers have migrated. Never rename or remove a field without a migration window.

**[HOST — voice: nova]**
How do you backfill two years of data safely?

**[SEAN — voice: onyx]**
Monthly batches to a staging prefix. Validate each month with quality gates. Atomic swap to production only after all months pass. Never overwrite production in place during the backfill.

**[HOST — voice: nova]**
What belongs in a dead letter queue?

**[SEAN — voice: onyx]**
Records that failed after max retries and where retrying won't help — schema mismatches, malformed records, permission failures. Alert when depth is above zero. Every D-L-Q message needs investigation and a replay plan.

**[HOST — voice: nova]**
Build or buy for pipeline orchestration?

**[SEAN — voice: onyx]**
Almost always buy. Orchestration is a solved problem. Airflow, Step Functions, M-W-A-A — any of them are better than a custom scheduler. Save your engineering time for business logic that's actually yours.

**[HOST — voice: nova]**
What's the difference between a data S-L-A and a data S-L-O?

**[SEAN — voice: onyx]**
An S-L-A is a commitment to a consumer, usually with consequences if breached. An S-L-O is the internal target you set to stay safely ahead of the S-L-A. You monitor and alert on S-L-O breaches so you fix problems before they become S-L-A violations.

**[HOST — voice: nova]**
That's a wrap. Pipeline architecture, microservice design, testing, observability, backfill, failure handling — all in one session. The common thread across all of it is this: design for the consumer, design for failure, and design for correctness of the data — not just completion of the job.

**[SEAN — voice: onyx]**
And that last point is the one that separates the senior engineers I've learned the most from. They're not satisfied when the job is green. They ask — but is the data right?

---
END OF SCRIPT
Total sections: 14 topics + rapid-fire
Voices: HOST (nova), SEAN (onyx)
