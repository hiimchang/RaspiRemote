import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time
from dronekit import connect
import threading

broker_address ="localhost"
broker_port = 1883

def pictureStream (seconds):
     global takingPictures
     cap = cv.VideoCapture(0)
     while takingPictures:
        ret, frame = cap.read()
        _, buffer = cv.imencode('.jpg', frame)
        # Converting into encoded bytes
     jpg_as_text = base64.b64encode(buffer)
     client.publish('picture', jpg_as_text)
     time.sleep(seconds)