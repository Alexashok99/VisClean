
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from tkinter import scrolledtext

from setting.settings import FONT_SIZE

class UpperFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bootstyle="primary")
        self.grid_columnconfigure(0, weight=9, minsize=400)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=50)

    def create_widgets(self):
        # self.show_text = ttk.Label(
        #     self,
        #     text="Welcome to the File Scanner App!",
        #     font= FONT_SIZE["Log"],
        #     bootstyle="inverse-primary",
        #     anchor="center", justify="center"
        # )
        # self.show_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.show_text = scrolledtext.ScrolledText(
            self,
            wrap="word",
            bg="#BEEAD7",
            fg="#333333",
            font=("Consolas", 10),
            height=2
        )
        self.show_text.grid(row=0, column=0, sticky="nsew")

        self.search_entry = ttk.Entry(self, bootstyle="info")
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.btn_widget = ttk.Button(
            self, text="Search", bootstyle="success",
            command= self.search_action
        )
        self.btn_widget.grid(row=0, column=2, sticky="ew", padx=10, pady=10)
        ToolTip(self.btn_widget, text="Click to start Help")

    def update_status(self, text):
        # self.show_text.config(text=text)
        self.show_text.insert(tk.END, f"{text}\n")

    def get_search_text(self):
        return self.search_entry.get()
    

    def search_action(self):
        """Perform search action based on the entry text."""
        search_text = self.get_search_text()
        if search_text:
            self.show_text.delete(1.0, tk.END)
            self.update_status(f"Searching for: {search_text}")
            self.search_entry.delete(0, tk.END)  # Clear the entry after search
            # Here you would implement the actual search logic

            print(f"Searching for: {search_text}")
            # Here you would implement the actual search logic
        else:
            self.update_status("Please enter a search term.")
            print("Please enter a search term.")
    




if __name__ == "__main__":
    root = ttk.Window(themename='darkly')
    upper_frame = UpperFrame(root)
    upper_frame.create_widgets()
    upper_frame.pack(expand=True, fill='both')
    root.mainloop()
