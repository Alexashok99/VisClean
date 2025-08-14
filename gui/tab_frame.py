
# gui/tab_frame.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext


class TabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Create frames (tabs)
        self.Scanning = ttk.Frame(self.notebook)
        self.Results = ttk.Frame(self.notebook)
        self.view_info = ttk.Frame(self.notebook)

        # Add tabs to Notebook
        self.notebook.add(self.Scanning, text="Scanning")
        self.notebook.add(self.Results, text="Results Summary")
        self.notebook.add(self.view_info, text="File Info")

        # Add content in Tab 1
        self.txt_area = scrolledtext.ScrolledText(self.Scanning, wrap=tk.WORD, 
                                                 bg="#BEEAD7", 
                                                 fg="#333333", 
                                                 font=("Consolas", 10))
        self.txt_area.pack(expand=True, fill="both", padx=10, pady=10)
        self.txt_area.insert(tk.END, "This is the Scanning tab. You can add your scanning results here.")

        # Add content in Tab 2
        self.results_text = scrolledtext.ScrolledText(self.Results, wrap=tk.WORD, 
                                                      bg="#BEEAD7", 
                                                      fg="#333333", 
                                                      font=("Consolas", 10))
        self.results_text.pack(expand=True, fill="both", padx=10, pady=10)
        self.results_text.insert(tk.END, "This is the Results Summary tab. You can add your results summary here.")

        # Add content in Tab 3
        self.tree = ttk.Treeview(
            self.view_info,
            columns=("Name", "Type", "Size", "Last Modified"),
            show="headings",       # Hide first empty column
            bootstyle=INFO         # Bootstyle theme color
        )

        # Define headings
        self.tree.heading("Name", text="File Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size (MB)")
        self.tree.heading("Last Modified", text="Last Modified")

        # Set column widths
        self.tree.column("Name", width=200)
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Size", width=100, anchor="center")
        self.tree.column("Last Modified", width=150, anchor="center")

        # Add scrollbar
        scroll_y = ttk.Scrollbar(self.view_info, orient="vertical", command=self.tree.yview, bootstyle=ROUND)
        self.tree.configure(yscroll=scroll_y.set)

        # Pack widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Notebook Example")
    root.geometry("400x300")

    tab_frame = TabFrame(root)
    tab_frame.pack(expand=True, fill="both")

    root.mainloop()
