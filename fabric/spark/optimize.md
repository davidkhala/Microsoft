# small file problem
Cause
- Spark is a parallel-processing framework, with data stored multiple worker nodes.
- Parquet files are immutable, with new files written for every update or delete.
- This process can result in a large number of small files,

Impact: queries over large amounts of data can run slowly

# OptimizeWrite
Similar to [Databricks optimized-writes](https://docs.databricks.com/en/delta/tune-file-size.html#optimized-writes-for-delta-lake-on-databricks)

`OptimizeWrite` is enabled by default 
- in Spark session level
    - `spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", False)`
- in Table Properties
  - TODO
