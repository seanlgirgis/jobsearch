# FastAI

## What is FastAPI

FastAPI is a modern high-performance Python framework for building APIs
on top of ASGI.\
\
It is commonly used to expose data products, query APIs, metadata
services, model prediction endpoints, pipeline trigger endpoints, and
internal platform control planes.\
\
FastAPI provides:\
- Typed request and response models\
- Automatic validation\
- Generated OpenAPI/Swagger documentation\
- Native async support\
- Clean deployment with containers and cloud-native platforms.

FastAPI is an ASGI-based Python API framework widely used in data and
platform engineering for building scalable, typed, high-performance
services.

# Use Cases

### Serving ML Predictions

Validate request, call model, return response - Backend systems: loaded
model, SageMaker, BedRock, feature store

### Data Access API

Expose controlled Query Endpoints - Backend systems: PostgreSQL,
Snowflake, Athena, OpenSearch

### Pipeline trigger

Receive request and start workflow - Backend systems: Airflow, Step
Functions, Glue, ECS task

### Metadata service

Manage dataset, job, and lineage metadata -- Backend systems: Dynamo DB,
PostgreSQL, OpenSearch

## ASGI, Uvicorn and Runtime model

FastAPI runs on ASGI (Asynchronous Server Gateway Interface), the
async-capable foundation used by modern Python web frameworks. In
production, it\'s typically served by Uvicorn directly, or by Gunicorn
managing a pool of Uvicorn workers.

This matters because the runtime model determines how your API handles
concurrent requests, slow I/O, CPU-bound work, and graceful shutdown.

For data engineering workloads, most endpoints are I/O-heavy: database
reads, AWS service calls, model endpoint queries, job status checks,
metadata fetches. ASGI handles this well because a single worker can
suspend a waiting request and pick up another one, rather than blocking
on a slow network call.

## FastAPI Stack Components

### FastAPI 

Application framework. Handles routes, dependencies, validation, and
auto-generated docs.

### Starlette 

ASGI foundation FastAPI is built on. Provides middleware, routing, and
request/response primitives.

### Uvicorn 

ASGI server. The default choice for containerized deployments.

### Gunicorn 

Process manager. Used to spin up multiple Uvicorn workers on Linux
hosts.

## Async vs Sync endpoints

FastAPI supports both. The right choice depends on what libraries
you\'re calling and the shape of the workload.

Use async def when your endpoint uses async-compatible clients: async
database drivers, async HTTP clients, or anything built for the event
loop.

Use regular def when working with blocking libraries, CPU-bound code, or
any library that doesn\'t support async.

The costly mistake is mixing them blindly. An async def endpoint that
calls a blocking driver or blocking HTTP client will freeze the event
loop. A regular def endpoint waiting on many network calls wastes
concurrency unless you scale workers or switch to async clients.

## Async def vs def Endpoint

async def Use when calling async-compatible clients: async database
drivers, async HTTP clients, or anything built for the event loop.

def Use when working with blocking libraries, CPU-bound code, or
libraries that don\'t support async.

**The costly mistake** Mixing them blindly. An async def endpoint that
calls a blocking driver freezes the event loop. A regular def endpoint
waiting on many network calls wastes concurrency unless you scale
workers or switch to async clients.

## Pydantic Request and Response Models

Pydantic models define request and response contracts as Python types.
FastAPI uses them for validation, serialization, documentation, and
OpenAPI schema generation.

### Why this matters at scale

Request Models Bad input fails before it reaches a warehouse query,
feature lookup, or model endpoint. Validation happens at the boundary,
not inside your business logic.

Response Models Prevent accidental leakage of internal columns, debug
fields, secrets, or oversized payloads. You control exactly what goes
out.

The bigger picture At scale, API contracts become data contracts.
Pydantic is what enforces that boundary.

## Common Pydantic Model Types

Request Model

Rejects malformed input early, before it touches any downstream logic.

Response Model

Controls output shape and hides internal fields, debug data, or
sensitive columns.

Enum / Literal

Prevents invalid modes or unsupported job names from entering the
pipeline.

Field Constraints

Documents expected limits and enforces basic data quality at the
boundary.

## Dependency Injection with Depends

FastAPI\'s dependency injection pattern is built around Depends. It
keeps shared concerns out of route handlers and in one place.

### What belongs behind a dependency

Authentication / Authorization Validate tokens and enforce access rules
before the route handler runs.

Database Sessions Open, yield, and close connections consistently across
routes.

Configuration / Settings Inject environment-aware settings objects
without importing globals.

Platform Clients S3 clients, feature flag services, tracing context,
tenant identity.

Repository Classes Reusable service or data-access classes shared across
multiple routes.

Why it matters for data engineering

Routes frequently need the same platform resources. Putting them behind
dependencies keeps route handlers clean, makes testing easier, and makes
swapping implementations straightforward.

## Common Dependency Layers

Config

get_settings() --- Centralizes environment variables and limits.

Auth

get_current_user() --- Applies identity consistently across routes.

DB

get_session() --- Controls transaction and connection lifecycle.

Service

get_prediction_service() --- Keeps route handlers thin and testable.

## Database Access and Connection Pooling

Opening a fresh connection per request works in demos. In production it
falls apart fast. FastAPI apps scale horizontally, so total database
connections multiply quickly: workers times replicas times pool size
adds up to a number that will overwhelm your database under burst
traffic.

### Common patterns

PostgreSQL Use SQLAlchemy with a configured connection pool. Add
PgBouncer in front if connection count becomes a problem. For async
routes, use async SQLAlchemy or asyncpg directly.

Analytics Warehouses (Snowflake, Athena) Don\'t treat the API like an
open query console. Put guardrails around row limits, query timeouts,
query shape, and user permissions. These systems charge by scan or by
compute, and an unbounded query from an API route is an expensive
surprise.

The rule of thumb Connections are a finite resource. Manage the pool,
not just the query.

## Connection Management Rules

Pool Size

Size the pool from what your database can handle, not from what your API
hopes to need.

Timeouts

Set query and request timeouts explicitly. Never let a slow query hold a
worker indefinitely.

Result Size

Always paginate or cap row counts. Unbounded queries are a reliability
and cost risk.

Transactions

Keep them short. Never hold a lock while waiting on a remote call or
external service.

## FastAPI as a Data API Layer

FastAPI works well here when the API exposes curated operations, not raw
database access. Good endpoints answer specific questions: return this
entity, score this event, start this pipeline, check this job, pull this
approved aggregate.

### What a good data API does

Exposes intent, not implementation. The caller asks for a result, not a
query.

Protects backend systems. Pagination, indexed filters, row limits, and
timeouts keep downstream systems stable under load.

Owns the query logic. Business rules and query shape live in the API
layer, not in the client.

Validates at the boundary. Schema enforcement happens before anything
touches the database.

The warning sign

If an endpoint accepts arbitrary SQL, the API is a liability, not an
asset.

## Data API Shape Patterns

### Metrics 

> Good: filtered endpoint with row limits and indexed params.
>
> Bad: arbitrary SQL string passed in from the client.

### ML Serving 

> Good: typed feature request with a defined schema.
>
> Bad: unvalidated JSON blob sent directly to the model.

### Pipeline Ops 

> Good: trigger by approved job name from a known list.
>
> Bad: shell command submitted by the user.

### Search 

> Good: allowed filters and a safe query DSL.
>
> Bad: direct passthrough to the backend query engine.

## Background Tasks and Pipeline Triggers

FastAPI\'s BackgroundTasks runs lightweight work after the response is
sent. Good for side effects like audit writes, notifications, or metric
emissions. Not a replacement for a durable queue or orchestrator.

### When to use BackgroundTasks

Fire-and-forget side effects that are low stakes and fast. If the work
fails silently, nothing breaks.

### When to use a real queue or orchestrator

Anything that needs durability, retries, visibility, or guaranteed
execution. An API response is not a delivery guarantee.

### Common AWS patterns for pipeline triggers

#### Step Functions 

Start an execution for multi-step workflows with built-in state and
retry logic.

#### ECS 

Task Submit a containerized job for heavier compute work.

#### Lambda 

Invoke directly for short event-driven processing.

#### EventBridge 

Publish an event and let downstream consumers decide what to do with it.

#### Airflow DAG 

Trigger through a controlled API endpoint when orchestration already
lives in Airflow.

## Background Tasks: When to Use What

### Audit Log Write 

> BackgroundTasks works for low-stakes writes. In production, prefer a
> direct write or a queue for durability.

### Email Notification 

> Acceptable for simple cases. In production, route through SQS or
> EventBridge for reliability and retry.

### Glue Job Trigger 

> Skip BackgroundTasks entirely. Call the Glue API directly and return
> the run ID in the response.

### Long ETL 

> Never use BackgroundTasks. Hand off to Airflow, Step Functions, ECS,
> or Glue and let the orchestrator own it.

## Middleware and Cross-Cutting Concerns

> Middleware wraps every request and response. It belongs to
> infrastructure concerns, not business logic.

### What belongs in middleware

> Request IDs, timing, structured logging, security headers, metrics
> emission, and CORS policy.

### What does not belong in middleware

> Business logic, database queries, or anything with meaningful latency.
> Middleware runs on every request.

### CORS

> Only matters when browser clients call your API from a different
> origin. Internal service-to-service calls don\'t need it.

The common production mistake is allowing all origins, all methods, and
credentials together. Each one of those is a separate surface area
decision. Don\'t default all three to open.

## OAuth2, JWT, and API Security

FastAPI includes OAuth2 utilities, but the framework doesn\'t secure the
system on its own. In production, identity comes from an external
provider: Cognito, Okta, Azure AD, Auth0, or an internal service. The
API validates the token, extracts claims, and enforces authorization
rules.

### What a JWT carries

Subject, issuer, audience, scopes, roles, and expiration. All signed.

### What the API must validate

> Signature, expiration, issuer, audience, and required scopes. Decoding
> the token and trusting the JSON is not validation.

**The rule** Treat every inbound token as untrusted until the signature
and claims are verified. Decoding is not the same as validating.

## Security Layers in Production

### Identity Provider 

> Source of truth for identity. Common choices: Cognito, Okta, Azure AD,
> Auth0, or internal SSO.

Token Validation

Verify signature, expiration, issuer, audience, and required scopes. Not
just decode.

Authorization

> Enforce scopes and roles at the route level. Add row-level or
> tenant-level checks where data isolation is required.

Transport

> TLS terminated at the load balancer, API Gateway, or ingress
> controller. Never plain HTTP in production.

## OpenAPI and Swagger as Data Contracts

FastAPI generates OpenAPI schemas and Swagger docs automatically from
routes and Pydantic models. For data teams this isn\'t just a
convenience feature. It\'s a living contract between the API and
everything that calls it.

### Who benefits

> Frontend teams, analytics engineers, notebook users, platform
> engineers, and downstream services all use it to understand how to
> call the API without reading the source code.

### What it feeds downstream

> Client generation, contract testing, governance reviews, and
> documentation portals. One schema, many consumers.

**The mindset shift** Treat the OpenAPI schema as a published artifact,
not a debug tool. If the schema changes, the contract changed.

**\**

## Auto-Generated OpenAPI Endpoints

### /docs 

Swagger UI for interactive exploration and manual testing directly in
the browser.

### /redoc 

Alternative documentation UI with a cleaner read-only layout.

### /openapi.json 

> Machine-readable contract. Feed this to client generators, contract
> tests, or governance tooling.

## Deployment: ECS Fargate vs Lambda

### ECS Fargate 

> The strong default for production APIs. Containers stay warm,
> connection pools persist, and network behavior is stable. Integrates
> cleanly with VPC resources like RDS, ElastiCache, OpenSearch, and
> private subnets. Scaling is predictable.

### AWS Lambda with Mangum 

> Attractive for low-traffic APIs, internal tools, and bursty workloads.
> The Mangum adapter wraps FastAPI for the Lambda runtime. But there are
> real tradeoffs to plan for.

### Cold Starts 

> Python Lambda functions have noticeable cold start latency, especially
> with heavy dependencies.

### Connection Reuse 

> No persistent connection pool between invocations. Each cold start
> reopens connections.

### Payload Limits 

> API Gateway enforces request and response size limits. Not suitable
> for large data transfers.

### API Gateway Behavior 

> Timeout limits, payload constraints, and routing rules differ from a
> standard load balancer setup.

**The decision rule** Long-running, high-traffic, or VPC-integrated APIs
belong on ECS. Lightweight, infrequent, or event-driven APIs are
reasonable Lambda candidates.

## Deployment Options

### ECS Fargate 

> Best for steady APIs, database connection pools, and VPC-heavy
> workloads. Tradeoff: more infrastructure to manage than Lambda.

### Lambda + Mangum 

> Best for low-traffic, event-driven, or internal tool APIs. Tradeoff:
> cold starts and connection constraints at scale.

### EKS 

> Best for large platform teams already running Kubernetes. Tradeoff:
> operational overhead is significant unless Kubernetes is already the
> standard.

## Testing, Observability, and Performance

### Testing

FastAPI\'s TestClient covers the basics. Production-grade tests should
go further: route behavior, dependency overrides, auth enforcement,
validation errors, transaction boundaries, and failure paths. A data API
that only tests the happy path is hiding production surprises.

### Observability

Structured logs, request IDs, latency metrics, error rates, dependency
timing, and backend query timing. If you can\'t see where a slow request
spent its time, you can\'t fix it.

### Performance

Start with the slowest dependency, not the worker count. The bottleneck
is usually a bad query plan, an unbounded warehouse scan, a cold model
endpoint, or a missing index. Scaling workers around a slow query just
spreads the problem.

**The rule** More workers don\'t fix a bad query. Fix the query first.

## Performance Levers and Their Tradeoffs

### More Workers

> Increases concurrency but also increases database connection pressure
> proportionally.

### Async I/O 

> Only helps if the downstream dependencies are actually
> async-compatible. Async routes calling blocking libraries gain
> nothing.

### Caching 

Reduces load effectively but introduces invalidation and data freshness
complexity.

### Pagination 

> Prevents oversized memory and network responses. Should be a default,
> not an afterthought.

### Response Models 

> Enforce clean contracts but carry a validation cost at high request
> volumes. Worth it, but not free.

## When FastAPI Is the Right Choice

### FastAPI fits well 

> when you need a Python-native API with clear contracts, automatic
> documentation, strong validation, and solid performance for I/O-heavy
> workloads. It\'s a natural fit when the team already writes Python for
> data engineering, ML, analytics, orchestration, or platform tooling.

### Where it fits less well

> Thin static site backends with no real API logic. Organizations
> already standardized on another runtime. Ultra-low-latency systems
> where Python\'s overhead matters. Mostly long-running compute
> workloads where the API is just a wrapper around heavy processing.

**The nuance** In those cases FastAPI can still serve as a control
plane: triggering work, checking status, enforcing contracts. Just not
as the compute engine itself.

## FastAPI: When to Choose It and When to Look Elsewhere

### You need typed Python APIs quickly 

Consider another option if you only need a static site or a simple form
backend.

### You serve ML predictions or metadata 

> Consider another option if you need extreme low-latency systems where
> Python\'s overhead is a constraint.

### You expose curated data platform operations 

> Consider another option if the use case is ad hoc analytics query
> serving at warehouse scale.

### You want automatic OpenAPI contracts 

> Consider another option if your platform already mandates a different
> API framework.

## Interview Q&A

### When would you use async endpoints in FastAPI for a data platform?

> I would use async endpoints when the call chain is I/O-bound and
> async-compatible, such as async database drivers or async HTTP calls
> to model services. I would avoid async if the endpoint calls blocking
> libraries like Pandas-heavy code, boto3, or sync database drivers
> unless those calls are isolated properly.

### How do Pydantic models help in production data APIs?

> They make request and response contracts explicit. That protects
> backend systems from malformed input, documents the API through
> OpenAPI, and prevents accidental leakage of internal fields. For data
> teams, that turns an API boundary into a data contract.

### What is the risk of exposing warehouse queries through FastAPI?

> If the API allows arbitrary SQL or unbounded filters, users can
> trigger expensive scans, leak data, or overwhelm the warehouse. A
> better design exposes curated endpoints with validation, limits,
> pagination, authorization, and query patterns that match indexes or
> partitioning.

### How would you manage database connections in a FastAPI service?

> I would create shared engines or pools at application startup, use
> request-scoped sessions, close sessions reliably, and size pools based
> on database capacity. For Postgres at scale, I would consider
> PgBouncer or RDS Proxy depending on deployment style.

### ECS Fargate or Lambda for FastAPI?

> ECS Fargate is usually better for steady APIs, low latency, VPC
> access, and database connection pooling. Lambda with Mangum can work
> well for low-traffic or bursty APIs, but cold starts and relational
> database connection storms need careful handling.

### How would you secure a FastAPI endpoint used by internal data tools?

> I would validate OAuth2 or JWT tokens from a trusted identity
> provider, verify issuer, audience, expiration, and signature, then
> enforce scopes or roles at the endpoint or dependency layer. For data
> APIs, I would also apply tenant, row-level, or dataset-level
> authorization where needed.
