import paho.mqtt.client as mqtt
import sys
import random
import time
import json
import tago
import numpy as np
# Definitions
# put here your device token
import repackage
repackage.up()
device_token = 'cc8d3e6a-eab9-4b3f-8cf7-3a0cb850f50d'

broker = "mqtt.tago.io"
broker_port = 1883
mqtt_keep_alive = 60

# MQTT publish topic must be tago/data/post
mqtt_publish_topic = "tago/data/post"

# put any name here, TagoIO doesn't validate this username.
mqtt_username = 'eduardoalexandree.ps@gmail.com'

# MQTT password must be the device token (TagoIO does validate this password)
mqtt_password = device_token

# Callback - MQTT broker connection is on

env1, env2, env3 = random.randint(15, 28), [random.randint(15, 28)], [
    random.randint(15, 28)]


def on_connect(client, userdata, flags, rc):
    print("[STATUS] Connected to MQTT broker. Result: " + str(rc))


# Main program
print("[STATUS] Initializing MQTT...")
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.connect(broker, broker_port, mqtt_keep_alive)
timeCount = 0
iteration = 1
while True:

    print(f"Iteração: {iteration}")
    lst = []
    if timeCount == 10:
        lst = np.array(lst)
    temperature_json = {"variable": "temperature",
                        "unit": "F", "value": env1}
    temperature_json_string = json.dumps(temperature_json)
    client.publish(mqtt_publish_topic, temperature_json_string)
    timeCount = 0
    env1 = (random.randint(15, 28))
    env2.append(random.randint(15, 28))
    env3.append(random.randint(15, 28))
    lst = [env1, env2, env3]
    timeCount += 1
    iteration += 1
    time.sleep(2)

print("Data sent to TagoIO platform")