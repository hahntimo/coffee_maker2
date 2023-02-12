__version__ = "1.0"

import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import argparse
import os
from PIL import Image, ImageTk

import glob_var
from GUI import glob_style
from GUI import menus


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
        self.style.configure("Treeview", rowheight=30)
        self.style.configure("TButton", font=glob_style.label_style_medium)

        if prod_mode:
            self.attributes('-fullscreen', True)
            self.configure(cursor=glob_style.cursor)

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)
        self.welcome_label = ttk.Label(self, text=f"Kaldi OS {__version__}", font=("Arial", 40),
                                       background=glob_style.background_color_master)
        self.welcome_label.grid(row=0, column=0, sticky="s", padx=7, pady=7)

        self.logo_image = Image.open("assets/coffein.png")
        self.logo_image = self.logo_image.resize((364, 300), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo,
                                   background=glob_style.background_color_master)
        self.logo_label.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        if not self.prod_mode:
            self.dev_mode_label = ttk.Label(self, text="developer mode", background=glob_style.background_color_master)
            self.dev_mode_label.grid(row=2, column=0, sticky="n", padx=7, pady=7)

        self.after(4000, self.start)

    def start(self):
        self.withdraw()
        glob_var.main_menu_frame = menus.MainMenu(self.prod_mode)


def run(opt):
    # load configuration JSON
    if not os.path.exists("configurations.json"):
        with open("configurations.json", "w") as outfile:
            outfile.write(json.dumps(glob_var.default_config_json, indent=4))

    with open('configurations.json', 'r') as json_file:
        glob_var.config_json = json.load(json_file)

    if opt.prod_mode:
        pass

    glob_var.boot_frame = BootScreen(opt.prod_mode)
    glob_var.boot_frame.mainloop()


def params():
    parser = argparse.ArgumentParser(description='Coffee Maker',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--prod-mode', action='store_true', help='Allow running without an RasPi.')
    return parser.parse_args()


if __name__ == "__main__":
    options = params()
    run(options)
