import os
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
from datetime import timedelta
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

        self.telemetry_active = False

        # Display logo
        self.logo()
        self.window.after(2500, self.start_menu)
        print("WINDOW STARTED")

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

    def start_menu(self):
        if hasattr(self, 'logo_label') and self.logo_label.winfo_exists():
            self.logo_label.grid_forget()
        
        # Frame to contain the buttons
        self.button_frame = tk.Frame(self.window, bg="black")
        self.button_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Display the 'Begin Simulation' button
        self.begin_button = tk.Button(self.button_frame, text="Begin Telemetry Simulation", command=self.begin_simulation,
                                      fg="#00FF00", bg="black", font=("Courier", 24), borderwidth=0)
        self.begin_button.pack(pady=20)

        # More Information button
        self.info_button = tk.Button(self.button_frame, text="More Information", command=self.show_information,
                                     fg="#00FF00", bg="black", font=("Courier", 20), borderwidth=0)
        self.info_button.pack(pady=20)

        # Exit button to close the program
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.window.quit,
                                     fg="#FF0000", bg="black", font=("Courier", 20), borderwidth=0)
        self.exit_button.pack(pady=20)

        # Mouse hover effect
        for btn in [self.begin_button, self.info_button, self.exit_button]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#525252"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="black"))

        # Configure grid for the button frame
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

    def show_information(self):
        """Display personal information within the main window."""
        # Remove the buttons frame
        self.button_frame.place_forget()

        # New frame to contain the information
        self.info_frame = tk.Frame(self.window, bg="black")
        self.info_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Replace the placeholders with your actual details
        details = {
            "For More Information\n\n"
            "Name": "Brayden Tomlinson",
            "Email": "btommowork@gmail.com",
        }

        row = 0
        for key, value in details.items():
            tk.Label(self.info_frame, text=f"{key}: {value}", font=("Courier", 16), bg="black", fg="#00FF00").grid(row=row, column=0, padx=10, pady=5)
            row += 1

        # Back button to return to the main screen
        back_button = tk.Button(self.info_frame, text="Back", command=self.back_to_main, font=("Courier", 16), bg="#00FF00")
        back_button.grid(row=row, column=0, pady=20)

        # Mouse hover effect
        for btn in [back_button]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#525252"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#00FF00"))

    def back_to_main(self):
        """Return to the main screen."""
        # Remove the information frame
        self.info_frame.place_forget()
        # Show the buttons frame again
        self.start_menu()

    def begin_simulation(self):
        # Remove the menu (button frame in this case)
        self.button_frame.place_forget()
        # Initialize the UI for the telemetry data
        self.init_ui()
        self.telemetry_active = True

    def map1(self):
        # Get directory
        script_dir = os.path.dirname(os.path.realpath(__file__))

        map1_path = os.path.join(script_dir, 'Sat_Image.png')
        map1 = Image.open(map1_path)

        width = 900
        height = 600

        map1 = map1.resize((width, height), Image.LANCZOS)
        map1_image = ImageTk.PhotoImage(map1)

        # Create a canvas with size of the image plus the border
        canvas_width = width + 4  # 2px border on each side
        canvas_height = height + 4  # 2px border on each side

        self.map1_canvas = tk.Canvas(self.window, width=canvas_width, height=canvas_height, bg='green', highlightthickness=0)
        self.map1_canvas.place(x=20, y=400)

        # Place the image inside the canvas
        self.map1_canvas.create_image(2, 2, anchor=tk.NW, image=map1_image)
        self.map1_canvas.image = map1_image

    def add_dot(self, x, y):
        dot_radius = 3
        self.map1_canvas.create_oval(x-dot_radius, y-dot_radius, x+dot_radius, y+dot_radius, fill='#00FF00')


    def init_ui(self):

        # Remove logo if it exists
        if hasattr(self, 'logo_label') and self.logo_label.winfo_exists():
            self.logo_label.grid_remove()

        # Set general settings for all the labels
        settings = {"fg": "#00FF00", "bg": "black", "font": ("Courier", 20)}

        # Frame for Telemetry Data Labels
        frame_labels = tk.Frame(self.window, bg="black")
        frame_labels.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.altitude_label = tk.Label(frame_labels, text="Altitude:", **settings)
        self.altitude_label.grid(row=1, column=0, sticky="w", padx=5, pady=10)

        self.velocity_label = tk.Label(frame_labels, text="Velocity:", width=25, anchor="w", **settings)
        self.velocity_label.grid(row=2, column=0, sticky="w", padx=5, pady=10)

        self.fuel_label1 = tk.Label(frame_labels, text="Stage 1 Fuel:", **settings)
        self.fuel_label1.grid(row=3, column=0, sticky="w", padx=5, pady=10)

        self.fuel_label2 = tk.Label(frame_labels, text="Stage 2 Fuel:", **settings)
        self.fuel_label2.grid(row=4, column=0, sticky="w", padx=5, pady=10)

        self.staging_label = tk.Label(frame_labels, text="", fg="#00FF00", bg="black", font=("Courier", 25))
        self.staging_label.grid(row=2, column=4, columnspan=2, sticky="w", padx=5, pady=10)

        # Spacecraft Status static label
        self.status_label_static = tk.Label(frame_labels, text="Vehicle Status:", fg="#00FF00", bg="black", font=("Courier", 23))
        self.status_label_static.grid(row=0, column=4, sticky="w", padx=5, pady=10)

        self.status_message = tk.StringVar()

        # Dynamic status message label
        self.status_label_dynamic = tk.Label(frame_labels, textvariable=self.status_message, fg="#00FF00", bg="black", font=("Courier", 23), width=25, anchor="w")
        self.status_label_dynamic.grid(row=1, column=4, sticky="w", padx=5, pady=10)

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

        self.altitude_graph.set_xlim(0, 60)
        self.altitude_graph.set_ylim(0, 100)
        self.altitude_graph.set_title('Altitude(KM):', color='#00FF00')

        self.velocity_graph.set_xlim(0, 60)
        self.velocity_graph.set_ylim(0, 5500)
        self.velocity_graph.set_title('Velocity(KM/H):', color='#00FF00')

        self.fuel_graph.set_xlim(0, 60)
        self.fuel_graph.set_ylim(0, 100)
        self.fuel_graph.set_title('Stage 1 Fuel(%):', color='#00FF00')

        self.altitude_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.altitude_graph.transAxes, color='#00FF00', linewidth=2)
        self.velocity_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.velocity_graph.transAxes, color='#00FF00', linewidth=2)
        self.fuel_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.fuel_graph.transAxes, color='#00FF00', linewidth=2)

        self.altitude_graph.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00FF00')
        self.velocity_graph.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00FF00')
        self.fuel_graph.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00FF00')

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graphs)
        self.fig.tight_layout(pad=4)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Adjust the size of the grid cells
        for i in range(2):
            self.window.grid_rowconfigure(i, weight=1)
            self.window.grid_columnconfigure(i, weight=1)

        # Add the "Menu" button to the bottom-left corner
        self.menu_button = tk.Button(self.window, text="Menu",
                                     command=self.return_to_menu,
                                     fg="#00FF00", bg="black", font=("Courier", 15), borderwidth=0)
        self.menu_button.place(x=10, y=self.window.winfo_height() - 40)

        # Mouse hover effect
        for btn in [self.menu_button]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#525252"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="black"))

        # Time and data lists
        self.times = []
        self.altitudes = []
        self.velocities = []
        self.fuels = []

        self.simulation_start_time = time.time() # Stores the simulation start time

        # Initialize the timer label for the countdown
        self.timer_label = tk.Label(frame_labels, text="T- 00:00:10", fg="#00FF00", bg="black", font=("Courier", 30))
        self.timer_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)

        # Center the label in the window for the Y-axis
        self.window.grid_rowconfigure(0, weight=1)

        # Start the countdown timer
        self.start_countdown()

    def start_countdown(self):
        self.remaining_time = 10  # 10 seconds for the countdown
        self.countdown()

    def countdown(self):
        self.map1()
        self.add_dot(345, 300)
        if self.remaining_time >= 0:
            # Convert the remaining time into HH:MM:SS format
            mins, sec = divmod(self.remaining_time, 60)
            hours, mins = divmod(mins, 60)
            time_str = "T- {:02d}:{:02d}:{:02d}".format(hours, mins, sec)

            # Check for specific times to display messages
            if self.remaining_time == 10:
                self.status_message.set("Engine Startup")
                print("Engine Startup")
            elif self.remaining_time == 1:
                self.status_message.set("Engine Ignition")
                print("Engine Ignition")

            # Update the timer label
            self.timer_label.config(text=time_str)

            # Schedule the function to run after 1 second
            self.countdown_id = self.window.after(1000, self.countdown)

            # Decrement the remaining time
            self.remaining_time -= 1
        else:
            # Once the countdown is done, remove the countdown timer label
            self.timer_label.grid_forget()
        
            # Display the T+0 message
            self.status_message.set("Engine Full Power")
            print("Engine Full Power")

            # Initialize the simulation start time
            self.simulation_start_time = time.time()

            # Reset the label's text to T+ 00:00:00
            self.timer_label.config(text="T+ 00:00:00")
        
            # Make the label visible again on the grid
            self.timer_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)

            # Start the telemetry data function
            self.update_telemetry_data(self.simulation_start_time)

    def update_telemetry_data(self, simulation_time):
        # Stop updating if telemetry is not active
        if not self.telemetry_active:
            return

        if time.time() - simulation_time <= 60:  # Run for 2 minutes
            elapsed_time = time.time() - simulation_time
            elapsed_percent = elapsed_time / 60  # Percentage of the launch time that has elapsed

            # Update Vehicle Status Messages
            if round(elapsed_time) == 2:
                self.status_message.set("Liftoff")
            elif round(elapsed_time) == 10:
                self.status_message.set("Engine Throttle Down")
            elif round(elapsed_time) == 20:
                self.status_message.set("Max-Q")
            elif round(elapsed_time) == 30:
                self.status_message.set("Engine Throttle Up")
            elif round(elapsed_time) == 40:
                self.status_message.set("Engine Full Power")
            elif round(elapsed_time) == 55:
                self.status_message.set("Engine Throttle Down")
            elif round(elapsed_time) == 58:
                self.status_message.set("Stage Separation")

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
            self.telemetry_update_id = self.window.after(10, lambda: self.update_telemetry_data(simulation_time))
        else:
            self.staging_label.config(text="STAGE SEPARATION CONFIRMED")
            print("SIMULATION COMPLETE")

    def update_ui(self, altitude, velocity, fuel):
        # Append the new data to the lists
        self.times.append(time.time() - self.simulation_start_time) # Using the simulation start time to get relative time
        self.altitudes.append(altitude)
        self.velocities.append(velocity)
        self.fuels.append(fuel)

        self.map1()
        self.add_dot(345, 300)

        elapsed_time = timedelta(seconds=int(self.times[-1]))

        # Update the T+ timer on the UI
        hours, remainder = divmod(elapsed_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_label.config(text=f"T+ {hours:02}:{minutes:02}:{seconds:02}")

        # Update the labels with the new data
        self.timer_label.config(text=f"T+ {elapsed_time}")
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

        self.altitude_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.altitude_graph.transAxes, color='#00FF00', linewidth=2)
        self.velocity_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.velocity_graph.transAxes, color='#00FF00', linewidth=2)
        self.fuel_graph.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], transform=self.fuel_graph.transAxes, color='#00FF00', linewidth=2)

        self.altitude_graph.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00FF00')
        self.velocity_graph.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00FF00')
        self.fuel_graph.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00FF00')


        self.canvas.draw()

    def return_to_menu(self):
        self.telemetry_active = False
        # Cancel scheduled updates if necessary
        if hasattr(self, 'telemetry_update_id'):
            self.window.after_cancel(self.telemetry_update_id)
        if hasattr(self, 'countdown_id'):
            self.window.after_cancel(self.countdown_id)
    
        # Start the main menu again
        self.start_menu()
    
        # Hide and destroy telemetry-related widgets
        self.menu_button.place_forget()
        self.canvas.get_tk_widget().pack_forget()
        for widget in self.window.winfo_children():
            if widget != self.button_frame:  # Make sure not to destroy the start menu you just displayed.
                widget.destroy()

window = tk.Tk()
app = TelemetryInterface(window)
window.mainloop()