# source_of_truth.json — Experience Highlights Cleanup (Task 2)
# Run this with Antigravity against: D:\StudyBook\temp\jobsearch\data\source_of_truth.json
# Goal: trim bloated highlights in older experience entries to 6–8 strong bullets each

---

## Context

The pipeline sends the `highlights` array directly to Grok as resume bullet candidates.
Having 12–29 bullets per role wastes tokens and creates noise. Each role should have
6–8 tight, quantified bullets that tell a clear impact story.

---

## EXPERIENCE 1: G6 Hospitality LLC — Performance Engineer (Mar–Nov 2017)
**Current:** 12 bullets (many are repetitive/low-impact)
**Target:** 6 bullets

Replace the entire highlights array with EXACTLY these 6 bullets:
```json
[
  "Managed Dynatrace AppMon/Synthetics monitoring for Brand.com and all critical hospitality systems.",
  "Led 'FAST' project: data-mined real-user performance metrics from Gomez Synthetic Monitoring to surface optimization recommendations adopted by engineering teams.",
  "Upgraded Dynatrace from 6.5 to 7.0 and enforced TLS 1.2 security — zero regression in production monitoring during cutover.",
  "Integrated HP Performance Center with Dynatrace, enabling unified load test + APM correlation.",
  "Implemented End-User Monitoring (EUM) and end-to-end transaction tracing across web and mobile.",
  "Participated in cloud migration planning to AWS, evaluating mobile monitoring tools and providing APM readiness assessment."
]
```

---

## EXPERIENCE 2: CA Technologies / TIAA-CREF — SME for CA APM (2011–2016)
**Current:** 16 bullets (many repeat the same theme)
**Target:** 7 bullets

Replace the entire highlights array with EXACTLY these 7 bullets:
```json
[
  "Served as CA APM SME for TIAA-CREF, managing 50+ Enterprise Managers and 4,000–6,000 instrumented agents across the enterprise.",
  "Led large-scale CA APM upgrades (9.1 → 10.1) with zero unplanned downtime, coordinating cross-functional IT teams.",
  "Designed and implemented custom Management Modules — dashboards, alerts, SLA thresholds — adopted as standards across client environments.",
  "Built Perl/Ksh data-extraction scripts for automated performance reporting, replacing manual weekly exports.",
  "Provided sizing recommendations and Golden Image agent deployments, reducing onboarding time for new applications.",
  "Collaborated with J2EE/WebLogic performance teams to resolve bottlenecks identified via APM telemetry.",
  "Delivered client training programs and technical documentation adopted by internal CA and customer teams."
]
```

---

## EXPERIENCE 3: Corpus Inc. / Sprint (AMDOCS projects) — Developer / Support Engineer (2001–2007)
**Current:** 29 bullets (severe bloat — many low-level implementation details)
**Target:** 8 bullets

Replace the entire highlights array with EXACTLY these 8 bullets:
```json
[
  "Developed high-availability multithreaded C++ billing interfaces using POSIX threads, mutex locks, semaphores, socket programming, and Marconi APIs — supporting telecom billing at Sprint scale.",
  "Delivered performance enhancements in C/C++/Pro*C/PL/SQL billing processes: reduced memory usage 75%, improved throughput 20%, and achieved 10x database performance via sequence optimization.",
  "Maintained and enhanced AMDOCS Flexible Bill Formatter, EDI interfaces, and Enabler/CSM/EMS modules across full billing lifecycle (invoicing, settlement, reporting).",
  "Reverse-engineered and documented undocumented AMDOCS PRM APIs to enable interface integration not supported by vendor.",
  "Designed interfaces using UML/Rational Rose; applied OO design patterns (Functors, Containers) to build reusable threading and socket utility libraries.",
  "Automated WebLogic/WebSphere system administration using Korn Shell scripting, eliminating manual deployment steps.",
  "Supervised test team using Mercury Test Director; led QA cycles and production bug triage for billing and CSM modules.",
  "Operated across HPUX, SunOS, and Linux environments; maintained code in CVS and ClearCase throughout 6-year engagement."
]
```

---

## EXPERIENCE 4: Sabre — Senior Systems & Data Migration Engineer (May 2008–Jan 2010)
**Current:** 6 bullets (3 are near-duplicates of the top 3)
**Target:** 4 bullets — deduplicate

Replace the entire highlights array with EXACTLY these 4 bullets:
```json
[
  "Led migration of a high-throughput shopping engine from 200+ MySQL nodes to a 6-node Oracle RAC cluster — handling 10x the transaction volume of VISA.",
  "Optimized core transaction processing using C++ and OCCI, reducing physical hardware footprint by 95% while maintaining sub-second query latency.",
  "Built CPPUNIT testing framework in C++/OCCI/OCI to validate migration correctness across millions of transaction records.",
  "Automated schema conversion and data validation pipelines to ensure integrity throughout the phased migration cutover."
]
```

---

## EXPERIENCE 5: AT&T — Performance Test Engineer (Aug 2010–Jul 2011)
**Current:** 4 bullets (2 are near-duplicates)
**Target:** 3 bullets — deduplicate

Replace the entire highlights array with EXACTLY these 3 bullets:
```json
[
  "Analyzed J2EE telecom web applications under load to identify optimal throughput limits and resource bottlenecks (JDBC connections, threads, heap memory, CPU, GC pressure).",
  "Installed and configured JMX Monitoring, Wily Introscope, and Thread Dump automation scripts for real-time visibility during load tests.",
  "Documented performance baselines and regression thresholds used by engineering teams for release gate decisions."
]
```

---

## EXPERIENCE 6: Computer Science Corporation (CSC) — IRS CADE Project (Oct 2007–May 2008)
**Current:** 3 bullets (2 are near-duplicates)
**Target:** 2 bullets — deduplicate

Replace the entire highlights array with EXACTLY these 2 bullets:
```json
[
  "Designed UML class/sequence diagrams and developed modules for the IRS CADE mainframe modernization project.",
  "Built CICS/MQ Series/XML messaging interfaces in VC++ with DB2 backend — adhering to government system architecture standards."
]
```

---

## VALIDATION AFTER EDITS

Verify bullet counts per experience:
- CITI: exactly 10 bullets (already done in Task 1 — do NOT change)
- G6 Hospitality: exactly 6 bullets
- HCL/Entergy: unchanged (exclude_from_resume: true — leave as-is)
- CA Technologies/TIAA-CREF: exactly 7 bullets
- AT&T: exactly 3 bullets
- Sabre: exactly 4 bullets
- CSC: exactly 2 bullets
- Corpus/Sprint: exactly 8 bullets
- Simplex: unchanged (exclude_from_resume: true — leave as-is)
- Humber College: unchanged (exclude_from_resume: true — leave as-is)

Save back to: D:\StudyBook\temp\jobsearch\data\source_of_truth.json
JSON must remain valid after all edits.
