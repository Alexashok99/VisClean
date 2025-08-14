
# src/scanner.py
import time
import os 
from pathlib import Path
from setting.constants import FILE_TYPES


class Scanner:
    def __init__(self):
        self.csv_log = []
        self.pkl_log = []   
        self.file_stats = {ftype: {"count": 0, "size": 0} for ftype in FILE_TYPES}
        self.file_stats["OTHER"] = {"count": 0, "size": 0}  # extra category
        
    def scan(self, directory, log_area=None):
        """_summary_

        Args:
            directory (_type_ path): _description_
            log_area (Tab1-tab_frame,, optional): Tab frame Scrolleable Text. Defaults to None.

        Raises:
            ValueError: _description_
        """
        start_time = time.time()  # Start timer
        self.log_area = log_area
        self.directory = Path(directory)
        if not self.directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        # print(f"Scanning directory: {self.directory}")
        num = 0
        for root, _, filenames in os.walk(self.directory):
            for filename in filenames:
                file_path = Path(root) / filename
                num += 1
                self.log = f"{num}. 📁 Scanning: {file_path}"
                self.pkl_log.append(self.log)
                self.csv_log.append(file_path)
        # print(self.csv_log)
            # File type calculation (extension check)
                ext = file_path.suffix.lower()
                matched = False
                for ftype, fext in FILE_TYPES.items():
                    if ext == fext:
                        self.file_stats[ftype]["count"] += 1
                        self.file_stats[ftype]["size"] += file_path.stat().st_size
                        matched = True
                        break

                if not matched:  # falls into OTHER category
                    self.file_stats["OTHER"]["count"] += 1
                    self.file_stats["OTHER"]["size"] += file_path.stat().st_size
        end_time = time.time()  # End timer
        total_time = end_time - start_time
        self.fps = num / total_time if total_time > 0 else 0
        self.log_area.insert("end", f"\n✅ Scan complete! Files Found: {num}\n")
        self.log_area.insert("end", f"⏱ Time Taken: {total_time:.2f} seconds\n")
        self.log_area.insert("end", f"⚡ Actual Speed: {self.fps:.2f} files/sec\n")
        # time.sleep(5)


        # Convert size to MB
        for ftype in self.file_stats:
            self.file_stats[ftype]["size"] = round(self.file_stats[ftype]["size"] / (1024 * 1024), 3)

   
    def get_file_paths(self):
        return self.csv_log
        
    def get_logs(self):
        return self.pkl_log
    
    def get_file_stats(self):
        """Returns a dict: {FileType: {'count': x, 'size': y}}"""
        return {ftype: data for ftype, data in self.file_stats.items() if data["count"] > 0}

    def reset(self):
        self.csv_log.clear()
        self.pkl_log.clear()
 
