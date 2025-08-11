
import time
import os
from pathlib import Path
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import themes
from tkinter import filedialog, messagebox, scrolledtext

# From local modules
#from gui Folder
from .menu_bar import AppMenuBar
from .widgets import Segment
from .tab_frame import TabFrame
from .rt_frame import RightFrame
from .botm_br import BottomBar
#from setting Folder
from setting.settings import *
#From src Folder
from src.scanner import Scanner
from src.log_saving import FileSaving

def choose_folder():
    return filedialog.askdirectory()

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

        # Initialize scanner and file saving logic
        self.scanner = Scanner()
        self.log_saving = FileSaving()

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
        self.view_btn = self.widgets_seg.btn_widgets("View Result", lambda: print("Scan Button Clicked"), st="disabled", row=2, col=0)
        self.sav_res = self.widgets_seg.btn_widgets("Save Result", comnd= self.save_file_infotxt, st="disabled", row=3, col=0)
        self.sav_log = self.widgets_seg.btn_widgets("Save Logs", comnd= self.save_pkl_logs,st="disabled", row=4, col=0)
        self.sv_csv = self.widgets_seg.btn_widgets("Save to CSV", comnd=self.run_save_csv, st="disabled", row=5, col=0)
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

        self.tab_frame = TabFrame(mm_lower)
        self.tab_frame.pack(expand=True, fill="both")

        aa = "Hello, this is a placeholder for the main content area. You can add your widgets here."
        for i in range(51):
            self.tab_frame.txt_area.insert(tk.END, f"{aa}\n")
            self.tab_frame.txt_area.see("end-1c")  # Scroll to the end

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

    def select_folder(self):
        folder = choose_folder()
        if folder:
            # Reset old scan data
            self.scanner.reset()
            self.tab_frame.txt_area.delete(1.0, tk.END)

            self.source = folder # Store the selected folder path
            self.tab_frame.txt_area.insert(tk.END, f"📂 Selected folder: {folder}\n")
            self.btn_scan.config(state="normal")
        else:
            messagebox.showwarning("Warning", "No folder selected.")

        self.view_btn.config(state="disabled")
        self.sav_res.config(state="disabled")
        self.sav_log.config(state="disabled")
        self.sv_csv.config(state="disabled")


    def run_scanning(self):
        self.scanner.reset()
        self.tab_frame.txt_area.delete(1.0, tk.END)
        self.tab_frame.txt_area.insert(tk.END, "🔍 Scanning started...\n")
        self.update_idletasks()

        start_time = time.time()  # Start timer
        num = 0
        for root, dirs, files in os.walk(self.source):
            for file_name in files:
                scanning_path = Path(root) / file_name
                num += 1
                log = f"{num}. 📁 Scanning: {scanning_path}"
                self.tab_frame.txt_area.insert(tk.END, log + "\n")
                self.tab_frame.txt_area.see(tk.END)
                self.update_idletasks()
                self.tab_frame.txt_area.delete(1.0, tk.END)
                # time.sleep(0.01)  # Simulate some delay for scanning
        time_taken = time.time() - start_time
        self.tab_frame.txt_area.insert(tk.END, f"✅ Scan completed in {time_taken:.2f} seconds.\n")
        self.tab_frame.txt_area.insert(tk.END, "------------------Scan End------------------------\n")

        # Internal Scanning
        self.scanner.scan(self.source, self.tab_frame.txt_area)

        for ftype, data in self.scanner.get_file_stats().items():
            self.tab_frame.txt_area.insert(tk.END, f"{ftype}: {data['count']} files, {data['size']} MB \n")
        # self.tab_frame.txt_area.insert(tk.END, f"📊 File statistics: {self.scanner.get_file_stats()}\n")

        # self.tab_frame.txt_area.insert(tk.END, f"✅ Scan completed. {num} files scanned.\n")
        self.tab_frame.txt_area.insert(tk.END, "💾 You can now save the logs as CSV or PKL and Files Info in Text file.\n")
        self.tab_frame.txt_area.see(tk.END)

        self.view_btn.config(state="normal")
        self.sav_res.config(state="normal")
        self.sav_log.config(state="normal")
        self.sv_csv.config(state="normal")

    
    def run_save_csv(self):
        self.tab_frame.txt_area.insert(tk.END, "💾 Saving logs as CSV...\n")
        # Example logic for saving CSV
        self.log_saving.csv_logs_save(self.scanner.get_file_paths())
        self.tab_frame.txt_area.insert(tk.END, "✅ CSV logs saved successfully.\n")
        self.sv_csv.config(state="disabled")
        
    def save_pkl_logs(self):
        self.tab_frame.txt_area.insert(tk.END, "💾 Saving logs as PKL...\n")
        # Example logic for saving PKL
        self.log_saving.pkl_logs_save(self.scanner.get_logs())
        self.tab_frame.txt_area.insert(tk.END, "✅ PKL logs saved successfully.\n")
        self.sav_log.config(state="disabled")

    def save_file_infotxt(self):
        self.tab_frame.txt_area.insert(tk.END, "💾 Saving file info...\n")
        # Example logic for saving file info in Text File
        self.log_saving.save_file_info(self.scanner.get_file_stats().items())
        self.tab_frame.txt_area.insert(tk.END, "✅ File info saved successfully in Text file.\n")
        self.sav_res.config(state="disabled")
