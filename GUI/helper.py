import tkinter as tk
from tkinter import ttk

from GUI import glob_style


class MenuFrame(tk.Toplevel):
    def __init__(self, prod_mode):
        super().__init__()
        self.prod_mode = prod_mode
        self.geometry(glob_style.screen_resolution)
        self.configure(background=glob_style.background_color_master)
        if prod_mode:
            self.attributes('-fullscreen', True)
            self.configure(cursor=glob_style.cursor)
