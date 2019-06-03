#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import json
import paho.mqtt.client as mqtt
import time
import yaml
import numpy as np
from multiprocessing import Process, Value
from parts.actuator import PCA9685, PWMSteering, PWMThrottle


class MPMQTTReceiver():
    def __init__(self, host='localhost', port=1883, keepalive=60):
        self.time = Value(ctypes.c_int, 0)
        self.throttle = Value(ctypes.c_float, 0.0)
        self.steering = Value(ctypes.c_float, 0.0)
        self.is_run = Value(ctypes.c_bool, True)

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(host, port, keepalive)

        self._p = Process(target=self._process, args=())
        self._p.start()
        return

    def close(self):
        self.is_run.value = False
        self._p.join()

    def _on_connect(self, client, userdata, flags, rc, topic='mqtt/sensor'):
        self._client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        driver_msg = json.loads(msg.payload.decode('utf-8'))
        self.time.value = driver_msg['time']
        self.throttle.value = driver_msg['throttle']
        self.steering.value = driver_msg['steering']

    def _process(self):
        self._client.loop_start()
        while self.is_run.value:
            time.sleep(0.01)
        self._client.loop_stop()


class RCController():
    def __init__(self, throttle_id=0, steering_id=1):
        self.throt = PWMThrottle(PCA9685(throttle_id))
        self.steer = PWMSteering(PCA9685(steering_id))
        self.throt_limit = [-1.0, 1.0]
        self.steer_limit = [-1.0, 1.0]
        self.throt_direction = -1
        self.steer_direction = -1
        return

    def set_value(self, value, mode='steer'):
        if mode == 'throt':
            controller = self.throt
            limit = self.throt_limit
            direction = self.throt_direction
        elif mode == 'steer':
            controller = self.steer
            limit = self.steer_limit
            direction = self.steer_direction
        output_value = np.clip(value, limit[0], limit[1])
        controller.run(output_value * direction)
        return output_value

    def shutdown(self):
        self.throt.shutdown()
        self.steer.shutdown()
        return


def main():
    ymlfile = open('config.yml')
    cfg = yaml.load(ymlfile)
    ymlfile.close()

    mp_receiver = MPMQTTReceiver(host=cfg['pi_ip'])
    controller = RCController()

    while True:
        throttle_value = mp_receiver.throttle.value
        steering_value = mp_receiver.steering.value

        time_diff_sec = abs(mp_receiver.time.value - time.time())
        if time_diff_sec > 1.0:
            throttle_value = 0
            steering_value = 0

        throttle_output = controller.set_value(throttle_value, mode='throt')
        steering_output = controller.set_value(steering_value, mode='steer')

        print('Time diff: {}, Throttle: {}, Steering: {}'.format(time_diff_sec, throttle_output, steering_output))
        time.sleep(0.01)

    controller.shutdown()
    mp_receiver.close()


if __name__ == '__main__':
    main()
