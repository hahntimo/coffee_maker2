import multiprocessing
import RPi.GPIO as GPIO
import time

import glob_var


class SwitchController(multiprocessing.Process):
    def __init__(self, mp_data):
        multiprocessing.Process.__init__(self)
        self.mp_data = mp_data
        self.servo = None
        self.prev_state = None

    def set_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(glob_var.PIN_SWITCH_SERVO, GPIO.OUT)
        self.servo = GPIO.PWM(glob_var.PIN_SWITCH_SERVO, 50)
        self.servo.start(0)

    def run(self):
        print("switch process running")
        self.set_pins()
        while True:
            new_angle = self.mp_data["angle"]

            if new_angle != self.prev_state:
                angle_signal = (new_angle / 18) + 2
                print("SET ANGLE:", f"{new_angle}°", angle_signal)

                GPIO.output(glob_var.PIN_SWITCH_SERVO, True)
                self.servo.ChangeDutyCycle(angle_signal)
                time.sleep(1)
                GPIO.output(glob_var.PIN_SWITCH_SERVO, False)
                self.servo.ChangeDutyCycle(0)

