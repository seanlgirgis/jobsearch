# Toyota CloudFormation Cram (10 Q&A)

## 1) What is CloudFormation, and why is it better than manual console setup?
CloudFormation is AWS's native Infrastructure as Code service. You declare desired infrastructure in templates, and CloudFormation reconciles current state to desired state by creating, updating, replacing, or deleting resources. It gives repeatability, source control, auditability, and easier disaster recovery compared to manual console changes.

## 2) What are `Resources`, `Parameters`, `Outputs`, `Conditions`, and `Mappings`?
- `Resources`: Declares AWS resources to manage. Keep logical IDs stable.
- `Parameters`: Deploy-time inputs (env, VPC IDs, sizing). Do not pass secrets directly.
- `Outputs`: Publishes stack values for cross-stack use. Export only stable contracts.
- `Conditions`: Controls whether resources are created (for example, prod-only alarms).
- `Mappings`: Static lookup tables (region/env sizing). Avoid for frequently changing values.

## 3) What is a Change Set? What is the most dangerous keyword?
A Change Set previews what CloudFormation will do before execution. The most dangerous word is `Replacement` because the old physical resource can be removed and replaced, risking downtime, broken references, or data impact. For stateful resources, use `Retain` or `Snapshot` policies.

## 4) Difference between `DeletionPolicy` and `UpdateReplacePolicy`?
`DeletionPolicy` controls what happens when a resource is deleted from the stack or stack is deleted.  
`UpdateReplacePolicy` controls what happens to the old resource when an update requires replacement.  
Example: for RDS, set both to `Snapshot`; for long-lived S3 data, often use `Retain`.

## 5) What is drift, what causes it, and how do you remediate?
Drift is when deployed resources no longer match the template, usually from manual console/CLI edits. Detect it with drift detection, then decide: if intentional, codify it in the template; if unintentional, redeploy to restore expected state. Never leave undocumented "temporary" changes in production.

## 6) How do you structure stacks for a large data platform?
Split by ownership, lifecycle, and blast radius:
- Foundation: VPC, subnets, routing, IAM/KMS baseline
- Storage/data foundation: S3, policies, catalog/lake controls
- Compute/pipeline: Glue, Lambda, ECS/Fargate, EMR, Step Functions
- Data-domain stacks: customer/orders/finance
- Observability: alarms, logs, dashboards
- Environment separation: dev/test/prod
Keep stateful shared resources separate from fast-changing app stacks.

## 7) CloudFormation vs CDK vs Terraform?
Use CloudFormation for AWS-native governance and lifecycle control. Use CDK when you want reusable patterns in code (Python/TypeScript), knowing it synthesizes to CloudFormation. Use Terraform when managing multi-provider infrastructure (AWS + Snowflake/Datadog/GitHub/Kubernetes). Hard rule: never let two tools manage the same resource.

## 8) What is a Stack Policy? How is it different from IAM?
Stack Policy controls what CloudFormation can update inside a stack (for example, protecting stateful resources from accidental replacement). IAM controls who can call CloudFormation APIs. Risk: stack policies can block emergency changes, so define and document override procedure.

## 9) When use Lambda Custom Resources, and what safety rules?
Use custom resources only when CloudFormation lacks native support. Lambda must handle `Create`/`Update`/`Delete` and always return success/failure. Safety rules:
- Always handle exceptions and respond
- Keep logic idempotent (retries happen)
- Make delete behavior safe (CI/DR teardown)
- Log request IDs for debugging and audit

## 10) What is your production deployment rhythm?
1. Validate and lint template  
2. Create and review Change Set (`Replacement`, deletes, IAM, SG, KMS, stateful impact)  
3. Ensure retention/snapshot protections are correct  
4. Execute in approved maintenance window  
5. Run smoke tests  
6. Check alarms/logs and pipeline health  
7. Record deployment evidence and approvals

