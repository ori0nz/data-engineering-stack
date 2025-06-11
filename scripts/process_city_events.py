# ./scripts/process_city_events.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, TimestampType

def main():
    """
    Main function to run the Spark Streaming application.
    """
    # Define the connection properties for Spark to connect to HDFS
    # We need to tell Spark how to find the NameNode
    HDFS_NAMENODE_ADDRESS = "hdfs://namenode:9000"

    # Define Kafka properties
    KAFKA_BOOTSTRAP_SERVERS = "kafka1:9092,kafka2:9092"
    KAFKA_TOPIC = "city-events"

    # Define the schema for the incoming JSON data from Kafka
    # This must match the structure of the data sent by the producer
    schema = StructType([
        StructField("city_name", StringType(), True),
        StructField("temperature", FloatType(), True),
        StructField("humidity", FloatType(), True),
        StructField("pm25", IntegerType(), True),
        StructField("traffic_index", FloatType(), True),
        StructField("event_type", StringType(), True),
        StructField("timestamp", StringType(), True) # Read as string first, then cast
    ])

    # Create a SparkSession
    # We need to include packages for Kafka and Delta Lake integration
    spark = SparkSession.builder \
        .appName("CityEventsProcessor") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,io.delta:delta-spark_2.12:3.2.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN") # Reduce verbosity of logs

    print("Spark Session created successfully.")

    # Read data as a stream from the Kafka topic
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()

    print("Streaming DataFrame created from Kafka.")

    # The 'value' column from Kafka is binary, cast it to a string
    # Then parse the JSON string using the defined schema
    parsed_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("data")) \
                        .select("data.*")

    # Add a data transformation: convert temperature to Fahrenheit
    transformed_df = parsed_df.withColumn("temperature_fahrenheit", (col("temperature") * 9/5) + 32) \
                              .withColumn("timestamp", col("timestamp").cast(TimestampType())) # Cast timestamp string to actual timestamp

    # --- SINK STAGE ---
    # For now, let's write the output to the console to verify our logic
    # This is the easiest way to see the results of a streaming query
    '''
    query = transformed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()
    '''

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

    print("Streaming query started. Writing to console...")
    
    # Wait for the streaming query to terminate
    query.awaitTermination()


if __name__ == "__main__":
    main()