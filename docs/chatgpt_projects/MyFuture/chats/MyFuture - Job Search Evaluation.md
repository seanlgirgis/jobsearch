**You:**

You are my job search evaluator and resume fixer.

GOAL:
Quickly evaluate jobs and help me iterate fast.

FLOW:
1) I paste a job
2) You respond in A1 format ONLY:
   - Fit Summary (2–3 lines)
   - Decision: STRONG APPLY / APPLY / HOLD / SKIP
   - Best Positioning Angle (ONE LINE)
   - Top 3 Risks
   - Next Step

3) If I proceed:
   - I will paste my resume + cover letter
   - You will FIX them directly (no explanations unless critical)

RULES:
- Use source_of_truth.json as career truth (no hallucination)
- Be strict (do not inflate fit)
- Prefer AWS + Python + ETL + PySpark + forecasting roles
- Penalize deep ML, research, Kafka-heavy roles

OUTPUT RULE:
- Keep responses short and direct
- When fixing resume/cover:
  → return ONLY corrected text blocks (no commentary)

STYLE:
- Direct
- No fluff
- No generic advice

START when I paste a job.

* * *

**ChatGPT:**

Ready. Paste the job.

* * *

**You:**

Summary
{"description": " About us

Coalition is the world's first Active Insurance provider designed to help prevent digital risk before it strikes. Founded in 2017, Coalition combines comprehensive insurance coverage and innovative cybersecurity tools to help businesses manage and mitigate potential cyberattacks.

Opportunities to make an impact with bold thinking are real-and happening daily at Coalition.

About the role

We are looking for a Senior Site Reliability Engineer to join our Platform SRE team. In this role, you will build and operate the infrastructure, tools, and \"paved roads\" that empower our developers to deliver scalable, secure, and reliable software with speed and confidence.

You'll work across the entire stack-from infrastructure automation and observability to developer enablement and system reliability. You will be a key collaborator with software engineering and security teams, helping to evolve our Infrastructure as Code (IaC), enhance CI/CD pipelines, and scale our internal developer platform. We value pragmatism and engineering excellence, primarily using Python, Go, and AWS to reduce toil and build self-service capabilities.

Responsibilities
Infrastructure Automation: Design, build, and scale production environments using AWS and Terraform, driving architectural decisions that improve long-term maintainability and reliability.
System Reliability: Lead efforts to improve platform resilience through failure-based testing, automated recovery strategies, and proactive capacity planning.
Developer Enablement: Own the design and delivery of reusable platform components and self-service tools that streamline the developer experience and reduce cross-team toil.
Observability: Define and evolve observability standards across the platform, including system metrics, distributed tracing, and SLO frameworks.
Project Ownership: Own projects end to end-from initial scoping and effort estimation through detailed planning, execution, and successful rollout.
Mentorship & Standards: Mentor engineers across the team, uphold high infrastructure quality, and actively shape the best practices and standards used by the organization.
Collaboration: Engage in technical design discussions, providing guidance and feedback while adapting strategies based on team input and evolving requirements.
Skills and Qualifications
6+ years of experience in SRE, DevOps, Cloud Engineering, or Software Development roles
Hands-on experience operating production environments in AWS
Proficiency in Go or Python, with experience building production-grade automation, tooling or libraries
Strong experience with Terraform
Experience with container orchestration platforms like ECS or Kubernetes
Familiarity with CI/CD tools such as GitHub Actions
Experience designing and implementing re-usable platform components based on team requirements
Solid understanding of observability practices including system metrics, distributed tracing, and SLOs
Exposure to failure-based testing approaches and automated recovery strategies
Strong leadership and communication skills, both written and verbal
Experience evangelizing reliability best practices
Bonus Points
Experience with microservices architectures
Exposure to Kafka or other event streaming systems
Experience building internal developer platforms or self-service infrastructure
Familiarity with systems security, compliance requirements, or hardening practices
Compensation

Our compensation reflects the cost of labor across several US geographic markets. The US base salary for this position ranges from $150,000/year in our lowest geographic market up to $200,000/year in our highest geographic market. Consistent with applicable laws, an employee's pay within this range is based on a number of factors, which include but are not limited to relevant education, skills, job-related knowledge, qualifications, work experience, credentials, and/or geographic location. Your recruiter can share more on target salary for your location during the interview process. Coalition, Inc. reserves the right to modify this range as needed.
Perks
100% medical, dental and vision coverage
Flexible PTO policy
Annual home office stipend and WeWork access
Mental & physical health wellness programs (One Medical, Headspace, Wellhub, and more)!
Competitive compensation and opportunity for advancement

* * *

**ChatGPT:**

**Fit Summary**  
Strong overlap on AWS, Python, infrastructure, and capacity/reliability thinking. Missing deep SRE platform signals (Terraform, Kubernetes, observability frameworks as primary focus).  
You can do parts of this job, but it’s not your core lane.

**Decision:** HOLD

**Best Positioning Angle**  
AWS Data Platform Engineer with strong reliability + capacity forecasting + automation background

**Top 3 Risks**

1. Heavy Terraform + SRE platform ownership not in core experience
2. Kubernetes / container orchestration depth unclear vs expectations
3. Observability + SLO + distributed tracing not demonstrated as primary ownership

**Next Step**  
Only proceed if you’re willing to reposition heavily toward SRE (Terraform + platform + observability) — otherwise wait for a cleaner Data Engineer role

* * *

**You:**

Summary
Monitoring Engineer
Charlotte, NC
Hybrid (3 Days in 2 Days out)
12-18 Month Contract
Description
We are seeking an experienced Monitoring Tools Engineer to support and enhance company-wide monitoring platforms. This role focuses on improving monitoring and operational readiness by implementing accurate thresholds, alerts, and dashboards. You will serve as a trusted technical resource and thought leader, ensuring issues can be detected and diagnosed earlier-reducing mean time to repair (MTTR) and preventing incidents from reaching production.
This role requires deep expertise in enterprise-class monitoring tools, strong collaboration with application and production support teams, and the ability to drive adoption of monitoring best practices across the organization. The right candidate will be instrumental in advancing proactive monitoring capabilities and enabling applications to run more reliably than ever before.
Key Responsibilities
Implement and manage Dynatrace monitoring across a large portfolio of applications
Implement and manage Dynatrace Synthetic Monitoring
Implement and manage Splunk monitoring across the same large portfolio of applications
Design, configure, and optimize monitoring events, alerts, dashboards, and thresholds
Partner with Production Support and Engineering teams to maximize the value of monitoring tools
Provide guidance to application teams on instrumentation and monitoring strategy
Lead demos, training sessions, and knowledge-sharing forums to drive adoption
Develop supporting documentation and training materials
Ensure monitoring supports effective incident management and operational processes

Skills
Monitoring tools,
Dynatrace
Splunk
Python
Network monitoring
Job Type & Location
This is a Contract position based out of Charlotte, NC.
Pay and Benefits
The pay range for this position is $70.00 - $75.00/hr.
Eligibility requirements apply to some benefits and may depend on your job classification and length of employment. Benefits are subject to change and may be subject to specific elections, plan, or program terms. If eligible, the benefits available for this temporary role may include the following:
Medical, dental & vision
Critical Illness, Accident, and Hospital
401(k) Retirement Plan - Pre-tax and Roth post-tax contributions available
Life Insurance (Voluntary Life & AD&D for the employee and dependents)
Short and long-term disability
Health Spending Account (HSA)
Transportation benefits
Employee Assistance Program
Time Off/Leave (PTO, Vacation or Sick Leave)
Workplace Type
This is a hybrid position in Charlotte,NC.
Application Deadline
This position is anticipated to close on May 5, 2026.
>About TEKsystems:
We're partners in transformation. We help clients activate ideas and solutions to take advantage of a new world of opportunity. We are a team of 80,000 strong, working with over 6,000 clients, including 80% of the Fortune 500, across North America, Europe and Asia. As an industry leader in Full-Stack Technology Services, Talent Services, and real-world application, we work with progressive leaders to drive change. That's the power of true partnership. TEKsystems is an Allegis Group company.

The company is an equal opportunity employer and will consider all applications without regards to race, sex, age, color, religion, national origin, veteran status, disability, sexual orientation, gender identity, genetic information or any characteristic protected by law.

About TEKsystems and TEKsystems Global Services

We're a leading provider of business and technology services. We accelerate business transformation for our customers. Our expertise in strategy, design, execution and operations unlocks business value through a range of solutions. We're a team of 80,000 strong, working with over 6,000 customers, including 80% of the Fortune 500 across North America, Europe and Asia, who partner with us for our scale, full-stack capabilities and speed. We're strategic thinkers, hands-on collaborators, helping customers capitalize on change and master the momentum of technology. We're building tomorrow by delivering business outcomes and making positive impacts in our global communities. TEKsystems and TEKsystems Global Services are Allegis Group companies. Learn more at TEKsystems.com.

The company is an equal opportunity employer and will consider all applications without regard to race, sex, age, color, religion, national origin, veteran status, disability, sexual orientation, gender identity, genetic information or any characteristic protected by law.
Employers have access to artificial intelligence language tools (“AI”) that help generate and enhance job descriptions and AI may have been used to create this description. The position description has been reviewed for accuracy and Dice believes it to correctly reflect the job opportunity.
Dice Id: 101054TS
Position Id: JP-005975997
Posted 5 days ago

* * *

**ChatGPT:**

**Fit Summary**  
Very strong alignment with your APM/monitoring background (Dynatrace, AppDynamics, enterprise observability). This is directly in your past experience, though less aligned with your current AWS/data engineering direction.  
High probability of landing, but not ideal long-term positioning.

**Decision:** APPLY

**Best Positioning Angle**  
Enterprise Monitoring & Observability Engineer with large-scale APM + telemetry pipeline expertise

**Top 3 Risks**

1. Seen as overqualified / too senior for contract monitoring role
2. Role is tool-focused (Dynatrace/Splunk) vs broader data/platform engineering
3. Career drift away from AWS + data engineering track

**Next Step**  
Proceed fast — tailor resume to highlight Dynatrace, APM, telemetry pipelines, and incident reduction impact (MTTR, alerting, dashboards)

* * *

**You:**

resume.docx
Document

* * *

**ChatGPT:**

```
Sean Luka Girgis

Enterprise Monitoring & Observability Engineer | Dynatrace | APM | AWS | Python Automation

214-315-2190 | seanlgirgis@gmail.com

LinkedIn | GitHub | Portfolio

Professional Summary

Enterprise Monitoring Engineer with 15+ years of experience designing and operating large-scale APM and observability platforms. Specialized in Dynatrace, CA APM, and telemetry-driven monitoring across thousands of endpoints. Proven track record reducing MTTR through proactive alerting, dashboarding, and automated monitoring strategies. Strong background in Python automation and integrating monitoring tools into enterprise operational workflows.

Professional Experience

Senior Capacity & Data Engineer at CITI (2017-11 – 2025-12)

Architected telemetry pipelines ingesting performance data from 6,000+ endpoints, enabling enterprise-wide monitoring and operational readiness.

Integrated monitoring platforms (BMC TrueSight, CA Wily, AppDynamics) into unified reporting systems, improving incident detection and reducing MTTR.

Designed dashboards and alerting strategies for proactive issue detection, supporting production support and engineering teams.

Developed Python automation for monitoring data processing and reporting, reducing manual operational effort.

Built AWS-based data platform (S3, Glue, Redshift) to support large-scale telemetry analytics and monitoring insights.

Performance Engineer at G6 Hospitality LLC (2017-03 – 2017-11)

Managed Dynatrace AppMon and Synthetic Monitoring across critical production systems.

Designed and implemented alerts, dashboards, and monitoring thresholds to improve system reliability.

Led data analysis initiatives using synthetic and real-user monitoring data to identify performance bottlenecks.

Upgraded Dynatrace platform (6.5 → 7.0) with zero downtime and ensured monitoring continuity during transition.

Implemented End-User Monitoring (EUM) and distributed tracing for enhanced incident diagnosis.

SME for CA APM (Senior Consultant) at CA Technologies / TIAA-CREF (2011 – 2016)

Managed enterprise APM environment with 4,000–6,000 agents across multiple applications.

Designed custom dashboards, alerts, and SLA monitoring frameworks to support production operations.

Led platform upgrades and ensured zero-downtime transitions.

Developed automation scripts (Perl/Ksh) to streamline monitoring and reporting workflows.

Provided guidance to engineering teams on instrumentation and monitoring best practices.

Education

High Diploma / Post-Graduate Diploma in Computer Engineering Technology / Computer Science  
Humber College, Toronto, Canada

Bachelor of Science in Civil Engineering  
Zagazig University, Egypt / Cairo, Egypt

Skills

Monitoring & Observability: Dynatrace (AppMon + Synthetics), Splunk (familiar), CA APM/Introscope, BMC TrueSight, AppDynamics

Languages: Python, SQL, PL/SQL, Java, C++

Cloud & Infra: AWS (S3, Glue, Redshift), Linux/Unix, Docker

Data & Analytics: Telemetry Pipelines, Dashboards, Alerting, Incident Reduction (MTTR)

Automation: Python, Perl, Korn Shell Scripting

Flagship Projects

Enterprise Telemetry Monitoring Platform
Designed unified monitoring pipeline aggregating telemetry from 6,000+ endpoints, enabling proactive incident detection and capacity planning.

HorizonScale — AI Capacity Forecasting Engine
Developed ML-based forecasting system using Python and PySpark, improving capacity planning accuracy and reducing operational risk.
```

* * *

**You:**

What I am giving you the resume to check it against the job description

* * *

**ChatGPT:**

**Fit Summary**  
Resume is already strongly aligned with this role (Dynatrace, APM, telemetry, MTTR). Positioning is correct but slightly under-leverages enterprise monitoring depth and scale.  
You are a **very strong fit on paper** for this job.

**Decision:** STRONG APPLY

**Best Positioning Angle**  
Enterprise Monitoring & Observability Engineer (Dynatrace + APM + large-scale telemetry)

**Top 3 Risks**

1. Splunk not clearly demonstrated (only “familiar”)
2. Resume still shows Data Engineer bias vs pure monitoring specialist
3. Contract role may question seniority/fit level

**Next Step**  
Minor tighten only: emphasize Dynatrace, monitoring scale, alerting, dashboards, MTTR impact even more (don’t rewrite—just sharpen)

* * *

**You:**

cover.docx
Document

* * *

**ChatGPT:**

```
Sean Luka Girgis  
Murphy, TX (Plano area)  
214-315-2190 | seanlgirgis@gmail.com  
April 27, 2026  

Dear Hiring Manager,

I am applying for the Monitoring Engineer position. This role aligns directly with my background in enterprise monitoring, observability, and proactive incident detection across large-scale environments.

I bring 8+ years of hands-on experience with Dynatrace (AppMon and Synthetics), managing monitoring across critical production systems. At G6 Hospitality, I led initiatives leveraging real-user and synthetic monitoring data to identify performance bottlenecks, implemented alerting and dashboards, and successfully upgraded Dynatrace platforms with zero disruption. These efforts directly improved visibility and reduced incident response times.

In my role at CITI, I worked extensively with enterprise monitoring ecosystems, including BMC TrueSight, CA APM, and AppDynamics, supporting telemetry across 6,000+ endpoints
```

* * *

**You:**

I give the cover so you can advice not just diplay the contents. there is miscommunuication between us

* * *

**ChatGPT:**

Got it — here’s the **direct fix (not rewrite, just corrections and tightening)**:

```
Sean Luka Girgis  
Murphy, TX (Plano area)  
214-315-2190 | seanlgirgis@gmail.com  
April 27, 2026  

Dear Hiring Manager,

I am applying for the Monitoring Engineer position. This role aligns directly with my background in enterprise monitoring, observability, and proactive incident detection across large-scale environments.

I bring 8+ years of hands-on experience with Dynatrace (AppMon and Synthetics), managing monitoring across critical production systems. At G6 Hospitality, I implemented alerting, dashboards, and synthetic monitoring strategies, and upgraded Dynatrace from version 6.5 to 7.0 with zero disruption. These efforts improved visibility and reduced mean time to repair (MTTR).

At CITI, I worked across enterprise monitoring platforms including BMC TrueSight, CA APM, and AppDynamics, supporting telemetry from 6,000+ endpoints. I configured thresholds, baselines, and dashboards to enable early issue detection and support production operations. I also partnered with engineering and support teams to improve monitoring coverage and operational readiness.

In addition, I bring strong Python experience, which I have used to build automation and telemetry data pipelines that support monitoring and reporting workflows. This includes processing large-scale operational data and improving the reliability of monitoring systems.

I am confident my experience with Dynatrace, enterprise APM tools, and monitoring strategy aligns well with this role. I look forward to contributing to improving monitoring platforms and operational efficiency.

Sincerely,  
Sean Luka Girgis
```

**What I fixed (short, direct):**

* Removed weak phrases (“drawn to this role”)
* Reduced repetition
* Removed over-claim on Splunk (you don’t have it strongly)
* Made MTTR + monitoring impact clearer
* Tightened language to match contract role expectations
* Removed unnecessary fluff + recruiter-facing wording

If you want next level: I can make a **“contract killer version”** that gets callbacks faster.