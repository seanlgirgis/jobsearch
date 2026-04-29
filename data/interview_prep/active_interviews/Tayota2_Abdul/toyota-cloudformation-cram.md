# Toyota CloudFormation Cram (Updated)

## 1) What is CloudFormation, and why not manual console changes?
CloudFormation is AWS's native declarative Infrastructure as Code service. You define desired resources in templates, and CloudFormation reconciles current to desired state (create/update/replace/delete). It gives repeatability, auditability, source control, and better disaster recovery than manual console work.

## 2) Core template sections: `Resources`, `Parameters`, `Outputs`, `Conditions`, `Mappings`
- `Resources`: AWS resources managed by the stack. Keep logical IDs stable.
- `Parameters`: Deploy-time inputs (env, VPC IDs, sizing). Avoid passing secrets directly.
- `Outputs`: Published values for cross-stack use. Export only stable contracts.
- `Conditions`: Create resources conditionally (for example, prod-only alarms).
- `Mappings`: Static lookup tables (region/env values). Avoid for frequently changing config.

## 3) What is a Change Set and what is the danger word?
A Change Set previews what CloudFormation will do before execution. Danger word: `Replacement`. It can replace physical resources and break data continuity, ARNs, or connections. Review replacements, deletions, IAM, SG, and KMS changes before production execution.

## 4) `DeletionPolicy` vs `UpdateReplacePolicy`
- `DeletionPolicy`: what happens when resource is removed from stack or stack is deleted.
- `UpdateReplacePolicy`: what happens to old resource when update requires replacement.
Example: for RDS use `Snapshot` (often both policies). For long-lived S3 data stores, often `Retain`.

## 5) What is drift and how do you remediate?
Drift means deployed resources no longer match the template, usually from manual console/CLI changes. Run drift detection, then:
- intentional change -> codify in template and redeploy
- unintentional change -> redeploy to restore desired state
Never leave undocumented production drift.

## 6) How to structure stacks for a large data platform
Split by ownership, lifecycle, and blast radius:
- Foundation: VPC, subnets, routes
- Security baseline: IAM, KMS, boundaries
- Storage/data foundation: S3, lake controls, catalog
- Compute/pipeline: Glue, Lambda, ECS/Fargate, EMR, Step Functions
- Observability: alarms, logs, dashboards
- Domain/env separation: customer/orders/finance + dev/test/prod
Keep stateful shared resources separate from frequently changing app stacks.

## 7) CloudFormation vs CDK vs Terraform
- CloudFormation: best for AWS-native governance/lifecycle.
- CDK: code-first authoring that synthesizes to CloudFormation.
- Terraform: best for multi-provider infrastructure.
Hard rule: never let two tools manage the same resource.

## 8) Stack Policy vs IAM
IAM controls who can call CloudFormation APIs.
Stack policy controls what CloudFormation can modify inside the stack.
Use stack policies to protect stateful resources, but document emergency override process because policies can block urgent fixes.

## 9) Lambda Custom Resources: when and how
Use only when CloudFormation lacks native support. Lambda receives `Create`/`Update`/`Delete` and must always return success/failure.
Safety rules:
- always handle exceptions and respond
- keep logic idempotent
- make delete behavior safe
- log request IDs for debugging and audit

## 10) Production deployment rhythm
1. Validate + lint template
2. Create change set
3. Review replacements/deletes/IAM/SG/KMS/stateful impact
4. Confirm retention/snapshot protections
5. Execute in approved window
6. Run smoke tests
7. Check alarms/logs/pipeline health
8. Record deployment evidence

## 11) Protecting production RDS from accidental impact
- `DeletionPolicy` and `UpdateReplacePolicy` to `Snapshot` or `Retain` as needed
- Enable RDS deletion protection
- Isolate RDS in separate stack
- Use stack policy + termination protection
- Review change sets for `Replacement`
- Verify backups/snapshots and restore readiness

## 12) `Snapshot` vs `Retain` tradeoff
- `Snapshot`: cleaner automated teardown with recovery point.
- `Retain`: resource outlives stack for immediate continuity.
Tradeoff: `Retain` can leave orphaned resources that require explicit ownership, cost governance, and drift control.

## 13) Why IAM/SG-only changes are still risky
Even without `Replacement`, IAM and security group edits can silently break Glue/ECS/Lambda/EMR/RDS connectivity and permissions. Always diff exact permissions/rules, map impacted workloads, and run targeted smoke tests.

## 14) `UPDATE_ROLLBACK_FAILED` recovery path
Update failed and rollback also failed, leaving stack stuck. Read stack events for first root cause, fix underlying issue, run `continue-update-rollback` (skip blocked logical resource only if needed), return stack to stable state, then redeploy corrected template.

## 15) Why one giant stack is a bad idea
It increases blast radius, review complexity, failure coupling, and rollback risk. A small app change can impact network, IAM, and data resources if everything is bundled together.

## 16) CDK adoption mistake to avoid
Treating CDK as "safe by abstraction" without reviewing synthesized CloudFormation. Always inspect generated IAM policies, logical IDs, retention settings, and replacement-sensitive properties.

## 17) StackSets: when and rollout controls
Use for org-wide multi-account/multi-region baselines (logging, guardrails, shared controls). Require phased rollout, non-prod validation, controlled concurrency/failure tolerance, and rollback playbooks.

## 18) Hard mixed-tool ownership rule
If using Terraform and CloudFormation in one org: enforce single-owner-per-resource boundaries. Integrate via outputs/interfaces, not dual ownership.
