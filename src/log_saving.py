
# from src.scanner import Scanner
import pickle
import csv
import os
import datetime

class FileSaving:
    def __init__(self):
        self.data_path = r"data\logs.pkl"
        self.csv_data_path = r"data\logs.csv"
        self.text_info_path = r"data\file_info.txt"
   

    def csv_logs_save(self, csv_data):
        csv_file = csv_data
        heading = ['Name', 'Size', 'File type', 'Last modified']
        with open(self.csv_data_path, 'w', newline='', encoding="utf-8") as f:
            writ = csv.writer(f)
            writ.writerow(heading)
            for scanning_path in csv_file:
                file_name = scanning_path.stem
                file_ext = scanning_path.suffix.lstrip('.')
                modified_time = os.path.getmtime(scanning_path)
                modified_date = datetime.datetime.fromtimestamp(modified_time).strftime("%d-%m-%Y %I:%M %p") 
                size = f"{round((scanning_path.stat().st_size) / (1024 * 1024), 3)} MB"
                data = [file_name, size, file_ext, modified_date]
                writ.writerow(data)
        # print(f"📄 Report saved to {self.csv_data_path}")


    def pkl_logs_save(self, pkl_data):
        pkl_log = pkl_data
        with open(self.data_path, 'wb') as pkl_file:
            pickle.dump(pkl_log, pkl_file)
        # print(f"📦 Logs saved to {self.data_path}")

    def save_file_info(self, file_path):
        head = ['Name', 'Total Number', 'Total Size']
        with open(self.text_info_path, 'w', encoding="utf-8") as f:
            f.write("File Information Report\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n")
            f.write("-" * 50 + "\n")
            f.write(f"{' | '.join(head)}\n")
            f.write("-" * 50 + "\n")
            for ftype, data in file_path:
                count = data['count']
                size = data['size']
                f.write(f"{ftype} | {count} | {size} MB\n")
        # for ftype, data in file_path:
        #     count = data['count']
        #     size = data['size']
        #     print(f"File Type: {ftype}, Count: {count}, Size: {size} MB")
        # print(f"Saving file info for {file_path}")
        
# if __name__ == "__main__":
#     file_saving = FileSaving()
