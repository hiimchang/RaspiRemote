import json
import sys
import time
import paho.mqtt.client as mqtt
import os

from numpy import random

def readmission(aFileName):
    print("\nReading mission from file: %s" % aFileName)
    missionlist = {'coordinates':[]}
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i == 0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray = line.split('\t')
                ln_lat = float(linearray[8])
                ln_lon = float(linearray[9])
                #ln_alt = float(linearray[10])

                missionlist['coordinates'].append([ln_lat, ln_lon])

    return missionlist


def Dash(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client

    print('Dash ready')
    print('Connection mode: ', connection_mode)
    print('Operation mode: ', operation_mode)
    op_mode = operation_mode

    if connection_mode == 'global':
        external_broker_address = external_broker
    else:
        external_broker_address = 'localhost'

    external_broker_port = 8000
    external_client = mqtt.Client("Dash", transport="websockets")
    if external_broker_address == 'classpip.upc.edu':
        external_client.username_pw_set(username, password)
    external_client.connect(external_broker_address, external_broker_port)

    internal_broker_address = 'localhost'
    internal_broker_port = 1884

    internal_client = mqtt.Client("Dash")
    internal_client.connect(internal_broker_address, internal_broker_port)

    print('Waiting....')
    print('---------')

    external_client.publish('Dash/autopilotService/connect', '')
    time.sleep(10)

    mission = readmission('/home/ubuntu/RaspiRemote/TransversalProject/images/test_3105/1/plan3105_1.waypoints')
    waypoints_json = json.dumps(mission)

    external_client.publish('Dash/autopilotService/executeFlightPlan', waypoints_json)
    # external_client.publish('dash/cameraService/executePicturesPlan', picturepoints_json)

    internal_client.loop_start()
    external_client.loop_forever()


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

    Dash(connection_mode, operation_mode, external_broker, username, password)
