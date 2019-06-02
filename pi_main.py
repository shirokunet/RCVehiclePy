#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt


def main():
    host = '10.0.0.88'
    port = 1883
    keepalive = 60
    topic = 'mqtt/sensor'

    def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        throttle_value = str(msg.payload).split(',')[0]
        steerring_value = str(msg.payload).split(',')[1]
        print(msg.topic, throttle_value, steerring_value)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, keepalive)

    client.loop_forever()


if __name__ == '__main__':
    main()
