# Search bots

**Strategy:** `documentation/SEARCH_STRATEGY.md`  
**How to run:** `documentation/HOW_IT_WORKS.md` · **today:** `documentation/LIVE.md`  
**Agents:** `agent_work/HANDOFF.md`

## Run Indeed

```powershell
.\search_bots\run_indeed.ps1 -Live -Limit 5
```

**Terms (one file):** `search_bots/terms.json` — 6 categories, 54 phrases. New category = new key.

**Drops:** `V:\Bots_Jobs\indeed\Apply\` and `\Wait\` (decision folders, not search-pack names)  
**Ledger:** `V:\Bots_Jobs\indeed\ledger.csv` (`human_processed=N` until you set Y)

Apply ≥80 · Wait 60–79 · Reject not written. First empty-cache lookback 7 days, then 1 day. FT posted max under $140k skipped. Annotation/rater titles skipped.
