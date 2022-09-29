from kafka import KafkaConsumer

# Fire up the Kafka Consumer
topic = "init_test_topic"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=['localhost:9092'])


topic = "init_test_topic"

for msg in consumer:
        print(msg.value)

