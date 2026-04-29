# CI/CD with GitHub Actions, Docker, and ECS

---

## What CI/CD Means in Production

CI/CD is the release control system for code, images, infrastructure, data
jobs, task definitions, and configuration. For senior data engineering, the
goal is not only faster deployment. The goal is repeatable delivery with
proof, auditability, rollback, and low operational surprise.

Build once, test once, promote the same artifact. Rebuilding separately for
production weakens the value of staging.

Automation without tests, immutable tags, approvals, and rollback is just a
faster way to ship mistakes.

**Pipeline responsibilities and risks**

Code — lint, test, package. Risk: broken logic shipped.
Image — build reproducible container. Risk: large or vulnerable runtime.
ECR — store immutable image. Risk: mutable tags hide change.
ECS — deploy task definition revision. Risk: task runs but app is unhealthy.
Data — validate schema and quality. Risk: green deploy, wrong output.

---

## Reference Architecture

GitHub as source control, GitHub Actions as the workflow engine, OIDC for
AWS credentials, Docker for packaging, ECR for image storage, ECS Fargate for
runtime, CloudWatch for logs, and Terraform or CloudFormation for
infrastructure.

```
Pull request
  -> lint, unit tests, integration tests
Merge to main
  -> build Docker image
  -> tag with Git SHA
  -> assume AWS role through OIDC
  -> push image to ECR
  -> render ECS task definition
  -> deploy ECS service
  -> run smoke tests
  -> promote or rollback
```

In ECS, the key release object is the task definition revision pointing to a
specific image tag or digest.

Never mix risky infrastructure mutation and routine app deployment in one
unreviewed step.

---

## GitHub Actions Workflow Structure

Workflows are made from triggers, jobs, steps, runners, permissions, and
environments. Pull requests should validate. Protected branch pushes should
deploy through controlled gates.

```yaml
name: ci-cd-ecs
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  id-token: write
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest -q
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-ecs-deploy
          aws-region: us-east-1
```

Use `needs` for dependency order and `environment` for approvals, protected
secrets, and deployment history.

Set explicit workflow permissions. Broad defaults create a quiet security hole.

---

## Docker Multi-Stage Builds

Multi-stage builds separate build-time dependencies from runtime dependencies.
This reduces ECS image pull time, attack surface, and cold deployment friction.

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Small images deploy faster and reduce the time ECS spends pulling layers
before a task can become healthy.

Never bake secrets or environment-specific values into the image. Runtime
config belongs in ECS, Secrets Manager, or Parameter Store.

**Base image options**

`slim` — good compatibility. Not the smallest.
`alpine` — very small. Native dependency pain.
`distroless` — low attack surface. Hard to debug interactively.

---

## Amazon ECR Registry Strategy

ECR stores the image artifacts ECS deploys. Use SHA-based immutable tags,
lifecycle policies, scanning, and clear retention. Human tags are acceptable,
but the pipeline should deploy a known digest or Git SHA tag.

```bash
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.us-east-1.amazonaws.com

docker build -t data-api:${GITHUB_SHA} .
docker tag data-api:${GITHUB_SHA} \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/data-api:${GITHUB_SHA}
docker push \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/data-api:${GITHUB_SHA}
```

Immutable tags make rollback believable. You can redeploy the exact prior
artifact instead of guessing what `latest` used to mean.

`latest` is convenient for demos and dangerous for production. It hides the
artifact identity.

---

## OIDC Authentication to AWS

OIDC lets GitHub Actions assume an IAM role with short-lived credentials.
This removes long-term AWS keys from GitHub Secrets and shifts control into
IAM trust policy conditions.

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
  },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
    },
    "StringLike": {
      "token.actions.githubusercontent.com:sub":
        "repo:seanlgirgis/data-platform:ref:refs/heads/main"
    }
  }
}
```

OIDC is safer because credentials are temporary and scoped by IAM role plus
trust policy.

A loose trust policy can let unexpected branches or workflows deploy to
production.

---

## Pipeline Tests

Testing should be layered: linting, unit tests, integration tests, contract
tests, and smoke tests. Data pipelines also need schema, idempotency, replay,
and data quality checks.

**Test layers**

Unit — runs on pull request. Proves logic works in isolation.
Integration — runs on PR or staging. Proves dependencies work.
Contract — runs before deploy. Proves consumers are not broken.
Smoke — runs after deploy. Proves live service responds.
Data quality — runs after job run. Proves output is trustworthy.

For data workloads, correctness means the data is right, not merely that the
process exited successfully.

A green HTTP health check does not prove the app can reach the database,
queue, cache, or secret store.

---

## ECS Deployment Strategies

ECS rolling updates are simple and good for many stateless services.
Blue/green deployments with CodeDeploy are stronger when you need controlled
traffic shifting, safer rollback, or isolation between old and new task sets.

**Strategies**

Rolling — routine stateless releases. Simpler but old and new tasks overlap.
Blue/green — critical APIs. More moving parts.
Canary — risky changes. Requires strong metrics.
One-off task — batch and backfill jobs. Retry visibility is manual.

```bash
aws ecs update-service \
  --cluster prod-data-platform \
  --service data-api-service \
  --task-definition data-api:42 \
  --force-new-deployment
```

Rolling safety depends on desired count, minimum healthy percent, maximum
percent, target group health, and good readiness checks.

Bad health checks can make ECS declare victory while users see failures.

---

## Environment Promotion

Promotion should move one tested artifact from dev to staging to production.
GitHub Environments can require approvals, protect secrets, and keep a
deployment history per environment.

```yaml
deploy-staging:
  environment: staging
  steps:
    - run: ./deploy.sh staging $GITHUB_SHA

deploy-prod:
  needs: deploy-staging
  environment: production
  steps:
    - run: ./deploy.sh production $GITHUB_SHA
```

The same image should move forward. Only environment configuration should
change.

If production rebuilds the image, staging did not truly validate the
production artifact.

---

## Secrets Management

Separate deployment credentials from runtime secrets. Use OIDC and IAM for
deployment. Use AWS Secrets Manager or SSM Parameter Store for application
secrets referenced by ECS task definitions.

**Secret stores**

GitHub Secrets — CI-only external tokens. Easy to overuse.
Secrets Manager — rotating secrets. Higher cost.
Parameter Store — config and secure strings. Rotation is manual.
ECS task definition — runtime reference. Plain env vars can leak.

```json
"secrets": [
  {
    "name": "DATABASE_PASSWORD",
    "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/db/password"
  }
]
```

Good pipelines avoid exposing secrets in source, Docker layers, logs,
Terraform outputs, and command echoes.

Terraform state may contain sensitive values. Protect the backend like
production data.

---

## Infrastructure as Code

Terraform or CloudFormation should define ECR, ECS services, IAM roles,
target groups, log groups, networking, alarms, and deployment roles. Run plan
on pull requests and apply only through protected paths.

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/ecs/data-api.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

A Terraform plan in a pull request turns infrastructure into a reviewable
contract.

Never run applies against shared state without locking and least-privilege IAM.

---

## Data Engineering CI/CD

Data engineering releases include Glue jobs, Lambda functions, Airflow DAGs,
ECS workers, dbt models, schema migrations, Step Functions, and data quality
rules. A deployment may be technically healthy but analytically wrong.

**Artifact deploy and validate patterns**

Glue job — update script and job definition. Validate: run sample dataset.
Lambda — zip or image. Validate: invoke test event.
Airflow DAG — sync DAG. Validate: parse and dry run.
ECS worker — task definition. Validate: retry and idempotency.
dbt — model run. Validate: schema and freshness tests.

Data release contracts include schema, partitioning, ordering, idempotency
keys, late data, and replay behavior.

A nightly batch can hide a bad deployment for hours. Build early warning
checks into the pipeline.

---

## Rollback and Observability

Rollback usually means redeploying a previous ECS task definition or letting
CodeDeploy shift traffic back. It only works cleanly if images are immutable
and schema changes are backward-compatible.

```bash
aws ecs describe-services \
  --cluster prod-data-platform \
  --services data-api-service \
  --query 'services[0].taskDefinition'

aws ecs update-service \
  --cluster prod-data-platform \
  --service data-api-service \
  --task-definition data-api:41
```

Practice rollback before an outage. Keep prior task definitions and image
tags available.

Database migrations can make rollback impossible. Use expand-and-contract
changes for risky schema work.

**Observability signals**

ECS events — ECS console and API. Task placement and start failures.
Logs — CloudWatch Logs. Application exceptions.
Target health — ALB. Load balancer reachability.
Metrics — CloudWatch. Latency, errors, saturation.

---

## Silent Deployment Failures

Silent failures happen when the pipeline is green but production behavior is
wrong. Common with ECS because the platform can stabilize tasks even when the
business function is broken.

**Failure modes**

Wrong image — mutable tag changed. Prevention: use SHA or digest.
Bad health check — shallow endpoint. Prevention: readiness checks.
Missing env var — unsafe fallback. Prevention: fail-fast startup.
IAM gap — only fails on edge path. Prevention: integration tests.
Schema drift — app starts fine. Prevention: contract checks.

Test the actual user or consumer path: endpoint, queue message, job trigger,
database write, or output file.

The scariest pipeline is not red. It is green and wrong.

---

## Interview Q&A

**Q: Why use OIDC instead of AWS keys in GitHub Secrets?**

OIDC uses short-lived credentials through IAM role assumption. There is no
long-term key to leak, and access can be scoped by repo, branch, workflow,
and environment.

---

**Q: How should Docker images be tagged for ECS?**

Use immutable Git SHA tags or image digests. Optional release tags are fine,
but production deployment should know the exact artifact identity.

---

**Q: Rolling update or blue/green?**

Rolling is simpler for normal stateless services. Blue/green is safer for
critical workloads that need controlled traffic shift, validation, and fast
rollback.

---

**Q: What tests matter for data engineering CI/CD?**

Unit, integration, contract, smoke, schema, freshness, uniqueness,
idempotency, and replay tests. The output data must be trusted, not merely
produced.

---

**Q: How do you safely run Terraform in CI/CD?**

Plan on pull requests, apply only from protected branches or environments,
use remote state with locking, limit IAM permissions, and separate risky
infrastructure changes from routine app deploys.

---

**Q: Why can an ECS deployment look successful while the app is broken?**

ECS may only know that tasks are running. Bad environment variables, shallow
health checks, missing IAM, dependency failures, or schema drift can still
break the real workload.
