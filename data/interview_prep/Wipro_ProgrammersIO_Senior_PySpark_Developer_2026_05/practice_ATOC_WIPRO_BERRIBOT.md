<a id="toc"></a>
## Table of Contents

- [01 — Story and Role Fit](#sec-01-story-and-role-fit)
- >[Q01 Tell me about yourself and why you are a good fit for this Senior PySpark Developer role?](#q01)
- [02 — PySpark](#sec-02-pyspark)
- >[Q02 Explain your PySpark experience and how you used it in production-style data pipelines.](#q02)
- >[Q03 How does a PySpark job execute in the background?](#q03)
- >[Q04 What is the difference between a transformation and an action in PySpark?](#q04)
- >[Q05 What is shuffle in Spark, and why is it expensive?](#q05)
- >[Q06 How would you troubleshoot a slow PySpark job?](#q06)
- >[Q07 How do you handle duplicates in PySpark?](#q07)
- >[Q08 How do you join two DataFrames in PySpark, and what can go wrong?](#q08)
- >[Q09 How do you handle nulls in PySpark?](#q09)
- >[Q10 How do you use window functions in PySpark?](#q10)
- >[Q11 — How do you read and write files in PySpark?](#q11)
---
<a id="sec-01-story-and-role-fit"></a>
# 01 — Story and Role Fit


<a id="q01"></a>
## Q01 Tell me about yourself and why you are a good fit for this Senior PySpark Developer role?
[Back to TOC](#toc)

I am a senior data engineer with strong experience in PySpark,
SQL, Unix/Linux, ETL workflows, and production troubleshooting.

At Citi, I worked on telemetry and time-series data pipelines
used for reporting, forecasting, validation, and capacity
planning. As data volume grew, we moved heavier processing from
single-machine Python/Pandas patterns toward PySpark and
Hadoop-style distributed processing.

That background maps well to this role because it requires
PySpark script analysis, SQL, Unix shell scripting, ETL
understanding, scheduling concepts, and the ability to
troubleshoot production data workflows in a financial-services
environment.

punch line:
My fit is PySpark, SQL, Unix, ETL, and production troubleshooting
from a financial-services data pipeline background.

<a id="sec-02-pyspark"></a>
# 02 — PySpark

<a id="q02"></a>
## Q02 Explain your PySpark experience and how you used it in production-style data pipelines.
[Back to TOC](#toc)

At Citi, my PySpark experience came from scaling telemetry and
time-series data pipelines that supported reporting, validation,
capacity planning, and forecasting.

Originally, a lot of the processing was done with Python and Pandas.
As the data volume grew, single-machine processing became a bottleneck,
so we moved heavier transformation and forecasting workloads toward
PySpark and Hadoop-style distributed processing.

The work involved DataFrame-style transformations: selecting and
filtering data, joining telemetry with reference data, grouping and
aggregating metrics by host, application, service, and time bucket,
and preparing cleaned datasets for reporting and forecasting.

From a production-support point of view, I focused on row counts,
schema consistency, missing or late data, duplicate records, null
spikes, failed transformations, and downstream report mismatches.

For performance, I paid attention to partitioning, shuffle-heavy
operations like joins and groupBy, avoiding unnecessary actions, and
using partitioned outputs so downstream reads were more efficient.

So my PySpark experience is strongest around practical ETL processing,
large operational datasets, validation, troubleshooting, and preparing
data for reporting and forecasting.

Punchline:
My PySpark experience is practical production ETL: large telemetry
datasets, DataFrame transformations, SQL-style aggregation, validation,
troubleshooting, and scaling heavier workloads beyond single-machine
Python/Pandas.

<a id="q03"></a>
## Q03 How does a PySpark job execute in the background?
[Back to TOC](#toc)

PySpark code starts on the driver. Transformations such as select,
filter, join, and groupBy are lazy, so they build an execution plan
instead of running immediately.

When an action runs, such as count, show, collect, or write, Spark
triggers a job. Spark breaks the job into stages, and each stage is
broken into tasks. Executors then run those tasks across partitions
of the data in parallel.

The expensive point is usually shuffle. Shuffle happens during wide
operations like joins, groupBy, distinct, and repartition, where data
has to move across executors.

### Punchline

Transformations build the plan, actions trigger execution, executors
process partitions in parallel, and shuffle is usually the expensive
part to watch.

<a id="q04"></a>
## Q04 What is the difference between a transformation and an action in PySpark?
[Back to TOC](#toc)

Transformations are operations that define a new DataFrame but do not
execute immediately. Examples include `select`, `filter`, `withColumn`,
`join`, and `groupBy`.

Spark treats transformations as lazy. It builds an execution plan on the
driver, but it does not process the data until an action is called.

Actions trigger execution. Examples include `show`, `count`, `collect`,
and `write`. When an action runs, Spark turns the plan into jobs, stages,
and tasks. Executors then process the tasks across partitions of the data.

### Punchline

Transformations build the plan; actions trigger the plan to run.

<a id="q05"></a>
## Q05 What is shuffle in Spark, and why is it expensive?
[Back to TOC](#toc)

Shuffle is the movement of data across executors so Spark can bring
matching keys together.

It usually happens during wide operations like `join`, `groupBy`,
`distinct`, and `repartition`. For example, if I group telemetry by
`server_id`, Spark may need to move records with the same `server_id`
from different partitions onto the same executor-side task.

Shuffle is expensive because it involves network transfer, disk spill,
serialization, and extra coordination between stages. It is often where
slow Spark jobs spend most of their time.

To reduce shuffle, I look at partitioning, join keys, data skew,
broadcasting small lookup tables, and avoiding unnecessary repartition
or repeated wide operations.

### Punchline

Shuffle is expensive data movement across executors so matching keys
can meet for joins, grouping, distinct, or repartition.


<a id="q06"></a>
## Q06 How would you troubleshoot a slow PySpark job?
[Back to TOC](#toc)

To troubleshoot a slow PySpark job, I would start with the basics:
confirm the input row counts, schema, filters, and expected output.
I want to know whether the job is slow because of data volume, bad
logic, data quality, or execution behavior.

Then I would inspect the execution plan using `.explain()` and review
driver and executor logs for memory warnings, failed tasks, retries,
or spill symptoms.

The main performance areas I would check are shuffle, joins, skew,
partitions, and file layout. Wide operations like `join`, `groupBy`,
`distinct`, and `repartition` can create expensive shuffle. If a join
is slow, I would check whether one side is small enough for a broadcast
join, so Spark can avoid shuffling the larger dataset.

I would also check for data skew, where one key or one partition has
much more data than the others. That can make one task run much longer
than the rest. Then I would review partition sizing, unnecessary actions
like repeated `count()`, and the small files problem, especially when
reading or writing many tiny files on HDFS or S3.

My goal is to identify whether the bottleneck is data movement, skew,
bad partitioning, repeated actions, file layout, or resource pressure,
then fix the smallest thing that gives the biggest improvement.

### Punchline

I troubleshoot slow PySpark jobs by checking row counts, schema,
execution plan, logs, shuffle, joins, skew, partitions, repeated actions,
and small files.


<a id="q07"></a>
## Q07 How do you handle duplicates in PySpark?
[Back to TOC](#toc)

To handle duplicates in PySpark, I first identify whether they are
full-row duplicates or business-key duplicates.

For full-row duplicates, I can use `distinct()` or `dropDuplicates()`.
For simple key-based deduplication, I can use:

```python
df.dropDuplicates(["user_id"])
```
But I would use that only when it does not matter which record survives.

If the business rule says to keep a specific record, such as the latest
record per user or server, I use a window function. I partition by the
business key, order by the timestamp descending, assign row_number(),
and keep only row number 1.

That is safer for production pipelines because it makes the deduplication
rule explicit and repeatable.



Use this code snippet in the file too:

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

w = Window.partitionBy("user_id").orderBy(F.col("updated_at").desc())

latest_df = (
    df.withColumn("rn", F.row_number().over(w))
      .filter(F.col("rn") == 1)
      .drop("rn")
)

```

### Punchline

For duplicates, first define the business key; use dropDuplicates
for simple cases, and use a window function when the surviving row matters.

<a id="q08"></a>
## Q08 How do you join two DataFrames in PySpark, and what can go wrong?
[Back to TOC](#toc)

To join two DataFrames in PySpark, I use the `.join()` method with
the right DataFrame, the join condition, and the join type. The default
is usually an inner join, but in production pipelines I often need a
left join when I want to preserve all records from the main dataset.

The first thing I check is the business meaning of the join key. I want
to know whether the key is unique, whether null keys are expected, and
whether duplicate keys are valid or a data-quality issue.

From a performance perspective, the biggest risk is shuffle. Joining
large datasets can require Spark to move data across executors so
matching keys can meet. If one side of the join is small enough, I may
use a broadcast join so Spark sends the small lookup DataFrame to the
executors instead of shuffling the large dataset.

From a data-integrity perspective, joins can go wrong because of null
keys, duplicate keys, schema mismatches, ambiguous column names, wrong
join type, or row explosion. For example, if both sides have duplicate
keys, the join can multiply rows unexpectedly.

To protect the pipeline, I validate row counts before and after the join,
check null and duplicate key counts, rename ambiguous columns, confirm
the join type, and compare the output against expected business logic.

### Punchline

For joins, I validate the key, join type, row counts, nulls, duplicates,
schema, shuffle risk, and possible row explosion.


<a id="q09"></a>
## Q09 How do you handle nulls in PySpark?
[Back to TOC](#toc)

To handle nulls in PySpark, I first look at the business meaning of the
field. I do not blindly drop rows, because nulls may represent missing
source data, late data, optional fields, or a real data-quality problem.

For analysis, I use `isNull()` and `isNotNull()` to count and isolate
missing records. If the row is not useful without that field, I may use
`dropna()`. But if the row should be preserved, I use `fillna()` or a
business default, such as zero for a metric or `"UNKNOWN"` for a category.

The important part is that the rule must be explicit. Dropping nulls
without understanding the data can change row counts, skew metrics, or
break downstream reporting and forecasting.

### Punchline

I handle nulls by first understanding the business rule, then using
`isNull`, `isNotNull`, `dropna`, or `fillna` without blindly dropping data.

<a id="q10"></a>
## Q10 How do you use window functions in PySpark?
[Back to TOC](#toc)

In PySpark, I use window functions when I need calculations across
related rows without collapsing the DataFrame like a normal `groupBy`.

First, I define a window using `Window.partitionBy()` for the business
key and `orderBy()` for the sequence. For example, I may partition by
`server_id` or `customer_id` and order by an update timestamp.

A common use case is keeping the latest record per key. I use
`row_number()` over the window, order by timestamp descending, and keep
only row number 1.

Window functions are also useful for rank, running totals, rolling
metrics, and time-series comparisons. The key point is that they let me
calculate within a group while preserving row-level detail.
```python

from pyspark.sql import functions as F
from pyspark.sql.window import Window

w = Window.partitionBy("server_id").orderBy(F.col("event_time").desc())

latest_df = (
    df.withColumn("rn", F.row_number().over(w))
      .filter(F.col("rn") == 1)
      .drop("rn")
)
```

### Punchline

Window functions let me calculate within a business-key group, such as
latest record, rank, or rolling metric, without losing row-level detail.side the window specification, you can extract complex, time-series insights while maintaining the original granularity of your DataFrame.


<a id="q11"></a>
## Q11 — How do you read and write files in PySpark?
[Back to TOC](#toc)

read.csv
read.parquet
header
schema
inferSchema
explicit schema
write.parquet
mode
partitionBy
overwrite vs append