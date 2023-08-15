import tkinter as tk
from PIL import Image, ImageTk

def display_image_with_dot(image_path, x, y):
    """
    Display an image with a red dot at the specified (x, y) coordinate.
    """
    # Initialize the main window
    root = tk.Tk()
    root.title("Image with Red Dot")

    # Load the image using PIL and convert to ImageTk format
    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)

    # Create a canvas for the image
    canvas = tk.Canvas(root, width=img.width, height=img.height)
    canvas.pack()

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    # Draw a red dot on the given x, y coordinate
    dot_radius = 3
    canvas.create_oval(x-dot_radius, y-dot_radius, x+dot_radius, y+dot_radius, fill='red')

    root.mainloop()

# Test with a sample image and coordinate (50, 50)
# Note: Replace 'sample.jpg' with the path to your image
# display_image_with_dot('sample.jpg', 50, 50)

# The function call is commented out for now. Uncomment it when you want to run.
# Make sure you have an image named 'sample.jpg' in the directory or replace it with your image path.

"Function 'display_image_with_dot' is defined."

display_image_with_dot('C:\\Users\\Pc\\Desktop\\Telemetry_UI\\TESTS\\Test_Image.png', 530, 420)
