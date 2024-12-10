import os
from kafka import KafkaConsumer
import json
import time

consumer = KafkaConsumer(
    'kafka-nifi-dst',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='json_saver',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Waiting for messages...")

# for message in consumer:
#     print(f"Received message: {message.value}")

os.makedirs('./output', exist_ok=True)

for message in consumer:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f'output_{timestamp}.json'
    # print(f"Received message: {message.value}")

    with open(f"./output/{filename}", 'w') as file:
        json.dump(message.value, file)
        file.flush()
