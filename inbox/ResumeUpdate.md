# Instructions for Local Code Agent: Build Sean Girgis's Resumes

## Mission

Build polished, truthful, ATS-friendly resumes for **Sean Luka Girgis** using the local career source files. The immediate goal is to obtain **part-time, remote, evening/weekend income**, while remaining open to **higher-income senior roles**.

Create two targeted resume versions:

1. **Part-Time Consulting Resume â€” priority deliverable**
   - Target: freelance projects, fractional consulting, and flexible part-time work.
   - Availability: evenings/weekends, ideally 5â€“15 hours per week.
   - Focus: Python automation, AI workflow automation, data integration, report automation, Splunk/APM/observability, capacity reporting, Power BI cataloging, RAG/knowledge-base prototypes, and mentoring.

2. **Senior Career Resume â€” secondary deliverable**
   - Target: high-income senior full-time, contract, or consulting opportunities.
   - Focus: senior data engineering, capacity and performance engineering, AI-enabled infrastructure optimization, Python/SQL/ETL, AWS, PySpark, forecasting, observability, and enterprise delivery.

Do not merely reformat an old resume. Rebuild the content around the target audience and the strongest verified evidence.

## Source-of-truth rules

Start by locating and reading these sources, if present:

- `sean_girgis_searchable_profile.md`
- Current and previous resumes (`.docx`, `.pdf`, `.md`, `.txt`)
- `data/master/master_career_data.yaml`
- `data/master/skills.yaml`
- `data/master/bofa_stated_ai_work.md`
- `SEAN.md`
- `SEAN_NOW.md`
- Relevant project documentation that verifies technologies, dates, or results

Search the working directory recursively rather than assuming exact parent paths. Treat `master_career_data.yaml` and `skills.yaml` as authoritative where available. Use the searchable profile for positioning, but cross-check it against the master sources.

Never invent or infer an employer, title, date, certification, degree, technology, production status, project result, or metric. If sources conflict, do not silently choose one. Record the conflict in `resume_questions_for_sean.md` and use only the safest verified wording in the draft.

## Essential positioning

Sean's core story is:

> A senior capacity, performance, and data engineer who uses practical AI and automation to improve operational workâ€”not a generic candidate attempting to switch careers into AI.

For part-time/freelance work, make the value proposition immediately understandable to a buyer:

> Senior enterprise engineer who automates manual data, reporting, and operational workflows using Python and practical AI, with deep capacity, performance, Splunk/APM, and observability experience.

The part-time resume should lead with business problems Sean can solve, not with a vague senior title or a long list of tools.

## Privacy and accuracy safeguards

- Do not include confidential, proprietary, or internal Bank of America or LTIMindtree information.
- Do not expose internal prompts, data, screenshots, architecture, credentials, URLs, identifiers, or unlisted tools.
- Describe current work only at a sanitized, portable business-outcome level.
- Treat **CAPTAIN as research/investigation**, not a deployed production system.
- Do not claim beginner/self-studied technologies as production expertise. This specifically includes Databricks, Delta Lake, dbt, Snowflake, Unity Catalog, DLT, and Azure data-platform foundations unless a stronger source explicitly verifies professional use.
- Distinguish AI-assisted development, prototypes, research, and production work.
- Do not show Sean's age, birth date, photo, marital status, religion, full street address, or references.
- Use Murphy, Texas / Dallasâ€“Fort Worth only if useful; do not add a street address.
- Include U.S. citizenship or work authorization only if appropriate for the intended version.
- Do not place â€œseeking side incomeâ€ on the resume. Use professional wording such as â€œAvailable for select remote evening/weekend engagementsâ€ only on the consulting version.
- Do not write anything suggesting current employer resources or time will be used for outside work.

## Resume A: Part-Time Consulting

### Target headline

Use or improve this, without exaggeration:

**Python & AI Automation Consultant | Data Workflows | Reporting | Splunk/APM**

### Length and structure

Keep the resume to **two pages maximum** using this approximate order:

1. Name and contact line
2. Target headline
3. Three- to five-line value summary
4. Consulting capabilities / services
5. Selected outcomes or representative projects
6. Relevant professional experience
7. Focused technical skills
8. Education and selected certifications

### Content emphasis

Emphasize verified examples such as:

- Python and AI-assisted workflow automation
- Automated data collection and reporting
- JIRA, MSSQL, and Splunk integrations used as capacity data sources
- Capacity/performance analysis, forecasting, and reporting
- APM and observability: CA APM, Dynatrace, AppDynamics, BMC TrueSight, and Splunk-related work
- Power BI cataloging, organization, and migration support using Copilot/AI/Python
- RAG/FAISS, knowledge-base, and agentic workflow projects, with prototype or project status stated honestly
- Python, SQL, Pandas, ETL, APIs, Linux/Unix, PowerShell, and AWS
- Mentoring or enablement in analytics, data engineering, automation, and practical AI usage when supported by the sources

Prioritize compact engagements that a client could buy: reporting automation, data cleanup and integration, API-based workflows, operational dashboards/catalogs, observability analysis, capacity forecasting, and small knowledge-base solutions.

Use results only when verified. Candidate metrics in the source material include approximately **1.5 hours saved per capacity report**, approximately **2,700 reports annually**, a **90% reduction in forecasting cycles**, telemetry from **6,000+ endpoints**, and large APM estates. Verify each metric and its context before using it. Do not repeat the same metric in multiple sections.

Older roles should be compressed into an â€œEarlier Experienceâ€ section unless directly relevant to the consulting offer. Preserve the depth of experience without making the document feel dated.

### Availability statement

Near the summary or contact block, add a restrained statement such as:

**Available for select remote evening and weekend consulting engagements.**

Do not state a rigid 4â€“8 or 5â€“15 hour limit unless Sean confirms it during the build.

## Resume B: Senior Career / Higher-Income Roles

### Target headline

Use or improve this:

**Senior Data Engineer | Capacity Planning, Performance & AI-Driven Infrastructure Optimization**

### Length and structure

Aim for **two pages**, allowing a third only if removal would hide material, directly relevant enterprise accomplishments. Use:

1. Name and contact line
2. Target headline
3. Executive summary
4. Core competencies
5. Professional experience in reverse chronological order
6. Selected projects, if they add evidence not already shown
7. Technical skills
8. Education and certifications

### Content emphasis

Show the combination of:

- Capacity planning, performance engineering, forecasting, and operational risk reduction
- Python, SQL, Oracle/MSSQL, Pandas, ETL/ELT, telemetry pipelines, data quality, and visualization
- AWS, PySpark/Spark, Airflow, Docker, Parquet, and related data-platform skills at the level verified by sources
- APM/observability depth across CA APM, Dynatrace, AppDynamics, BMC TrueSight, and Splunk
- Practical AI augmentation: automated reporting, data-source integration, agentic workflows, RAG/FAISS, Copilot-assisted solutions, and forecasting
- Experience delivering in banking, regulated enterprises, telecom, travel/hospitality, utilities, and government environments

Give current and recent work the most space. Consolidate early-career roles while preserving major accomplishments such as large-scale APM deployments and the Sabre migration when verified.

## Writing standards

- Use clear U.S. English and a confident, factual tone.
- Write accomplishment bullets, not job-description inventories.
- Start bullets with strong verbs and show: **problem/action + technology/method + result**.
- Prefer specific evidence over adjectives such as â€œinnovative,â€ â€œdynamic,â€ or â€œresults-driven.â€
- Keep most bullets to one or two lines.
- Avoid first-person pronouns.
- Avoid keyword stuffing, skill bars, star ratings, icons, graphics, tables, text boxes, columns, headers/footers containing critical text, and decorative timelines.
- Spell out uncommon abbreviations on first use when space allows.
- Do not claim Sean personally built every component if the source only supports team participation.
- Do not copy source sentences mechanically. Rewrite them into concise resume language without changing their meaning.
- Avoid repetitive bullets across Summary, Projects, and Experience.

## ATS and formatting requirements

- Use a single-column layout.
- Use standard section headings.
- Use an ATS-safe font such as Aptos, Calibri, Arial, or Helvetica at approximately 10.5â€“11.5 pt.
- Make Sean's name prominent, but keep styling restrained.
- Use consistent date formats and right/left alignment that survives text extraction.
- Ensure hyperlinks remain clickable in DOCX and PDF, but also display understandable link text.
- Include email, phone, LinkedIn, GitHub, and portfolio/site only when verified and useful.
- Do not include X/Twitter unless a target use case clearly benefits from it.
- Put the most relevant keywords naturally in the headline, summary, skills, and evidence bullets.
- Avoid page breaks that split an employer heading from its first bullet.
- Remove hidden metadata, comments, tracked changes, and placeholder text before final delivery.

## Required outputs

Create a folder named `resume_output` and produce:

1. `Sean_Girgis_Part_Time_Consulting_Resume.docx`
2. `Sean_Girgis_Part_Time_Consulting_Resume.pdf`
3. `Sean_Girgis_Part_Time_Consulting_Resume.txt` â€” plain-text ATS extraction
4. `Sean_Girgis_Senior_Career_Resume.docx`
5. `Sean_Girgis_Senior_Career_Resume.pdf`
6. `Sean_Girgis_Senior_Career_Resume.txt` â€” plain-text ATS extraction
7. `resume_questions_for_sean.md`
8. `resume_build_report.md`

The build report must state:

- Which sources were used
- Which facts or metrics were omitted because they could not be verified
- Any source conflicts and how they were handled
- Page count of each PDF
- Whether DOCX and PDF text extraction succeeded
- Whether any text was clipped, overlapped, or placed outside the page
- The primary job families and ATS keywords targeted in each version

## Questions to resolve before declaring final

Do not halt the first draft for every missing detail. Build the safest draft, then place concise questions in `resume_questions_for_sean.md`. At minimum verify:

- Exact LTIMindtree start date and official title
- Whether the client name â€œBank of Americaâ€ may be stated publicly
- Whether current-role accomplishments may be quantified publicly
- Correct end date for Citi and whether there is any overlap/gap to explain
- Preferred displayed name: Sean Girgis or Sean Luka Girgis
- Whether to display Murphy, TX, DFW, or â€œDallasâ€“Fort Worth, TXâ€
- Preferred availability wording and weekly hour range
- Whether the consulting resume should mention current employment
- Which phone, email, LinkedIn, GitHub, and portfolio links are current
- Whether Brainbench certifications should remain

If Sean answers these questions, update both resumes and repeat validation.

## Validation procedure

Before finishing:

1. Render every DOCX to PDF using LibreOffice, Microsoft Word automation, or another reliable renderer.
2. Inspect every rendered page visually at normal zoom for clipping, awkward wrapping, excess whitespace, dense sections, broken bullets, and orphaned headings.
3. Extract text from every PDF and compare it with the intended content.
4. Confirm there are no unsupported claims, duplicate bullets, spelling errors, placeholders, or confidential details.
5. Confirm page limits and that the most important content appears on page one.
6. Confirm both versions are meaningfully targetedâ€”not merely different headlines on identical content.
7. If rendering or extraction fails, fix the cause and rerun validation rather than declaring success.

## Optional targeted variants

After the two base resumes are approved, the agent may derive focused copies for a real job posting or freelance opportunity. Do not create numerous speculative variants. Prioritize these families:

- Python / AI workflow automation consultant
- Data integration / ETL / reporting automation
- Splunk / APM / observability consultant
- Capacity planning / performance engineering consultant
- Senior data engineer / AWS / PySpark
- AI enablement, evaluator, or technical mentor

For a targeted variant, preserve all truth and privacy rules, add only keywords supported by Sean's experience, and provide a short match/gap analysis separately from the resume.

## Definition of done

The task is complete only when both resume versions exist in DOCX, PDF, and clean plain text; all content is source-supported and sanitized; the PDFs have been visually inspected; ATS extraction is readable; unresolved facts are documented; and the consulting resume clearly presents Sean as available for selective remote evening/weekend engagements without implying a second full-time job.