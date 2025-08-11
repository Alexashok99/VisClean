

import tkinter as tk
import ttkbootstrap as ttk

#Locals Imports
from setting.settings import*


class MainApp(ttk.Window):
    def __init__(self):
        super().__init__(THEME)
        self.title(TITLE)
        self.geometry(f"{WSIZE[0]}x{WSIZE[1]}+{POS[0]}+{POS[1]}")
        self.iconbitmap(ICON)
        self.minsize(WSIZE[0], WSIZE[1])


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()