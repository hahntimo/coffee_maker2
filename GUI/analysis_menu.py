import tkinter as tk
from tkinter import ttk, messagebox
import json

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
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.menu_label = ttk.Label(self, text="Punpe")
        self.menu_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        self.frame = ttk.Frame(self)
        self.frame.grid(row=1, column=0, sticky="news", padx=7, pady=7)
        self.frame.rowconfigure((0, 1, 2), weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=2, column=0, columnspan=2, sticky="wes", padx=5, pady=5)

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
                                            variable=self.slider_value,
                                            command=lambda _: self.change_switch_state(self.slider_value.get()))
        self.calibration_slider.grid(row=1, column=0, columnspan=3, sticky="we", padx=7, pady=7)

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
        self.status_string = tk.StringVar(self, "Stop")
        self.status_label = ttk.Label(self.frame, font=glob_style.label_style_big,
                                      background=glob_style.background_color_frame,
                                      textvariable=self.status_string)
        self.status_label.grid(row=0, column=0, sticky="ns", padx=7, pady=7)

        self.slider = ttk.Scale(self.frame, from_=-40, to=40, variable=self.revolution_var,
                                command=self.change_revolution)
        self.slider.grid(row=1, column=0, sticky="we", padx=7, pady=7)

        self.calibration_button = ttk.Button(self.frame, text="Kalibrierung")
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
            self.status_string.set("stop")

        glob_var.spinner_task_queue.put(("change_parameters", revolution))

    def return_menu(self):
        glob_var.test_frame.deiconify()
        self.withdraw()