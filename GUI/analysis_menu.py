import tkinter as tk
from tkinter import ttk, messagebox
import json
import time

from GUI import helper, glob_style
import glob_var


class TestMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.menu_label = ttk.Label(self, text="Testfunktionen")
        self.menu_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        self.frame = ttk.Frame(self)
        self.frame.grid(row=1, column=0, sticky="news", padx=7, pady=7)
        self.frame.rowconfigure((0, 1), weight=1)
        self.frame.columnconfigure((0, 1), weight=1)

        self.pump_icon = tk.PhotoImage(file="assets/icons/pump.png")
        self.start_pump_menu_button = ttk.Button(self.frame, text="Pumpe", image=self.pump_icon,
                                                 compound="top", command=self.start_pump_menu)
        self.start_pump_menu_button.grid(row=0, column=0, sticky="news", padx=7, pady=7)

        self.heater_icon = tk.PhotoImage(file="assets/icons/heater.png")
        self.start_heater_menu_button = ttk.Button(self.frame, text="Heizelement",
                                                   image=self.heater_icon, compound="top",
                                                   command=self.start_heater_menu)
        self.start_heater_menu_button.grid(row=0, column=1, sticky="news", padx=7, pady=7)

        self.spinner_icon = tk.PhotoImage(file="assets/icons/spinner.png")
        self.start_can_spinner_menu_button = ttk.Button(self.frame, text="Drehteller",
                                                        image=self.spinner_icon, compound="top",
                                                        command=self.start_can_spinner_menu)
        self.start_can_spinner_menu_button.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.switch_icon = tk.PhotoImage(file="assets/icons/switch.png")
        self.start_switch_menu_button = ttk.Button(self.frame, text="Wasserweiche",
                                                   image=self.switch_icon, compound="top",
                                                   command=self.start_switch_menu)
        self.start_switch_menu_button.grid(row=1, column=1, sticky="news", padx=7, pady=7)

        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=2, column=0, columnspan=2, sticky="wes", padx=5, pady=5)

    def start_pump_menu(self):
        if glob_var.pump_menu_frame is None:
            glob_var.pump_menu_frame = PumpMenu(self.prod_mode)
        else:
            glob_var.pump_menu_frame.deiconify()

    def start_heater_menu(self):
        pass

    def start_can_spinner_menu(self):
        if glob_var.can_spinner_menu_frame is None:
            glob_var.can_spinner_menu_frame = SpinnerMenu(self.prod_mode)
        else:
            glob_var.can_spinner_menu_frame.deiconify()

    def start_switch_menu(self):
        if glob_var.switch_menu_frame is None:
            glob_var.switch_menu_frame = SwitchMenu(self.prod_mode)
        else:
            glob_var.switch_menu_frame.deiconify()

    def return_menu(self):
        glob_var.main_menu_frame.deiconify()
        self.withdraw()


class PumpMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)
        self.current_tab = None
        self.pump_running = False

        self.rowconfigure((1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        self.menu_label = ttk.Label(self, text="Pumpe")
        self.menu_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        # --- control tabs ---
        self.tabs = ttk.Notebook(self)
        self.tab_flow_speed = ttk.Frame(self.tabs)
        self.tab_time_volume = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_flow_speed, text="Flußgeschwindigkeit")
        self.tabs.add(self.tab_time_volume, text="Dosierung")
        self.tabs.grid(row=1, column=0, sticky="news", padx=7, pady=7)
        self.tabs.bind('<<NotebookTabChanged>>', lambda _: self.tab_change())

        # tab flow speed
        self.tab_flow_speed.rowconfigure((0, 1), weight=1)
        self.tab_flow_speed.columnconfigure(0, weight=1)

        self.flow_rate = tk.IntVar(self, 0)
        self.flow_rate_string = tk.StringVar(self, "STOP")

        self.flow_rate_label = ttk.Label(self.tab_flow_speed, textvariable=self.flow_rate_string,
                                         font=glob_style.label_style_big,
                                         background=glob_style.background_color_frame)
        self.flow_rate_label.grid(row=0, column=0, padx=7, pady=7)

        self.flow_rate_slider = ttk.Scale(self.tab_flow_speed, variable=self.flow_rate,
                                          from_=0, to=300, command=self.change_flow_rate)
        self.flow_rate_slider.grid(row=1, column=0, sticky="we", padx=7, pady=7)

        # tab time flow
        self.tab_time_volume.rowconfigure((0, 1, 2, 3), weight=1)
        self.tab_time_volume.columnconfigure((0, 1), weight=1)

        self.volume_label = ttk.Label(self.tab_time_volume, text="Volumen (ml)",
                                      font=glob_style.label_style_medium,
                                      background=glob_style.background_color_frame)
        self.volume_label.grid(row=0, column=0, sticky="e", padx=7, pady=7)
        self.volume_entry = ttk.Entry(self.tab_time_volume, font=glob_style.label_style_medium)
        self.volume_entry.grid(row=0, column=1, padx=7, pady=7)
        self.volume_entry.bind("<Button-1>",
                               lambda _: helper.NumPad(prod_mode=self.prod_mode,
                                                       input_field=self.volume_entry,
                                                       input_type="float",
                                                       info_message="Volumen in Milliliter"))

        self.time_span_label = ttk.Label(self.tab_time_volume, text="Zeitraum (min.)",
                                         font=glob_style.label_style_medium,
                                         background=glob_style.background_color_frame)
        self.time_span_label.grid(row=1, column=0, sticky="e", padx=7, pady=7)
        self.time_span_entry = ttk.Entry(self.tab_time_volume, font=glob_style.label_style_medium)
        self.time_span_entry.grid(row=1, column=1, padx=7, pady=7)
        self.time_span_entry.bind("<Button-1>",
                                  lambda _: helper.NumPad(prod_mode=self.prod_mode,
                                                          input_field=self.time_span_entry,
                                                          input_type="time",
                                                          info_message="Zeitraum in Minuten"))

        self.progress_bar_status = tk.DoubleVar(self, 0)
        self.progress_bar = ttk.Progressbar(self.tab_time_volume, maximum=100)
        self.progress_bar.grid(row=2, column=0, columnspan=2, sticky="we", padx=7, pady=7)

        self.start_stop_button = ttk.Button(self.tab_time_volume, text="start",
                                            command=self.start_stop_time_volume)
        self.start_stop_button.grid(row=3, column=0, columnspan=2, padx=7, pady=7)

        # --- calibration frame ---
        self.calibration_frame = ttk.Frame(self)
        self.calibration_frame.grid(row=2, column=0, sticky="news", padx=7, pady=7)
        self.calibration_frame.rowconfigure(0, weight=1)
        self.calibration_frame.columnconfigure((0, 1), weight=1)

        self.calibrate_step_delay_button = ttk.Button(self.calibration_frame, text="Motor kalibrieren",
                                                      command=self.calibrate_motor_step_delay)
        self.calibrate_step_delay_button.grid(row=0, column=0, sticky="we", padx=7, pady=7)

        self.calibrate_water_flow_button = ttk.Button(self.calibration_frame, text="Flussrate kalibrieren",
                                                      command=self.calibrate_water_flow)
        self.calibrate_water_flow_button.grid(row=0, column=1, sticky="we", padx=7, pady=7)

        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=3, column=0, columnspan=2, sticky="wes", padx=5, pady=5)

    def tab_change(self):
        tab_index = (self.tabs.index(self.tabs.select()))
        if self.current_tab is not None and self.pump_running:
            messagebox.showinfo(message="Pumpe gestoppt")
            self.start_stop_button.configure(text="start")
            self.flow_rate.set(0)
            self.flow_rate_string.set("STOP")
            self.progress_bar_status.set(0)
            self.pump_running = False
        elif self.current_tab is None:
            self.current_tab = tab_index

    def change_flow_rate(self, *args):
        flow_rate = self.flow_rate.get()
        if flow_rate == 0:
            self.pump_running = False
            self.flow_rate_string.set("STOP")
        else:
            self.pump_running = True
            self.flow_rate_string.set(f"{flow_rate} ml/min.")

    def refresh_progress_bar(self):
        target_steps = glob_var.pump_mp_data["target_steps"]
        remaining_steps = glob_var.pump_mp_data["remaining_steps"]
        if remaining_steps != 0:
            percentage = ((target_steps - remaining_steps) / target_steps) * 100
            self.progress_bar_status.set(percentage)
            self.after(500, lambda: self.refresh_progress_bar())
        else:
            self.pump_running = False
            self.start_stop_button.configure(text="start")

    def start_stop_time_volume(self):
        if self.pump_running:
            glob_var.pump_task_queue.put({"task": "stop"})
            self.pump_running = False
            self.start_stop_button.configure(text="start")
        else:
            if self.volume_entry.get() == "" or self.time_span_entry.get() == "":
                messagebox.showwarning(message="Unvollständige Angaben")
            else:
                time_input = self.time_span_entry.get().split(":")
                if len(time_input) == 2:
                    time_in_seconds = (int(time_input[0]) if time_input[0] != "" else 0) * 60 + \
                                      (int(time_input[1]) if time_input[1] != "" else 0)
                else:
                    time_in_seconds = (int(time_input[0]) if time_input[0] != "" else 0) * 60

                volume_in_ml = float(self.volume_entry.get().replace(",", "."))
                task_dict = {"task": "volume_over_time",
                             "volume": volume_in_ml,
                             "time": time_in_seconds}
                glob_var.pump_task_queue.put(task_dict)
                self.pump_running = True
                self.start_stop_button.configure(text="stop")
                self.after(500, self.refresh_progress_bar)


    def calibrate_motor_step_delay(self):
        pass

    def calibrate_water_flow(self):
        pass

    def return_menu(self):
        glob_var.test_frame.deiconify()
        self.withdraw()


class SwitchMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)
        self.rowconfigure((1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        self.menu_label = ttk.Label(self, text="Wassserweiche")
        self.menu_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        # control frame
        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=1, column=0, sticky="news", padx=7, pady=7)
        self.control_frame.rowconfigure(0, weight=1)
        self.control_frame.columnconfigure((0, 1, 2), weight=1)

        self.brew_icon = tk.PhotoImage(file="assets/icons/can.png")
        self.set_brew_state_button = ttk.Button(self.control_frame, text="Brüharm",
                                                image=self.brew_icon, compound="top",
                                                command=lambda: self.change_switch_state(
                                                    glob_var.config_json["calibration"]
                                                    ["servo_angle_brewing"])
                                                )
        self.set_brew_state_button.grid(row=0, column=0, sticky="news", padx=7, pady=7)

        self.heater_icon = tk.PhotoImage(file="assets/icons/heater_small.png")
        self.set_heater_state_button = ttk.Button(self.control_frame, text="Heizelement",
                                                  image=self.heater_icon, compound="top",
                                                  command=lambda: self.change_switch_state(
                                                      glob_var.config_json["calibration"]
                                                      ["servo_angle_heater"]))
        self.set_heater_state_button.grid(row=0, column=2, sticky="news", padx=7, pady=7)

        # calibration frame
        self.calibration_frame = ttk.Frame(self)
        self.calibration_frame.grid(row=2, column=0, sticky="news", padx=7, pady=7)
        self.calibration_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.calibration_frame.columnconfigure((0, 1, 2), weight=1)

        self.calibration_info = tk.StringVar(self, f"Kalibrierung: {glob_var.config_json['calibration']['servo_angle_heater']}°")
        self.calibration_label = ttk.Label(self.calibration_frame, textvariable=self.calibration_info,
                                           font=glob_style.label_style_medium,
                                           background=glob_style.background_color_frame)
        self.calibration_label.grid(row=0, column=0, columnspan=3, padx=7, pady=7)

        self.slider_value = tk.IntVar(self, glob_var.config_json["calibration"]["servo_angle_heater"])
        self.calibration_slider = ttk.Scale(self.calibration_frame, from_=180, to=0,
                                            variable=self.slider_value)
        self.calibration_slider.grid(row=1, column=0, columnspan=3, sticky="we", padx=7, pady=7)
        self.calibration_slider.bind("<ButtonRelease-1>",
                                     lambda _: self.change_switch_state(self.slider_value.get()))

        self.brew_calibration_value = tk.StringVar(self)
        self.brew_calibration_entry = ttk.Entry(self.calibration_frame,
                                                font=glob_style.label_style_medium,
                                                background=glob_style.background_color_frame,
                                                textvariable=self.brew_calibration_value)
        self.brew_calibration_entry.grid(row=2, column=0, padx=7, pady=7)
        self.brew_calibration_entry.bind("<Button-1>",
                                         lambda _: helper.NumPad(prod_mode=self.prod_mode,
                                                                 input_field=self.brew_calibration_entry,
                                                                 input_type="int",
                                                                 info_message="Servo Winkel Brüharm"))

        self.heater_calibration_value = tk.StringVar(self)
        self.heater_calibration_entry = ttk.Entry(self.calibration_frame,
                                                  font=glob_style.label_style_medium,
                                                  background=glob_style.background_color_frame,
                                                  textvariable=self.heater_calibration_value)
        self.heater_calibration_entry.grid(row=2, column=2, padx=7, pady=7)
        self.heater_calibration_entry.bind("<Button-1>",
                                           lambda _: helper.NumPad(prod_mode=self.prod_mode,
                                                                   input_field=self.heater_calibration_entry,
                                                                   input_type="int",
                                                                   info_message="Servo Winkel Heizelement"))

        self.save_calibration_button = ttk.Button(self.calibration_frame, text="speichern",
                                                  command=self.save_calibration)
        self.save_calibration_button.grid(row=3, column=0, columnspan=3, padx=7, pady=7)

        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=3, column=0, columnspan=2, sticky="wes", padx=5, pady=5)

        self.set_calibration_value()

    def change_switch_state(self, servo_target_angle):
        glob_var.switch_mp_data["angle"] = servo_target_angle
        self.slider_value.set(servo_target_angle)
        self.calibration_info.set(f"Kalibrierung: {servo_target_angle}°")

    def save_calibration(self):
        glob_var.config_json["calibration"]["servo_angle_brewing"] = int(self.brew_calibration_value.get())
        glob_var.config_json["calibration"]["servo_angle_heater"] = int(self.heater_calibration_value.get())
        with open("configurations.json", "w") as outfile:
            outfile.write(json.dumps(glob_var.config_json, indent=4))

    def set_calibration_value(self):
        self.brew_calibration_value.set(str(glob_var.config_json["calibration"]["servo_angle_brewing"]))
        self.heater_calibration_value.set(str(glob_var.config_json["calibration"]["servo_angle_heater"]))

    def return_menu(self):
        glob_var.test_frame.deiconify()
        self.withdraw()


class SpinnerMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.menu_label = ttk.Label(self, text="Drehteller")
        self.menu_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        self.frame = ttk.Frame(self)
        self.frame.grid(row=1, column=0, sticky="news", padx=7, pady=7)
        self.frame.rowconfigure((0, 1, 2), weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.revolution_var = tk.IntVar(self, 0)
        self.status_string = tk.StringVar(self, "STOP")
        self.status_label = ttk.Label(self.frame, font=glob_style.label_style_big,
                                      background=glob_style.background_color_frame,
                                      textvariable=self.status_string)
        self.status_label.grid(row=0, column=0, sticky="ns", padx=7, pady=7)

        self.slider = ttk.Scale(self.frame, from_=-40, to=40, variable=self.revolution_var,
                                command=self.change_revolution)
        self.slider.grid(row=1, column=0, sticky="we", padx=7, pady=7)

        self.calibration_button = ttk.Button(self.frame, text="Kalibrierung", command=self.calibrate)
        self.calibration_button.grid(row=2, column=0, sticky="we", padx=7, pady=7)

        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=2, column=0, columnspan=2, sticky="wes", padx=5, pady=5)

    def change_revolution(self, *args):
        revolution = self.revolution_var.get()
        if revolution > 0:
            self.status_string.set(f"{revolution} Umdrehungen/min \u27F3")
        elif revolution < 0:
            self.status_string.set(f"{revolution} Umdrehungen/min \u27F2")
        else:
            self.status_string.set("STOP")

        glob_var.spinner_task_queue.put(("change_parameters", revolution))

    @staticmethod
    def calibrate():
        glob_var.pitcher_spinner_input_queue.put(("calibrate", None))
        while True:
            time.sleep(0.1)
            return_type, data = glob_var.pitcher_spinner_output_queue.get()
            if return_type == "calibration_done":
                glob_var.config_json["calibration"]["spinner_step_delay"] = data
                with open("configurations.json", "w") as outfile:
                    outfile.write(json.dumps(glob_var.config_json, indent=4))
                helper.InfoMessage(title="Kalibrierung", message=f"Delay pro step: {data}")
                break

    def return_menu(self):
        glob_var.test_frame.deiconify()
        self.withdraw()