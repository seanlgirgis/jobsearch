## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: AWS IAM
Output filename: final_aws-iam.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\aws-iam\audio_script_aws-iam.md

---

**[HOST — voice: nova]**

Let's start at the very beginning. What is I-A-M, and why does every A-W-S conversation come back to it?

---

**[SEAN — voice: onyx]**

So... basically... I-A-M is the control plane for identity and permissions across A-W-S. Every request to S-three, E-C-two, Lambda, Glue, Redshift, all of it, is evaluated through policy logic before access is granted. It answers three practical questions every time: who is calling, are they authenticated, and are they authorized for this exact action on this exact resource. It's global at the account level, so one bad decision can have wide blast radius. If you master I-A-M, you've got the foundation for secure engineering in A-W-S.

---

**[HOST — voice: nova]**

Got it. Walk me through the building blocks: users, groups, roles, and policies. How do they fit together in real teams?

---

**[SEAN — voice: onyx]**

Here's the thing... users are long-lived identities, groups are management containers, roles are temporary identity projections, and policies are the actual permission language. A user might represent a human sign-in, and groups make policy assignment scalable across teams. Roles are what modern systems should use because S-T-S issues temporary credentials instead of permanent keys. Policies in J-S-O-N define Allow or Deny with Action, Resource, and optional Condition. Everything else is structure; policy evaluation is where access truly happens.

---

**[HOST — voice: nova]**

When we say policy evaluation, what does that document really look like, and what are the pieces interviewers care about most?

---

**[SEAN — voice: onyx]**

Here's the key insight... each statement has Effect, Action, Resource, and sometimes Condition, and those four fields drive everything. Effect is Allow or Deny, and explicit Deny always wins no matter where Allow appears. Action is the A-P-I operation set, Resource is the targeted A-R-N scope, and Condition applies context like M-F-A, V-P-C source, or time boundaries. Default posture is implicit deny until a valid allow path exists. Least privilege comes from narrowing both Action and Resource aggressively, then adding condition controls.

---

**[HOST — voice: nova]**

You always emphasize roles over users. Make that distinction concrete for production systems.

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... users come with static credentials, roles come with expiring credentials, and that's the difference between contained risk and long-lived exposure. A leaked access key tied to a user can survive for months if governance is weak, but a stolen S-T-S token dies quickly by design. E-C-two instances should use instance profiles, Lambda needs execution roles, E-C-S tasks need task roles, and Glue jobs need service roles. NEVER put human access keys into server environments for machine workloads. ALWAYS bind compute to roles and let the S-D-K fetch credentials automatically.

---

**[HOST — voice: nova]**

Let's get practical. How do services actually receive permissions when they run?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... an E-C-two instance with an attached role gets temporary credentials from the instance metadata service, and the app doesn't need embedded secrets. Lambda assumes its execution role on each invocation and needs CloudWatch Logs permissions or observability breaks fast. In E-C-S, task execution role and task role are separate responsibilities, and confusing them is a classic outage pattern. Glue service roles usually need S-three access, Glue Catalog privileges, and optional K-M-S or Secrets Manager access. The pattern is consistent: identity is attached to runtime, not hardcoded in code.

---

**[HOST — voice: nova]**

Where does AssumeRole fit in, especially for multi-account engineering?

---

**[SEAN — voice: onyx]**

Two things matter here... AssumeRole is both a security boundary and an operational bridge. One identity calls S-T-S, receives temporary session credentials, and operates as a target role with scoped permissions. For cross-account data platforms, account A assumes a role in account B to write to shared lakes or query controlled assets. The trust policy defines who may assume, while the permission policy defines what happens after assumption. If either side is wrong, access fails or over-permits.

---

**[HOST — voice: nova]**

What does good I-A-M hygiene look like in a data engineering stack day to day?

---

**[SEAN — voice: onyx]**

Now... the important distinction is... least privilege is not a slogan, it's a repeatable design discipline. Glue crawlers, E-T-L jobs, Lambda triggers, Redshift access roles, each workload gets its own narrow role with explicit resource scope. Then resource policies, especially on S-three buckets, add a second control plane so identity mistakes don't immediately become data exposure. CloudTrail gives change traceability, Access Analyzer surfaces excessive exposure, and Config tracks drift over time. ZERO standing permissions beyond workload need is the target state.

---

**[HOST — voice: nova]**

Before rapid-fire, call out the most common mistakes you see so people can avoid them.

---

**[SEAN — voice: onyx]**

So... basically... the worst mistakes are predictable and expensive. Hardcoded keys in code or environment files, wildcard star permissions in production, and root-account usage for daily tasks are immediate red flags. Teams also mix up E-C-S task role versus execution role, then lose hours debugging access denied paths. Another frequent miss is forgetting logs permissions on Lambda, which blinds incident response. If a team audits for these five issues monthly, their security posture improves fast.

---

**[HOST — voice: nova]**

Rapid-fire question one: what's the difference between an I-A-M role and an I-A-M user?

---

**[SEAN — voice: onyx]**

Here's the thing... an I-A-M user is a long-lived identity, usually for human access, while a role is a temporary identity assumed for specific work. Users often carry persistent credentials unless tightly governed. Roles issue temporary credentials through S-T-S with bounded lifetime. For services and automation, roles are the correct default. For humans, federated access plus role assumption is usually better than raw users with keys.

---

**[HOST — voice: nova]**

Question two: explicit Deny and explicit Allow both exist for the same action. What wins?

---

**[SEAN — voice: onyx]**

Here's the key insight... explicit Deny always wins, full stop. A-W-S evaluates all applicable policies, but the moment explicit Deny matches the request context, access is rejected. No allow statement can override that deny result. That's why deny guardrails are so effective for high-risk controls. It's also why policy reviews must include negative-path testing.

---

**[HOST — voice: nova]**

Question three: a Glue job can't read from S-three, and it already has a role. What do you check first?

---

**[SEAN — voice: onyx]**

Right... so the way I think about this... first validate the assumed role identity at runtime, then inspect effective policy and bucket policy together. Confirm Action and Resource in the role policy match the exact S-three path, not just the bucket root. Check for explicit Deny in identity policy, bucket policy, boundary, or organizational controls. Verify K-M-S permissions if the objects are encrypted. Finally confirm network path, endpoint policy, and region alignment.

---

**[HOST — voice: nova]**

Question four: what is a trust policy, and how is it different from a permission policy?

---

**[SEAN — voice: onyx]**

Let me give you a concrete example... trust policy answers who can assume this role, permission policy answers what this role can do after assumption. If your C-I-C-D role isn't listed as a trusted principal, AssumeRole fails even if permissions look perfect. If trust is open but permission is broad, assumption succeeds but blast radius becomes dangerous. Both policies must be intentionally scoped. Think of trust as the front door, permission as room-level authorization.

---

**[HOST — voice: nova]**

Question five: your deployment pipeline needs to deploy into A-W-S securely. What's the right setup?

---

**[SEAN — voice: onyx]**

Two things matter here... use O-I-D-C federation or equivalent short-lived identity to AssumeRole, and avoid stored long-term keys entirely. Build a dedicated deployment role with narrow permissions per environment, plus condition constraints like branch, audience, and repository context where possible. Add explicit deny guardrails for privileged paths and require approvals for production actions. Log all AssumeRole and deployment actions in CloudTrail with alerting. That gives strong security without slowing delivery.

---

## END OF SCRIPT
