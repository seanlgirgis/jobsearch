# Interview Q&A

1. **How do you connect Databricks to S3 securely?**
Use IAM role-based access and Unity Catalog storage credential/external location concepts.

2. **Why avoid hardcoded access keys?**
Role-based access is safer, more controllable, and easier to audit.

3. **What is the value of silver and gold layers?**
Silver enforces data quality. Gold serves analytics and feature consumers.

4. **Where do quality checks fit?**
At each promotion step, especially before silver and gold publishing.

5. **How does this map to your background?**
It maps directly to my AWS S3/Glue/Redshift pipeline foundations.

6. **Do you need AWS credentials for this lab?**
No, this is architecture and pseudocode rehearsal only for tonight.

7. **How do you discuss Databricks honestly?**
As practical exposure built on stronger AWS and Spark pipeline delivery.

8. **How does this support ML pipelines?**
Gold outputs can feed stable, validated feature datasets for ML workflows.
