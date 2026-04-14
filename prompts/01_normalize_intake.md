# Prompt: Normalize Job Intake
# Usage: paste this prompt + the raw job posting text into any AI (Gemini, ChatGPT, Claude.ai)
# Output: clean structured JSON ready for the pipeline
# No API key needed — use your existing subscription

---

You are a job posting parser. Convert the raw job posting below into clean structured JSON.

RULES:
- Extract only what is explicitly stated — no guessing, no invention
- If a field is not mentioned, use null
- Compensation: extract min/max as integers (no $ or commas), null if not stated
- Work type: "Remote" | "Hybrid" | "On-site" | null
- Employment type: "Full Time" | "Part Time" | "Contract" | "Contract-to-Hire" | null
- For skills: separate must-have (explicitly required) from nice-to-have (preferred/bonus)
- Write job_summary yourself in 2-3 sentences: role, company context, core focus

Output ONLY this JSON — no explanation, no markdown fences:

{
  "company": "exact company name",
  "title": "exact job title from posting",
  "location": "City, State or Remote",
  "work_type": "Remote | Hybrid | On-site | null",
  "employment_type": "Full Time | Part Time | Contract | null",
  "source": "LinkedIn | Indeed | Company Website | Referral | null",
  "compensation": {
    "min": null,
    "max": null,
    "currency": "USD",
    "type": "salary | hourly | null",
    "notes": "any bonus/equity notes or null"
  },
  "company_website": "https://... or null",
  "job_summary": "2-3 sentence summary of role, company, and core focus",
  "responsibilities": [
    "clean rephrased bullet"
  ],
  "requirements": {
    "must_have": [
      "explicitly required skill or credential"
    ],
    "nice_to_have": [
      "preferred or bonus skill"
    ]
  },
  "ats_keywords": [
    "important keyword or phrase from posting"
  ],
  "about_company": "1-2 sentences on what the company does, stage, industry",
  "red_flags": [
    "anything unusual: unclear comp, contract bait-and-switch, vague role, etc. — or empty array"
  ]
}

---
RAW JOB POSTING:

[PASTE JOB TEXT HERE]
