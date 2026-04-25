# Audio Script — AI-Powered Job Search Pipeline
# Slug: job-search-ai
# HOST voice: nova | SEAN voice: onyx
# Chunk target: ~750 chars

---

**[HOST — voice: nova]**
Today we're doing something a little different. Instead of covering an A-W-S service or a data engineering pattern, we're walking through a real project Sean built — an A-I-powered job search pipeline that automates the entire application process from intake to submission. Sean, let's start with why. Why did you build this?

**[SEAN — voice: onyx]**
Honestly, necessity. Searching for a senior data engineering role means tailoring every resume, every cover letter, researching every company — and doing that manually for dozens of applications is a full-time job on top of the actual job search. I figured if I'm going to spend time on this, I'd rather spend it building a system that does the repetitive work and let me focus on the parts that actually require judgment.

**[HOST — voice: nova]**
And this isn't just a few scripts. Walk me through the overall scope.

**[SEAN — voice: onyx]**
The mental model I use is: it's a data pipeline where the input is a raw job posting and the output is a tailored, production-ready resume and cover letter, tracked in a structured system. Ten stages running in sequence, orchestrated by a single Python script. Drop in a job posting, run one command, get back a folder with everything you need to apply.

**[HOST — voice: nova]**
What's the first thing the pipeline does when a job comes in?

**[SEAN — voice: onyx]**
Before anything else, it runs a duplicate check. I've applied to a lot of jobs, and companies repost the same role constantly across different platforms. Running the full pipeline on something I've already applied to wastes time and A-P-I credits. So stage zero uses FAISS with local sentence-transformer embeddings to compare the new job description against every job I've already processed. If the semantic similarity is above the threshold, the pipeline blocks right there.

**[HOST — voice: nova]**
You're running the embeddings locally — not through an A-P-I?

**[SEAN — voice: onyx]**
Right. The embedding model is all-MiniLM-L6-v2, running locally via sentence-transformers with a FAISS index on disk. There's no cloud call for this step. It's fast, it's private, and it rebuilds the index in seconds when a new job is accepted. For something that runs on every single intake, keeping it local was the right call.

**[HOST — voice: nova]**
Once it passes the duplicate check, what happens?

**[SEAN — voice: onyx]**
Stage one is scoring. This is where the RAG pattern kicks in. The pipeline retrieves my master career profile — structured YAML with skills, roles, and experience summaries — and injects it alongside the job description into a structured prompt. Grok analyzes the combination and returns a match score, a skill gap analysis, and a recommendation. First live run scored an eighty-five percent match on a Collective Health role.

**[HOST — voice: nova]**
And "Grok" here — that's the xAI Grok API?

**[SEAN — voice: onyx]**
Exactly. xAI's Grok is the primary L-L-M. And I use it in two tiers. Grok-3-mini handles the lighter tasks — scoring, parsing, classification, company research. Grok-3, the full model, handles the heavy generation work — resume tailoring and cover letter writing. The reason is cost and quality. You don't need the full model to score a job or extract structure from a posting. But when you're generating content that's going in front of a hiring manager, you want the best reasoning you can get.

**[HOST — voice: nova]**
How does the Grok integration actually work under the hood?

**[SEAN — voice: onyx]**
Here's what I like about it — Grok exposes an OpenAI-compatible API endpoint. So the client is just the standard OpenAI Python library pointed at x-dot-ai instead of OpenAI. That means every LangChain chain, every prompt template, every tool that works with OpenAI works with Grok without any code changes. If I want to switch models or fall back to OpenAI, it's one environment variable. The model is a configuration parameter, not a code dependency.

**[HOST — voice: nova]**
Let's walk through the middle stages. After scoring and accepting a job, what does the pipeline do?

**[SEAN — voice: onyx]**
Stage three tailors the job data — the pipeline extracts structured information from the posting: required skills, preferred qualifications, seniority signals, company culture indicators, and maps them to the relevant parts of my profile. The output is a structured YAML file that drives everything downstream. Stage four generates the resume intermediate — a tailored JSON resume that selects and rewrites bullet points to match the role's keywords, while staying grounded in the master profile as the source of truth. Stage five renders that JSON into a production-ready DOCX resume and a Markdown preview.

**[HOST — voice: nova]**
The DOCX output is for direct submission?

**[SEAN — voice: onyx]**
Yes — A-T-S-safe formatting, ready to attach and submit. The Markdown preview is for quick review before submission. Then stage six runs company research — Grok fetches and summarises publicly available information about the company: size, recent news, engineering culture, tech stack signals. That research feeds directly into stage seven, the cover letter generation, so the letter references specific things about the company rather than generic filler.

**[HOST — voice: nova]**
And the pipeline classifies the type of employer?

**[SEAN — voice: onyx]**
That's actually one of the things I'm most pleased with. The cover letter generator classifies the target as either an agency or a direct employer and adjusts tone accordingly. Agency cover letters are more concise and skills-forward. Direct employer letters are more narrative and culture-aligned. That classification happens automatically from the job posting content.

**[HOST — voice: nova]**
What's the final stage before tracking?

**[SEAN — voice: onyx]**
There's a quality gate before the application is marked as submitted. A strict validation check that confirms all required output files exist, meet minimum size requirements, and pass basic content checks. Only after the quality gate passes does the pipeline write the application record to metadata YAML with the date, method, and status. If the quality gate fails, nothing gets marked as applied. It's a blocking step.

**[HOST — voice: nova]**
That's the same quality gate pattern from the data pipeline design work — no silent success.

**[SEAN — voice: onyx]**
Exactly the same principle. A pipeline that completes successfully but produces wrong output is more dangerous than one that fails. In this context, marking a job as "applied" when the documents aren't ready means I might not notice the application didn't actually go through. The gate forces that review.

**[HOST — voice: nova]**
Let's talk about one of the trickier engineering problems. What was the hardest thing to get right?

**[SEAN — voice: onyx]**
Two things stood out. The first was structured output reliability. Language models don't always return the YAML or JSON structure you asked for — sometimes you get free-form prose with the right information buried inside it. I built a regex-based extraction fallback layer that recovers structured data from improperly formatted responses. Combined with prompt templates that include concrete output format examples, the failure rate dropped significantly.

**[HOST — voice: nova]**
And the second?

**[SEAN — voice: onyx]**
Windows encoding in subprocess pipelines. The auto-pipeline script runs Python scripts as subprocesses to keep each stage isolated. On Windows, if a job description or a status message contains Unicode — which they do, because the scripts use emoji for status output — you hit encoding errors that silently truncate output or crash the subprocess. The fix was enforcing PYTHONUTF8=1 in the environment copy passed to every subprocess call, and explicit UTF-8 encoding on every file read and write.

**[HOST — voice: nova]**
The project didn't stop at the application pipeline. There's a whole second system here.

**[SEAN — voice: onyx]**
Right — that's what I call StudyBook. Once the application pipeline was running, I realized the other half of interview prep — actually knowing the material deeply enough to answer technical questions well — needed the same treatment. So I built a parallel pipeline: generate structured audio learning scripts for each topic, convert them to M-P-3 audio using G-P-T-4o text-to-speech, host the audio on Cloudflare R2, and generate complete H-T-M-L reference pages that go live on my GitHub Pages site.

**[HOST — voice: nova]**
And that's the website where this audio is hosted.

**[SEAN — voice: onyx]**
Exactly. The page you're reading right now was built by that pipeline. Twenty-one technical topics, each with audio, code examples, tables, interview Q-and-A, and a cheat sheet — all generated and maintained through automation. Claude Code orchestrates the quality review, gap analysis, and HTML regeneration. ChatGPT generates the initial content. The whole thing is A-I-assisted end to end.

**[HOST — voice: nova]**
What would you build differently if you started over?

**[SEAN — voice: onyx]**
What I've learned from this is that local JSON and YAML storage works fine for an M-V-P but starts to show friction when you want to query across jobs — "show me all roles where I scored above eighty percent" requires scanning files rather than a query. I'd add SQLite from the start. I'd also build the Streamlit U-I earlier. The C-L-I is great for automation but reviewing outputs is awkward without a proper interface. And I'd define the data contract between pipeline stages more formally from day one instead of letting the YAML structure evolve organically.

**[HOST — voice: nova]**
Last question — what was the most satisfying moment building this?

**[SEAN — voice: onyx]**
The first live run. Feeding in the Collective Health job description, watching the pipeline run all ten stages, and getting back a folder with a tailored resume, a research summary, and a cover letter that actually referenced specific things about the company. And the score said eighty-five percent match. That was the moment it stopped being a project and started being a tool.

**[HOST — voice: nova]**
A-I pipeline that builds your job search materials and your interview preparation library simultaneously — that's a genuinely useful system. The source is public on GitHub at github-dot-com slash seanlgirgis slash jobsearch.

**[SEAN — voice: onyx]**
And it's still actively evolving. The Gmail scanner for automatic job intake, the search integration, the Streamlit interface — all in progress. This one's not done.

---
END OF SCRIPT
Voices: HOST (nova), SEAN (onyx)
Project: AI-Powered Job Search Pipeline
GitHub: https://github.com/seanlgirgis/jobsearch
