from kafka import KafkaProducer
import json
import time

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8') 
)

# Send messages to the Kafka topic
for i in range(10): 
    message = {
        "id": i,
        "message": f"Test message {i}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send the message to the topic 'kafka-nifi-dst'
    producer.send('kafka-nifi-dst', value=message)
    print(f"Sent message: {message}")
    
    time.sleep(1) 

# Close the producer
producer.close()
