from flask import Flask, render_template, Response, request
import cv2
import dataiku
import numpy as np
from kafka import KafkaConsumer

KAFKA_SERVER='localhost:29092'

haar_location = dataiku.get_custom_variables()['haar_eyes']
body_classifier = cv2.CascadeClassifier(haar_location)

topic = "distributed-video1"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=[KAFKA_SERVER])

def gen_frames():  
    for msg in consumer:

        frame = cv2.imdecode((np.frombuffer(msg.value, dtype=np.uint8)), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        bodies = body_classifier.detectMultiScale(gray, 1.2, 70)   
        for (x,y,w,h) in bodies:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,20,147),6)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/haar_kafka')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

