# Toyota CloudFormation Cram (Updated)

<a id="toc"></a>
## Table of Contents
1. [1) What is CloudFormation, and why not manual console changes?](#sec-1)
2. [2) Core template sections: `Resources`, `Parameters`, `Outputs`, `Conditions`, `Mappings`](#sec-2)
3. [3) What is a Change Set and what is the danger word?](#sec-3)
4. [4) `DeletionPolicy` vs `UpdateReplacePolicy`](#sec-4)
5. [5) What is drift and how do you remediate?](#sec-5)
6. [6) How to structure stacks for a large data platform](#sec-6)
7. [7) CloudFormation vs CDK vs Terraform](#sec-7)
8. [8) Stack Policy vs IAM](#sec-8)
9. [9) Lambda Custom Resources: when and how](#sec-9)
10. [10) Production deployment rhythm](#sec-10)
11. [11) Protecting production RDS from accidental impact](#sec-11)
12. [12) `Snapshot` vs `Retain` tradeoff](#sec-12)
13. [13) Why IAM/SG-only changes are still risky](#sec-13)
14. [14) `UPDATE_ROLLBACK_FAILED` recovery path](#sec-14)
15. [15) Why one giant stack is a bad idea](#sec-15)
16. [16) CDK adoption mistake to avoid](#sec-16)
17. [17) StackSets: when and rollout controls](#sec-17)
18. [18) Hard mixed-tool ownership rule](#sec-18)

<a id="sec-1"></a>
## 1) What is CloudFormation, and why not manual console changes?
CloudFormation is AWS's native declarative Infrastructure as Code service. You define desired resources in templates, and CloudFormation reconciles current to desired state (create/update/replace/delete). It gives repeatability, auditability, source control, and better disaster recovery than manual console work.
[Back to TOC](#toc)


<a id="sec-2"></a>
## 2) Core template sections: `Resources`, `Parameters`, `Outputs`, `Conditions`, `Mappings`
- `Resources`: AWS resources managed by the stack. Keep logical IDs stable.
- `Parameters`: Deploy-time inputs (env, VPC IDs, sizing). Avoid passing secrets directly.
- `Outputs`: Published values for cross-stack use. Export only stable contracts.
- `Conditions`: Create resources conditionally (for example, prod-only alarms).
- `Mappings`: Static lookup tables (region/env values). Avoid for frequently changing config.

[Back to TOC](#toc)

<a id="sec-3"></a>
## 3) What is a Change Set and what is the danger word?
A Change Set previews what CloudFormation will do before execution. Danger word: `Replacement`. It can replace physical resources and break data continuity, ARNs, or connections. Review replacements, deletions, IAM, SG, and KMS changes before production execution.
[Back to TOC](#toc)


<a id="sec-4"></a>
## 4) `DeletionPolicy` vs `UpdateReplacePolicy`
- `DeletionPolicy`: what happens when resource is removed from stack or stack is deleted.
- `UpdateReplacePolicy`: what happens to old resource when update requires replacement.
[Back to TOC](#toc)

Example: for RDS use `Snapshot` (often both policies). For long-lived S3 data stores, often `Retain`.

<a id="sec-5"></a>
## 5) What is drift and how do you remediate?
Drift means deployed resources no longer match the template, usually from manual console/CLI changes. Run drift detection, then:
- intentional change -> codify in template and redeploy
- unintentional change -> redeploy to restore desired state
Never leave undocumented production drift.

[Back to TOC](#toc)

<a id="sec-6"></a>
## 6) How to structure stacks for a large data platform
Split by ownership, lifecycle, and blast radius:
- Foundation: VPC, subnets, routes
- Security baseline: IAM, KMS, boundaries
- Storage/data foundation: S3, lake controls, catalog
- Compute/pipeline: Glue, Lambda, ECS/Fargate, EMR, Step Functions
- Observability: alarms, logs, dashboards
- Domain/env separation: customer/orders/finance + dev/test/prod
Keep stateful shared resources separate from frequently changing app stacks.

[Back to TOC](#toc)

<a id="sec-7"></a>
## 7) CloudFormation vs CDK vs Terraform
- CloudFormation: best for AWS-native governance/lifecycle.
- CDK: code-first authoring that synthesizes to CloudFormation.
- Terraform: best for multi-provider infrastructure.
Hard rule: never let two tools manage the same resource.

[Back to TOC](#toc)

<a id="sec-8"></a>
## 8) Stack Policy vs IAM
IAM controls who can call CloudFormation APIs.
Stack policy controls what CloudFormation can modify inside the stack.
Use stack policies to protect stateful resources, but document emergency override process because policies can block urgent fixes.

[Back to TOC](#toc)

<a id="sec-9"></a>
## 9) Lambda Custom Resources: when and how
Use only when CloudFormation lacks native support. Lambda receives `Create`/`Update`/`Delete` and must always return success/failure.
Safety rules:
- always handle exceptions and respond
- keep logic idempotent
- make delete behavior safe
- log request IDs for debugging and audit

[Back to TOC](#toc)

<a id="sec-10"></a>
## 10) Production deployment rhythm
1. Validate + lint template
2. Create change set
3. Review replacements/deletes/IAM/SG/KMS/stateful impact
4. Confirm retention/snapshot protections
5. Execute in approved window
6. Run smoke tests
7. Check alarms/logs/pipeline health
8. Record deployment evidence

[Back to TOC](#toc)

<a id="sec-11"></a>
## 11) Protecting production RDS from accidental impact
- `DeletionPolicy` and `UpdateReplacePolicy` to `Snapshot` or `Retain` as needed
- Enable RDS deletion protection
- Isolate RDS in separate stack
- Use stack policy + termination protection
- Review change sets for `Replacement`
- Verify backups/snapshots and restore readiness

[Back to TOC](#toc)

<a id="sec-12"></a>
## 12) `Snapshot` vs `Retain` tradeoff
- `Snapshot`: cleaner automated teardown with recovery point.
- `Retain`: resource outlives stack for immediate continuity.
Tradeoff: `Retain` can leave orphaned resources that require explicit ownership, cost governance, and drift control.

[Back to TOC](#toc)

<a id="sec-13"></a>
## 13) Why IAM/SG-only changes are still risky
Even without `Replacement`, IAM and security group edits can silently break Glue/ECS/Lambda/EMR/RDS connectivity and permissions. Always diff exact permissions/rules, map impacted workloads, and run targeted smoke tests.

[Back to TOC](#toc)

<a id="sec-14"></a>
## 14) `UPDATE_ROLLBACK_FAILED` recovery path
Update failed and rollback also failed, leaving stack stuck. Read stack events for first root cause, fix underlying issue, run `continue-update-rollback` (skip blocked logical resource only if needed), return stack to stable state, then redeploy corrected template.

[Back to TOC](#toc)

<a id="sec-15"></a>
## 15) Why one giant stack is a bad idea
It increases blast radius, review complexity, failure coupling, and rollback risk. A small app change can impact network, IAM, and data resources if everything is bundled together.

[Back to TOC](#toc)

<a id="sec-16"></a>
## 16) CDK adoption mistake to avoid
Treating CDK as "safe by abstraction" without reviewing synthesized CloudFormation. Always inspect generated IAM policies, logical IDs, retention settings, and replacement-sensitive properties.
[Back to TOC](#toc)


<a id="sec-17"></a>
## 17) StackSets: when and rollout controls
Use for org-wide multi-account/multi-region baselines (logging, guardrails, shared controls). Require phased rollout, non-prod validation, controlled concurrency/failure tolerance, and rollback playbooks.

[Back to TOC](#toc)

<a id="sec-18"></a>
## 18) Hard mixed-tool ownership rule
If using Terraform and CloudFormation in one org: enforce single-owner-per-resource boundaries. Integrate via outputs/interfaces, not dual ownership.
[Back to TOC](#toc)

