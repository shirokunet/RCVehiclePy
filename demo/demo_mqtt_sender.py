#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import paho.mqtt.client as mqtt

host = '10.0.0.88'
port = 1883
keepalive = 60
topic = 'mqtt/sensor'

client = mqtt.Client()
client.connect(host, port, keepalive)


while True:
    client.publish(topic, 'Hello')
    time.sleep(1)

client.disconnect()
