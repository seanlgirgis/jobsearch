## What CloudFormation Is

CloudFormation is AWS's native IaC engine. You write a template declaring
what you want. CloudFormation diffs it against the current stack and
creates, updates, replaces, or deletes resources to match.

---

### What it manages

S3, IAM, VPCs, Glue, Athena, Redshift, EMR, ECS, RDS, Lambda.
If it lives in AWS, CloudFormation can own it.

---

### Why it matters

For data engineering it's a **repeatability contract** — not just a
deployment tool. Bucket policies, crawlers, workgroups, VPC endpoints,
IAM roles: if they only exist by hand, they aren't reproducible.

## Where CloudFormation Earns Its Place

**Repeatable Environments**
Same S3, Glue, IAM, VPC, and compute layout across dev, test, and prod.
No manual drift between environments.

**Compliance**
Template history shows exactly who changed encryption, access,
retention, and networking rules — and when.

**Disaster Recovery**
Core infrastructure rebuilt from source-controlled templates.
No archaeology required.

**Multi-Account Governance**
StackSets push approved baselines across many AWS accounts and regions
from a single place.

## Template Structure

Written in YAML or JSON. YAML is the standard choice — easier to read,
supports comments, and handles nested definitions cleanly.

---
## Key Sections

**Resources**
Declares AWS resources. Keep logical IDs stable — changing them
triggers replacement, not update.

**Parameters**
Accepts values at deploy time. Always add constraints, allowed values,
and clear descriptions.

**Outputs**
Exposes stack values for other stacks to consume. Export only stable
cross-stack contracts.

**Conditions**
Controls whether a resource gets created. Useful for dev/prod
differences — but don't overfit one template to every scenario.

**Mappings**
Static lookup table. Good for region or environment sizing maps.
Bad for config that changes frequently.

---

## Parameters, Mappings, Conditions, Outputs


These four sections turn a static resource file into an
environment-aware deployment unit — one template that works
across dev, QA, staging, and prod without duplication.

---

**Parameters** — values supplied at deploy time.
Use for: env name, VPC ID, subnet IDs, instance sizing, feature toggles.
Avoid when: the value is a secret or should never be manually supplied.

**Mappings** — static lookups keyed by region or environment.
Use for: region-specific AMIs, environment sizing, static lookup tables.
Avoid when: values change often or come from service discovery.

**Conditions** — logic that controls what gets built.
Use for: optional alarms, prod-only retention, dev-only test resources.
Avoid when: too many branches make the template unreadable.

**Outputs** — values the stack publishes after deployment.
Use for: bucket names, role ARNs, security group IDs, endpoint URLs.
Avoid when: the value is unstable or should stay private.


## Stacks, Nested Stacks, and StackSets

These define ownership boundaries, blast radius, and operational complexity —
not just organization.

---

**Single Stack**
One template, one deployed unit.
Good for small services or a single pipeline component.
Risk: grows too large and becomes dangerous to update.

**Nested Stacks**
Shared modules (VPC, IAM, S3, Glue baseline) composed into a parent stack.
Good for reuse. Tradeoff: failure tracing gets more layered.

**StackSets**
One template deployed across many accounts and regions.
Good for org-wide guardrails and standard baselines.
Tradeoff: requires strong account governance and careful rollout controls.

---

**Common data engineering pattern**
Split infrastructure into layers: network → security → storage → compute → pipelines.
Keeps a Glue job deployment from touching VPC routing or org-wide logging.


## Change Sets and Safe Deployment

A change set previews what CloudFormation will do before it does it.
For production, reviewing a change set is the minimum safe step
before applying any infrastructure update.

---

**What it shows**
Which resources will be added, modified, replaced, or removed.

**The word to watch**
`Replacement` — CloudFormation creates a new physical resource
and deletes the old one. Data, connections, and ARNs may not survive.

**What a change set does not tell you**
Application-level impact. A change set can look clean and still
break workloads.

---

## Production Review Checklist

**Resource Replacement**
Stateful resources — RDS, Redshift, ElastiCache — may lose data
or cause downtime if replaced.

**IAM Changes**
Can silently break Glue jobs, EMR clusters, ECS tasks, Lambda
functions, or cross-account access.

**Deletion Actions**
May remove logs, buckets, alarms, roles, or endpoints that running
systems depend on.

**Security Group Changes**
Can break database connectivity or cut off private service access.

---

## Rollback Behavior

When a stack update or create fails, CloudFormation rolls back to the
last stable state. On create failure it deletes what it built. On update
failure it restores the prior template state.

**Common rollback triggers**
Failed resource creation, missing permissions, dependency timeout,
service quota limits, validation errors, or failed wait conditions.

---

**The important distinction**
Rollback protects stack state — not business state. A partial data
migration, a changed external policy, or a broken app dependency
may still need manual recovery.

---

**Stuck rollbacks**
`UPDATE_ROLLBACK_FAILED` is painful. Skip the problem resource,
fix the template, redeploy.

```bash
aws cloudformation continue-update-rollback \
  --stack-name prod-data-platform \
  --resources-to-skip ProblemResourceLogicalId
```

---

**Rollback Controls**

**Disable Rollback on Create**
Leaves resources in place after failure — useful for debugging new stacks.

**Rollback Triggers**
Monitors CloudWatch alarms and rolls back if a critical alarm fires.

**Continue Update Rollback**
Recovers a stack stuck in failed rollback state.

**DeletionPolicy**
Preserves stateful resources during stack deletion or replacement.

---

