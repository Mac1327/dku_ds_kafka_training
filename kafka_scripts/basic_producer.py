from datetime import datetime
from kafka import KafkaProducer
from time import sleep
import json
import hashlib

producer = KafkaProducer(bootstrap_servers='10.128.0.32:9092')
topic = "init_test_topic"

print('producing ...')
count=0
while True:
	count+=1
	now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
	hash_val = hashlib.sha256(str.encode(str(count)+now)).hexdigest()
	to_pub ={
		'date_time': now,
		'count': count,
		'hash' :hash_val
	}
	
	producer.send(topic, json.dumps(to_pub).encode('utf-8'))
	sleep(0.5)



