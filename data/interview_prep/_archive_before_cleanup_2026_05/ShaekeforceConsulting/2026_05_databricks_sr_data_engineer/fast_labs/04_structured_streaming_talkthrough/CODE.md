```python
# Conceptual pseudocode only (not a full runnable production script)

stream_df = (
    spark.readStream
         .format("cloudFiles")
         .option("cloudFiles.format", "json")
         .load("/mnt/raw/events")
)

transformed_df = (
    stream_df
      .withColumn("event_date", F.to_date("event_ts"))
      .filter("event_type is not null")
)

query = (
    transformed_df.writeStream
      .format("delta")
      .outputMode("append")
      .option("checkpointLocation", "/mnt/checkpoints/events_stream")
      .trigger(processingTime="30 seconds")
      .toTable("default.events_silver_stream")
)

# query.awaitTermination()
```
