import tkinter as tk
from tkinter import ttk

from GUI import helper, glob_style
import main


class MainMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.menu_label = ttk.Label(self, text=f"Juna OS {main.__version__}")
        self.menu_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        self.frame = ttk.Frame(self)
        self.frame.grid(row=1, column=0, sticky="news", padx=15, pady=15)

        self.frame.rowconfigure((0, 1), weight=1)
        self.frame.columnconfigure((0, 1), weight=1)

        self.brew_icon = tk.PhotoImage(file="assets/icons/brewing.png")
        self.brew_button = ttk.Button(self.frame, text="Brühen", image=self.brew_icon,
                                      compound="top")
        self.brew_button.grid(row=0, column=0, sticky="news", padx=7, pady=7)

        self.profile_icon = tk.PhotoImage(file="assets/icons/profiles.png")
        self.profile_button = ttk.Button(self.frame, text="Profile", image=self.profile_icon,
                                         compound="top")
        self.profile_button.grid(row=0, column=1, sticky="news", padx=7, pady=7)

        self.testing_icon = tk.PhotoImage(file="assets/icons/testing.png")
        self.testing_button = ttk.Button(self.frame, text="Analyse", image=self.testing_icon,
                                         compound="top")
        self.testing_button.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.settings_icon = tk.PhotoImage(file="assets/icons/settings.png")
        self.settings_button = ttk.Button(self.frame, text="Einstellungen", image=self.settings_icon,
                                          compound="top")
        self.settings_button.grid(row=1, column=1, sticky="news", padx=7, pady=7)

    def start_brew_menu(self):
        pass

    def start_profile_menu(self):
        pass

    def start_settings_menu(self):
        pass

    def start_testing_menu(self):
        pass
