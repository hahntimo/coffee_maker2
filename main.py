__version__ = "1.0"

import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import argparse
import git
import time
import os
import requests
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
        self.style.configure('TFrame', background=glob_style.background_color_frame)
        self.style.configure("TCheckbutton", background=glob_style.background_color_frame)

        if prod_mode:
            self.attributes('-fullscreen', True)
            self.configure(cursor=glob_style.cursor)

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)
        self.welcome_label = ttk.Label(self, text=f"Juna OS {__version__}", font=("Arial", 50),
                                       background=glob_style.background_color_master)
        self.welcome_label.grid(row=0, column=0, sticky="s", padx=7, pady=7)

        self.logo_image = Image.open("assets/coffein.png")
        self.logo_image = self.logo_image.resize((364, 300), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo,
                                   background=glob_style.background_color_master)
        self.logo_label.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.git_status_label = ttk.Label(self, background=glob_style.background_color_master)
        self.git_status_label.grid(row=2, column=0, sticky="n", padx=7, pady=7)

        self.after(1000, self.boot)

    def boot(self):
        if self.prod_mode:
            self.git_status_label["text"] = "Suche nach Update..."
            repo_path = os.path.dirname(os.path.abspath(__file__))
            os.chdir(repo_path)
            repository = git.Repo()
            repository.git.checkout("main")
            for attempt in range(10):
                try:
                    requests.head("https://google.com", timeout=1)
                    current_repo_state = repository.head.commit
                    repository.remotes.origin.pull()

                    if current_repo_state != repository.head.commit:
                        self.git_status_label["text"] = "Neue Version heruntergeladen"
                        self.after(2000, self.start)
                    else:
                        self.git_status_label["text"] = "Kein neues Update gefunden"
                        self.after(2000, self.start)

                    break
                except requests.Timeout:
                    time.sleep(1)
            else:
                self.git_status_label["text"] = "Keine Verbindung zum Internet"
                self.after(2000, self.start)

        else:
            self.git_status_label["text"] = "Developer mode"
            self.after(1000, self.start)

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
