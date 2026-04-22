# SAMSUNG HM INTERVIEW — AUDIO PLAY SCRIPT

## STRICT INSTRUCTIONS FOR NOTEBOOKLM

This is a word-for-word audio interview script. You are not summarizing. You are not discussing. You are performing a live job interview as two characters.

- **Host 1** is DAVID — the Hiring Manager at Samsung Austin Semiconductor. David is direct, technical, and probing.
- **Host 2** is SEAN — the candidate. Sean is confident, precise, and answers exactly as written.
- Read every line exactly as written. Do not paraphrase. Do not add commentary between lines. Do not break character. Do not editorialize.
- This is a rehearsal recording. Accuracy is everything.

---

DAVID: Good morning Sean, thanks for making time. I'm David Rojas, I manage the Capacity Planning team here at Samsung Austin Semiconductor. Let's just get into it. Walk me through your capacity planning experience.

SEAN: At Citi I owned end-to-end capacity planning for the infrastructure estate across four global regions — think of it as the fab capacity function but for servers and storage instead of wafer tools. I built automated ETL pipelines pulling peak utilization telemetry from BMC TrueSight Capacity Optimization across six thousand plus assets. I performed bottleneck investigations identifying which asset classes were approaching capacity thresholds. I built short-range and long-range views — weekly operational reporting and six-month planning horizon forecasting using Prophet and scikit-learn ML models. And I ran monthly capacity reviews with engineering, finance, and procurement — translating utilization data into procurement decisions with quantified cost and lead time for each option.

DAVID: Do you have manufacturing or fab experience?

SEAN: I don't have direct fab experience — I'll be straight about that. What I have is deep mastery of the analytical methodology that sits under all capacity planning regardless of domain: utilization modeling, bottleneck forecasting, Factory Physics, supply chain lead time analysis. Those skills take years to build. Semiconductor domain knowledge — process steps, MES systems, fab-specific terminology — I can learn in months. I've done exactly that before: I entered financial services IT with no banking background and was running the capacity planning system for Citi within my first year. The question isn't whether I know wafer fabs today. It's whether I can apply rigorous capacity planning methodology in a new domain — and I have a strong track record of doing exactly that.

DAVID: How do you approach a bottleneck investigation?

SEAN: Systematic decomposition, top down. First — is it a capacity issue or a utilization issue? If peak utilization is high and growing, that's a structural capacity gap. If peak utilization is high but adjacent assets are under-utilized, that's a scheduling or allocation gap. These have completely different solutions — one requires procurement, the other requires rebalancing. Second — what's the timing signature? A sudden spike points to a discrete event. A gradual trend points to organic growth approaching the ceiling. Third — is it the actual bottleneck or a downstream effect? In fab terms — is WIP building because that tool is slow, or because the tool feeding it is starving it? I correlate queue depth, move rate, and upstream WIP to separate cause from symptom. The output isn't just "this is bottlenecked" — it's here's why, here's the quantified impact, here's the recommended action.

DAVID: What is Factory Physics and how do you apply it?

SEAN: Factory Physics is the study of how manufacturing systems behave under load — specifically the relationships between WIP, throughput, and cycle time. The foundational relationship is Little's Law: average WIP equals throughput rate times average cycle time. In a fab — if a hundred lots are in WIP and throughput is twenty lots per day, average cycle time is five days. If WIP doubles to two hundred lots but throughput stays at twenty per day, cycle time doubles to ten days. The other critical behavior: as tool utilization approaches one hundred percent, cycle time increases exponentially — not linearly. A tool at ninety-five percent utilization has dramatically worse cycle time than one at eighty percent, even though the gap looks small. That nonlinear behavior is why capacity planning cannot just chase utilization to one hundred percent. I applied the same queuing theory in IT — a server at ninety percent utilization behaves very differently from one at seventy percent. The math translates directly.

DAVID: What is OEE and how does it connect to capacity planning?

SEAN: OEE stands for Overall Equipment Effectiveness. The formula is Availability times Performance times Quality. Availability is actual uptime divided by planned production time — it captures downtime losses. Performance is actual throughput rate divided by ideal rate — it captures slow cycles. Quality is good units divided by total units — it captures yield loss. For example: ninety percent availability times eighty percent performance times ninety-five percent quality equals sixty-eight point four percent OEE. World class targets eighty-five percent or higher. For capacity planning, OEE is the bridge from theoretical to real capacity. A tool rated at one hundred lots per week at sixty-eight percent OEE delivers sixty-eight lots per week effective. Plan against theoretical and you will consistently miss output. I used identical logic in IT — effective capacity equals theoretical times availability times performance efficiency. The math is the same.

DAVID: Walk me through how you would approach a full capacity analysis.

SEAN: I start by defining the resource and the constraint — what are we measuring and what threshold represents a problem? In a fab that's tool utilization rate and WIP queue depth. Then I pull twelve to twenty-four months of historical utilization data and decompose the trend — linear growth, seasonal pattern, or event-driven spikes. From that I build a forecast — statistical for stable trends, Prophet ML-based for volatile or seasonal data. The forecast gives the expected crossover point where demand exceeds available capacity. Then I calculate the gap at each planning horizon — three months, six months, twelve months. Is the gap addressable through efficiency improvements or does it require net-new capacity? Finally I present risk-tiered options: do nothing and quantify the cost of miss, optimize utilization with investment and lead time, or procure with full cost and lead time. Leadership decides with full information, not just a status update.

DAVID: Tell me about your ML forecasting experience.

SEAN: I used a two-model architecture in HorizonScale. First: Prophet for time-series forecasting. It handles seasonality and trend decomposition natively — weekly patterns, monthly cycles, holiday effects — and generates a forecast with confidence intervals so I can show the uncertainty band, not just the expected trajectory. Second: scikit-learn classifiers — Random Forest and Gradient Boosting — trained to classify assets as at-risk or safe based on derived features: growth rate, utilization trend slope, variance, days to threshold. This gave a binary risk signal easier for operational teams to act on than a curve. The pipeline ran on PySpark at banking scale — thousands of assets processed in parallel with a generator-based architecture. Ninety percent cycle time reduction versus the original sequential design. For a fab environment: replace server telemetry with tool utilization data, replace CMDB with equipment master data. The pipeline architecture and model structure transfer directly.

DAVID: How do you present capacity risk to leadership?

SEAN: Risk-tiered format with clear action items. Leadership doesn't need queuing theory — they need: what's at risk, by when, what does it cost, what's the recommended action. My standard structure: first, current state — utilization versus threshold and WIP levels in one view, traffic-light format. Second, risk horizon — which resources breach capacity at three, six, and twelve months, ranked by severity. Third, options and cost — for each at-risk item: do nothing, optimize utilization, or procure — each with investment and lead time. Fourth, decision deadline — by when does leadership need to act to stay on track? That's the forcing function. At Citi I automated this from HorizonScale — same format every month, which built trust in the numbers. Consistency in reporting is as important as accuracy.

DAVID: What is supply chain management in a fab context?

SEAN: Two dimensions. Equipment supply chain: leading-edge fab tools have eighteen to twenty-four month lead times. A capacity gap identified today cannot be filled for two years. Capacity planning must look twenty-four plus months out and signal equipment needs well ahead of demand. Spare parts are critical too — a tool down waiting for a part for three weeks is a massive capacity loss. Materials and consumables: wafers, gases, chemicals, photomasks. Demand forecasting feeds procurement cycles. A sudden lot start ramp requires more raw wafers — if procurement didn't anticipate it, the capacity plan is impossible to execute regardless of tool availability. The capacity planner sits at the intersection of both: forecast demand accurately, communicate constraints to production, give procurement enough lead time to support the plan. I did the same at Citi — my six-month forecasting horizon aligned directly to the hardware procurement cycle.

DAVID: Why Samsung, and why this role?

SEAN: Samsung operates at a manufacturing scale that's genuinely rare. Advanced semiconductor fabrication at the Taylor fab is one of the most technically demanding manufacturing environments in the world. Capacity planning in a fab isn't just data work — it directly determines what gets built, when, and at what cost. The analytical rigor required — Factory Physics, bottleneck modeling, supply chain forecasting — is exactly what I've been doing in infrastructure capacity, and I want to apply it in a domain where the stakes are higher and the problems are harder. The Taylor fab is a strategic U.S. investment for Samsung. Being part of building out the operational excellence layer of that facility is genuinely exciting to me.

DAVID: What happened at Citi — why did you leave?

SEAN: I was at Citi for eight years and delivered strong results. My role was eliminated as part of a broader organizational restructuring — not performance related. I've used the time to sharpen my skills and I'm actively looking for the right long-term fit. The Samsung role is at the top of my list.

DAVID: What's your salary expectation?

SEAN: I'm targeting a base in the range of one hundred forty-five thousand to one hundred sixty thousand dollars. I understand Samsung structures compensation as base plus bonus without RSUs, and I'm open to discussing the full package.

DAVID: When can you start?

SEAN: I'm available to start immediately and can align with your preferred onboarding timeline.

DAVID: Are you comfortable with the on-site requirement and U.S. export control compliance?

SEAN: Yes on both. Fully on-site in Taylor works for me. And I understand this role has U.S. export control compliance requirements — I can complete any required verification promptly.

DAVID: Good. Do you have any questions for me?

SEAN: A few. What does the split look like between short-range capacity management — daily and weekly WIP — and long-range planning at the six to eighteen month horizon? And what tools and data infrastructure is the team currently using — are you pulling from MES data directly or through separate analytics platforms? And finally — where are the biggest gaps today that this role is expected to close?

DAVID: Those are good questions. We'll follow up on next steps.

SEAN: Thank you David. I appreciate the time and I'm genuinely excited about this opportunity.

---

## END OF SCRIPT
