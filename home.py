import tkinter as tk
from configparser import ConfigParser
import os

def create_default_config():
    config = ConfigParser()
 
    # Add sections and key-value pairs
    config['boid'] = {
        'population': 50, 
        'colour': 'blue'
        }
    
    config['genetic_algorithm'] = {
        'generations': 90,  
        'mutation_rate': 0.03,
        }
 
    # Write the configuration to a file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# looks for config file, if not found creates a default config file
if os.path.exists('config.ini'):
    print("Loading config.ini...")
else:
    print("Config file not found...")
    print("Creating config.ini...")
    create_default_config()
    print("Config created...")

def boid_options():
    print("boid options...")

    config = ConfigParser()
    config.read('config.ini')

    print(config['boid']['population'])

def ga_options():
    print("ga options...")

def data_options():
    print("data options...")

def toggle_checkbox():
    # Toggle the state of the checkbox
    checkbox_state.set(not checkbox_state.get())

def run_simulation_click():
    print("Button clicked")

root = tk.Tk()
root.title("Genetic Algorithm Boid Simulation")
root.geometry("400x400")


my_menu = tk.Menu(root)

root.config(menu=my_menu)

#Create a menu item boid
boid_menu = tk.Menu(my_menu)
my_menu.add_cascade(label='Boid', menu=boid_menu)
boid_menu.add_command(label='Options...', command=boid_options)

#Create a menu item genetic algorithm
ga_menu = tk.Menu(my_menu)
my_menu.add_cascade(label='GA', menu=ga_menu)
ga_menu.add_command(label='Options...', command=ga_options)


#Create a menu item data
data_menu = tk.Menu(my_menu)
my_menu.add_cascade(label='Data', menu=data_menu)
data_menu.add_command(label='Options...', command=data_options)

# Create a label and place it in the grid
label1 = tk.Label(root, text="Show Simulation Graphics")
label1.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Create a checkbox and place it in the grid
checkbox_state = tk.BooleanVar()
checkbox1 = tk.Checkbutton(root, variable=tk.BooleanVar(), command=toggle_checkbox)
checkbox1.grid(row=0, column=1, padx=10, pady=5, sticky="e")

# Create a label and place it in the grid
label2 = tk.Label(root, text="Boid Profile")
label2.grid(row=1, column=0, padx=10, pady=5, sticky="w")

boid_profile = tk.StringVar()
boid_profile.set("Boid Profile 1") # set default value
drop = tk.OptionMenu(root, boid_profile, 'Boid Profile 1', 'Boid Profile 2')
drop.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Create a label and place it in the grid
label3 = tk.Label(root, text="Genetic Algorithm Profile")
label3.grid(row=2, column=0, padx=10, pady=5, sticky="w")

boid_profile = tk.StringVar()
boid_profile.set("GA Profile 1") # set default value
drop = tk.OptionMenu(root, boid_profile, 'GA Profile 1', 'GA Profile 2')
drop.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Create a button and place it in the window
button = tk.Button(root, text="Run Simulation", command=run_simulation_click)
button.grid(row=3, column=0, padx=5, pady=5, sticky="e")

root.mainloop()