import GA_Assignment as GA

import copy
import random

from configparser import ConfigParser

gene_types = 7 # this is the number of genes an individual needs
hardCoded_gene_bounds = { # The bounds a gene can go to e.g -10 to +10
    "max_speed": 5,
    "neighbor_radius": 75,
    "alignment_weight": 1,
    "cohesion_weight": 1,
    "separation_weight": 1,
    "avoid_radius": 57,
    "max_avoid_force": 5
 } # want to change gene bounds to dictionary


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

        self.fitness = None

    def __str__(self) -> str:
        return "str: "+str(self.gene)

def generatePop(population_size):
    population = []

    # Load the configuration file
    # config = ConfigParser()
    # config.read(boid_profile_path)

    # makes new individual for all population size
    for i in range (0, population_size):
        new_gene = [
            round(random.uniform(1                                              ,    hardCoded_gene_bounds["max_speed"]), 2),
            round(random.uniform(hardCoded_gene_bounds["neighbor_radius"]    *-1,    hardCoded_gene_bounds["neighbor_radius"])),
            round(random.uniform(hardCoded_gene_bounds["alignment_weight"]   *-1,    hardCoded_gene_bounds["alignment_weight"]), 2),
            round(random.uniform(hardCoded_gene_bounds["cohesion_weight"]    *-1,    hardCoded_gene_bounds["cohesion_weight"]), 2),
            round(random.uniform(hardCoded_gene_bounds["separation_weight"]  *-1,    hardCoded_gene_bounds["separation_weight"]), 2),
            round(random.uniform(hardCoded_gene_bounds["avoid_radius"]       *-1,    hardCoded_gene_bounds["avoid_radius"])),
            round(random.uniform(hardCoded_gene_bounds["max_avoid_force"]    *-1,    hardCoded_gene_bounds["max_avoid_force"]), 2)
        ]

        ind = individual()
        ind.gene = copy.deepcopy(new_gene) # set the loaded 'gene' values from file into the ind object
        population.append(ind) # add the individual to the population list

    return population


def main(boid_profile, ga_profile):
    config = ConfigParser()
    config.read('config.ini')

    boid_profile_path = config['paths']['boid_profiles']
    ga_profile_path = config['paths']['genetic_profiles']

    #ga_profile = "ga profile 1"  # need to have this passed in
    #boid_profile = "boid profile 1" # need to have this passed in

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
    GA.hardCoded_gene_bounds = hardCoded_gene_bounds
    GA.life_span = int(ga_profile_data.get('termination_condition', 'Not found'))


    mutation_step = {
        "max_speed": 0.2,
        "neighbor_radius": 1,
        "alignment_weight": 0.1,
        "cohesion_weight": 0.1,
        "separation_weight": 0.1,
        "avoid_radius": 2,
        "max_avoid_force": 0.2
    } # when these genes mutate, how much by

    no_generations = 100

    print(f'Mutation rate: {ga_mutation_rate}')
    print(f'Mutation Step:\n {mutation_step}')
    print(f'NO. Generations: {no_generations}')
    print(f'Population Size: {ga_population_size}')

    print(f"Generation gene example: {population[0]}")

    GA.main(
        muteChance = ga_mutation_rate,
        muteStep = mutation_step,   # mutation step: when mutation occours, by how much does it mutate
        pop = population,           # the list of boid settings that makes up the population to be trained
        G = no_generations,         # Number of generations
        N = gene_types,             # Number of geneomes in the gene
        P = ga_population_size      # size of the population
    )