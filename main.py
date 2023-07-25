__version__ = "1.0"

import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import argparse
import os
from PIL import Image, ImageTk
from multiprocessing import Manager, Queue

import glob_var
from GUI import glob_style, menus


class BootScreen(tk.Tk):
    def __init__(self, prod_mode):
        super().__init__()
        self.prod_mode = prod_mode
        self.geometry(glob_style.screen_resolution)
        self.configure(bg=glob_style.background_color_master)
        self.style = ThemedStyle(self)
        self.style.set_theme(glob_style.theme)
        # self.style.configure('TButton', font=('Arial', 50))
        self.style.configure("TFrame", background=glob_style.background_color_frame)
        self.style.configure("TCheckbutton", background=glob_style.background_color_frame)
        self.style.configure("Treeview", rowheight=40)
        self.style.configure("TButton", font=glob_style.label_style_medium)
        self.style.configure("TScale", background=glob_style.background_color_frame)
        self.style.configure("TNotebook.Tab", font=("Arial", 20))

        if prod_mode:
            self.attributes('-fullscreen', True)
            self.configure(cursor=glob_style.cursor)

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)
        self.welcome_label = ttk.Label(self, text=f"Kaldi OS {__version__}", font=("Arial", 40), background=glob_style.background_color_master)
        self.welcome_label.grid(row=0, column=0, sticky="s", padx=7, pady=7)

        self.logo_image = Image.open("assets/coffein.png")
        self.logo_image = self.logo_image.resize((364, 300), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo,
                                   background=glob_style.background_color_master)
        self.logo_label.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        label_text = "productive mode" if self.prod_mode else "developer mode"
        self.dev_mode_label = ttk.Label(self, text=label_text, background=glob_style.background_color_master)
        self.dev_mode_label.grid(row=2, column=0, sticky="n", padx=7, pady=7)

        ms_delay = 4000 if self.prod_mode else 1000
        self.after(ms_delay, self.start)

    def start(self):
        # switch to main menu
        self.withdraw()
        glob_var.main_menu_frame = menus.MainMenu(self.prod_mode)


def run(opt):
    # load configuration JSON
    if not os.path.exists("configurations.json"):
        with open("configurations.json", "w") as config_file:
            config_file.write(json.dumps(glob_var.default_config_json, indent=4))

    with open('configurations.json', 'r') as json_file:
        glob_var.config_json = json.load(json_file)

    # define mp managers & mp data handlers
    # switch
    switch_manager = Manager()
    glob_var.switch_mp_data = switch_manager.dict()
    glob_var.switch_mp_data["heater_switch"] = True
    glob_var.switch_mp_data["brewer_switch"] = False
    glob_var.switch_mp_data["heater"] = False

    # spinner
    glob_var.spinner_task_queue = Queue()
    glob_var.spinner_output_queue = Queue()

    # pump
    glob_var.pump_task_queue = Queue()
    pump_manager = Manager()
    glob_var.pump_mp_data = pump_manager.dict()
    glob_var.pump_mp_data["target_steps"] = 0
    glob_var.pump_mp_data["remaining_steps"] = 0

    heater_manager = Manager()
    glob_var.heater_mp_data = heater_manager.dict()
    glob_var.heater_mp_data["target_temp"] = 0
    glob_var.heater_mp_data["heating_up"] = False

    # define controller processes
    if opt.prod_mode:
        import controllers

        # switch
        glob_var.switch_process = controllers.SwitchController(glob_var.switch_mp_data)
        glob_var.switch_process.start()

        # spinner
        glob_var.spinner_process = \
            controllers.SpinnerController(task_queue=glob_var.spinner_task_queue,
                                          output_queue=glob_var.spinner_output_queue,
                                          runtime_delay=glob_var.config_json["calibration"]["spinner_step_delay"])
        glob_var.spinner_process.start()

        # pump
        glob_var.pump_process = \
            controllers.PumpController(task_queue=glob_var.pump_task_queue,
                                       process_data=glob_var.pump_mp_data,
                                       switch_mp_data=glob_var.switch_mp_data,
                                       config_json=glob_var.config_json
                                       )
        glob_var.pump_process.start()

        # heater
        glob_var.heater_process = \
            controllers.HeaterController(switch_mp_data=glob_var.switch_mp_data,
                                         pump_mp_data=glob_var.pump_mp_data,
                                         heater_mp_data=glob_var.heater_mp_data)

    glob_var.boot_frame = BootScreen(opt.prod_mode)
    glob_var.boot_frame.mainloop()


def params():
    parser = argparse.ArgumentParser(description='Coffee Maker',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--prod-mode', action='store_true', help='Allow running without a RasPi.')
    return parser.parse_args()


if __name__ == "__main__":
    options = params()
    run(options)
