# TOYOTA RAMYA RECRUITER SCREEN — GPT-4o-mini-audio-preview SCRIPT
# Thursday April 23, 2026 — 10:00 AM CT

---

## API INSTRUCTIONS FOR CALLER

This script is formatted for the GPT-4o-mini-audio-preview API.
Two voices are required — call the API separately for each speaker and stitch the audio.

**RAMYA voice:** `nova` — warm, professional female (Toyota's best for a recruiter persona)
**SEAN voice:** `onyx` — deep, authoritative male (best for a senior engineering candidate)

### Sample API call per line:
```
model: gpt-4o-mini-audio-preview
modalities: ["text", "audio"]
audio: { voice: "nova", format: "mp3" }   ← for RAMYA lines
audio: { voice: "onyx", format: "mp3" }   ← for SEAN lines
temperature: 0.7
```

Process each speaker block separately, export as MP3, then merge in sequence.

---

## SCRIPT BEGINS

---

**[RAMYA — voice: nova]**

Hi Sean... good morning! I'm Ramya Ravichandran... recruiter here at Toyota Financial Services. Thanks SO much for making time today. I was referred to you by Codie... and she spoke VERY highly of you. So... I'm reaching out about the Lead Senior Python Developer role... requisition one-zero-three-zero-one-six-five-five. Before we dive in... can you just tell me a little about yourself?

---

**[SEAN — voice: onyx]**

Of course... thanks for having me, Ramya. So... basically... I'm a Senior Python Developer with over TWENTY years of enterprise experience. Most recently... I spent EIGHT years at Citi as a Senior Capacity and Data Engineer — that was my longest and deepest role... and honestly... it was FUNDAMENTALLY a Python platform engineering job. Here's the core of what I did... I built backend data infrastructure for capacity planning across FOUR global regions — automated Python pipelines consuming REST A-P-I-s from enterprise monitoring systems... processing telemetry from SIX THOUSAND plus endpoints... containerized with Docker on A-W-S E-C-S... with C-I-C-D deployment workflows baked in. I built reusable modules that MULTIPLE engineering teams consumed — not one-off scripts... but platform-grade Python services. Now... on top of that... I built something called HorizonScale — an A-I-driven forecasting engine in Python using Prophet and Sigh-kit-learn... deployed on A-W-S with a Streamlit dashboard for real-time insights. It cut forecasting cycle time by NINETY percent. I'm in Plano... the four-day onsite works perfectly for me... I'm available immediately... and the Lead Senior Python Developer role at Toyota Financial is EXACTLY the kind of platform engineering work I want to do next.

---

**[RAMYA — voice: nova]**

Wow... that's a really impressive background... I can see why Codie was excited. Now... why Toyota Financial Services specifically? What drew you to THIS role?

---

**[SEAN — voice: onyx]**

Here's the thing... Toyota Financial Services operates at a scale where engineering quality directly affects MILLIONS of customers. The combination of Python platform work — microservices... REST A-P-I-s... A-W-S — combined with the rigor of a financial services environment... that's EXACTLY what I'm built for. I spent eight years at Citi doing precisely this kind of work in a regulated... high-stakes financial services environment. Toyota Financial is... basically... the natural next chapter — same discipline... larger platform... MORE impact. And look... the Plano location is a strong fit too — I'm local... no relocation... I can be in the office four days a week from day ONE.

---

**[RAMYA — voice: nova]**

That makes total sense... I love that. Now let's talk a bit about your technical background... can you walk me through your Python and A-W-S experience?

---

**[SEAN — voice: onyx]**

Absolutely. So... Python has been my PRIMARY language for eight-plus years. At Citi I used it for EVERYTHING — REST A-P-I integrations consuming TrueSight and AppDynamics A-P-I-s... E-T-L pipeline design with Pandas and Pie-Spark... M-L model development with Prophet and Sigh-kit-learn... and building reusable Python framework modules that other engineering teams consumed. Now... on the A-W-S side... I built a hybrid platform using S-3 as the data landing zone... A-W-S Glue for E-T-L transformation jobs... Redshift for analytical workloads... and E-C-S and Fargate for containerized Python pipeline execution. I containerized Python E-T-L jobs with Docker for on-demand cloud-scale processing... and I built C-I-C-D deployment pipelines to keep delivery consistent across environments. For this Toyota role specifically... the E-T-L pipeline stack on Glue... S-3... Lambda... and E-C-S? That maps DIRECTLY to what I built at Citi. E-C-S Fargate... A-P-I Gateway... CloudWatch — I'm comfortable in that environment.

---

**[RAMYA — voice: nova]**

Perfect... that's great to hear. The role mentions REST A-P-I-s and microservices quite a bit... have you actually BUILT those in Python?

---

**[SEAN — voice: onyx]**

Yes — and here's the key thing... REST A-P-I integration and building modular... A-P-I-first Python services... that's been CORE to what I've been doing. At Citi I built Python services that consumed REST A-P-I-s from multiple enterprise systems — BMC TrueSight... AppDynamics... CMDB — extracted... transformed... and loaded data into downstream pipelines. I designed those modules to be independently deployable and reusable — it's the SAME pattern as microservices architecture. On the documentation side... I've worked with A-P-I contracts and structured interface design. Fast-A-P-I and Open-A-P-I... Swagger specifically... I've been building with those patterns and I'm actively deepening my Fast-A-P-I experience. Honestly... the framework is very approachable for someone with strong Python and REST A-P-I background — the learning curve is minimal.

---

**[RAMYA — voice: nova]**

Got it... and what about E-T-L pipelines on A-W-S? Tell me more about that experience.

---

**[SEAN — voice: onyx]**

Strong and direct. At Citi... I built E-T-L pipelines on A-W-S using S-3 as the raw data landing zone... A-W-S Glue for transformation jobs... and Redshift as the analytical target. I used the Glue Data Catalog to manage schema metadata across datasets. For compute... containerized Python E-T-L jobs on E-C-S and Fargate — Docker images deployed on demand... scaled automatically... no server management needed. Lambda for lightweight... event-driven triggers between pipeline stages. The specific stack in THIS Toyota role — Glue E-T-L... Glue Catalog... S-3... Lambda... E-C-S — that is the stack I have PRODUCTION experience with.

---

**[RAMYA — voice: nova]**

Love it... now... the role also mentions Terraform. Do you have experience with that?

---

**[SEAN — voice: onyx]**

I'll be straight with you... I haven't used Terraform in production. My infrastructure work at Citi was provisioned through internal platforms and A-W-S-native tooling directly. Terraform's on my active learning list... and honestly... I can ramp quickly — the declarative infrastructure-as-code model is straightforward for someone with deep A-W-S hands-on experience. It's a tool gap... not a knowledge gap.

---

**[RAMYA — voice: nova]**

I appreciate the honesty... that's totally fine. Now... tell me about a challenging project you're really proud of.

---

**[SEAN — voice: onyx]**

Two come to mind... Let me start with the FAST project at G6 Hospitality — that's the parent company of Motel 6. Here's the story... I built an E-T-L pipeline that mined Dynatrace AppMon for real-user performance data across the Brand-dot-com ecommerce site. Now... this wasn't guesses or synthetic tests — this was ACTUAL user behavior data... extracted and analyzed through Python. We used data mining to identify the EXACT bottlenecks that were costing the site revenue. The whole philosophy was... instrument... extract... mine... act. Simple as that...... Now... the SECOND one is HorizonScale at Citi. I needed to forecast capacity for THOUSANDS of infrastructure assets... SIX months ahead... but the legacy process was a TEN-DAY manual Excel cycle. Completely reactive... always behind. So... I built HorizonScale from scratch in Python — Pie-Spark pipeline at banking scale... Prophet for time-series forecasting... Sigh-kit-learn classifiers for risk flagging... generator-based parallel architecture so assets processed SIMULTANEOUSLY instead of one by one. The result? NINETY percent cycle time reduction... and six-month-ahead bottleneck prediction at NINETY percent-plus accuracy. That went from a ten-day manual process... to MINUTES.

---

**[RAMYA — voice: nova]**

That's... genuinely impressive. How do you handle ambiguity? Like when requirements aren't clear?

---

**[SEAN — voice: onyx]**

Basically... I anchor on the data and work backwards to the decision. Here's a real example — at Citi... when I joined... there was NO clear owner for capacity planning. Just a manual process and a lot of tribal knowledge floating around. So I mapped what data existed... what decisions depended on it... and what was missing. That gave me a roadmap... even when the requirements were completely unclear. My experience is... ambiguity usually means stakeholders haven't agreed on what PROBLEM they're solving. I bring them a shared data model... and let the NUMBERS drive the conversation to a decision.

---

**[RAMYA — voice: nova]**

That's a great approach. Now... why are you leaving Citi? What happened there?

---

**[SEAN — voice: onyx]**

So... I was at Citi for EIGHT years and delivered strong results — I built the capacity planning platform from the ground up. My role was eliminated as part of a broader organizational restructuring... NOT performance related. I've used the time to sharpen my skills... and I'm focused on finding the right long-term fit. Toyota Financial is at the TOP of my list.

---

**[RAMYA — voice: nova]**

Understood... and are you interviewing with other companies right now?

---

**[SEAN — voice: onyx]**

Yes... I have a few conversations in progress — including with Samsung and Capital One. But... Toyota Financial is my TOP priority... given the Python platform focus... the Plano location... and the financial services environment I know well.

---

**[RAMYA — voice: nova]**

Good to know. Are you authorized to work in the United States?

---

**[SEAN — voice: onyx]**

I'm a U-S citizen. No visa... no sponsorship needed... no restrictions of any kind.

---

**[RAMYA — voice: nova]**

Perfect. This role requires four days onsite in Plano... with Friday as a potential remote day. Is that acceptable?

---

**[SEAN — voice: onyx]**

Fully comfortable. I'm in Plano — the commute's easy... and honestly... I PREFER being in the office with the team.

---

**[RAMYA — voice: nova]**

Wonderful. And... what is your salary expectation for this role?

---

**[SEAN — voice: onyx]**

I'm targeting ONE-HUNDRED AND EIGHTY-FIVE THOUSAND dollars base.

---

**[RAMYA — voice: nova]**

Got it. And when would you be able to start?

---

**[SEAN — voice: onyx]**

I'm available to start IMMEDIATELY... and I can align with whatever onboarding timeline works for the team.

---

**[RAMYA — voice: nova]**

That's great to hear. Do you have any questions for me?

---

**[SEAN — voice: onyx]**

A few... Now... first — what does the technical interview with the hiring manager look like? Format... focus areas... what should I be preparing for? Second... is this a new headcount from the recent reorg... or a backfill? Third... what does the team structure look like — size... what they're building... where this role sits? And... fourth... what's the timeline from this conversation to an offer?

---

**[RAMYA — voice: nova]**

Those are GREAT questions... I'll follow up with all of that detail. Thank you SO much Sean — it was really wonderful speaking with you today.

---

**[SEAN — voice: onyx]**

Thank you Ramya... I genuinely appreciate the time... and I'm looking forward to next steps.

---

## END OF SCRIPT
