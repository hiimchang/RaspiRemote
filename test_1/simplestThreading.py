import time
import paho.mqtt.client as mqtt

broker_address = "10.4.111.17"
broker_port = 22

client = mqtt.Client("Publisher_1234")
client.connect(broker_address, broker_port)
client.publish('command', 'arm')
time.sleep(5)
client.publish('command', 'takeoff')
print("Goodbye")
