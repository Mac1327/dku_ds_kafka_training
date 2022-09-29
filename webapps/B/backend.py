from flask import Flask, render_template, Response, request
import cv2

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from kafka_training import loop_people, edges
from kafka import KafkaConsumer

KAFKA_SERVER='localhost:29092'

topic = "distributed-video1"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=[KAFKA_SERVER])

model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']

def gen_frames():  
    for msg in consumer:
        frame = cv2.imdecode((np.frombuffer(msg.value, dtype=np.uint8)), cv2.IMREAD_COLOR)
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 384,640)
        input_img = tf.cast(img, dtype=tf.int32)

        results = movenet(input_img)
        keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))

        loop_people(frame, keypoints_with_scores, edges, 0.1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/pose_stream')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

