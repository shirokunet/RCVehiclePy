
import ctypes
from multiprocessing import Process, Value
from pynput import keyboard
from time import sleep

from parts.actuator import PCA9685, PWMSteering, PWMThrottle


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
            sleep(0.01)
        key_listener.stop()


class RCController():
    def __init__(self, throttle_id=0, steering_id=1):
        self.throt = PWMThrottle(PCA9685(throttle_id))
        self.steer = PWMSteering(PCA9685(steering_id))
        self.throt_test_rate = 0.3
        self.steer_test_rate = 1.0
        self.throt_direction = -1
        self.steer_direction = -1
        return

    def set_value(self, value, mode='steer'):
        if mode == 'throt':
            controller = self.throt
            rate = self.throt_test_rate
            direction = self.throt_direction
        elif mode == 'steer':
            controller = self.steer
            rate = self.steer_test_rate
            direction = self.steer_direction    
        value = value * rate
        controller.run(value * direction)
        return

    def shutdown(self):
        self.throt.shutdown()
        self.steer.shutdown()
        return


def main():
    mp_driver = MPDriverInput()
    controller = RCController()

    print('Press esc to exit')

    while mp_driver.is_run.value:
        controller.set_value(mp_driver.throttle.value, mode='throt')
        controller.set_value(mp_driver.steering.value, mode='steer')

        print('Throttle: {}, Steering: {}'.format(mp_driver.throttle.value, mp_driver.steering.value))
        sleep(0.01)

    mp_driver.close()


if __name__ == '__main__':
    main()
