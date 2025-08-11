
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class AppMenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        # File menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="New", command=lambda: print("New file"))
        file_menu.add_command(label="Open", command=lambda: print("Open file"))
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=lambda: print("Save file"))
        self.add_cascade(label="File", menu=file_menu)

        # Help menu
        self.help_check_string = tk.StringVar()
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_checkbutton(
            label="Check",
            onvalue="on",
            offvalue="off",
            variable=self.help_check_string
        )
        help_menu.add_command(
            label="Show Check Value",
            command=lambda: print(self.help_check_string.get())
        )
        self.add_cascade(label="Help", menu=help_menu)

        # Exercise menu with sub-menu
        exercise_menu = tk.Menu(self, tearoff=False)
        exercise_menu.add_command(label="Exercise Test 1")

        exercise_sub_menu = tk.Menu(exercise_menu, tearoff=False)
        exercise_sub_menu.add_command(label="Some more stuff")
        exercise_menu.add_cascade(label="More stuff", menu=exercise_sub_menu)

        self.add_cascade(label="Exercise", menu=exercise_menu)
