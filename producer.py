
import sys
import time
import cv2
from kafka import KafkaProducer

KAFKA_SERVER='localhost:29092'

topic = "distributed-video1"

def publish_camera():
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(topic, buffer.tobytes())
            # Commeet the sleep if video is chaoppy
            time.sleep(0.1)

    except:
        print("\nExiting.")
        sys.exit(1)
    camera.release()
if __name__ == '__main__':
    print("publishing feed!")
    publish_camera()