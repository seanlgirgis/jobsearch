<a id="toc"></a>
# Wipro / Programmers.io Senior PySpark Developer Practice ATOC

Purpose:
Prepare for the Wipro / Programmers.io Senior PySpark Developer interview
by practicing speakable, safe, role-targeted answers.

ATOC means:
- Answer
- Tune
- One-liner / punchline
- Confidence

---

## Table of Contents

- [Wipro / Programmers.io Senior PySpark Developer Practice ATOC](#wipro--programmersio-senior-pyspark-developer-practice-atoc)
  - [Table of Contents](#table-of-contents)
- [00 — Human Interview Mode](#00--human-interview-mode)
  - [Human strategy for tomorrow](#human-strategy-for-tomorrow)
  - [30-second opening](#30-second-opening)
  - [If I get stuck](#if-i-get-stuck)
- [01 — Story and Role Fit](#01--story-and-role-fit)
  - [Q01 Tell me about yourself and why you are a good fit for this Senior PySpark Developer role?](#q01-tell-me-about-yourself-and-why-you-are-a-good-fit-for-this-senior-pyspark-developer-role)
  - [Q01 — Tell me about yourself and why you are a good fit for this Senior PySpark Developer role?](#q01--tell-me-about-yourself-and-why-you-are-a-good-fit-for-this-senior-pyspark-developer-role)
- [02 — PySpark](#02--pyspark)
  - [Q02 Explain your PySpark experience and how you used it in production-style data pipelines.](#q02-explain-your-pyspark-experience-and-how-you-used-it-in-production-style-data-pipelines)
  - [Q03 How does a PySpark job execute in the background?](#q03-how-does-a-pyspark-job-execute-in-the-background)
  - [Q04 What is the difference between a transformation and an action in PySpark?](#q04-what-is-the-difference-between-a-transformation-and-an-action-in-pyspark)
  - [Q05 What is shuffle in Spark, and why is it expensive?](#q05-what-is-shuffle-in-spark-and-why-is-it-expensive)
  - [Q06 How would you troubleshoot a slow PySpark job?](#q06-how-would-you-troubleshoot-a-slow-pyspark-job)
  - [Q07 How do you handle duplicates in PySpark?](#q07-how-do-you-handle-duplicates-in-pyspark)
  - [Q08 How do you join two DataFrames in PySpark, and what can go wrong?](#q08-how-do-you-join-two-dataframes-in-pyspark-and-what-can-go-wrong)
  - [Q09 How do you handle nulls in PySpark?](#q09-how-do-you-handle-nulls-in-pyspark)
  - [Q10 How do you use window functions in PySpark?](#q10-how-do-you-use-window-functions-in-pyspark)
  - [Q11 How do you read and write files in PySpark?](#q11-how-do-you-read-and-write-files-in-pyspark)
- [03 — Tomorrow Review Path](#03--tomorrow-review-path)
  - [Best review order](#best-review-order)
  - [20-minute rapid review](#20-minute-rapid-review)
  - [60-minute review](#60-minute-review)
  - [Final confidence script](#final-confidence-script)
  - [H01 — Tell me about yourself and how your background fits this role?](#h01--tell-me-about-yourself-and-how-your-background-fits-this-role)
  - [H02 — Walk me through a production PySpark or ETL issue you troubleshot.](#h02--walk-me-through-a-production-pyspark-or-etl-issue-you-troubleshot)
  - [H03 — How strong are you in PySpark, and where are you still growing?](#h03--how-strong-are-you-in-pyspark-and-where-are-you-still-growing)
  - [H04 — What would you do if a PySpark job failed during a production run?](#h04--what-would-you-do-if-a-pyspark-job-failed-during-a-production-run)
  - [H05 — How have you used Unix shell scripting in data or ETL workflows?](#h05--how-have-you-used-unix-shell-scripting-in-data-or-etl-workflows)
  - [H06 — What is your experience with scheduling tools like Airflow, Autosys, or Control-M?](#h06--what-is-your-experience-with-scheduling-tools-like-airflow-autosys-or-control-m)
  - [H07 — How strong are you in SQL, and how have you used it with data pipelines?](#h07--how-strong-are-you-in-sql-and-how-have-you-used-it-with-data-pipelines)
  - [H08 — How would you troubleshoot an ETL pipeline from source to final output?](#h08--how-would-you-troubleshoot-an-etl-pipeline-from-source-to-final-output)
  - [H09 — What questions would you ask the interviewer?](#h09--what-questions-would-you-ask-the-interviewer)
  - [H10 — Before we finish, is there anything else you would like us to know?](#h10--before-we-finish-is-there-anything-else-you-would-like-us-to-know)
  - [H11 — What Unix commands do you commonly use when troubleshooting data jobs?](#h11--what-unix-commands-do-you-commonly-use-when-troubleshooting-data-jobs)
  
  
  

---

<a id="sec-00-human-interview-mode"></a>
# 00 — Human Interview Mode

[Back to TOC](#toc)

## Human strategy for tomorrow

This is no longer Berribot-only. Treat it like a conversation.

Main goal:
Show that I can explain PySpark, SQL, Unix, ETL, and production
troubleshooting clearly from real enterprise experience.

Answer pattern:
1. Define the concept.
2. Give a simple example.
3. Explain the production risk.
4. Say how I validate or troubleshoot it.

Core positioning:
I am strongest in PySpark-style data processing, SQL, Unix/Linux,
ETL workflows, production troubleshooting, validation, and
financial-services data pipelines.

Safe scheduling wording:
I have production workflow support experience, dependency tracking,
runbooks, validation checkpoints, and Airflow-style orchestration
awareness. Autosys and Control-M are awareness/ramp-up areas for me,
not my deepest hands-on administration tools.

Do not overclaim:
- Deep Spark cluster administration
- Kubernetes
- Kafka
- Databricks production ownership
- Autosys / Control-M administration

## 30-second opening

I am a senior data engineer with strong experience in PySpark, SQL,
Unix/Linux, ETL workflows, and production troubleshooting.

At Citi, I worked on telemetry and time-series data pipelines used for
reporting, forecasting, validation, and capacity planning. As the data
volume grew, we moved heavier processing from single-machine Python
and Pandas patterns toward PySpark and Hadoop-style distributed
processing.

This role fits me because it combines PySpark script analysis, SQL,
Unix shell scripting, ETL understanding, scheduling concepts, and
production data troubleshooting in a financial-services environment.

## If I get stuck

Use this recovery line:

That is a good question. The way I would approach it in production is
to first validate the input, row counts, schema, and business rule, then
look at the execution behavior, logs, and downstream impact.

---

<a id="sec-01-story-and-role-fit"></a>
# 01 — Story and Role Fit

<a id="q01"></a>
## Q01 Tell me about yourself and why you are a good fit for this Senior PySpark Developer role?

[Back to TOC](#toc)

## Q01 — Tell me about yourself and why you are a good fit for this Senior PySpark Developer role?

1. Professional identity
   I am a senior data engineer with strong experience in PySpark, SQL,
   Unix/Linux, ETL workflows, and production troubleshooting.

2. Citi data pipeline background
   At Citi, I worked on telemetry and time-series data pipelines used for
   reporting, forecasting, validation, and capacity planning.

3. Scaling from Pandas to PySpark
   As data volume grew, we moved heavier processing from single-machine
   Python/Pandas patterns toward PySpark and Hadoop-style distributed
   processing.

4. Role fit
   That background maps well to this role because it requires PySpark script
   analysis, SQL, Unix shell scripting, ETL understanding, scheduling
   concepts, and the ability to troubleshoot production data workflows.

5. Financial-services fit
   The financial-services environment also fits my background because I have
   worked with production discipline: validation, row counts, schema checks,
   downstream impact, and reliable reporting.

```python
# Simple example of the kind of PySpark pipeline pattern I am comfortable with
from pyspark.sql import functions as F

result_df = (
    telemetry_df
    .filter(F.col("event_time").isNotNull())
    .join(reference_df, on="server_id", how="left")
    .groupBy("application", "service", "process_date")
    .agg(
        F.count("*").alias("row_count"),
        F.avg("metric_value").alias("avg_metric"),
        F.max("metric_value").alias("peak_metric")
    )
)

result_df.write.mode("overwrite").partitionBy("process_date").parquet(output_path)
```

Punchline
My fit is practical PySpark data engineering: SQL, Unix/Linux, ETL
workflows, production troubleshooting, and financial-services data
pipeline experience.


 Punchline

My fit is PySpark, SQL, Unix, ETL, and production troubleshooting
from a financial-services data pipeline background.

---

<a id="sec-02-pyspark"></a>
# 02 — PySpark

<a id="q02"></a>
## Q02 Explain your PySpark experience and how you used it in production-style data pipelines.

[Back to TOC](#toc)


1. Citi PySpark context
   At Citi, my PySpark experience came from scaling telemetry and
   time-series data pipelines that supported reporting, validation,
   capacity planning, and forecasting.

2. Python/Pandas to PySpark scaling
   Originally, a lot of the processing was done with Python and Pandas.

As the data volume grew, single-machine processing became a bottleneck,
so we moved heavier transformation and forecasting workloads toward
PySpark and Hadoop-style distributed processing.

3. DataFrame-style transformations
   The work involved DataFrame-style transformations: selecting and
   filtering data, joining telemetry with reference data, grouping and
   aggregating metrics by host, application, service, and time bucket, and
   preparing cleaned datasets for reporting and forecasting.

4. Production validation and troubleshooting
   From a production-support point of view, I focused on row counts, schema
   consistency, missing or late data, duplicate records, null spikes, failed
   transformations, and downstream report mismatches.

5. Performance awareness
   For performance, I paid attention to partitioning, shuffle-heavy
   operations like joins and `groupBy`, avoiding unnecessary actions, and
   using partitioned outputs so downstream reads were more efficient.

6. My strongest PySpark lane
   So my PySpark experience is strongest around practical ETL processing,
   large operational datasets, validation, troubleshooting, and preparing
   data for reporting and forecasting.

```python
from pyspark.sql import functions as F

clean_df = (
    telemetry_df
    .filter(F.col("event_time").isNotNull())
    .filter(F.col("metric_value").isNotNull())
    .join(reference_df, on="server_id", how="left")
    .groupBy("host", "application", "service", "process_date")
    .agg(
        F.count("*").alias("row_count"),
        F.avg("metric_value").alias("avg_metric"),
        F.max("metric_value").alias("peak_metric")
    )
)

clean_df.write.mode("overwrite").partitionBy("process_date").parquet(output_path)
```




 Punchline

My PySpark experience is practical production ETL: large telemetry
datasets, DataFrame transformations, SQL-style aggregation, validation,
troubleshooting, and scaling heavier workloads beyond single-machine
Python/Pandas.

---

<a id="q03"></a>
## Q03 How does a PySpark job execute in the background?

[Back to TOC](#toc)


1. Driver starts the work
   PySpark code starts on the driver.

The driver reads the code, builds the execution plan, and coordinates
the work.

2. Transformations are lazy
   Transformations such as `select`, `filter`, `join`, and `groupBy` do not
   run immediately.

Spark uses them to build an execution plan.

3. Action triggers execution
   When an action runs, such as `count`, `show`, `collect`, or `write`,
   Spark triggers a job.

That is when Spark actually starts processing the data.

4. Jobs, stages, and tasks
   Spark breaks the job into stages.

Each stage is broken into tasks.

Executors run those tasks across partitions of the data in parallel.

5. Shuffle is the expensive point
   The expensive point is usually shuffle.

Shuffle happens during wide operations like `join`, `groupBy`,
`distinct`, and `repartition`, where data has to move across executors.

```python
# Transformations: lazy, build the plan
filtered_df = df.filter(df.status == "ACTIVE")

grouped_df = (
    filtered_df
    .groupBy("server_id")
    .count()
)

# Action: triggers the Spark job
grouped_df.show()

# Another action: triggers execution
grouped_df.write.mode("overwrite").parquet(output_path)
```


 Punchline

Transformations build the plan, actions trigger execution, executors
process partitions in parallel, and shuffle is usually the expensive
part to watch.

---

<a id="q04"></a>
## Q04 What is the difference between a transformation and an action in PySpark?

[Back to TOC](#toc)

1.0 Transformation definition
Transformations are operations that define a new DataFrame but do not
execute immediately.

Examples include `select`, `filter`, `withColumn`, `join`, and `groupBy`.

2.0 Lazy evaluation
Spark treats transformations as lazy.

That means Spark builds an execution plan on the driver, but it does not
actually process the data until an action is called.

3.0 Action definition
Actions trigger execution.

Examples include `show`, `count`, `collect`, and `write`.

4.0 What happens when action runs
When an action runs, Spark turns the plan into jobs, stages, and tasks.

Executors then process those tasks across partitions of the data.

5.0 Production meaning
In production, this matters because repeated actions like repeated
`count()` calls can trigger repeated execution if the DataFrame is not
cached or persisted.

So I try to understand when the job is only building a plan versus when
it is actually executing work.

```python
# Transformations: define a new DataFrame, but do not execute yet
filtered_df = df.filter(df.status == "ACTIVE")

selected_df = filtered_df.select(
    "server_id",
    "event_time",
    "metric_value"
)

enriched_df = selected_df.withColumn(
    "metric_double",
    selected_df.metric_value * 2
)

# Action: triggers execution
enriched_df.count()

# Another action: triggers execution
enriched_df.show(10)

# Write is also an action
enriched_df.write.mode("overwrite").parquet(output_path)
```



 Punchline

Transformations build the plan; actions trigger the plan to run.

---

<a id="q05"></a>
## Q05 What is shuffle in Spark, and why is it expensive?

[Back to TOC](#toc)

1.0 Shuffle definition
Shuffle is the movement of data across executors so Spark can bring
matching keys together.

It happens when records that belong together are currently spread across
different partitions or executors, and Spark needs to reorganize them.

2.0 Wide operations
Shuffle usually happens during wide operations like join, groupBy,
distinct, and repartition.

For example, if I group telemetry by server_id, Spark may need to move
records with the same server_id from different partitions so they can
be processed together.

3.0 Why shuffle is expensive
Shuffle is expensive because it involves network transfer, disk spill,
serialization, and extra coordination between stages.

It is often where slow Spark jobs spend most of their time.

4.0 What I check
To reduce shuffle, I look at partitioning, join keys, data skew,
broadcasting small lookup tables, and avoiding unnecessary repartition
or repeated wide operations.

5.0 Production view
In production, I do not treat shuffle as automatically bad, because some
shuffle is necessary. But I watch for unnecessary shuffle, repeated
shuffle, skewed shuffle, or shuffle caused by poor partitioning or join
strategy.

 Punchline

Shuffle is expensive data movement across executors so matching keys
can meet for joins, grouping, distinct, or repartition.

---

<a id="q06"></a>
## Q06 How would you troubleshoot a slow PySpark job?

[Back to TOC](#toc)

1. Start with basic validation
To troubleshoot a slow PySpark job, I would start with the basics:
confirm the input row counts, schema, filters, and expected output.
I want to know whether the job is slow because of data volume, bad logic,
data quality, or Spark execution behavior.
2. Inspect plan and logs
Then I would inspect the execution plan using .explain() and review
driver and executor logs for memory warnings, failed tasks, retries, or
spill symptoms.
3. Check shuffle and wide operations
The main performance area I would check is shuffle.
Wide operations like join, groupBy, distinct, and repartition
can create expensive shuffle because Spark may need to move data across
executors.
4. Check joins and broadcast option
If a join is slow, I would check whether one side is small enough for a
broadcast join. That allows Spark to send the small lookup DataFrame to the executors
instead of shuffling the larger dataset.
5. Check data skew
I would also check for data skew, where one key or one partition has
much more data than the others. That can make one task run much longer than the rest and slow down the
whole job.

6. Check partitions and file layout
Then I would review partition sizing and file layout.
I would look for too few partitions, too many partitions, bad partition
columns, or the small files problem, especially when reading or writing
many tiny files on HDFS or S3.

7. Check repeated actions
I would also check for unnecessary repeated actions like repeated
count(), show(), or collect() calls. Those can trigger Spark to recompute the same lineage multiple times if
the DataFrame is not cached or persisted appropriately.

8. Fix the smallest useful bottleneck
My goal is to identify whether the bottleneck is data movement, skew,
bad partitioning, repeated actions, file layout, or resource pressure.
Then I would fix the smallest thing that gives the biggest improvement.


 Punchline

I troubleshoot slow PySpark jobs by checking row counts, schema,
execution plan, logs, shuffle, joins, skew, partitions, repeated actions,
and small files.

---

<a id="q07"></a>
## Q07 How do you handle duplicates in PySpark?

[Back to TOC](#toc)

1. Identify duplicate type

To handle duplicates in PySpark, I first identify whether they are
full-row duplicates or business-key duplicates.

2. Full-row duplicates

For full-row duplicates, I can use distinct() or dropDuplicates().

3. Simple key duplicates

For simple key-based deduplication, I can use dropDuplicates(["user_id"]).
But I only use that when it does not matter which record survives.

4. Business-rule deduplication

If the business rule says to keep a specific record, such as the latest
record per user or server, I use a window function. I partition by the
business key, order by the timestamp descending, assign row_number(),
and keep only row number 1.

5. Production safety

That is safer for production pipelines because it makes the
deduplication rule explicit, repeatable, and tied to business logic.

```python
df.dropDuplicates(["user_id"])
```


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

 Punchline

For duplicates, first define the business key; use dropDuplicates
for simple cases, and use a window function when the surviving row matters.

---

<a id="q08"></a>
## Q08 How do you join two DataFrames in PySpark, and what can go wrong?

[Back to TOC](#toc)

1. Basic join idea

To join two DataFrames in PySpark, I use the .join() method with the
right DataFrame, the join condition, and the join type. The default is
usually an inner join, but in production pipelines I often need a left
join when I want to preserve all records from the main dataset.

2. First check: business meaning of the key

The first thing I check is the business meaning of the join key. I want
to know whether the key is unique, whether null keys are expected, and
whether duplicate keys are valid or a data-quality issue.

3. Common problems: row explosion and ambiguous columns

If both sides have duplicate keys, the join can multiply rows. If a left
join suddenly creates more rows than the main dataset, I investigate
duplicate keys on the lookup side.

If both DataFrames have the same column names, Spark may create ambiguous
column references or make the result harder to use.

4. Performance concern: shuffle

From a performance perspective, the biggest risk is shuffle. Joining large
datasets can require Spark to move data across executors so matching keys
can meet.

If one side of the join is small enough, I may use a broadcast join so
Spark sends the small lookup DataFrame to the executors instead of
shuffling the large dataset.

5. Production validation after the join

To protect the pipeline, I validate row counts before and after the join,
check null and duplicate key counts, rename ambiguous columns, confirm
the join type, and compare the output against expected business logic.

 Punchline

For joins, I validate the key, join type, row counts, nulls, duplicates,
schema, shuffle risk, and possible row explosion.

---

<a id="q09"></a>
## Q09 How do you handle nulls in PySpark?

[Back to TOC](#toc)

1.	Understand business meaning
Nulls in data would mean missing source data, late data, optional fields, 
or a real data-quality problem.
2.	Detect and isolate nulls
For analysis, I use isNull() and isNotNull() to count and isolate
missing records..
3.	Decide drop or preserve
 If the row is not useful without that field, I may use
dropna(). But if the row should be preserved, I use fillna() or a
business default, such as zero for a metric or "UNKNOWN" for a category.
4.	Protect downstream results
The important part is that the rule must be explicit. Dropping nulls
without understanding the data can change row counts, skew metrics, or
break downstream reporting and forecasting.


 Punchline

I handle nulls by first understanding the business rule, then using
`isNull`, `isNotNull`, `dropna`, or `fillna` without blindly dropping data.

---

<a id="q10"></a>
## Q10 How do you use window functions in PySpark?

[Back to TOC](#toc)

1.	Why use window functions
In PySpark, I use window functions when I need calculations across
related rows without collapsing the DataFrame like a normal groupBy.
2.	Define the window
First, I define a window using Window.partitionBy() for the business
key and orderBy() for the sequence. For example, I may partition by
server_id or customer_id and order by an update timestamp.
3.	Latest record per key
A common use case is keeping the latest record per key. I use
row_number() over the window, order by timestamp descending, and keep
only row number 1.
4.	Other use cases
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

5.	Key idea
They calculate within a group while preserving row-level detail.
 


 Punchline

Window functions let me calculate within a business-key group, such as
latest record, rank, or rolling metric, without losing row-level detail.

---

<a id="q11"></a>
## Q11 How do you read and write files in PySpark?

[Back to TOC](#toc)

Q11 — Tell me about yourself and how your background fits this role?

1.	Read with spark.read
In PySpark, I usually read files through spark.read, depending on
the file format. CSV, Parquet, JSON, etc.
2.	CSV needs options
 For CSV, I pay attention to options like header,
delimiter, and schema. 
```python
df = (
    spark.read
         .option("header", "true")
         .schema(my_schema)
         .csv(input_path)
)

```
3.	Prefer explicit schema
I prefer an explicit
schema instead of relying blindly on inferSchema, because explicit
schemas make the job more predictable.  


4.	Prefer Parquet for analytics
For larger analytics workloads, I prefer Parquet when available because
it is columnar and efficient for downstream reads.
```python
df = spark.read.parquet(input_path)

```
5.	Write carefully 
When writing, choose format, mode, output path, and partition strategy
carefully.
```python
(
    df.write
      .mode("overwrite")
      .partitionBy("date")
      .parquet(output_path)
)

```
6.	Validate after write
I use overwrite only when I intentionally want to replace data, and
append when I am adding new records. In production, I validate row
counts, schema, partition columns, and output paths after the write.


 Punchline

For file handling, I use explicit schemas, choose the right format,
write mode, and partitioning strategy, and validate the output.




<a id="sec-03-tomorrow-review-path"></a>
# 03 — Tomorrow Review Path

[Back to TOC](#toc)

## Best review order

For the human interview, focus on these first:

1. 00 — Human Interview Mode
2. Q01 — Story and role fit
3. Q02 — PySpark experience
4. Q03 — PySpark execution
5. Q05 — Shuffle
6. Q06 — Slow job troubleshooting
7. Q08 — Joins
8. Q10 — Window functions
9. Q11 — Read/write files

## 20-minute rapid review

Read only:
- Human strategy for tomorrow
- 30-second opening
- Q01 punchline
- Q02 punchline
- Q03 punchline
- Q05 punchline
- Q06 punchline
- Q08 punchline
- Q10 punchline
- Q11 punchline

## 60-minute review

1. Read 00 — Human Interview Mode.
2. Practice Q01 out loud twice.
3. Practice Q02 out loud twice.
4. Review Q03, Q05, and Q06.
5. Review Q08 and Q10.
6. Review Q11.
7. Finish with the recovery line.

## Final confidence script

I do not need to sound like a Spark architect. I need to sound like a
production data engineer who can read PySpark, explain SQL logic, work
in Unix/Linux, troubleshoot ETL pipelines, validate data, and communicate
clearly.

My lane is:
PySpark, SQL, Unix, ETL, production troubleshooting, and financial-services
data pipelines.


---

<a id="h01"></a>
## H01 — Tell me about yourself and how your background fits this role?
[Back to TOC](#toc)
1. Professional identity

I am a senior data engineer with strong experience in PySpark, SQL,
Unix/Linux, ETL workflows, and production troubleshooting.

2. Citi pipeline background

At Citi, I worked on telemetry and time-series data pipelines that
supported reporting, validation, capacity planning, and forecasting.
Originally, much of the processing was done with Python and Pandas.

3. Scaling story

As the data volume grew, single-machine processing became a bottleneck.
We moved heavier transformation and forecasting workloads toward PySpark
and Hadoop-style distributed processing.

4. Actual data work

My work with the data pipelines included filtering, joins, grouping,
aggregations, time buckets, reference data, and cleaned datasets for
reporting and forecasting.

5. Production support strength

From a production-support point of view, I focused on row counts, schema
consistency, missing or late data, duplicate records, null spikes, failed
transformations, and downstream report mismatches.

6. Role fit

That is why this role fits me. It needs PySpark development and analysis,
SQL, Unix shell scripting, ETL understanding, and production
troubleshooting. Those are the areas where my background is strongest.


 Punchline

My fit is PySpark, SQL, Unix, ETL, and production troubleshooting
from a financial-services data pipeline background.


---

<a id="h02"></a>
## H02 — Walk me through a production PySpark or ETL issue you troubleshot.
[Back to TOC](#toc)

H02 — Walk me through a production PySpark or ETL issue you troubleshot?

1.	Context
One production-style issue I can describe came from our monthly capacity
and forecasting processing cycle at Citi. This was not a nightly pipeline.
It was a month-end workflow that ran over a couple of days and produced
telemetry-based reporting and forecasting outputs for capacity planning
and management review.
2.	Pipeline purpose
The system collected infrastructure telemetry from monitoring and capacity
tools, prepared time-series datasets, grouped metrics by system, host,
application, service, and time period, and then produced reporting and
forecasting outputs. The business value was to identify capacity risk,
utilization trends, bottlenecks, and systems that needed attention. 
3.	Problem
One issue we had to troubleshoot was when the final monthly reporting
numbers did not line up with expectations. I did not start by assuming
the forecast was wrong. I traced the data path step by step: source
telemetry, input extracts, schema, row counts, date ranges, missing
systems, duplicate records, null spikes, aggregation logic, and final
reporting output.
4.	Investigation
The investigation pattern was to compare expected versus actual counts
by date, system, and group. If a host, application, or metric family was
missing or undercounted, I traced it backward to see whether the problem
came from the source extract, the transformation step, the aggregation
logic, or the reporting layer..
5.	Compare expected vs actual
The root cause turned out to be a layout change in one of the downstream
file types. That change affected part of the join and grouping logic,
which caused many endpoint systems to be dropped from the final output.


6.	Action
Once we confirmed the layout change was legitimate and would continue
going forward, we documented it, aligned with the stakeholders, applied
a hot fix, and reran safely after confirming the rerun would not duplicate
or corrupt output.  After that, we strengthened the pipeline with schema checks 
and earlier failure alerts so a similar issue would be caught before producing a bad
final result.

7.	Lesson Learnt
The lesson learned was that a green job status does not always mean the
output is correct. You still need validation checks around counts, schema,
expected groups, and business-level output.
 


 Punchline

For ETL troubleshooting, I trace the monthly processing cycle from
source telemetry to final reporting, validate counts and schema at each
stage, find where the mismatch starts, and improve checks so the next
cycle is safer.


---

<a id="h03"></a>
## H03 — How strong are you in PySpark, and where are you still growing?
[Back to TOC](#toc)

1. Practical PySpark strength

I am strongest in practical PySpark data engineering: reading data,
cleaning it, joins, aggregations, handling duplicates and nulls,
window functions, and preparing curated datasets.

2. Production ETL and troubleshooting

I am comfortable using Spark DataFrames for transformations,
SQL-style logic, row-count validation, schema checks, shuffle awareness,
partitioning concepts, and performance troubleshooting.

3. Honest growth area

I am still growing in deeper Spark platform areas: cluster tuning,
advanced internals, and environment-specific tooling.

4. Execution model awareness

I understand the execution model from driver to executors,
transformations, actions, jobs, stages, tasks, partitioning, and shuffle.

5. Role match

This role fits me well because it needs someone who can develop, read,
enhance, analyze, and troubleshoot PySpark scripts with SQL, Unix,
ETL workflows, and scheduling concepts.


 Punchline

My PySpark strength is practical ETL and production troubleshooting;
I can read, analyze, validate, and improve PySpark pipelines, while
continuing to grow deeper in Spark platform tuning.

---

<a id="h04"></a>
## H04 — What would you do if a PySpark job failed during a production run?
[Back to TOC](#toc)

1.	Check both sides
Inspect the job failure from the job-execution side and the data-pipeline side. 
2.	Job execution side
Check scheduler/job status, start time, parameters, failed step, Spark logs, failed stages, executor errors, and whether it failed during read, transform, join, shuffle or write. 
3.	Data pipeline side
Check upstream files or tables, schema changes, input counts, bad records, nulls, duplicates and other data-quality issues. 
4.	Rerun safety
Before rerunning, confirm whether the job overwrites, appends, uses checkpoints and could create duplicate output. 
5.	Downstream impact
Check affected reports, tables, business users and whether a clean rerun, partial rerun, partial rerun, or manual validation is needed.


 Punchline

When a PySpark job fails, I check logs, failed stages, parameters,
dependencies, data quality, downstream impact, and rerun safety before
simply restarting it.


---

<a id="h05"></a>
## H05 — How have you used Unix shell scripting in data or ETL workflows?
[Back to TOC](#toc)

1.	Shell as connective tissue
Shell scripting is useful around data and reporting workflows for automation, file handling, checks, logging and operational control.
2.	Pre-checks before the job
Before a process runs, shell can check input files, processing dates.  Environment variables, folders, and stop safely with a non-zero exit code if something important is missing. 
3.	Logs and operational checks
Shell commands like grep, awk, sed, sort, uniq, wc, tail and file commands help with errors, counts, file presence, archiving and reruns. 
4.	Right tool for the right layer
Shell should handle orchestration and OS-level workflow control.  Python, SQL, or PySpark should handle deeper transformations logic.
5.	Production separation
Shell keeps the workflow repeatable and operationally safe. Python, SQL, and PySpark handle the actual data logic
6.	Shell is a helper not the solution
Shell is a helper solution it is a tool .. solution for orchestration are systems like Apache Airflow/ Broadcom Autosys/ BMC ControlM ..  When any of these solutions exist, then shell can help enabling automation, investigation and troubleshooting.


 Punchline

Unix shell scripting is the workflow glue: file checks, environment
setup, job calls, logging, exit codes, archives, and rerun support,
while PySpark, SQL, or Python handles the heavy data logic.

---

<a id="h06"></a>
## H06 — What is your experience with scheduling tools like Airflow, Autosys, or Control-M?
[Back to TOC](#toc)

1.	Strongest recent experience
My strongest recent experience is production workflow support: dependencies, validation checkpoints, rerun planning, logs and Airflow-style orchestration concepts.
2.	Older scheduling exposure
I have exposure to enterprise batch processing concepts from my Telecom/ sprint time where BMC Control-M and Broadcom/Ca Autosys were used .. Ideas such as calendars, dependencies, upstream/downstream jobs, failure handling, reruns and logs. 
3.	Citi data-pipeline pattern
At CITI, the pattern was similar: Confirm inputs are ready, run steps in the right order, validate outputs, reruns when needed. Dependencies checks, review logs, review runs in Web UI
4.	Honest positioning
I am not claiming to be administrator for any of the said system, But I understand scheduling concepts and DAG philosophy in scheduling. I understand production workflow discipline and how to use it for smooth operations and troubleshooting of data pipelines. I can ramp quickly on the specific scheduler that the project/ team uses. 


 Punchline

My scheduling strength is production workflow thinking: dependencies,
calendars, retries, logs, reruns, validation, and downstream impact.
Control-M is older exposure; Airflow-style orchestration and production
workflow support are closer to my recent work.

--- 

<a id="h07"></a>
## H07 — How strong are you in SQL, and how have you used it with data pipelines?
[Back to TOC](#toc)

1.	SQL strength
SQL is one of my stronger areas. I have used it  for ingestion, transformations, feature development, validation, reporting and troubleshooting
2.	Pipeline usage
In telemetry and forecasting, I used SQL to join source data with reference data, aggregate metrics by system and time, validate row counts, detect nulls, find out of range metrics, create running averages, tag data as per business case and check unusual data patterns.
3.	SQL Techniques
I used CASE expressions, CTEs, joins, aggregations and window functions to create clear reporting datasets and feature style datasets for forecasting and capacity analysis
4.	Troubleshooting
SQl is one of stronger tools in my toolset when it comes to troubleshooting. In SQL I can check counts, filtered counts, duplicate keys, null spikes, date ranges and aggregation logic to find where the mismatch starts. 


 Punchline

SQL is one of my strongest tools for joining, aggregating, validating,
reconciling, reporting, and troubleshooting pipeline data.

--- 
<a id="h08"></a>
## H08 — How would you troubleshoot an ETL pipeline from source to final output?
[Back to TOC](#toc)

1.	Trace the whole path
Troubleshoot the ETL pipeline by tracing the data path from source to final output instead of looking only at the failed step.
2.	Validate the source
I validate the source: Did the file, table or extract arrive. Did the data in the source match the schema. Is the data in the source matching the expected conditions expected ex. Dates. Does the data counts match that of last know good runs?
3.	Validate Transformations
Check filters, joins, aggregation, null handling, duplicates, Business rules, errors and failed steps. Compare counts to find where the drift starts
4.	Validate the output
Check row counts, schemas, partitions, totals and sample records. Check whether the table or report/ table matches the business expectations. 
5.	Check rerun safety
Before rerunning, make sure issues are resolved. Make sure that rerunning will not duplicate some results. Use check points 
6.	Guards for next time and reporting
After the fix, add checks and early failure and alerts so that that error will not happen next time or be handled in a safer way.  Persist changes that are legitimate if concerned parties approve of. Provide full documentation on the situation, RCA and solution provided. 


 Punchline

For ETL troubleshooting, I trace source to transform to output, compare
counts to known good runs, find where the mismatch starts, check rerun
safety, and add guards for next time.



--- 

<a id="h09"></a>
## H09 — What questions would you ask the interviewer?
[Back to TOC](#toc)

1. What does success look like for this role in the first 90 days?

2. What would make someone unusually successful in this role beyond
   just meeting the job description?

3. What types of PySpark pipelines would I be supporting or enhancing:
   ingestion, transformation, reporting, forecasting, or production
   support?

4. How is the work split between PySpark development, SQL work,
   Unix/backend scripting, and production troubleshooting?

5. What scheduling or automation tools are currently used for these
   workflows, such as Airflow, Autosys, or Control-M?

 Punchline

I want to understand the real production workflow, the success criteria,
and where PySpark, SQL, Unix scripting, and troubleshooting fit day to day.


---

<a id="h10"></a>
## H10 — Before we finish, is there anything else you would like us to know?
[Back to TOC](#toc)

1. Genuine Interest + Skill Match
Yes, I am genuinely interested in this opportunity. This role lines up
well with my background in PySpark, SQL, Unix/Linux, ETL workflows, and
production troubleshooting.

2. Production Discipline
What I believe I can bring is not only coding, but also production
discipline: validating inputs and outputs, tracing pipeline issues,
checking row counts and schema, understanding downstream impact, and
communicating clearly with the team.

3. Hybrid Comfort + Ready to Contribute
I also understand this is a hybrid Dallas/Wipro role, and I am comfortable
with that. I would be excited to contribute as a Senior PySpark Developer
and help support reliable data pipelines for the client.

 Punchline

I bring PySpark, SQL, Unix, ETL, and production troubleshooting experience,
and I am ready to contribute in a hybrid Dallas/Wipro role.


---

<a id="h11"></a>
## H11 — What Unix commands do you commonly use when troubleshooting data jobs?
[Back to TOC](#toc)

1. Fast First-Line Troubleshooting

Unix commands give me a fast way to troubleshoot data pipeline runs.
I use them for a variety of purposes, including file checks, log review,
searching for text patterns, record counts, field checks, and basic
operational validation.

2. File, Count, Log Checks, and Permissions

I use ls and find to check whether files exist, wc -l to check record
counts, and ls -l to inspect file permissions. If a permission change is
needed, chmod can be used when appropriate.

I also use less, head, and tail to inspect log files or sample portions
of input and output files.

3. Search, Field Checks, and Duplicates

I use grep to search for text patterns such as errors, warnings, job IDs,
or specific records. I use awk, sed, and cut for field-level checks, and
sort and uniq to find duplicates or repeated patterns.

4. Data Pipeline Purpose

In a data pipeline, these commands help me confirm input and output files,
validate record counts and intermediate steps, search logs for errors and
stats, compare against known good runs, and support rerun analysis.

 Punchline

Unix commands are my first-line troubleshooting tools for checking files,
logs, counts, errors, permissions, and rerun readiness around ETL jobs.


---

