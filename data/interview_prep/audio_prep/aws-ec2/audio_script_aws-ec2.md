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

Let's start at the foundation. What problem does E-C-two solve, why does it exist?

---

**[SEAN — voice: onyx]**

So... basically... before E-C-two, teams had to buy physical servers, wait for procurement, rack hardware, patch operating systems, and then hope capacity estimates were right months later. That created long lead times, high upfront capital spend, and painful overprovisioning because nobody wanted to run out of compute in peak season. E-C-two changed the model to on-demand virtual machines you can launch in minutes, scale up or down quickly, and pay for based on usage instead of owning idle hardware. It's still FUNDAMENTALLY important today because serverless is great for many tasks, but it has hard execution ceilings and runtime constraints. If you need persistent processes, deep operating system control, custom native libraries, or sustained high-throughput disk and network behavior, E-C-two is still the right primitive.

---

**[HOST — voice: nova]**

Makes sense. There are so many instance types though, so how do you choose without guessing?

---

**[SEAN — voice: onyx]**

Here's the thing... the name tells you a lot once you decode it. Family plus generation plus attributes plus size, like r seven g dot two x large, where r signals memory focus and g hints at Graviton architecture. For data work, m family is balanced and usually the safest starting point, r family is for memory-heavy joins and Spark executors, c family fits C-P-U-bound transforms and broker workloads, and i family is for local high-speed storage patterns. Burstable t family can be cheap for dev hosts, but it will throttle under sustained demand, so it's risky for steady pipelines. A practical playbook is start on m five or m six g, observe bottlenecks in metrics, then move to r family if memory pressure dominates or c family if compute saturation dominates. Treat instance selection as an iterative performance and cost loop, not a one-time guess.

---

**[HOST — voice: nova]**

Got it. What about cost strategy, when do you pick on-demand, reserved, or spot?

---

**[SEAN — voice: onyx]**

Here's the key insight... each option maps to a different risk profile. On-demand is flexibility first, pay per second, no long commitment, ideal for unpredictable jobs and development environments. Reserved capacity is commitment first, typically one year or three year terms, and it can be up to SEVENTY-TWO percent cheaper for stable baseline workloads that run continuously. Spot is interruption-tolerant capacity that can be up to NINETY percent cheaper, but A-W-S can reclaim it with roughly a two-minute warning, so workloads must checkpoint and recover cleanly. The production pattern for data teams is hybrid: reserved for steady baseline nodes, spot for burst workers that are stateless, and on-demand for unknown or transitional demand. Never put stateful coordinators or critical databases on spot, because reclaim events will hurt reliability faster than the savings justify.

---

**[HOST — voice: nova]**

Let's go deeper on storage. How should we think about E-B-S, instance store, and E-F-S?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... choose by persistence, latency, and sharing needs. E-B-S is network-attached block storage, persistent across stop and start, and it's the standard default for durable instance volumes. For most workloads, g p three is cost-effective and starts with THREE THOUSAND I-O-P-S baseline, while i o two is for demanding systems that may need up to SIXTY-FOUR THOUSAND I-O-P-S and stronger consistency expectations. Instance store is local N-V-M-E attached to the host, so it's extremely fast, but data is ephemeral and disappears when the instance stops or fails over, which is perfect for shuffle and scratch, not durable truth. E-F-S is shared file storage you can mount from multiple instances, useful for shared artifacts and common assets, but with higher latency than block storage. One critical gotcha: E-B-S lives in a single availability zone, so cross-zone attachment won't work.

---

**[HOST — voice: nova]**

And on networking plus permissions, how does an E-C-two instance securely talk to other services?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... imagine an E-T-L worker in a private subnet inside a V-P-C. It has no direct inbound internet route, security groups allow only required flows, and traffic to S-three or Glue goes through private endpoints instead of public paths. Permission is handled through an I-A-M instance profile attached to the instance role, so short-lived credentials rotate automatically and applications fetch them from metadata, not hardcoded files. That's EXACTLY the control plane pattern you want for regulated environments: private network paths plus least-privilege identity. The anti-pattern is embedding long-lived keys on disk, because key sprawl and rotation failures become inevitable. Keep compute private, keep identity role-based, and keep permission scope tightly aligned to what the process actually needs.

---

**[HOST — voice: nova]**

Now let's talk scaling. How does Auto Scaling actually help data workloads in real operations?

---

**[SEAN — voice: onyx]**

Two things matter here... capacity elasticity and operational discipline. Auto Scaling Groups define minimum, desired, and maximum counts, then policies react to signals like C-P-U utilization or scheduled demand windows. In mature environments, instances are cattle, not pets, so they launch from templates, bootstrap through user data, run workloads, and terminate without manual S-S-H tuning. If fronted by an A-L-B, health checks and traffic distribution stay consistent while failed nodes are replaced automatically. For analytics teams, this mental model maps directly to managed cluster behavior in services like E-M-R, where worker pools scale based on queue depth and utilization patterns. Once you understand A-S-G behavior, you make better choices on warm capacity, cooldown timing, and cost versus latency tradeoffs.

---

**[HOST — voice: nova]**

Where does E-C-two show up day-to-day in a real data engineering stack, beyond theory?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... even when you use managed products, E-C-two is frequently the substrate under the hood. Redshift nodes, many R-D-S configurations, E-M-R workers, and M-S-K brokers all inherit characteristics from underlying compute, network, and storage design choices. Direct E-C-two usage still appears when teams need persistent schedulers, custom runtimes, low-level system packages, or workloads that exceed serverless ceilings. Typical examples include long-running E-T-L services, self-managed orchestration components, jump hosts, and specialized broker or cache nodes. The decision rule is simple: use managed services when they meet reliability and feature needs, then use E-C-two when you need deeper control, tighter tuning, or predictable behavior not exposed by managed abstractions. That's why strong E-C-two fundamentals improve decisions across the entire platform.

---

**[HOST — voice: nova]**

What are the mistakes that repeatedly cause outages or wasted cost with E-C-two?

---

**[SEAN — voice: onyx]**

So... basically... teams often lose reliability through preventable basics. First, they hardcode A-W-S credentials instead of using I-A-M instance profiles, which creates security debt and painful rotations. Second, they route S-three access over public internet paths instead of V-P-C endpoints, which is slower, less secure, and usually more expensive. Third, they skip tagging standards, so finance and operations can't map runaway resources to owners or environments. Fourth, they put stateful services on spot and then act surprised when interruption events break consistency. Fifth, they place E-B-S volumes in the wrong availability zone or forget DeleteOnTermination behavior on data disks, then lose persistence unexpectedly during replacement events. The winning habit is explicit lifecycle design: identity, networking, storage durability, and cost controls must be intentional from day one.

---

**[HOST — voice: nova]**

Rapid-fire round. What's the difference between an E-B-S-backed instance and an instance-store-backed instance?

---

**[SEAN — voice: onyx]**

Here's the thing... E-B-S-backed instances rely on persistent network block storage, so volume data survives stop and start events and can be snapshotted cleanly. Instance-store-backed setups use local host storage with very high throughput and low latency, but the data is ephemeral. If the instance terminates or the host changes, that local data is gone. So choose E-B-S when durability matters, and choose instance store when speed matters more than persistence.

---

**[HOST — voice: nova]**

When should we use spot, and when should we absolutely avoid it?

---

**[SEAN — voice: onyx]**

Here's the key insight... use spot for interruptible, stateless, retry-friendly work like batch transforms, transient Spark executors, and distributed workers that checkpoint progress. Avoid spot for stateful control planes, databases, and anything that can't recover safely from abrupt reclaim events. A-W-S may reclaim spot with short notice, so architecture must assume interruption as normal. If interruption handling isn't engineered and tested, spot isn't a discount, it's a reliability liability.

---

**[HOST — voice: nova]**

How does an E-C-two instance get permission to read from S-three?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... attach an I-A-M role through an instance profile, grant only required S-three actions on required prefixes, and let temporary credentials rotate automatically. The application reads credentials from the metadata service, not hardcoded configuration files. That removes static key management and supports auditable least privilege. It's cleaner, safer, and easier to operate at scale.

---

**[HOST — voice: nova]**

What's the difference between a security group and a network A-C-L?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... security groups are stateful controls attached to instance network interfaces, so return traffic is automatically allowed for established flows. Network A-C-L rules are stateless subnet-level filters, so you must explicitly allow both inbound and outbound paths. Security groups are usually the primary day-to-day control for application boundaries, while network A-C-L settings provide broader subnet guardrails. Use both intentionally, but rely on security groups for most workload segmentation logic.

---

**[HOST — voice: nova]**

Last one. If an E-T-L job runs for four hours every night, what instance type and purchasing model would you recommend, and why?

---

**[SEAN — voice: onyx]**

Two things matter here... workload profile and interruption tolerance. I'd start with an m family baseline, then move to r family if memory pressure appears during joins or shuffles, and validate with real utilization and latency metrics. For purchasing, a scheduled baseline on reserved capacity can reduce predictable nightly cost, while burst workers can run on spot if the pipeline checkpoints safely. If the workload is highly stateful or restart-expensive, keep the critical stages on on-demand or reserved and isolate spot to retry-friendly steps. That's how you balance cost and reliability without betting the pipeline on interruption luck.

---

## END OF SCRIPT
