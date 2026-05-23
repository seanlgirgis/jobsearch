```python
# Architecture pseudocode only (no AWS credentials required tonight)

# 1) Raw landing in S3
s3_raw_path = "s3://example-raw-bucket/orders/"

# 2) Databricks reads raw data
raw_df = spark.read.format("json").load(s3_raw_path)

# 3) Transform to Silver quality layer
silver_df = (
    raw_df
      .dropDuplicates(["order_id"])
      .filter("order_id is not null")
)

# 4) Write Silver Delta
silver_df.write.format("delta").mode("overwrite").saveAsTable("default.orders_silver")

# 5) Quality checks (pseudo)
# validate_schema(silver_df)
# validate_nulls(silver_df)
# reconcile_counts(raw_df, silver_df)

# 6) Build Gold for analytics/ML features
gold_df = spark.sql("""
SELECT customer_id, count(*) as order_count, sum(order_total) as total_spend
FROM default.orders_silver
GROUP BY customer_id
""")

gold_df.write.format("delta").mode("overwrite").saveAsTable("default.orders_gold")

# Security/governance concepts:
# - IAM role grants S3 access
# - Unity Catalog storage credential references role ARN
# - External location maps governed S3 path
```
