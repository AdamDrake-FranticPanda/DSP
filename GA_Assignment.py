### will default to stablinski-tang and -5 to 5 gene limit

import copy
import random
import matplotlib.pyplot as plt

global func, d, usePlot
func = "S" # so the program knows which function to use from assignment | can be changed by being ran through import
d = 50 # The bounds a gene can go to e.g -10 to +10
usePlot = False # if imort wants to do a 2D plot


# ----------------------------------

import boid_simulation

number_of_boids = 20 # dictionary needs to be passed in


# ----------------------------------

def main(muteChance,    # the chance of a gene mutating
         ca,    # when a gene mutates, by how much
         pop,   # the population
         G,     # Amount of generations
         N,     # number of genomes | 'd' in assignment
         P,     # number of genes (population size)
         X = d      # gene range | 'x' in assignment | will take either the default value or the one passed in through import
         ):

    # Variable X is the bounds a gene can go to e.g -10 to + 10
    CA = round(ca,2) # rounds the mutation chance to the 2nd number

    population = copy.deepcopy(pop) #list of individuals
    offspring = []

    highestPerGeneration = []
    lowestPerGeneration = []
    averages = []

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

        return fitness

    #left func in assignment - styblinski-tang
    # calculates the fitness of an individual
    def fitnessFuncS(ind):
        result=0
        for i in range (0,N):
            result += (ind.gene[i]**4) - 16*(ind.gene[i]**2) + (5*ind.gene[i])
            #              x[i]^4         - 16x[i]^2         +      5x[i]
        return result/2
        # 1/2 of result

    #right func in assignment - dixon-price
    # calculates the fitness of an individual
    def fitnessFuncD(ind):
        result=0
        for i in range (1,N):
            result += i*(2*(ind.gene[i]**2)-ind.gene[i-1])**2

        return (ind.gene[0]-1)**2 + result

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
            # Depending on the fitness funtions we're using calculate a fitness value
            if func == "S":
                current.fitness = fitnessFuncS(current)
            elif func == "boidTest":
                current.fitness = boidFitnessFuncTest(current)
            else:
                current.fitness = fitnessFuncD(current)

            if current.fitness < lowestFit:
                lowestFit = current.fitness
            elif current.fitness > highestFit:
                highestFit = current.fitness

            totalfit += current.fitness

        return totalfit

    def findBestIndIndex(pop):
        best = pop[0].fitness
        index = 0
        for i in range(0,P):
            if pop[i].fitness > best:
                index = i
                best = pop[i].fitness
        return index

    def findWorstIndIndex(pop):
        worst = pop[0].fitness
        index = 0
        for i in range(0,P):
            if pop[i].fitness < worst:
                index = i
                worst = pop[i].fitness
        return index

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
            if func == "S":
                offspring1.fitness = fitnessFuncS(offspring1)
                offspring2.fitness = fitnessFuncS(offspring2)
            elif func == "boidTest":
                # run the simulations with the new genes to get a fitness value
                offspring1.fitness = boidFitnessFuncTest(offspring1)
                offspring2.fitness = boidFitnessFuncTest(offspring2)
                #print(f"Simulations Ran For Offspring...")
            else:
                offspring1.fitness = fitnessFuncD(offspring1)
                offspring2.fitness = fitnessFuncD(offspring2)


            # compare the two offsprings, and add the best to the offspring population
            if offspring1.fitness < offspring2.fitness:
                offspring.append(copy.deepcopy(offspring1))
            else:
                offspring.append(copy.deepcopy(offspring2))

        # mutation of the offspring population
        for i in range(0, P): # for all individuals
            for x in range(0, N): # for every genome in gene
                rand_check = random.randint(1,10000)/100
                #print(f"{rand_check} | {muteChance}")
                if rand_check <= muteChance:# chance to mutate
                    #print("Mutated")
                    changeAmount = CA# amount it will mutate by

                    if random.randint(0,1) == 1:# 50% chance for it to be negative mutation
                        changeAmount=changeAmount*-1

                    offspring[i].gene[x] =  offspring[i].gene[x]+changeAmount # apply mutation

                    # keep within gene (X) bounds
                    if offspring[i].gene[x] > X:
                        offspring[i].gene[x] = X
                    elif offspring[i].gene[x] < X*-1:
                        offspring[i].gene[x] = X*-1

        #copy best of pop to worst of offspring
        offspring[findBestIndIndex(offspring)] = copy.deepcopy(population[findWorstIndIndex(population)])
        
        #set offspring to population for next generation
        population = copy.deepcopy(offspring)

        #for 2D plot
        averages.append(fitnessOfPopulation(population)/P)
        highestPerGeneration.append(highestFit)
        lowestPerGeneration.append(lowestFit)
        #reset offspring for next generation
        offspring = []
        
        print(f"Finished Generation:{j}")
        print(f"Best Candidate:{population[findBestIndIndex(population)]}")

    avrgFitness = round(fitnessOfPopulation(population)/P,2)#calculate the average fitness of the current generation
    print(f"MC:{round(muteChance,2)} MS:{round(ca,2)} avrgFitness:{round(avrgFitness,2)}")

    # if being ran for 2d run, else being run for 3d sweep
    if usePlot == True:
        if func == "S":
            plt.title("Styblinski-tang")
        elif func == "boidTest":
            plt.title("Distance Fitness")
        else:
            plt.title("Dixon-price")

        plt.plot(highestPerGeneration, label ="Highest", color='red')
        plt.plot(averages, label="Average", color='orange')
        plt.plot(lowestPerGeneration, label ="Lowest", color='green')
        plt.legend(['Highest','Average','Lowest'])
        plt.show()
    else:
        #return and terminal output for 3D sweep
        return avrgFitness