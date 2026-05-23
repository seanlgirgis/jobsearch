```python
# Databricks notebook-ready code
from pyspark.sql import functions as F

# 1) Sample data with quality issues
rows = [
    (1, "A100", 25.0, "ACTIVE"),
    (2, "A101", None, "ACTIVE"),
    (3, "A101", 40.0, "ACTIVE"),
    (4, None, -5.0, "ACTIVE"),
    (5, "A103", 15.0, "UNKNOWN")
]

df = spark.createDataFrame(rows, ["id","account_id","amount","status"])
display(df)

# 2) Schema check
expected_cols = ["id","account_id","amount","status"]
schema_ok = set(df.columns) == set(expected_cols)

# 3) Null check
null_account = df.filter(F.col("account_id").isNull()).count()
null_amount = df.filter(F.col("amount").isNull()).count()

# 4) Duplicate check
dup_account = (
    df.groupBy("account_id")
      .agg(F.count("*").alias("cnt"))
      .filter((F.col("account_id").isNotNull()) & (F.col("cnt") > 1))
      .count()
)

# 5) Row count check
row_count = df.count()
row_count_ok = row_count >= 5

# 6) Business rule check
invalid_amount = df.filter(F.col("amount") < 0).count()
invalid_status = df.filter(~F.col("status").isin("ACTIVE","INACTIVE")).count()

# 7) Build data_quality_report DataFrame
report_rows = [
    ("schema_check", "PASS" if schema_ok else "FAIL", f"expected={expected_cols}"),
    ("null_check_account_id", "PASS" if null_account == 0 else "FAIL", f"null_count={null_account}"),
    ("null_check_amount", "PASS" if null_amount == 0 else "FAIL", f"null_count={null_amount}"),
    ("duplicate_check_account_id", "PASS" if dup_account == 0 else "FAIL", f"dup_groups={dup_account}"),
    ("row_count_check", "PASS" if row_count_ok else "FAIL", f"row_count={row_count}"),
    ("business_rule_amount_non_negative", "PASS" if invalid_amount == 0 else "FAIL", f"invalid_count={invalid_amount}"),
    ("business_rule_status_allowed", "PASS" if invalid_status == 0 else "FAIL", f"invalid_count={invalid_status}")
]

data_quality_report = spark.createDataFrame(report_rows, ["check_name","status","details"])
display(data_quality_report)
```
