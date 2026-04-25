# Audio Script — Interview Master: Full Mock Interview Prep
# Slug: interview-master
# HOST voice: nova | SEAN voice: onyx
# Chunk target: ~750 chars

---

**[HOST — voice: nova]**
This session is your full interview prep — the elevator pitch, career story, behavioral answers, technical depth, project walkthroughs, and the questions you ask back. Sean, let's start with the thirty-second pitch. Someone asks: who are you?

**[SEAN — voice: onyx]**
I'm Sean Girgis — a Senior Data Engineer with twenty-plus years of enterprise experience. Most recently I spent eight years at Citigroup building production-grade data pipelines: E-T-L at scale, M-L-driven capacity forecasting, and a hybrid A-W-S and Oracle data platform. I'm based in the Dallas–Fort Worth area, I'm a U-S citizen with no sponsorship requirement, and I'm looking for a senior data engineering or cloud data platform role where I can bring the full stack — Python, Py-Spark, A-W-S, and the A-I and M-L capabilities I've been building alongside my core engineering work.

**[HOST — voice: nova]**
Good. Now the two-minute version for a hiring manager. Walk me through your background.

**[SEAN — voice: onyx]**
I started in software development in nineteen ninety-nine — C-plus-plus, multithreaded systems, Oracle databases. Six years at Corpus Inc. supporting Sprint's billing infrastructure — processing telecom billing at a scale comparable to VISA's transaction volume. After that I spent time at Sabre: a migration of a high-throughput shopping engine from two hundred-plus My-S-Q-L nodes to a six-node Oracle R-A-C cluster, reducing the hardware footprint by ninety-five percent while maintaining sub-second query latency. Then five years at C-A Technologies as an S-M-E for C-A A-P-M at TIAA-CREF — fifty-plus Enterprise Managers, four thousand to six thousand instrumented agents — that's where I moved from building systems to building intelligence about systems.

**[SEAN — voice: onyx]**
Then G6 Hospitality — a performance engineering role where I built the extraction pipeline from Dynatrace AppMon, segmented performance by geography and device, and produced analytics that drove frontend optimization recommendations for brand-dot-com. Then eight years at Citigroup. I built Python and Pandas E-T-L pipelines ingesting P-ninety-five telemetry from sixty-five thousand-plus endpoints. I designed an M-L forecasting layer that predicted infrastructure capacity bottlenecks six months ahead using Prophet and scikit-learn. I built the hybrid A-W-S and Oracle platform. And I built the analytics layer on top — Streamlit and Plotly dashboards used by senior stakeholders. I left Citigroup at the end of twenty twenty-five with everything I set out to build there delivered.

**[HOST — voice: nova]**
Why did you leave, and why are you looking now?

**[SEAN — voice: onyx]**
Eight years is a long run and I'm proud of what I built. The honest answer is the role had reached its natural ceiling within the capacity planning function. I'd built the E-T-L pipeline, the M-L forecasting layer, the A-W-S migration, the dashboards — and the team's mandate didn't have room to go further into the modern data stack. There was no path to Databricks, dbt, or event-driven architectures. I left on my own terms and immediately started building: HorizonScale to deepen my M-L and Py-Spark work, an A-I job search pipeline to get hands-on with L-L-M A-P-Is, and self-study on Delta Lake and dbt. I'm looking for a role where data engineering is a first-class function, not a support function embedded in an infrastructure team.

**[HOST — voice: nova]**
Tell me about a time you turned a slow manual process into an automated system.

**[SEAN — voice: onyx]**
The monthly capacity planning report at Citi. The team would extract P-ninety-five telemetry from B-M-C TrueSight across sixty-five thousand-plus endpoints, manually divide it by region and system type in Excel, enrich it by hand from the C-M-D-B and AppDynamics, apply safety and ceiling factors using spreadsheet formulas, and publish reports to enterprise teams. That process took five to ten business days every single month. My task was clear: replace the entire manual workflow with a pipeline that produced the same deliverables — same format, same structure — but automatically and reliably.

**[SEAN — voice: onyx]**
I built a Python E-T-L pipeline end to end. Extraction queried Oracle databases directly via S-Q-L-Alchemy and cx-Oracle — no manual exports. Pandas for transformation, NumPy for vectorized safety and ceiling calculations across sixty-five thousand-plus rows. The hardest part was cross-system identifier normalization — three enterprise source systems with independent naming conventions for the same endpoints. I built normalization rules to produce a canonical hostname key and a priority-order enrichment join with fallback. Dual S-Q-Lite architecture: monthly databases for per-period detail, a master database for multi-month progression tracking. openpyxl generated the Excel workbooks automatically. Version-controlled in GitLab. The reports that took five to ten days were produced in the first or second hour after the monthly data was available.

**[HOST — voice: nova]**
Tell me about a project you built from scratch with real business impact.

**[SEAN — voice: onyx]**
The capacity forecasting M-L system at Citi. The team had good historical data but all analysis was backward-looking — here's what happened last month. Teams only found out their infrastructure was approaching capacity when it was already close to the limit, leaving little time to respond. At a bank, capacity failures have regulatory implications. I set out to build a forecasting system that predicted infrastructure capacity six months ahead with enough reliability to drive procurement and architecture decisions. I built the M-L layer using Prophet in logistic growth mode — constraining forecasts between zero and one hundred percent utilization because a linear model will forecast one hundred and ten percent C-P-U, which is meaningless. The system achieved ninety-plus percent forecast accuracy over the six-month window. In one case, a memory trend that looked like a capacity problem turned out to be a memory leak — the early warning created time to fix the real problem rather than just provisioning more RAM.

**[HOST — voice: nova]**
Tell me about a time you influenced a technical decision without having direct authority.

**[SEAN — voice: onyx]**
At Citi, the capacity planning team had always operated on a manual Excel workflow. No mandate to change it — it worked, it was familiar, and people had processes built around it. I started by building the pipeline as a proof of concept, running it in parallel with the manual process for one monthly cycle. I presented the comparison side by side: the manual output took nine days, the pipeline took two hours. More importantly, I ran a diff between the two outputs and showed where they diverged — places where the manual process had applied factors inconsistently or missed enrichment data for some endpoints. The quality argument was as strong as the speed argument. The pipeline replaced the manual process, and that mental shift opened the door for the M-L forecasting work that came after.

**[HOST — voice: nova]**
What's the hardest technical problem you've ever solved?

**[SEAN — voice: onyx]**
The Sabre migration. A high-throughput shopping engine moving from two hundred-plus My-S-Q-L nodes to a six-node Oracle R-A-C cluster — transaction volume comparable to VISA, zero tolerance for data loss, sub-second latency required throughout the cutover. The core engineering problem: how do you validate that data from two hundred-plus nodes arrived intact when the transaction volumes are in the billions? I built a C-P-P-U-N-I-T testing framework in C-plus-plus with O-C-C-I and O-C-I that ran automated validation across millions of transaction records — row counts, hash-based checksums on key fields, spot-check queries on high-value transactions. Schema conversion was automated. C-plus-plus transaction processing code was optimized for the Oracle environment with O-C-C-I query patterns, connection pooling, and batch commit sizing. The migration completed with no data loss and no S-L-A breach. Ninety-five percent hardware reduction. The deep lesson: at that scale, you can't test correctness manually. That thinking shows up in everything I've built since — quality gates, validation pipelines, automated correctness checks.

**[HOST — voice: nova]**
Tell me about a failure and what you learned from it.

**[SEAN — voice: onyx]**
Early in the Citi pipeline work, I built a reporting pipeline that was producing outputs quickly — I was proud of the speed improvement. What I hadn't built was a robust validation layer. The pipeline completed successfully but silently produced incorrect output — the enrichment join had failed for a subset of records in a way that didn't raise an error, and reports went out with those records showing as unowned rather than flagged. The root cause was an edge case in the hostname normalization logic not covered by my test data. I rebuilt the validation layer completely: explicit row count checks at each stage, enrichment coverage rate tracking, a flag for any no-match record rather than silently including nulls, and an exit criteria check the pipeline had to pass before marking the run complete. The principle I apply now: a pipeline that completes without errors but produces wrong output is more dangerous than one that fails loudly. Silent success is not success.

**[HOST — voice: nova]**
Let's go technical. How do you approach designing a data pipeline from scratch?

**[SEAN — voice: onyx]**
I start with the output — what decision or product does this pipeline serve, and what does the consumer actually need? That drives everything backward: schema at the end, transformations that produce it, sources that provide the inputs, latency requirements for batch versus streaming. Then I define the data contract between stages. Each stage has an input schema and an output schema. I define those contracts explicitly before writing any transformation logic. This makes the pipeline modular — each stage can be tested, replaced, or rerun independently. Quality gates are non-negotiable: every stage has entrance criteria — validate input before processing — and exit criteria — validate output before passing downstream. And idempotency: every stage should be safe to rerun. Drop and recreate rather than append. The same input produces the same output every time regardless of how many runs have happened. This makes debugging practical — rerun any stage from the last known-good checkpoint with no fear of duplicates.

**[HOST — voice: nova]**
Batch versus streaming — how do you choose?

**[SEAN — voice: onyx]**
Start with the business latency requirement. If decisions need data that's seconds old — fraud detection, real-time pricing, operational alerting — streaming is required. If the decision horizon is hours or days — monthly capacity reports, daily analytics, weekly model refresh — batch is simpler, cheaper, and more reliable. Most of my production work has been batch. The Citi pipeline was monthly. HorizonScale is a monthly forecast cycle. The G6 performance analysis was weekly. In all of those, streaming would have added significant infrastructure and operational complexity with zero business benefit — the analysis wasn't consumed in real time. Where I'd choose streaming: anything where data value decays in minutes, where downstream systems need to react immediately, or where data volume makes periodic large batch loads impractical. For most analytics and reporting use cases, well-designed scheduled batch covers the need without the streaming overhead.

**[HOST — voice: nova]**
Walk me through how you'd design an A-W-S data lake for a large enterprise.

**[SEAN — voice: onyx]**
S3 as the storage foundation — cheap, durable, decoupled from compute. Medallion-style prefix structure: raw layer for data exactly as it arrived — never transform in place; silver layer for cleaned, validated, enriched data in Parquet with Snappy compression; gold layer for business-ready aggregates. Keep the layers separate so any layer can be reprocessed from the layer above without touching source data. Glue Data Catalog as the metastore — register all table schemas, partition information, and lineage. Athena for ad-hoc S-Q-L over S3, serverless, pay per query. Redshift for workloads that need consistent sub-second response. Step Functions or M-W-A-A Airflow for orchestration. I-A-M roles with least-privilege at every layer — Glue jobs get only the S3 prefixes they need, nothing else. And partition strategy: Parquet partitioned by date or region eliminates full-table scans. Small file consolidation to prevent the performance problem at scale.

**[HOST — voice: nova]**
You have eight thousand-plus time-series models to run. How do you parallelize that in Spark?

**[SEAN — voice: onyx]**
The Py-Spark Grouped Map U-D-F pattern. This is the right approach when you have a Python M-L function — like Prophet — that can't natively distribute across a Spark cluster but needs to run independently on each logical group in the data. Structure: group the data by host-I-D and resource, so each partition contains the complete time series for one host-resource pair. Define a Pandas U-D-F that receives a Pandas dataframe for one partition, runs the complete model fit, generates the forecast, and returns the results. Spark automatically distributes partitions across the worker fleet. No cross-partition communication, no shared state, no coordination overhead — embarrassingly parallel. One key operational detail: reduce Prophet's uncertainty-samples from one thousand to one hundred in the distributed version. The confidence interval accuracy degradation at fleet scale is negligible, but the throughput gain is ten-x. That single change makes the fleet-scale run tractable within a reasonable job window.

**[HOST — voice: nova]**
How does Facebook Prophet work and when would you choose it over SARIMA?

**[SEAN — voice: onyx]**
Prophet is a decomposable model — it separates the time series into a trend component, seasonality components at multiple frequencies via Fourier series, and holiday effects. It fits these via Stan's Bayesian inference, then combines them. Because it's decomposable, it handles missing data gracefully, it's robust to outliers, and the components are interpretable. I'd choose Prophet when the series has strong multi-frequency seasonality, when you need to incorporate known future events like holidays, or when you're running a model tournament across heterogeneous series and want a robust default that handles many patterns reasonably well. I use logistic growth mode rather than linear — that constrains the forecast physically between zero and one hundred percent utilization. SARIMA is better when the series has a single dominant seasonal period, the data is regular with no missing values, and you want a classical statistical model whose behavior is fully auditable. The champion-challenger tournament selects between them per series, which is the right approach when you have eight thousand heterogeneous series.

**[HOST — voice: nova]**
What is R-A-G and how does it work in a production pipeline?

**[SEAN — voice: onyx]**
R-A-G — Retrieval-Augmented Generation — grounds an L-L-M's response in retrieved documents rather than relying solely on the model's training knowledge. Embed a query and a document corpus using the same embedding model, retrieve the most semantically similar documents to the query, inject those documents into the prompt context, and ask the L-L-M to answer using that context. This lets you use a general-purpose L-L-M on proprietary or current data without fine-tuning. In my job search pipeline, the R-A-G pattern drives the job scoring stage. The master career profile is the retrieval corpus. The incoming job description is the query. The pipeline retrieves relevant profile sections, injects them alongside the job description into a structured prompt, and asks Grok to return a match score, skill gap analysis, and recommendation. The career profile is the hard boundary for what the L-L-M can say about experience — it can't invent accomplishments that aren't in the profile. The retrieval grounds the generation.

**[HOST — voice: nova]**
Let's do a quick pass on the four projects. Job Search Pipeline — what is it?

**[SEAN — voice: onyx]**
A ten-stage sequential pipeline where the input is a raw job posting and the output is a production-ready application package — tailored resume, cover letter, company research — tracked in a structured system. Stage zero runs a FAISS semantic duplicate check so I don't waste A-P-I credits on jobs already processed. Stage one uses R-A-G to score the posting against my career profile — first live run scored eighty-five percent on a Collective Health role. Stages three through five extract structured job data, generate a tailored J-SON resume grounded in the master profile, and render it to A-T-S-safe D-O-C-X. Stages six through eight run company research and generate a cover letter that references specific things about the company. Stage nine is a blocking quality gate before anything is marked as applied. Primary L-L-M is Grok — grok-three-mini for light tasks like scoring and parsing, grok-three for heavy generation that goes in front of a hiring manager.

**[HOST — voice: nova]**
HorizonScale — how does the model tournament work?

**[SEAN — voice: onyx]**
I use the first thirty-two months of data for training, hold out the most recent four months as a backtest window that no model sees during training, and then compare Prophet, SARIMA, and X-G-Boost on M-A-P-E — mean absolute percentage error — against those real held-out values. The model with the lowest M-A-P-E wins as champion for that specific host-resource pair. So different models win on different series — Prophet might win for a server with strong seasonal patterns, SARIMA wins on a server with a clean weekly cycle and low noise, X-G-Boost wins on trend-dominated series. Using a single global model means accepting poor forecast quality on the series where it doesn't fit — and those are often the CAPACITY-BREACH scenarios where accuracy matters most. The tournament adds engineering complexity but produces a risk report that is genuinely more trustworthy.

**[HOST — voice: nova]**
What are your three strongest technical areas — honestly?

**[SEAN — voice: onyx]**
First: production pipeline engineering. Twenty years of building systems that can't fail — telecom billing at Sprint, migration at Sabre, capacity intelligence at Citi. I think in terms of failure modes first, then correctness, then performance. Quality gates, idempotency, validation at every stage boundary — that discipline is deeply ingrained. Second: cross-system data integration. Most of my interesting work has involved joining data from multiple sources with incompatible identifiers, different update cadences, and inconsistent quality. Three enterprise source systems at Citi with independent naming conventions for the same sixty-five thousand endpoints. Making disparate systems speak to each other cleanly is where I've done some of my best work. Third: translating data into decisions. I think carefully about who consumes the output and what they actually need. The dashboards I build look the way they do because I've thought about the V-P who needs to act on this, not the data engineer who produced it.

**[HOST — voice: nova]**
What's a genuine weakness you're actively working on?

**[SEAN — voice: onyx]**
The modern lakehouse tooling gap is real and I'm honest about it. Databricks in production, dbt at enterprise scale, event streaming with Kafka or Kinesis — I have strong conceptual understanding and I've been actively studying and building with these tools, but I haven't shipped production systems with them yet. That's the honest assessment. What I'd push back on is treating that as a disqualifying gap. I have twenty-plus years of the underlying skills — Python, Py-Spark, S-Q-L, distributed systems, data modeling — and I've demonstrated across my career that I ramp quickly by mapping new tooling to what I already know rather than starting from zero. Glue and Py-Spark at Citi, Prophet and FAISS for HorizonScale, Grok and LangChain for the job search pipeline — each of those was new and I shipped production work on all of them. The Databricks and dbt gap is a three-to-six month gap with production access, not a foundational one.

**[HOST — voice: nova]**
Last section — the questions you ask back. What are your best ones?

**[SEAN — voice: onyx]**
I always ask at least three. First: what does the data engineering team own end-to-end — from raw ingestion to serving — and where does the boundary with data science or analytics engineering sit? That tells me whether I'd be building the full pipeline or just one slice of it. Second: what's the biggest data reliability or quality challenge you're dealing with right now? That shows me what I'd actually be working on, not what the job description says. Third: what would a successful first ninety days look like — what would they have shipped, what would they have learned? That tells me how the team thinks about onboarding and whether expectations are realistic. I also ask about pipeline observability — what does a data engineer know about whether their pipelines ran correctly last night — because the answer tells me immediately how mature the platform is. And I ask how A-I and M-L fit into the data team's roadmap, because that determines whether the work I'm most excited about is in scope or in a separate building I'll never walk into.

---
END OF SCRIPT
Voices: HOST (nova), SEAN (onyx)
Project: Interview Master — Full Mock Interview Prep
Slug: interview-master
