from kafka import KafkaConsumer

# Create a KafkaConsumer instance
consumer = KafkaConsumer(
    'neowstopic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    auto_commit_interval_ms=1000,
    value_deserializer=lambda x: x.decode('utf-8')
)

# Start consuming messages
try:
    for message in consumer:
        print(message.value)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
