from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import json
from utils import data_process, connection_db, write_to_mongo

mongo_collection = connection_db()

# Create the Spark Session
spark = (
    SparkSession
    .builder
    .appName("Streaming from Kafka")
    .config("spark.streaming.stopGracefullyOnShutdown", True)
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.11-2.4.5')
    .config("spark.sql.shuffle.partitions", 1)
    .master("local[*]")
    .getOrCreate()
)

# Read from Kafka topic
kafka_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "172.25.0.13:9092")
    .option("subscribe", "TOPICA")
    .option("failOnDataLoss", "false") \
    .load()
)

print("consommation .....")
# Cast the 'value' column to string
kafka_json_df = kafka_df.withColumn("value", expr("cast(value as string)"))

# Define a global list to store the values
collected_values = []

# Define the foreachBatch function
def collect_to_list(batch_df, batch_id):
    # Collect the values in the batch and append them to the global list
    global collected_values
    batch_values = batch_df.select("value").rdd.map(lambda row: row.value).collect()
    
    # Use json.loads() instead of json.load()
    for value in batch_values:
        collected_values.append(json.loads(value))
    
    print("Current list of values:", collected_values)
    
    # Process data and write to MongoDB
    data_cleaned = data_process(collected_values)
    write_to_mongo(mongo_collection, data_cleaned)
    
    # Clear collected values after processing
    collected_values.clear()

# Write stream with foreachBatch and checkpointLocation
query = (
    kafka_json_df
    .writeStream
    .foreachBatch(collect_to_list) 
    .outputMode("append")
    .option("checkpointLocation", "/checkpoint") 
    .start()
)

query.awaitTermination()
spark.close()
