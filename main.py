import json
import os
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

    if not achievement_list:
        raise ValueError("Invalid game name or no achievements found for the specified game.")
    
    return achievement_list

# Function to fetch descriptions from the website
def fetch_descriptions(game_name):
    web_url = "https://www.trueachievements.com/game/" + game_name.replace(' ', '-') + "/achievements"
    fetched_page = requests.get(web_url)
    beautifulsoup = BeautifulSoup(fetched_page.text, "html.parser")
    description_list = [description.get_text() for description in beautifulsoup.find_all('p', attrs={"data-bf": True})]
    if not description_list:
        raise ValueError("No achievement descriptions found.")
    
    return description_list

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

# Function to save and load previous game names
def save_game_names(game_input, filename="saved_games.json"):
    global games
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            games = json.load(f)
    else:
        games = []
    if str(game_input) not in games:
        games.append(game_input)
    with open(filename, 'w') as f:
        json.dump(games, f)

# Function to update checkbox states on change
def on_checkbox_change(checkbox_value, variable, checkbox_states):
    checkbox_states[checkbox_value] = variable.get()
    save_checkbox_states(checkbox_states)

# Function to show description in a popup
def show_description(description):
    top = tk.Toplevel()
    top.title("Description")
    top.configure(bg="#272727")

    frame = tk.Frame(top, bg="#272727")
    frame.pack(padx=10, pady=10)

    desc_label = tk.Label(frame, text=description, bg="#272727", fg="white", font=("lexend", 12), wraplength=400, justify='left')
    desc_label.pack(padx=10, pady=10)

    close_button = tk.Button(top, text="Close", command=top.destroy, bg="#272727", fg="white", font=("lexend", 12))
    close_button.pack(pady=(0, 10), padx=10)

# Function to add checkboxes dynamically to the frame
def add_checkboxes(frame, achievement_list, description_list, checkbox_states):
    sorted_achievements, sorted_descriptions = zip(*sorted(zip(achievement_list, description_list)))

    max_checkbox_width = 0
    max_desc_button_width = 0

    for achievement, description in zip(sorted_achievements, sorted_descriptions):
        checkbox_value = achievement
        checkbox_var = tk.BooleanVar()
        checkbox_var.set(checkbox_states.get(checkbox_value, False))

        sub_frame = tk.Frame(frame, bg="#272727")
        sub_frame.pack(fill='x', anchor='w', pady=1)

        sub_frame.columnconfigure(0, weight=1)
        sub_frame.columnconfigure(1, weight=1)

        checkbox = tk.Checkbutton(
            sub_frame, text=checkbox_value, variable=checkbox_var,
            command=lambda v=checkbox_value, var=checkbox_var: on_checkbox_change(v, var, checkbox_states), bg="#272727", fg="white", selectcolor="#272727", font=("lexend", 12))
        checkbox.grid(row=0, column=0, sticky='w')

        desc_button = tk.Button(sub_frame, text="Description", command=lambda d=description: show_description(d), bg="#272727", fg="white", font=("lexend", 12))
        desc_button.grid(row=0, column=1, sticky='e')

        # Update max widths
        checkbox_width = checkbox.winfo_reqwidth()
        desc_button_width = desc_button.winfo_reqwidth()
        max_checkbox_width = max(max_checkbox_width, checkbox_width)
        max_desc_button_width = max(max_desc_button_width, desc_button_width)

    # Set canvas width
    total_width = max_checkbox_width + max_desc_button_width + 3  # adding padding
    return total_width

# Function to handle mouse wheel scrolling
def on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Function to create the achievements window
def create_achievements_window(game_input, achievement_list, description_list, checkbox_states):
    root = tk.Tk()
    root.title(game_input + " Achievements")
    root.configure(bg="#272727")

    # Create canvas and scrollbar
    canvas = tk.Canvas(root, bg="#272727")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e, canvas))
    
    # Create a frame inside the canvas
    frame = tk.Frame(canvas, bg="#272727")
    frame.pack(fill=BOTH, expand=True)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Add return to menu button
    return_button = tk.Button(frame, text="Return to Menu", bg="#272727", fg="white", font=("lexend", 12), command=lambda: return_to_menu(root))
    return_button.pack()

    # Add checkboxes and get required canvas width
    canvas_width = add_checkboxes(frame, achievement_list, description_list, checkbox_states)
    canvas.config(width=canvas_width)

    root.mainloop()

# Function to return to the main menu
def return_to_menu(current_window):
    current_window.destroy()
    create_main_menu()

# Function to create the main menu window
def create_main_menu():
    menu_root = tk.Tk()
    menu_root.title("Achievement Tracker")
    menu_root.configure(bg="#272727")
    menu_root.geometry("300x200")

    frame = tk.Frame(menu_root, bg="#272727")
    frame.pack(padx=10)

    game_label = tk.Label(frame, text="Enter game name:", bg="#272727", fg="white", font=("lexend", 12))
    game_label.pack(pady=(0, 5))

    game_entry = tk.Entry(frame, font=("lexend", 12))
    game_entry.pack(pady=(0, 10))

    def on_submit():
        game_input = game_entry.get().title()
        try:
            achievement_list = fetch_achievements(game_input)
            description_list = fetch_descriptions(game_input)
            checkbox_states = load_checkbox_states()
            save_game_names(game_input, filename="saved_games.json")
            menu_root.destroy()
            create_achievements_window(game_input, achievement_list, description_list, checkbox_states)
        except ValueError as e:
            error_label.config(text=str(e))
    
    submit_button = tk.Button(frame, text="Submit", command=on_submit, bg="#272727", fg="white", font=("lexend", 12))
    submit_button.pack()

    close_button = tk.Button(menu_root, text="Close", command=menu_root.destroy, bg="#272727", fg="white", font=("lexend", 12), width=6)
    close_button.pack()

    error_label = tk.Label(frame, text="", bg="#272727", fg="red", font=("lexend", 12))
    error_label.pack()

    menu_root.mainloop()

def main():
    create_main_menu()

main()