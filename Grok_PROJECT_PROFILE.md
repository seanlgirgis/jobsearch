# Grok Project Profile — jobsearch

**Path:** `D:\Workarea\jobsearch`  
**Type:** hybrid (pipeline + career vault)  
**Profile version:** 2026-09-06

## One-Line Summary

Personal job-market pipeline — listings, tailored resume/cover, applied-job tracking, interview prep, gigs.

## Does this project

- Ingest and score jobs; tailor resume/cover; track applied jobs and gigs
- Hold master career data (`data/master/`) and interview prep
- Run API automation and ChatGPT manual flows from this folder

## Does not

- Store LTIM/BofA work-learning digests (**ALOK**)
- Host Coursera/DataCamp courses (**learning**)
- Replace interview algorithm practice (**python_dsa**)
- Store command nuggets (**local_memory**)

## Route signals — keywords

jobsearch, job search, resume, cover letter, applied job, gig, Upwork, Indeed, LinkedIn intake, master_career_data

## Route signals — paths

`D:\Workarea\jobsearch`, `data/applied_jobs/`, `data/jobs/`, `data/master/`, `JobSearch_V2/`

## Default work mode

bite_sized

## Read first (child agents)

1. `D:\Workarea\Grok_DIRECTOR\Grok_SEAN.md`
2. `D:\Workarea\Grok_DIRECTOR\Grok_SEAN_NOW.md`
3. `BOOTSTRAP.md`
4. This file
5. Task-specific paths only

## Hard rules

- One job or one pipeline step per task unless Sean asks otherwise
- Activate `.\env_setter.ps1` before Python
- Do not invent employment history; use `data/master/`
- Sean manages Git unless delegated
