```text id="4m7k2a"
MODE_ID: C2
TASK: Tailor my existing cover letter intermediate JSON for the supplied job posting and return a render-ready JSON artifact.

INPUTS:
1) intake.md
2) cover_intermediate_v1.json

PRIMARY GOAL:
Rewrite the cover letter intermediate toward the target role WITHOUT inventing facts.

VERY IMPORTANT:
Some capabilities may exist in the current cover/resume context but may be under-emphasized because prior direction targeted a different role.

Examples of buried experience that may need to be surfaced when relevant:
- Dynatrace administration
- Synthetic Monitoring
- RUM / EUM
- transaction tracing
- telemetry analysis
- dashboarding
- alerting / thresholds
- onboarding / instrumentation
- scripting / automation
- CA APM
- BMC TrueSight
- AppDynamics
- operational reporting
- observability workflows
- performance engineering
- shell scripting
- Python automation
- AWS data engineering
- ETL pipelines
- PySpark
- forecasting
- data migration
- data quality / reconciliation
- RAG / GenAI / agentic workflows

YOU ARE ALLOWED TO:
- Reframe existing truthful experience
- Promote under-emphasized relevant work
- Shift positioning angle
- Rewrite the intro, body paragraphs, conclusion, and sign-off for stronger alignment
- Surface buried skills/tools already present
- Make the letter tighter, more direct, and more job-specific

YOU ARE NOT ALLOWED TO:
- Invent employers
- Invent dates
- Invent degrees
- Invent certifications
- Invent metrics
- Invent tools never mentioned anywhere
- Invent production experience where none exists
- Claim hands-on experience with a technology unless it is supported by source_of_truth.json or cover_intermediate_v1.json / resume_intermediate_v1.json context

STRICT CAREER TRUTH RULE:
Use source_of_truth.json and the provided cover_intermediate_v1.json as career truth.
If resume_intermediate_v1.json is also provided, you may use it as supporting career truth.
If the job asks for a tool that is not supported by career truth, do NOT claim it.

STRICT SCHEMA RULE:
- Preserve the exact same top-level JSON keys from the input cover_intermediate_v1.json.
- Preserve the same general structure and data types.
- Do not add commentary fields.
- Do not add metadata fields.
- Do not wrap JSON inside another object.
- Do not rename the artifact.

ROLE TARGETING LOGIC:

IF THE ROLE IS OBSERVABILITY / APM / DYNATRACE:
- elevate Dynatrace
- elevate RUM / EUM / Synthetics
- elevate telemetry analysis
- elevate dashboards / alerts / thresholds
- elevate operational visibility
- elevate scripting / automation
- elevate onboarding / instrumentation
- elevate operational reporting
- elevate performance analysis
- elevate dependency mapping / tracing if supported
- elevate upgrade / migration coordination if supported
- reduce AWS / ML / Data Engineering emphasis unless still relevant

IF THE ROLE IS DATA ENGINEERING:
- elevate AWS
- elevate ETL / ELT
- elevate Python / SQL
- elevate PySpark / Spark
- elevate migration
- elevate orchestration
- elevate reconciliation / data quality
- elevate reporting pipelines
- reduce APM-only language unless relevant

IF THE ROLE IS AI / AGENTIC / RAG:
- elevate Bedrock
- elevate RAG
- elevate vector embeddings
- elevate orchestration workflows
- elevate automation pipelines
- elevate GenAI integrations
- keep claims grounded and do not invent frameworks

WRITING QUALITY RULES:
- Keep one coherent persona aligned to the job.
- Keep the letter professional, direct, and contractor-friendly when appropriate.
- Avoid generic praise.
- Avoid overlong paragraphs.
- Avoid “20+ years” unless it helps the role; usually soften seniority to reduce overqualification risk.
- Prefer practical proof over buzzwords.
- Make the candidate materially more interviewable for the specific role.
- Keep body paragraphs focused on job requirements.
- Keep total letter concise and readable.

OUTPUT FORMAT — ABSOLUTELY STRICT:
You must return ONE downloadable file with this exact filename:

cover_intermediate_v1.json

DO NOT rename it.
DO NOT add “clean”.
DO NOT add “customized”.
DO NOT add a timestamp.
DO NOT add job name.
DO NOT add suffixes.
DO NOT return the JSON in the chat body if downloadable file output is available.

FALLBACK ONLY IF DOWNLOADABLE FILE CREATION IS NOT AVAILABLE:
Return EXACTLY ONE inline code block containing ONLY valid JSON.

FALLBACK RULES:
- The code block must contain the complete updated cover_intermediate_v1.json.
- No explanation before it.
- No explanation after it.
- No markdown except the single JSON code block.
- No partial JSON.
- No truncation.

FINAL CHECK BEFORE OUTPUT:
- Filename must be exactly: cover_intermediate_v1.json
- JSON must be valid.
- Schema must match the input.
- No invented facts.
- No commentary.
- No extra files.
```
