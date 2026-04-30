# AI-Powered Job Search Pipeline

<a id="toc"></a>
## Table of Contents
1. [Structured Output Reliability](#sec-1)
2. [Windows Encoding in Subprocess Pipelines](#sec-2)

GitHub: [seanlgirgis/jobsearch](https://github.com/seanlgirgis/jobsearch)

---

## Why It Was Built

Searching for a senior data engineering role means tailoring every resume,
every cover letter, and researching every company. Done manually across dozens
of applications, that's a full-time job stacked on top of the actual job
search.

The goal: automate the craft — produce tailored, high-quality, grounded
documents for each role at a fraction of the time cost. Every output is
reviewed before submission. The pipeline removes the friction, not the
judgment.

The pipeline is not a bot that fires off applications automatically. It
produces a production-ready folder — resume, cover letter, company research —
and the human decides whether to submit.

---

## Pipeline Mental Model

Input is a raw job posting. Output is a tailored, production-ready application
package tracked in a structured system. Ten stages run in sequence, orchestrated
by a single Python script. Drop in a posting, run one command, get back a
folder with everything needed to apply.

The orchestrator is `scripts/10_auto_pipeline.py` — runs each stage as a
subprocess, passes the job UUID as context, and halts immediately on any
stage failure.

**Stage map**

`00` Duplicate Gate — FAISS semantic similarity check against all previously processed jobs.
`01` Job Scoring — RAG-based match score, skill gap analysis, and recommendation via Grok.
`02` Intake Decision — accept or reject based on score threshold; rejected jobs are logged but not processed.
`03` Job Tailoring — extract structured YAML: skills, qualifications, seniority signals, culture indicators.
`04` Resume Intermediate — generate tailored JSON resume; select and rewrite bullets to match role keywords.
`05` Resume Render — render JSON to ATS-safe DOCX + Markdown preview.
`06` Company Research — Grok fetches and summarises company size, culture, tech stack, recent news.
`07` Cover Intermediate — generate tailored cover letter JSON with research embedded.
`08` Cover Render — render cover letter to DOCX; classify employer type (agency vs direct) and adjust tone automatically.
`09` Quality Gate + Status — validate all outputs exist, meet size requirements, pass content checks; write metadata YAML.

---

## Stage 00 — Duplicate Detection

Before any LLM call, the pipeline runs a semantic duplicate check. Companies
repost the same role continuously across LinkedIn, Indeed, and their own
careers page. Without a gate, the pipeline wastes API credits on jobs already
in the tracker.

Embedding model: `all-MiniLM-L6-v2` from `sentence-transformers` — runs
entirely on-device, no cloud API call. The FAISS index is persisted to disk
and rebuilt in seconds whenever a new job is accepted. If cosine similarity
between the new posting and any existing job exceeds the threshold, the
pipeline blocks at stage 00 and logs the potential duplicate.

```python
# Stage 00 — semantic duplicate check (simplified)
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/faiss/jobs.index")

embedding = model.encode([new_job_text])
D, I = index.search(np.array(embedding, dtype="float32"), k=1)
similarity = 1 - D[0][0]   # cosine similarity

if similarity > DUPLICATE_THRESHOLD:
    raise DuplicateJobError(f"Similarity {similarity:.2f} — possible duplicate")
```

Running embeddings locally is deliberate: every job description contains
sensitive company and role details. No job text is sent to any external API
at this stage.

---

## Stage 01 — Job Scoring with RAG

The RAG pattern: the master career profile — a structured YAML with all
skills, roles, experience summaries, and competency indicators — is retrieved
and injected alongside the full job description into a structured prompt. Grok
analyzes the pair and returns a structured response.

**RAG scoring output fields**

`match_score` — integer 0–100. Example: `85`
`skill_gaps` — list of strings. Example: `["dbt", "Terraform IaC"]`
`recommendation` — `ACCEPT` or `PASS`
`reasoning` — string summary of fit vs. gaps

The master career profile is the single source of truth. All downstream
stages are grounded in this profile. The LLM cannot invent experience that
isn't in the profile YAML.

The first live run scored 85% on a Collective Health Senior Data Engineer role.
Below the threshold, the job is logged as "passed" and no further API calls
are made.

---

## Two-Tier Model Strategy

Not every stage needs the same reasoning depth. Routing lighter tasks to a
smaller model reduces cost without sacrificing quality where it matters.

`grok-3-mini` — scoring, parsing, classification, company research. Sufficient
reasoning at lower cost; these are structured extraction tasks.

`grok-3` — resume tailoring, cover letter generation. Full model reasoning for
generation work that goes in front of a hiring manager.

The model is a configuration parameter, not a hard-coded string. Every stage
reads its model from a central config — switching the entire pipeline to a
different model is a single environment variable change.

Over-using the full model on lightweight tasks is a common cost trap in LLM
pipelines. The tier split cut per-job cost significantly without degrading
output quality.

---

## OpenAI-Compatible Grok Client

xAI's Grok exposes an OpenAI-compatible REST API. The pipeline uses the
standard `openai` Python library pointed at `https://api.x.ai/v1`. No custom
HTTP client. Every LangChain chain and prompt template built for OpenAI works
with Grok without code changes.

```python
# src/ai/grok_client.py (simplified)
from openai import OpenAI

class GrokClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ["XAI_API_KEY"],
            base_url="https://api.x.ai/v1",
        )
        self.mini_model  = "grok-3-mini"
        self.heavy_model = "grok-3"

    def complete(self, messages, heavy=False):
        model = self.heavy_model if heavy else self.mini_model
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
```

The OpenAI-compatible interface means the entire pipeline could switch to
GPT-4o or any other OpenAI-compatible provider by changing `base_url` and
`api_key`. The model layer is fully decoupled from business logic.

---

## Stages 03–05 — Tailoring and Resume Generation

**Stage 03** extracts structured information from the job posting: required
skills, preferred qualifications, seniority signals, and culture indicators.
Output is a structured YAML file that all downstream stages consume — rather
than re-parsing the raw job text repeatedly.

**Stage 04** generates the resume intermediate — a tailored JSON resume that
selects the most relevant bullet points from the master profile and rewrites
them to match the role's keyword signals. The rewriting is grounded: Grok is
instructed to select and sharpen existing experience, not invent achievements.
The master profile YAML is the hard boundary.

**Stage 05** renders the JSON resume into two formats: an ATS-safe DOCX ready
to attach and submit, and a Markdown preview for quick human review. The DOCX
uses `python-docx` with templated section ordering and consistent
font/spacing — no custom formatting that might confuse ATS parsers.

```
# Stage 05 output layout per job
data/jobs/{uuid}/
├── raw/          # original job posting text
├── score/        # stage 01 scoring YAML
├── tailored/     # stage 03 structured job YAML
├── generated/
│   ├── resume_{uuid}.json      # stage 04 intermediate
│   ├── resume_{uuid}.docx      # stage 05 render
│   ├── resume_{uuid}.md        # stage 05 preview
│   ├── research_{uuid}.md      # stage 06 company notes
│   ├── cover_{uuid}.json       # stage 07 intermediate
│   └── cover_{uuid}.docx       # stage 08 render
└── metadata_{uuid}.yaml        # status and audit trail
```

---

## Stages 06–08 — Company Research and Cover Letter

**Stage 06** runs company research: Grok fetches and summarises publicly
available information — size, funding stage, recent news, engineering culture
signals, tech stack indicators, and leadership context. Saved as a Markdown
summary that feeds directly into stage 07. Goal: give the cover letter
generator enough context to reference specific, real things about the company
rather than producing generic filler.

**Stage 07** generates the cover letter intermediate in JSON format. The
structure separates: opening hook, experience alignment section,
company-specific section (references the stage 06 research), and closing.
Separating these into structured fields makes it easier to regenerate
individual sections without rerunning the full generation.

**Stage 08** classifies the target employer as agency or direct employer, then
renders the cover letter to DOCX with tone adjusted accordingly. Agency letters
are concise and skills-forward. Direct employer letters are narrative and
culture-aligned. The classification is automatic — Grok determines the employer
type from the job posting content.

The agency vs. direct classification is one of the highest-signal design
decisions. Sending a narrative culture-alignment letter to a staffing agency
wastes their time. Sending a bullet-list skills sheet to a direct employer
misses the relationship-building opportunity.

---

## Stage 09 — Quality Gate and Status Tracking

A blocking quality gate before any application is marked as submitted.
Confirms all required output files exist, meet minimum size thresholds (ruling
out truncated or empty outputs), and pass basic content checks. Only after all
checks pass does the pipeline write the application record to
`metadata_{uuid}.yaml` with date, method, status, and score.

If any check fails, the pipeline raises an error and job status stays
in-progress. Nothing is marked as applied. The human must investigate, fix,
and rerun.

```python
# Stage 09 quality checks (simplified)
REQUIRED_FILES = ["resume_{uuid}.docx", "cover_{uuid}.docx", "research_{uuid}.md"]
MIN_SIZES      = {"resume": 8_000, "cover": 3_000, "research": 1_000}  # bytes

for f in REQUIRED_FILES:
    path = job_dir / "generated" / f.format(uuid=uuid)
    if not path.exists():
        raise QualityGateError(f"Missing: {path.name}")
    if path.stat().st_size < MIN_SIZES[f.split("_")[0]]:
        raise QualityGateError(f"Too small ({path.stat().st_size}B): {path.name}")

# All checks passed — write status
metadata["status"]       = "applied"
metadata["applied_date"] = datetime.utcnow().isoformat()
write_yaml(metadata_path, metadata)
```

Marking a job as "applied" when documents aren't ready means you might not
realize the application didn't go through. The quality gate forces review
before status is written — no silent success state.

---

## UUID-Based Data Model

Each job processed by the pipeline gets a UUID at intake. All data,
intermediates, and outputs for that job live under `data/jobs/{uuid}/` — a
self-contained folder that can be inspected, regenerated, or archived
independently of every other job. The UUID also serves as the foreign key for
the FAISS index entry and the status registry.

The status registry is a lightweight YAML file (`data/registry.yaml`) that
maps UUIDs to top-level metadata: company, role title, date processed, score,
and status. This is what the pipeline queries for reporting without scanning
individual job folders.

**Data model layers**

Career profile — `data/profile/career_profile.yaml`. Single source of truth for all experience and skills.
Job registry — `data/registry.yaml`. UUID to metadata index for fast status queries.
FAISS index — `data/faiss/jobs.index`. Semantic duplicate detection across all processed jobs.
Per-job folder — `data/jobs/{uuid}/`. All raw, intermediate, and generated files for one job.
Job metadata — `data/jobs/{uuid}/metadata_{uuid}.yaml`. Full audit trail: scores, status, timestamps, decisions.

---

## StudyBook — The Interview Prep Extension

Once the application pipeline was running, the other half of the problem
became clear: getting the application is only useful if you can win the
interview. StudyBook is the parallel pipeline — generates structured audio
learning scripts for technical topics, converts them to MP3 using GPT-4o TTS,
hosts audio on Cloudflare R2, and generates complete HTML reference pages that
go live on GitHub Pages.

21+ technical topics: AWS services, data engineering patterns, system design,
pipeline design, and project deep-dives. Each page has audio, code examples,
tables, interview Q&A, and a cheat sheet. Claude Code orchestrates quality
review and gap analysis. ChatGPT Project 1 generates audio scripts. ChatGPT
Project 2 generates HTML pages.

```
# StudyBook pipeline (conceptual)
1. Identify topic gap (gap analysis vs. target JD requirements)
2. ChatGPT Project 1 → structured HOST/SEAN audio script (.md)
3. run_mission_audio.ps1 → GPT-4o TTS → chunked MP3s → stitched final MP3
4. Upload final_{slug}.mp3 to Cloudflare R2 bucket
5. ChatGPT Project 2 → full HTML reference page
6. Save to seanlgirgis.github.io/learning/{slug}.html
7. git push → GitHub Pages → live in 30 seconds
```

---

## Engineering Challenges

<a id="sec-1"></a>
### Structured Output Reliability

Language models don't always return the YAML or JSON structure the prompt
asks for. Sometimes well-formed JSON. Sometimes JSON wrapped in markdown code
fences. Sometimes free-form prose with structured data buried inside. Each
variation breaks a naive `json.loads()` call.

The fix was a two-layer approach: prompt templates that include concrete output
format examples, and a regex-based extraction fallback that attempts to recover
structured data from improperly formatted responses before raising an error.

```python
# Structured output extraction with fallback
import re, json

def extract_json(raw: str) -> dict:
    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # Fallback: extract from markdown code fence
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    # Last resort: find first {...} block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No extractable JSON found in model response")
```

---
[Back to TOC](#toc)


<a id="sec-2"></a>
### Windows Encoding in Subprocess Pipelines

The auto-pipeline script runs each stage as a Python subprocess to keep stages
isolated and independently restartable. On Windows, when a job description or
status message contains Unicode — which they do, because the scripts use emoji
for status output — the default encoding for subprocess stdout/stderr is not
UTF-8. This causes encoding errors that silently truncate output or crash the
stage entirely with error messages that don't make the root cause obvious.

The fix was two-part: enforce `PYTHONUTF8=1` in the environment dictionary
passed to every `subprocess.run()` call, and add explicit `encoding="utf-8"`
on every file open.

```python
# Subprocess call with UTF-8 enforcement
import subprocess, os

env = os.environ.copy()
env["PYTHONUTF8"] = "1"

result = subprocess.run(
    ["python", stage_script, "--uuid", job_uuid],
    capture_output=True,
    text=True,
    encoding="utf-8",
    env=env,
)
if result.returncode != 0:
    raise StageError(f"Stage failed:\n{result.stderr}")
```

---

## Lessons Learned

**SQLite from day one, not YAML files.**
Local YAML is fine for an MVP — zero infrastructure, immediately inspectable.
But cross-job queries require scanning every metadata file rather than running
a SQL query. SQLite is still a local file, still zero infra, but you get full
query capability without changing the deployment model.

**Build the Streamlit UI earlier.**
The CLI is great for automation but reviewing outputs before submission is
awkward without a proper interface. A simple Streamlit app showing each job's
score, status, and generated documents side by side would cut review time and
reduce the chance of missing a quality issue.

**Define data contracts between stages formally from the start.**
The YAML structures evolved organically as new stages were added — field names
changed, optional fields became required, new stages expected keys that earlier
stages didn't always produce. Pydantic models or JSON Schema for each stage's
input and output would have caught contract violations at stage boundaries
rather than buried inside downstream parsing errors.

---

## What's Next

**Gmail scanner** — auto-detect new job alert emails, extract the job URL or
posting text, and feed it into the pipeline without manual input.
Status: In progress.

**SQLite registry** — replace file-scan queries with proper SQL across job
history.
Status: Planned.

**Streamlit UI** — review dashboard for generated documents, status tracking,
and rerun controls.
Status: Planned.

**Gap analysis automation** — auto-identify StudyBook topic gaps vs. target
JDs; generate prompt files for the ChatGPT workflow automatically.
Status: Planned.

**LinkedIn integration** — direct job search and posting ingestion via API or
scraping.
Status: Researching.

---

## Interview Q&A

**Walk me through the architecture of this pipeline end to end.**

Ten-stage sequential data pipeline. Input is a raw job posting. Output is a
production-ready application package. Stage zero runs a semantic duplicate
check using FAISS and local embeddings — no API call, no cost, no processing
time wasted on reposted roles. Stage one uses RAG to score the job against my
career profile and returns a match score, skill gap analysis, and accept/reject
recommendation. If accepted, stages three through five extract structured job
data, generate a tailored JSON resume, and render it to DOCX. Stages six
through eight run company research and generate a tailored cover letter with
automatic agency vs. direct employer tone adjustment. Stage nine is a blocking
quality gate that validates all outputs before writing the "applied" status.
The whole pipeline runs from a single orchestrator script.

---

**Why did you choose Grok over OpenAI for the primary LLM?**

Two things: API compatibility and two-tier model economics. Grok exposes an
OpenAI-compatible endpoint — the entire pipeline uses the standard OpenAI
Python library pointed at `x.ai` instead of OpenAI. No custom client, no
LangChain adapter changes, no lock-in. Switching to GPT-4o is one environment
variable change.

On economics: grok-3-mini handles all light tasks at significantly lower cost
per call. grok-3 is reserved for generation work that goes in front of a
hiring manager. That tier split means you get the reasoning quality where you
need it without paying full-model rates for every API call in the pipeline.

---

**How does the FAISS duplicate detection work and why run it locally?**

Stage zero embeds the incoming job description using all-MiniLM-L6-v2,
running entirely on-device. It then searches the FAISS flat index of all
previously processed job embeddings for the nearest neighbor using cosine
similarity. If similarity exceeds the threshold, the pipeline blocks and logs
the potential duplicate.

Running locally was the right call for three reasons: fast (milliseconds, not
seconds), free (no API cost on every intake), and private (job descriptions
contain sensitive company and role details that don't need to leave the
machine for an embedding operation).

---

**How did you handle structured output reliability from the LLM?**

Language models don't always return the exact JSON or YAML the prompt requests.
The solution was a layered extraction approach: prompt templates include
concrete output format examples, which reduces off-format responses
significantly. For cases that still slip through, a regex-based extraction
fallback attempts to recover structured data from the raw response — tries
direct parse, then code fence extraction, then raw JSON block extraction.
Combined, these two layers dropped the structured output failure rate to near
zero in production.

---

**What is the quality gate and why is it a blocking step?**

Stage nine confirms all required output files exist, meet minimum byte-size
thresholds ruling out truncated outputs, and pass basic content checks. Only
after all checks pass does the pipeline write "applied" to the job's metadata.
If any check fails, the job status stays in-progress and the human must
investigate and rerun.

It's blocking by design — same principle as production data pipelines: a
pipeline that completes silently but produces wrong output is more dangerous
than one that fails loudly. Marking a job as applied when the resume or cover
letter isn't ready means you might miss the window to fix it.

---

**What would you build differently if you started over?**

Three things. SQLite from day one instead of YAML files for the job registry —
cross-job queries require scanning files rather than running SQL. The
Streamlit review interface earlier — the CLI is great for automation but
reviewing outputs before submission is awkward without a proper interface.
And formal data contracts between pipeline stages from the start — Pydantic
models or JSON Schema for each stage's input and output — rather than letting
YAML structures evolve organically and cause rounds of refactoring when
downstream stages expected fields that upstream stages didn't consistently
produce.
[Back to TOC](#toc)

