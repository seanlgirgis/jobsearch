```python
# Databricks notebook-ready code
from pyspark.sql import functions as F
from pyspark.sql import Window

# 1) Sample records with duplicate-ish entities
rows = [
    (101, "John A. Smith", "Austin", "TX", "john.smith@email.com", "2026-05-01"),
    (102, "john smith", "austin", "tx", "john.smith+promo@email.com", "2026-05-02"),
    (103, "J Smith", "Austin", "TX", "jsmith@email.com", "2026-05-03"),
    (201, "Mary Jones", "Dallas", "TX", "mary.j@email.com", "2026-05-01"),
    (202, "Mary  Jones", "dallas", "tx", "mary.j@email.com", "2026-05-04")
]

df = spark.createDataFrame(rows, ["record_id","full_name","city","state","email","updated_at"])

# 2) Normalize name
n1 = df.withColumn("name_norm", F.lower(F.regexp_replace(F.trim(F.col("full_name")), "[^a-zA-Z0-9 ]", "")))
n1 = n1.withColumn("name_norm", F.regexp_replace(F.col("name_norm"), "\\s+", " "))

# 3) Normalize city/state
n2 = (
    n1
    .withColumn("city_norm", F.lower(F.trim(F.col("city"))))
    .withColumn("state_norm", F.upper(F.trim(F.col("state"))))
    .withColumn("email_norm", F.lower(F.regexp_replace(F.col("email"), "\\+[^@]*@", "@")))
)

# 4) Create deterministic match_key
n3 = n2.withColumn("match_key", F.concat_ws("|", F.col("name_norm"), F.col("city_norm"), F.col("state_norm")))

# 5) Identify duplicate groups
dup_groups = (
    n3.groupBy("match_key")
      .agg(F.count("*").alias("group_count"))
      .filter(F.col("group_count") > 1)
)

display(dup_groups)

# 6) Choose surviving record (latest updated_at)
w = Window.partitionBy("match_key").orderBy(F.col("updated_at").desc(), F.col("record_id").asc())
resolved = (
    n3.withColumn("rn", F.row_number().over(w))
      .withColumn("is_survivor", F.when(F.col("rn") == 1, F.lit(1)).otherwise(F.lit(0)))
)

survivors = resolved.filter(F.col("is_survivor") == 1).drop("rn")

# 7) Write matched output as Delta table
(
    survivors.write.format("delta").mode("overwrite").saveAsTable("default.lab02_entity_resolved")
)

display(survivors)
```
