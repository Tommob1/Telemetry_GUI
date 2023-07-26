import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

class TelemetryInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Simulated Telemetry UI")
        self.window.geometry("800x800")
        self.window.resizable(False, False)
        self.window.configure(background="black")

        # Telemetry Data Labels
        self.altitude_label = tk.Label(window, fg="green", bg="black", font=("Courier", 20))
        self.altitude_label.pack()

        self.velocity_label = tk.Label(window, fg="green", bg="black", font=("Courier", 20))
        self.velocity_label.pack()

        self.fuel_label1 = tk.Label(window, fg="green", bg="black", font=("Courier", 20))
        self.fuel_label1.pack()

        self.fuel_label2 = tk.Label(window, fg="green", bg="black", font=("Courier", 20))
        self.fuel_label2.pack()

        self.staging_label = tk.Label(window, fg="green", bg="black", font=("Courier", 23))
        self.staging_label.pack()

        # Telemetry Data Graphs
        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.altitude_graph = self.fig.add_subplot(311)
        self.velocity_graph = self.fig.add_subplot(312)
        self.fuel_graph = self.fig.add_subplot(313)

        self.altitude_graph.set_facecolor('black')
        self.velocity_graph.set_facecolor('black')
        self.fuel_graph.set_facecolor('black')

        self.altitude_graph.set_title('Altitude vs Time', color='green')
        self.velocity_graph.set_title('Velocity vs Time', color='green')
        self.fuel_graph.set_title('Fuel vs Time', color='green')

        self.altitude_graph.tick_params(colors='green', grid_color='green')
        self.velocity_graph.tick_params(colors='green', grid_color='green')
        self.fuel_graph.tick_params(colors='green', grid_color='green')

        self.fig.subplots_adjust(hspace=0.5)
        self.fig.patch.set_facecolor('black')

        self.canvas = FigureCanvasTkAgg(self.fig, master=window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        # Time and data lists
        self.times = []
        self.altitudes = []
        self.velocities = []
        self.fuels = []

        # Update function launched in a new thread
        threading.Thread(target=self.update_telemetry_data).start()

    def update_telemetry_data(self):
        simulation_time = time.time()
        while time.time() - simulation_time <= 240:  # Run for 4 minutes
            elapsed_time = time.time() - simulation_time
            elapsed_percent = elapsed_time / 240  # Percentage of the launch time that has elapsed

            # Calculate altitude, velocity and fuel data based on the elapsed time
            altitude = 100 * elapsed_percent  # Altitude increases from 0 to 100
            velocity = 5000 * elapsed_percent  # Velocity increases from 0 to 5000
            fuel = 100 - (100 * elapsed_percent)  # Fuel decreases from 100% to 0%

            # Update the labels with the new data
            self.altitude_label.config(text="Altitude: %.2f KM" % altitude)
            self.velocity_label.config(text="Velocity: %.2f KM/H" % velocity)
            self.fuel_label1.config(text="Stage 1 Fuel: %.2f%%" % fuel)
            self.fuel_label2.config(text="Stage 2 Fuel: 100%")

            # Append the new data to the lists
            self.times.append(elapsed_time)
            self.altitudes.append(altitude)
            self.velocities.append(velocity)
            self.fuels.append(fuel)

            # Plot the new data
            self.altitude_graph.clear()
            self.altitude_graph.plot(self.times, self.altitudes, 'g')
            self.altitude_graph.set_xlim(0, 240)
            self.altitude_graph.set_ylim(0, 100)

            self.velocity_graph.clear()
            self.velocity_graph.plot(self.times, self.velocities, 'g')
            self.velocity_graph.set_xlim(0, 240)
            self.velocity_graph.set_ylim(0, 5000)

            self.fuel_graph.clear()
            self.fuel_graph.plot(self.times, self.fuels, 'g')
            self.fuel_graph.set_xlim(0, 240)
            self.fuel_graph.set_ylim(0, 100)

            self.canvas.draw()

            # Wait for 0.1 second before updating again
            time.sleep(0.01)

        print("SIMULATION FINISHED")
        self.staging_label.config(text="STAGE SEPERATION CONFIRMED")

window = tk.Tk()
print("WINDOW STARTED")
app = TelemetryInterface(window)
window.mainloop()
