import platform


def on_pi():
    if 'arm' in platform.machine():
        return True
    return False
