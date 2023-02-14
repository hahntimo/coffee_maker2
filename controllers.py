import multiprocessing
import RPi.GPIO as GPIO
import time
import threading

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
                self.prev_state = new_angle
                angle_signal = (new_angle / 18) + 2
                GPIO.output(glob_var.PIN_SWITCH_SERVO, True)
                self.servo.ChangeDutyCycle(angle_signal)
                time.sleep(0.5)
                GPIO.output(glob_var.PIN_SWITCH_SERVO, False)
                self.servo.ChangeDutyCycle(0)


class SpinnerController(multiprocessing.Process):
    def __init__(self, task_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.output_queue = output_queue

        self.revolution = 0
        self.direction = 1
        self.running = False
        self.theoretical_delay = 0  # theoretical pause between steps
        self.runtime_delay = 0  # delay occurring through runtime delay
        self.actual_delay = 0  # self.theoretical_delay - self.runtime_delay
        self.spr = 6400 * 2  # steps per revolution
        """
        self.DIR_PIN = 19
        self.STEP_PIN = 26
        self.MOTOR_PIN_1 = 16
        self.MOTOR_PIN_2 = 20
        self.MOTOR_PIN_3 = 21"""

    def run(self):
        self.set_pins()
        threading.Thread(target=self.handler).start()

        while True:
            new_task, data = self.task_queue.get()

            if new_task == "change_parameters":
                self.change_parameters(new_revolution=data)
            elif new_task == "calibrate":
                self.calibrate()

    def set_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(glob_var.PIN_SPINNER_DIRECTION, GPIO.OUT)
        GPIO.setup(glob_var.PIN_SPINNER_STEP, GPIO.OUT)

        GPIO.setup((glob_var.PIN_SPINNER_MOTOR_1,
                    glob_var.PIN_SPINNER_MOTOR_2,
                    glob_var.PIN_SPINNER_MOTOR_3), GPIO.OUT)
        GPIO.output((glob_var.PIN_SPINNER_MOTOR_1,
                    glob_var.PIN_SPINNER_MOTOR_2,
                    glob_var.PIN_SPINNER_MOTOR_3), (1, 0, 1))

    def calibrate(self):
        global spinner_calibration_diff

        def test_run():
            global spinner_calibration_diff
            start_time = time.time()
            for step in range(test_steps):
                GPIO.output(glob_var.PIN_SPINNER_STEP, GPIO.HIGH)
                GPIO.output(glob_var.PIN_SPINNER_STEP, GPIO.LOW)
            end_time = time.time()
            spinner_calibration_diff = end_time - start_time

        test_steps = 1000

        self.running = False

        test_thread = threading.Thread(target=test_run)
        test_thread.start()
        test_thread.join()

        while spinner_calibration_diff is None:
            time.sleep(0.1)

        print("DIFF FROM THREAD:", spinner_calibration_diff)
        delay_per_substep = spinner_calibration_diff / (test_steps * 2)

        self.runtime_delay = delay_per_substep
        spinner_calibration_diff = None
        self.output_queue.put(("calibration_done", self.runtime_delay))

    def change_parameters(self, new_revolution):
        self.revolution = abs(new_revolution)
        self.running = True if self.revolution != 0 else False
        self.direction = 0 if new_revolution > 0 else 1

        if new_revolution == 0:
            self.running = False

        elif new_revolution > 0:
            self.running = False
            self.direction = 0
            GPIO.output(glob_var.PIN_SPINNER_DIRECTION, self.direction)
            self.actual_delay = (60 / (self.revolution * self.spr)) - self.runtime_delay
            if self.actual_delay < 0:
                self.actual_delay = 0
            self.running = True

        elif new_revolution < 0:
            self.running = False
            self.direction = 1
            GPIO.output(glob_var.PIN_SPINNER_DIRECTION, self.direction)
            self.actual_delay = (60 / (self.revolution * self.spr)) - self.runtime_delay
            if self.actual_delay < 0:
                self.actual_delay = 0
            self.running = True

    def handler(self):
        while True:
            if self.running:
                GPIO.output(glob_var.PIN_SPINNER_STEP, GPIO.HIGH)
                time.sleep(self.actual_delay)
                GPIO.output(glob_var.PIN_SPINNER_STEP, GPIO.LOW)
                time.sleep(self.actual_delay)

    def cleanup(self):
        GPIO.cleanup()
        print("CLEANUP SUCCESS")

