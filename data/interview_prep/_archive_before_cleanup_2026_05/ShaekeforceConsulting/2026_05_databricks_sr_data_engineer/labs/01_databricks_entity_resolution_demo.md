```python
# Databricks notebook source
from pyspark.sql import functions as F

# Sample records with duplicate-ish names
data = [
    (1, "John A. Smith", "john.smith@example.com"),
    (2, "john smith", "john.smith+spam@example.com"),
    (3, "J. Smith", "jsmith@example.com"),
    (4, "Mary Jones", "mary.jones@example.com"),
    (5, "Mary  Jones ", "mary.jones@example.com"),
    (6, "M. Jones", "mjones@example.com")
]

df = spark.createDataFrame(data, ["id", "full_name", "email"])
display(df)
```

```python
# Normalize names and emails
normalized = (
    df
    .withColumn("name_norm", F.lower(F.trim(F.regexp_replace("full_name", r"[^a-zA-Z0-9 ]", ""))))
    .withColumn("name_norm", F.regexp_replace("name_norm", r"\\s+", " "))
    .withColumn("email_norm", F.lower(F.trim(F.regexp_replace("email", r"\\+[^@]*@", "@"))))
)

display(normalized)
```

```python
# Build a simple match_key
scored = (
    normalized
    .withColumn("name_key", F.regexp_replace("name_norm", " ", ""))
    .withColumn("match_key", F.concat_ws("|", F.col("name_key"), F.col("email_norm")))
)

display(scored)
```

```python
# Drop duplicates by match_key
# Keep earliest id as survivor
windowed = scored.orderBy("id")
deduped = windowed.dropDuplicates(["match_key"])

display(deduped.orderBy("id"))
```

```python
# Save as Delta table (Databricks Free Edition-compatible)
# Writes to managed table in default metastore/catalog
(
    deduped
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("default.entity_resolution_demo")
)
```

```sql
-- Query with SQL
SELECT id, full_name, email, match_key
FROM default.entity_resolution_demo
ORDER BY id;
```

```sql
-- Quick quality check
SELECT match_key, COUNT(*) AS cnt
FROM default.entity_resolution_demo
GROUP BY match_key
HAVING COUNT(*) > 1;
```
