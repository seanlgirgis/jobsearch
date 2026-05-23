# PySpark Coding Drills

## 1) Read CSV
```python
df = spark.read.option("header", True).csv("/data/input.csv")
```

## 2) Read Parquet
```python
df = spark.read.parquet("/data/input.parquet")
```

## 3) Select and Filter
```python
out = df.select("id", "amount").filter("amount > 100")
```

## 4) groupBy Aggregate
```python
from pyspark.sql import functions as F
agg = df.groupBy("region").agg(F.sum("amount").alias("total"))
```

## 5) Inner Join
```python
joined = left.join(right, "customer_id", "inner")
```

## 6) Left Join
```python
joined = left.join(right, "customer_id", "left")
```

## 7) Handle Nulls
```python
clean = df.fillna({"city": "UNKNOWN", "amount": 0})
```

## 8) Remove Duplicates
```python
dedup = df.dropDuplicates(["business_key"])
```

## 9) Find Duplicate Keys
```python
from pyspark.sql import functions as F
dups = (df.groupBy("business_key")
          .count()
          .filter("count > 1"))
```

## 10) Latest Record Per Key
```python
from pyspark.sql import Window, functions as F
w = Window.partitionBy("id").orderBy(F.col("updated_at").desc())
out = df.withColumn("rn", F.row_number().over(w)).filter("rn = 1").drop("rn")
```

## 11) Rank Rows
```python
from pyspark.sql import Window, functions as F
w = Window.partitionBy("team").orderBy(F.col("score").desc())
r = df.withColumn("rnk", F.rank().over(w))
```

## 12) Add Derived Column
```python
from pyspark.sql import functions as F
out = df.withColumn("amount_usd", F.col("amount_local") * F.lit(1.08))
```

## 13) Write Partitioned Parquet
```python
out.write.mode("overwrite").partitionBy("biz_date").parquet("/out/fact")
```

## 14) Explain Plan
```python
out.explain(True)
```

## 15) Troubleshoot Slow Job (pattern)
```python
# Checklist: filter early, select fewer cols, check skew keys,
# use broadcast for small dims, avoid unnecessary repartition.
```
