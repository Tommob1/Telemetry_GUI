# Telemetry User-Interface for ELA internship
# Started 16-07-2023

import tkinter as tk
from PIL import ImageTk, Image
import random
import threading
import time

class   TelemetryInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Simulated Telemetry UI")
        self.window.geometry("1920x1080")
        self.window.resizable(False, False)
        self.window.configure(background="black")

        # Telemetry Data Labels
        

window = tk.Tk()
print("WINDOW STARTED")
window.mainloop()