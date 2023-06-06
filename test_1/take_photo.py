# coding=utf-8
import sys
import datetime
import os
import time
import json

def takephoto():
    dir_img = '/home/ubuntu/RaspiRemote/TransversalProject/images/'
    #   definition of parameters, more at https://www.raspberrypi.org/app/uploads/2013/07/RaspiCam-Documentation.pdf
    # rotation
    rot = '180'
    # saturation，-100 - 100
    sa = '30'
    # width
    width = '1920'
    # height
    height = '1080'
    # timeout
    timeout = '1000'
    # ISO
    iso = '100'
    # shutter speed in microseconds
    ss = '10000'  # 1/200 seconds
    save_str = datetime.datetime.strftime(datetime.datetime.now(),
                                          '%Y-%m-%d-%H-%M-%S')
    print('shot time:', save_str)
    os.system('raspistill -o ' + dir_img + save_str + '.jpg ' +
              ' -ISO ' + iso +
              ' -ss ' + ss +
              ' -rot ' + rot +
              ' -sa ' + sa +
              ' -w ' + width +
              ' -h ' + height +
              ' -t ' + timeout)
