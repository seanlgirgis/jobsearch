# Interview Q&A

1. **Which checks matter most first?**
Schema, null, duplicate, row count, and core business-rule checks.

2. **Why run checks per layer?**
So bad data is blocked early and does not propagate.

3. **How do you make checks actionable?**
Use pass/fail criteria, logging, and owner-based alerts.

4. **How do you handle failures?**
Contain impact, remediate, rerun safely, then prevent recurrence.

5. **How do you test data pipelines?**
Unit-test transforms and verify expected dataset outputs and edge cases.

6. **How does this support stakeholders?**
It protects reporting and ML consumers from silent data defects.

7. **How does this map to role requirements?**
Directly maps to validation, automated checks, monitoring, and operational support.

8. **How do you position yourself?**
As reliability-focused data engineer with strong quality and operations ownership.
