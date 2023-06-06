import json
import paho.mqtt.client as mqtt


broker_address = "localhost"
broker_port = 1883

client = mqtt.Client("On board controller")
client.connect(broker_address, broker_port)

wp = {
    'lat': 41.345,
    'lon': 1.342,
    'takePic': True
}
wp_json = json.dumps(wp)
client.publish("wp", wp_json)
client.loop_forever()
