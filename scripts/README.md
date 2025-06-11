## 📝 Submitting a Spark Application

This script is **not run with Python directly**, but should be submitted to the Spark cluster using the `spark-submit` command.

Open a new terminal window and run the following command from the **project root directory**:

### Bash

```bash
docker-compose exec spark-master spark-submit \
--conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
--conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
/opt/bitnami/spark/scripts/process_city_events.py
```

### 🔍 Command Breakdown

- `docker-compose exec spark-master`: Executes the command inside the `spark-master` container.
- `spark-submit`: The standard command to submit a Spark job.
- `--packages ...`: **Important!** This tells Spark to automatically download and load the neces

## Running Spark Jobs

With the custom Spark image, you can now run streaming jobs with Delta Lake and Kafka support using a simple command:

```bash
# Simple command - dependencies already included in the image
docker-compose exec spark-master spark-submit /opt/bitnami/spark/scripts/process_city_events.py
```

**✅ No need for additional packages or configurations** - everything is pre-installed!

## 🧠 Explanation of Key Changes

- `.format("delta")`: Instructs Spark to store the data using the **high-performance and reliable Delta format**.
- `.start(HDFS_OUTPUT_PATH)`: Defines the **HDFS path** where the Delta Lake table will be stored: `/lake/city_events`.
- `.option("checkpointLocation", ...)`: This is **critical** for structured streaming. Spark stores processing progress (e.g., Kafka offsets) at this checkpoint path.  
  If the Spark job is interrupted, it can **resume from the last state** to avoid data loss or duplication — ensuring **true fault tolerance**.

---

### 💡 Why We Changed from Console to Delta Lake

Using the **console sink** allows us to quickly and immediately see what the transformed data looks like, without writing it to a file system.  
This is **very convenient for debugging and quick verification** during development.

However, our ultimate goal is **not just to view the data on the screen**, but to **build a reliable Data Lake** that can support future analytics and machine learning tasks.  
To do that, we need to **persist the data** to long-term storage.

Using `.format("delta")` helps us achieve that by writing the streaming data to a **Delta Lake table** — enabling data versioning, ACID transactions, and scalable queries.


## ✏️ Step 2: Modify the `process_city_events.py` Script

Open the `process_city_events.py` file located in the `./scripts/` directory and scroll to the **bottom** of the file to find the `writeStream` section.

### 🔁 Replace the existing code:

#### ❌ Original code (Console Sink):

```python
# --- SINK STAGE (OLD) ---
# For now, let's write the output to the console to verify our logic
query = transformed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()
```

#### ✅ Updated code (Delta Lake Sink on HDFS):

```python
# --- SINK STAGE (NEW) ---
# Now, let's write the streaming data to a Delta Lake table on HDFS
# We need a checkpoint location for fault-tolerant streaming
HDFS_CHECKPOINT_LOCATION = "hdfs://namenode:9000/checkpoints/city_events"
HDFS_OUTPUT_PATH = "hdfs://namenode:9000/lake/city_events"

query = transformed_df.writeStream \
    .outputMode("append") \
    .format("delta") \
    .option("checkpointLocation", HDFS_CHECKPOINT_LOCATION) \
    .start(HDFS_OUTPUT_PATH)
```

### 🧠 Explanation of Key Changes

- `.format("delta")`: Instructs Spark to store the data using the **high-performance and reliable Delta format**.
- `.start(HDFS_OUTPUT_PATH)`: Defines the **HDFS path** where the Delta Lake table will be stored: `/lake/city_events`.
- `.option("checkpointLocation", ...)`: This is **critical** for structured streaming. Spark stores processing progress (e.g., Kafka offsets) at this checkpoint path.  
  If the Spark job is interrupted, it can **resume from the last state** to avoid data loss or duplication — ensuring **true fault tolerance**.

---

## 🔁 Step 3: Re-submit the Spark Application

After saving the modified script, return to the terminal window where you previously ran the `spark-submit` command.

1. Press `Ctrl + C` to stop the running Spark job that was outputting to the console.
2. Then, re-run the exact same `spark-submit` command:

### Bash

```bash
docker-compose exec spark-master spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.2.0 \
/opt/bitnami/spark/scripts/process_city_events.py
```

This will now start a streaming job that **writes to Delta Lake on HDFS** with full **checkpoin**
