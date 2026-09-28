# Search strategy for Sean

Updated 2026-09-14. The search catalog is `search_bots/terms.json`: six categories,
54 phrases. These are search hypotheses to assess from actual results. Sean chooses
which jobs to pursue; an Apply filename is an advisory label, not an application.

## What to search

| Category | Purpose | Example phrases |
|---|---|---|
| capacity_performance | Established infrastructure capacity and performance experience | IT capacity planning; application performance engineer; cloud capacity optimization |
| observability_apm | Monitoring and APM work, including vendor vocabulary | Dynatrace consultant; AppDynamics engineer; Splunk observability; BMC Helix capacity |
| practical_ai | Applying AI to existing business and engineering workflows | AI enablement consultant; AI adoption specialist; AI workflow automation; RAG consultant |
| python_reporting_automation | Python, SQL and reporting integration rather than a generic data-platform career | Python reporting automation; infrastructure reporting analyst; Power BI migration consultant |
| technical_consulting | Technical delivery and customer advisory work using established strengths | performance engineering consultant; Dynatrace professional services; observability solutions engineer |
| part_time_remote | Smaller engagements and alternative working arrangements | part time Python automation; fractional AI consultant; contract capacity planning; forward deployed AI engineer contract |

Use short alternative phrases. Requiring Python, SQL, APM, AI and remote together can
miss roles whose titles use only one or two of those terms. The current Indeed adapter
already supplies `location=remote`; the posting still determines actual geographic
eligibility and hours. Dallas/Plano hybrid coverage would be a separate location search.

The categories are discovery routes. A job found through a part-time phrase may be
full-time. The same job may appear in several routes; DNA keeps the first discovery.
Drop **folders** are Apply / Wait (decision), not the search-pack name. The pack
is the ledger `search_pack` column.

Generic data engineer, data scientist, ML engineer, prompt engineer and forward-deployed
engineer are not the main positioning. The catalog includes `forward deployed engineer`
and `forward deployed AI engineer` as adjacent practical-AI searches for general/full-time
openings, plus explicit contract and part-time variants in `part_time_remote`. Read
production tooling, model-training depth, travel, quota, on-call demands, and work
schedules in the job rather than treating a title as proof of fit.

## Why these phrases

Employer vocabulary supports the new categories. These pages were reviewed for role
language, not as a shortlist of jobs Sean should apply for:

- [Brunswick AI Enablement Consultant](https://job-boards.greenhouse.io/brunswickgroup/jobs/8636851002)
  describes prompting guidance, workflow redesign and adoption of AI tools. This is
  closer to Sean's current direction than model training or research. The listing is
  in London; it is an example of the job family, not a geographic recommendation.
- [Dynatrace Technology Consultant](https://apply.careers.dynatrace.com/job/apply/1391662100/)
  includes monitoring, performance diagnosis, dashboards and customer guidance.
- [Dynatrace Solutions Engineer](https://careers.dynatrace.com/jobs/1292475300/)
  illustrates a technical role inside a sales organization. Its responsibilities include
  demos and proofs of concept, which is why a blanket exclusion of the word sales
  could hide potentially relevant technical work. Travel and presales fit need review.

## Avoidances

`config/search_bots_exclusions.json` keeps the existing DataAnnotation company exclusion
and expands title fragments for annotators, AI tutors, response reviewers, search raters,
and ads/internet assessors. Fragments match titles, not every mention in a description.
They are editable; check exclusions when a potentially useful role is missing.

[Outlier's expert community](https://app.outlier.ai/opportunities/4705643005) describes
reviewing and rating AI responses. [TELUS Digital's AI Community listings](https://jobs.telusdigital.com/search/jobs/in?cfm5=AI+Community)
include ads assessors and raters. These illustrate additional sources of annotation-style
work. No new blanket company bans were added: employers and staffing firms can also
advertise relevant engineering or consulting positions. Add an exact company only after
its actual results show it is consistently unwanted.

Daily reposting alone is not proof of spam. Existing DNA skips a known Indeed job key
or identical normalized capture text. A relisted job with a new key and altered capture
can still be new to the cache; fuzzy repost detection is not implemented. Do not assume
the cache catches every duplicate advertisement.

## Salary and working hours

- Full-time salary ranges with a known maximum below $140,000 USD are excluded before
  evaluation. $120k-$160k remains eligible; $120k-$135k is excluded. This preserves the
  existing maximum-of-range policy.
- A known hourly rate is annualized at 2,080 hours for comparison: $60/hour gives
  $124,800; $70/hour gives $145,600. This is not a guarantee of contract income or benefits.
- Explicit part-time/fractional/flexible-hours postings have no floor. An explicit
  full-time field takes priority over flexible-hours wording. Contract/freelance by
  itself does not prove reduced hours, nor does the search query establish hours.
- Unknown pay, unclear pay units and identified non-USD amounts remain for review.
  The parser is deliberately limited; unusual or conflicting pay snippets may need review.
- Short company names and pay fields are retained. The capture parser recognizes labeled
  fields and legacy captures, so exclusions use the job title rather than the Indeed URL.

## Week-first and refresh operation

Configuration now selects seven days when the DNA cache is empty and one day when it
already has records. For deployment after POC tests, explicitly pass `-Fromage 7` for
the catch-up; the existing test cache already counts as a previous run. Keep that cache.
The approved replacement policy is 24 jittered, non-overlapping scheduled fires/day
with `-Fromage 2`. Dynamic batches cover every enabled phrase daily: with 54 phrases,
six runs carry three phrases and eighteen carry two. The 48-hour overlap plus DNA
avoids a missed-run black hole. This is an implementation target; the current code
still uses one phrase and `fromage=1`. Resume a deliberate failed catch-up with
`-Fromage 7`.

This is a query/filter POC, not completed unattended deployment. The local live adapter
still reads the first results page per phrase and uses a positive total `-Limit`.
It does not currently mean unlimited pagination, and no scheduler is installed here.
The deployed bot needs to host the existing SQLite recurrence safely. It should start,
run one phrase, persist the Chrome profile/SQLite/DNA/logs, and exit quietly; it must
not turn an hourly fire into a long multi-query browser grind.

Assess the next results by which phrases produce work Sean would actually pursue.
Use the ledger's category and query fields; `human_processed=Y` records review, not
approval or rejection. It cannot by itself measure an approval rate.
