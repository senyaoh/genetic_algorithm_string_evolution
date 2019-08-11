#!/usr/bin/env python3

'''
This is a demostration of genetic algorthm by evolving random strings into a target string.
'''

__author__ = 'Senyao Hou'
__copyright__ = 'Copyright 2019, Insomnia Project'
__credits__ = ['Senyao Hou']
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Senyao Hou'
__email__ = 'senyao.hou@gmail.com'
__status__ = 'Development'

import time
import operator
import string, random
from typing import List
from random import randrange
from numpy.random import choice

'''
In practice there should be a set of rules for evaluating the target
rather than defining the target explicitly
'''
TARGET_STR: str = "deoxyribonucleicacid"
STR_LEN: int = len(TARGET_STR)

'''Ideally population should be a function following a certain distribution'''
POPULATION: int = 1000

MUTATION_RATE: float = 0.01

class Specimen:
    phenotype: str = None
    parent_A = None
    parent_B = None
    fitness: int = None
    survival_p: float = None
    generation: int = 0
    mutation: bool = False

    def __init__(self, phenotype: str):
        '''
        Constructor that takes a string as parameter to create a specimen
        '''
        self.phenotype = phenotype
        self.evaluate_fitness()

    def evaluate_fitness(self):
        '''
        Calculate the fitness for the specimen, whenever there's a match at the same index with the target string,
        the fitness increase by 1, ranging from 0 to the length of the target string
        '''
        fitness: int = 0
        for i in range(STR_LEN):
            if self.phenotype[i] == TARGET_STR[i]:
                fitness += 1
        self.fitness = fitness

    def __str__(self):
        return f"Phenotype:{self.phenotype}, Fitness:{self.fitness}, Survival_p:{self.survival_p}, Generation:{self.generation}, Mutated:{self.mutation}"


def specimen_generator(size: int) -> List[Specimen]:
    '''
    Generate a list of specimen for the given population
    '''
    specimens = []
    fitness_sum = 0
    for i in range(size):
        random_str = ''.join(random.choice(string.ascii_lowercase) for x in range(STR_LEN))
        specimen = Specimen(random_str)
        specimens.append(specimen)
        fitness_sum += specimen.fitness

    '''Calculate the survival probability for each specimen'''
    for specimen in specimens:
        specimen.survival_p = specimen.fitness / fitness_sum
    return specimens


def selection(specimens: List[Specimen]) -> List[Specimen]:
    '''
    Randomly select 2 specimens based on the survival probability
    '''
    specimens_p = []
    for specimen in specimens:
        specimens_p.append(specimen.survival_p)
    chosen_specimens = choice(specimens, 2, p=specimens_p)
    return chosen_specimens


def crossover(parent_A: Specimen, parent_B: Specimen) -> Specimen:
    '''
    Take two specimens and randomly choose a character at the same index from them
    to create a new specimen
    '''
    child_str = ""
    for i in range(STR_LEN):
        child_str += choice([parent_A.phenotype[i], parent_B.phenotype[i]], p=[0.5, 0.5])
    child = Specimen(child_str)
    child.parent_A = parent_A
    child.parent_B = parent_B
    child.generation = parent_A.generation + 1
    return child


def mutation(specimen: Specimen) -> Specimen:
    '''
    randomly select a character in the string and change it to a random character that isn't itself
    '''
    str_list = list(specimen.phenotype)
    random_index = randrange(len(str_list))
    str_list[random_index] = random.choice(string.ascii_lowercase.replace(str_list[random_index],""))
    specimen.phenotype = "".join(str_list)
    specimen.mutation = True
    '''Update fitness after mutation'''
    specimen.evaluate_fitness()
    return specimen


def generate_generation(last_generation: List[Specimen]) -> List[Specimen]:
    new_generation = []
    fitness_sum = 0
    for i in range(POPULATION):
        '''
        Step 2: Selection
        Evaluate the fitness of each specimen of the population and 
        build a mating pool based on survival probability
        '''
        parents = selection(last_generation)
        
        '''
        Step 3: Crossover
        Create a child by combining the phenotype of the parents
        '''
        child = crossover(parents[0], parents[1])

        '''
        Step 4: Mutation
        Mutate the child for a given mutation rate
        '''
        if choice([True, False], p=[MUTATION_RATE, 1 - MUTATION_RATE]):
            child = mutation(child)
        
        fitness_sum += child.fitness
        new_generation.append(child)

    '''Calculate and set the survival probability for each specimen'''
    for specimen in new_generation:
        specimen.survival_p = specimen.fitness / fitness_sum

    return new_generation


def sort_by_fitness(specimens: List[Specimen]) -> List[Specimen]:
    '''
    Given a list of specimens, sort them by their fitness in descending order and return a new list
    '''
    sorted_specimens = sorted(specimens, reverse=True, key=operator.attrgetter('fitness'))
    return sorted_specimens


def trace_ancestry(specimen: Specimen) -> List[Specimen]:
    '''
    Given a specimen, trace all of its ancestry(currently only trace parent_A for each generation)
    and return them in a list in the order of generation
    '''
    family_lineage = []
    current_generation = specimen
    family_lineage.insert(0, current_generation)
    while current_generation.parent_A is not None:
        current_generation = current_generation.parent_A
        family_lineage.insert(0, current_generation)
    return family_lineage


def simulate():
    start_time = time.time()
    print("Simulation initiating")
    print(f"Target Specimen:{TARGET_STR}")
    print(f"Population Size:{POPULATION}")
    print(f"Mutation Rate:{MUTATION_RATE}")
    print("\n")

    '''
    Step 1: Initialization
    Create a population of specimens, each with randomly generated phenotype
    '''
    found_specimen: Specimen = None
    current_generation = specimen_generator(POPULATION)
    print("Generation 0")
    print("Best Fit Specimen:")
    print(sort_by_fitness(current_generation)[0])
    print("\n")

    '''Repeat Step 2, 3, 4 in generate_generation()'''
    while True:
        current_generation = generate_generation(current_generation)
        print(f"Generation {current_generation[0].generation}")
        print("Fittest specimen in current generation:")
        sorted_specimens = sort_by_fitness(current_generation)
        print(sorted_specimens[0])
        print("\n")
        if sorted_specimens[0].fitness == STR_LEN:
            found_specimen = sorted_specimens[0]
            print("We found the fittest specimen!")
            print(found_specimen)
            print("\n")
            break
    
    '''Trace ancestry of found specimen'''
    family_lineage = trace_ancestry(found_specimen)
    print("Family Lineage of the found specimen:")
    print('\n------>\n'.join(str(specimen) for specimen in family_lineage))

    end_time = time.time()
    duration = end_time - start_time
    print(f'The program took {str(duration)} seconds to complete.')
if __name__ == "__main__":
    simulate()