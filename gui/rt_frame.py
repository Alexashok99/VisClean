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
                          bootstyle="inverse-purple",
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

    def progress_bar(self):
        """Create a progress bar."""
        progress_int = ttk.IntVar(value=50)
        progress = ttk.Floodgauge(
            self, 
            text='Progress', 
            variable=progress_int,
            bootstyle='danger',
            mask='mask {}%'
        )
        progress.pack(pady=10, fill='x')
        ttk.Scale(self, from_=0, to=100, variable=progress_int).pack()

        # Example meter
        meter = ttk.Meter(
            self,
            amounttotal=100,
            amountused=10,
            interactive=True,
            bootstyle='info'
        )
        meter.pack(pady=10, fill='x')

if __name__ == "__main__":
    root = ttk.Window(themename='darkly')
    root.title('Right Frame Example')
    right_frame = RightFrame(root)
    right_frame.create_widgets()
    right_frame.progress_bar()
    root.mainloop()
