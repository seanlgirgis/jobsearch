```python
# Databricks Free Edition friendly
from pyspark.sql import functions as F

# 1) sample records
rows = [
    (1, "  Alice Smith ", "AUSTIN", "TX", 120.0),
    (2, "bob jones", "Austin", "tx", 90.5),
    (3, "Carla  Green", "Dallas", "TX", 300.0)
]

# 2) Spark DataFrame
raw_df = spark.createDataFrame(rows, ["customer_id", "full_name", "city", "state", "amount"])
display(raw_df)

# 3) simple transformation + normalized columns
clean_df = (
    raw_df
    .withColumn("full_name_norm", F.lower(F.regexp_replace(F.trim(F.col("full_name")), "\\s+", " ")))
    .withColumn("city_norm", F.lower(F.trim(F.col("city"))))
    .withColumn("state_norm", F.upper(F.trim(F.col("state"))))
)

display(clean_df)

# 4) write Delta table
(
    clean_df
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("default.lab01_dataframe_delta")
)

# 5) SQL query
result_df = spark.sql("""
SELECT customer_id, full_name_norm, city_norm, state_norm, amount
FROM default.lab01_dataframe_delta
ORDER BY customer_id
""")

display(result_df)
```
