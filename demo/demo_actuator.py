#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import time

import sys, os
sys.path.append(os.path.join(os.path.dirname('__file__'), '..'))
from parts.actuator import PCA9685, PWMSteering, PWMThrottle


class ControlTest():
    def __init__(self, throttle_id=0, steering_id=1):
        self.throt = PWMThrottle(PCA9685(throttle_id))
        self.steer = PWMSteering(PCA9685(steering_id))
        self.throt_test_rate = 0.3
        self.steer_test_rate = 1.0
        self.throt_direction = -1
        self.steer_direction = -1
        self.loop_interval = 0.05
        return

    def test_loop(self, mode='steer'):
        if mode == 'throt':
            controller = self.throt
            rate = self.throt_test_rate
            direction = self.throt_direction
            test_array = np.concatenate([np.arange(0.0, 1.0, 0.01), \
                                         np.arange(1.0, 0.0, -0.01)])
        elif mode == 'steer':
            controller = self.steer
            rate = self.steer_test_rate
            direction = self.steer_direction
            test_array = np.concatenate([np.arange(0.0, -1.0, -0.01), \
                                         np.arange(-1.0, 1.0, 0.01), \
                                         np.arange(1.0, 0.0, -0.01)])
    
        for i in range(len(test_array)):
            value = test_array[i] * rate
            controller.run(value * direction)
            print(mode, value)
            time.sleep(self.loop_interval)

        controller.run(0)

        return

    def shutdown(self):
        self.throt.shutdown()
        self.steer.shutdown()
        return


def main():
    ct = ControlTest()
    ct.test_loop(mode='throt')
    ct.test_loop(mode='steer')
    ct.shutdown()
    return


if __name__ == '__main__':
    main()
