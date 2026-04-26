## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: AWS EventBridge
Output filename: final_aws-eventbridge.mp3
Script path: ..\jobsearch\data\interview_prep\audio_prep\aws-eventbridge\audio_script_aws-eventbridge.md

---

**[HOST — voice: nova]**

What is A-W-S EventBridge, and why does it matter for a Senior Data Engineer?

---

**[SEAN — voice: onyx]**

So... basically... EventBridge is a fully managed event bus that lets you route events between services, systems, and accounts without tight coupling. It’s how you build event-driven architectures in A-W-S where producers emit events and consumers react asynchronously. For a Senior Data Engineer, this matters because it replaces brittle pipeline triggers with decoupled, scalable workflows. Instead of chaining jobs manually, you let events drive orchestration. That becomes critical at scale where coordination overhead becomes the bottleneck.

---

**[HOST — voice: nova]**

Got it. Walk me through the different event bus types.

---

**[SEAN — voice: onyx]**

Here's the key insight... there are three main buses: default, custom, and partner. The default bus automatically receives events from A-W-S services like S-3 or Lambda. Custom buses are what you define for your own application domains — for example, a data platform bus for ingestion events. Partner buses integrate SaaS providers like Zendesk or Datadog. The senior-level decision is isolation — you separate domains using custom buses to avoid noisy neighbors and enforce governance boundaries.

---

**[HOST — voice: nova]**

And how do rules and event patterns actually match events?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... EventBridge uses JSON-based pattern matching on event fields like source, detail-type, and payload structure. Rules filter events and route them to targets. The pitfall is that matching is exact unless you explicitly use prefixes or wildcards. Another common issue is schema drift — if your event shape changes, rules silently stop matching. At scale, you need schema versioning and validation, otherwise pipelines fail invisibly.

---

**[HOST — voice: nova]**

Makes sense. What about scheduling — EventBridge Scheduler versus classic cron rules?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... classic EventBridge rules support cron and rate expressions but are limited in scale and flexibility. EventBridge Scheduler is a newer service designed for high-scale, one-time or recurring schedules with better reliability guarantees. It supports millions of schedules and fine-grained retry controls. For data engineering, Scheduler is better for orchestrating batch jobs or backfills. The key is choosing Scheduler when you need scale and control, not just simple cron triggers.

---

**[HOST — voice: nova]**

Let’s talk targets and fan-out patterns.

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... one event can trigger multiple targets like Lambda, Step Functions, S-Q-S, S-N-S, or even external A-P-Is. That’s fan-out. You might emit a “data-ingested” event that triggers validation, enrichment, and downstream analytics in parallel. The tradeoff is observability — once you fan out, tracing becomes harder. So you need correlation IDs and structured logging to track the full event lifecycle.

---

**[HOST — voice: nova]**

How does cross-account and cross-region routing work?

---

**[SEAN — voice: onyx]**

Two things matter here... permissions and architecture. EventBridge supports sending events across accounts using resource policies on the event bus. Cross-region routing is supported but adds latency. In multi-account data platforms, you often centralize ingestion in one account and distribute events outward. The key is designing for least privilege — only allow specific producers and consumers, not broad access.

---

**[HOST — voice: nova]**

What about reliability guarantees?

---

**[SEAN — voice: onyx]**

Here's the thing... EventBridge provides at-least-once delivery. That means duplicates are possible — ALWAYS assume idempotency. It retries failed deliveries with exponential backoff and supports dead-letter queues. If your target fails, the event can be sent to an S-Q-S DLQ for later processing. Senior engineers design consumers to be idempotent and resilient, otherwise duplicates corrupt downstream datasets.

---

**[HOST — voice: nova]**

And security and governance?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... security is enforced through I-A-M policies and event bus resource policies. You control who can put events and who can consume them. Governance comes from isolating buses, tagging resources, and auditing via Cloud-Trail. The principle is ZERO standing permissions — only grant access where absolutely needed. Otherwise, you risk unauthorized event injection.

---

**[HOST — voice: nova]**

How do you handle observability and troubleshooting?

---

**[SEAN — voice: onyx]**

Here's the key insight... EventBridge itself is stateless, so observability comes from integrations. You use Cloud-Watch metrics for rule invocations and failures, and logs from targets. The tricky part is debugging dropped events — often it’s pattern mismatch or permission issues. Senior engineers add event replay mechanisms and schema registries to validate events before they hit production.

---

**[HOST — voice: nova]**

What about cost and scaling tradeoffs?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... you pay per event published and per matched rule. At high volume, fan-out multiplies cost quickly. Compared to S-Q-S or Kinesis, EventBridge is more expensive but simpler. The tradeoff is operational overhead versus cost. For high-throughput streaming, you might use Kinesis. For orchestration and integration, EventBridge is the better choice.

---

**[HOST — voice: nova]**

What are common mistakes engineers make?

---

**[SEAN — voice: onyx]**

So... basically... first, ignoring idempotency and getting duplicate processing issues. Second, overly broad event patterns that match unintended events. Third, not versioning schemas, which breaks consumers silently. Fourth, using the default bus for everything instead of isolating domains. And finally, underestimating observability — without tracing, debugging becomes extremely painful.

---

**[HOST — voice: nova]**

Let’s do a quick rapid-fire round.

---

**[SEAN — voice: onyx]**

Let’s go.

---

**[HOST — voice: nova]**

When would you NOT use EventBridge?

---

**[SEAN — voice: onyx]**

When you need ultra-high throughput streaming, like real-time analytics pipelines, Kinesis or Kafka is better. EventBridge isn’t optimized for sustained high-volume data streams. It’s better for event routing and orchestration. Also, if you need strict ordering guarantees, EventBridge isn’t the right fit.

---

**[HOST — voice: nova]**

How do you ensure idempotency?

---

**[SEAN — voice: onyx]**

Use unique event IDs and store processed IDs in a database or cache. Design consumers so repeated processing produces the same result. Avoid side effects without checks. Idempotency is critical because delivery is at-least-once.

---

**[HOST — voice: nova]**

Biggest interview gotcha?

---

**[SEAN — voice: onyx]**

Candidates often forget that event patterns must match EXACT structure. Even small schema changes break rules. Another gotcha is assuming exactly-once delivery. Senior candidates always mention idempotency and DLQs.

---

**[HOST — voice: nova]**

Default bus versus custom bus?

---

**[SEAN — voice: onyx]**

Default bus is for A-W-S service events. Custom buses are for application-specific events. Use custom buses for isolation and governance. Never overload the default bus for everything.

---

**[HOST — voice: nova]**

EventBridge versus S-Q-S?

---

**[SEAN — voice: onyx]**

EventBridge is for routing and fan-out. S-Q-S is for queuing and buffering. EventBridge doesn’t store messages long-term like S-Q-S. Often, you use both together in a pipeline.

---

## END OF SCRIPT