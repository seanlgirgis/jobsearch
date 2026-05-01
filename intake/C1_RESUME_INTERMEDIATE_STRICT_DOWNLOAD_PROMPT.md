MODE_ID: C1
TASK: Tailor my existing resume intermediate JSON for the supplied job posting and return a render-ready JSON artifact.

INPUTS:
1) intake.md
2) resume_intermediate_v1.json

PRIMARY GOAL:
Reposition the resume toward the target role WITHOUT inventing facts.

VERY IMPORTANT:
Some capabilities may exist in the current resume but are under-emphasized because prior resume direction was targeting a different role.

Examples of buried experience that may need to be surfaced when relevant:
- Dynatrace administration
- Synthetic Monitoring
- RUM / EUM
- transaction tracing
- telemetry analysis
- dashboarding
- onboarding / instrumentation
- scripting / automation
- CA APM
- operational reporting
- observability workflows
- migration support
- performance engineering
- shell scripting
- Python automation
- AWS data engineering
- ETL pipelines
- PySpark
- forecasting
- data migration
- data quality / reconciliation

YOU ARE ALLOWED TO:
- Reframe existing truthful experience
- Promote under-emphasized relevant work
- Shift positioning angle
- Rewrite bullets for stronger alignment
- Surface buried skills/tools already present
- Reorganize summary, skills, projects, and bullets for ATS alignment

YOU ARE NOT ALLOWED TO:
- Invent employers
- Invent dates
- Invent degrees
- Invent certifications
- Invent metrics
- Invent tools never mentioned anywhere
- Invent production experience where none exists
- Claim hands-on experience with a technology unless it is supported by source_of_truth.json or the input resume_intermediate_v1.json

STRICT CAREER TRUTH RULE:
Use source_of_truth.json and resume_intermediate_v1.json as the only career truth.
If the job asks for a tool that is not supported by career truth, do NOT claim it.
If useful, place unsupported-but-learning tools only in a clearly labeled “Learning / Exposure” skill group if that group already exists or can safely replace a less useful skills group without breaking schema.

STRICT SCHEMA RULE:
- Preserve the exact same top-level JSON keys from the input resume_intermediate_v1.json.
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
- Optimize ATS keyword alignment aggressively but naturally.
- Prefer impact-first bullet wording.
- Keep bullets concise and role-targeted.
- Remove or reduce irrelevant emphasis.
- Improve recruiter readability.
- Improve keyword coverage without keyword stuffing.
- Make the candidate materially more interviewable for the specific role.

OUTPUT FORMAT — ABSOLUTELY STRICT:
You must return ONE downloadable file with this exact filename:

resume_intermediate_v1.json

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
- The code block must contain the complete updated resume_intermediate_v1.json.
- No explanation before it.
- No explanation after it.
- No markdown except the single JSON code block.
- No partial JSON.
- No truncation.

FINAL CHECK BEFORE OUTPUT:
- Filename must be exactly: resume_intermediate_v1.json
- JSON must be valid.
- Schema must match the input.
- No invented facts.
- No commentary.
- No extra files.