import os
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import time
import math

class TelemetryInterface:
    
    def __init__(self, window):
        self.window = window
        self.window.title("Simulated Telemetry UI")
        self.window.geometry("1920x1080")
        self.window.resizable(False, False)
        self.window.configure(background="black")

        # Display logo
        self.logo()
        self.window.after(5000, self.init_simulation)

    def logo(self):
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        logo_path = os.path.join(script_dir, 'ela_logo.png')
        logo = Image.open(logo_path)

        width = 481
        height = 312

        logo = logo.resize((width, height), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo)

        self.logo_label = tk.Label(self.window, image=logo_image, borderwidth=0, bg="black")
        self.logo_label.image = logo_image

        # Center the label in the window
        self.logo_label.grid(row=0, column=0, sticky='nsew')

        # Make the cell span across the entire window
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)


    def init_simulation(self):
        # Remove logo
        self.logo_label.grid_remove()

        # Telemetry Data Labels
        self.altitude_label = tk.Label(self.window, fg="#00FF00", bg="black", font=("Courier", 20))
        self.altitude_label.pack()

        self.velocity_label = tk.Label(self.window, fg="#00FF00", bg="black", font=("Courier", 20))
        self.velocity_label.pack()

        self.fuel_label1 = tk.Label(self.window, fg="#00FF00", bg="black", font=("Courier", 20))
        self.fuel_label1.pack()

        self.fuel_label2 = tk.Label(self.window, fg="#00FF00", bg="black", font=("Courier", 20))
        self.fuel_label2.pack()

        self.staging_label = tk.Label(self.window, fg="#00FF00", bg="black", font=("Courier", 23))
        self.staging_label.pack()

        # Telemetry Data Graphs
        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.altitude_graph = self.fig.add_subplot(311)
        self.velocity_graph = self.fig.add_subplot(312)
        self.fuel_graph = self.fig.add_subplot(313)

        self.altitude_graph.set_facecolor('black')
        self.velocity_graph.set_facecolor('black')
        self.fuel_graph.set_facecolor('black')

        self.altitude_graph.set_title('Altitude vs Time', color='#00FF00')
        self.velocity_graph.set_title('Velocity vs Time', color='#00FF00')
        self.fuel_graph.set_title('Fuel vs Time', color='#00FF00')

        self.altitude_graph.tick_params(colors='#00FF00', grid_color='#00FF00')
        self.velocity_graph.tick_params(colors='#00FF00', grid_color='#00FF00')
        self.fuel_graph.tick_params(colors='#00FF00', grid_color='#00FF00')

        self.fig.subplots_adjust(hspace=0.5)
        self.fig.patch.set_facecolor('black')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        # Time and data lists
        self.times = []
        self.altitudes = []
        self.velocities = []
        self.fuels = []

        # Update function launched in a new thread
        self.window.after(0, lambda: self.update_telemetry_data(time.time()))

    def update_telemetry_data(self, simulation_time):
        if time.time() - simulation_time <= 60:  # Run for 4 minutes
            elapsed_time = time.time() - simulation_time
            elapsed_percent = elapsed_time / 60  # Percentage of the launch time that has elapsed

            altitude_growth_factor = 0.15
            velocity_growth_factor = 0.15

            # Calculate altitude, velocity and fuel data based on the elapsed time
            altitude = 100 * (1 - math.exp(-altitude_growth_factor * elapsed_time))  # Altitude increases from 0 to 100
            velocity = 5000 * (1 - math.exp(-velocity_growth_factor * elapsed_time))  # Velocity increases from 0 to 5000
            fuel = 100 - (100 * elapsed_percent)  # Fuel decreases from 100% to 0%

			# Update the UI
            self.update_ui(altitude, velocity, fuel)
            
			# Schedule the next update
            self.window.after(100, lambda: self.update_telemetry_data(simulation_time))
        else:
            self.staging_label.config(text="STAGE SEPARATION CONFIRMED")
            print("SIMULATION COMPLETE")

    def update_ui(self, altitude, velocity, fuel):
        # Update the labels with the new data
        self.altitude_label.config(text="Altitude: %.2f KM" % altitude)
        self.velocity_label.config(text="Velocity: %.2f KM/H" % velocity)
        self.fuel_label1.config(text="Stage 1 Fuel: %.2f%%" % fuel)
        self.fuel_label2.config(text="Stage 2 Fuel: 100%")

        # Plot the new data
        self.altitude_graph.clear()
        self.altitude_graph.plot(self.times, self.altitudes, 'g')
        self.altitude_graph.set_xlim(0, 60)
        self.altitude_graph.set_ylim(0, 100)

        self.velocity_graph.clear()
        self.velocity_graph.plot(self.times, self.velocities, 'g')
        self.velocity_graph.set_xlim(0, 60)
        self.velocity_graph.set_ylim(0, 5000)

        self.fuel_graph.clear()
        self.fuel_graph.plot(self.times, self.fuels, 'g')
        self.fuel_graph.set_xlim(0, 60)
        self.fuel_graph.set_ylim(0, 100)

        self.canvas.draw()


window = tk.Tk()
print("WINDOW STARTED")
app = TelemetryInterface(window)
window.mainloop()
