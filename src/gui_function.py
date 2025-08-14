
import os
import time
import csv
import tkinter as tk
import threading

from pathlib import Path
from tkinter import filedialog, messagebox


def choose_folder():
    return filedialog.askdirectory()

class GUIFunction:
     
    def select_folder(self):
        self.masseage.show_toast("Warning", "Please Choose a Folder", bt="warning")  # Test toast notification
        folder = choose_folder()
        if folder:
            self.upper_frm.show_text.delete(1.0, tk.END)  # Clear previous text
            self.upper_frm.update_status(f"Selected Folder: {folder}")
            self.masseage.show_toast("Folder Selected", f"You have selected: {folder}", bt="success")
            # Reset old scan data
            self.scanner.reset()
            self.tab_frame.txt_area.delete(1.0, tk.END)

            self.source = folder # Store the selected folder path
            self.tab_frame.txt_area.insert(tk.END, f"📂 Selected folder: {folder}\n")
            self.btn_scan.config(state="normal")
        else:
            messagebox.showwarning("Warning", "No folder selected.")
            self.upper_frm.update_status("No folder selected.")
            self.masseage.show_toast("Warning", "No folder selected.", bt="warning")

        self.sav_res.config(state="disabled")
        self.sav_log.config(state="disabled")
        self.sv_csv.config(state="disabled")

    def run_scanning(self):
        # Thread start
        scan_thread = threading.Thread(target=self._scan_files, daemon=True)
        scan_thread.start()

    def _scan_files(self):
        if not hasattr(self, 'source') or not self.source:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return
        self.tab_frame.notebook.select(self.tab_frame.Scanning)
        self.masseage.show_toast("Scanning", "Scanning started...", bt="info")
        self.scanner.reset()

        start_time = time.time()
        num = 0
        for root, dirs, files in os.walk(self.source):
            for file_name in files:
                scanning_path = Path(root) / file_name
                num += 1
                # GUI safe update
                self.after(0, lambda log=f"{num}. 📁 Scanning: {scanning_path}":
                self.tab_frame.txt_area.insert(tk.END, log + "\n"))
                self.tab_frame.txt_area.see(tk.END)
                self.update_idletasks()
                self.tab_frame.txt_area.delete(1.0, tk.END)
                # Simulate some delay for scanning
                # time.sleep(0.01)  # Optional

        time_taken = time.time() - start_time
        self.fps = round((num / time_taken if time_taken > 0 else 0))
        self.scanner.scan(self.source, self.tab_frame.txt_area)

        self.after(0, lambda: self._scanning_complete())

    def _scanning_complete(self):
        self.upper_frm.update_status(f"Scanned {self.fps} files per second.")
        self.btn_scan.config(state="disabled")
        self.view_btn.config(state="disabled")
        self.sav_res.config(state="normal")
        self.sav_log.config(state="normal")
        self.sv_csv.config(state="normal")
        self.files_csv.config(state="disabled")


    
    def run_save_csv(self):
        self.tab_frame.txt_area.insert(tk.END, "💾 Saving logs as CSV...\n")
        # Example logic for saving CSV
        self.log_saving.csv_logs_save(self.scanner.get_file_paths())
        self.tab_frame.txt_area.insert(tk.END, "✅ CSV logs saved successfully.\n")
        self.sv_csv.config(state="disabled")
        self.files_csv.config(state="normal")
        
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
        self.view_btn.config(state="normal")

    def goto_tab2(self):
        """Switch to the Results tab."""
        self.tab_frame.results_text.delete(1.0, tk.END)

        self.tab_frame.notebook.select(self.tab_frame.Results)
        if os.path.exists(self.log_saving.text_info_path):
            with open(self.log_saving.text_info_path, 'r', encoding='utf-8') as f:
                self.tab_frame.results_text.insert(tk.END, f.read() + "\n")
        else:
            self.tab_frame.results_text.insert(tk.END, "No file info available.\n")


    def goto_tab3(self):
        """Switch to the File Info tab."""
        self.tab_frame.notebook.select(self.tab_frame.view_info)
        self.tab_frame.tree.delete(*self.tab_frame.tree.get_children())
        if os.path.exists(self.log_saving.csv_data_path):
            with open(self.log_saving.csv_data_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    self.tab_frame.tree.insert("", "end", values=row)
        else:
            self.tab_frame.tree.insert("", "end", values=("No data available", "", "", ""))
