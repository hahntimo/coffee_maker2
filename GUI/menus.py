import tkinter as tk
from tkinter import ttk, messagebox
import json

from GUI import helper, glob_style
import glob_var
import main


class MainMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)
        #self.prod_mode = prod_mode

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
                                      compound="top", command=self.start_brew_menu)
        self.brew_button.grid(row=0, column=0, sticky="news", padx=7, pady=7)

        self.profile_icon = tk.PhotoImage(file="assets/icons/profiles.png")
        self.profile_button = ttk.Button(self.frame, text="Profile", image=self.profile_icon,
                                         compound="top", command=self.start_brew_menu)
        self.profile_button.grid(row=0, column=1, sticky="news", padx=7, pady=7)

        self.testing_icon = tk.PhotoImage(file="assets/icons/testing.png")
        self.testing_button = ttk.Button(self.frame, text="Analyse", image=self.testing_icon,
                                         compound="top", command=self.start_testing_menu)
        self.testing_button.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.settings_icon = tk.PhotoImage(file="assets/icons/settings.png")
        self.settings_button = ttk.Button(self.frame, text="Einstellungen", image=self.settings_icon,
                                          compound="top", command=self.start_settings_menu)
        self.settings_button.grid(row=1, column=1, sticky="news", padx=7, pady=7)

    def start_brew_menu(self):
        glob_var.profile_frame = ProfileMenu(self.prod_mode)

    def start_profile_menu(self):
        pass

    def start_settings_menu(self):
        glob_var.settings_frame = SettingsMenu(self.prod_mode)

    def start_testing_menu(self):
        pass


class ProfileMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)
        self.selected_profile = None

        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.menu_label = ttk.Label(self, text=f"Profile")
        self.menu_label.grid(row=0, column=0, columnspan=2, sticky="n", padx=5, pady=5)

        # overview
        self.overview_frame = ttk.Frame(self)
        self.overview_frame.grid(row=1, column=0, sticky="news", padx=7, pady=7)
        self.overview_frame.rowconfigure((0, 1), weight=1)
        self.overview_frame.columnconfigure((0, 1), weight=1)

        self.overview_tree = ttk.Treeview(self.overview_frame, show="tree")
        self.overview_tree.grid(row=0, column=0, columnspan=2, sticky="news", padx=3, pady=3)
        self.overview_tree.bind("<ButtonRelease-1>", self.select_profile)

        self.delete_profile_icon = tk.PhotoImage(file="assets/icons/trash_can.png")
        self.delete_profile_button = ttk.Button(self.overview_frame, image=self.delete_profile_icon,
                                                command=self.delete_profile)
        self.delete_profile_button.grid(row=1, column=0, sticky="news", padx=3, pady=3)

        self.new_profile_icon = tk.PhotoImage(file="assets/icons/add.png")
        self.new_profile_button = ttk.Button(self.overview_frame, image=self.new_profile_icon)
        self.new_profile_button.grid(row=1, column=1, sticky="news", padx=3, pady=3)

        # settings
        self.settings_frame = ttk.Frame(self)
        self.settings_frame.grid(row=1, column=1, sticky="news", padx=7, pady=7)
        self.settings_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.settings_frame.columnconfigure((0, 1), weight=1)

        # name (key)
        self.name_var = tk.StringVar(value=None)
        self.name_label = ttk.Label(self.settings_frame, text="Name",
                                    background=glob_style.background_color_frame)
        self.name_label.grid(row=0, column=0, sticky="nes", padx=3, pady=3)
        self.name_entry = ttk.Entry(self.settings_frame, background=glob_style.background_color_frame,
                                    textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="nws", padx=3, pady=3)

        # blooming_bool
        self.blooming_bool_var = tk.BooleanVar(value=False)
        self.blooming_bool_label = ttk.Label(self.settings_frame, text="Blooming",
                                             background=glob_style.background_color_frame)
        self.blooming_bool_label.grid(row=1, column=0, sticky="nes", padx=3, pady=3)
        self.blooming_bool_entry = ttk.Checkbutton(self.settings_frame, variable=self.blooming_bool_var)
        self.blooming_bool_entry.grid(row=1, column=1, sticky="nws", padx=3, pady=3)

        # blooming_duration
        self.blooming_duration_var = tk.StringVar()
        self.blooming_duration_label = ttk.Label(self.settings_frame, text="Blooming-Dauer (Sek.)",
                                                 background=glob_style.background_color_frame)
        self.blooming_duration_label.grid(row=2, column=0, sticky="nes", padx=3, pady=3)
        self.blooming_duration_entry = ttk.Entry(self.settings_frame, background=glob_style.background_color_frame,
                                                 textvariable=self.blooming_duration_var)
        self.blooming_duration_entry.grid(row=2, column=1, sticky="nws", padx=3, pady=3)

        # coffee_gr_per_500ml
        self.water_ratio_var = tk.StringVar()
        self.water_ratio_label = ttk.Label(self.settings_frame, text="Mahlgut/500ml (Gr.)",
                                           background=glob_style.background_color_frame)
        self.water_ratio_label.grid(row=3, column=0, sticky="nes", padx=3, pady=3)
        self.water_ratio_entry = ttk.Entry(self.settings_frame, textvariable=self.water_ratio_var,
                                           background=glob_style.background_color_frame)
        self.water_ratio_entry.grid(row=3, column=1, sticky="nws", padx=3, pady=3)

        # brew_speed_ml_per_minute
        self.brew_speed_var = tk.StringVar()
        self.brew_speed_label = ttk.Label(self.settings_frame, text="Brühgeschwindigkeit (ml/min)",
                                          background=glob_style.background_color_frame)
        self.brew_speed_label.grid(row=4, column=0, sticky="nes", padx=3, pady=3)
        self.brew_speed_entry = ttk.Entry(self.settings_frame, textvariable=self.brew_speed_var,
                                          background=glob_style.background_color_frame)
        self.brew_speed_entry.grid(row=4, column=1, sticky="nws", padx=3, pady=3)

        # save button
        self.save_icon = tk.PhotoImage(file="assets/icons/save.png")
        self.save_button = ttk.Button(self.settings_frame, image=self.save_icon,
                                      command=self.save_changes)
        self.save_button.grid(row=5, column=0, columnspan=2, sticky="wes", padx=7, pady=7)

        # return button
        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=2, column=0, columnspan=2, sticky="wes", padx=5, pady=5)

        self.refresh_overview_tree()

    def refresh_overview_tree(self):
        self.overview_tree.delete(*self.overview_tree.get_children())
        for profile in glob_var.config_json["profiles"]:
            self.overview_tree.insert("", tk.END, text=profile)

    def delete_profile(self):
        if self.selected_profile != "" and self.selected_profile is not None:
            if messagebox.askyesno(message=f"Profil '{self.selected_profile}' löschen?"):
                glob_var.config_json["profiles"].pop(self.selected_profile)
                with open("configurations.json", "w") as outfile:
                    outfile.write(json.dumps(glob_var.config_json, indent=4))
                self.refresh_overview_tree()

    def select_profile(self, *args):
        _tree_item = self.overview_tree.focus()
        self.selected_profile = self.overview_tree.item(_tree_item)["text"]
        if self.selected_profile != "":
            self.name_var.set(self.selected_profile)
            self.blooming_bool_var.set(glob_var.config_json["profiles"][self.selected_profile]["blooming_bool"])
            self.blooming_duration_var.set(str(glob_var.config_json["profiles"][self.selected_profile]["blooming_duration"]))
            self.water_ratio_var.set(str(glob_var.config_json["profiles"][self.selected_profile]["coffee_gr_per_500ml"]))
            self.brew_speed_var.set(str(glob_var.config_json["profiles"][self.selected_profile]["brew_speed_ml_per_minute"]))

    def save_changes(self):
        if messagebox.askyesno(message="Änderungen übernehmen?"):
            glob_var.config_json["profiles"][self.selected_profile] = \
                {"blooming_bool": self.blooming_bool_var.get(),
                 "blooming_duration": float(self.blooming_duration_var.get()),
                 "coffee_gr_per_500ml": float(self.water_ratio_var.get()),
                 "brew_speed_ml_per_minute": float(self.brew_speed_var.get())}

            if self.selected_profile != self.name_var.get():
                print("name changed")
                # d = {'old_name': 1}
                # d['new_name'] = d.pop('old_name')

                glob_var.config_json["profiles"][self.name_var.get()] = \
                    glob_var.config_json["profiles"].pop(self.selected_profile)
            with open("configurations.json", "w") as outfile:
                outfile.write(json.dumps(glob_var.config_json, indent=4))

    def return_menu(self):
        glob_var.main_menu_frame.deiconify()
        self.withdraw()


class SettingsMenu(helper.MenuFrame):
    def __init__(self, prod_mode):
        super().__init__(prod_mode)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.menu_label = ttk.Label(self, text=f"Einstellungen")
        self.menu_label.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        self.frame = ttk.Frame(self)
        self.frame.grid(row=1, column=0, sticky="news", padx=15, pady=10)

        self.frame.rowconfigure((0), weight=1)
        self.frame.columnconfigure((0, 1), weight=1)

        self.sound_bool = tk.BooleanVar(value=glob_var.config_json["settings"]["sound_on"])
        self.sound_label = ttk.Label(self.frame, text="Sound abspielen", font=glob_style.label_style_big,
                                     background=glob_style.background_color_frame)
        self.sound_label.grid(row=0, column=0, sticky="new", padx=7, pady=7)
        self.sound_checkbox = ttk.Checkbutton(self.frame, variable=self.sound_bool,
                                              command=self.change_audio_settings)
        self.sound_checkbox.grid(row=0, column=1, sticky="new", padx=7, pady=7)

        self.return_button = ttk.Button(self, text="\u21E6", command=self.return_menu)
        self.return_button.grid(row=2, column=0, columnspan=2, sticky="sew", padx=5, pady=5)

    def change_audio_settings(self):
        glob_var.config_json["settings"]["sound_on"] = self.sound_bool.get()
        with open("configurations.json", "w") as outfile:
            outfile.write(json.dumps(glob_var.config_json, indent=4))

    def return_menu(self):
        glob_var.main_menu_frame.deiconify()
        self.withdraw()
