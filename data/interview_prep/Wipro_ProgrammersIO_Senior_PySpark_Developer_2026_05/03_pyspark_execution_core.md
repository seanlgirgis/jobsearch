# PySpark Execution Core

## Concepts (Interview-Safe)
- Driver: Coordinates Spark app, builds plan, schedules work.
- Executor: Worker process that runs tasks and stores cached data.
- Cluster manager: Resource allocator (YARN/K8s/Standalone).
- Transformation: Lazy operation returning new DataFrame.
- Action: Triggers execution (show/count/write/collect).
- Lazy evaluation: Spark delays execution to optimize full DAG.
- Job: Execution unit triggered by one action.
- Stage: Group of tasks separated by shuffle boundaries.
- Task: Smallest unit run on one partition.
- Partition: Logical chunk of data for parallel processing.
- Shuffle: Data movement across executors for wide operations.
- Narrow transformation: No full redistribution (map/filter/select).
- Wide transformation: Requires shuffle (groupBy/join/orderBy).
- Cache/persist: Store intermediate results for reuse.
- Broadcast join: Send small table to executors to avoid large shuffle.
- Skew: Uneven key distribution causing straggler tasks.

## Quick Interview Scripts
Q: How does Spark execute a DataFrame pipeline?
A: "Transformations build a lazy DAG on the driver. An action triggers job
execution, Spark splits work into stages and tasks, executors process
partitions, and shuffle occurs at wide operations like joins/groupBy."

Q: Difference between job, stage, task?
A: "Job comes from an action, stages are separated by shuffle boundaries,
and tasks are per-partition units executed on executors."

Q: What is shuffle and why expensive?
A: "Shuffle moves data across executors and involves network, disk, and
serialization overhead, so reducing unnecessary shuffle is key."

Q: When to use broadcast join?
A: "When one side is small enough to broadcast, to reduce large data
movement and speed up joins."

Q: How do you handle skew?
A: "Detect skewed keys, repartition carefully, consider salting for heavy
keys, and validate stage/task timing improvements."
