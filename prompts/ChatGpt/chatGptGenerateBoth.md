MODE_ID: C0
TASK: Generate or tailor BOTH resume and cover intermediate JSON artifacts for the supplied job posting.

INPUTS:
1) intake.md
2) source_of_truth.json
3) optional resume_intermediate_v1.json template/current draft
4) optional cover_intermediate_v1.json template/current draft

PRIMARY GOAL:
Create two render-ready JSON artifacts for this exact job:
- resume_intermediate_v1.json
- cover_intermediate_v1.json

The artifacts must improve job fit, ATS alignment, recruiter readability, and truthful positioning WITHOUT inventing facts.

CAREER TRUTH:
Use source_of_truth.json as the only career truth.
If current intermediate JSON files are provided, use them as schema/templates and as supporting wording only.
Do not invent employers, dates, degrees, certifications, metrics, tools, or production experience.

IMPORTANT:
Some capabilities may be under-emphasized because prior resumes targeted a different role.

Surface relevant truthful experience when applicable:
- Dynatrace administration
- Synthetic Monitoring
- RUM / EUM
- transaction tracing
- telemetry analysis
- dashboarding
- alerts / thresholds
- onboarding / instrumentation
- CA APM
- BMC TrueSight
- AppDynamics
- ServiceNow user-level ITSM/reporting if relevant
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

STRICT NO-INVENTION RULES:
Do NOT claim:
- hands-on Terraform unless source truth supports it
- hands-on Ansible unless source truth supports it
- Dynatrace API work unless source truth supports it
- PowerShell expertise unless source truth supports it
- ServiceNow administration unless source truth supports it
- Kubernetes production work unless source truth supports it
- Kafka production work unless source truth supports it
- deep Azure ownership unless source truth supports it

If a job asks for a tool not strongly supported:
- do not fake it
- omit it or frame as adjacent/transferable only when truthful
- ServiceNow may be framed only as user-level incident/change/reporting experience if present

ROLE TARGETING LOGIC:

IF ROLE IS OBSERVABILITY / APM / DYNATRACE:
Position as:
Dynatrace / APM / Observability Engineer

Elevate:
- Dynatrace AppMon/Synthetics
- RUM / EUM
- transaction tracing
- dependency visibility
- telemetry analysis
- dashboards, alerts, thresholds
- monitoring onboarding / instrumentation
- performance analysis
- operational reporting
- Python / shell automation
- CA APM / BMC TrueSight / AppDynamics
- incident/change workflow exposure where truthful

Reduce:
- generic data engineering branding
- heavy ML/AI wording
- AWS lakehouse unless relevant

IF ROLE IS DATA ENGINEERING:
Position as:
AWS / Python / ETL / PySpark Data Engineer

Elevate:
- AWS
- ETL / ELT
- Python / SQL
- PySpark / Spark
- migration
- orchestration
- reconciliation / data quality
- reporting pipelines

Reduce:
- APM-only language unless relevant

IF ROLE IS AI / AGENTIC / RAG:
Position as:
AWS Data Engineer / AI Pipeline Engineer

Elevate:
- Bedrock
- RAG
- vector embeddings
- agentic workflows
- orchestration
- automation pipelines
- GenAI integrations

Reduce:
- unsupported framework claims

RESUME JSON RULES:
If resume_intermediate_v1.json is provided:
- preserve the exact same top-level keys
- preserve the same general schema and data types
- rewrite summary, bullets, skills, and projects for this job

If no resume_intermediate_v1.json is provided:
Create this exact schema:

{
  "personal": {
    "full_name": "",
    "phone": "",
    "email": "",
    "linkedin": "",
    "github": "",
    "personal_website": "",
    "preferred_title": ""
  },
  "summary": "",
  "experience": [
    {
      "company": "",
      "title": "",
      "start_date": "",
      "end_date": "",
      "bullets": []
    }
  ],
  "education": [
    {
      "degree": "",
      "institution": "",
      "location": "",
      "dates": ""
    }
  ],
  "skills": {},
  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": []
    }
  ]
}

COVER JSON RULES:
If cover_intermediate_v1.json is provided:
- preserve exact same top-level keys
- preserve same general schema and data types
- rewrite intro, body, conclusion, and sign_off for this job

If no cover_intermediate_v1.json is provided:
Create this exact schema:

{
  "header": {
    "name": "",
    "address": "",
    "phone": "",
    "email": "",
    "date": "",
    "employer_address": ""
  },
  "salutation": "Dear Hiring Manager,",
  "intro": "",
  "body": [],
  "conclusion": "",
  "sign_off": ""
}

WRITING QUALITY:
- one coherent persona
- direct, practical, job-specific
- ATS-optimized without keyword stuffing
- concise impact-first bullets
- no generic praise
- no long cover paragraphs
- reduce overqualification signals unless seniority helps

OUTPUT FORMAT — ABSOLUTELY STRICT:
Return EXACTLY TWO downloadable files with these exact filenames:

resume_intermediate_v1.json
cover_intermediate_v1.json

DO NOT rename them.
DO NOT add clean/custom/final/job/company/date suffixes.
DO NOT put JSON in the chat body if downloadable files are available.
DO NOT include explanations.
DO NOT include commentary.
DO NOT create extra files.

FALLBACK ONLY IF DOWNLOADABLE FILE CREATION IS NOT AVAILABLE:
Return exactly two separate inline code blocks.

First code block:
complete valid JSON for resume_intermediate_v1.json

Second code block:
complete valid JSON for cover_intermediate_v1.json

No explanation before, between, or after.