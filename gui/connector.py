
# gui/connector.py

import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tooltip import ToolTip

class ConnectorFunc:
    def __init__(self):
        pass




    def tool_tip(self, widget, text):
        """Add a tooltip to a widget."""
        tooltip = ToolTip(widget, text=text, bootstyle='danger-inverse')
        return tooltip
    
    def show_toast(self, title, message, bt=None):
        """Show a toast notification."""
        self.toast = ToastNotification(
            title=title, 
            message=message,
            duration=2000,
            bootstyle= bt if bt else 'dark',
            position=(50, 100, 'ne')
        )
        self.toast.show_toast()

    def tes_toast(self, title, message):
        """Test toast notification."""
        self.show_toast(title=title, message=message)

    def create_widgets(self, parent):

        self.btn_widget = ttk.Button(parent, text="Click Me", 
                                    bootstyle="success",
                                    command=self.tes_toast)
    
        