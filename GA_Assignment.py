### will default to stablinski-tang and -5 to 5 gene limit

import copy
import random
import matplotlib.pyplot as plt

global func, usePlot
func = "S" # so the program knows which function to use from assignment | can be changed by being ran through import
#d = 50 # The bounds a gene can go to e.g -10 to +10
hardCoded_gene_bounds = { # The bounds a gene can go to e.g -10 to +10
    "max_speed": 5,
    "neighbor_radius": 75,
    "alignment_weight": 1,
    "cohesion_weight": 1,
    "separation_weight": 1,
    "avoid_radius": 57,
    "max_avoid_force": 5
 } # want to change gene bounds to dictionary


usePlot = False # if imort wants to do a 2D plot


# ----------------------------------

import boid_simulation

number_of_boids = 20 # dictionary needs to be passed in


# ----------------------------------

def main(muteChance,    # the chance of a gene mutating
         muteStep,    # when a gene mutates, by how much
         pop,   # the population
         G,     # Amount of generations
         N,     # number of genomes | 'd' in assignment
         P,     # number of genes (population size)
         gene_bounds = hardCoded_gene_bounds  # gene range | 'x' in assignment | will take either the default value or the one passed in through import
         ):

    # Variable X is the bounds a gene can go to e.g -10 to + 10
    #muteStep = round(muteStep,2) # rounds the mutation change to the 2nd number

    population = copy.deepcopy(pop) #list of individuals
    offspring = []

    highestPerGeneration = []
    lowestPerGeneration = []
    averages = []

    def printAllFitnesses(pop):
        for ind in pop:
            print(ind.fitness)

    def boidFitnessFuncTest(ind):
        fitness = boid_simulation.run(
            num_boids           = int(  number_of_boids),
            max_speed           = int(  ind.gene[0]), 
            neighbor_radius     = int(  ind.gene[1]),
            alignment_weight    = float(ind.gene[2]),
            cohesion_weight     = float(ind.gene[3]),
            separation_weight   = float(ind.gene[4]),
            avoid_radius        = int(  ind.gene[5]),
            max_avoid_force     = float(ind.gene[6]),
            show_graphics       = False
        )
        #print(f"fitness = {fitness}")
        return fitness

    # returns the total fitness of a population
    def fitnessOfPopulation(pop):
        totalfit = 0

        global highestFit
        global lowestFit

        highestFit = copy.deepcopy(pop[0].fitness)
        lowestFit = copy.deepcopy(pop[0].fitness)
        #test population fitness
        for i in range(0, P):
            current = pop[i]

            # we shouldnt need this line, unnecisary re running of simulation?
            #current.fitness = boidFitnessFuncTest(current)

            if current.fitness < lowestFit:
                lowestFit = current.fitness
            elif current.fitness > highestFit:
                highestFit = current.fitness

            totalfit += current.fitness

        return totalfit
    
    def findBestIndex(pop):
        best_index = 0
        best_fitness = pop[0].fitness
        for i in range(1, len(pop)):
            if pop[i].fitness < best_fitness:
                best_fitness = pop[i].fitness
                best_index = i
        return best_index

    def findWorstIndex(pop):
        worst_index = 0
        worst_fitness = pop[0].fitness
        for i in range(1, len(pop)):
            if pop[i].fitness > worst_fitness:
                worst_fitness = pop[i].fitness
                worst_index = i
        return worst_index

    # set initial fitness for all individuals in population
    for individual in population:
        individual.fitness = boidFitnessFuncTest(individual)
        #print(individual.fitness)

    #print("Set fitness values for initial population")

    #loop for amount of generations
    print(f"Generations {G}")
    for j in range(0, G):
        #crossover
        # for the size of the population generate an offspring using two random individuals from main population
        # using some genes from ind1 and some from ind2 (crossover)
        for person in population:
            #select two random parents (selection)
            offspring1 = copy.deepcopy(population[random.randint(0, P-1)])# set offspring 1 # get random individual
            offspring2 = copy.deepcopy(population[random.randint(0, P-1)])# set offspring 2 # get random individual

            crosspoint = random.randint(0,N-1) # choose random crosspoint
            
            # up until the cross point, swap the two offsprings genes
            tempGene = copy.deepcopy(offspring1.gene)
            for geneIndex in range(0,crosspoint):
                offspring1.gene[geneIndex] = copy.deepcopy(offspring2.gene[geneIndex])
                offspring2.gene[geneIndex] = copy.deepcopy(tempGene[geneIndex])

            # calculating an offsprings fitness
            # run the simulations with the new genes to get a new fitness value
            offspring1.fitness = boidFitnessFuncTest(offspring1)
            offspring2.fitness = boidFitnessFuncTest(offspring2)
            #print(f"Simulations Ran For Offspring...")


            # compare the two offsprings, and add the best to the offspring population
            if offspring1.fitness < offspring2.fitness:
                offspring.append(copy.deepcopy(offspring1))
            else:
                offspring.append(copy.deepcopy(offspring2))

        # new mutation loop for offspring population
        for individual in offspring:
            mutated = False
            #print(f"Original Gene: {individual.gene}")
            for geneome, (key, gene_bound) in zip(individual.gene, gene_bounds.items()):
                # check if we are going to mutate this geneome
                rand_check = random.randint(1,10000)/100

                # if we are mutating do this
                if rand_check <= muteChance:
                    mutated = True

                    #print("Mutation triggered")

                    # get the genome
                    # get the mute_step for the correct genome
                    geneome_mute_step = muteStep[key]

                    # 50% chance for it to be negative mutation
                    if random.randint(0,1) == 1:
                        geneome_mute_step=geneome_mute_step*-1
                    

                    # apply geneome mutation
                    geneome+=geneome_mute_step

                    # keep genome in gene_bounds
                    if geneome > gene_bound:
                        geneome = gene_bound
                    elif geneome < gene_bound*-1:
                        geneome = gene_bound*-1

                    #print(f"Gene: {geneome}, Key: {key}, geneBound: {gene_bound}, geneStep: {geneome_mute_step}")

            # now that the gene is mutated we need to update its fitness score
            if mutated:
                individual.fitness = boidFitnessFuncTest(individual)
                    
            #print(f"After Potential Mute Gene: {individual.gene}")

        #copy best of population to worst of offspring

        #put the worst of population into the best of offspring

        offspring_worst_index = findWorstIndex(offspring)

        population_best_index = findBestIndex(population)

        offspring[offspring_worst_index] = copy.deepcopy(population[population_best_index])

        #offspring[findBestIndIndex(offspring)] = copy.deepcopy(population[findWorstIndIndex(population)])
        # ^ offspring best                      =               population worst

        #set offspring to population for next generation
        population = copy.deepcopy(offspring)

        population_best_index = findBestIndex(population)
        population_worst_index = findWorstIndex(population)

        #reset offspring for next generation
        offspring = []
        
        #print(f"Finished Generation:{j}")
        print(f"G{j} Best Candidate: {population[population_best_index]}")
        print(f"    Fitness: {population[population_best_index].fitness}")
        print(f"G{j} Worst Candidate: {population[population_worst_index]}")
        print(f"    Fitness: {population[population_worst_index].fitness}")

        #calculate the average fitness of the current generation
        avrgFitness = round(fitnessOfPopulation(population)/P,2)
        print(f"G{j} AvrgFitness: {avrgFitness}")

        #for 2D plot
        averages.append(avrgFitness)
        highestPerGeneration.append(highestFit)
        lowestPerGeneration.append(lowestFit)


    # if being ran for 2d run, else being run for 3d sweep
    if usePlot == True:
        plt.title("Dixon-price")

        plt.plot(highestPerGeneration, label ="Highest", color='red')
        plt.plot(averages, label="Average", color='orange')
        plt.plot(lowestPerGeneration, label ="Lowest", color='green')
        plt.legend(['Highest','Average','Lowest'])
        plt.show()
    else:
        #return and terminal output for 3D sweep
        return avrgFitness