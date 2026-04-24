# Learning Artifact Prompt Template
# Replace {{TOPIC}} with the exact topic name (e.g., "Terraform", "FastAPI").
# Generate A1, A2, B, C separately — one prompt per Codex/Gemini session.
#
# OUTPUT PATHS:
#   A1 script → D:\StudyBook\temp\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md
#   A1 audio  → run: python scripts\generate_audio_generic.py --script <path_to_A1_md> --output <audio_dir>
#   A2 HTML   → D:\StudyBook\temp\seanlgirgis.github.io\learning\{slug}.html
#   B, C      → D:\StudyBook\temp\jobsearch\data\interview_prep\artifacts\{topic}\

---

## ARTIFACT A1 — GPT-4o Audio Script
## (feeds directly into generate_audio_generic.py — same pipeline as interview prep audio)

```
You are a Professional Radio Scriptwriter producing a TTS-optimized learning audio script.
Topic: {{TOPIC}}
Target engine: gpt-4o-mini-tts / gpt-4o-mini-audio-preview

SPEAKERS:
  HOST  → voice: nova  (warm, curious — asks questions, introduces concepts, short turns)
  SEAN  → voice: onyx  (calm, senior, credible — explains, gives examples, states tradeoffs)

AUDIENCE: Sean is a senior Python/AWS/data engineer (20 years experience) preparing for a
technical interview at Toyota Financial Services (fintech). He knows cloud, data pipelines,
and Python deeply. He is building hands-on knowledge of {{TOPIC}}.
Skip basics. Go straight to how it works, why it exists, and what matters in production.

════════════════════════════════════════════════
NON-NEGOTIABLE RULES (same as master TTS rules)
════════════════════════════════════════════════

FORMATTING:
- Every block uses EXACT format: **[SPEAKER NAME — voice: voice_name]**
- One blank line after label, then spoken text, then --- divider
- Never two speakers in one block. Never metadata inside spoken text.

CONTRACTIONS — mandatory, no exceptions:
  "I have not" → "I haven't"  |  "It is" → "It's"  |  "I am" → "I'm"
  "Do not" → "Don't"  |  "That is" → "That's"  |  "We have" → "We've"

PAUSING via punctuation (controls TTS breathing):
  ,      → micro pause (~0.3s) — use naturally
  ...    → thoughtful pause (~1.0s) — after key claims, before pivots
  ......  → topic transition (~1.5-2.0s) — between major concept shifts only
  —      → sharp contrast break — use sparingly
  MAX 4 ellipses per block.

EMPHASIS via ALL CAPS — only for:
  Key metrics/numbers: "NINETY percent", "SIX THOUSAND endpoints"
  Critical contrast words: "EXACTLY", "FUNDAMENTALLY", "PRIMARY"
  MAX 3 ALL CAPS words per block.

PHONETIC NORMALIZATION — mandatory substitutions:
  AWS → A-W-S          |  API → A-P-I           |  ETL → E-T-L
  ECS → E-C-S          |  CI/CD → C-I-C-D       |  SQL → S-Q-L
  IAM → I-A-M          |  JWT → J-W-T            |  OAuth2 → Oh-Auth 2
  REST → R-E-S-T       |  FastAPI → Fast-A-P-I   |  OpenAPI → Open-A-P-I
  PySpark → Pie-Spark  |  scikit-learn → Sigh-kit-learn  |  PyTorch → Pie-Torch
  MSK → M-S-K          |  SQS → S-Q-S            |  VPC → V-P-C
  HCL → H-C-L          |  IaC → I-A-C            |  ECR → E-C-R
  (Add any topic-specific acronyms from {{TOPIC}} using the same pattern)

NUMBERS as spoken words:
  "8 years" → "eight years"  |  "90%" → "NINETY percent"
  "$185,000" → "ONE-HUNDRED AND EIGHTY-FIVE THOUSAND dollars"

NO markdown inside spoken text. No bullets, no headers, no backticks, no bold markers.
Convert lists to flowing spoken sentences ("First... Second... Third...").

CONVERSATIONAL BRIDGES — every SEAN block opens with one, rotate (no repeats in a row):
  "So... basically..."  |  "Here's the thing..."  |  "Here's the key insight..."
  "Right... so the way I think about this..."  |  "Let me give you a concrete example..."
  "Two things matter here..."  |  "Now... the important distinction is..."

CHUNKING: Each block ~1,200–1,800 characters of spoken text. Split at speaker turns only.

════════════════════════════════════════════════
SCRIPT STRUCTURE (produce all sections in order)
════════════════════════════════════════════════

Section 1 — Why {{TOPIC}} Exists (2 HOST + SEAN exchanges)
  HOST introduces the topic with a question like "So... what problem does {{TOPIC}} solve?"
  SEAN explains the core problem and why existing alternatives weren't enough.

Section 2 — Core Concepts (4–5 HOST + SEAN exchanges, one concept per exchange)
  HOST asks about each concept by name.
  SEAN explains with an analogy drawn from Python, AWS, or data engineering.
  For each: name it, explain it, give a real-world data engineering example.

Section 3 — End-to-End Workflow (1–2 exchanges)
  HOST: "Walk me through what actually happens when you use {{TOPIC}} end-to-end."
  SEAN describes a realistic fintech/data engineering scenario using {{TOPIC}}.
  Concrete, sequential — no vague generalities.

Section 4 — Tradeoffs: {{TOPIC}} vs Alternatives (2 exchanges)
  HOST asks directly: "When would you NOT use {{TOPIC}}?"
  SEAN names the alternatives (things the listener already knows) and states the tradeoffs clearly.

Section 5 — Common Mistakes (1–2 exchanges)
  HOST: "What do engineers get wrong with {{TOPIC}}?"
  SEAN names 2–3 specific mistakes. Direct. No hedging.

Section 6 — Recap Q&A (5 HOST questions + SEAN answers)
  These are the 5 most likely interview questions on {{TOPIC}}.
  SEAN answers each in 3–5 sentences. Interview-ready delivery.
  HOST questions are short (1 sentence). SEAN answers are confident and complete.

════════════════════════════════════════════════
OUTPUT FORMAT
════════════════════════════════════════════════

Begin with this header block:

## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)

HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male

Process each [SPEAKER] block as a separate API call.
Export each as MP3. Merge in sequence for final audio.

---

Then the full script using **[SPEAKER — voice: voice_name]** blocks.
End with: ## END OF SCRIPT

PROHIBITIONS:
❌ Do NOT invent content not grounded in {{TOPIC}}
❌ Do NOT add coaching notes, meta-commentary, or AI self-references
❌ Do NOT leave any technical acronym un-normalized
❌ Do NOT repeat the same conversational bridge twice in a row
❌ Do NOT exceed 4 ellipses per block
❌ Do NOT capitalize entire sentences
❌ Do NOT speak markdown characters, headers, or labels

BEGIN THE SCRIPT NOW.
```

---

## ARTIFACT A2 — HTML Article (for seanlgirgis.github.io/learning/)

```
You are a senior engineer writing a technical reference article on: {{TOPIC}}.
Output must be a complete, self-contained HTML file ready to save as
{{TOPIC_SLUG}}.html (e.g., terraform.html, fastapi.html).

EXACT SITE REQUIREMENTS — match these precisely:

1. Use this exact CSS (paste verbatim in <style> tag — do not modify):

:root {
    --primary: #004a99;
    --accent:  #e67e22;
    --text:    #222;
    --muted:   #666;
    --bg:      #f4f7f6;
    --line:    #dde3ea;
    --code-bg: #1e2a38;
    --code-fg: #e8edf2;
    --hi-bg:   #e8f4fd;
    --warn-bg: #fff8e6;
}
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; background: var(--bg); font-family: 'Inter', sans-serif; color: var(--text); line-height: 1.7; font-size: 16px; }
.doc { max-width: 820px; margin: 0 auto; background: #fff; padding: 48px 52px 80px; min-height: 100vh; }
@media (max-width: 680px) { .doc { padding: 28px 20px 60px; } }
.topnav { font-size:0.88em; margin-bottom:32px; color:var(--muted); }
.topnav a { color:var(--primary); text-decoration:none; }
h1 { color:var(--primary); font-size:2em; margin:0 0 10px; line-height:1.25; }
.subtitle { color:var(--muted); font-size:0.9em; margin:0 0 24px; }
.tag-row { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:32px; }
.tag { background:var(--hi-bg); color:var(--primary); padding:3px 10px; border-radius:12px; font-size:0.82em; font-weight:600; }
.audio-box { border:1px solid var(--line); border-left:5px solid var(--accent); border-radius:6px; padding:18px 22px; margin-bottom:36px; background:#fffdf9; }
.audio-box .audio-label { font-weight:700; color:var(--accent); font-size:0.92em; margin-bottom:10px; }
.toc { background:#f7f9fc; border:1px solid var(--line); border-radius:6px; padding:22px 28px; margin-bottom:44px; }
.toc h2 { margin:0 0 14px; font-size:0.82em; text-transform:uppercase; letter-spacing:0.08em; color:var(--muted); font-weight:700; }
.toc ol { margin:0; padding-left:20px; columns:2; column-gap:32px; }
.toc li { margin-bottom:6px; break-inside:avoid; }
.toc a { color:var(--primary); text-decoration:none; font-size:0.93em; }
.doc h2 { color:var(--primary); font-size:1.25em; margin:52px 0 14px; padding-bottom:8px; border-bottom:2px solid var(--line); }
.doc h3 { color:#333; font-size:1.02em; margin:28px 0 10px; }
.back-top { display:block; text-align:right; font-size:0.82em; color:var(--muted); text-decoration:none; margin-top:28px; padding-top:10px; border-top:1px solid var(--line); }
code { background:#eef2f7; color:var(--primary); padding:2px 6px; border-radius:3px; font-size:0.88em; font-family:'Consolas','Courier New',monospace; }
pre { background:var(--code-bg); color:var(--code-fg); padding:18px 22px; border-radius:6px; overflow-x:auto; font-size:0.87em; line-height:1.6; margin:14px 0; font-family:'Consolas','Courier New',monospace; }
pre code { background:none; color:inherit; padding:0; font-size:inherit; }
table { width:100%; border-collapse:collapse; margin:16px 0; font-size:0.91em; }
th { background:var(--primary); color:#fff; padding:9px 14px; text-align:left; font-weight:600; }
td { padding:8px 14px; border-bottom:1px solid #eee; }
tr:nth-child(even) td { background:#f8fafc; }
.hi { background:var(--hi-bg); border-left:4px solid var(--primary); padding:13px 17px; border-radius:0 5px 5px 0; margin:16px 0; font-size:0.95em; }
.warn { background:var(--warn-bg); border-left:4px solid var(--accent); padding:13px 17px; border-radius:0 5px 5px 0; margin:16px 0; font-size:0.95em; }
.qa { margin-bottom:22px; }
.qa-q { font-weight:700; color:var(--primary); margin-bottom:6px; font-size:0.97em; }
.qa-a { border-left:3px solid var(--accent); padding:10px 16px; background:#fffaf5; border-radius:0 5px 5px 0; font-style:italic; color:#444; line-height:1.75; }
.cheat { background:var(--code-bg); color:var(--code-fg); border-radius:6px; padding:22px 26px; }
.cheat-row { display:grid; grid-template-columns:170px 1fr; gap:10px; padding:7px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.9em; }
.cheat-row:last-child { border-bottom:none; }
.ct { color:#f5a623; font-family:monospace; font-weight:bold; }
.cd { color:#c8d8e8; }

2. Include this Google Fonts link in <head>:
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

3. Use this EXACT HTML skeleton — fill in the [...] placeholders:

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[TOPIC FULL NAME] - Engineering Reference | Sean Girgis</title>
<link rel="canonical" href="https://seanlgirgis.github.io/learning/[SLUG].html">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>[PASTE EXACT CSS ABOVE]</style>
</head>
<body id="top">
<div class="doc">

  <div class="topnav">
    <a href="https://seanlgirgis.github.io/#learning">&#8592; Learning Hub</a> / [TOPIC FULL NAME] - Engineering Reference
  </div>

  <h1>[TOPIC FULL NAME]</h1>
  <p class="subtitle">Engineering reference &middot; Senior Data Engineer &middot; Last updated [YYYY-MM-DD] &middot; [X]-[Y] min read</p>

  <div class="tag-row">
    [4–7 relevant .tag spans]
  </div>

  <div class="audio-box">
    <div class="audio-label">&#127911; Audio Overview</div>
    <audio controls preload="metadata" style="width:100%;margin-top:6px;">
      <source src="" type="audio/mp4">
    </audio>
    <p style="font-size:0.82em;color:#aaa;margin-top:8px;">Audio generated separately — paste URL when available.</p>
  </div>

  <div class="toc">
    <h2>Contents</h2>
    <ol>
      [TOC entries matching your sections]
    </ol>
  </div>

  [SECTIONS — see structure below]

</div>
</body>
</html>

4. SECTION STRUCTURE (produce all of these):

   s1: What {{TOPIC}} Actually Is — 3 paragraphs. What problem it solves. How it fits the AWS/data stack.
       End with a <div class="hi"> callout: the single most important mental model.
       Include a <pre> ASCII diagram showing {{TOPIC}}'s place in the stack.

   s2: Core Concepts — cover 4–6 fundamental concepts. Each gets an <h3>, 2–3 paragraphs,
       and a <pre> code snippet (HCL, Python, YAML, or CLI as appropriate).
       Use <div class="warn"> for at least one common mistake per section.

   s3: [Topic-specific deep section — e.g., "State Management" for Terraform,
        "Routing & Dependency Injection" for FastAPI. You decide the best topic.]
       Include a comparison <table> with relevant alternatives.

   s4: [Topic-specific deep section #2 — e.g., "Remote Backends & Workspaces" for Terraform,
        "Auth & Security" for FastAPI.]
       Include at least one <pre> code block showing a realistic pattern.

   s5: {{TOPIC}} in Production — a realistic end-to-end scenario in a fintech/data engineering context.
       Prose description + a <pre> showing the key config or command sequence.
       Use <div class="hi"> for the key architectural insight.

   s6: Common Gotchas & Anti-Patterns — minimum 5 items. Prose, not bullets.
       Use <div class="warn"> for the most dangerous one.

   s7: 10 Key Engineering Interview Questions
       Use .qa / .qa-q / .qa-a div structure. Answers: 3–5 sentences each.
       Questions must cover: conceptual, tradeoff, hands-on, and architecture.
       Answers must sound like a confident senior engineer — not a textbook.

   s8: Quick Reference Cheat Sheet
       Use .cheat div with .cheat-row / .ct / .cd structure.
       Cover: key CLI commands, key config patterns, key terms.
       Minimum 12 rows.

5. After every h2 section (s1 through s7), include:
   <a class="back-top" href="#top">&#8593; Back to top</a>

6. CONTENT QUALITY:
   - Write at senior engineer level. Skip obvious basics.
   - Be opinionated: state what the right approach is and why.
   - Every table must have a "Data Engineering Use Case" or "When to Use" column.
   - Every code block must be syntactically correct and represent a real pattern (not pseudocode).
   - No filler sentences. If a sentence doesn't teach something, cut it.

AUDIENCE CONTEXT: Senior Python/data engineer preparing for Toyota Financial Services
technical interview (fintech, Python/AWS/DevOps/microservices role).
This article will be published at seanlgirgis.github.io/learning/{{TOPIC_SLUG}}.html

OUTPUT: The complete HTML file only. No markdown. No explanation outside the HTML.
BEGIN NOW.
```

---

## ARTIFACT B — Tutorial + Interview Q&A (Markdown — for personal study)

```
You are a senior engineer writing a technical study guide on: {{TOPIC}}.

AUDIENCE: Senior Python/data engineer preparing for a technical interview at Toyota Financial
Services (fintech). Role: Lead Senior Python Developer. Emphasis: Python, AWS, microservices,
DevOps, platform engineering. Engineer has strong Python/AWS but is building hands-on
depth in {{TOPIC}}.

FORMAT: Markdown. Working code only — no pseudocode. Target: 2,000–3,000 words.

STRUCTURE:

### 1. 60-Second Mental Model
One paragraph. What {{TOPIC}} is and why it exists. One sentence on where it fits in
a modern cloud/data stack.

### 2. Setup
Exact install commands. Only what's needed to follow the examples below.

### 3. Core Concepts with Code
4–6 concepts. For each:
- Concept name as heading
- 2–3 sentence explanation
- Working code snippet with inline comments
- One "gotcha" — the mistake most engineers make with this concept

### 4. Realistic End-to-End Example
Complete working example in a fintech/data engineering context. All code included.
Inline comments on non-obvious decisions.

### 5. Interview Q&A — 12 Questions
Format:
**Q: [question]**
A: [3–5 sentence answer. Direct. Includes the key term, the key tradeoff, when you'd use it.
   Sounds like a senior engineer, not a textbook.]

Cover: conceptual, tradeoff (X vs Y), hands-on ("how would you..."), architecture design.

### 6. Cheat Sheet
Compact table or list:
- Key CLI commands
- Key config patterns / code snippets
- Key terms with one-line definitions

OUTPUT: Markdown only. Begin with the 60-Second Mental Model — no preamble.
```

---

## ARTIFACT C — Capstone Project Spec

```
You are a senior engineering mentor designing a hands-on capstone project on: {{TOPIC}}.

AUDIENCE: Senior Python/data engineer who studied {{TOPIC}} and now needs to BUILD something
to demonstrate working knowledge before a technical interview at Toyota Financial Services.
Completable in 2–4 hours on a laptop. Free-tier AWS acceptable; no paid services unless
free tier is explicitly stated.

The deliverable must be demo-able or describable in an interview.

OUTPUT FORMAT:

### Project Title
Short, professional name.

### What You're Building
2–3 sentences. End state: what runs, what it does, what you can show.

### Why This Proves the Skill
List 5–6 specific competencies an interviewer would probe, explicitly mapped to this project.

### Prerequisites
Tools + installs (exact commands). Accounts needed. Estimated setup time.

### Step-by-Step Build
Numbered steps. Each step:
- What and why
- Exact code, config, or command
- Expected output / verification ("You should see...", "Run X to confirm Y")

Steps must build incrementally — the engineer understands the system as it grows.

### Validation Checklist
8–10 checkboxes the engineer can tick to confirm completion and correctness.
Frame each as a test: "[ ] Running X shows Y."

### Extension Challenges
3 stretch goals (Easy / Medium / Hard). 15–30 min each.

### Interview Talking Points
6–8 bullets framed for a hiring manager:
- Key architectural decisions made and why
- Scale considerations
- What breaks at 10x and how you'd address it
- What you'd add in a real production system

OUTPUT: Markdown only. Begin with Project Title — no preamble.
```

---

## TOPIC QUEUE

| # | Topic | Slug | A1 Audio | A2 HTML | B Study | C Capstone |
|---|-------|------|----------|---------|---------|------------|
| 1 | Terraform | terraform | ☐ | ☐ | ☐ | ☐ |
| 2 | FastAPI | fastapi | ☐ | ☐ | ☐ | ☐ |
| 3 | CI/CD with GitHub Actions + Docker + ECS | cicd-github-ecs | ☐ | ☐ | ☐ | ☐ |
| 4 | AWS CloudFormation | aws-cloudformation | ☐ | ☐ | ☐ | ☐ |
| 5 | AWS MSK / Apache Kafka | aws-msk-kafka | ☐ | ☐ | ☐ | ☐ |
| 6 | Snowflake + PyIceberg | snowflake-pyiceberg | ☐ | ☐ | ☐ | ☐ |
| 7 | OpenSearch / Elasticsearch | opensearch | ☐ | ☐ | ☐ | ☐ |

---

## USAGE NOTES

1. **Start with Terraform — it's 🔴 Critical.** Ramya (Toyota recruiter) flagged it explicitly.
   Technical HM interview is week of April 28.

2. **Order per topic:** A1 → run audio → A2 → B → C

3. **A1 Audio Pipeline (same as interview prep audio):**
   a. Paste A1 prompt (with {{TOPIC}} filled in) into Codex or GPT-4o
   b. Save output to:
      `D:\StudyBook\temp\jobsearch\data\interview_prep\audio_prep\{topic_slug}\audio_script_{topic_slug}.md`
   c. Run env_setter.ps1 (loads OPENAI_API_KEY)
   d. Run: `python scripts\generate_audio_generic.py --script <path_to_script.md>`
      (optionally add --output <dir> — defaults to audio_clips/ next to script)
   e. Stitch MP3s with ffmpeg (the script prints the exact command when done)
   f. Upload final MP3 to R2 or hosting, paste URL into A2 `<audio src="">` tag

4. **Do NOT use NotebookLM for A1.** It goes off-topic. The A1 prompt produces a
   HOST + SEAN dialogue in the exact `**[SPEAKER — voice: voice_name]**` format
   that `generate_audio_generic.py` expects. Feed it straight to the GPT-4o pipeline.

5. **A2 HTML files go to:** `D:\StudyBook\temp\seanlgirgis.github.io\learning\{slug}.html`
   **B and C go to:** `D:\StudyBook\temp\jobsearch\data\interview_prep\artifacts\{topic}\`

6. **One Codex/Gemini session per artifact.** Don't combine — context limits degrade quality.

7. **For {{TOPIC_SLUG}} in A2:** use the slug from the queue table above
   (e.g., "terraform", "fastapi", "aws-msk-kafka").

8. **generate_audio_generic.py** is the reusable script (replaces the hardcoded
   generate_interview_audio.py). Works for any A1 script AND interview prep audio files.
   Located at: `D:\StudyBook\temp\jobsearch\scripts\generate_audio_generic.py`
