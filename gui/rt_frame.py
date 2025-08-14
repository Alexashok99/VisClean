
# gui/rt_frame.py

import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.widgets import DateEntry, Floodgauge, Meter
from ttkbootstrap.toast import ToastNotification

class RightFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        

    def tool_tip(self, widget, text, bt=None):
        """Add a tooltip to a widget."""
        tooltip = ToolTip(widget, text=text, bootstyle=bt if bt else 'danger-inverse')
        return tooltip
    
    def show_toast(self):
        """Show a toast notification."""
        self.toast = ToastNotification(
            title='This is a message title', 
            message='This is the actual message',
            duration=2000,
            bootstyle='dark',
            position=(50, 100, 'ne')
        )
        self.toast.show_toast()

    
    def create_widgets(self):
        """Create widgets for the right frame."""
        label = ttk.Label(self, text="Right Side", 
                          font=("Arial", 12), 
                          bootstyle="info-inverse",
                          anchor="center",justify="center"
                          )
        label.pack(expand=True, fill="both", pady=10)

        # Example button with tooltip
        button = ttk.Button(self, text="Click Me", 
                            bootstyle="success",
                            command=self.show_toast
                            )
        button.pack(pady=10)
        self.tool_tip(button, "This is a button that you can click.")
        
        # Example entry field
        entry = ttk.Entry(self)
        entry.pack(pady=10)
        self.tool_tip(entry, "Enter some text here.")

        """_summary_
        Create a progress bar to show scanning progress.
        The progress bar will be updated during the scanning process.
        """
    def progress_bar(self):
        self.progress_int = ttk.IntVar(value=0)
        self.progress = ttk.Floodgauge(
            self, 
            text='Progress', 
            variable=self.progress_int,
            bootstyle='danger',
            mask='{}%'
        )
        self.progress.pack(pady=10, fill='x')
        ttk.Scale(self, from_=0, to=100, variable=self.progress_int).pack()

        """_summary_
        Create a speed meter to show scanning speed.
        """
        self.meter = ttk.Meter(
            self,
            amounttotal=100,   # max value, yahan speed ka scale set karein
            amountused=0,      # start from 0
            interactive=False,
            metertype="semi",  # semi-circle meter
            textright="fps",  # text on the right side
            subtext='Scanning Speed',
            stripethickness=10,  # thickness of the stripes
            bootstyle='success'  # style of the meter
        )
        self.meter.pack(pady=10, fill='x')


if __name__ == "__main__":
    root = ttk.Window(themename='darkly')
    root.title('Right Frame Example')
    right_frame = RightFrame(root)
    right_frame.create_widgets()
    right_frame.progress_bar()
    root.mainloop()
