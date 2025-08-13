import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class SpeedMeter(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(padx=20, pady=20, fill='x')

        # Meter widget
        self.meter = ttk.Meter(
            self,
            amounttotal=100,   # Max value (e.g. 100 MB/sec)
            amountused=0,
            metersize=200,
            bootstyle='success',
            subtext='MB/s'
        )
        self.meter.pack(pady=10)

        # Button to simulate scanning
        ttk.Button(self, text="Start Scan", command=self.start_scan).pack(pady=5)

    def start_scan(self):
        total_data = 500  # total MB to scan (example)
        scanned = 0
        last_time = time.time()

        for _ in range(50):  # simulate 50 steps
            time.sleep(0.1)  # scanning delay
            scanned += 10    # MB scanned in this step

            # Calculate speed
            current_time = time.time()
            elapsed = current_time - last_time
            last_time = current_time
            speed = 10 / elapsed  # MB/s

            # Update meter
            self.meter.configure(amountused=speed)

            # Also update subtext dynamically
            self.meter.configure(subtext=f"{speed:.2f} MB/s")

if __name__ == "__main__":
    app = ttk.Window(themename="superhero")
    SpeedMeter(app)
    app.mainloop()
