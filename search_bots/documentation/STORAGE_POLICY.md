# Storage policy (Grok Bot + this PC)

**Sage default:** work **local for speed**, publish to **OneDrive**, delete local job dumps only after the replica is **verified** and **old enough**. DNA and ledgers are not ephemeral.

`/workspace` is **one shared disk for every Bot on the account**, not a private slice per Bot. This project uses **folders**, not a second quota.

## Layout on the Bot (`/workspace`)

```
/workspace/jobsearch/
  dna/                 # persistent; do not auto-delete
  ledger/              # persistent copies
  runs/
    <run_id>/          # one folder per live run (outputs for that run only)
      Apply/
      Wait/
      run.log
```

On this PC (guinea pig): `D:\Workarea\jobsearch\data\search_bots\` maps to the same roles (`cache/` = dna, `ready/` = outputs, `logs/runs/` = run logs).

## Layout on OneDrive (`V:\Bots_Jobs`)

```
V:\Bots_Jobs\indeed\
  Apply\
  Wait\
  ledger.csv
  LAST_RUN.log
  BOT_STATUS.txt
  LAST_ERROR.txt
```

This is what **you** open. The Bot cannot rely on `data/` on your laptop.

## Per-run folders

Each `-Live` run gets `runs/<run_id>/`. Isolation: one failed run does not mix files with the next. After a successful OneDrive flush, that run folder is a **candidate for delete**, not DNA.

## Copy then wait then delete

1. Write the run **only** under `/workspace/jobsearch/` (or `data/search_bots/` on this PC).
2. Flush to OneDrive. Record size + hash of each copied file.
3. **Do not delete** on the same run as the copy.
4. **Retention (default: 7 days, minimum 24 hours)** after a copy that still **re-reads** on OneDrive with the **same size/hash**.
5. Also require `human_processed=Y` on the ledger row **or** 7 days, whichever you prefer for safety. Default here: **7 days after verified copy**. 24 hours is the floor if you tighten later.
6. If OneDrive is missing or hash mismatches: **keep local**, re-queue, no delete.

**Never auto-delete**

- DNA / `jk` index  
- Ledger  
- `handoff_queue.json`  
- Last 5 run logs  

## Why not 24 hours only

A write to `V:` can succeed in the OneDrive **client** and fail in the **cloud**. Seven days covers sync lag, a closed lid, and you not having marked `Y` yet. 24 hours is acceptable **minimum age**, not the only gate.

## Security

- No `.env`, no API keys, no BofA/client names in `/workspace` dumps or OneDrive.  
- All Bots on the account can read `/workspace` — do not put secrets there.  
- Keys stay in the Bot secret store / `.env` on this PC, never in job folders.
