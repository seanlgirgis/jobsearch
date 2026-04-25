# Audio Script — Citi High-Scale Telemetry Pipeline
# Slug: citi-telemetry
# HOST voice: nova | SEAN voice: onyx
# Chunk target: ~750 chars

---

**[HOST — voice: nova]**
Today we're walking through one of the highest-scale data engineering projects in Sean's career — a telemetry pipeline he designed at Citigroup for the Capacity and Planning team. Sean, set the scene. What did this team do?

**[SEAN — voice: onyx]**
The Capacity and Planning team sat at the center of a global infrastructure operation. Our job was to help business and technology teams across Citi understand their infrastructure capacity — where they had room, where they were running tight, and what decisions they needed to make. We were looking at somewhere between sixty-five and seventy thousand endpoints worldwide, spread across four global regions and dozens of departments. Physical servers, virtual machines, databases, containers — all of it.

**[HOST — voice: nova]**
And when you arrived, how was that analysis being done?

**[SEAN — voice: onyx]**
Entirely manually, in Excel. The team would extract telemetry data from BMC TrueSight — that's the enterprise monitoring platform Citi used — pull the P-ninety-five time-series for four K-P-Is: C-P-U, memory, disk, and network. Then someone would manually divide the data into spreadsheets by region and system type, enrich each section with reference data pulled from the C-M-D-B and from AppDynamics, clean the data by hand, calculate utilization metrics, apply safety and ceiling factors, sort everything, and finally produce the reports. Start to finish, that process took anywhere from five to ten days every month.

**[HOST — voice: nova]**
Five to ten days, every month, for sixty-five thousand endpoints.

**[SEAN — voice: onyx]**
And it had to be done monthly. Capacity planning has a monthly cadence — procurement cycles, infrastructure change windows, budget conversations — all of it runs on that clock. So the team was spending a significant chunk of every month just producing the input data for the conversations, before any actual planning work could happen. That's the problem I came in to solve.

**[HOST — voice: nova]**
Walk me through the data sources. Where was the raw telemetry coming from?

**[SEAN — voice: onyx]**
Three sources. BMC TrueSight was the primary source — it's the enterprise monitoring platform that captures P-ninety-five telemetry for C-P-U, memory, disk, and network across all monitored systems. TrueSight runs on an Oracle database backend, so the pipeline extracted data by querying Oracle directly rather than relying on manual exports — which was both faster and more reliable. P-ninety-five is important here because capacity planning cares about the high end of utilization, not the average. The average can look comfortable while the peak is hitting the ceiling. Then we enriched with two reference sources: the C-M-D-B, which is Citi's Change Management Database running on S-Q-L Server — it held asset inventory, ownership, region, department, tier, and classification for every system. And AppDynamics, which gave us additional server-level metadata: ownership details, location, departmental assignment, and application context that weren't always in the C-M-D-B.

**[HOST — voice: nova]**
So TrueSight is the performance data, and C-M-D-B plus AppDynamics are the enrichment layers.

**[SEAN — voice: onyx]**
Exactly. Raw telemetry tells you that a server has an eighty percent C-P-U P-ninety-five. The enrichment tells you which department owns that server, which region it sits in, what tier it is, and who to contact when it needs action. Without the enrichment, the telemetry is an unaddressed problem. With it, it becomes an actionable report that goes to a specific team.

**[HOST — voice: nova]**
Tell me about the safety and ceiling factors. What were those?

**[SEAN — voice: onyx]**
These are standard capacity planning constructs. The ceiling is the maximum threshold a resource should reach under normal operations — for C-P-U we used ninety percent. Hitting ninety percent C-P-U consistently is a signal that a system is at capacity, not a signal to wait and see. The safety factor accounts for the inherent uncertainty in P-ninety-five measurements — a single month's P-ninety-five doesn't capture every spike, and your confidence in the numbers isn't a hundred percent. We applied a multiplier of one-point-one-five to the raw utilization — essentially saying, assume your real peak is fifteen percent higher than what you measured. Combined, these turned the raw P-ninety-five into an adjusted utilization number that was conservative enough to catch problems before they became outages, but not so aggressive that everything looked like it needed immediate action.

**[HOST — voice: nova]**
And those adjusted numbers drove two different outputs?

**[SEAN — voice: onyx]**
Two directions. On one side: systems with very low adjusted utilization — the under-utilized — represented a saving opportunity. Downsize the resource allocation, consolidate onto fewer physical hosts, or promote from physical to virtual or from on-premises to cloud. On the other side: systems trending toward the ninety percent ceiling, or already projected to cross it within a planning window. Those triggered proactive notifications to the owning teams. Not alerts — notifications, with enough lead time for the team to engage our consultation and develop a response. And the response wasn't always "add more hardware." Sometimes it was a bug fix. Sometimes it was a rework of how the application used memory. Capacity problems often have a software root cause, and catching them early enough meant there was time to address the real problem rather than just throwing hardware at it.

**[HOST — voice: nova]**
Let's talk about the pipeline you built. What did the architecture look like?

**[SEAN — voice: onyx]**
Python end to end, with Pandas doing the heavy transformation work and NumPy for the calculations. The pipeline starts by ingesting the BMC TrueSight export — the raw P-ninety-five time-series for all monitored endpoints. It massages that data: standardizing formats, handling missing values, normalizing identifiers so the join keys match across sources. Then it joins against the C-M-D-B via S-Q-L Server queries and the AppDynamics reference data to attach all the enrichment columns. Clean, transformed, enriched data gets loaded into S-Q-Lite.

**[HOST — voice: nova]**
Why S-Q-Lite specifically?

**[SEAN — voice: onyx]**
Two reasons. First, the data volume fits S-Q-Lite comfortably — sixty-five thousand endpoints across four K-P-Is, monthly cadence, a couple of years of history. That's a large dataset for Excel, but it's not a distributed system problem. Second, we needed a specific database design: a master database that tracked the progression of every endpoint across months — so you could see a system trending from fifty percent to sixty-five percent to seventy-eight percent C-P-U over three months — and separate monthly databases for each reporting period. S-Q-Lite gave us file-level isolation per month with a clean query interface, and the master database joined them into a longitudinal view.

**[HOST — voice: nova]**
And the output — the team was still producing Excel reports?

**[SEAN — voice: onyx]**
The Excel reports were the deliverable because that's what the enterprise teams consumed. The pipeline regenerated them automatically from the database using openpyxl — structured workbooks with the same layout and formatting the teams expected, produced programmatically without any manual Excel work. What used to take five to ten days of manual work — the exports, the joins, the cleaning, the calculations, the sorting — was now produced in the first or second hour after the monthly data was ready. Same output format, same structure the enterprise teams expected, but generated from a pipeline instead of from a team of people working for a week and a half.

**[HOST — voice: nova]**
What about the internal reporting side?

**[SEAN — voice: onyx]**
Streamlit. We built an internal dashboard that the capacity team used to browse the data, review month-over-month progression for individual systems or departments, drill into the under-utilization and near-capacity lists, and track which systems had been actioned versus which were still outstanding. The combination of the automated Excel output for enterprise distribution and the Streamlit dashboard for internal analysis gave the team both the external deliverable and an internal tool they hadn't had before.

**[HOST — voice: nova]**
What did that transformation mean for the team's actual work?

**[SEAN — voice: onyx]**
It freed the team from data production and gave them back time for data analysis. Before the pipeline, most of the month was spent generating the inputs. After, the inputs arrived in two hours and the team spent the rest of the month actually planning — consulting with enterprise teams, analyzing trends, identifying systemic patterns across departments. The pipeline didn't replace the capacity planning expertise. It removed the manual data work that was blocking the capacity planning expertise from being applied.

**[HOST — voice: nova]**
Any technical challenges that stood out?

**[SEAN — voice: onyx]**
The join complexity. Sixty-five thousand endpoints with identifiers that don't always match cleanly across three source systems. Server names in TrueSight don't always format identically to hostnames in the C-M-D-B. Reference data in AppDynamics uses yet another naming convention. Getting the join keys to resolve correctly — handling aliases, naming inconsistencies, and records that exist in one source but not another — was the most labor-intensive part of the initial build. Once the normalization logic was solid, the pipeline ran reliably. But getting to reliable joins across three enterprise systems with inconsistent naming took significant data investigation work upfront.

**[HOST — voice: nova]**
Sixty-five to seventy thousand endpoints, four global regions, five to ten days down to one to two hours. That's a meaningful transformation.

**[SEAN — voice: onyx]**
The number that landed hardest with stakeholders was the time reduction. But the more important outcome was the quality improvement. Manual processes over five to ten days introduce drift — people making judgment calls, applying factors inconsistently, missing enrichment data for some regions. The pipeline applied the same logic to every endpoint, every month, deterministically. The reports became more consistent and more trustworthy, which made the enterprise teams more willing to act on them.

---
END OF SCRIPT
Voices: HOST (nova), SEAN (onyx)
Project: Citi High-Scale Telemetry Pipeline
Slug: citi-telemetry
