# coding=utf-8
import sys
import datetime
import os
from mpu_6050 import mpu6050
import time
import csv


if __name__ == '__main__':
    dir = "/home/ubuntu/RaspiRemote/images_sample"
    mpu = mpu6050(0x68)
    if not os.path.exists(dir):
        os.mkdir(dir)
    print("save path:", dir)

    # 旋转角度
    rot = "180"
    # 饱和度，-100 - 100
    sa = "30"
    # 宽度
    width = "1920"
    # 高度
    height = "1080"

    # 更多参数参见摄像头文档http://shumeipai.nxez.com/2014/09/21/raspicam-documentation.html

    start_time = int(time.time())
    if sys.argv.__len__() == 2:
        interval = int(sys.argv[1])
    else:
        interval = 10
    print("start time:", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    shot_time = start_time + interval

    while True:
        now_time = int(time.time())
        if now_time == shot_time:
            save_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
            print("shot time:", save_str)
            os.system("raspistill -o " + dir + save_str + ".jpg " +
                      "-rot " + rot +
                      " -sa " + sa +
                      " -w " + width +
                      " -h " + height)
            shot_time = now_time + interval
