import tkinter as tk
from configparser import ConfigParser
import os

boid_profile_path = 'boid_profiles.ini'

boid_selected_profile = None

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

    # Read config data
    config = ConfigParser()
    config.read(boid_profile_path)

    def boid_profile_save(saveData):
        print("Saving profile...")

        global boid_selected_profile

        print(boid_selected_profile)

        config = ConfigParser()
        config.read(boid_profile_path)

        selected_item = boid_selected_profile## current problem is that we dont know what index was last selected

        if selected_item == '' or selected_item == None:
            print("Error: No selected profile")
            return

        # Iterate over all keys and values in the dictionary
        for value in saveData:
            if value == '' or value == None:
                print("Error: Empty value in profile")
                return

        config[selected_item]['PROFILE_ID'] = saveData[0]
        config[selected_item]['NUM_BOIDS'] = saveData[1]
        config[selected_item]['MAX_SPEED'] = saveData[2]
        config[selected_item]['NEIGHBOR_RADIUS'] = saveData[3]
        config[selected_item]['ALIGNMENT_WEIGHT'] = saveData[4]
        config[selected_item]['COHESION_WEIGHT'] = saveData[5]
        config[selected_item]['SEPARATION_WEIGHT'] = saveData[6]
        config[selected_item]['AVOID_RADIUS'] = saveData[7]
        config[selected_item]['MAX_AVOID_FORCE'] = saveData[8]

        # Write the changes back to the config file
        with open(boid_profile_path, 'w') as config_file:
            config.write(config_file)
        print("Boid profile saved")

    def on_select(event):
        global boid_selected_profile

        # Read config data again just in case of an update
        config = ConfigParser()
        config.read(boid_profile_path)

        # Get the currently selected item from the listbox
        selected_index = my_listbox.curselection()
        if selected_index:
            selected_item = my_listbox.get(selected_index[0])
            # Retrieve configuration data for the selected item
            try:
                target_profile = selected_item
                boid_config = config[selected_item]
                boid_selected_profile = selected_item
                print(f"selected item:{boid_selected_profile}")
                entry_PROFILE_ID        .delete(0, tk.END)
                entry_NUM_BOIDS         .delete(0, tk.END)  # Clear previous value        
                entry_MAX_SPEED         .delete(0, tk.END)
                entry_NEIGHBOR_RADIUS   .delete(0, tk.END)
                entry_ALIGNMENT_WEIGHT  .delete(0, tk.END)
                entry_COHESION_WEIGHT   .delete(0, tk.END)
                entry_SEPARATION_WEIGHT .delete(0, tk.END)
                entry_AVOID_RADIUS      .delete(0, tk.END)
                entry_MAX_AVOID_FORCE   .delete(0, tk.END)

                entry_PROFILE_ID        .insert(tk.END, boid_config.get('PROFILE_ID', ''))
                entry_NUM_BOIDS         .insert(tk.END, boid_config.get('NUM_BOIDS', ''))  # Insert value
                entry_MAX_SPEED         .insert(tk.END, boid_config.get('MAX_SPEED', ''))
                entry_NEIGHBOR_RADIUS   .insert(tk.END, boid_config.get('NEIGHBOR_RADIUS', ''))
                entry_ALIGNMENT_WEIGHT  .insert(tk.END, boid_config.get('ALIGNMENT_WEIGHT', ''))
                entry_COHESION_WEIGHT   .insert(tk.END, boid_config.get('COHESION_WEIGHT', ''))
                entry_SEPARATION_WEIGHT .insert(tk.END, boid_config.get('SEPARATION_WEIGHT', ''))
                entry_AVOID_RADIUS      .insert(tk.END, boid_config.get('AVOID_RADIUS', ''))
                entry_MAX_AVOID_FORCE   .insert(tk.END, boid_config.get('MAX_AVOID_FORCE', ''))
                return target_profile
            except KeyError:
                tk.messagebox.showerror("Error", f"No configuration found for '{selected_item}'")

    def on_closing():
        print("Closing boid options...")

        global boid_selected_profile
        boid_selected_profile = None

        popup.destroy()  # Close the window
    
    popup = tk.Toplevel()
    popup.title("Boid Options")
    popup.geometry("600x300")
    # Bind the function to the window's close event
    popup.protocol("WM_DELETE_WINDOW", on_closing)

    # Disable original window while popup is open
    popup.grab_set()

    # Create frames for inner grids
    frame1 = tk.Frame(popup, borderwidth=1, relief="solid")
    frame2 = tk.Frame(popup, borderwidth=1, relief="solid")
    frame3 = tk.Frame(popup, borderwidth=1, relief="solid")

    # Layout main grid
    frame1.grid(row=0, column=0, padx=10, pady=5)
    frame2.grid(row=0, column=1, padx=10, pady=5)
    frame3.grid(row=0, column=2, padx=10, pady=5)

    # Listbox
    my_listbox = tk.Listbox(frame2)
    my_listbox.grid(row=0, column=0, padx=10, pady=5)

    # Populate listbox with profile names
    for profile in config.sections():
        my_listbox.insert(tk.END, profile)

    # Entry for NUM_BOIDS
    label_PROFILE_ID        = tk.Label(frame3, text="Profile ID:")
    label_NUM_BOIDS         = tk.Label(frame3, text="Number of:")
    label_MAX_SPEED         = tk.Label(frame3, text="Max Speed:")
    label_NEIGHBOR_RADIUS   = tk.Label(frame3, text="Neighbor Radius:")
    label_ALIGNMENT_WEIGHT  = tk.Label(frame3, text="Alignment Weight:")
    label_COHESION_WEIGHT   = tk.Label(frame3, text="Cohesion Weight:")
    label_SEPARATION_WEIGHT = tk.Label(frame3, text="Separation Weight:")
    label_AVOID_RADIUS      = tk.Label(frame3, text="Avoid Radius:")
    label_MAX_AVOID_FORCE   = tk.Label(frame3, text="Avoid Force:")
    
    entry_PROFILE_ID        = tk.Entry(frame3, width=30)
    entry_NUM_BOIDS         = tk.Entry(frame3, width=30)
    entry_MAX_SPEED         = tk.Entry(frame3, width=30)
    entry_NEIGHBOR_RADIUS   = tk.Entry(frame3, width=30)
    entry_ALIGNMENT_WEIGHT  = tk.Entry(frame3, width=30)
    entry_COHESION_WEIGHT   = tk.Entry(frame3, width=30)
    entry_SEPARATION_WEIGHT = tk.Entry(frame3, width=30)
    entry_AVOID_RADIUS      = tk.Entry(frame3, width=30)
    entry_MAX_AVOID_FORCE   = tk.Entry(frame3, width=30)


    # Add a close button to the popup window
    new_button = tk.Button(frame1, text="New", command=on_closing)

    save_button = tk.Button(
        frame1, 
        text="Save", 
        command=lambda: boid_profile_save(
            [
                entry_PROFILE_ID.get(),
                entry_NUM_BOIDS.get(),
                entry_MAX_SPEED.get(),
                entry_NEIGHBOR_RADIUS.get(),
                entry_ALIGNMENT_WEIGHT.get(),
                entry_COHESION_WEIGHT.get(),
                entry_SEPARATION_WEIGHT.get(),
                entry_AVOID_RADIUS.get(),
                entry_MAX_AVOID_FORCE.get()
                ]
        )
        )



    delete_button = tk.Button(frame1, text="Delete", command=on_closing)
    close_button = tk.Button(frame1, text="Close", command=on_closing)

    new_button.grid(row=0, column=0, padx=10, pady=5)
    save_button.grid(row=1, column=0, padx=10, pady=5)
    delete_button.grid(row=2, column=0, padx=10, pady=5)
    close_button.grid(row=3, column=0, padx=10, pady=5)
    

    # placing all the tkinter elements
    label_PROFILE_ID        .grid(row=0, column=0, padx=10, pady=5, sticky="e")
    label_NUM_BOIDS         .grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_MAX_SPEED         .grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_NEIGHBOR_RADIUS   .grid(row=3, column=0, padx=10, pady=5, sticky="e")
    label_ALIGNMENT_WEIGHT  .grid(row=4, column=0, padx=10, pady=5, sticky="e")
    label_COHESION_WEIGHT   .grid(row=5, column=0, padx=10, pady=5, sticky="e")
    label_SEPARATION_WEIGHT .grid(row=6, column=0, padx=10, pady=5, sticky="e")
    label_AVOID_RADIUS      .grid(row=7, column=0, padx=10, pady=5, sticky="e")
    label_MAX_AVOID_FORCE   .grid(row=8, column=0, padx=10, pady=5, sticky="e")

    entry_PROFILE_ID        .grid(row=0, column=1, padx=10, pady=5, sticky="w")
    entry_NUM_BOIDS         .grid(row=1, column=1, padx=10, pady=5, sticky="w")
    entry_MAX_SPEED         .grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entry_NEIGHBOR_RADIUS   .grid(row=3, column=1, padx=10, pady=5, sticky="w")
    entry_ALIGNMENT_WEIGHT  .grid(row=4, column=1, padx=10, pady=5, sticky="w")
    entry_COHESION_WEIGHT   .grid(row=5, column=1, padx=10, pady=5, sticky="w")
    entry_SEPARATION_WEIGHT .grid(row=6, column=1, padx=10, pady=5, sticky="w")
    entry_AVOID_RADIUS      .grid(row=7, column=1, padx=10, pady=5, sticky="w")
    entry_MAX_AVOID_FORCE   .grid(row=8, column=1, padx=10, pady=5, sticky="w")
    

    # Bind selection event to listbox
    my_listbox.bind('<<ListboxSelect>>', on_select)

    popup.mainloop()

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

config = ConfigParser()
config.read('boid_profiles.ini')

boid_profile = tk.StringVar()
boid_profile.set(config.sections()[0]) # set default value
drop = tk.OptionMenu(root, boid_profile, '')

for profile in config.sections():
    drop['menu'].add_command(label=profile, command=tk._setit(boid_profile, profile))

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