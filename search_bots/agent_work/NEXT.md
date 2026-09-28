# Next work (Sean picks)

1. **Review** `V:\Bots_Jobs\indeed\Wait` and `\Apply`; set ledger `human_processed=Y`. Kill or keep phrases in `search_bots/terms.json`.
2. **Scheduler change first:** implement/test 24 jittered non-overlapping fires/day, `fromage=2`, and dynamic daily batches. Formula: `ceil(remaining_due_phrases / remaining_run_slots_today)`; 54 phrases starts with six 3-phrase runs then eighteen 2-phrase runs. Use SQLite history to keep light searches together and heavy searches alone within time/page caps.
3. **Deployment:** then host that scheduler in Task Scheduler or a local container. Keep the persistent Chrome profile, SQLite/DNA, logs and OneDrive handoff mounted; no automated login/CAPTCHA/Cloudflare action.
3. **SMTP** in `.env` if email on block is wanted (`seanlgirgis@gmail.com`).
4. Stay off Grok Bot for Indeed scraping.
5. LinkedIn live later.
6. Merge LTM into yaml; demote `source_of_truth.json`.

Do not 10k-grind. Do not click Cloudflare from code.
