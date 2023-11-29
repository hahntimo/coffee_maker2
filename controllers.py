"""Includes subprocesses to control motors, sensors and relays. Package gets imported by main.py
only in productive mode"""

import multiprocessing
import RPi.GPIO as GPIO
import time
import threading
from w1thermsensor import W1ThermSensor

import glob_var

GPIO.setwarnings(False)


class RelayController(multiprocessing.Process):
    """Control status of relays for valves and heating element"""
    def __init__(self, mp_data):
        multiprocessing.Process.__init__(self)
        self.mp_data = mp_data
        self.brewer_valve_relay_state = True
        self.heater_valve_relay_state = True
        self.heater_relay_state = True

    def set_pins(self):
        """Configure pins of raspberry pi and set them to default values"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(glob_var.PIN_HEATER_VALVE_RELAY, GPIO.OUT)
        GPIO.setup(glob_var.PIN_BREWER_VALVE_RELAY, GPIO.OUT)
        GPIO.setup(glob_var.PIN_HEATER_RELAY, GPIO.OUT)

        GPIO.output(glob_var.PIN_HEATER_VALVE_RELAY, self.heater_valve_relay_state)
        GPIO.output(glob_var.PIN_BREWER_VALVE_RELAY, self.brewer_valve_relay_state)
        GPIO.output(glob_var.PIN_HEATER_RELAY, self.heater_relay_state)

    def run(self):
        """Start process (overwrites inherited method). Within an infinite while-loop the process
        checks for changes in the multiprocessing manager dictionary and sets the respective relay
        to the new state."""
        self.set_pins()
        while True:
            """heater valve relay"""
            if self.mp_data["heater_valve"] != self.heater_valve_relay_state:
                GPIO.output(glob_var.PIN_HEATER_VALVE_RELAY, self.mp_data["heater_valve"])
                self.heater_valve_relay_state = self.mp_data["heater_valve"]

            """brewer valve relay"""
            if self.mp_data["brewer_valve"] != self.brewer_valve_relay_state:
                GPIO.output(glob_var.PIN_BREWER_VALVE_RELAY, self.mp_data["brewer_valve"])
                self.brewer_valve_relay_state = self.mp_data["brewer_valve"]

            """heater relay"""
            if self.mp_data["heater"] != self.heater_relay_state:
                GPIO.output(glob_var.PIN_HEATER_RELAY, self.mp_data["heater"])
                self.heater_relay_state = self.mp_data["heater"]


class SpinnerController(multiprocessing.Process):
    def __init__(self, task_queue, output_queue, runtime_delay):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.output_queue = output_queue

        self.revolution = 0
        self.direction = 1
        self.running = False
        self.theoretical_delay = 0  # theoretical pause between steps
        self.runtime_delay = runtime_delay # delay occurring through runtime delay
        self.actual_delay = 0  # self.theoretical_delay - self.runtime_delay
        self.spr = 6400 * 2  # steps per revolution

    def run(self):
        """Start process (overwrites inherited method)"""
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


class PumpController(multiprocessing.Process):
    def __init__(self, task_queue, process_data, relay_mp_data, config_json):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.process_data = process_data
        self.relay_mp_data = relay_mp_data

        self.revolution = 0
        self.direction = 0

        self.theoretical_delay = 0  # theoretical pause between steps
        self.runtime_delay = config_json["calibration"]["pump_step_delay"]  # delay occurring through runtime delay
        self.actual_delay = 0  # self.theoretical_delay - self.runtime_delay
        self.spr = 4000 * 2  # steps per revolution

        self.ml_per_revolution = config_json["calibration"]["pump_ml_per_revolution"]
        self.volume_calibration_target_steps = 100000
        self.task_target_steps = 0

        self.config_json = config_json
        self.speed_tuple = None

    def run(self):
        self.set_pins()
        threading.Thread(target=self.handler).start()

        while True:
            task_dict = self.task_queue.get()
            if task_dict["task"] == "volume_over_time":
                volume_in_ml = task_dict["volume"]
                time_in_seconds = task_dict["time"]

                self.actual_delay = 1 / self.spr
                self.task_target_steps = int((volume_in_ml / self.ml_per_revolution) * (self.spr / 2))
                self.actual_delay = time_in_seconds/(self.task_target_steps * 2)
                self.process_data["target_steps"] = self.task_target_steps

            elif task_dict["task"] == "step_delay_calibration":
                pass

            elif task_dict["task"] == "volume_revolution_calibration":
                self.relay_mp_data["brewer_valve"] = True
                self.relay_mp_data["heater_valve"] = False
                self.actual_delay = 0
                self.task_target_steps = self.volume_calibration_target_steps
                self.process_data["target_steps"] = self.task_target_steps

            elif task_dict["task"] == "stop":
                self.task_target_steps = 0
                self.process_data["remaining_steps"] = 0

    def set_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(glob_var.PIN_PUMP_DIRECTION, GPIO.OUT)
        GPIO.setup(glob_var.PIN_PUMP_STEP, GPIO.OUT)
        GPIO.output(glob_var.PIN_PUMP_DIRECTION, self.direction)
        GPIO.setup((glob_var.PIN_PUMP_MOTOR_1, glob_var.PIN_PUMP_MOTOR_2, glob_var.PIN_PUMP_MOTOR_3), GPIO.OUT)
        GPIO.output((glob_var.PIN_PUMP_MOTOR_1, glob_var.PIN_PUMP_MOTOR_2, glob_var.PIN_PUMP_MOTOR_3), (1, 0, 1))

    def set_speed(self):
        pass

    def handler(self):
        while True:
            self.process_data["remaining_steps"] = self.task_target_steps
            if self.task_target_steps != 0:
                self.task_target_steps -= 1
                GPIO.output(glob_var.PIN_PUMP_STEP, GPIO.HIGH)
                time.sleep(self.actual_delay)
                GPIO.output(glob_var.PIN_PUMP_STEP, GPIO.LOW)
                time.sleep(self.actual_delay)


class HeaterController(multiprocessing.Process):
    def __init__(self, relay_mp_data, pump_mp_data, heater_mp_data):
        multiprocessing.Process.__init__(self)

        self.relay_mp_data = relay_mp_data
        self.pump_mp_data = pump_mp_data
        self.heater_mp_data = heater_mp_data

        self.sensor = W1ThermSensor()

    def run(self):
        threading.Thread(target=self.handler).start()
        while True:
            self.heater_mp_data["current_temp"] = self.sensor.get_temperature()

    def handler(self):
        pass


class BrewingProcess(multiprocessing.Process):
    def __init__(self, relay_mp_data, pump_mp_data, heater_mp_data, spinner_mp_data):
        multiprocessing.Process.__init__(self)

        self.relay_mp_data = relay_mp_data
        self.pump_mp_data = pump_mp_data
        self.heater_mp_data = heater_mp_data
        self.spinner_mp_data = spinner_mp_data
