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
        self.window.resizable(True, True)
        self.window.configure(background="black")
        self.window.attributes('-fullscreen', True)

        # Display logo
        self.logo()
        self.window.after(2500, self.init_simulation)
        print("""███████╗██╗      █████╗ 
██╔════╝██║     ██╔══██╗
█████╗  ██║     ███████║
██╔══╝  ██║     ██╔══██║
███████╗███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝""")

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

        # Set general settings for all the labels
        settings = {"fg": "#00FF00", "bg": "black", "font": ("Courier", 20)}

        # Frame for Telemetry Data Labels
        frame_labels = tk.Frame(self.window, bg="black")
        frame_labels.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.timer_label = tk.Label(frame_labels, text="T+", **settings)
        self.timer_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)

    
        self.altitude_label = tk.Label(frame_labels, text="Altitude:", **settings)
        self.altitude_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.velocity_label = tk.Label(frame_labels, text="Velocity:", **settings)
        self.velocity_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.fuel_label1 = tk.Label(frame_labels, text="Fuel 1:", **settings)
        self.fuel_label1.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.fuel_label2 = tk.Label(frame_labels, text="Fuel 2:", **settings)
        self.fuel_label2.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.staging_label = tk.Label(frame_labels, text="", fg="#00FF00", bg="black", font=("Courier", 23))
        self.staging_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Frame for Telemetry Data Graphs
        frame_graphs = tk.Frame(self.window, bg="black")
        frame_graphs.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.fig = Figure(figsize=(8, 10), dpi=100)
        self.altitude_graph = self.fig.add_subplot(311)
        self.velocity_graph = self.fig.add_subplot(312)
        self.fuel_graph = self.fig.add_subplot(313)

        self.altitude_graph.set_facecolor('black')
        self.velocity_graph.set_facecolor('black')
        self.fuel_graph.set_facecolor('black')

        self.altitude_graph.tick_params(colors='#00FF00', grid_color='#00FF00')
        self.velocity_graph.tick_params(colors='#00FF00', grid_color='#00FF00')
        self.fuel_graph.tick_params(colors='#00FF00', grid_color='#00FF00')

        self.fig.patch.set_facecolor('black')

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graphs)
        self.fig.tight_layout(pad=4)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Adjust the size of the grid cells
        for i in range(2):
            self.window.grid_rowconfigure(i, weight=1)
            self.window.grid_columnconfigure(i, weight=1)

        # Time and data lists
        self.times = []
        self.altitudes = []
        self.velocities = []
        self.fuels = []

        self.simulation_start_time = time.time() # Stores the simulation start time

        # Update function launched in a new thread
        self.window.after(0, lambda: self.update_telemetry_data(self.simulation_start_time))

    def update_telemetry_data(self, simulation_time):
        global elapsed_time
        if time.time() - simulation_time <= 60:  # Run for 2 minutes
            elapsed_time = time.time() - simulation_time
            elapsed_percent = elapsed_time / 60  # Percentage of the launch time that has elapsed

            altitude_growth_factor = 0.01
            velocity_growth_factor = 0.012

            # Calculate altitude, velocity and fuel data based on the elapsed time
            #SIMULATED ALTITUDE AND VELOCITY RUN EXPONETIALLY SLOWER. CHANGE TO BE EXPONETIALLY FASTER
            altitude = 100 * (math.exp(altitude_growth_factor * elapsed_time) - 1)  # Altitude increases from 0 to 100
            velocity = 5000 * (math.exp(velocity_growth_factor * elapsed_time) - 1)  # Velocity increases from 0 to 5000
            fuel = 100 - (100 * elapsed_percent)  # Fuel decreases from 100% to 0%

			# Update the UI
            self.update_ui(altitude, velocity, fuel)
            
			# Schedule the next update
            self.window.after(10, lambda: self.update_telemetry_data(simulation_time))
        else:
            self.staging_label.config(text="STAGE SEPARATION CONFIRMED")
            print("SIMULATION COMPLETE")

    def update_ui(self, altitude, velocity, fuel):
        # Append the new data to the lists
        self.times.append(time.time() - self.simulation_start_time) # Using the simulation start time to get relative time
        self.altitudes.append(altitude)
        self.velocities.append(velocity)
        self.fuels.append(fuel)

        # Update the labels with the new data
        self.timer_label.config(text="T+ %.2f seconds" % elapsed_time)
        self.altitude_label.config(text="Altitude: %.2f KM" % altitude)
        self.velocity_label.config(text="Velocity: %.2f KM/H" % velocity)
        self.fuel_label1.config(text="Stage 1 Fuel: %.2f%%" % fuel)
        self.fuel_label2.config(text="Stage 2 Fuel: 100%")

        # Plot the new data
        self.altitude_graph.clear()
        self.altitude_graph.plot(self.times, self.altitudes, 'g')
        self.altitude_graph.set_xlim(0, 60)
        self.altitude_graph.set_ylim(0, 100)
        self.altitude_graph.set_title('Altitude(KM):', color='#00FF00')

        self.velocity_graph.clear()
        self.velocity_graph.plot(self.times, self.velocities, 'g')
        self.velocity_graph.set_xlim(0, 60)
        self.velocity_graph.set_ylim(0, 5500)
        self.velocity_graph.set_title('Velocity(KM/H):', color='#00FF00')

        self.fuel_graph.clear()
        self.fuel_graph.plot(self.times, self.fuels, 'g')
        self.fuel_graph.set_xlim(0, 60)
        self.fuel_graph.set_ylim(0, 100)
        self.fuel_graph.set_title('Stage 1 Fuel(%):', color='#00FF00')

        # Add these lines after you have setup your subplot and before you draw the canvas

        self.altitude_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.altitude_graph.transAxes, color='#00FF00', linewidth=2)
        self.velocity_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.velocity_graph.transAxes, color='#00FF00', linewidth=2)
        self.fuel_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.fuel_graph.transAxes, color='#00FF00', linewidth=2)

        self.canvas.draw()

window = tk.Tk()
print("WINDOW STARTED")
app = TelemetryInterface(window)
window.mainloop()
