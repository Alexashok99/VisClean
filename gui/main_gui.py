

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import themes

# From local modules
from .menu_bar import AppMenuBar
from .widgets import Segment
from .tab_frame import TabFrame
from .rt_frame import RightFrame
from .botm_br import BottomBar

from setting.settings import *



class MainApp(ttk.Window):
    def __init__(self):
        super().__init__(THEME)
        self.title(TITLE)
        self.geometry(f"{WSIZE[0]}x{WSIZE[1]}+{POS[0]}+{POS[1]}")
        self.iconbitmap(ICON)
        self.minsize(WSIZE[0], WSIZE[1])

        # Attach menu bar
        menu_bar = AppMenuBar(self)
        self.config(menu=menu_bar)
        
        # 2-column layout: Sidebar (20%) and Main Area (80%)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.bottom_bar()


    def create_sidebar(self):
        # Sidebar frame (20% width, full height)
        sidebar = ttk.Frame(self)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_columnconfigure(0, weight=1)   # Horizontal expand
        sidebar.grid_rowconfigure(0, weight=1)      # Space for top section
        sidebar.grid_rowconfigure(1, weight=9)      # Rest space for other widgets

        # Top section (logo/title)
        top_section = ttk.Frame(sidebar)
        top_section.grid(row=0, column=0, sticky="ew")
        ttk.Label(top_section, text="🔍 File Scanner", font=FONT_SIZE["Button"]).pack()

        # Main button area (compact)
        button_area = ttk.Frame(sidebar, border=1, relief="solid")
        button_area.grid(row=1, column=0, sticky="n")  # 'n' keeps buttons at top

        # Create Segment inside button_area
        self.widgets_seg = Segment(button_area)
        self.widgets_seg.pack(fill='x', padx=5, pady=5)  # Only expand horizontally

        # Buttons - compact size
        self.widgets_seg.btn_widgets("Choose Folder", lambda: print("Scan Files Button"), row=0, col=0)
        self.widgets_seg.btn_widgets("Scan Files", lambda: print("Folder Selected"), row=1, col=0)
        self.widgets_seg.btn_widgets("View Result", lambda: print("Scan Button Clicked"), row=2, col=0)
        self.widgets_seg.btn_widgets("Save Result", lambda: print("Scan Files Button"), row=3, col=0)
        self.widgets_seg.btn_widgets("Save Logs", lambda: print("Save Logs to pkl"), row=4, col=0)
        self.widgets_seg.btn_widgets("Save to CSV", lambda: print("Save to CSV"), row=5, col=0)
        self.widgets_seg.btn_widgets("Close App", lambda: self.destroy(), row=6, col=0)

        # Entry box
        self.widgets_seg.entry_widgets(row=7, col=0)

        # Status text
        self.widgets_seg.text_widgets("Status: Ready", bg="lightgray", row=8, col=0)



    def create_main_area(self):
        main_area = ttk.Frame(self)
        main_area.grid(row=0, column=1, sticky="nsew")

        # Configure main area layout
        main_area.grid_columnconfigure(0, weight=4)
        main_area.grid_columnconfigure(1, weight=1)
        main_area.grid_rowconfigure(0, weight=1)
        main_area.grid_rowconfigure(1, weight=9)

        # Create segments in the main area
        mm_uper = ttk.Frame(main_area)
        mm_uper.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Placeholder for main area content
        ttk.Label(mm_uper, 
                  text="Show Text Here", 
                  anchor="center", 
                  justify="center",
                  font=FONT_SIZE["Heading"], 
                  foreground="black",
                  background="grey").pack(side="left",expand=True, fill="both")
        
        wg_segment = Segment(mm_uper)
        wg_segment.pack(expand=True, fill="x", padx=5, pady=5)
        wg_segment.entry_widgets(row=0, col=1)

        wg_segment.btn_widgets("Search", lambda: print("Search Button"), row=0, col=2)
        
        # Create lower main area segment
        mm_lower = ttk.Frame(main_area)
        mm_lower.grid(row=1, column=0, sticky="nsew")

        tab_frame = TabFrame(mm_lower)
        tab_frame.pack(expand=True, fill="both")

        aa = "Hello, this is a placeholder for the main content area. You can add your widgets here."
        for i in range(51):
            tab_frame.txt_area.insert(tk.END, f"{aa}\n")
            tab_frame.txt_area.see("end-1c")  # Scroll to the end

        mm_rside = ttk.Frame(main_area)
        mm_rside.grid(row=1, column=1, sticky="nsew")
        # Placeholder for right side content
        rt_frm = RightFrame(mm_rside)
        rt_frm.pack(expand=True, fill="both")
        rt_frm.create_widgets()
        rt_frm.progress_bar()
        



    def bottom_bar(self):
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ewns")

        bottom_bar = BottomBar(bottom_bar)
        bottom_bar.pack(side="bottom", fill="both")

  


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()