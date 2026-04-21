# Samsung HM Interview — Audio 5: Behavioral & General Questions
## What This Audio Covers
All the behavioral and situational questions a Hiring Manager will ask: the manufacturing experience challenge, line analysis, Production and Engineering coordination, presenting risk to leadership, quantifying throughput impact, plus the standard closing questions — Why Samsung, why leaving Citi, competing offers, salary, start date, and export control.

---

## "Do you have manufacturing / fab experience?"

> "I don't have direct fab experience — I'll be straight about that. What I have is deep mastery of the analytical methodology that sits under all capacity planning regardless of domain: utilization modeling, bottleneck forecasting, Factory Physics, supply chain lead time analysis.
>
> Those skills take years to build. Semiconductor domain knowledge — process steps, MES systems, fab-specific terminology — I can learn in months. I've done exactly that before: I entered financial services IT with no banking background and was running the capacity planning system for Citi within my first year.
>
> The question is not whether I know wafer fabs today. It is whether I can apply rigorous capacity planning methodology in a new domain — and I have a strong track record of doing exactly that."

---

## "How do you perform line analysis and identify line movement constraints?"

Line analysis is about understanding how product flows across all process steps — not just one tool — and finding where it accumulates, slows, or starves.

> "I start by mapping the process flow: all steps, tools per step, throughput rate at each tool. Then I overlay WIP data — where are queues building? WIP accumulates upstream of a bottleneck.
>
> Key metrics per step: queue depth, move rate, cycle time versus standard, utilization.
>
> A healthy line has WIP distributed evenly. An unhealthy line has WIP piling at one or two steps — those are your constraints.
>
> Line balance is the goal: matching throughput at every step to the pace set by the bottleneck so WIP flows smoothly. Imbalance wastes capacity on fast tools while the bottleneck is overloaded.
>
> At Citi I did the same across server tiers — mapping utilization flow to find where processing was accumulating and which tier was the constraint."

---

## "How do you coordinate between Production and Fab Engineering teams?"

These teams have natural tension: Production wants output now — minimize downtime. Engineering wants stability — experiments, preventive maintenance, qualifications.

> "The capacity planner's job is to quantify that tension with data, not referee it politically.
>
> I build a shared model that shows: if Engineering takes Tool X offline 8 hours this week, it costs Y lots of output. That forces an explicit decision — is the engineering run worth Y lots? Both sides use the same numbers. The conversation shifts from 'my team's priority' to 'what is the right tradeoff for the business.'
>
> At Citi: infrastructure engineering wanted maintenance windows, application teams wanted 100 percent availability. Same dynamic. A shared data model that quantified the tradeoff — maintenance now versus risk of unplanned outage later — turned arguments into decisions."

---

## "How do you present capacity risk to leadership?"

> "Risk-tiered format with clear action items. Leadership does not need queuing theory — they need: what is at risk, by when, what does it cost, what is the recommended action.
>
> My standard structure: first, current state — OEE and utilization versus threshold and WIP levels in one view, traffic-light format. Second, risk horizon — which resources breach capacity at 3, 6, and 12 months, ranked by severity — impact times probability. Third, options and cost — for each at-risk item: do nothing — cost of miss; efficiency improvement — investment plus lead time; procure — cost plus lead time. Fourth, decision deadline — by when does leadership need to act to stay on track? That is the forcing function.
>
> At Citi I automated this from HorizonScale — same format every month, which built trust in the numbers. Consistency in reporting is as important as accuracy."

---

## "How do you quantify the impact of a throughput improvement?"

Three dimensions: output, revenue, and cost avoidance.

> "Output: if the bottleneck tool throughput increases 5 percent and it is the line constraint, total fab output increases 5 percent. Convert to wafer starts or die count.
>
> Revenue: incremental output times average selling price. 1,000 more wafers per month at $5,000 per wafer equals $5 million per month additional revenue.
>
> Cost avoidance: if the improvement delays a $20 million tool procurement by 18 months, that is quantifiable capital deferral — the NPV of deferred spend.
>
> At Citi: throughput improvements that reduced forecasted server procurement were quantified as dollars of CapEx avoided over the planning horizon. That is how you get engineering work approved — translate utilization percentages into dollar impact."

---

## "Why Samsung / Why this role?"

> "Samsung operates at a manufacturing scale that is genuinely rare — advanced semiconductor fabrication at the Taylor fab is one of the most technically demanding manufacturing environments in the world.
>
> Capacity planning in a fab is not just data work — it directly determines what gets built, when, and at what cost. The analytical rigor required — Factory Physics, bottleneck modeling, supply chain forecasting — is exactly what I have been doing in infrastructure capacity, and I want to apply it in a domain where the stakes are higher and the problems are harder.
>
> The Taylor fab is a strategic U.S. investment for Samsung. Being part of building out the operational excellence layer of that facility is genuinely exciting — it is a generational project."

---

## "Why are you leaving / what happened at Citi?"

> "I was at Citi for 8 years and delivered strong results. My role was eliminated as part of a broader organizational restructuring — not performance related. I have used the time to sharpen my skills and I am actively looking for the right long-term fit. The Samsung role is at the top of my list."

---

## "Are you interviewing elsewhere?"

> "Yes, I have a few conversations in progress — including with Toyota Financial Services and Capital One. Samsung is my top priority given the capacity planning focus, the analytical depth the role requires, and the scale of what is being built at the Taylor facility."

---

## "What is your salary expectation?"

> "I'm targeting a base in the range of $145,000 to $160,000. I understand Samsung structures comp as base plus bonus without RSUs, and I'm open to discussing the full package."

Say the range. Pause. Do not elaborate further unless he asks.

---

## "When can you start?"

> "I am available to start immediately and can align with your preferred onboarding timeline."

---

## U.S. Export Control and On-Site

**Export Control:**
> "Yes — I understand this role has U.S. Export Control compliance requirements and I can complete any required verification promptly."

**On-site:**
> "Yes, fully on-site in Taylor works for me and I can support whatever schedule the team needs."

---

## Questions to Ask David Rojas

At the end of the interview, ask these. They show you think like a capacity planner, not a job applicant.

1. "What does the split look like between short-range capacity management — daily and weekly WIP — and long-range planning at the 6 to 18 month horizon?"
2. "What tools and data infrastructure is the team currently using — are you pulling from MES data directly or through separate analytics platforms?"
3. "Where are the biggest gaps today — analytical tooling, forecasting maturity, or coordination between the engineering and production teams?"
4. "How mature is the use of statistical or ML forecasting in the current capacity process?"
5. "What does success look like in the first 90 days for this role?"
