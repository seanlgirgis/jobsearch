# Karat Practice Plan

## Assessment Plan
- Round 1: Clarify problem, constraints, expected output.
- Round 2: Write simple correct solution first.
- Round 3: Improve readability/performance.
- Round 4: Validate with edge cases aloud.

## Likely Question Patterns
- Data cleanup and deduplication
- Grouped metrics and ranking
- Latest record per key
- Join and anti-join checks
- Log/file parsing mini tasks
- Debugging broken transformation

## 10 Practice Prompts
1. Python: deduplicate list of dicts by id using latest timestamp.
2. Python: parse CSV lines and return invalid rows.
3. PySpark: latest transaction per customer.
4. PySpark: detect duplicate business keys and counts.
5. PySpark: join fact/dim and compute daily totals.
6. SQL: top 3 customers per month by spend.
7. SQL: anti-join source vs target missing ids.
8. SQL: null-rate report by date.
9. SQL: running total by account over time.
10. Unix + Python: count error lines and print top 5 messages.

## Explain Thinking Out Loud
- State assumptions early.
- Narrate data shape and edge cases.
- Mention tradeoffs briefly.
- Say what you would test before production.

## What Not To Do During Karat
- Do not go silent for long stretches.
- Do not over-engineer before baseline solution.
- Do not bluff on unknown tools.
- Do not skip sample input/output checks.
