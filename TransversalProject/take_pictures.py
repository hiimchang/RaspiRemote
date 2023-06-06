# coding=utf-8
import sys
import datetime
import os
from mpu6050 import mpu6050
import time
import csv
import xml.etree.cElementTree as ET


if __name__ == '__main__':

    dir = '/home/ubuntu/RaspiRemote/TransversalProject/images/1905_1/'
    dir_imu = '/home/ubuntu/RaspiRemote/TransversalProject/images/1905_1/IMU_0.csv'

    mpu = mpu6050(0x68)

    if not os.path.exists(dir):
        os.mkdir(dir)
    print('images will be saved in:', dir)

    f = open(dir_imu, 'w')

    #   definition of parameters, more at https://www.raspberrypi.org/app/uploads/2013/07/RaspiCam-Documentation.pdf
    # rotation
    rot = '180'
    # saturation，-100 - 100
    sa = '30'
    # width
    width = '2560'
    # height
    height = '1440'
    # timeout in millisecond
    timeout = '2000'
    # ISO
    iso = '600'
    # shutter speed in microseconds
    ss = str(20000/int(iso))
    # set exposure mode
    mode = 'sports'
    start_time = int(time.time())
    if sys.argv.__len__() == 2:
        interval = int(sys.argv[1])
    else:
        interval = 3  # default value is 3s, interval(seconds) > timeout(millisecond)
    print('start time:', datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    shot_time = start_time + interval

    while True:
        now_time = int(time.time())
        if now_time == shot_time:
            save_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
            print('shot time:', save_str)
            os.system('raspistill -o ' + dir + save_str + '.jpg' +
                      ' -rot ' + rot +
                      ' -sa ' + sa +
                      ' -h ' + height +
                      ' -w ' + width +
                      ' -t ' + timeout)

            #                     ' -ISO ' + iso +
            #                       ' -ss ' + ss +

            accel_data = mpu.get_accel_data()
            gyro_data = mpu.get_gyro_data()
            f.write(str(accel_data['x']) + ',' + str(accel_data['y']) + ',' + str(accel_data['z']) + ',' +
                    str(gyro_data['x']) + ',' + str(gyro_data['y']) + ',' + str(gyro_data['z']) + ',' +
                    str(mpu.get_temp()) + '\n')
            f.flush()
            shot_time = now_time + interval
