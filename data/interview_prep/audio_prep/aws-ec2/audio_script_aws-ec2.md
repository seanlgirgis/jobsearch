## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: Amazon EC2
Output filename: final_aws-ec2.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md

---

**[HOST — voice: nova]**

Sean, let's talk about Amazon E-C-2. For a Senior Data Engineer, this isn't just, spin up a virtual machine. What is E-C-2 really, and why does it still matter in a world full of Lambda, Glue, Fargate, and managed services?

---

**[SEAN — voice: onyx]**

So... basically... Amazon E-C-2 is the raw compute layer of A-W-S. It's where you rent virtual servers, choose the size, choose the network placement, attach storage, assign permissions, and decide how much operational control you want.

For a Senior Data Engineer, E-C-2 matters because not every workload fits neatly into a managed box. Some jobs need custom libraries, long runtimes, local disks, heavy memory, special networking, or control over the operating system. That's where E-C-2 still wins.

The junior answer is, E-C-2 is a virtual machine. The senior answer is, E-C-2 is a compute decision surface. It forces decisions about cost model, failure recovery, storage persistence, scaling strategy, network isolation, bootstrap automation, and security boundaries.

In data engineering, I reach for E-C-2 when I need predictable heavyweight execution, custom runtime control, specialized hardware, or batch jobs that don't behave nicely inside serverless limits. Lambda is great for short event-driven work. Glue is great for managed Spark-style pipelines. Fargate is great for containerized services without managing hosts. But when the workload is big, weird, stateful, or needs deep host-level control, E-C-2 is still the grown-up tool.

---

**[HOST — voice: nova]**

Got it. So before we even talk pricing or storage, the first decision is the instance type. How should a data engineer think about E-C-2 instance families?

---

**[SEAN — voice: onyx]**

Here's the thing... instance families are A-W-S telling you what the hardware is optimized for. If you pick the wrong family, you can have a pipeline that's expensive and still slow.

Compute optimized instances are for workloads where C-P-U is the bottleneck. Think compression, encoding, distributed query workers, data transformation, or stateless services doing a lot of parallel compute. Memory optimized instances are for workloads where the working set needs to stay in RAM. That's common with Spark executors, Presto-style query engines, large joins, caching layers, and in-memory feature processing.

Storage optimized instances are for workloads that hammer local disk. They usually matter when you need very high local I-O, temporary shuffle space, log processing, or databases that benefit from fast attached storage. GPU optimized instances are for model training, inference, image processing, vector workloads, and anything where parallel numeric acceleration matters.

General purpose instances are fine when the workload is balanced or unknown. But at scale, balanced can become wasteful. A senior engineer watches the bottleneck. If C-P-U is saturated and memory is fine, go compute optimized. If memory pressure causes spills to disk, go memory optimized. If the job dies because shuffle disks are overloaded, storage optimized may beat just adding more average machines.

The key is that instance selection should come from metrics, not vibes. Cloud-Watch, application logs, Spark U-I metrics, disk throughput, and network saturation tell you what family you actually need.

---

**[HOST — voice: nova]**

Makes sense. Now pricing is where a lot of interview answers get shallow. Can you walk through On-Demand, Reserved Instances, Spot, and Savings Plans like you're making a real architecture choice?

---

**[SEAN — voice: onyx]**

Here's the key insight... E-C-2 pricing is about matching commitment to workload certainty. On-Demand is the default: no long-term commitment, highest flexibility, highest unit price. It's good for experiments, unpredictable workloads, urgent production fixes, and anything where you don't yet know the steady-state pattern.

Reserved Instances are a commitment to a specific instance configuration or family, usually for one year or three years. They can save money, but they're less flexible. They're best when you know you need a baseline fleet for a long time, like fixed query workers, monitoring nodes, or a stable platform service.

Savings Plans are usually more flexible. Instead of committing to a particular machine, you commit to spend a certain amount per hour. Compute Savings Plans can apply across instance family, size, region, and even some other compute services. For real teams, this is often easier to manage than guessing exact instance types.

Spot is the big lever for batch workloads. You can get deep discounts, sometimes dramatically cheaper than On-Demand, but A-W-S can reclaim the instance. That means Spot is excellent for fault-tolerant batch jobs, distributed processing, backfills, image generation, test environments, and queues where work can be retried.

The commitment math is simple in principle. Stable baseline goes under Savings Plans or Reserved Instances. Bursty uncertain work stays On-Demand. Interruptible batch uses Spot. The mistake is buying commitments for workloads you haven't measured. Measure first, commit second.

---

**[HOST — voice: nova]**

And that leads naturally into storage. E-C-2 has E-B-S and instance store, and they sound similar to beginners. What's the real difference?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... E-B-S is network-attached block storage that lives independently from the instance lifecycle. Instance store is local storage physically attached to the host, and it's temporary.

With E-B-S, data persists when you stop and start the instance. You can snapshot it, restore it, resize it, encrypt it, and attach it to another compatible instance. That's the normal choice for boot volumes, application data, database files, pipeline state, and anything you can't casually lose.

Instance store is different. It's often very fast, but it doesn't survive stop, termination, or host failure. It's great for scratch space, temporary shuffle data, local cache, intermediate files, and workloads where the source of truth is somewhere else, like S-3 or a database.

The interview trap is saying instance store is faster, so it's better. That's incomplete. Better depends on failure semantics. If the data is durable elsewhere and you need speed, instance store can be excellent. If losing the volume means losing business data, use E-B-S.

For data engineering, I usually treat S-3 or a database as the durable source of truth, E-B-S as reliable attached working storage, and instance store as fast disposable workspace. That mental model keeps pipelines recoverable.

---

**[HOST — voice: nova]**

Good distinction. Let's go one layer deeper into E-B-S. How do gp three, io two, and st one fit into real workloads?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... gp three is the default workhorse. It's a general purpose S-S-D volume where you can provision capacity, I-O-P-S, and throughput more independently than older generations. For most application servers, boot disks, moderate databases, Airflow workers, and pipeline machines, gp three is the practical starting point.

io two is for high-performance, high-durability, low-latency storage where I-O-P-S consistency matters. Think critical relational databases, high-write metadata stores, or transactional systems where storage latency directly affects production. You don't pick io two because it sounds premium. You pick it when the workload proves it needs provisioned I-O-P-S and consistency.

st one is throughput-optimized hard disk storage. It's not for small random reads. It's for large sequential workloads, like log processing, big file scans, staging areas, or data processing where megabytes per second matter more than tiny random I-O operations.

So the simple rule is this: gp three for most things, io two for serious consistent I-O-P-S, st one for large sequential throughput at lower cost. A senior engineer also asks what belongs on E-B-S at all. If the data is object-style, lake-style, and shared across many compute nodes, S-3 may be the better durable layer.

---

**[HOST — voice: nova]**

Nice. Now let's connect E-C-2 to networking. What should a Senior Data Engineer know about V-P-C networking on E-C-2?

---

**[SEAN — voice: onyx]**

Two things matter here... where the instance lives, and what can talk to it. Every E-C-2 instance runs inside a V-P-C subnet. The subnet decides its availability zone placement and whether it's public-facing or private-only.

For data engineering, most E-C-2 workers should live in private subnets. They don't need direct inbound internet access. They need controlled outbound access, access to S-3, access to databases, access to Kafka, or access to internal services. That usually means route tables, NAT gateways, V-P-C endpoints, and carefully designed security groups.

Security groups are stateful firewalls attached to elastic network interfaces, or E-N-Is. An E-N-I gives the instance its network identity: private I-P, security groups, and sometimes multiple network attachments. In more advanced designs, E-N-Is matter for failover, appliances, multi-homed instances, and traffic separation.

The senior answer is not, open port twenty-two and move on. The senior answer is, define the network blast radius. Put compute near the data. Keep workers private. Use least-permissive security groups. Prefer V-P-C endpoints for A-W-S services when private routing and lower exposure matter.

And for interview depth, remember that subnet placement affects availability. If all pipeline workers land in one availability zone, one zone issue can break the whole job. Network design is reliability design.

---

**[HOST — voice: nova]**

That security angle matters. How do I-A-M instance profiles and the metadata service fit into this?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... applications on E-C-2 should not use hardcoded A-W-S keys. They should get temporary credentials through an I-A-M role attached to the instance profile.

An instance profile is the bridge that lets an E-C-2 instance assume an I-A-M role. The A-W-S S-D-K running on the machine checks the default credential provider chain. When it sees it's running on E-C-2, it calls the instance metadata service, gets temporary credentials, and refreshes them automatically.

That means your Python job, Spark connector, or ingestion script can access S-3, Cloud-Watch, K-M-S, S-Q-S, or other services without embedding secrets on disk. This is one of the cleanest patterns in A-W-S security.

The metadata service is powerful, so it must be protected. Use version two of the instance metadata service where possible because it requires a session token. Avoid letting untrusted workloads on the instance call metadata freely. And keep the role scoped to what the job actually needs.

For a data engineer, this is a big interview signal. A junior person says, put keys in the config file. A senior person says, use an instance profile, short-lived credentials, least privilege, and no static secrets on the host.

---

**[HOST — voice: nova]**

Let's talk about scaling. What are Auto Scaling Groups really doing, and what pieces should we know beyond, add more servers?

---

**[SEAN — voice: onyx]**

So... basically... an Auto Scaling Group keeps a desired number of E-C-2 instances running from a defined template. That template is usually a launch template, which describes the A-M-I, instance type, security groups, I-A-M instance profile, user data, storage, and other launch settings.

The A-S-G has minimum, maximum, and desired capacity. Scaling policies decide when to add or remove instances. For example, scale out when C-P-U stays high, queue depth grows, consumer lag increases, or custom Cloud-Watch metrics show work backing up.

Cooldowns and warmups matter because scaling is not instant. If a data worker takes several minutes to bootstrap, you don't want the group repeatedly adding machines before the previous ones are ready. Lifecycle hooks also matter because they let you run custom logic when an instance launches or terminates. For data workloads, that can mean registering with a coordinator, draining tasks, uploading logs, or gracefully leaving a consumer group.

A senior engineer doesn't just say, use auto scaling. They ask what metric represents pressure. C-P-U might be meaningless for an I-O-bound job. Queue depth, Kafka lag, batch backlog, or scheduler latency may be much better signals.

The best A-S-G designs scale based on business work, not just machine heat.

---

**[HOST — voice: nova]**

And when traffic comes in, we often add load balancers. How do A-L-B and N-L-B differ, and when should data engineers care?

---

**[SEAN — voice: onyx]**

Here's the thing... A-L-B and N-L-B solve different layers of the problem. An Application Load Balancer works at the application layer. It's strong for H-T-T-P and H-T-T-P-S traffic, path routing, host routing, headers, health checks, and web-style services.

A Network Load Balancer works at the transport layer. It's built for very high throughput, low latency, static I-P needs, and T-C-P or U-D-P style traffic. It's useful when you're fronting systems that aren't normal web A-P-Is, or when performance and connection behavior are the main concern.

Data engineers care when E-C-2 is serving data products, internal query services, streaming endpoints, model inference, ingestion A-P-Is, or administrative U-Is. If it's a REST-style service, A-L-B is usually the natural fit. If it's Kafka-like traffic, custom T-C-P, very high connection volume, or low-latency network traffic, N-L-B may be the better fit.

The subtle point is that load balancers also define health and failure behavior. A bad health check can remove good workers or keep bad workers alive. For pipelines, that can mean failed ingestion, partial service outages, or weird retry storms.

So load balancing isn't just traffic distribution. It's production control over how clients discover healthy compute.

---

**[HOST — voice: nova]**

Placement groups are one of those topics people memorize and forget. Can you make cluster, spread, and partition placement groups practical?

---

**[SEAN — voice: onyx]**

Here's the key insight... placement groups are about controlling physical placement to influence latency, throughput, and failure isolation.

A cluster placement group puts instances close together. The reason is low latency and high network throughput between nodes. That's useful for tightly coupled workloads, distributed training, high-performance computing, or certain Spark and E-M-R-style jobs that are very chatty across nodes.

A spread placement group spreads instances across distinct hardware. The goal is fault isolation. You use it when each instance is critical and you don't want a single hardware failure to take down several of them.

A partition placement group divides instances into partitions, where each partition maps to separate racks or hardware groupings. This is useful for large distributed systems like H-D-F-S-style storage, Cassandra-style databases, Kafka clusters, or big compute fleets where you want failure domains but still need scale.

For data engineering, the senior move is matching placement to the distributed system. Cluster improves performance for tightly coupled compute. Spread protects small critical fleets. Partition supports large systems that replicate data across failure domains.

And the gotcha is capacity. Placement constraints can make launches fail if A-W-S can't satisfy the request. So you use placement groups intentionally, not casually.

---

**[HOST — voice: nova]**

Let's bring this back to data engineering architecture. When does E-C-2 beat Lambda, Fargate, and Glue?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... E-C-2 wins when control matters more than convenience. Lambda is excellent for short, event-driven tasks, but it has runtime, package, memory, and execution model constraints. Fargate is great for containers, but it abstracts the host. Glue is strong for managed E-T-L, but it may not fit every dependency, runtime, cost pattern, or operational style.

E-C-2 is often the better answer for long-running workers, custom agents, heavyweight batch processing, specialized libraries, high local disk needs, custom network clients, migration jobs, legacy workloads, and workloads that need persistent daemons.

For example, if I'm running a custom ingestion engine that keeps connections open, writes checkpoints, uses local caching, and needs special native libraries, E-C-2 may be simpler than forcing it into Lambda or Glue. If I'm running a large batch backfill with retryable chunks, Spot E-C-2 workers behind a queue can be extremely cost-effective.

The danger is using E-C-2 because it's familiar. Managed services reduce operational load. So the senior question is, what control do I actually need? If the answer is none, use the managed service. If the answer is runtime control, networking control, hardware choice, or cost control at scale, E-C-2 belongs on the table.

---

**[HOST — voice: nova]**

Before an instance runs work, it has to be built. How do A-M-Is, golden images, user data, and cloud-init fit together?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... imagine every data worker needs Python packages, system libraries, logging agents, security tools, and a bootstrap script. You can install all of that at launch time, or you can bake most of it into an A-M-I.

An A-M-I is the machine image used to launch the instance. A golden image is a standardized A-M-I that already contains approved dependencies, hardening, monitoring, and baseline configuration. The advantage is fast, consistent launches. The tradeoff is image maintenance. When dependencies change or security patches are needed, you need a new image pipeline.

User data and cloud-init run during boot. They're great for lightweight bootstrap actions: pulling configuration, registering with a scheduler, setting environment variables, installing a small final dependency, or starting the right service. But if user data turns into a giant installation script, launches become slow and fragile.

The senior pattern is usually hybrid. Bake stable heavy dependencies into a golden image. Use user data for environment-specific configuration. Keep bootstrapping idempotent, logged, and short.

For data platforms, this matters because scale events and replacements happen under pressure. If your worker takes twenty minutes to build itself and fails randomly during package install, your A-S-G isn't really elastic. It's just hopeful.

---

**[HOST — voice: nova]**

Let's close the main section with cost optimization. What are the big levers that actually matter for E-C-2 cost?

---

**[SEAN — voice: onyx]**

Two things matter here... don't overpay for idle capacity, and don't buy the wrong commitment. Rightsizing is the first lever. If an instance runs at five percent C-P-U, low memory, and low network, it's probably oversized. If it constantly spills to disk or throttles on I-O, it's probably undersized in the wrong dimension.

Spot is one of the strongest levers for data engineering batch work. If jobs are checkpointed, chunked, and retryable, Spot can cut compute cost dramatically. But Spot requires design discipline. Workers must tolerate interruption, persist progress outside the instance, and avoid assuming local state survives.

Savings Plans are the baseline lever. If you know your platform always runs a certain amount of compute, commit to that baseline. But don't cover every spike. Spikes are exactly where On-Demand and Spot flexibility helps.

Also watch hidden cost drivers. Oversized E-B-S volumes, provisioned I-O-P-S nobody uses, NAT gateway data processing, cross availability zone traffic, and idle load balancers can all surprise teams.

My simple rule is, tag everything, measure utilization, separate baseline from burst, use Spot for retryable batch, and commit only after usage is stable. Cost optimization is not a one-time cleanup. It's an operating rhythm.

---

**[HOST — voice: nova]**

What are the common mistakes and gotchas you see with E-C-2 in data engineering environments?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... most E-C-2 problems are not caused by E-C-2 itself. They're caused by unclear ownership of state, security, bootstrap, and failure recovery.

One mistake is treating the instance as the source of truth. If the instance dies and the job loses its only copy of progress, the architecture is fragile. State should be externalized to S-3, a database, a queue, or a checkpoint store.

Another mistake is using static credentials. That creates secret rotation problems and increases blast radius. Instance profiles and short-lived credentials should be the default.

A third mistake is weak bootstrap discipline. Giant user data scripts, manual patching, and snowflake servers create inconsistent fleets. If one worker is different from the others, debugging becomes a mess.

Networking mistakes are also common. Public instances that should be private, wide-open security groups, missing V-P-C endpoints, or expensive cross-zone traffic can all become production issues.

And finally, teams often scale on the wrong metric. C-P-U scaling won't solve a queue backlog caused by downstream throttling. More workers can make the system worse if the bottleneck is S-3 request rate, database locks, or external A-P-I limits.

The senior posture is simple: make compute replaceable, state durable, credentials temporary, bootstrap repeatable, and scaling tied to real work pressure.

---

**[HOST — voice: nova]**

Let's do a quick rapid-fire round.

---

**[SEAN — voice: onyx]**

Let's go.

---

**[HOST — voice: nova]**

First question. When would you use Spot instances for a data pipeline?

---

**[SEAN — voice: onyx]**

Use Spot when the workload is interruptible and retryable. Good examples are batch backfills, file conversions, distributed transforms, test workloads, and queue-based workers. The job must checkpoint progress outside the instance, usually in S-3, a database, or a durable queue. If interruption causes data loss or a production outage, Spot is the wrong default.

---

**[HOST — voice: nova]**

Second question. What survives when an E-C-2 instance is stopped?

---

**[SEAN — voice: onyx]**

E-B-S volumes normally survive a stop, unless they're configured for deletion on termination and the instance is actually terminated. The private I-P usually remains with the stopped instance. Instance store does not survive stop, termination, or underlying host loss. Anything important should live on E-B-S, S-3, or another durable system.

---

**[HOST — voice: nova]**

Third question. What's the safest way for an application on E-C-2 to access S-3?

---

**[SEAN — voice: onyx]**

Attach an I-A-M role through an instance profile and grant only the S-3 permissions the application needs. The A-W-S S-D-K will automatically retrieve temporary credentials from the instance metadata service. Don't put access keys in code, environment files, or local config. For private networking, also consider an S-3 V-P-C endpoint.

---

**[HOST — voice: nova]**

Fourth question. A data job needs huge sequential reads and writes. Which E-B-S type would you consider?

---

**[SEAN — voice: onyx]**

For large sequential throughput, st one can be a good fit because it's throughput optimized. For general purpose workloads, gp three is usually the safer default. If the workload needs consistent high random I-O-P-S, io two is the premium choice. The best answer depends on whether the bottleneck is throughput, random I-O, or latency consistency.

---

**[HOST — voice: nova]**

Fifth question. What's one senior-level E-C-2 cost optimization answer?

---

**[SEAN — voice: onyx]**

Separate baseline compute from burst compute. Cover stable baseline usage with Savings Plans or Reserved Instances, keep uncertain demand On-Demand, and use Spot for retryable batch. Rightsize based on metrics, not guesses. Also check storage, NAT gateway, and cross-zone transfer costs, because the bill is not only instance hours.

---

## END OF SCRIPT
