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
        self.altitude_label = tk.Label(window, fg="white", bg="black", font=("Helvetica", 16))
        self.altitude_label.pack()

        self.velocity_label = tk.Label(window, fg="white", bg="black", font=("Helvetica", 16))
        self.velocity_label.pack()

        self.fuel_label1 = tk.Label(window, fg="white", bg="black", font=("Helvetica", 16))

        #Update function launched in a new thread
        threading.Thread(target=self.update_telemetry_data).start()

    def update_telemetry_data(self):
        simulation_time = time.time()
        while time.time() - simulation_time <= 60:  # Run for 1 minute
            elapsed_time = time.time() - simulation_time
            elapsed_percent = elapsed_time / 60  # Percentage of the launch time that has elapsed

            # Calculate altitude, velocity and fuel data based on the elapsed time
            altitude = 100 * elapsed_percent  # Altitude increases from 0 to 100,000
            velocity = 5000 * elapsed_percent  # Velocity increases from 0 to 5,000
            fuel = 100 - (100 * elapsed_percent)  # Fuel decreases from 100% to 0%

            # Update the labels with the new data
            self.altitude_label.config(text="Altitude: %.2f KM" % altitude)
            self.velocity_label.config(text="Velocity: %.2f KM/H" % velocity)
            self.fuel_label1.config(text="Fuel: %.2f%%" % fuel)

            # Wait for 0.1 second before updating again
            time.sleep(0.1)

        print("SIMULATION FINISHED")

window = tk.Tk()
print("WINDOW STARTED")
app = TelemetryInterface(window)
window.mainloop()