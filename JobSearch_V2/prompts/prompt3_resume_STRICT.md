# Prompt 3 — C1 Resume Intermediate

Use this prompt after A1 and B1 are complete.

Copy/paste this:

MODE_ID: C1
TASK: Produce strict pipeline artifacts as downloadable files

JOB:
<paste full job posting>

POSITIONING_ANGLE:
<paste exact angle from A1>

RULES:
- source_of_truth.json is the only career truth.
- No invented employers, titles, dates, metrics, tools, education, certifications, projects, or skills.
- One dominant angle only.
- POSITIONING_ANGLE is authoritative.
- The resume summary MUST begin with the exact POSITIONING_ANGLE text provided.
- Do not rewrite, soften, expand, rename, or reinterpret POSITIONING_ANGLE.
- Never replace "AWS Data Engineer" with "AWS ML Data Engineer" unless POSITIONING_ANGLE explicitly says that.
- Keep ML positioned as ML-enabled data engineering, forecasting, scikit-learn, Prophet, and data pipeline support unless the job and source_of_truth.json justify otherwise.
- Do not overstate beginner/learning skills as production expertise.
- Do not claim expert Kafka, TensorFlow, PyTorch, Databricks, Snowflake, Terraform, Kubernetes, or deep learning unless source_of_truth.json supports that exact level.
- Deterministic, parser-safe output only.

OUTPUT:
FILES_READY: tailored_data_v1.yaml,resume_intermediate_v1.json

OUTPUT FORMAT (STRICT):
1) Create EXACTLY two downloadable files/attachments:
   - tailored_data_v1.yaml
   - resume_intermediate_v1.json
2) Do NOT print normal narrative text.
3) After creating files, print one line only:
   FILES_READY: tailored_data_v1.yaml,resume_intermediate_v1.json

If file attachments are NOT available in this chat:
- Output EXACT fallback blocks only, no extra text.
- Each file must be inside a clean, copyable code block.

Fallback format:

=== FILE: tailored_data_v1.yaml ===
<yaml>
=== END FILE ===

=== FILE: resume_intermediate_v1.json ===
<json>
=== END FILE ===

FINAL SELF-CHECK BEFORE ANSWERING:
- Did summary begin with exact POSITIONING_ANGLE plus a period?
- Did output include exactly two files?
- Did output avoid normal narrative text?
- Did output avoid placeholders: Unknown, N/A, TBD, Your Name, Para text?
- Did output avoid invented claims?
- Did output avoid overstating Kafka, TensorFlow, PyTorch, Kubernetes, Databricks, Snowflake, or Terraform?
