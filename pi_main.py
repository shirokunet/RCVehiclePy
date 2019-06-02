#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import json
import paho.mqtt.client as mqtt
import time
from multiprocessing import Process, Value
from parts.actuator import PCA9685, PWMSteering, PWMThrottle


class MPMQTTReceiver():
    def __init__(self):
        self.throttle = Value(ctypes.c_float,0.0)
        self.steering = Value(ctypes.c_float,0.0)
        self.is_run = Value(ctypes.c_bool,True)

        self._set_mqtt()
        self._p = Process(target=self._process, args=())
        self._p.start()
        return

    def close(self):
        self.is_run.value = False
        self._p.join()

    def _set_mqtt(self, host='10.0.0.88', port=1883, keepalive=60):
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(host, port, keepalive)

    def _on_connect(self, client, userdata, flags, rc, topic='mqtt/sensor'):
        self._client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        driver_msg = json.loads(msg.payload.decode('utf-8'))
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
        self.throt_limit = [-0.8, 0.3]
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
        controller.run(np.clip(value * direction, limit[0], limit[1]))
        return

    def shutdown(self):
        self.throt.shutdown()
        self.steer.shutdown()
        return


def main():
    mp_receiver = MPMQTTReceiver()
    controller = RCController()

    while True:
        controller.set_value(mp_receiver.throttle.value, mode='throt')
        controller.set_value(mp_receiver.steering.value, mode='steer')
        print('Throttle: {}, Steering: {}'.format(mp_receiver.throttle.value, \
                mp_receiver.steering.value))
        time.sleep(0.01)

    controller.shutdown()
    mp_receiver.close()


if __name__ == '__main__':
    main()
