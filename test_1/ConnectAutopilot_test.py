from dronekit import connect
import time

connection_string = "/dev/ttyS0"

vehicle = connect(connection_string, wait_ready=True, baud=
115200)

print("Connected")
print(" Autopilot Firmware version: %s" % vehicle.version)
print(" Global Location: %s" % vehicle.location.global_frame)
print(" Velocity: %s" % vehicle.velocity)
print(" Battery: %s" % vehicle.battery)
print(" Heading: %s" % vehicle.heading)
print(" Is Armable?: %s" % vehicle.is_armable)
vehicle.close()
