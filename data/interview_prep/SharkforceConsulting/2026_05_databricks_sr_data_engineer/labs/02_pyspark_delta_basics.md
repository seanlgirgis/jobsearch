```python
# Databricks notebook source
from pyspark.sql import functions as F

rows = [
    (1, "alpha", 10.0),
    (2, "beta", 20.0),
    (3, "gamma", 30.0)
]

df = spark.createDataFrame(rows, ["id", "name", "value"])
display(df)
```

```python
# Write Delta table
(
    df
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("default.delta_basics_demo")
)
```

```python
# Read table as DataFrame
delta_df = spark.table("default.delta_basics_demo")
display(delta_df)
```

```sql
-- Query table with SQL
SELECT id, name, value
FROM default.delta_basics_demo
ORDER BY id;
```

```python
# Append example
new_rows = spark.createDataFrame([(4, "delta", 40.0)], ["id", "name", "value"])
(
    new_rows
    .write
    .format("delta")
    .mode("append")
    .saveAsTable("default.delta_basics_demo")
)
```

```sql
-- Verify append
SELECT COUNT(*) AS total_rows
FROM default.delta_basics_demo;
```

```text
overwrite: replaces existing table data with the new DataFrame.
append: adds new rows to existing table data.
```
