#!/usr/bin/python3
# -*- coding: utf-8 -*-

import platform


def on_pi():
    if 'arm' in platform.machine():
        return True
    return False
