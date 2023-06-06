# coding=utf-8
import math
import sys
import datetime
import os
import json
import cv2 as cv
import dronekit
import numpy as np
import paho.mqtt.client as mqtt
import base64
import threading
import time
from mpu6050 import mpu6050


def distanceInMeters(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5


def send_video_stream(origin, client):
    global sending_video_stream
    global cap

    cap = cv.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))
    print(width, height)

    topic_to_publish = f'cameraService/{origin}/videoFrame'

    while sending_video_stream:
        # Read Frame
        ret, frame = cap.read()
        if ret:
            _, image_buffer = cv.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(image_buffer)
            client.publish(topic_to_publish, jpg_as_text)
            time.sleep(0.2)


def on_external_message(client, userdata, message):
    global external_client
    process_message(message, external_client)


def on_internal_message(client, userdata, message):
    global internal_client
    process_message(message, internal_client)


def takePicture():
    dir_img = '/home/ubuntu/RaspiRemote/TransversalProject/images/test_0206/4/img/'

    #   definition of parameters, more at https://www.raspberrypi.org/app/uploads/2013/07/RaspiCam-Documentation.pdf
    # rotation
    rot = '0'
    # saturation，-100 - 100
    sa = '30'
    # width
    width = '1920'
    # height
    height = '1080'
    # timeout
    timeout = '3000'
    # ISO
    iso = '200'
    # shutter speed in microseconds
    ss = str(20000 / int(iso))
    # set exposure mode
    mode = 'sports'

    save_str = datetime.datetime.strftime(datetime.datetime.now(),
                                          '%Y-%m-%d-%H-%M-%S')
    print('shot time:', save_str)
    os.system('raspistill -o ' + dir_img + save_str + '.jpg ' +
              ' -rot ' + rot +
              ' -sa ' + sa +
              ' -t ' + timeout)

    recordIMU()


def recordIMU():
    dir_imu = '/home/ubuntu/RaspiRemote/TransversalProject/images/test_0206/4/IMU_1.txt'

    mpu = mpu6050(0x68)
    f = open(dir_imu, 'w')

    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()
    f.write(str(accel_data['x']) + ',' + str(accel_data['y']) + ',' + str(accel_data['z']) + ',' +
            str(gyro_data['x']) + ',' + str(gyro_data['y']) + ',' + str(gyro_data['z']) + ',' +
            str(mpu.get_temp()))
    time.sleep(0.1)


def takePicturesInstant():
    global takingPicturesInstant

    start_time = int(time.time())
    interval = 5
    print('start time:', datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    shot_time = start_time + interval

    while takingPicturesInstant:
        now_time = int(time.time())
        if now_time == shot_time:
            takePicture()
            shot_time = now_time + interval


def executePicturesPlan(pwaypoints_json):
    global external_client
    global internal_client
    global position

    altitude = 4  # a default Alt value is 6
    picturePoints = json.loads(pwaypoints_json)
    distanceThreshold = 0.5

    for pp in picturePoints['coordinates']:
        nextPoint = dronekit.LocationGlobalRelative(float(pp[0]), float(pp[1]), altitude)
        currentLocation = dronekit.LocationGlobalRelative(
            float(position["lat"]), float(position["lon"]), float(position["altitude"]))
        dist = distanceInMeters(nextPoint, currentLocation)

        while dist > distanceThreshold:
            time.sleep(0.15)
            currentLocation = dronekit.LocationGlobalRelative(
                float(position["lat"]), float(position["lon"]), float(position["altitude"]))
            dist = distanceInMeters(nextPoint, currentLocation)
        print('At taking pictures point')
        takePicture()
        recordIMU()


def process_message(message, client):
    global sending_video_stream
    global cap
    global position
    global takingPicturesInstant

    split = message.topic.split('/')
    origin = split[0]
    command = split[2]

    if command == 'telemetryInfo':
        position = json.loads(str(message.payload.decode('utf-8')))

    if command == 'executePicturesPlan':
        picturesPoints_json = str(message.payload.decode('utf-8'))
        w = threading.Thread(target=executePicturesPlan, args=[picturesPoints_json, ])
        w.start()

        # waypoints_json_dir = str(message.payload.decode('utf-8'))
        # with open(waypoints_json_dir, 'r') as j:
        #     w = threading.Thread(target=executePicturesPlan, args=[j, ])
        #     w.start()

    if command == 'startVideoStream':
        print('start video stream')
        sending_video_stream = True
        w = threading.Thread(
            target=send_video_stream,
            args=(origin, client),
        )
        w.start()

    if command == 'stopVideoStream':
        print('stop video stream')
        sending_video_stream = False

    if command == 'takePicturesInstant':
        print('start to take pictures')
        takingPicturesInstant = True
        w = threading.Thread(
            target=takePicturesInstant)
        w.start()

    if command == 'takePicture':
        print('hovering to take a picture')
        takePicture()

    # if command == 'PicturePointsToCamera':
    #     print(f"Received `{message.payload.decode('utf-8')}` from `{message.topic}` topic")


def CameraService(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state
    global cap
    global sending_video_stream
    global takingPicturesInstant

    sending_video_stream = False
    takingPicturesInstant = False

    print('Camera ready')
    print('Connection mode: ', connection_mode)
    print('Operation mode: ', operation_mode)
    op_mode = operation_mode

    internal_broker_address = 'localhost'
    internal_broker_port = 1884

    if connection_mode == 'global':
        external_broker_address = external_broker
    else:
        external_broker_address = 'localhost'

    print('External broker: ', external_broker_address)

    # the external broker must run always in port 8000
    external_broker_port = 8000

    external_client = mqtt.Client('Camera_external', transport='websockets')
    if external_broker_address == 'classpip.upc.edu':
        external_client.username_pw_set(username, password)

    external_client.on_message = on_external_message
    external_client.connect(external_broker_address, external_broker_port)

    internal_client = mqtt.Client('Camera_internal')
    internal_client.on_message = on_internal_message
    internal_client.connect(internal_broker_address, internal_broker_port)

    print('Waiting....')
    print('---------')
    external_client.subscribe('+/cameraService/#', 2)
    internal_client.subscribe('+/cameraService/#')
    external_client.subscribe('autopilotService/+/telemetryInfo', 1)
    # external_client.subscribe('webApplication/cameraService/PicturePointsToCamera')

    internal_client.loop_start()
    external_client.loop_start()


if __name__ == '__main__':
    connection_mode = sys.argv[1]  # global or local
    operation_mode = sys.argv[2]  # simulation or production
    username = None
    password = None
    if connection_mode == 'global':
        external_broker = sys.argv[3]
        if external_broker == 'classpip.upc.edu':
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None

    CameraService(connection_mode, operation_mode, external_broker, username, password)
