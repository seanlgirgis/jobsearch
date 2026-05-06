# Interview Q&A

1. **What is Structured Streaming?**
A Spark model for processing continuous data using unbounded-table semantics.

2. **What is micro-batch?**
Recurring small processing windows rather than one giant batch.

3. **Why checkpointing matters?**
It supports recovery and helps avoid data loss during failures.

4. **What is a trigger interval?**
It defines how often streaming batches execute.

5. **How do you handle late data?**
Use event-time logic, windows, and clear lateness policy.

6. **How do you handle schema drift?**
Add schema governance and controlled evolution checks.

7. **How do you monitor streaming jobs?**
Track lag, failed batches, throughput, and quality signals.

8. **How do you frame your experience safely?**
Practical exposure to concepts and operations, with stronger Spark batch foundations.
