
# src/gui_function.py

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
        """_summary_
        This method allows the user to select a folder using a file dialog.
        It updates the status label and clears previous text in the upper frame.
        """
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

    def animate_text(self):
        """_summary_
        This method animates the text in the bottom bar to indicate scanning progress.
        It updates the label with a dot animation to show that scanning is in progress.
        It runs in a separate thread to avoid blocking the GUI.
        It stops when the scanning is complete.
        """
        self.bottom_bar.label.config(text="Scanning in progress")  # reset label
        while self.rt_frm.progress_int.get() < 100:
            base_text = "Scanning in progress"
            for j in range(4):
                if self.rt_frm.progress_int.get() >= 100:
                    break
                self.bottom_bar.label.config(text=base_text + "." * j)
                time.sleep(0.5)




    def run_scanning(self):
        """_summary_
        This method initiates the file scanning process in a separate thread."""
        # Thread start
        scan_thread = threading.Thread(target=self._scan_files, daemon=True)
        scan_thread.start()

    def _scan_files(self):
        """Perform the file scanning operation."""
        """_summary_
        This method scans files in the selected folder, updates the GUI with progress,
        and handles file statistics.
        """
        self.rt_frm.progress_int.set(0)  # ✅ Reset speed/progress meter
        self.bottom_bar.progress_botm['value'] = 0  # Reset progress bar
        self.bottom_bar.progress_botm.start(10)  # Start progress bar animation

        # Start the animation thread
        # Start animate text in background
        threading.Thread(target=self.animate_text, daemon=True).start()

        if not hasattr(self, 'source') or not self.source:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return
        self.tab_frame.notebook.select(self.tab_frame.Scanning)
        self.masseage.show_toast("Scanning", "Scanning started...", bt="info")
        self.scanner.reset()

        self.btn_scan.config(state="disabled")
        self.choose_file.config(state="disabled")

        # --- Get total file count for progress ---
        total_files = sum(len(files) for _, _, files in os.walk(self.source))
        processed_files = 0

        start_time = time.time()
        num = 0
        for root, dirs, files in os.walk(self.source):
            for file_name in files:
                processed_files += 1
                scanning_path = Path(root) / file_name
                num += 1

                # Calculate speed
                elapsed = time.time() - start_time
                speed = num / elapsed if elapsed > 0 else 0

                # Update progress % and meter
                progress_percent = (processed_files / total_files) * 100 if total_files > 0 else 0
                self.after(0, lambda p=progress_percent: self.rt_frm.progress_int.set(int(p)))

                # Update speed meter
                self.after(0, lambda s=speed: self.rt_frm.meter.configure(
                amountused=min(s, self.rt_frm.meter['amounttotal'])))

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

        self.bottom_bar.progress_botm.stop()  # Stop progress bar
        self.bottom_bar.progress_botm['value'] = 100  # Set to 100
        self.bottom_bar.label.config(text=f"Scanning completed in {time_taken:.2f} seconds.")

    def _scanning_complete(self):
        """_summary_
        This method is called when the scanning is complete.
        It updates the GUI with the scanning results, enables buttons, and displays the speed.
        """
        self.upper_frm.update_status(f"Scanned {self.fps} files per second.")
        self.choose_file.config(state="normal")
        self.view_btn.config(state="disabled")
        self.sav_res.config(state="normal")
        self.sav_log.config(state="normal")
        self.sv_csv.config(state="normal")
        self.files_csv.config(state="disabled")


    
    def run_save_csv(self):
        """_summary_
        This method saves the scanned file information to a CSV file.
        It updates the GUI with the status of the save operation.
        """
        self.tab_frame.txt_area.insert(tk.END, "💾 Saving logs as CSV...\n")
        # Example logic for saving CSV
        self.log_saving.csv_logs_save(self.scanner.get_file_paths())
        self.tab_frame.txt_area.insert(tk.END, "✅ CSV logs saved successfully.\n")
        self.sv_csv.config(state="disabled")
        self.files_csv.config(state="normal")
        
    def save_pkl_logs(self):
        """_summary_
        This method saves the scanned logs in PKL format.
        It updates the GUI with the status of the save operation.
        """
        self.tab_frame.txt_area.insert(tk.END, "💾 Saving logs as PKL...\n")
        # Example logic for saving PKL
        self.log_saving.pkl_logs_save(self.scanner.get_logs())
        self.tab_frame.txt_area.insert(tk.END, "✅ PKL logs saved successfully.\n")
        self.sav_log.config(state="disabled")

    def save_file_infotxt(self):
        """_summary_
        This method saves the file information in a text file.
        It updates the GUI with the status of the save operation.
        """
        self.tab_frame.txt_area.insert(tk.END, "💾 Saving file info...\n")
        # Example logic for saving file info in Text File
        self.log_saving.save_file_info(self.scanner.get_file_stats().items())
        self.tab_frame.txt_area.insert(tk.END, "✅ File info saved successfully in Text file.\n")
        self.sav_res.config(state="disabled")
        self.view_btn.config(state="normal")

    def goto_tab2(self):
        """Switch to the Results tab.
        It clears the results text area and loads the saved file info(Text File) if available."""
        self.tab_frame.results_text.delete(1.0, tk.END)

        self.tab_frame.notebook.select(self.tab_frame.Results)
        if os.path.exists(self.log_saving.text_info_path):
            with open(self.log_saving.text_info_path, 'r', encoding='utf-8') as f:
                self.tab_frame.results_text.insert(tk.END, f.read() + "\n")
        else:
            self.tab_frame.results_text.insert(tk.END, "No file info available.\n")


    def goto_tab3(self):
        """Switch to the File Info tab.
        It loads the CSV data into the treeview for display.
        """
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
