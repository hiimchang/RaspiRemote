#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
mission_basic.py: Example demonstrating basic mission operations including creating, clearing and monitoring missions.

Full documentation is provided at https://dronekit-python.readthedocs.io/en/latest/examples/mission_basic.html
"""
from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil

# Connect to the Vehicle
connection_string = 'udpin:0.0.0.0:14551'
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5


def distance_to_current_waypoint():
    """
    Gets distance in metres to the current waypoint.
    It returns None for the first waypoint (Home location).
    """
    nextwaypoint = vehicle.commands.next
    if nextwaypoint == 0:
        return None
    missionitem = vehicle.commands[nextwaypoint - 1]  # commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat, lon, alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint


def download_mission():
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()  # wait until download is complete.


def readmission(aFileName):
    """
    Load a mission from a file into a list. The mission definition is in the Waypoint file
    format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).
    This function is used by upload_mission().
    """
    print("\nReading mission from file: %s" % aFileName)
    missionlist = []
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i == 0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray = line.split('\t')
                print(linearray)
                # ln_index = int(linearray[0])
                # ln_currentwp = int(linearray[1])
                # ln_frame = int(linearray[2])
                ln_command = int(linearray[3])
                ln_param1 = int(linearray[4])
                ln_param2 = int(linearray[5])
                # ln_param3 = float(linearray[6])
                # ln_param4 = float(linearray[7])
                # ln_param5 = float(linearray[8])
                # ln_param6 = float(linearray[9])
                # ln_param7 = float(linearray[10])
                ln_lat = float(linearray[11])
                ln_lon = float(linearray[12])
                ln_alt = float(linearray[13])
                cmd = Command(0, 0, 0, ln_command, ln_param1, ln_param2, 1, 0,
                              0, 0, 0, ln_lat, ln_lon, ln_alt)
                missionlist.append(cmd)
    return missionlist


def adds_square_mission():
    """
    Adds a takeoff command and four waypoint commands to the current mission.
    The waypoints are positioned to form a square of side length 2*aSize around the specified LocationGlobal (aLocation).

    The function assumes vehicle.commands matches the vehicle mission state
    (you must have called download at least once in the session and after clearing the mission)
    """

    cmds = vehicle.commands

    print(" Clear any existing commands")
    cmds.clear()

    print(" Define/add new commands.")
    cmds.add(
        Command(0, 0, 0, 0, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0,
                0, 0, 41.51555555555556, 2.111388888888889, 118))
    vehicle.home_location = LocationGlobal(41.51555555555556, 2.111388888888889, 118)

    """
    Upload a mission from a file. 
    """
    # Read mission from file
    missionlist = readmission('/home/ubuntu/RaspiRemote/mpmission.txt')
    print("\nUpload mission from a file: %s" % '/home/ubuntu/RaspiRemote/mpmission.txt')

    # Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)

    """
    Upload a mission manually. 
    """
    # for wp in [
    #     Command(0, 0, 0, 0, 16, 1, 1, 0.0, 0.0, 0.0, 0.0, 41.51555555555556, 2.1108333333333333, 117.0),
    #     Command(0, 0, 0, 3, 22, 0, 1, 0.0, 0.0, 0.0, 0.0, 41.515, 2.1102777777777777, 116.0),
    #     Command(0, 0, 0, 3, 16, 0, 1, 0.0, 0.0, 0.0, 0.0, 41.514722222222225, 2.111388888888889, 119.0),
    #     Command(0, 0, 0, 3, 16, 0, 1, 0.0, 0.0, 0.0, 0.0, 41.51416666666667, 2.1119444444444446, 117.0),
    #     Command(0, 0, 0, 3, 16, 0, 1, 0.0, 0.0, 0.0, 0.0, 41.515, 2.111666666666667, 118.0),
    #     Command(0, 0, 0, 3, 16, 0, 1, 0.0, 0.0, 0.0, 0.0, 41.515277777777776, 2.1119444444444446, 122.0),
    #     Command(0, 0, 0, 3, 16, 0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    # ]:
    #     cmds.add(wp)
    print(" Upload new commands to vehicle")
    cmds.upload()

    # Add new commands. The meaning/order of the parameters is documented in the Command class.

    # Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
    # cmds.add(
    #     Command(0, 0, 0, 0, 41.51555555555556, 2.111388888888889, 118, 0, 0,
    #             0, 0, 0, 0, 10))

    # Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands

    # cmds.add(
    #     Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0,
    #             0, 0, 0, point1.lat, point1.lon, 11))
    # cmds.add(
    #     Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0,
    #             0, 0, 0, point2.lat, point2.lon, 12))
    # cmds.add(
    #     Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0,
    #             0, 0, 0, point3.lat, point3.lon, 13))
    # cmds.add(
    #     Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0,
    #             0, 0, 0, point4.lat, point4.lon, 14))
    # cmds.add(
    #     Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0,
    #             0, 0, 0, point4.lat, point4.lon, 15))


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(30)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= 30 * 0.95:  # Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)


print('Create a new mission (for current location)')
adds_square_mission()

# From Copter 3.3 you will be able to take off using a mission item. Plane must take off using a mission item (currently).
arm_and_takeoff(10)

print("Starting mission")
# Reset mission set to first (0) waypoint
vehicle.commands.next = 0

# Set mode to AUTO to start mission
vehicle.mode = VehicleMode("AUTO")

# Monitor mission.
# Demonstrates getting and setting the command number
# Uses distance_to_current_waypoint(), a convenience function for finding the
#   distance to the next waypoint.

while True:
    nextwaypoint = vehicle.commands.next
    print('Distance to waypoint (%s): %s' % (nextwaypoint, distance_to_current_waypoint()))
    print(" Battery: %s" % vehicle.battery)

    # if nextwaypoint == 3:  # Skip to next waypoint
    #     print('Skipping to Waypoint 5 when reach waypoint 3')
    #     vehicle.commands.next = 5
    if nextwaypoint == 7:  # Dummy waypoint - as soon as we reach waypoint 4 this is true and we exit.
        print("Exit 'standard' mission when start heading to final dummy waypoint (7)")
        break
    time.sleep(1)

print('Return to launch')
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
