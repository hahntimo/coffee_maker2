import tkinter as tk
from tkinter import ttk, messagebox
import json

from GUI import glob_style
import glob_var


class MenuFrame(tk.Toplevel):
    def __init__(self, prod_mode):
        super().__init__()
        self.prod_mode = prod_mode
        self.geometry(glob_style.screen_resolution)
        self.configure(background=glob_style.background_color_master)
        if prod_mode:
            self.attributes('-fullscreen', True)
            self.configure(cursor=glob_style.cursor)


class NumPad(tk.Toplevel):
    def __init__(self, prod_mode, input_field, info_message, input_type="float"):
        super().__init__()
        self.prod_mode = prod_mode
        self.geometry(glob_style.screen_resolution)
        if self.prod_mode:
            self.attributes("-fullscreen", True)
            self.config(cursor=glob_style.cursor)

        self.input_field = input_field
        self.info_message = info_message
        self.input_type = input_type

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.info_message_label = ttk.Label(self, text=self.info_message,
                                            font=glob_style.label_style_medium)
        self.info_message_label.grid(row=0, column=0, columnspan=4, sticky="news", padx=5, pady=5)

        self.value_display = ttk.Entry(self, font=glob_style.label_style_big)
        self.value_display.grid(row=1, column=0, columnspan=4, sticky="news", padx=5, pady=5)
        self.value_display.insert(0, self.input_field.get())

        self.button_1 = ttk.Button(self, text="1", command=lambda: self.add_digit(1))
        self.button_1.grid(row=2, column=0, sticky="news", padx=5, pady=5)

        self.button_2 = ttk.Button(self, text="2", command=lambda: self.add_digit(2))
        self.button_2.grid(row=2, column=1, sticky="news", padx=5, pady=5)

        self.button_3 = ttk.Button(self, text="3", command=lambda: self.add_digit(3))
        self.button_3.grid(row=2, column=2, sticky="news", padx=5, pady=5)

        self.button_4 = ttk.Button(self, text="4", command=lambda: self.add_digit(4))
        self.button_4.grid(row=3, column=0, sticky="news", padx=5, pady=5)

        self.button_5 = ttk.Button(self, text="5", command=lambda: self.add_digit(5))
        self.button_5.grid(row=3, column=1, sticky="news", padx=5, pady=5)

        self.button_6 = ttk.Button(self, text="6", command=lambda: self.add_digit(6))
        self.button_6.grid(row=3, column=2, sticky="news", padx=5, pady=5)

        self.button_7 = ttk.Button(self, text="7", command=lambda: self.add_digit(7))
        self.button_7.grid(row=4, column=0, sticky="news", padx=5, pady=5)

        self.button_8 = ttk.Button(self, text="8", command=lambda: self.add_digit(8))
        self.button_8.grid(row=4, column=1, sticky="news", padx=5, pady=5)

        self.button_9 = ttk.Button(self, text="9", command=lambda: self.add_digit(9))
        self.button_9.grid(row=4, column=2, sticky="news", padx=5, pady=5)

        self.button_0 = ttk.Button(self, text="0", command=lambda: self.add_digit(0))
        self.button_0.grid(row=5, column=0, columnspan=2, sticky="news", padx=5, pady=5)

        if self.input_type == "float":
            self.button_comma = ttk.Button(self, text=".", command=lambda: self.add_digit("."))
            self.button_comma.grid(row=5, column=2, sticky="news", padx=5, pady=5)
        elif self.input_type == "time":
            self.button_colon = ttk.Button(self, text=":", command=lambda: self.add_digit(":"))
            self.button_colon.grid(row=5, column=2, sticky="news", padx=5, pady=5)

        self.button_delete = ttk.Button(self, text="\u2190", command=self.remove_digit)
        self.button_delete.grid(row=2, column=3, rowspan=2, sticky="news", padx=5, pady=5)

        self.button_enter = ttk.Button(self, text="\u2936", command=self.enter)
        self.button_enter.grid(row=4, column=3, rowspan=2, sticky="news", padx=5, pady=5)

    def add_digit(self, value):
        current_input = self.value_display.get()
        if not (value == ":" and current_input.count(":")) and not \
                (value == "." and current_input.count(".")):
            self.value_display.insert(tk.END, value)

    def remove_digit(self):
        current_input = self.value_display.get()
        if len(current_input) > 0:
            self.value_display.delete((len(current_input) - 1), tk.END)

    def enter(self):
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, self.value_display.get())
        self.withdraw()


class Keyboard(tk.Toplevel):
    def __init__(self, prod_mode, info_message, input_field=None, return_type="entry"):
        super().__init__()
        self.prod_mode = prod_mode
        self.geometry(glob_style.screen_resolution)
        if self.prod_mode:
            self.attributes("-fullscreen", True)
            self.config(cursor=glob_style.cursor)

        self.info_message = info_message
        self.input_field = input_field
        self.return_type = return_type

        self.upper_case = False

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.info_message_label = ttk.Label(self, text=self.info_message,
                                            font=glob_style.label_style_medium)
        self.info_message_label.grid(row=0, column=0, columnspan=11, sticky="news", padx=5, pady=5)

        self.value_display = ttk.Entry(self, font=glob_style.label_style_big)
        self.value_display.grid(row=1, column=0, columnspan=8, sticky="news", padx=5, pady=5)
        if self.return_type == "entry":
            self.value_display.insert(0, self.input_field.get())

        self.delete_button = ttk.Button(self, text="\u2190", command=self.delete_char)
        self.delete_button.grid(row=1, column=8, columnspan=3, sticky="news", padx=5, pady=5)

        key_list = [["q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ü"],
                    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä"],
                    ["SHIFT", "y", "x", "c", "v", "b", "n", "m", ",", ".", "-"]]

        self.key_dict = {}
        for i, key_row in enumerate(key_list):
            for y, key in enumerate(key_row):
                if key == "SHIFT":
                    self.key_dict[f"key_{key_row}_{key}"] = \
                        ttk.Button(self, text="\u21E7", command=self.shift)
                else:
                    self.key_dict[f"key_{key_row}_{key}"] = \
                        ttk.Button(self, text=key, command=lambda _=key: self.add_char(_))
                self.key_dict[f"key_{key_row}_{key}"].grid(row=i+2, column=y, sticky="news", padx=2, pady=2)

        self.space_bar = ttk.Button(self, command=lambda c: self.add_char(" "))
        self.space_bar.grid(row=5, column=3, columnspan=5, sticky="news", padx=5, pady=5)

        self.enter_button = ttk.Button(self, text="\u2936", command=self.enter)
        self.enter_button.grid(row=5, column=8, columnspan=3, sticky="news", padx=5, pady=5)

    def add_char(self, char):
        char = char.upper() if self.upper_case and char.isalpha() else char
        self.value_display.insert(tk.END, char)

    def delete_char(self):
        current_input = self.value_display.get()
        if len(current_input) > 0:
            self.value_display.delete((len(current_input) - 1), tk.END)

    def shift(self):
        if self.upper_case:
            self.upper_case = False
        else:
            self.upper_case = True
        for char in self.key_dict:
            current_char = self.key_dict[char]["text"]
            if current_char.isalpha():
                self.key_dict[char].configure(text=current_char.upper() if self.upper_case else current_char.lower())

    def enter(self):
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, self.value_display.get())
        self.withdraw()


class CalibrationInput(MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="news", padx=7, pady=7)
        self.frame.rowconfigure((0, 1, 2), weight=1)
        self.frame.columnconfigure((0, 1), weight=1)

        self.info_label = ttk.Label(self.frame, text="Kalibrierung abgeschlossen",
                                    font=glob_style.label_style_big,
                                    background=glob_style.background_color_frame)
        self.info_label.grid(row=0, column=0, columnspan=2, padx=7, pady=7)

        self.input_label = ttk.Label(self.frame, text="Wassermenge (in ml.):",
                                     font=glob_style.label_style_medium,
                                     background=glob_style.background_color_frame)
        self.input_label.grid(row=1, column=0, sticky="e", padx=7, pady=7)

        self.input_entry = ttk.Entry(self.frame, font=glob_style.label_style_medium)
        self.input_entry.grid(row=1, column=1, sticky="we", padx=7, pady=7)
        self.input_entry.bind("<Button-1>",
                              lambda _: NumPad(prod_mode=self.prod_mode,
                                               input_field=self.input_entry,
                                               input_type="float",
                                               info_message="Wassermenge in Milliliter"))

        self.save_button = ttk.Button(self.frame, text="speichern",
                                      command=self.save_calibration_result)
        self.save_button.grid(row=2, column=0, columnspan=2, sticky="we", padx=7, pady=7)

        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=1, column=0, sticky="we", padx=5, pady=5)

    def save_calibration_result(self):
        pumped_volume = self.input_entry.get()
        if pumped_volume == "":
            messagebox.showwarning(message="Bitte gültigen Wert eingeben")
        else:
            if self.prod_mode:
                steps_per_revolution = glob_var.pump_process.spr
                calibration_steps = glob_var.pump_process.volume_calibration_target_steps
            else:
                steps_per_revolution = 8000
                calibration_steps = 100000

            revolutions_done = calibration_steps / steps_per_revolution
            ml_per_revolution = float(pumped_volume) / revolutions_done

            if self.prod_mode:
                glob_var.pump_process.ml_per_revolution = ml_per_revolution

            glob_var.config_json["calibration"]["pump_ml_per_revolution"] = ml_per_revolution
            with open("configurations.json", "w") as outfile:
                outfile.write(json.dumps(glob_var.config_json, indent=4))

            messagebox.showinfo(message=f"Steps: {calibration_steps}\n"
                                        f"Umdrehungen: {revolutions_done}\n"
                                        f"ml/Umdrehung: {ml_per_revolution}")

            self.return_menu()

    def return_menu(self):
        glob_var.pump_menu_frame.deiconify()
        self.destroy()
