import json
import matplotlib.pyplot as plt
import seaborn as sns
from functions import *

class Individual:
    def __init__(self, genome_size):
        self.code = [random.uniform(0, 1) for _ in range(genome_size)]
        self.fitness = None

    def calcFit(self, simulate_game):
        self.fitness = simulate_game(self.code)
        return self.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

def tournament_selection(population):
    TOURNAMENT_SIZE = 5
    best = None
    for _ in range(TOURNAMENT_SIZE):
        candidate = random.choice(population)
        if best is None or candidate.fitness > best.fitness:
            best = candidate
    return best

def roulette_selection(population):
    total_fitness = sum(ind.fitness for ind in population)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual in population:
        current += individual.fitness
        if current >= pick:
            return individual

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1.code) - 1)
    child1 = Individual(len(parent1.code))
    child2 = Individual(len(parent1.code))
    child1.code = parent1.code[:point] + parent2.code[point:]
    child2.code = parent2.code[:point] + parent1.code[point:]
    return child1, child2

def mutation(individual, mutation_rate=0.1):
    for i in range(len(individual.code)):
        if random.uniform(0, 1) < mutation_rate:
            individual.code[i] += random.uniform(-0.3, 0.3)
            individual.code[i] = max(0, min(1, individual.code[i]))

# Parametri genetskog algoritma
GENS = 40
POPULATION_SIZE = 10
GENOME_SIZE = 4

data = []
population = [Individual(GENOME_SIZE) for _ in range(POPULATION_SIZE)]

# Evaluacija prve generacije
for individual in population:
    individual.calcFit(simulate_game)

# Glavna petlja genetskog algoritma
for generation in range(GENS):
    population.sort(reverse=True)
    new_population = []
    ELITISM_COUNT = 2
    new_population.extend(population[:ELITISM_COUNT])

    while len(new_population) < POPULATION_SIZE:
        parent1 = tournament_selection(population)
        parent2 = tournament_selection(population)
        child1, child2 = crossover(parent1, parent2)
        mutation(child1, 0.2)
        mutation(child2, 0.2)
        child1.calcFit(simulate_game)
        child2.calcFit(simulate_game)
        new_population.append(child1)
        if len(new_population) < POPULATION_SIZE:
            new_population.append(child2)

    population = new_population
    for i in range(ELITISM_COUNT):
        population[i].calcFit(simulate_game)

    best_individual = max(population, key=lambda ind: ind.fitness)
    worst_individual = min(population, key=lambda ind: ind.fitness)
    avg_fitness = sum(ind.fitness for ind in population) / len(population)

    log_entry = f"Generation {generation + 1}: Best fitness = {best_individual.fitness}, Worst fitness = {worst_individual.fitness}, Avg fitness = {avg_fitness}\nBest genome: {best_individual.code}"
    data.append(log_entry)

    print(log_entry)