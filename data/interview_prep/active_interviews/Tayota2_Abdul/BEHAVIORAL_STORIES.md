# Behavioral Stories — Abdul Interview
**Toyota Way Values mapped to your real projects**
*Read once. Sleep on it. You already know these stories.*

---

## Story 1 — "Tell me about a time you solved a problem at a scale you hadn't seen before"
**Toyota Value: Drive Curiosity + Get Better and Better**

**S:** At HorizonScale we had 2,000+ servers and needed 180-day capacity forecasts. Nobody had built this before internally. The data was 8,000+ time series — way too many to model manually.

**T:** I needed a forecasting system that could handle that volume, pick the right model per series, and actually be trusted by the ops team.

**A:** I got curious about the data first — spent time understanding how different server types behaved before writing a line of code. Then I built a model tournament: Prophet, ARIMA, Holt-Winters running head to head, with the winner selected automatically by error metric per series. Built observability in so the team could see which model won and why.

**R:** We went from manual one-off forecasts to a platform that ran across the full fleet. Ops team started making proactive capacity decisions instead of reactive ones. The curiosity paid off — if I'd just picked one model and shipped it, half the fleet would have had bad forecasts.

---

## Story 2 — "Tell me about a time a system failed and how you handled it"
**Toyota Value: Observe Thoroughly + Work with Integrity**

**S:** At Citi we had a telemetry pipeline feeding financial dashboards. One morning the dashboards went green — no alerts — but the numbers looked wrong to an analyst who knew the data well.

**T:** I had to figure out if it was a data problem or a display problem, fast, without panicking the team or escalating prematurely.

**A:** I went to the source — not the dashboard, not the logs. I pulled the raw Bronze layer and compared it to what was showing in Gold. Found that a schema change upstream had shifted a column name. The pipeline kept running, records were landing, but the join was silently dropping rows. Classic schema drift. I quarantined the affected partition, fixed the transformation, and replayed from Bronze. Then I added a schema contract check at ingestion so it would alert next time, not pass silently.

**R:** Data was corrected and back in dashboards within two hours. More importantly I made the invisible failure visible. Green pipelines don't guarantee correct data — that was the lesson we built into the system.

---

## Story 3 — "Tell me about a time you delivered something that changed how a team operated"
**Toyota Value: Act for Others + Create Room to Grow**

**S:** At G6 Hospitality, the operations team was flying blind. They had alerts, but the alerts were noise — firing constantly with no signal. Engineers were fatigued and ignoring them.

**T:** My job was to build an observability platform using Dynatrace that operations could actually trust and act on.

**A:** I started by sitting with the ops team — not the engineers. I asked what decisions they needed to make and when. Turned out they didn't need more data, they needed the right three signals at the right time. I redesigned the alerting around those three signals, added synthetic monitoring to catch issues before real users hit them, and built the FAST project dashboard so the morning standup had one source of truth.

**R:** Alert fatigue dropped dramatically. The ops team went from ignoring dashboards to running their morning standup off them. The shift was simple: I treated ops as the customer, not the endpoint.

---

## Story 4 — "Tell me about a time you had to convince a team to change direction"
**Toyota Value: Work with Integrity + Show Respect for People**

**S:** We were mid-build on a data pipeline and a senior engineer on the team was pushing to load the full table every run — full reload, every hour. It was simpler to code. The timeline pressure made everyone want to agree.

**T:** I knew at the data volumes we were projecting, full reloads would become cost-prohibitive and slow within three months. I had to make the case without creating conflict.

**A:** I didn't argue in the meeting. I built a quick projection — took the current table size, growth rate, and hourly reload cost — and put the numbers in front of the team quietly. Not "you're wrong," but "here's what this looks like in Q3." Then I offered to own the incremental design so the complexity wasn't on him.

**R:** The team moved to incremental. No drama. Six months later the pipeline was processing 10x the original volume and the cost was a fraction of what full reloads would have been. The lesson: integrity means showing the truth, not winning the argument.

---

## Story 5 — "Tell me about a time you improved a process that others had accepted as normal"
**Toyota Value: Continue the Quest for Improvement**

**S:** On the Citi team, every deployment was a manual checklist — someone SSHed into servers, ran commands, checked logs by hand. It took 45 minutes and two engineers. Everyone accepted it because it had always been that way.

**T:** I thought if one step goes wrong, there's no rollback, no audit trail, and it depends on whoever is on-call that week knowing the exact order.

**A:** I proposed automating the deployment with a CI/CD pipeline — nothing fancy, just parameterized jobs with a clear pass/fail gate and a rollback step. I built it on my own time first to show it worked, then walked the team through it. I made sure the senior engineer who owned the checklist was the one who ran the first automated deploy, not me.

**R:** Deployments went from 45 minutes and two people to 8 minutes and one approval click. More importantly, every deploy was now auditable. The team lead later said it was one of the highest-value things we shipped that quarter — and it wasn't on anyone's roadmap.

---

## The One-Line Version (for when your brain is foggy)

| Story | One Line |
|---|---|
| HorizonScale forecasting | "I got curious before I coded — ran a model tournament across 8,000 series" |
| Citi schema drift failure | "Green pipeline, wrong data — I traced it to silent schema drift and replayed from Bronze" |
| G6 ops dashboard | "I treated ops as the customer, not the endpoint — three signals beat 300 alerts" |
| Incremental vs full reload | "I put the numbers in front of the team, not the argument" |
| CI/CD improvement | "45 minutes manual → 8 minutes automated, and I let the senior guy run the first one" |

---

*You know these stories. Sleep. Wednesday you sharpen. Thursday you show up.*

---

## The Opener — "Why Toyota?"

> "Toyota Financial Services is enabling people to own vehicles they couldn't otherwise — that's a real equity play. I want to build the data platform that makes that run reliably at scale."

30 seconds. Specific. Done.

**Wednesday morning — 10 minutes only:** Google "Toyota Financial Services Mobility for All 2026" so you have one real recent detail to drop in. One fact. That's it.

---

## Virtual Interview Reminders (Teams over computer)

- **Camera on. Business casual on top. Background clean. Lighting in front of you, not behind.**
- **The PDF said "computer skills."** For a Lead SE that's not about Excel. It means: can you communicate clearly without being in the room? Every answer you give is a demo of that. Structured. Not rushing. Eye contact with camera not screen.
- **Smile when you join.** Abdul sees your face before you speak. First impression is frame and energy, not words.
