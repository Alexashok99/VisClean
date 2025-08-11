
import tkinter as tk
import ttkbootstrap as ttk


class Segment(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid_columnconfigure((0), weight=1, uniform="a")  # make columns resize evenly
        self.grid_rowconfigure(0, weight=1, uniform="a")  # allow row to expand

    def text_widgets(self, label_text,fnt=None,bg=None, row=0, col=0):
        """Create and place a label widget."""
        label = ttk.Label(self, text=label_text, font=fnt, background=bg)
        label.grid(row=row, column=col, sticky='ew', padx=5, pady=5)
        return label

    def btn_widgets(self, button_text, comnd, st=None,row=0, col=1):
        """Create and place a button widget."""
        btn = ttk.Button(self, text=button_text, command=comnd, state=st)
        btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
        return btn

    def entry_widgets(self, row=0, col=2):
        """Create and place an entry widget."""
        entry = ttk.Entry(self)
        entry.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
        return entry
    

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    segment = Segment(root)
    segment.text_widgets("Example Label", fnt=("Arial", 12), row=0, col=0)
    segment.btn_widgets("Click Me", lambda: print("Button Clicked"), row=0, col=1)
    segment.entry_widgets(row=0, col=2)
    segment.pack(expand=True, fill='both')
    root.mainloop()
