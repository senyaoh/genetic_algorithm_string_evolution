# String Evolution -- A simple demostration of Genetic Algorithm 
## Inspired by Ayla's presentation on neuroevolution and a gift for her birthday🎂

## Requirement
* Please use python version >= 3.6 because typing and f-strings are used, you can check by running `python3 --version`
* Please make sure you have `numpy` installed, you can do it by running `pip3 install numpy`

## Run the program
1. If you have Git installed, go on and clone the repository:
```bash
git clone https://github.com/senyaoh/genetic_algorithm_string_evolution.git
```
2. To execute the program, simply run inside the repository folder:
```bash
python3 ga_string_evolution.py
```

## Description
This is a demostration of genetic algorthm by evolving random strings into a target string.

### Step 1: Initialization
We first create a given population of random strings of the length of the target string.

### Evaluate Fitness
We evaluate the fitness of a given string by comparing the character at the same index with the target string, if it matches, the fitness increased by 1, highest fitness is the length of the string, which means every character matches.

### Survival Probability
We then calculate the survival probability of each string by dividing the fitness of the string by the sum of fitness of all strings in current generation. 

### Step 2: Selection
We randomly pick 2 strings based on their survival probability, the higher the probability the more likely they get picked for crossover.

### Step 3: Crossover
We take the selected strings and combine them into a new string by randomly pick a character from one the string at each index. 

### Create new generation
Step 2 & 3 will be repeated for as many times as the size of the defined population to create a new generation.

### Step 4: Mutation
We randomly pick strings in the new generation based on the given mutation rate and give them a mutation. We mutate a string by randomly select one character in the string and change it into another random character.

### Evolution
We repeat the above steps until a string that matches the target string is created.

