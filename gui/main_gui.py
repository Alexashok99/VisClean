
# gui/main_gui.py

# import time
# import os
# from pathlib import Path
# import csv
# import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from ttkbootstrap import themes
# from tkinter import filedialog, messagebox, scrolledtext

# From local modules
#from gui Folder
from .menu_bar import AppMenuBar
from .widgets import Segment
from .tab_frame import TabFrame
from .rt_frame import RightFrame
from .botm_br import BottomBar
from .connector import ConnectorFunc
from .upper_frame import UpperFrame
#from setting Folder
from setting.settings import *
#From src Folder
from src.scanner import Scanner
from src.log_saving import FileSaving
from src.gui_function import GUIFunction



class MainApp(ttk.Window, GUIFunction):
    def __init__(self):
        super().__init__(themename=THEME1)
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

        # Initialize scanner and file saving logic
        self.scanner = Scanner()
        self.log_saving = FileSaving()

        self.masseage = ConnectorFunc()

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
        self.choose_file = self.widgets_seg.btn_widgets("Choose Folder", comnd=self.select_folder, row=0, col=0)
        self.btn_scan = self.widgets_seg.btn_widgets("Scan Files", comnd=self.run_scanning, st="disabled", row=1, col=0)
        self.view_btn = self.widgets_seg.btn_widgets("View Result", comnd= self.goto_tab2, st="normal", row=2, col=0)
        self.sav_res = self.widgets_seg.btn_widgets("Save Result", comnd= self.save_file_infotxt, st="disabled", row=3, col=0)
        self.sav_log = self.widgets_seg.btn_widgets("Save Logs", comnd= self.save_pkl_logs,st="disabled", row=4, col=0)
        self.sv_csv = self.widgets_seg.btn_widgets("Save to CSV", comnd=self.run_save_csv, st="disabled", row=5, col=0)
        self.files_csv = self.widgets_seg.btn_widgets("View Files", comnd=self.goto_tab3, st="normal", row=6, col=0)
        self.widgets_seg.btn_widgets("Close App", lambda: self.destroy(), row=7, col=0)

        # Entry box
        self.widgets_seg.entry_widgets(row=8, col=0)

        # Status text
        self.widgets_seg.text_widgets("Status: Ready", bg="lightgray", row=9, col=0)


    #----------------------------------Main Area GUI----------------------------------#
    # Create the main area with upper frame, tab frame, and right frame
    def create_main_area(self):
        self.main_area = ttk.Frame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        # Configure main area layout
        self.main_area.grid_columnconfigure(0, weight=4)
        self.main_area.grid_columnconfigure(1, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=9)

        self.upper_main_area()  # Create upper part of main area
        self.create_tab_frame()  # Create tab frame in lower part of main area
        self.create_right_frame()  # Create right frame with additional widgets

    #----------------------------------Upper Frame GUI----------------------------------#
    def upper_main_area(self):
        """Create the upper part of the main area with segments and widgets."""
        # Create segments in the main area
        mm_uper = ttk.Frame(self.main_area)
        mm_uper.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.upper_frm = UpperFrame(mm_uper)
        self.upper_frm.pack(expand=True, fill="both")

        self.upper_frm.create_widgets() 
        self.upper_frm.update_status("Welcome to the File Scanner App!")
        
 
    #----------------------------------Tab Frame GUI----------------------------------#
    def create_tab_frame(self):
        """Create the tab frame with Scanning, Results, and File Info tabs."""    
        # Create lower main area segment
        mm_lower = ttk.Frame(self.main_area)
        mm_lower.grid(row=1, column=0, sticky="nsew")

        self.tab_frame = TabFrame(mm_lower)
        self.tab_frame.pack(expand=True, fill="both")


    #----------------------------------Right Frame GUI----------------------------------#
    def create_right_frame(self):
        """Create the right frame with additional widgets."""
        # Create right side frame for additional widgets
        mm_rside = ttk.Frame(self.main_area)
        mm_rside.grid(row=1, column=1, sticky="nsew")
        # Placeholder for right side content
        self.rt_frm = RightFrame(mm_rside)
        self.rt_frm.pack(expand=True, fill="both")
        self.rt_frm.create_widgets()
        self.rt_frm.progress_bar()
        self.rt_frm.tool_tip(self.btn_scan, "This button starts the scanning process.", bt='success-inverse')
        self.rt_frm.tool_tip(self.choose_file, "This button starts the scanning process.", bt='danger-inverse')
        


    #----------------------------------Bottom Bar GUI----------------------------------#
    # Create a bottom bar with status and progress bar
    def bottom_bar(self):
        bottom_bar_frm = ttk.Frame(self)
        bottom_bar_frm.grid(row=1, column=0, columnspan=2, sticky="ewns")
        # Configure bottom bar layout
        self.bottom_bar = BottomBar(bottom_bar_frm)
        self.bottom_bar.pack(side="bottom", fill="both")

#----------------------------------End of MainApp Class GUI----------------------------------#
