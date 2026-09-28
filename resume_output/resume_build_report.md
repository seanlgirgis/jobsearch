# Resume Build Report

## Result

Created a part-time consulting resume and a senior-career resume. Both identify LTIMindtree as Sean's current employer and omit the client name throughout. The consulting version presents availability as selective remote evening/weekend work rather than a second full-time position.

## Sources Used

- `inbox/ResumeUpdate.md`
- `outbox/sean_girgis_searchable_profile.md`
- `data/master/master_career_data.yaml`
- `data/master/skills.yaml`
- `data/master/bofa_stated_ai_work.md`, used only for Sean-stated current-work content and sanitized so the client is not named
- `D:/Workarea/Grok_DIRECTOR/SEAN.md`
- `D:/Workarea/Grok_DIRECTOR/SEAN_NOW.md`

## Accuracy and Privacy Decisions

- Current employer is displayed as LTIMindtree only.
- The client name is omitted from DOCX, PDF, and ATS text.
- The LTIMindtree start date is shown conservatively as 2026 pending confirmation of the month.
- CAPTAIN is not named; the underlying knowledge-base and command-center concept is clearly labeled research/investigation rather than production.
- Current-role metrics of approximately 1.5 hours saved per report and approximately 2,700 reports annually are omitted until Sean confirms they may be stated publicly.
- The derived approximately 4,050 annual hours figure is omitted.
- No Power BI report count is claimed because none is verified.
- Beginner or self-studied Databricks, Delta Lake, dbt, Snowflake, Unity Catalog, DLT, and Azure skills are omitted from the primary skill sections to avoid suggesting production expertise.
- The claim that the Sabre workload was ten times VISA scale is omitted because it is unusually specific and not needed for these base resumes.

## Validation

- Part-time consulting PDF: 1 page.
- Senior-career PDF: 2 pages.
- Both DOCX files were rendered through Microsoft Word to PDF after the packaged LibreOffice renderer was unavailable.
- Every rendered page was inspected as a PNG. No clipping, overlap, broken bullets, missing glyphs, or text outside the page was found.
- DOCX text extraction succeeded for both files.
- PDF text extraction succeeded for both files and produced readable ATS text files.
- Automated checks found no client-name references and no TODO, TBD, or placeholder text in the final DOCX and PDF content.
- DOCX metadata was scrubbed, including Word revision-session identifiers.

## Targeting

### Part-Time Consulting Resume

Primary families: Python automation consultant, AI workflow automation, data integration and reporting automation, capacity/performance consulting, Splunk/APM/observability consulting, Power BI cataloging, and small RAG/knowledge solutions.

Core ATS terms: Python, AI automation, PowerShell, APIs, SQL, Pandas, ETL/ELT, capacity planning, forecasting, Splunk, Power BI, CA APM, Dynatrace, AppDynamics, BMC TrueSight, RAG, FAISS, MCP, and LLM workflows.

### Senior Career Resume

Primary families: senior data engineer, capacity planning engineer, performance engineer, observability/APM engineer, AWS/PySpark data engineer, and AI-enabled infrastructure optimization.

Core ATS terms: Python, SQL, Oracle, Pandas, ETL/ELT, PySpark, Spark, Airflow, AWS S3, Glue, Athena, Bedrock, Parquet, capacity planning, forecasting, data quality, observability, APM, Prophet, scikit-learn, Docker, RAG, FAISS, and LLM agents.
