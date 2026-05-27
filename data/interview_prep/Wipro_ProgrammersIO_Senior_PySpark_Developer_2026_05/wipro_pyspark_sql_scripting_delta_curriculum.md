# Wipro Senior PySpark Developer — Delta Study Curriculum

Purpose:
Build a focused recovery/study map from the interview gaps. The interview
tested mostly:

- PySpark internals and syntax
- SQL window/query coding
- Unix shell scripting
- Spark performance tuning
- Spark skew/shuffle handling

This curriculum is not a broad Databricks course. It is a practical
interview-prep and hands-on drill plan for Senior PySpark Developer
screening questions.

---

## 0. How to Use This Curriculum

Use this as a 3-layer map:

1. **Delta Rescue**
   - Fix the exact topics that came up and were weak.

2. **Core Fluency**
   - Practice the common coding patterns until they can be written quickly.

3. **Completing the Topic**
   - Add adjacent concepts that make the answers stronger and prevent
     future surprise questions.

Recommended time boxes:

| Time Available | What to Do |
|---|---|
| 2 hours | Study Section 1 only: exact missed interview deltas |
| 1 day | Sections 1 + 2 + 3 |
| 3 days | Sections 1–5 plus labs |
| 1 week | Full curriculum including side topics and repeated mock drills |

---

# 1. Delta Rescue Map — Exact Interview Gaps

## 1.1 Spark Architecture

Know cold:

- driver
- executor
- cluster manager
- lazy transformations
- actions
- jobs
- stages
- tasks
- partitions
- shuffle

Interview answer:

Spark code begins at the driver. Transformations build a lazy execution
plan. An action triggers execution. Spark converts the plan into jobs,
stages, and tasks. Executors run tasks against partitions of the data.
Shuffle is usually the expensive step because data moves across executors.

Hands-on drill:

```python
df = spark.read.parquet(path)
df2 = df.filter("amount > 0").groupBy("department").count()
df2.explain(True)
df2.show()
```

Explain:
- Which lines are transformations?
- Which line is the action?
- Where might shuffle happen?

---

## 1.2 RDD vs DataFrame

Expected answer:

RDD is lower-level and gives more control over distributed objects.
DataFrame is higher-level, schema-aware, SQL-like, and optimized by
Catalyst. In most production PySpark data engineering work, DataFrames
are preferred because they are easier to read, integrate with SQL, and
benefit from Spark optimizations.

Punchline:

Use DataFrames for most structured ETL work; use RDDs only when you need
lower-level control.

---

## 1.3 groupByKey vs reduceByKey

This is RDD-level Spark.

Expected answer:

`groupByKey` brings all values for a key together across the network.
That can be expensive because it shuffles all values before aggregation.

`reduceByKey` performs local combining before the shuffle, so less data
moves across the network. For aggregations like sum or count,
`reduceByKey` is usually better.

Example:

```python
rdd = sc.parallelize([
    ("A", 1), ("A", 2), ("B", 5), ("B", 10)
])

result = rdd.reduceByKey(lambda a, b: a + b)
```

Punchline:

For aggregations, `reduceByKey` is usually better because it combines
locally before shuffle.

---

## 1.4 Repartition vs Coalesce

Expected answer:

`repartition()` increases or changes partitions and usually causes a
full shuffle. Use it when you need to redistribute data by count or key.

`coalesce()` usually reduces the number of partitions with less shuffle.
Use it after filtering or before writing output when partitions became
too small.

Example:

```python
df_rebalanced = df.repartition(200, "department_id")
df_smaller = df.coalesce(20)
```

Punchline:

Use `repartition` when you need a new distribution; use `coalesce` when
reducing partitions with less shuffle.

---

## 1.5 Adaptive Query Execution, AQE

Expected answer:

Adaptive Query Execution lets Spark adjust the physical plan at runtime
using actual data statistics. It can coalesce shuffle partitions, change
join strategy, and help with skewed joins after Spark sees real data
sizes.

Important features:

- coalesce shuffle partitions
- convert sort-merge join to broadcast join when possible
- optimize skew joins
- runtime plan adjustment

Punchline:

AQE adjusts the Spark execution plan at runtime based on actual data,
not only estimates.

---

## 1.6 Persistence / Storage Levels

Expected answer:

Persistence controls where Spark keeps reused data: memory, disk, or
both. Use it when the same DataFrame/RDD will be used multiple times.
Release it with `unpersist()` when done.

Examples:

```python
from pyspark import StorageLevel

df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK)
df.unpersist()
```

Common levels:

- MEMORY_ONLY
- MEMORY_AND_DISK
- DISK_ONLY
- MEMORY_ONLY_SER
- MEMORY_AND_DISK_SER

Punchline:

Persist when data will be reused; unpersist when done.

---

## 1.7 Predicate Pushdown

Expected answer:

Predicate pushdown means Spark pushes filters closer to the data source
so less data is read. With Parquet, ORC, and some databases, Spark can
skip irrelevant data based on filters.

Example:

```python
df = (
    spark.read.parquet(path)
         .filter("business_date = '2026-05-01'")
)
```

Punchline:

Predicate pushdown reduces I/O by applying filters as close to the
source as possible.

---

## 1.8 Salting for Skew

Expected answer:

Salting is used when data is skewed and one key is too large. A random
or calculated salt bucket is added to spread a hot key across multiple
partitions. For joins, the large side is salted and the small side is
expanded across the same salt buckets.

Example:

```python
from pyspark.sql import functions as F

salt_buckets = 10

large_salted = large_df.withColumn(
    "salt",
    (F.rand() * salt_buckets).cast("int")
)

small_expanded = (
    small_df
    .withColumn("salt_array", F.sequence(F.lit(0), F.lit(salt_buckets - 1)))
    .withColumn("salt", F.explode("salt_array"))
    .drop("salt_array")
)

joined = large_salted.join(
    small_expanded,
    on=["join_key", "salt"],
    how="inner"
)
```

Punchline:

Salting spreads one hot key across multiple buckets so one executor does
not get stuck processing one massive partition.

---

## 1.9 Broadcast Join

Expected answer:

Use broadcast join when one DataFrame is small enough to send to all
executors. This helps avoid shuffling the larger dataset.

Example:

```python
from pyspark.sql.functions import broadcast

joined = large_df.join(
    broadcast(small_lookup_df),
    on="lookup_id",
    how="left"
)
```

Punchline:

Broadcast the small side so the large side does not need a heavy shuffle.

---

## 1.10 PySpark Join Syntax

Same column name:

```python
joined = left_df.join(
    right_df,
    on="customer_id",
    how="inner"
)
```

Different column names:

```python
joined = left_df.join(
    right_df,
    left_df.customer_id == right_df.id,
    "left"
)
```

Common risks:

- wrong join type
- null keys
- duplicate keys
- row explosion
- ambiguous column names
- shuffle
- skew

Punchline:

Always validate join key, join type, row counts, nulls, duplicates, and
possible row explosion.

---

## 1.11 Top 2 Salaries per Department — SQL

```sql
WITH ranked AS (
    SELECT
        department_id,
        employee_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC
        ) AS rn
    FROM employees
)
SELECT
    department_id,
    employee_id,
    salary
FROM ranked
WHERE rn <= 2;
```

If ties matter:

```sql
WITH ranked AS (
    SELECT
        department_id,
        employee_id,
        salary,
        RANK() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC
        ) AS rnk
    FROM employees
)
SELECT *
FROM ranked
WHERE rnk <= 2;
```

Punchline:

Use `ROW_NUMBER` or `RANK` over `PARTITION BY department ORDER BY salary
DESC`, then filter rank <= 2.

---

## 1.12 Top 2 Salaries per Department — PySpark

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

w = Window.partitionBy("department_id").orderBy(F.col("salary").desc())

top2 = (
    employees
    .withColumn("rn", F.row_number().over(w))
    .filter(F.col("rn") <= 2)
    .drop("rn")
)
```

If ties matter, use `rank()` or `dense_rank()`.

---

## 1.13 Print Lines 15–20 from a File — Unix

Preferred:

```bash
sed -n '15,20p' file.txt
```

Alternative:

```bash
awk 'NR>=15 && NR<=20' file.txt
```

Punchline:

Use `sed -n '15,20p' file.txt` or `awk 'NR>=15 && NR<=20' file.txt`.

---

## 1.14 Flatten an Array in PySpark

```python
from pyspark.sql import functions as F

flat = df.select(
    "id",
    F.explode("items").alias("item")
)
```

If preserving rows with empty/null arrays:

```python
flat = df.select(
    "id",
    F.explode_outer("items").alias("item")
)
```

Punchline:

Use `explode` to turn array elements into rows.

---

## 1.15 Common Elements Between Two Arrays

```python
from pyspark.sql import functions as F

df2 = df.withColumn(
    "common_items",
    F.array_intersect(F.col("array1"), F.col("array2"))
)
```

Punchline:

Use `array_intersect` for common elements between arrays.

---

# 2. Core PySpark Coding Fluency

Practice these until they are automatic.

## 2.1 Read CSV with Explicit Schema

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("employee_id", StringType(), True),
    StructField("department_id", StringType(), True),
    StructField("salary", IntegerType(), True),
])

df = (
    spark.read
         .option("header", "true")
         .schema(schema)
         .csv(input_path)
)
```

## 2.2 Read / Write Parquet

```python
df = spark.read.parquet(input_path)

(
    df.write
      .mode("overwrite")
      .partitionBy("business_date")
      .parquet(output_path)
)
```

## 2.3 Select, Filter, WithColumn

```python
from pyspark.sql import functions as F

clean = (
    df.select("employee_id", "department_id", "salary")
      .filter(F.col("salary").isNotNull())
      .withColumn("salary_band",
                  F.when(F.col("salary") >= 100000, "HIGH")
                   .otherwise("NORMAL"))
)
```

## 2.4 Group and Aggregate

```python
agg = (
    df.groupBy("department_id")
      .agg(
          F.count("*").alias("row_count"),
          F.avg("salary").alias("avg_salary"),
          F.max("salary").alias("max_salary")
      )
)
```

## 2.5 Duplicate Detection

```python
dupes = (
    df.groupBy("employee_id")
      .count()
      .filter(F.col("count") > 1)
)
```

## 2.6 Latest Record per Key

```python
from pyspark.sql.window import Window
from pyspark.sql import functions as F

w = Window.partitionBy("employee_id").orderBy(F.col("updated_at").desc())

latest = (
    df.withColumn("rn", F.row_number().over(w))
      .filter(F.col("rn") == 1)
      .drop("rn")
)
```

## 2.7 Left Join with Validation

```python
joined = fact_df.join(
    dim_df,
    on="department_id",
    how="left"
)

print("fact count:", fact_df.count())
print("joined count:", joined.count())
```

## 2.8 Explain Plan

```python
joined.explain(True)
```

---

# 3. SQL Fluency Track

## 3.1 Must-Know SQL Patterns

- inner join
- left join
- group by
- having
- CTE
- row_number
- rank
- dense_rank
- case
- null handling
- duplicate detection
- top N per group
- anti-join
- exists / not exists

## 3.2 Duplicate Keys

```sql
SELECT employee_id, COUNT(*) AS cnt
FROM employees
GROUP BY employee_id
HAVING COUNT(*) > 1;
```

## 3.3 Null Counts

```sql
SELECT
    SUM(CASE WHEN salary IS NULL THEN 1 ELSE 0 END) AS null_salary_count,
    COUNT(*) AS total_count
FROM employees;
```

## 3.4 Left Join and Missing Matches

```sql
SELECT e.*
FROM employees e
LEFT JOIN departments d
    ON e.department_id = d.department_id
WHERE d.department_id IS NULL;
```

## 3.5 Aggregation with HAVING

```sql
SELECT department_id, COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 10;
```

## 3.6 Top N per Group

```sql
WITH ranked AS (
    SELECT
        department_id,
        employee_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC
        ) AS rn
    FROM employees
)
SELECT *
FROM ranked
WHERE rn <= 2;
```

## 3.7 Running Total

```sql
SELECT
    department_id,
    employee_id,
    salary,
    SUM(salary) OVER (
        PARTITION BY department_id
        ORDER BY employee_id
    ) AS running_salary
FROM employees;
```

---

# 4. Unix / Shell Scripting Fluency

## 4.1 File and Log Commands

```bash
ls -lh
find . -name "*.csv"
wc -l file.csv
head file.csv
tail -100 app.log
grep "ERROR" app.log
grep -i "failed" app.log
```

## 4.2 Print Lines 15–20

```bash
sed -n '15,20p' file.txt
awk 'NR>=15 && NR<=20' file.txt
```

## 4.3 Count Error Types

```bash
grep "ERROR" app.log | awk '{print $5}' | sort | uniq -c | sort -nr
```

## 4.4 Check File Exists

```bash
if [ -f "$INPUT_FILE" ]; then
    echo "File exists"
else
    echo "Missing file"
    exit 1
fi
```

## 4.5 Loop Files

```bash
for f in *.csv; do
    echo "Processing $f"
done
```

## 4.6 Exit Code

```bash
python job.py

if [ $? -ne 0 ]; then
    echo "Job failed"
    exit 1
fi
```

## 4.7 Safe Shell Positioning

Interview answer:

Shell is the workflow glue. It checks files, sets environment variables,
calls jobs, checks exit codes, scans logs, archives files, and supports
reruns. Heavy data transformation belongs in Python, SQL, or PySpark.

---

# 5. Spark Performance and Skew Checklist

## 5.1 Performance Checklist

When a Spark job is slow, check:

- input row counts
- schema
- file format
- small files
- partition count
- join keys
- shuffle-heavy operations
- skewed keys
- repeated actions
- caching/persistence
- broadcast opportunities
- execution plan
- driver/executor logs
- spill / memory warnings
- output partitioning

## 5.2 Skew Checklist

When one task runs much longer than others:

- check key distribution
- check null-heavy keys
- check top key frequencies
- check join cardinality
- use broadcast join if one side is small
- use salting for hot keys
- filter bad/null keys if business allows
- repartition by better keys
- use AQE skew join handling when available

## 5.3 Top Key Frequency

```python
(
    df.groupBy("join_key")
      .count()
      .orderBy(F.col("count").desc())
      .show(20)
)
```

---

# 6. Side Topics to Complete the Topic

These were not all directly tested, but they complete the SQL / PySpark /
scripting interview lane.

## 6.1 DataFrame vs SQL API

Know that PySpark supports both:

```python
df.createOrReplaceTempView("employees")

spark.sql("""
    SELECT department_id, COUNT(*) AS cnt
    FROM employees
    GROUP BY department_id
""")
```

Answer:

DataFrame API and Spark SQL are both common. DataFrames are programmatic
and composable; SQL is expressive and useful for analysts and complex
queries.

## 6.2 Narrow vs Wide Transformations

Narrow:

- select
- filter
- withColumn
- map-like operations

Wide:

- groupBy
- join
- distinct
- repartition

Punchline:

Wide transformations usually require shuffle.

## 6.3 Cache vs Persist

`cache()` is shorthand for default persistence.
`persist()` lets you choose a storage level.

## 6.4 Bucketing

Bucketing organizes data by a hash of a key. It can help joins if both
tables are bucketed on the same key and Spark can use the layout.

Do not overclaim deep use. Know conceptually.

## 6.5 Partition Pruning vs Predicate Pushdown

Partition pruning:
Spark skips folders/partitions like `date=2026-05-01`.

Predicate pushdown:
Spark pushes filters into a data source/file reader to read less data.

## 6.6 Small Files Problem

Too many tiny files cause overhead when Spark schedules tasks and reads
metadata. Compact or coalesce/repartition before writing.

## 6.7 Explain Plan Basics

Look for:

- BroadcastHashJoin
- SortMergeJoin
- Exchange
- Filter
- Project
- HashAggregate

`Exchange` usually indicates shuffle.

## 6.8 Anti-Join

```python
missing = left_df.join(right_df, on="id", how="left_anti")
```

Used to find records in one dataset that do not match another.

## 6.9 Semi-Join

```python
matched_left_only = left_df.join(right_df, on="id", how="left_semi")
```

Used to keep left rows that have a match, without bringing right columns.

---

# 7. Hands-On Lab Plan

Create a small PySpark practice script with these DataFrames:

- employees(employee_id, department_id, salary, updated_at)
- departments(department_id, department_name)
- metrics(server_id, business_date, cpu, memory)
- lookup(server_id, application_name)

## Lab 1 — Employee SQL / PySpark

Tasks:

1. Top 2 salaries per department in SQL.
2. Top 2 salaries per department in PySpark.
3. Find duplicate employee IDs.
4. Keep latest employee record.
5. Find employees with missing department mapping.

## Lab 2 — Spark Performance Mini-Lab

Tasks:

1. Perform a join.
2. Explain the plan.
3. Try broadcast join.
4. Repartition by key.
5. Coalesce before output.
6. Identify where shuffle appears.

## Lab 3 — Shell Mini-Lab

Tasks:

1. Print lines 15–20 from a file.
2. Count errors from a log.
3. Check that input file exists.
4. Loop over CSV files.
5. Write non-zero exit if required file is missing.

---

# 8. Mock Interview Drill Set

Practice these out loud.

## Spark Internals

1. Explain Spark architecture.
2. What is lazy evaluation?
3. Transformation vs action?
4. What causes shuffle?
5. How do you reduce shuffle?
6. What is AQE?
7. What is predicate pushdown?
8. Cache vs persist?
9. Repartition vs coalesce?
10. How do you handle skew?

## PySpark Coding

1. Join two DataFrames.
2. Broadcast small lookup table.
3. Find duplicates.
4. Keep latest row by key.
5. Top 2 salaries per department.
6. Explode an array.
7. Find common elements between arrays.
8. Read CSV with schema.
9. Write partitioned Parquet.
10. Explain a query plan.

## SQL

1. Top N per group.
2. Find duplicates.
3. Left join missing matches.
4. Null counts.
5. CASE expressions.
6. CTEs.
7. Row number vs rank.
8. HAVING vs WHERE.

## Shell

1. Print lines 15–20.
2. Count error messages.
3. Check file exists.
4. Tail logs.
5. Use awk to print a column.
6. Use sort and uniq to count values.

---

# 9. Minimum Recovery Punchlines

Memorize these.

```text
AQE adjusts Spark’s plan at runtime using actual data statistics.
```

```text
Predicate pushdown reduces I/O by applying filters near the source.
```

```text
Salting spreads a hot key across buckets to reduce skew.
```

```text
repartition redistributes data and usually shuffles; coalesce reduces
partitions with less shuffle.
```

```text
reduceByKey is usually better than groupByKey for aggregation because
it combines locally before shuffle.
```

```text
Use ROW_NUMBER over PARTITION BY department ORDER BY salary DESC for
top N per department.
```

```text
Use sed -n '15,20p' file.txt to print lines 15 through 20.
```

```text
Use explode to flatten arrays and array_intersect for common array
elements.
```

---

# 10. Recommended Study Order

## First 2 Hours

1. Salting
2. Repartition vs coalesce
3. groupByKey vs reduceByKey
4. AQE
5. Predicate pushdown
6. Persistence levels
7. Top 2 SQL / PySpark
8. sed lines 15–20
9. explode / array_intersect
10. join syntax

## Next 1 Day

1. Write all PySpark snippets by hand.
2. Write all SQL snippets by hand.
3. Run shell mini-lab.
4. Practice mock interview questions out loud.

## 3-Day Upgrade

1. Build the hands-on DataFrame lab.
2. Run explain plans.
3. Practice skew and salting with fake data.
4. Build a one-page cheat sheet.
5. Do two mock interviews.

---

# 11. Final Positioning

The interview exposed that the next improvement area is not story or
general production experience. It is sharper exact syntax and Spark
interview mechanics.

Primary lane:

- SQL coding
- PySpark coding
- Spark performance
- Unix command fluency

Secondary lane:

- scheduling tools
- cloud architecture
- broad data engineering storytelling

Focus on the primary lane first.
