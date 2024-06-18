import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *

# Function to fetch achievements from the website
def fetch_achievements(game_name):
    web_url = "https://www.trueachievements.com/game/" + game_name.replace(' ', '-') + "/achievements"
    fetched_page = requests.get(web_url)
    beautifulsoup = BeautifulSoup(fetched_page.text, "html.parser")
    achievement_list = [achievement.string for achievement in beautifulsoup.find_all('a', 'title')]
    return achievement_list

# Function to save the checkbox states to a file
def save_checkbox_states(checkbox_states, filename="checkbox_states.json"):
    with open(filename, 'w') as f:
        json.dump(checkbox_states, f)

# Function to load the checkbox states from a file
def load_checkbox_states(filename="checkbox_states.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

# Function to update checkbox states on change
def on_checkbox_change(checkbox_value, variable, checkbox_states):
    checkbox_states[checkbox_value] = variable.get()
    save_checkbox_states(checkbox_states)

# Function to add checkboxes dynamically to the frame
def add_checkboxes(frame, achievement_list, checkbox_states):
    for achievement in achievement_list:
        checkbox_value = achievement
        checkbox_var = tk.BooleanVar()
        checkbox_var.set(checkbox_states.get(checkbox_value, False))

        checkbox = tk.Checkbutton(
            frame, text=checkbox_value, variable=checkbox_var,
            command=lambda v=checkbox_value, var=checkbox_var: on_checkbox_change(v, var, checkbox_states))
        checkbox.pack(anchor='w')

# Function to handle mouse wheel scrolling
def on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Main function to create the GUI
def main():
    game_input = input("Enter game name: ")
    achievement_list = fetch_achievements(game_input)
    checkbox_states = load_checkbox_states()

    # Create the main window
    root = tk.Tk()
    root.title(game_input.title() + " Achievements")

    # Create a canvas widget
    canvas = tk.Canvas(root)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Bind mouse wheel scrolling to the canvas
    canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e, canvas))

    # Create a frame inside the canvas
    frame = tk.Frame(canvas)

    # Add the frame to a window in the canvas
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Add checkboxes dynamically
    add_checkboxes(frame, achievement_list, checkbox_states)

    # Start the Tkinter event loop
    root.mainloop()

main()