import GA_Assignment as GA
import matplotlib.pyplot as plt
import numpy as np

import copy
import random

from configparser import ConfigParser

bestFit = 9999999999999999999999 
bestMute = 0
bestStep = 0

gene_types = 7 # this is the number of genes an individual needs
class individual:
    def __init__(self):
        self.gene = []

        # each gene corresponds to:     
        # max_speed        
        # neighbor_radius  
        # alignment_weight 
        # cohesion_weight  
        # separation_weight
        # avoid_radius     
        # max_avoid_force   

        self.fitness = 0

    def __str__(self) -> str:
        return "str: "+str(self.gene)

def generatePop(population_size):
    population = []

    # Load the configuration file
    config = ConfigParser()
    config.read(boid_profile_path)

    # makes new individual for all population size
    for i in range (0, population_size):
        # Get the values from the right section
        # new_gene = [
        #     float(  config.get(boid_profile, 'max_speed')),
        #     int(    config.get(boid_profile, 'neighbor_radius')),
        #     float(  config.get(boid_profile, 'alignment_weight')),
        #     float(  config.get(boid_profile, 'cohesion_weight')),
        #     float(  config.get(boid_profile, 'separation_weight')),
        #     int(    config.get(boid_profile, 'avoid_radius')),
        #     float(  config.get(boid_profile, 'max_avoid_force'))
        # ]

        new_gene = [
            float(  random.uniform(1, 5)),
            int(    random.uniform(10, 50)),
            float(  random.uniform(1, 100)/100),
            float(  random.uniform(1, 100)/100),
            float(  random.uniform(1, 100)/100),
            int(    random.uniform(10, 50)),
            float(  random.uniform(1, 15))
        ]

        ind = individual()
        ind.gene = copy.deepcopy(new_gene) # set the loaded 'gene' values from file into the ind object
        population.append(ind) # add the individual to the population list

    return population

def runTest(muteChance, muteStep):
    global bestFit
    global bestMute
    global bestStep
    mypop = copy.deepcopy(population)
    
    #single run of particular sweep | faster
    fitness = GA.main(muteChance,muteStep,mypop)

    if fitness >= 700:
        fitness = 700
    if fitness < bestFit:
        bestFit = fitness
        bestMute = muteChance
        bestStep = muteStep
    return fitness

def run3DSweep(samples, algo,mcStart, mcEnd, msStart, msEnd):
    print("Starting 3D Sweep")
    #makes 3d graph & axis for plt
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # makes array of evenly spaced values between a,b with samples c
    muteChance = np.linspace(mcStart,mcEnd,samples)
    muteStep = np.linspace(msStart,msEnd,samples)

    # make plt grid with the evenly spaced values
    X,Y = np.meshgrid(muteChance,muteStep)

    # runs runTest witht the even values generated for mc & ms and returns np array
    run = np.vectorize(runTest)
    Z = run(X,Y)

    # plots calculated points
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1,cmap='coolwarm', edgecolor='none')

    # add labels
    if algo == "1":
        ax.set_title("3D Sweep: styblinski-tang")
    else:
        ax.set_title("3D Sweep: dixon-price")

    ax.set_xlabel("Mutation Chance %")
    ax.set_ylabel("Mutation Change")
    ax.set_zlabel("Fitness")

    #runTest()
    print('Sweep Done')
    print(f'Best fitness: {bestFit}\nBest Mute Chance: {bestMute}\nBest Mute Step: {bestStep}')
    plt.show()


#choice = input("Select:\n1. 3D Sweep\n2. 2D Plot\n>>>: ")
#algo = input("1. Styblinski-tang\n2. Dixon-price\n>>>: ")

# so the GA uses the right function and gene range when ran
# if algo == "1":
#     GA.func = "S"
#     GA.d = 5
# else:
#     GA.func = "D"
#     GA.d = 10

# Generates population to use for every run of the sweep

# if choice == "1":
#     choice2 = float(input("Mutation Chance Start: "))
#     choice3 = float(input("Mutation Chance End: "))
#     choice4 = float(input("Mutation Step Start: "))
#     choice5 = float(input("Mutation Step End: "))
#     choice = input("How many samples: ")
#     run3DSweep(int(choice), algo, choice2, choice3, choice4, choice5)

# elif choice == "2":

config = ConfigParser()
config.read('config.ini')

boid_profile_path = config['paths']['boid_profiles']
ga_profile_path = config['paths']['genetic_profiles']

ga_profile = "ga profile 1"  # need to have this passed in
boid_profile = "boid profile 1" # need to have this passed in

# Read GA config data
ga_config = ConfigParser()
ga_config.read(ga_profile_path)

# Read Boid config data
boid_config = ConfigParser()
boid_config.read(boid_profile_path)


ga_profile_data = ga_config[ga_profile] # get dictionary of right section
boid_profile_data = boid_config[boid_profile]

ga_population_size = int(ga_profile_data.get('population_size', 'Not found'))
ga_fitness_function = "boidTest"

# config is 0.07 where GA needs 7 as 7%
ga_mutation_rate = float(ga_profile_data.get('mutation_rate', 'Not found'))*100 

population = generatePop(ga_population_size)

GA.usePlot = True
GA.func = ga_fitness_function
GA.number_of_boids = int(boid_profile_data.get('num_boids', 'Not found'))

mutation_step = 1
no_generations = 100

print(f'Mutation rate: {ga_mutation_rate}')
print(f'Mutation Step: {mutation_step}')
print(f'NO. Generations: {no_generations}')
print(f'Population Size: {ga_population_size}')

GA.main(
    muteChance = ga_mutation_rate,
    ca = mutation_step,     # mutation step: when mutation occours, by how much does it mutate
    pop = population,       # the list of boid settings that makes up the population to be trained
    G = no_generations,     # Number of generations
    N = gene_types,         # Number of geneomes in the gene
    P = ga_population_size  # size of the population
)