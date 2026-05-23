# ETL Troubleshooting

Use this flow: detect -> isolate -> fix -> validate -> prevent.

## 1) Missing input file
- Check upstream completion marker and path typo.
- Verify scheduler passed correct date/partition.
- Citi-style example: Upstream SFTP delay; run with latest available date,
  then controlled backfill after file arrives.

## 2) Schema mismatch
- Compare expected schema vs actual columns/types.
- Add explicit cast/map and quarantine bad rows.
- Citi-style: Vendor added column mid-week; introduced schema contract check
  before transform stage.

## 3) Duplicate records
- Group by business key to quantify.
- Apply dedup rule (latest timestamp, highest sequence).
- Citi-style: Duplicate CDC replay fixed with idempotent merge keys.

## 4) Null spike
- Track null ratio by day/source.
- Identify upstream extraction issue vs transformation bug.
- Citi-style: Nulls traced to source parser change; added null-threshold alert.

## 5) Late arriving data
- Use watermark/cutoff policy.
- Separate late-backfill path from normal SLA path.
- Citi-style: End-of-day table updated with T+1 late correction batch.

## 6) Failed Spark job
- Capture first meaningful error.
- Reproduce on sample partition.
- Patch and rerun targeted partition.

## 7) Slow Spark job
- Check skewed keys, shuffle-heavy joins, repartition misuse.
- Filter early, reduce columns, broadcast small dimensions.

## 8) SQL count mismatch
- Compare row counts by partition/date.
- Validate join cardinality and duplicate explosion.

## 9) Downstream report mismatch
- Reconcile metric logic, timezone cutoffs, and late data handling.
- Confirm report query uses same business rule version.

## 10) Restart/Rerun decision
- Rerun when logic fixed and idempotent.
- Patch-forward when partial writes require controlled correction.
- Always log incident cause and prevention action.
