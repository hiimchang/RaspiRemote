#!/usr/bin/env python

'''
 Useful coordinates for SITL --home=41.275519,1.986601,3,90
'''

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the Vehicle (in this case a simulator running DroneKit-SITL)
connection_string = 'udpin:0.0.0.0:14551'
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

'''
Arming turns on the vehicle`s motors in preparation for flight. The flight
 controller will not arm until the vehicle has passed a series of pre-arm
 checks to ensure that it is safe to fly.
'''


def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


# Execute initialization and take off
arm_and_takeoff(20)
'''
When the function returns, the app can continue in GUIDED mode or switch to AUTO mode to
 start a mission.
 
 * GUIDED mode is the recommended mode for flying Copter autonomously without a predefined a mission.
   It allows a Ground Control Station (GCS) or Companion Computer to control the vehicle "on the fly"
   and react to new events or situations as they occur. Visit:
   http://python.dronekit.io/guide/copter/guided_mode.html
   
 * AUTO mode is used to run pre-defined waypoint missions. Visit:
   http://python.dronekit.io/guide/auto_mode.html
   
 * RTL mode (Return to Launch): To return to the home position and land, we set the mode to RTL. The
   vehicle travels at the previously set default speed
'''

'''
You can set the target movement speed  using Vehicle.airspeed or Vehicle.groundspeed. The speed
 setting will then be used for all positional movement commands until it is set to another value
'''
print("Set default/target airspeed to 3 m/s")
vehicle.airspeed = 8

'''
The recommended method for position control is Vehicle.simple_goto(). This takes a LocationGlobal
 or LocationGlobalRelative argument.
'''
print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(41.51555555555556, 2.111388888888889, 118)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
point2 = LocationGlobalRelative(41.51555555555556, 2.1108333333333333, 117)
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
