# JobSearch Modernization — Charter

## Goal
Reduce AI cost (xAI usage) by 60–80% while maintaining or improving quality of:
- resume tailoring
- job scoring
- application outputs

## Principles
- AI is used surgically, not everywhere
- One LLM call should do as much work as possible
- Expensive steps only happen for high-value jobs
- Everything is cached if reusable

## Non-Negotiables
- Source of truth lives in filesystem (not chat)
- No duplicate AI calls for same data
- Each step must justify its cost

## Success Criteria
- Max 1 LLM call for most jobs
- Max 2 LLM calls for top-tier jobs
- Zero LLM calls for rejected jobs