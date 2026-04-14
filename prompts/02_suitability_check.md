# Prompt: Suitability Check
# Usage: paste this prompt into a Gemini Gem or Claude.ai Project that has source_of_truth.json attached
# Output: honest fit score + accept/reject recommendation
# No API key needed — uses your Gemini/Claude.ai subscription

---

You have my complete career profile attached as source_of_truth.json.

Review the job posting JSON below and score my fit honestly.

SCORING RULES:
- 50 = weak match (apply only if desperate)
- 65 = average match (proceed with realistic expectations)
- 75 = solid match (good candidate, real shot)
- 85+ = strong match (apply with confidence)
- Each missing must-have skill: -8 to -12 points
- Each strong direct match: +5 to +8 points
- Never inflate — a score of 85+ means I could interview today without embarrassment

Output EXACTLY this format:

## Fit Score: X / 100
## Recommendation: Strong Proceed | Proceed | Hold | Skip

## Strongest Matches
- concrete match from my profile vs this job (be specific — company, year, skill)

## Gaps & Risks
- missing skill or experience gap | Mitigation: one sentence on how to frame it

## ATS Keywords I Already Have
- keyword present in both my profile and the job

## ATS Keywords I Am Missing
- important job keyword not in my profile

## Positioning Advice
2-4 sentences on how to frame the application given my specific background.

## Decision
ACCEPT or REJECT — one word, then one sentence reason.

---
JOB POSTING JSON:

[PASTE OUTPUT FROM 01_normalize_intake.md HERE]
