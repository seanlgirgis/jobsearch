# Job Search Master Guide — Sean Luka Girgis
**Last Updated: April 2026 | Location: Murphy TX (DFW) | Open to: Remote / Hybrid / On-site DFW**

> This is your single source of truth for job searching. Everything is rated by effectiveness (descending). Treat it as a living document — update salary ranges and active companies as market shifts.

---

## Table of Contents
1. [Your Competitive Position](#1-your-competitive-position)
2. [Job Search Sites — Rated by Strength](#2-job-search-sites--rated-by-strength)
3. [Role Titles to Search — Rated by Fit](#3-role-titles-to-search--rated-by-fit)
4. [Search Terms & Keywords — Rated by Strength](#4-search-terms--keywords--rated-by-strength)
5. [Boolean Search Strings — Ready to Paste](#5-boolean-search-strings--ready-to-paste)
6. [Google X-Ray Strings](#6-google-x-ray-strings)
7. [Companies to Target Directly](#7-companies-to-target-directly)
8. [Recruiter Outreach Strategy](#8-recruiter-outreach-strategy)
9. [LinkedIn Profile Optimization](#9-linkedin-profile-optimization)
10. [DFW Market Notes](#10-dfw-market-notes)
11. [Remote vs Hybrid vs On-Site Strategy](#11-remote-vs-hybrid-vs-on-site-strategy)
12. [Salary Ranges & Negotiation Anchors](#12-salary-ranges--negotiation-anchors)
13. [Handling the Name Change](#13-handling-the-name-change)
14. [Daily Search Routine](#14-daily-search-routine)
15. [Application Tracker Checklist](#15-application-tracker-checklist)

---

## 1. Your Competitive Position

### Strengths (Lead with These)
| Strength | Evidence | Differentiator Level |
|---|---|---|
| 20+ yrs enterprise IT — Python, SQL, Linux | Citi, AT&T, Sabre, Ericsson | Very High |
| PySpark ETL @ scale (6,000+ endpoints) | Citi telemetry pipelines | Very High |
| AWS serverless data platform | Glue, Athena, S3, Bedrock, Redshift | High |
| Capacity Planning + ML forecasting | Prophet + scikit-learn, 15 yrs CP | Very High |
| GenAI / Text-to-SQL agent (production) | Claude 3 Sonnet at Citi | High |
| Full monitoring stack SME | CA APM, Dynatrace, AppDynamics, BMC | High |
| US Citizen, no sponsorship ever | Immediate start | High (removes friction) |
| DFW local — no relocation needed | Murphy TX | High |

### Honest Gaps (Prepare Answers)
| Gap | Mitigation |
|---|---|
| Databricks: 0 prod years | Self-studying Delta Lake, DLT, Unity Catalog, Workflows — bridge from Glue/PySpark |
| dbt: 0 prod years | Self-studying dbt-core with dbt-duckdb locally; SQL transform work at Citi is equivalent |
| Snowflake: 0 prod years | Self-studying; Redshift + Athena experience maps directly |
| Azure: 0 prod years | Foundational upskilling; AWS depth transfers |
| Certifications: Brainbench only (2000s) | Older certs; offset with 20 yrs production proof and current AI work |

### Your Best Pitch (30-Second Version)
> "Senior Data Engineer with 20 years of enterprise experience. At Citi I built PySpark ETL pipelines processing telemetry from 6,000+ servers, migrated ML workloads to AWS, and shipped a GenAI Text-to-SQL agent using Claude and Bedrock. I specialize in serverless AWS data platforms, capacity forecasting, and performance monitoring. US citizen in DFW, open to remote or hybrid."

---

## 2. Job Search Sites — Rated by Strength

**Rating key:** ★★★★★ = Use daily | ★★★★☆ = Use 3×/week | ★★★☆☆ = Check weekly | ★★☆☆☆ = Set alerts only | ★☆☆☆☆ = Niche / occasional

### Tier 1 — Use Daily ★★★★★

| Platform | URL | Why It's Tier 1 |
|---|---|---|
| **LinkedIn Jobs** | linkedin.com/jobs | Largest active pool, recruiter DMs, Easy Apply, algorithms surface you when active, DFW + remote filters work well |
| **Indeed** | indeed.com | Highest raw volume in DFW tech; smaller companies not on LinkedIn; set email alerts by title+location |
| **Dice** | dice.com | Tech-only; recruiters specifically for tech roles; good for mid-size companies overlooked on LinkedIn |

### Tier 2 — Use 3× per Week ★★★★☆

| Platform | URL | Why |
|---|---|---|
| **Glassdoor Jobs** | glassdoor.com/Job | Salary data + reviews help you filter; real job posts, not just scraped |
| **Built In Dallas** | builtindallas.com | DFW tech scene only — refreshes daily, curated startups and growth companies |
| **Levels.fyi Jobs** | levels.fyi/jobs | Big tech / FAANG-adjacent roles with full comp transparency (TC = base + RSU + bonus) |
| **Google Jobs** | google.com → search "data engineer Dallas" | Aggregates from everywhere — catches postings missed by individual boards |

### Tier 3 — Check Weekly ★★★☆☆

| Platform | URL | Why |
|---|---|---|
| **Wellfound (AngelList)** | wellfound.com/jobs | Startups + fintech seed-to-Series C; direct founder contact; AI/data roles exploding |
| **Otta** | app.otta.com/jobs | Curated quality over quantity; good signal-to-noise for senior roles |
| **Hired** | hired.com | Reverse recruiting — you create profile, companies pitch you; tech focus |
| **ai-jobs.net** | ai-jobs.net | AI/ML data engineering roles specifically; smaller but targeted |
| **DataJobs** | datajobs.com | Data-only board; good for niche data engineering titles |
| **FinancialJobsWeb** | financialjobsweb.com | Financial services / banking focus — aligns with Citi background |
| **Blind** | teamblind.com | Tech insider job posts + referral threads; also great for comp data |

### Tier 4 — Set Alerts, Check Monthly ★★☆☆☆

| Platform | URL | Why |
|---|---|---|
| **ZipRecruiter** | ziprecruiter.com | Recruiter-driven; set alert and let them come to you |
| **CareerBuilder** | careerbuilder.com | Older but catches enterprise / government-adjacent roles |
| **SimplyHired** | simplyhired.com | Aggregator; catches outliers missed elsewhere |
| **Monster** | monster.com | Lower signal but large pool; enterprise and staffing agency heavy |
| **FlexJobs** | flexjobs.com | Remote/flex-verified jobs; paid subscription, use only if prioritizing remote only |
| **We Work Remotely** | weworkremotely.com | Remote-only board; mostly startups |
| **Remotive** | remotive.com/remote-jobs | Remote jobs, tech focus |
| **Remote OK** | remoteok.com | Tech remote roles; skews startup |

### Tier 5 — Niche / Situational ★☆☆☆☆

| Platform | URL | When to Use |
|---|---|---|
| **USAJOBS** | usajobs.gov | Federal/government tech roles; US citizen is required — you qualify; slower process |
| **GovernmentJobs** | governmentjobs.com | State/local government tech; stable, pension, but lower comp |
| **Greenhouse direct** | boards.greenhouse.io | Search Google: `site:boards.greenhouse.io "data engineer"` |
| **Lever direct** | jobs.lever.co | Search Google: `site:jobs.lever.co "senior data engineer"` |
| **Workday direct** | myworkdayjobs.com | Search Google: `site:myworkdayjobs.com "capacity planning engineer"` |

---

## 3. Role Titles to Search — Rated by Fit

**Rating:** ★★★★★ = Perfect match | ★★★★☆ = Strong match | ★★★☆☆ = Good match, some stretch | ★★☆☆☆ = Adjacent, worth reading | ★☆☆☆☆ = Stretch, only if description fits

### Data Engineering Core ★★★★★

| Title | Why It Fits |
|---|---|
| **Senior Data Engineer** | Your primary target; 15+ years ETL, Python, SQL, PySpark, AWS |
| **Data Platform Engineer** | Same work as data engineer, different label; cloud architecture + pipelines |
| **ETL Engineer / ETL Developer** | Older title, less competition, direct match to 15 yrs ETL design |
| **Pipeline Engineer** | Exact match to what you built at Citi |
| **Cloud Data Engineer** | AWS Glue + Athena + S3 + serverless — precise fit |
| **AWS Data Engineer** | Direct match; Glue, Athena, Redshift, Bedrock, S3 |
| **PySpark Data Engineer** | Direct match; 6 yrs PySpark production at Citi |

### Data Engineering Senior/Staff ★★★★☆

| Title | Why It Fits |
|---|---|
| **Staff Data Engineer** | Natural step-up title; 20 yrs experience supports it |
| **Lead Data Engineer** | Team leadership dimension; applies if you've mentored |
| **Principal Data Engineer** | Architecture-heavy; 20 yrs depth supports it |
| **Data Warehouse Engineer** | 10 yrs dimensional modeling, Redshift, Athena |
| **Analytics Engineer** | SQL + transformations + reporting layer; dbt angle |
| **Data Architecture Engineer** | Design + governance + standards |

### Capacity Planning ★★★★★

| Title | Why It Fits |
|---|---|
| **Capacity Planning Engineer** | 15 yrs direct experience; ML forecasting; direct Citi proof |
| **Capacity Engineer** | Same role, shorter title |
| **Capacity Forecasting Engineer** | ML-driven forecasting with Prophet + scikit-learn |
| **Infrastructure Capacity Engineer** | Citi telemetry → infrastructure — direct match |
| **Performance and Capacity Engineer** | Combines your two domains |
| **Workload Planning Engineer** | Capacity planning language in enterprise/mainframe shops |
| **Resource Planning Engineer** | Capacity planning, sometimes finance-adjacent |

### Performance Monitoring / APM / Observability ★★★★☆

| Title | Why It Fits |
|---|---|
| **Performance Engineer** | 20 years; CA APM, Dynatrace, AppDynamics, BMC, Citi, AT&T |
| **Senior Performance Engineer** | Same + seniority layer |
| **Application Performance Engineer** | Direct APM SME match |
| **APM Engineer** | CA APM, Dynatrace, AppDynamics — SME-level |
| **Observability Engineer** | Monitoring, alerting, telemetry — aligns to Dynatrace + Citi work |
| **Monitoring Engineer** | Telemetry pipelines + alert configuration |
| **Platform Reliability Engineer** | SRE-adjacent; performance + availability focus |

### AI / GenAI Hybrid ★★★★☆

| Title | Why It Fits |
|---|---|
| **AI Data Engineer** | GenAI agent (Text-to-SQL) + data pipelines — production proof |
| **GenAI Data Engineer** | Claude 3 Sonnet + Bedrock at Citi |
| **AI Platform Engineer** | Pipeline + model serving + orchestration |
| **ML Platform Data Engineer** | PySpark + scikit-learn + forecasting pipelines |
| **Data Engineer, AI/ML Platform** | Same role, company-specific naming |
| **LLM Engineer (Data Pipelines)** | Text-to-SQL agent; data delivery side of LLM |

### SRE-Adjacent ★★★☆☆

| Title | Why It Fits |
|---|---|
| **Site Reliability Engineer (Data)** | Observability + pipeline reliability; stretch on SRE tooling |
| **Infrastructure Data Engineer** | Telemetry + pipeline — Citi maps directly |

### Migration / Modernization ★★★☆☆

| Title | Why It Fits |
|---|---|
| **Data Migration Engineer** | Legacy-to-cloud; on-prem Oracle → AWS is your story |
| **Cloud Migration Engineer (Data)** | Same; serverless transformation |
| **Modernization Engineer (Data Platform)** | ETL modernization + AI enablement |

### Stretch — Read JD Carefully ★★☆☆☆

| Title | Only Apply If... |
|---|---|
| **MLOps Engineer** | JD is pipeline + orchestration heavy (not model training) |
| **Data Science Engineer** | JD is engineering-heavy, not pure modeling |
| **Platform Engineer** | JD explicitly mentions data pipelines or monitoring |

---

## 4. Search Terms & Keywords — Rated by Strength

Use these as keyword inputs on job boards. Combine 2–4 at a time. Rated by how well they surface roles that match your exact profile.

### Tier 1 — Highest Yield ★★★★★

These appear in 80%+ of jobs you should apply to:

```
Python
SQL
PySpark
AWS
ETL
data pipelines
data engineer
Apache Spark
Airflow
Pandas
```

### Tier 2 — Strong Signal ★★★★☆

Add one or more of these to Tier 1 terms to narrow to your best fits:

```
AWS Glue
Amazon Athena
Amazon Redshift
S3
serverless
lakehouse
data warehousing
Parquet
capacity planning
forecasting
time-series
dimensional modeling
Docker
Linux
Git
```

### Tier 3 — Good Targeting ★★★☆☆

Use these to find your niche roles (capacity, monitoring, AI):

```
Prophet
scikit-learn
capacity forecasting
infrastructure forecasting
workload forecasting
observability
performance monitoring
APM
Dynatrace
AppDynamics
CA APM
BMC TrueSight
GenAI
LLM
Text-to-SQL
Bedrock
agentic
RAG
```

### Tier 4 — Specialty / Niche ★★☆☆☆

Use only when specifically targeting that domain:

```
Hive
Hadoop
FAISS
sentence-transformers
star schema
SCD Type 2
data quality
data governance
multiprocessing
Streamlit
plotly
Oracle
PL/SQL
Oracle RAC
PostgreSQL
shell scripting
Korn shell
Perl
```

### Tier 5 — Self-Study / Aspirational (Flag in Resume as "learning") ★☆☆☆☆

```
Databricks
Delta Lake
dbt
Snowflake
Unity Catalog
Delta Live Tables
Azure Data Factory
Azure Synapse
```

---

## 5. Boolean Search Strings — Ready to Paste

Copy and paste directly into LinkedIn, Indeed, Dice search boxes.

### Group A: Senior Data Engineer Core

```
"Senior Data Engineer" AND (Python AND SQL) AND (PySpark OR Spark) AND (AWS OR Redshift OR Athena) AND (Airflow OR ETL)
```

```
("Staff Data Engineer" OR "Lead Data Engineer" OR "Principal Data Engineer") AND ("data platform" OR "data pipelines") AND (AWS OR GCP OR Azure)
```

```
("Data Platform Engineer" OR "Cloud Data Engineer") AND (AWS AND (Glue OR Athena OR Redshift OR S3)) AND (Python OR PySpark)
```

### Group B: Capacity Planning

```
("Capacity Planning Engineer" OR "Capacity Engineer" OR "Infrastructure Capacity") AND (forecasting OR "time-series" OR Prophet OR scikit-learn)
```

```
("Capacity Forecasting" OR "Workload Planning" OR "Resource Planning") AND (Python OR SQL) AND (infrastructure OR platform)
```

```
("Senior Data Engineer" AND "capacity planning") AND (Python OR SQL) AND (monitoring OR observability)
```

### Group C: Performance / APM / Observability

```
("Performance Engineer" OR "APM Engineer" OR "Observability Engineer") AND (Dynatrace OR AppDynamics OR "CA APM" OR "BMC TrueSight")
```

```
("Senior Performance Engineer" OR "Application Performance Engineer") AND (latency OR throughput OR bottleneck) AND (monitoring OR observability)
```

```
("Observability Engineer" OR "Monitoring Engineer") AND (telemetry OR "real user monitoring" OR synthetic) AND (Python OR AWS)
```

### Group D: AI + Data Engineering

```
("AI Data Engineer" OR "GenAI Data Engineer" OR "LLM Engineer") AND (RAG OR "Text-to-SQL" OR embeddings OR Bedrock) AND (Python OR SQL)
```

```
("Data Engineer") AND (Bedrock OR LLM OR agentic OR GenAI) AND (pipeline OR orchestration OR ETL)
```

```
("ML Platform Engineer" OR "MLOps Engineer") AND ("data pipelines" OR PySpark OR Spark) AND (AWS OR cloud)
```

### Group E: Cloud Data + Forecasting Hybrid

```
("Data Engineer" OR "Data Platform Engineer") AND (AWS AND (Glue OR Athena OR Redshift)) AND (forecasting OR "capacity planning" OR "time-series")
```

```
("Senior Data Engineer") AND (serverless OR lakehouse) AND (PySpark OR Spark) AND (forecasting OR performance OR monitoring)
```

### Group F: DFW Local / Hybrid

```
("Data Engineer" OR "Performance Engineer" OR "Capacity Engineer") AND (Dallas OR Plano OR "Fort Worth" OR DFW) AND (hybrid OR "on-site")
```

```
("Senior Data Engineer") AND (Texas OR TX OR Dallas OR Plano) AND (Python OR PySpark OR AWS)
```

---

## 6. Google X-Ray Strings

Use in Google search bar to find jobs posted directly on company ATS systems, bypassing LinkedIn/Indeed fees.

### LinkedIn Jobs (Best for DFW + Remote)
```
site:linkedin.com/jobs "senior data engineer" "remote" Python PySpark
site:linkedin.com/jobs "capacity planning engineer" "remote" forecasting
site:linkedin.com/jobs "performance engineer" Dynatrace Texas
site:linkedin.com/jobs "data platform engineer" AWS Glue Athena
site:linkedin.com/jobs "observability engineer" "Dallas" OR "Plano" OR "remote"
site:linkedin.com/jobs "AI data engineer" OR "GenAI data engineer" Python Bedrock
```

### Greenhouse (Startup/Growth ATS)
```
site:boards.greenhouse.io "senior data engineer" AWS remote
site:boards.greenhouse.io "data platform engineer" PySpark
site:boards.greenhouse.io "capacity planning" Python forecasting
site:boards.greenhouse.io "AI engineer" OR "ML engineer" data pipelines
```

### Lever (Tech/Startup ATS)
```
site:jobs.lever.co "senior data engineer" PySpark AWS
site:jobs.lever.co "capacity engineer" OR "performance engineer" Python
site:jobs.lever.co "data engineer" GenAI OR LLM OR Bedrock
```

### Workday (Enterprise ATS)
```
site:myworkdayjobs.com "senior data engineer" Python SQL
site:myworkdayjobs.com "capacity planning engineer" forecasting
site:myworkdayjobs.com "performance engineer" APM observability
site:myworkdayjobs.com "data platform engineer" AWS Glue
```

### iCIMS (Healthcare, Insurance, Enterprise)
```
site:careers.icims.com "data engineer" Python AWS Dallas
site:careers.icims.com "capacity planning" OR "performance engineer"
```

---

## 7. Companies to Target Directly

Apply on their careers page — not through LinkedIn. Less competition, faster review.

### Banking & Fintech — DFW Area ★★★★★
| Company | Location | Notes | Careers URL |
|---|---|---|---|
| **JPMorgan Chase** | Plano/Dallas | Massive data/ML team; Citi background = instant credibility | careers.jpmorgan.com |
| **Comerica Bank** | Dallas HQ | Mid-size bank; strong data team; less competition | comerica.com/careers |
| **Goldman Sachs** | Dallas office | Strong engineering culture; data platform roles | goldmansachs.com/careers |
| **Bank of America** | Dallas | Large; data engineering, capacity teams | careers.bankofamerica.com |
| **Fiserv** | Irving | Fintech/payments; data platform heavy | fiserv.com/careers |
| **NCR Voyix** | Remote/Atlanta | POS + payments fintech; remote-friendly | ncrvoyix.com/careers |
| **Paymentus** | Remote | Fintech payments; Python + data engineering | paymentus.com/careers |

### Tech / Telecom — DFW Area ★★★★☆
| Company | Location | Notes | Careers URL |
|---|---|---|---|
| **AT&T** | Dallas HQ | Telecom data pipelines; you know the domain | att.jobs |
| **American Airlines** | Irving | Massive data team; capacity planning, flight ops data | jobs.aa.com |
| **Southwest Airlines** | Dallas HQ | Data platform team; loyal culture | jobs.southwestairlines.com |
| **Toyota North America** | Plano HQ | Analytics + data engineering; growing platform | toyota.com/usa/careers |
| **Nokia / Ericsson** | DFW | Telecom + network data — you know this world | careers.nokia.com |
| **Sabre** | Southlake TX | Travel tech; data heavy; you know the company | sabre.com/careers |
| **Liberty Mutual** | Irving | Insurance; regulated data — Citi experience is gold | libertymutual.com/careers |
| **USAA** | San Antonio (remote) | Insurance + banking; remote-friendly; Citi maps well | usaa.com/careers |

### Cloud / Data Tool Companies (Remote) ★★★★☆
| Company | Notes | Why |
|---|---|---|
| **Databricks** | Remote | Field eng / solutions architect — your PySpark depth + Databricks self-study |
| **Snowflake** | Remote | Data platform roles; Redshift/Athena maps; growth is still explosive |
| **dbt Labs** | Remote | Analytics engineering; dbt self-study + SQL depth |
| **Confluent** | Remote | Kafka/streaming data; pipeline engineer experience |
| **Palantir** | Remote/Dallas | Forward deployed engineer; enterprise data + AI |
| **AWS (Amazon)** | Remote/Irving | Solutions Architect, Data Engineer; Glue + Athena SME |

### Healthcare / Insurance (DFW) ★★★☆☆
| Company | Location | Notes |
|---|---|---|
| **Humana** | Remote/Dallas | Data pipelines, analytics; regulated = Citi familiar |
| **Aetna (CVS Health)** | Remote | Large data team; SQL + Python heavy |
| **Anthem/Elevance Health** | Remote | Data engineering + ML; large shop |
| **Tenet Healthcare** | Dallas HQ | Data warehousing, capacity planning for operations |

---

## 8. Recruiter Outreach Strategy

Recruiters are the fastest path to interviews. They are paid when you get placed — they want to help.

### How to Find Them on LinkedIn
Search LinkedIn for:
- `recruiter "data engineer" Dallas`
- `technical recruiter fintech Texas`
- `IT recruiter "capacity planning" OR "performance engineer"`
- `recruiter "PySpark" OR "data platform"`

### Recruiting Firms for DFW Tech — Rated ★★★★★

| Firm | Specialty | Website |
|---|---|---|
| **Motion Recruitment** | Tech, data engineering | motionrecruitment.com |
| **Insight Global** | Tech + enterprise | insightglobal.com |
| **TEKsystems** | Enterprise IT, data | teksystems.com |
| **Randstad Technologies** | Data, analytics, cloud | randstadusa.com |
| **Robert Half Technology** | Wide tech + DFW presence | roberthalf.com |
| **Hired.com** | Reverse recruiting; tech focus | hired.com |
| **Apex Group** | DFW-strong tech placement | apexgroup.com |

### LinkedIn Message Template — Copy & Send to 5 Recruiters Per Week

> Hi [Name] — I'm a Senior Data Engineer with 20+ years of enterprise experience (Python, PySpark, AWS, Airflow, SQL, Capacity Planning) and just transitioned out of Citi in December 2025. I'm open to roles in DFW (hybrid) or remote. Happy to connect if you're working anything in data engineering, performance/capacity, or AI-enabled data platforms.

**Follow-up after 1 week if no reply:**
> Hi [Name] — following up on my earlier note. Still actively searching — would love to chat if anything relevant comes across your desk.

---

## 9. LinkedIn Profile Optimization

Your LinkedIn is your passive inbound channel — recruiters search it constantly.

### Headline (Replace Generic Title)
**Current risk:** Generic headline is invisible to searches.
**Use this:**
> Senior Data Engineer | PySpark · AWS Glue · Athena · Airflow · GenAI Pipelines | 20 Years Enterprise | DFW & Remote

### Open to Work Settings
- Turn on **"Share with recruiters only"** (green banner optional)
- Set roles: Senior Data Engineer, Staff Data Engineer, Capacity Planning Engineer, Performance Engineer, Data Platform Engineer
- Set locations: Dallas-Fort Worth + Remote (United States)

### "About" Section — First 3 Lines Are Critical (Shown in Preview)
```
Senior Data Engineer with 20+ years of enterprise experience.
At Citi, I built PySpark ETL pipelines processing telemetry from 6,000+ endpoints,
migrated ML workloads to AWS, and shipped a production GenAI Text-to-SQL agent using Claude and Bedrock.
```

### Skills Section — Add All of These (Ordered by Recency/Relevance)
Python · PySpark · Apache Spark · SQL · AWS · AWS Glue · Amazon Athena · Amazon Redshift · Apache Airflow · ETL · Data Engineering · Pandas · Docker · Git · Linux · Capacity Planning · Time-Series Forecasting · Prophet · scikit-learn · Data Warehousing · Dimensional Modeling · GenAI · LLM · Bedrock · CA APM · Dynatrace · AppDynamics · BMC TrueSight · Streamlit · Hive · Hadoop · Data Quality · Data Governance

### Activity (Boosts Algorithm Visibility)
- Comment on 3–5 posts per week (data engineering, cloud, AI topics)
- Post once per week — short format works:
  - "I spent 2 hrs learning Databricks Delta Live Tables today. Here's what maps from AWS Glue..."
  - "Interesting pattern in time-series forecasting: why Prophet outperformed ARIMA for our use case..."
- Reshare industry news with a 2-sentence take

### LinkedIn URL
Ensure your URL is clean: `linkedin.com/in/sean-girgis-43bb1b5` — personalize if possible to `linkedin.com/in/sean-luka-girgis`

---

## 10. DFW Market Notes

### Why DFW Is Strong for You
- **Financial services cluster:** JPMorgan, Goldman, Bank of America, Citi (where you came from), Comerica, Fiserv — all have major DFW offices with data teams.
- **Telecom legacy:** AT&T HQ, Nokia, Ericsson — you have direct domain experience.
- **Travel / logistics:** American Airlines, Southwest, Sabre — data-heavy, capacity-planning-relevant.
- **Toyota, USAA, Liberty Mutual** — corporate HQ-level data teams.
- **Growing startup scene:** Built In Dallas tracks it daily — new postings weekly.

### Compensation Reality — DFW
DFW salaries are 5–15% below NYC/SF but cost of living is ~40% lower. Target:
- Senior Data Engineer: $130K–$175K base
- Staff/Principal: $160K–$210K base
- Remote (US company): often NYC/SF-pegged, $160K–$220K base
- Capacity/Performance Engineer (enterprise): $120K–$155K base

### Hybrid vs Full Remote in DFW
- Most large enterprises (JPMorgan, AA, AT&T) are requiring 3 days/week on-site in 2026.
- Startups + cloud companies (Databricks, Snowflake, dbt Labs) are still fully remote.
- **Sweet spot:** Remote-first companies with DFW presence for occasional meetings.

---

## 11. Remote vs Hybrid vs On-Site Strategy

### Recommended Priority Order

1. **Fully Remote (US)** — Highest salary, widest opportunity pool. Apply regardless of company HQ location. Your Citi remote experience proves you can operate at enterprise scale remotely.

2. **Hybrid DFW (2–3 days on-site)** — Best for DFW companies. Keeps you in the local network. Target financial services, airlines, Toyota.

3. **On-Site DFW Only** — Last resort unless compelling (company, comp, or growth). Murphy → Plano is 15 min. Murphy → Dallas is 25–35 min. Murphy → Irving (AA, Fiserv) is 45 min — acceptable.

### Filter Strategy on Job Boards
- LinkedIn: Filter → Remote **first** pass. Then relax to "Hybrid" for second pass.
- Indeed: Use "Remote" and "Plano, TX" as separate searches — don't combine or you miss things.
- Dice: Explicitly check "Remote" filter — their default includes everything.

---

## 12. Salary Ranges & Negotiation Anchors

### Target Salary by Role — 2026 DFW Market
| Role | Remote Range | DFW On-Site / Hybrid | Your Floor |
|---|---|---|---|
| Senior Data Engineer | $155K–$195K | $135K–$170K | $145K |
| Staff / Principal Data Engineer | $185K–$230K | $165K–$200K | $170K |
| Data Platform Engineer | $150K–$185K | $130K–$165K | $140K |
| Capacity Planning Engineer | $125K–$160K | $115K–$145K | $120K |
| Performance / APM Engineer | $120K–$155K | $110K–$140K | $115K |
| AI / GenAI Data Engineer | $165K–$210K | $145K–$185K | $155K |

### Negotiation Anchors
- **Open with:** 10–15% above your real floor.
- **If asked for current salary:** Decline or say "I prefer to focus on the role's budget." Texas has no salary history ban, but you have no obligation to disclose.
- **Total Comp:** Always ask for RSU vesting, bonus target, and 401K match — include in comparison.
- **Counter-offer:** Almost always possible. Counter once, accept or walk on round two.

---

## 13. Handling the Name Change

You legally changed from **Emad Girgis** to **Sean Luka Girgis** approximately 9 years ago (2017).

### On Resume / Applications
- Use **Sean Luka Girgis** exclusively.
- Do not reference the previous name on the resume.
- LinkedIn, GitHub, email — all under Sean Luka Girgis. ✓

### If a Background Check or Reference Asks
- Background checks will surface the previous name via court/legal records — this is normal and expected.
- If asked: "I legally changed my name approximately 9 years ago. My professional history under both names is mine."
- This is a non-issue for most employers when addressed directly.

### If a Reference Lists the Old Name
- Brief your references: "You may have my old name in your files — I legally changed it. The new name is Sean Luka Girgis. Just flag it to me if it comes up."

---

## 14. Daily Search Routine

**Time budget: 45–60 minutes per day**

### Morning (20–25 min) — Active Apply
1. Open LinkedIn Jobs → run your top 3 saved searches → apply to anything new that scores 75+.
2. Open Indeed → same 3 search terms → apply to 2–3 new roles.
3. Open Dice → "data engineer" or "capacity engineer" filter → scan new postings.

### Mid-Day (10–15 min) — Pipeline
4. Check email for recruiter inbound — reply same day.
5. Message 1–2 recruiters via LinkedIn (rotation through your target list).
6. Check Built In Dallas for new postings.

### Evening (10 min) — Maintenance
7. Log everything in your intake pipeline (intake.md → `.\job-check.ps1`).
8. Follow up on applications 7+ days old — email or LinkedIn message to recruiter/hiring manager.
9. Post or comment on LinkedIn (3× per week, not daily).

### Weekly (30 min, Sunday)
- Run Google X-ray strings for the week.
- Check Greenhouse/Lever/Workday direct for 10 target companies.
- Review Levels.fyi and Blind for new openings at well-compensated companies.
- Refresh saved search alerts on all platforms.

---

## 15. Application Tracker Checklist

For every job before you apply:

- [ ] Score ≥ 65 (use pipeline: `.\job-check.ps1` → `.\job-score.ps1`)
- [ ] JD saved to `intake\intake.md`
- [ ] Company researched (is it real? growing? funded? regulated industry?)
- [ ] Compensation range known or estimated (Glassdoor, Levels, LinkedIn)
- [ ] Resume tailored to JD ATS keywords (`.\job-run.ps1`)
- [ ] Cover letter generated and reviewed
- [ ] Applied via correct channel (company careers page preferred over Easy Apply)
- [ ] Application logged (`.\job-apply.ps1`)
- [ ] LinkedIn connection sent to hiring manager or recruiter at the company

### Application Velocity Targets
| Week | Applications | Goal |
|---|---|---|
| Week 1 | 5–8 | Get pipeline smooth, warm up |
| Week 2–4 | 10–15/week | Build interview pipeline |
| Month 2+ | 15–20/week | Full velocity until offer |

---

## Appendix A — Saved Search Presets (Copy to Job Boards)

### LinkedIn Saved Searches (Set Up All 5)
1. `Senior Data Engineer` — Remote, United States — Last 24 hours
2. `Data Platform Engineer` — Remote / Dallas-Fort Worth — Last 24 hours
3. `Capacity Planning Engineer` — Remote, United States — Last 24 hours
4. `Performance Engineer Observability` — Remote / Dallas — Last 24 hours
5. `AI Data Engineer GenAI` — Remote, United States — Last 24 hours

### Indeed Email Alerts (Set Up All 3)
1. `"data engineer" Python PySpark` — Dallas, TX + Remote — Daily
2. `"capacity planning engineer" OR "performance engineer"` — Remote — Daily
3. `"data platform engineer" AWS` — United States — Daily

### Dice Alerts (Set Up All 2)
1. `data engineer PySpark AWS` — Remote — Daily
2. `capacity engineer OR performance engineer` — Dallas TX — Daily

---

## Appendix B — Quick-Reference Keyword Combos

### Paste Directly into Any Search Box

**Highest fit:**
```
Senior Data Engineer Python PySpark AWS Airflow
```
```
Data Platform Engineer AWS Glue Athena Redshift Python
```
```
Capacity Planning Engineer forecasting Python scikit-learn
```

**Second tier:**
```
Performance Engineer APM Dynatrace AppDynamics Python
```
```
AI Data Engineer GenAI LLM Bedrock Text-to-SQL Python
```
```
Staff Data Engineer data pipelines ETL AWS PySpark
```

**DFW-specific:**
```
Data Engineer Dallas Texas hybrid Python SQL AWS
```
```
Capacity Engineer Plano Dallas remote forecasting
```
```
Observability Engineer Dallas Dynatrace APM Python
```

---

*Guide maintained as part of the jobsearch pipeline project at `D:\StudyBook\temp\jobsearch\docs\`*
*Profile source: `data\source_of_truth.json` + `data\master\skills.yaml`*
