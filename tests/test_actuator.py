#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest
from setup import on_pi

import sys, os
sys.path.append(os.path.join(os.path.dirname('__file__'), '../'))
from parts.actuator import PCA9685, PWMSteering, PWMThrottle


@pytest.mark.skipif(on_pi() == False, reason='Not on RPi')
def test_PCA9685():
    c = PCA9685(0)

@pytest.mark.skipif(on_pi() == False, reason='Not on RPi')
def test_PWMSteering():
    c = PCA9685(0)
    s = PWMSteering(c)

