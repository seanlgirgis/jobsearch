# SAMSUNG HM INTERVIEW — AUDIO PLAY SCRIPT 3
# Deep Technical Topics

## STRICT INSTRUCTIONS FOR NOTEBOOKLM

This is a word-for-word audio interview script. You are not summarizing. You are not discussing. You are performing a live job interview as two characters.

- **Host 1** is DAVID — the Hiring Manager at Samsung Austin Semiconductor. David is highly technical and probing.
- **Host 2** is SEAN — the candidate. Sean is precise and answers exactly as written.
- Read every line exactly as written. Do not paraphrase. Do not add commentary. Do not break character.

---

DAVID: Let's go deeper. What are the SEMI E10 equipment states?

SEAN: SEMI E10 is the industry standard classifying every minute of equipment time into one of six states. Productive — the tool is processing wafer lots, the only state that generates output. Standby — the tool is ready but there is no product in queue. Engineering — the tool is being used for experiments, qualifications, or process development. Scheduled Downtime — planned preventive maintenance or calibrations. Unscheduled Downtime — unexpected failures or waiting for parts. And Off — the tool is not available at all. These states matter because they define what actually happened to your capacity budget. A tool with fifteen percent in engineering and twelve percent in unscheduled downtime has far less productive window than the calendar suggests. Rising unscheduled downtime is an early warning signal of equipment reliability issues before you see the output miss.

DAVID: What is MES and how does capacity planning interact with it?

SEAN: MES stands for Manufacturing Execution System. It runs the fab floor in real time — tracking every lot at every step: location, tool used, step duration, holds, and excursions. For capacity planning, MES is the primary data source. It provides lot tracking — actual cycle time, move rates, WIP by step. It provides equipment history — uptime and downtime by SEMI E10 state. And it provides process data — tool assignment, recipe, and process time. Capacity planning queries MES to calculate actual OEE, actual versus standard cycle time, and WIP movement rates — then feeds those into forecasting models. I have not worked directly with fab MES systems, but the data extraction pattern is identical to what I built against BMC TrueSight — connect to the source, extract time-series telemetry, enrich with reference data, build analytical models on top.

DAVID: Walk me through Little's Law with a concrete example.

SEAN: Little's Law states that average WIP equals throughput rate times average cycle time. The shorthand is L equals lambda times W. Here is a concrete fab example. If there are one hundred lots in WIP and throughput is twenty lots per day, then average cycle time equals five days. Now if WIP doubles to two hundred lots but throughput stays at twenty lots per day, cycle time doubles to ten days. The power of Little's Law is that you do not need to measure cycle time directly — you can calculate it from WIP and throughput, both of which are directly observable in MES. The lever it reveals: to reduce cycle time without reducing WIP you must increase throughput. To reduce cycle time without increasing throughput you must reduce WIP. There is no free lunch — you cannot improve cycle time by wishing it.

DAVID: How do you calculate resource capacity and utilization?

SEAN: Utilization equals actual output divided by theoretical maximum capacity, expressed as a percentage. Headroom equals the threshold minus current peak utilization. If my threshold is eighty percent and current peak is seventy-two percent, I have eight points of headroom. Time to capacity breach: I take the growth slope from historical trending and project forward. Growing one point five percentage points per quarter with eight points of headroom gives approximately five quarters until breach — that is the planning deadline. Effective capacity is always theoretical capacity times availability. Raw theoretical capacity is never the real planning number — a tool rated for one hundred lots per week at eighty-five percent availability delivers eighty-five lots per week effective. Always plan against effective capacity, not theoretical.

DAVID: What is your experience with in-house versus cloud capacity planning?

SEAN: Both — Citi was a hybrid model. On-premises: Oracle warehouse, BMC TrueSight, server and storage estate. Quarterly planning cycles, twelve-month procurement horizons. The binding constraint is lead time — hardware takes months to arrive, so six-month-plus forecasting accuracy is critical. Cloud on AWS: S3, Glue, Redshift, ECS. Cloud changes the constraint model entirely — you can provision in minutes. Planning shifts from "do we have enough?" to "are we spending appropriately?" It becomes a FinOps problem: right-sizing instances, auto-scaling policies, Reserved versus On-Demand cost optimization. On-premises is a procurement and lead-time problem. Cloud is a cost optimization and right-sizing problem. Same analytical foundation, completely different action levers.

DAVID: How would you estimate the capacity of a bottleneck tool?

SEAN: Start with theoretical throughput — lots per hour at the tool's rated processing speed. That is the ceiling. Factor in availability: if the tool is up eighty-five percent of the time, effective capacity is eighty-five percent of theoretical. Factor in utilization within that uptime window: seventy percent utilization times eighty-five percent availability gives approximately sixty percent effective capacity. Now calculate the gap: if demand requires seventy-five percent of theoretical maximum and effective capacity is sixty percent, I have a fifteen-point gap — that confirms the bottleneck. Validate against cycle time data: cycle time rising alongside utilization is the classic queuing nonlinearity that confirms the tool is the constraint. That exponential rise in cycle time as utilization approaches one hundred percent is the signature of a true bottleneck.

DAVID: Throughput dropped ten percent this week. How do you find the cause?

SEAN: Systematic decomposition, top down, four checks. First — tool availability. Was the bottleneck tool down? Pull SEMI E10 uptime data for the week and compare to prior weeks. Second — WIP starvation. Was there a shortage of lot starts feeding the tool? Check upstream WIP levels and lot release data. Third — process rate. Did the tool run slower than normal? A recipe change or equipment degradation would show as longer cycle times at that step. Fourth — scheduling. Were lots misrouted, held, or sitting in queue waiting for operators or materials? Pull queue time data by step. For each dimension I pull time-series data and correlate timing with the throughput drop. The variable whose change coincides with the drop is the lead indicator. Quantify the impact, identify the corrective action, and drive it to closure.

---

## END OF SCRIPT 3
