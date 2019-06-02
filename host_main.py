#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import paho.mqtt.client as mqtt
import time
from multiprocessing import Process, Value
from pynput import keyboard


class MPDriverInput():
    def __init__(self):
        self.throttle = Value(ctypes.c_float,0.0)
        self.steering = Value(ctypes.c_float,0.0)
        self.is_run = Value(ctypes.c_bool,True)

        self._p = Process(target=self._process, args=(10,))
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

    def _process(self, num):
        key_listener = keyboard.Listener(on_press=self._on_press, \
                                         on_release=self._on_release)
        key_listener.start()
        while self.is_run.value:
            time.sleep(0.01)
        key_listener.stop()


def main():
    ### MQTT Setting ###
    host = '10.0.0.88'
    port = 1883
    keepalive = 60
    topic = 'mqtt/sensor'
    client = mqtt.Client()
    client.connect(host, port, keepalive)

    mp_driver = MPDriverInput()

    print('Press esc to exit:')

    while mp_driver.is_run.value:
        client.publish(topic, str(float(mp_driver.throttle.value)) \
                            + ','+ str(float(mp_driver.steering.value)))

        print('Throttle: {}, Steering: {}'.format(mp_driver.throttle.value, \
                                                  mp_driver.steering.value))
        time.sleep(0.01)

    mp_driver.close()
    client.disconnect()


if __name__ == '__main__':
    main()
