import pandas as pd
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *

gameInput = input("Enter game name: ")
web_url = "https://www.trueachievements.com/game/" + gameInput + "/achievements"
web_url = web_url.replace(' ', '-')
fetched_page = requests.get(web_url)

beautifulsoup = BeautifulSoup(fetched_page.text, "html.parser")
achievement_list = []

for achievement in beautifulsoup.find_all('a', 'title'):
    achievement_list.append(achievement.string)


def on_checkbox_change(checkbox_value, variable):
    return False

def add_checkboxes(frame):
    for i in range(len(achievement_list)):
        checkbox_value = str(achievement_list[i])
        checkbox_var = tk.BooleanVar()
        checkbox_var.set(False)  # Set the initial state (unchecked)

        checkbox = tk.Checkbutton(
            frame, text=checkbox_value, variable=checkbox_var,
            command=lambda v=checkbox_value: on_checkbox_change(v, checkbox_var))
        checkbox.pack(anchor='w')

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Create the main window
root = tk.Tk()
root.title(gameInput.title() + " Achievements")

# Create a canvas widget
canvas = tk.Canvas(root)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Add a scrollbar widget
scrollbar = tk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)


# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# Bind mouse wheel scrolling to the canvas
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Create a frame inside the canvas
frame = tk.Frame(canvas)

# Add the frame to a window in the canvas
canvas.create_window((0, 0), window=frame, anchor='nw')

# Add checkboxes dynamically
add_checkboxes(frame)

# Start the Tkinter event loop
root.mainloop()