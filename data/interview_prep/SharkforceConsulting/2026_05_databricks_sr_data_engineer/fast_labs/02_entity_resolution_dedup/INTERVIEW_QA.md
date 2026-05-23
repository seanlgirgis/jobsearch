# Interview Q&A

1. **Why deterministic matching first?**
It gives high-confidence, explainable matches and a strong baseline.

2. **When add probabilistic matching?**
When normalized deterministic keys still leave ambiguous cases.

3. **How do you reduce false positives?**
Use stricter thresholds, better features, and review queues for uncertain matches.

4. **How do you reduce false negatives?**
Improve normalization rules and expand candidate generation safely.

5. **How do you pick a survivor record?**
Use a clear business rule, for example latest update timestamp with tie-break.

6. **How do you make this auditable?**
Store match keys, scoring logic, and final decisions in persistent tables.

7. **How does this map to the role?**
It directly supports entity resolution, probabilistic matching, and dedup requirements.

8. **How do you frame your depth honestly?**
As practical data-quality-driven matching approach, not overclaimed specialist platform ownership.
