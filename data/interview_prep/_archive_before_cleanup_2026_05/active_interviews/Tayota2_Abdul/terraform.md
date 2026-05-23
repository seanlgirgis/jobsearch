# Terraform

<a id="toc"></a>
## Table of Contents
1. [What Terraform Actually Solves](#sec-1)
2. [HCL Syntax and Project Structure](#sec-2)
3. [Providers, Resources, Data Sources, and Outputs](#sec-3)
4. [State: The Real Source of Truth](#sec-4)
5. [Remote State with S3 and DynamoDB Locking](#sec-5)
6. [Plan, Apply, Destroy, and State Mutation](#sec-6)
7. [Modules for Reusable Infrastructure](#sec-7)
8. [Workspaces vs Separate State Files](#sec-8)
9. [Importing Existing AWS Resources](#sec-9)
10. [Terraform for Data Engineering Infrastructure](#sec-10)
11. [Secrets, Sensitive Values, and State Exposure](#sec-11)
12. [Drift Detection and Remediation](#sec-12)
13. [CI/CD with GitHub Actions and OIDC](#sec-13)
14. [Terraform vs CloudFormation](#sec-14)
15. [Interview Q&A](#sec-15)

---

<a id="sec-1"></a>
## What Terraform Actually Solves

Terraform turns cloud infrastructure into versioned, reviewable, repeatable
configuration. The real value for data engineering is making a platform
reproducible: S3 buckets, IAM roles, Glue catalogs, VPC networking, RDS,
ECS services, EventBridge schedules, Secrets Manager entries, and monitoring
policies — described in code and promoted through environments.

It is declarative. You describe the desired end state. Terraform compares
that against its recorded state and the provider API, then produces an
execution plan. This is different from a script that says how to create
things step by step.

**The contract:** code, state, and the cloud provider must agree.

**The danger:** treat it like a loose deploy script and it can delete or
recreate important resources — especially if state is wrong, backend access
is weak, or multiple people apply at once.

**Use Terraform for**
Repeatable AWS environments, shared platform components, network/IAM/storage/databases,
cross-cloud or vendor-neutral IaC.

**Be careful with**
Manual experiments never imported into state, application deploys better
handled by CI/CD, secrets and generated passwords in state, AWS-native
services where CloudFormation features arrive first.

---
[Back to TOC](#toc)


<a id="sec-2"></a>
## HCL Syntax and Project Structure

Terraform uses HCL, HashiCorp Configuration Language. Blocks define things,
arguments configure them, expressions compute values, references connect
resources. Clean projects separate provider config, variables, resources,
outputs, and backend config.

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  description = "AWS region for the workload."
  default     = "us-east-1"
}

resource "aws_s3_bucket" "raw" {
  bucket = "sean-data-platform-raw-${var.environment}"

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

output "raw_bucket_name" {
  value = aws_s3_bucket.raw.bucket
}
```

**Avoid** deep nested expressions, heavy dynamic blocks, and magic naming
conventions. They make plans hard to review and failures hard to debug.

**Common file layout**

`main.tf` — Core resources or module calls.
`providers.tf` — Provider versions and configuration.
`variables.tf` — Input variables and validation rules.
`outputs.tf` — Values exposed to humans, CI/CD, or other stacks.
`backend.tf` — Remote backend configuration.
`terraform.tfvars` — Environment-specific values. Never secrets.

---
[Back to TOC](#toc)


<a id="sec-3"></a>
## Providers, Resources, Data Sources, and Outputs

Providers are plugins that know how to talk to APIs: AWS, GitHub, Datadog,
Snowflake, Kubernetes. Resources create and manage infrastructure. Data
sources read existing infrastructure without owning it. Outputs expose
selected values after apply.

```hcl
data "aws_caller_identity" "current" {}

data "aws_vpc" "shared" {
  tags = {
    Name = "shared-data-vpc"
  }
}

resource "aws_security_group" "glue_jobs" {
  name        = "glue-jobs-${var.environment}"
  description = "Security group for Glue jobs"
  vpc_id      = data.aws_vpc.shared.id
}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}
```

**Provider** — No. Defines API client and credentials.
**Resource** — Yes. Owns the lifecycle of infrastructure.
**Data source** — No. Reads existing infrastructure.
**Output** — No. Publishes selected values from state.

Use data sources when referencing shared infrastructure owned elsewhere.
Use resources only when this state file is responsible for the lifecycle.

If two Terraform states manage the same AWS resource, you have an ownership
conflict. The result is drift, surprise changes, or destructive replacements.

---

[Back to TOC](#toc)

<a id="sec-4"></a>
## State: The Real Source of Truth

State maps configuration addresses to real provider objects.
`aws_s3_bucket.raw` maps to an actual S3 bucket. State contains resource IDs,
dependency metadata, attribute values, and sometimes sensitive values.
Terraform uses it to decide whether to create, update, replace, or delete.

Configuration says what you want.
The cloud provider says what exists.
State says what Terraform believes it owns.
A plan reconciles all three.

For production: state is operational data. Back it up, lock it, restrict it,
encrypt it, and treat edits as a break-glass operation.

Deleting `terraform.tfstate` does not delete AWS resources. It deletes
Terraform's memory of them — which can cause duplicate creation or
destructive imports later.

```bash
# Inspect state addresses
terraform state list

# Show one tracked object
terraform state show aws_s3_bucket.raw

# Move an object after refactoring resource names
terraform state mv aws_s3_bucket.raw aws_s3_bucket.data_raw

# Remove from state without deleting the cloud resource
terraform state rm aws_s3_bucket.legacy
```

---
[Back to TOC](#toc)


<a id="sec-5"></a>
## Remote State with S3 and DynamoDB Locking

Local state is fine for solo labs. Production needs remote state.
On AWS: encrypted S3 bucket with versioning + DynamoDB table for locking.
S3 stores the state file. DynamoDB prevents two applies from mutating the
same state at the same time.

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state-prod"
    key            = "data-platform/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
    encrypt        = true
  }
}
```

Remote state = shared memory. Versioned S3 = recovery. DynamoDB = concurrency control.

**Backend options**

Local state — personal demos and throwaway labs. No collaboration, easy to lose.
S3 backend — AWS teams wanting simple remote state. You manage bucket, encryption, versioning, and lock table.
Terraform Cloud — policy checks, hosted state, run history. Vendor platform and pricing considerations.
Consul backend — HashiCorp-heavy environments. More operational overhead.

**Bootstrap pattern**
The backend bucket and lock table cannot be created by the same backend they
configure on first run. Most teams use a small bootstrap stack, a separate
admin script, or a manually approved foundation module.

---

[Back to TOC](#toc)

<a id="sec-6"></a>
## Plan, Apply, Destroy, and State Mutation

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan

# Dangerous: destroys resources tracked by this state
terraform destroy
```

**Command reference**

`terraform plan` — No cloud change. No state change. Reads state and provider APIs.
`terraform apply` — Changes cloud. Changes state. State updated after successful ops.
`terraform destroy` — Changes cloud. Changes state. Deletes tracked resources unless protected.
`terraform refresh` — No cloud change. Changes state. Updates state view from provider; use carefully.

Review the plan like code. Look closely for replacements of stateful resources:
RDS, buckets, KMS keys, Glue catalogs, IAM roles used by running pipelines.

A clean plan does not mean the change is safe. It means Terraform can
calculate the change. Provider bugs, AWS quotas, naming collisions, and
runtime dependencies can still break the apply.

---

[Back to TOC](#toc)

<a id="sec-7"></a>
## Modules for Reusable Infrastructure

Modules package resources into reusable units: an S3 data lake bucket, an
ECS service, a Glue job pattern, an RDS instance, or a full environment slice.
Good modules expose stable inputs and outputs while hiding repetitive details.

```hcl
module "raw_bucket" {
  source = "./modules/s3-data-bucket"

  name        = "raw"
  environment = var.environment
  kms_key_id  = module.kms.key_id
  tags        = local.common_tags
}

module "glue_job" {
  source = "./modules/glue-python-job"

  job_name          = "ingest-customer-events"
  script_s3_path    = "s3://company-artifacts/glue/ingest.py"
  role_arn          = module.iam.glue_role_arn
  worker_type       = "G.1X"
  number_of_workers = 5
}
```

The best modules encode platform standards: encryption, tags, logging,
network rules, naming, and least-privilege IAM.

Avoid one universal mega-module for every workload. Large modules create
tight coupling and make blast radius hard to reason about.

**Module styles**

Small resource module — Reusable S3 bucket, IAM role, Glue job. Risk: too many tiny wrappers with little value.
Service module — ECS service, RDS cluster, data pipeline unit. Risk: inputs can become huge.
Environment module — Full dev/test/prod composition. Risk: harder to promote changes independently.

---

[Back to TOC](#toc)

<a id="sec-8"></a>
## Workspaces vs Separate State Files

Workspaces let one config directory maintain multiple state files. Useful for
small variations or ephemeral environments. For serious environment promotion,
most teams prefer separate state keys, separate folders, or separate root
modules per environment.

```bash
terraform workspace list
terraform workspace new dev
terraform workspace select prod

# Many teams prefer explicit backend keys instead:
# dev/data-platform/terraform.tfstate
# prod/data-platform/terraform.tfstate
```

Workspaces are not a strong environment boundary. A bad variable, provider
alias, or backend misconfiguration can still point a workspace at the wrong
account or resource names.

**Approaches**

Workspaces — Simple for similar stacks and temporary environments. Weak boundary; easy to confuse current workspace.
Separate backend keys — Clear state split while sharing code. Requires disciplined backend config.
Separate root folders — Very explicit environment ownership. Can duplicate code if modules are weak.
Separate accounts — Strongest AWS isolation. Requires account vending and cross-account access design.

For data platforms, separate state files usually win for dev, test, and prod
because access control and blast radius are easier to explain.

---

[Back to TOC](#toc)

<a id="sec-9"></a>
## Importing Existing AWS Resources

Import brings existing infrastructure under Terraform state. Common when a
team has manually created S3 buckets, IAM roles, VPCs, RDS instances, or
Glue resources. Import does not write perfect code automatically — you must
create matching resource blocks, import the real object, run a plan, and
reconcile differences until the plan is clean.

```hcl
# Terraform 1.5+ import block style
import {
  to = aws_s3_bucket.raw
  id = "existing-raw-data-bucket"
}

resource "aws_s3_bucket" "raw" {
  bucket = "existing-raw-data-bucket"
}

# Then run:
# terraform plan
# terraform apply
```

```bash
# Practical import flow
terraform import aws_iam_role.glue_role DataPlatformGlueRole
terraform state show aws_iam_role.glue_role
# Copy important attributes into configuration
terraform plan
# Repeat until plan is no-op or intentionally controlled
```

Import is a migration process, not a magic scanner. The goal is a no-op plan
where code, state, and AWS reality all agree.

Importing a production resource with incomplete configuration can cause
Terraform to plan destructive changes on the next apply. Always review the
first post-import plan carefully.

---

[Back to TOC](#toc)

<a id="sec-10"></a>
## Terraform for Data Engineering Infrastructure

Terraform is especially useful for provisioning durable infrastructure around
data pipelines: S3 buckets for raw/curated/artifact zones, IAM roles for
Glue/ECS/Lambda/Airflow, VPC networking, RDS or Aurora for metadata stores,
ECS services, EventBridge schedules, and CloudWatch alarms.

```hcl
resource "aws_glue_catalog_database" "curated" {
  name = "curated_${var.environment}"
}

resource "aws_iam_role" "glue" {
  name = "data-platform-glue-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "glue.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_db_instance" "metadata" {
  identifier          = "metadata-${var.environment}"
  engine              = "postgres"
  instance_class      = "db.t4g.medium"
  allocated_storage   = 100
  storage_encrypted   = true
  skip_final_snapshot = false
}
```

Terraform should create the platform skeleton. Pipeline code, SQL
transformations, and job artifacts should be deployed by application CI/CD,
not buried inside infrastructure state.

Don't let Terraform upload large scripts, data files, or changing artifacts
into S3 on every apply. That mixes infrastructure lifecycle with application
release lifecycle and makes plans noisy.

**What Terraform should and should not manage**

S3 data lake — Manage: buckets, encryption, lifecycle, access policies. Not: data files and daily partitions.
Glue — Manage: catalog DBs, roles, job definitions, connections. Not: rapid script iteration and package builds.
RDS — Manage: instance, subnet group, security group, parameters. Not: schema migrations and seed data.
ECS — Manage: cluster, service, task definition baseline, IAM. Not: frequent container image promotion logic.

---

[Back to TOC](#toc)

<a id="sec-11"></a>
## Secrets, Sensitive Values, and State Exposure

State can contain sensitive values even when variables are marked
`sensitive = true`. The flag hides values from CLI output — it does not
remove them from state. Secrets should live in Secrets Manager, SSM Parameter
Store, Vault, or a CI/CD secret store. Terraform can create secret containers
and access policies, but it should not casually store the secret values.

```hcl
resource "aws_secretsmanager_secret" "db_password" {
  name = "data-platform/${var.environment}/metadata-db-password"
}

# Better: create the secret container and let a secure rotation process
# set the value. Avoid hardcoding secret_string in Terraform.
```

Terraform manages where secrets live and who can access them.
It should rarely manage the secret payload itself.

A secret passed into Terraform can end up in state, logs, crash files,
plan files, or CI artifacts. Treat plan files and state files as sensitive.

**Patterns**

Plain variable password — High risk. Avoid.
`sensitive = true` — Still in state. Useful for output masking only.
Secrets Manager container only — Low risk. Preferred for most teams.
External rotation — Low risk. Best for production databases.

---

[Back to TOC](#toc)

<a id="sec-12"></a>
## Drift Detection and Remediation

Drift happens when real infrastructure changes outside Terraform: someone
edits an IAM policy in the console, changes an RDS parameter manually,
deletes a security group rule, or modifies bucket encryption. Terraform
detects drift during plan by reading provider APIs and comparing reality
against state and configuration.

```bash
# Detect drift without applying
terraform plan -detailed-exitcode

# Exit codes:
# 0 = no changes
# 1 = error
# 2 = changes present
```

Drift is not always bad. Emergency fixes happen. The discipline is to
reconcile the change back into code or revert it intentionally.

Blindly applying after drift detection can undo an emergency production
change. Review whether the drift is a bug, a hotfix, or an unauthorized mutation.

**Drift types**

Manual hotfix — Temporary security group rule. Convert to code or remove after incident.
Console accident — Bucket policy edited incorrectly. Apply Terraform to restore desired state.
Provider default change — AWS default attribute differs. Pin provider or add explicit config.
External controller — Kubernetes or autoscaler changes a count. Use lifecycle ignore carefully.

---

[Back to TOC](#toc)

<a id="sec-13"></a>
## CI/CD with GitHub Actions and OIDC

Terraform should run through a controlled pipeline for shared environments.
GitHub Actions can authenticate to AWS using OIDC — no long-lived access keys.
Common pattern: pull requests run format, validate, and plan; main branch
approval runs apply. Production applies should require environment protection,
code review, and sometimes a manual approval gate.

```yaml
name: terraform

on:
  pull_request:
  push:
    branches: [ main ]

permissions:
  id-token: write
  contents: read

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-terraform-role
          aws-region: us-east-1

      - uses: hashicorp/setup-terraform@v3

      - run: terraform init
      - run: terraform fmt -check -recursive
      - run: terraform validate
      - run: terraform plan -out=tfplan

      - name: Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve tfplan
```

OIDC lets GitHub request short-lived AWS credentials — much safer than
storing an AWS access key as a repository secret.

Never run automatic production apply from every branch. Plans from
untrusted pull requests can expose values through logs or abuse provider
credentials if the workflow is not locked down.

**Pipeline controls worth having**

Provider lock file — Keeps provider versions reproducible.
Plan artifact retention limits — Plan files can contain sensitive values.
Environment approval — Prevents accidental prod mutation.
Policy checks — Blocks public buckets, weak IAM, missing encryption.

---

[Back to TOC](#toc)

<a id="sec-14"></a>
## Terraform vs CloudFormation

Both manage infrastructure as code. They optimize for different realities.
CloudFormation is AWS-native and often supports AWS features early. Terraform
is provider-neutral with a mature module ecosystem.

Choose Terraform when the platform spans AWS plus external services, or when
module reuse and cross-provider workflow matter.
Choose CloudFormation when AWS-native integration, StackSets, or first-class
AWS support matter more.

Never split ownership of the same resource between Terraform and CloudFormation.
One resource, one infrastructure authority.

**Scope** — Terraform: multi-cloud and third-party. CloudFormation: AWS-native.
**Language** — Terraform: HCL. CloudFormation: YAML or JSON.
**State** — Terraform: managed by backend. CloudFormation: managed by AWS service.
**Feature freshness** — Terraform: depends on provider updates. CloudFormation: often earlier for AWS.
**Ecosystem** — Terraform: strong module registry. CloudFormation: strong AWS-native governance.

---

[Back to TOC](#toc)

<a id="sec-15"></a>
## Interview Q&A

**Q: What is Terraform state, and why is it risky in production?**

State maps Terraform resource addresses to real cloud resources and stores
many resource attributes. Losing it breaks ownership. Corrupting it causes
wrong plans. Exposing it can leak infrastructure topology and sensitive values.

---

**Q: How would you design Terraform state for dev, test, and prod?**

Separate state files, separate backend keys, ideally separate AWS accounts.
Shared modules keep code reusable, but state isolation keeps blast radius,
IAM permissions, and promotion boundaries clean.

---

**Q: Why use S3 plus DynamoDB for Terraform backend storage?**

S3 provides durable, versioned, encrypted state storage. DynamoDB provides
locking so two applies don't mutate the same state simultaneously. Together
they solve collaboration and recovery better than local state.

---

**Q: What should Terraform manage in a data engineering platform?**

Durable infrastructure: S3 buckets, IAM roles, VPC networking, Glue resources,
RDS instances, ECS services, EventBridge rules, KMS keys, and monitoring.
Not daily data files, schema migrations, or fast-changing application artifacts.

---

**Q: How do you handle secrets with Terraform?**

Avoid putting secret values directly in Terraform. Let Terraform create the
secret container and IAM permissions, then use Secrets Manager, SSM, Vault,
or a rotation process to set the actual value. Marking a variable sensitive
hides output but does not remove the value from state.

---

**Q: When would you choose CloudFormation over Terraform?**

When the org is AWS-only, needs native governance, wants StackSets, or
requires immediate support for new AWS features. Terraform wins when
cross-provider infrastructure, reusable modules, and a wider ecosystem
matter more.
[Back to TOC](#toc)

