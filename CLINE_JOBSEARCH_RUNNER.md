# Cline jobsearch runner

Operate one job or one pipeline step for Sean Girgis: intake, scoring, tailored
resumes/covers, application tracking, gigs, and application interview preparation.

## Read only what the step needs

At session start follow `AGENTS.md`: `BOOTSTRAP.md`, `PROFILE.md`,
`PROJECT_MEMORY.md`, then `CURRENT_STATE.md`. Next read this file and
[`docs/PIPELINE_OPERATOR.md`](docs/PIPELINE_OPERATOR.md), including its current
limitations. For one job, read only the named intake,
`data/master/candidate_profile_runtime.json`, and that job's returned outputs.
Do not scan the repository, enumerate unrelated jobs, load large career dumps,
or consult historical runbooks. Explore narrowly only when a command fails; use
the linked architecture reference and the failing module, then report the cause.

## Execute the requested step

Run from `D:\Workarea\jobsearch`. Activate before Python and check source freshness:

```powershell
. .\env_setter.ps1
python scripts\build_runtime_profile.py --check
if ($LASTEXITCODE -ne 0) { throw 'Runtime profile needs review' }
.\job-runner.ps1 .\intake\new_job.md -Mode gate
```

Replace `new_job.md` with the exact requested intake. Read the returned folder's
`score/local_gate.json`: stop on nonempty `eligibility_blocks`, `read_errors`, or
a duplicate/blocked decision. The cutover runner enforces these gates. Follow the
runbook's explicit override procedure only with an authorized reason.

For triage, run the same command with `-Mode triage`; report fit and stop. Generate
only when Sean's request already authorizes it, using `-Mode generate` and `-Cover`
if requested. A model recommendation is advisory. Require a nonblank reason for
either override; never invent one merely to get past a failed command. Do not
chain all steps blindly. Generate records explicit acceptance/override separately
from the recommendation. There is no accept/reject-only command.

Use `-AnalysisProfile <configured-name>` for Tier 1 and
`-GenerationProfile <configured-name>` for Tier 2. Defaults are `economy` and
`quality`; profile names such as `economy_deepseek` and `quality_claude` are valid
when configured in `config/model_profiles.local.json`. Both selected profiles need
structured-schema support and no fallbacks; the generation profile must set
`allow_artifacts: true`. Never change profile configuration or make a paid call
unless Sean asked for that run.

## Check truth and report the result

Follow the runtime profile's `public_safety` and evidence tiers. Current employer
is LTIMindtree; omit its client publicly. CAPTAIN is research, never production,
and its codename stays out of documents. Preserve unknown dates/title and
foundational skill limits. Do not invent history, metrics, depth, or production
status. Target capacity, performance, observability, Python automation, reporting,
and practical AI; do not recast Sean as a generic DS/ML specialist.

Inspect intermediate JSON, quality report, and every DOCX page before submission.
Report returned state; exact folder/resume/cover paths (or absent); gate result;
model recommendation and Sean's separate decision; profile/configured model;
each cache key and HIT/MISS when available; attempted-call bound; actual dollar
cost **unavailable** unless observed in provider records; and one next command.
Cline's own model usage is separate from pipeline API usage. Never label configured
models as proven provenance for an old cache hit: use the cache's saved model_used.

Never mark applied unless Sean explicitly requests it or confirms submission.
Use the runbook's apply-only command with real method/date/notes; it makes no
provider or renderer calls. Never erase
intake, cache claims, or historical records as routine cleanup. Sean manages Git.
