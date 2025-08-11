import ttkbootstrap as ttk
from ttkbootstrap.widgets import Progressbar


class BottomBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bootstyle="secondary")
        self.pack(side="bottom", fill="both")

        # Grid layout config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Status label (left side)
        self.label = ttk.Label(self, text="Status: Ready", anchor="w", 
                               bootstyle="inverse-secondary", 
                               font=("Arial", 10), 
                               foreground="black", 
                               background="lightgray"
                               )
        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Progress bar (right side)
        self.progress = Progressbar(
            self, orient="horizontal", length=200, mode="determinate", bootstyle="success-striped"
        )
        self.progress.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        self.progress['value'] = 40  # Example value
