#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import json
import paho.mqtt.client as mqtt
import time
import yaml
from multiprocessing import Process, Value
from pynput import keyboard


class MQTTSender():
    def __init__(self, host='10.0.0.88', port=1883, keepalive=60):
        self._client = mqtt.Client()
        self._client.connect(host, port, keepalive)
        return

    def disconnect(self):
        self._client.disconnect()
        return

    def publish(self, driver_msg, topic='mqtt/sensor'):
        self._client.publish(topic, json.dumps(driver_msg))
        return


class MPDriverInput():
    def __init__(self):
        self.throttle = Value(ctypes.c_float,0.0)
        self.steering = Value(ctypes.c_float,0.0)
        self.is_run = Value(ctypes.c_bool,True)

        self._p = Process(target=self._process, args=())
        self._p.start()
        return

    def close(self):
        self.is_run.value = False
        self._p.join()

    def _on_press(self, key):
        if key == keyboard.Key.esc:
            self.is_run.value = False
        elif key == keyboard.Key.up:
            self.throttle.value = 1.0
        elif key == keyboard.Key.down:
            self.throttle.value = -1.0
        elif key == keyboard.Key.left:
            self.steering.value = -1.0
        elif key == keyboard.Key.right:
            self.steering.value = 1.0

    def _on_release(self, key):
        if key == keyboard.Key.up or key == keyboard.Key.down:
            self.throttle.value = 0.0
        elif key == keyboard.Key.left or key == keyboard.Key.right:
            self.steering.value = 0.0

    def _process(self):
        key_listener = keyboard.Listener(on_press=self._on_press, \
                                         on_release=self._on_release)
        key_listener.start()
        while self.is_run.value:
            time.sleep(0.01)
        key_listener.stop()


def main():
    ymlfile = open('config.yml')
    cfg = yaml.load(ymlfile)
    ymlfile.close()

    sender = MQTTSender(host=cfg['pc_ip'])
    mp_driver = MPDriverInput()

    driver_msg = {
        'throttle': 0.0,
        'steering': 0.0
    }

    print('Press esc to exit:')
    while mp_driver.is_run.value:
        driver_msg['throttle'] = mp_driver.throttle.value
        driver_msg['steering'] = mp_driver.steering.value
        sender.publish(json.dumps(driver_msg))
        print('Throttle: {}, Steering: {}'.format(driver_msg['throttle'], driver_msg['steering']))
        time.sleep(0.01)

    mp_driver.close()
    sender.disconnect()


if __name__ == '__main__':
    main()
