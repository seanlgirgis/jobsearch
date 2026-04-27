JobSearch Modes: What C and D Mean

A1 = DISCUSS_AND_ADVISE
- Strategy conversation only.
- No pipeline files unless you explicitly ask.

B1 = SCORE_JOB
- Creates score report text only.
- Output target: score_report.md content.

C1 = TAILOR_RESUME_INTERMEDIATE
- Creates pipeline input for resume generation.
- Outputs TWO files:
  1) tailored_data_v1.yaml
  2) resume_intermediate_v1.json
- This is NOT a final resume DOCX. It is intermediate structured data.

D1 = COVER_INTERMEDIATE
- Creates pipeline input for cover letter rendering.
- Outputs ONE file:
  1) cover_intermediate_v1.json
- This is NOT final cover.docx. It is intermediate structured data.

How to call by ID

Use this pattern in ChatGPT Project:

MODE_ID: C1
JOB:
<paste full job posting>
CONSTRAINTS:
- optional notes

Expected behavior by mode
- A1: advice only
- B1: score_report.md content
- C1: tailored_data_v1.yaml + resume_intermediate_v1.json
- D1: cover_intermediate_v1.json

Recommended upload set to ChatGPT Project
- 00_MODE_README.txt
- 01_MODE_A1_DISCUSS_TEMPLATE.txt
- 02_MODE_B1_SCORE_TEMPLATE.txt
- 03_MODE_C1_TAILOR_RESUME_TEMPLATE.txt
- 04_MODE_D1_COVER_TEMPLATE.txt
- 05_MODE_ROUTER_PROJECT_INSTRUCTION.txt
