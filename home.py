import tkinter as tk
from configparser import ConfigParser
import os

boid_profile_path = ''
ga_profile_path = ''

boid_selected_profile = None
ga_selected_profile = None
new_profile_pending = False

def refresh_profile_list(my_listbox,path):
    print("Refreshing profile")

    my_listbox.delete(0, tk.END)

    config = ConfigParser()
    config.read(path)

    print(config.sections())

    for profile in config.sections():
        my_listbox.insert(tk.END, profile)
    pass

def create_default_config():
    config = ConfigParser()
 
    # Add sections and key-value pairs    
    config['paths'] = {
        'boid_profiles': 'boid_profiles.ini',  
        'ga_profiles': 'ga_profiles.ini',
        }
 
    # Write the configuration to a file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def boid_options():
    print("boid options...")

    # Read config data
    config = ConfigParser()
    config.read(boid_profile_path)

    def boid_profile_save(saveData):
        print("Saving profile...")

        global boid_selected_profile
        global new_profile_pending

        config = ConfigParser()
        config.read(boid_profile_path)

        # if there is a new profile pending then we will do this process then return
        if new_profile_pending == True:

            # Iterate over all keys and values in the dictionary
            for value in saveData[1:]: # check that all of the elements apart from the ID isnt empty
                if value == '' or value == None:
                    print("Error: Empty value in NEW profile")
                    return

            # Automatically assign an ID to the new profile by finding the highest current
            # existing id and iterating one to it
            highest_id = 0
            for section in config.sections():
                if 'profile_id' in config[section]:
                    if int(config[section]['profile_id']) > highest_id:
                        highest_id = int(config[section]['profile_id'])
            profile_id = highest_id+1

            entry_PROFILE_ID.config(state='normal')
            entry_PROFILE_ID.insert(0, profile_id)  # Insert the generated ID
            entry_PROFILE_ID.config(state='disabled')

            # Create a new section with the profile data
            section_name = f"boid profile {profile_id}"
            config[section_name] = {
                'profile_id': profile_id,
                'num_boids': saveData[1],
                'max_speed': saveData[2],
                'neighbor_radius': saveData[3],
                'alignment_weight': saveData[4],
                'cohesion_weight': saveData[5],
                'separation_weight': saveData[6],
                'avoid_radius': saveData[7],
                'max_avoid_force': saveData[8]
            }

            # Write the changes back to the config file
            with open(boid_profile_path, 'w') as configfile:
                config.write(configfile)

            new_button.config(state='normal')
            entry_PROFILE_ID.config(state='normal')
            new_profile_pending = False  
            refresh_profile_list(my_listbox,boid_profile_path)
            return      

        print(boid_selected_profile)

        selected_item = boid_selected_profile

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

    def profile_delete_current_selected():
        global boid_selected_profile

        if boid_selected_profile == None:
            print("No selected profile to delete")
            return

        del config[boid_selected_profile]

        with open(boid_profile_path, 'w') as configfile:
            config.write(configfile)

        boid_selected_profile = None
        refresh_profile_list(my_listbox,boid_profile_path)

    def boid_profile_create():
        global new_profile_pending

        new_profile_pending = True

        my_listbox.insert(tk.END, "New profile")
        new_button.config(state='disabled')
        entry_PROFILE_ID.delete(0, tk.END)  # Delete current text in entry
        entry_PROFILE_ID.config(state='disabled')

        # Clear all fields
        entry_PROFILE_ID        .delete(0, tk.END)
        entry_NUM_BOIDS         .delete(0, tk.END)  # Clear previous value        
        entry_MAX_SPEED         .delete(0, tk.END)
        entry_NEIGHBOR_RADIUS   .delete(0, tk.END)
        entry_ALIGNMENT_WEIGHT  .delete(0, tk.END)
        entry_COHESION_WEIGHT   .delete(0, tk.END)
        entry_SEPARATION_WEIGHT .delete(0, tk.END)
        entry_AVOID_RADIUS      .delete(0, tk.END)
        entry_MAX_AVOID_FORCE   .delete(0, tk.END)
        
    def on_profile_listbox_select(event):
        global boid_selected_profile
        global new_profile_pending

        # Read config data again just in case of an update
        config = ConfigParser()
        config.read(boid_profile_path)

        # Get the currently selected item from the listbox
        selected_index = my_listbox.curselection()

        if len(selected_index) <= 0:# if the listbox is deselected the index tuple will be empty
            print("Listbox de-selected...")
            return

        # check if the new selection is not the "new profile"
        selected_item = my_listbox.get(selected_index[0])
        if selected_item != 'New profile' and new_profile_pending == True:
            print("New profile creation aborted")
            new_button.config(state='normal')
            entry_PROFILE_ID.config(state='normal')
            new_profile_pending = False
            my_listbox.delete(my_listbox.size()-1)
            #return
        elif selected_item == 'New profile':
            return
        
        # find wich one was selected, clear current data and replace with right data
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
        global new_profile_pending

        boid_selected_profile = None
        new_profile_pending = False # might be redundant

        popup.destroy()  # Close the window
    
    popup = tk.Toplevel()
    popup.title("Boid Options")
    popup.geometry("600x300")
    # Bind the function to the window's close event
    popup.protocol("WM_DELETE_WINDOW", on_closing)

    # Disable original window while popup is open
    #popup.grab_set()

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


    # Add buttons to the popup window
    new_button = tk.Button(frame1, text="New", command=boid_profile_create)

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



    delete_button = tk.Button(frame1, text="Delete", command=profile_delete_current_selected)
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
    my_listbox.bind('<<ListboxSelect>>', on_profile_listbox_select)

    popup.mainloop()

def ga_options():
    print("ga options...")

    # Read config data
    config = ConfigParser()
    config.read(ga_profile_path)

    def ga_profile_save(saveData):
        print("Saving profile...")

        global ga_selected_profile
        global new_profile_pending

        # if there is a new profile pending then we will do this process then return
        if new_profile_pending == True:

            # Iterate over all keys and values in the dictionary
            for value in saveData[1:]: # check that all of the elements apart from the ID isnt empty
                if value == '' or value == None:
                    print("Error: Empty value in NEW profile")
                    return

            # Automatically assign an ID to the new profile by finding the highest current
            # existing id and iterating one to it
            highest_id = 0
            for section in config.sections():
                if 'profile_id' in config[section]:
                    if int(config[section]['profile_id']) > highest_id:
                        highest_id = int(config[section]['profile_id'])
            profile_id = highest_id+1

            entry_PROFILE_ID.config(state='normal')
            entry_PROFILE_ID.insert(0, profile_id)  # Insert the generated ID
            entry_PROFILE_ID.config(state='disabled')

            # Create a new section with the profile data
            section_name = f"ga profile {profile_id}"
            config[section_name] = {
                'profile_id': profile_id,
                'population_size': saveData[1],
                'selection_method': saveData[2],
                'crossover_rate': saveData[3],
                'mutation_rate': saveData[4],
                'termination_condition': saveData[5],
                'fitness_function': saveData[6]
            }

            # Write the changes back to the config file
            with open(ga_profile_path, 'w') as configfile:
                config.write(configfile)

            new_button.config(state='normal')
            entry_PROFILE_ID.config(state='normal')
            new_profile_pending = False  
            refresh_profile_list(my_listbox,ga_profile_path)
            return
        
        print(ga_selected_profile)

        selected_item = ga_selected_profile

        if selected_item == '' or selected_item == None:
            print("Error: No selected profile")
            return
        
        # Iterate over all keys and values in the dictionary
        for value in saveData:
            if value == '' or value == None:
                print("Error: Empty value in profile")
                return
            
        config[selected_item]["profile_id"] = saveData[0]
        config[selected_item]["population_size"] = saveData[1]
        config[selected_item]["selection_method"] = saveData[2]
        config[selected_item]["crossover_rate"] = saveData[3]
        config[selected_item]["mutation_rate"] = saveData[4]
        config[selected_item]["termination_conditio"] = saveData[5]
        config[selected_item]["fitness_function"] = saveData[6]

        # Write the changes back to the config file
        with open(ga_profile_path, 'w') as config_file:
            config.write(config_file)
        print("GA profile saved")

    def profile_delete_current_selected():
        global ga_selected_profile

        if ga_selected_profile == None:
            print("No selected profile to delete")
            return

        del config[ga_selected_profile]

        with open(ga_profile_path, 'w') as configfile:
            config.write(configfile)

        ga_selected_profile = None
        refresh_profile_list(my_listbox,ga_profile_path)

    def ga_profile_create():
        global new_profile_pending

        new_profile_pending = True

        my_listbox.insert(tk.END, "New profile")
        new_button.config(state='disabled')
        entry_PROFILE_ID.delete(0,tk.END) # Delete current text in entry
        entry_PROFILE_ID.config(state='disabled')


        # Clear all fields
        entry_POPULATION_SIZE      .delete(0, tk.END)
        entry_SELECTION_METHOD     .delete(0, tk.END)
        entry_CROSSOVER_RATE       .delete(0, tk.END)
        entry_MUTATION_RATE        .delete(0, tk.END)
        entry_TERMINATION_CONDITION.delete(0, tk.END)
        entry_FITNESS_FUNCTION     .delete(0, tk.END)

    def on_profile_listbox_select(event):
        global ga_selected_profile
        global new_profile_pending

        # Read config data again just in case of an update
        config = ConfigParser()
        config.read(ga_profile_path)

        # Get the currently selected item from the listbox
        selected_index = my_listbox.curselection()

        if len(selected_index) <= 0:# if the listbox is deselected the index tuple will be empty
            print("Listbox de-selected...")
            return

        # check if the new selection is not the "new profile"
        selected_item = my_listbox.get(selected_index[0])
        if selected_item != 'New profile' and new_profile_pending == True:
            print("New profile creation aborted")
            new_button.config(state='normal')
            entry_PROFILE_ID.config(state='normal')
            new_profile_pending = False
            my_listbox.delete(my_listbox.size()-1)
            #return
        elif selected_item == 'New profile':
            return
        
        # find wich one was selected, clear current data and replace with right data
        if selected_index:
            selected_item = my_listbox.get(selected_index[0])
            # Retrieve configuration data for the selected item
            try:
                target_profile = selected_item
                ga_config = config[selected_item]
                ga_selected_profile = selected_item
                print(f"selected item:{ga_selected_profile}")
                entry_PROFILE_ID           .delete(0, tk.END)
                entry_POPULATION_SIZE      .delete(0, tk.END)  # Clear previous value        
                entry_SELECTION_METHOD     .delete(0, tk.END)
                entry_CROSSOVER_RATE       .delete(0, tk.END)
                entry_MUTATION_RATE        .delete(0, tk.END)
                entry_TERMINATION_CONDITION.delete(0, tk.END)
                entry_FITNESS_FUNCTION     .delete(0, tk.END)

                entry_PROFILE_ID.insert(tk.END, ga_config.get('PROFILE_ID', ''))
                entry_POPULATION_SIZE.insert(tk.END, ga_config.get('population_size', ''))  # Insert value
                entry_SELECTION_METHOD.insert(tk.END, ga_config.get('selection_method', ''))
                entry_CROSSOVER_RATE.insert(tk.END, ga_config.get('crossover_rate', ''))
                entry_MUTATION_RATE.insert(tk.END, ga_config.get('mutation_rate', ''))
                entry_TERMINATION_CONDITION.insert(tk.END, ga_config.get('termination_condition', ''))
                entry_FITNESS_FUNCTION.insert(tk.END, ga_config.get('fitness_function', ''))
                return target_profile
            except KeyError:
                tk.messagebox.showerror("Error", f"No configuration found for '{selected_item}'")

    def on_closing():
        print("Closing GA options...")

        global ga_selected_profile
        global new_profile_pending

        ga_selected_profile = None
        new_profile_pending = False # might be redundant

        popup.destroy()  # Close the window
    
    popup = tk.Toplevel()
    popup.title("Genetic Algorithm Options")
    popup.geometry("650x300")
    # Bind the function to the window's close event
    popup.protocol("WM_DELETE_WINDOW", on_closing)

    # Disable original window while popup is open
    #popup.grab_set()

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

    # Entry for GA options
    label_PROFILE_ID            = tk.Label(frame3, text="Profile ID:")
    label_POPULATION_SIZE       = tk.Label(frame3, text="Population Size:")
    label_SELECTION_METHOD      = tk.Label(frame3, text="Selection Method:")
    label_CROSSOVER_RATE        = tk.Label(frame3, text="Crossover Rate:")
    label_MUTATION_RATE         = tk.Label(frame3, text="Mutation Rate:")
    label_TERMINATION_CONDITION = tk.Label(frame3, text="Termination Condition:")
    label_FITNESS_FUNCTION      = tk.Label(frame3, text="Fitness Function:")

    entry_PROFILE_ID            = tk.Entry(frame3, width=30)
    entry_POPULATION_SIZE       = tk.Entry(frame3, width=30)
    entry_SELECTION_METHOD      = tk.Entry(frame3, width=30)
    entry_CROSSOVER_RATE        = tk.Entry(frame3, width=30)
    entry_MUTATION_RATE         = tk.Entry(frame3, width=30)
    entry_TERMINATION_CONDITION = tk.Entry(frame3, width=30)
    entry_FITNESS_FUNCTION      = tk.Entry(frame3, width=30)

    # Add buttons to the popup window
    new_button = tk.Button(frame1, text="New", command=ga_profile_create)
    save_button = tk.Button(
        frame1, text="Save", 
        command=lambda: ga_profile_save(
            [
                entry_PROFILE_ID           .get(),
                entry_POPULATION_SIZE      .get(),
                entry_SELECTION_METHOD     .get(),
                entry_CROSSOVER_RATE       .get(),
                entry_MUTATION_RATE        .get(),
                entry_TERMINATION_CONDITION.get(),
                entry_FITNESS_FUNCTION     .get()
            ]
        )
        )
    delete_button = tk.Button(frame1, text="Delete", command=profile_delete_current_selected)
    close_button = tk.Button(frame1, text="Close", command=on_closing)

    new_button.grid(row=0, column=0, padx=10, pady=5)
    save_button.grid(row=1, column=0, padx=10, pady=5)
    delete_button.grid(row=2, column=0, padx=10, pady=5)
    close_button.grid(row=3, column=0, padx=10, pady=5)

    label_PROFILE_ID           .grid(row=0, column=0, padx=10, pady=5, sticky="e")
    label_POPULATION_SIZE      .grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_SELECTION_METHOD     .grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_CROSSOVER_RATE       .grid(row=3, column=0, padx=10, pady=5, sticky="e")
    label_MUTATION_RATE        .grid(row=4, column=0, padx=10, pady=5, sticky="e")
    label_TERMINATION_CONDITION.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    label_FITNESS_FUNCTION     .grid(row=6, column=0, padx=10, pady=5, sticky="e")

    entry_PROFILE_ID           .grid(row=0, column=1, padx=10, pady=5, sticky="w")
    entry_POPULATION_SIZE      .grid(row=1, column=1, padx=10, pady=5, sticky="w")
    entry_SELECTION_METHOD     .grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entry_CROSSOVER_RATE       .grid(row=3, column=1, padx=10, pady=5, sticky="w")
    entry_MUTATION_RATE        .grid(row=4, column=1, padx=10, pady=5, sticky="w")
    entry_TERMINATION_CONDITION.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    entry_FITNESS_FUNCTION     .grid(row=6, column=1, padx=10, pady=5, sticky="w")


    # Bind selection event to listbox
    my_listbox.bind('<<ListboxSelect>>', on_profile_listbox_select)

    popup.mainloop()

def data_options():
    print("data options...")

def toggle_checkbox(checkbox_state):
    # Toggle the state of the checkbox
    checkbox_state.set(not checkbox_state.get())

def run_simulation_click():
    print("Button clicked")

def main():

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
    checkbox1 = tk.Checkbutton(root, variable=tk.BooleanVar(), command=lambda: toggle_checkbox(checkbox_state))
    checkbox1.grid(row=0, column=1, padx=10, pady=5, sticky="e")

    # Create a label and place it in the grid
    label2 = tk.Label(root, text="Boid Profile")
    label2.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    boid_config = ConfigParser()
    boid_config.read(boid_profile_path)

    boid_profile = tk.StringVar()
    boid_profile.set(boid_config.sections()[0]) # set default value

    boid_sections = boid_config.sections()

    # Add the first section to the drop on initialisation
    boid_drop = tk.OptionMenu(root, boid_profile, boid_sections[0])

    # Add remaining profiles to the OptionMenu
    for profile in boid_sections[1:]:
        boid_drop['menu'].add_command(label=profile, command=tk._setit(boid_profile, profile))

    boid_drop.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Create a label and place it in the grid
    label3 = tk.Label(root, text="Genetic Algorithm Profile")
    label3.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    ga_config = ConfigParser()
    ga_config.read(ga_profile_path)

    ga_profile = tk.StringVar()
    ga_profile.set(ga_config.sections()[0]) # set default value
    # Initialize OptionMenu with the first profile from config_sections

    ga_sections = ga_config.sections()

    # Add the first section to the drop on initialisation
    ga_drop = tk.OptionMenu(root, ga_profile, ga_sections[0])

    # Add remaining profiles to the OptionMenu
    for profile in ga_sections[1:]:
        ga_drop['menu'].add_command(label=profile, command=tk._setit(ga_profile, profile))

    ga_drop.grid(row=2, column=1, padx=10, pady=5, sticky="w")


    # Create a button and place it in the window
    button = tk.Button(root, text="Run Simulation", command=run_simulation_click)
    button.grid(row=3, column=0, padx=5, pady=5, sticky="e")

    root.mainloop()

# looks for config file, if not found creates a default config file
if os.path.exists('config.ini'):
    print("Loading config.ini...")
else:
    print("Config file not found...")
    print("Creating config.ini...")
    create_default_config()
    print("Config created...")

config = ConfigParser()
config.read('config.ini')
boid_profile_path = config['paths']['boid_profiles']
ga_profile_path = config['paths']['genetic_profiles']

main()