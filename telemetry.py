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
        while time.time() - simulation_time <= 60: # Run sim for 1 minute
            # Altitude, Velocity and stage 1 fuel simulated data
            altitude = random.uniform(0, 100)
            velocity = random.uniform(0, 5000)
            fuel = max(100 - ((time.time() - simulation_time) / 60 * 100), 0) # Fuel decrease over simulation time

            # Update labels with simulated data
            self.altitude_label.config(text="Altitude: %.2f KM" % altitude)
            self.velocity_label.config(text="Velocity: %.2f KM/H" % velocity)
            self.fuel_label1.config(text="Fuel: %.2f%%" % fuel)

            # Update buffer
            time.sleep(0.1)

        print("SIMULATION FINISHED")

window = tk.Tk()
print("WINDOW STARTED")
app = TelemetryInterface(window)
window.mainloop()