# Samsung HM Interview — Audio 3: Manufacturing Domain Knowledge
## What This Audio Covers
The semiconductor and manufacturing concepts David Rojas will probe: Factory Physics, OEE, SEMI E10, Little's Law, takt time, lot starts, yield, and supply chain. These are the domain-specific questions that separate you from a generic data engineer.

---

## Factory Physics — What It Is and How You Apply It

Factory Physics is the study of how manufacturing systems behave under load — specifically the relationships between WIP, throughput, and cycle time.

The foundational relationship is Little's Law: L equals lambda times W. Average WIP equals throughput rate times average cycle time. Know two, you know the third.

In a fab: if 100 lots are in WIP and throughput is 20 lots per day, average cycle time is 5 days. If WIP doubles to 200 lots but throughput stays at 20 lots per day, cycle time doubles to 10 days. That is the lever — you cannot improve cycle time without either increasing throughput or reducing WIP.

The other critical behavior: as tool utilization approaches 100 percent, cycle time increases exponentially — not linearly. A tool at 95 percent utilization has dramatically worse cycle time than one at 80 percent, even though the utilization gap looks small. That nonlinear behavior is what Factory Physics captures — and it is why capacity planning cannot just chase utilization to 100 percent.

You applied the same queuing theory in IT — a server at 90 percent utilization behaves very differently from one at 70 percent. The math translates directly.

---

## OEE — Overall Equipment Effectiveness

OEE is the standard manufacturing KPI measuring actual equipment performance versus theoretical maximum.

The formula: OEE equals Availability times Performance times Quality.

- **Availability:** Actual uptime divided by planned production time — captures downtime losses
- **Performance:** Actual throughput rate divided by ideal rate — captures slow cycle losses
- **Quality:** Good units divided by total units — captures yield losses

Example: 90 percent availability times 80 percent performance times 95 percent quality equals 68.4 percent OEE. World-class targets 85 percent or higher.

For capacity planning, OEE is the bridge from theoretical to real capacity. A tool rated at 100 lots per week at 68 percent OEE delivers 68 lots per week effective. Plan against theoretical and you will consistently miss output.

You used identical logic in IT — effective capacity equals theoretical times availability times performance efficiency. Raw CPU capacity is never real capacity. The math is the same, the terminology shifts.

---

## SEMI E10 Equipment States

SEMI E10 is the industry standard classifying every minute of equipment time into one of six states:

- **Productive:** Processing wafer lots — the only state that generates output
- **Standby:** Ready but no product in queue
- **Engineering:** Experiments, qualifications, process development
- **Scheduled Downtime:** Planned preventive maintenance, calibrations
- **Unscheduled Downtime:** Unexpected failures, waiting for parts
- **Off:** Not available

These states matter because they define what actually happened to your capacity budget. A tool with 15 percent in engineering and 12 percent in unscheduled downtime has far less productive window than the calendar suggests. Rising unscheduled downtime is an early warning signal of equipment reliability issues before you see the output miss.

---

## Little's Law — Explained with an Example

Little's Law: L equals lambda times W. Average WIP equals throughput rate times average cycle time.

Fab example: 100 lots in WIP, throughput 20 lots per day, cycle time equals 5 days. WIP doubles to 200, throughput stays at 20 lots per day, cycle time doubles to 10 days.

The power: you do not need to measure cycle time directly. Calculate it from WIP and throughput, both of which are observable.

The lever: to reduce cycle time without reducing WIP, increase throughput. To reduce cycle time without increasing throughput, reduce WIP. There is no free lunch.

---

## Takt Time — What It Is and How It Connects to Capacity Planning

Takt time is the pace at which you must produce to meet customer demand. The formula is: available production time divided by customer demand rate.

Example: 168 hours per week available, customers need 200 lots per week. Takt time equals 0.84 hours per lot. The factory must complete one lot every 50 minutes.

For capacity planning: takt time sets the floor for required throughput. If the bottleneck tool completes one lot every 70 minutes, you have a gap — add capacity, reduce demand, or accept a miss.

Takt time also drives lot start planning: if cycle time is 45 days and you need 200 lots out in week 10, lot starts must begin in week 3.

---

## Lot Starts — How They Connect to Output Planning

Lot starts are the input lever for controlling output. The relationship is: Output equals Lot Starts times Yield, adjusted for cycle time and WIP.

You cannot pull product on demand — everything has a multi-week cycle time. The question is: given what we need to ship 6 to 8 weeks from now, what do we need to start today?

Lot start planning requires: demand signal, yield estimate per product, cycle time by product, current WIP in the line, and bottleneck tool capacity.

Same logic in IT: to hit a future capacity target you start procurement now because hardware lead times are 3 to 6 months. Forward-planning horizon and yield and attrition accounting are identical concepts.

---

## Yield — How It Impacts Capacity Planning

Yield is critical and often underweighted. If a step has 95 percent yield — 5 percent of lots fail or need rework — to produce 100 good lots you must start 105. That overhead is built into the lot start plan and tool capacity model.

Yield loss at the bottleneck is doubly expensive: you consumed bottleneck capacity on a lot that did not contribute to output. 5 percent yield loss at the bottleneck equals 5 percent effective capacity loss.

For long-range modeling: build yield assumptions per product and step, with sensitivity analysis — what does the capacity picture look like if yield drops from 95 percent to 90 percent? That drives both the lot start buffer and the equipment investment decision.

---

## Supply Chain Management in a Fab Context

Two dimensions in semiconductor manufacturing:

**Equipment supply chain:** Leading-edge fab tools have 18 to 24 month lead times. A capacity gap identified today cannot be filled for 2 years. Capacity planning must look 24 plus months out and signal equipment needs well ahead of demand. Spare parts are critical too — a tool down waiting for a part for 3 weeks is a massive capacity loss. Stocking decisions for critical spares are a supply chain optimization problem.

**Materials and consumables:** Wafers, gases, chemicals, photomasks. Demand forecasting feeds procurement cycles. A sudden lot start ramp requires more raw wafers — if procurement did not anticipate it, the capacity plan is impossible to execute regardless of tool availability.

The capacity planner sits at the intersection of both: forecast demand accurately, communicate constraints to production, give procurement enough lead time to support the plan. You did the same at Citi — your 6-month forecasting horizon aligned directly to the hardware procurement cycle.
