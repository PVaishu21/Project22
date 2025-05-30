import tkinter as tk
from tkinter import ttk
import datetime
import math
import random # Keep random for potential future use or if you want to re-add sparkles

def update_clock():
    now = datetime.datetime.now(datetime.timezone.utc)
    india_time = now + datetime.timedelta(hours=5, minutes=30) # IST is UTC+5:30

    # Update digital time
    digital_time_str = india_time.strftime("%I:%M:%S %p")
    digital_time_label.config(text=digital_time_str)

    # Update date, day, year
    date_str = india_time.strftime("%A, %B %d, %Y")
    date_label.config(text=date_str)

    # Clear canvas
    canvas.delete("all")

    # --- Draw clock background (medium color) ---
    # The main clock face circle
    canvas.create_oval(50, 50, 350, 350, fill="#d0d0d0", outline="black", width=0) # No internal outline

    # --- Add thick, highlighted clock border ---
    # Draw a slightly larger circle to create the border effect
    border_thickness = 8 # Adjust this value for thicker/thinner border
    canvas.create_oval(
        50 - border_thickness, 50 - border_thickness,
        350 + border_thickness, 350 + border_thickness,
        fill="#a0a0a0", outline="#606060", width=3 # A darker shade for highlight and outline
    )
    # Redraw the clock face on top to layer it correctly
    canvas.create_oval(50, 50, 350, 350, fill="#d0d0d0", outline="black", width=0)


    # Draw clock center
    canvas.create_oval(195, 195, 205, 205, fill="black")

    # Draw hour marks
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        x1 = 200 + 120 * math.cos(angle)
        y1 = 200 + 120 * math.sin(angle)
        x2 = 200 + 140 * math.cos(angle)
        y2 = 200 + 140 * math.sin(angle)
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    # Draw minute marks
    for i in range(60):
        if i % 5 != 0:
            angle = math.radians(i * 6 - 90)
            x1 = 200 + 130 * math.cos(angle)
            y1 = 200 + 130 * math.sin(angle)
            x2 = 200 + 135 * math.cos(angle)
            y2 = 200 + 135 * math.sin(angle)
            canvas.create_line(x1, y1, x2, y2, fill="black", width=1)

    # Get current time for analog clock
    hour = india_time.hour
    minute = india_time.minute
    second = india_time.second

    # Calculate angles for hands
    hour_angle = math.radians((hour % 12 + minute / 60) * 30 - 90)
    minute_angle = math.radians((minute + second / 60) * 6 - 90)
    second_angle = math.radians(second * 6 - 90)

    # Draw hour hand
    hour_hand_length = 80
    hx = 200 + hour_hand_length * math.cos(hour_angle)
    hy = 200 + hour_hand_length * math.sin(hour_angle)
    canvas.create_line(200, 200, hx, hy, fill="black", width=6, capstyle=tk.ROUND)

    # Draw minute hand
    minute_hand_length = 110
    mx = 200 + minute_hand_length * math.cos(minute_angle)
    my = 200 + minute_hand_length * math.sin(minute_angle)
    canvas.create_line(200, 200, mx, my, fill="black", width=4, capstyle=tk.ROUND)

    # Draw second hand
    second_hand_length = 120
    sx = 200 + second_hand_length * math.cos(second_angle)
    sy = 200 + second_hand_length * math.sin(second_angle)
    canvas.create_line(200, 200, sx, sy, fill="red", width=2, capstyle=tk.ROUND)

    # Schedule the update every 1000 milliseconds (1 second)
    window.after(1000, update_clock)

# Create the main window
window = tk.Tk()
window.title("Indian Analog and Digital Clock")
window.geometry("400x550") # Increased height for digital time and date

# Create a canvas for the analog clock
canvas = tk.Canvas(window, width=400, height=400, bg="white") # bg is white for the window's canvas area, not the clock face
canvas.pack(pady=10)

# Create a label for digital time
digital_time_label = ttk.Label(window, font=("Arial", 24, "bold"), foreground="blue")
digital_time_label.pack()

# Create a label for date, day, year
date_label = ttk.Label(window, font=("Arial", 16), foreground="green")
date_label.pack()

# Initial call to update the clock
update_clock()

# Start the Tkinter event loop
window.mainloop()