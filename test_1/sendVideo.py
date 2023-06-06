import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time
from dronekit import connect
import threading

broker_address = "localhost"
broker_port = 1883


def pictureStream(seconds):
    global takingPictures
    cap = cv.VideoCapture(0)
    while takingPictures:
        ret, frame = cap.read()
        _, buffer = cv.imencode('.jpg', frame)
        # Converting into encoded bytes
        jpg_as_text = base64.b64encode(buffer)
        client.publish('picture', jpg_as_text)
        time.sleep(seconds)


def on_message(client, userdata, message):
    global takingPictures
    if message.topic == 'getHeading':
        print('Get heading')
        connection_string = "/dev/ttyS0"
        vehicle = connect(connection_string, wait_ready=True, baud=115200)
        client.publish('heading', str(vehicle.heading))
        vehicle.close()

    if message.topic == 'takePicture':
        print('take picture')
        cap = cv.VideoCapture(0)
        ret, frame = cap.read()
        _, buffer = cv.imencode('.jpg', frame)
        # Converting into encoded bytes
        jpg_as_text = base64.b64encode(buffer)
        client.publish('picture', jpg_as_text)

    if message.topic == 'startPictureStream':
        seconds = int(message.payload)
        print('start picture stream ', seconds)
        takingPictures = True
        pictureStream
        w = threading.Thread(target=pictureStream, args=(seconds,))
        w.start()

    if message.topic == 'stopPictureStream':
        print('stop picture stream ')
        takingPictures = False


client = mqtt.Client("On board controller")
client.on_message = on_message
client.connect(broker_address, broker_port)
print('Waiting commands...')
# client.subscribe('getHeading')
client.subscribe('takePicture')
client.subscribe('startPictureStream')
client.subscribe('stopPictureStream')
client.loop_forever()
