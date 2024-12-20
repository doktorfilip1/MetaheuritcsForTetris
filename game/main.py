import random
from copy import deepcopy
import numpy as np
import json


class Individual:
    def __init__(self, genome_size):
        # Težinski faktori za različite aspekte igre
        self.code = [random.uniform(0, 1) for _ in range(genome_size)]
        self.fitness = None

    def calcFit(self, simulate_game):
        # Fitness funkcija simulira igru i vraća rezultat (npr. broj poena)
        self.fitness = simulate_game(self.code)
        return self.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness


def selection(population):
    TOURNAMENT_SIZE = 5
    best = None
    for _ in range(TOURNAMENT_SIZE):
        candidate = random.choice(population)
        if best is None or candidate.fitness > best.fitness:
            best = candidate
    return best


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
            individual.code[i] += random.uniform(-0.1, 0.1)
            individual.code[i] = max(0, min(1, individual.code[i]))


# Dummy funkcija koja simulira igru i vraća rezultat na osnovu težinskih faktora
def simulate_game(alpha):
    figures = [
        [[1, 0, 0], [1, 1, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[0, 1, 0], [1, 1, 1]],
        [[1, 1], [1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[1, 1, 1, 1]],
    ]
    x, y = 10, 20
    table = [[0 for _ in range(x)] for _ in range(y)]
    score = 0

    while True:
        next_block = random.choice(figures)  # Izbor nasumičnog bloka
        field_variations = []

        # Generisanje svih rotacija i validnih varijacija za blok
        for rotation in range(4):
            rotated_block = np.rot90(next_block, rotation)
            if can_place_next_block(table, rotated_block):
                field_variations.extend(find_all_field_variations_for_block(table, rotated_block))

        if not field_variations:  # Ako nema validnih pozicija, igra se završava
            break

        # Pronalazak najboljeg fitnesa i ažuriranje tabele
        best_fitness = float('inf')
        best_field = None
        for field in field_variations:
            fitness = calculate_fitness(field, alpha)
            if fitness < best_fitness:
                best_fitness = fitness
                best_field = field

        table = best_field

        # Provera i uklanjanje kompletnih linija
        for i in range(y):
            if all(table[i][j] == 1 for j in range(x)):
                score += 2
                for m in range(i, 0, -1):
                    table[m] = table[m - 1][:]
                table[0] = [0] * x

    return score


def is_valid_placement(field, block, row, col):
    """Check if placing the block at (row, col) is valid."""
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    if row + block_h > field_h or col + block_w > field_w:
        return False  # Block goes out of bounds

    for i in range(block_h):
        for j in range(block_w):
            if block[i][j] == 1 and field[row + i][col + j] == 1:
                return False  # Overlap with occupied space

    return True

def can_fall_to_position(field, block, row, col):
    """Check if the block can rest at the given position."""
    block_h, block_w = len(block), len(block[0])
    field_h = len(field)

    # Block is at the bottom or rests on another block
    if row + block_h == field_h or any(
        block[i][j] == 1 and field[row + i + 1][col + j] == 1
        for i in range(block_h)
        for j in range(block_w)
    ):
        return True

    return False

def place_block(field, block, row, col):
    """Place the block on the field at (row, col)."""
    field = deepcopy(field)
    block_h, block_w = len(block), len(block[0])

    for i in range(block_h):
        for j in range(block_w):
            if block[i][j] == 1:
                field[row + i][col + j] = 1

    return field

def can_place_next_block(field, block):
    """Check if the next block can be placed on the field in any valid position."""
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    for col in range(field_w - block_w + 1):
        for row in range(field_h - block_h, -1, -1):  # Start from bottom
            if is_valid_placement(field, block, row, col) and can_fall_to_position(field, block, row, col):
                return True

    return False

def find_all_field_variations_for_block(field, block):
    """Find all possible field variations with the block placed in its current orientation."""
    variations = []
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    for col in range(field_w - block_w + 1):
        for row in range(field_h - block_h, -1, -1):  # Start from bottom
            if is_valid_placement(field, block, row, col) and can_fall_to_position(field, block, row, col):
                new_field = place_block(field, block, row, col)
                variations.append(new_field)
                break  # Only consider the first valid placement for each column

    return variations


def calculate_fitness(field, alpha):
    """Calculate the fitness of the field based on empty spaces, max height, roughness, potential lines, and full lines."""
    height = len(field)
    width = len(field[0])

    # Calculate empty block spaces
    empty_spaces = 0
    for col in range(width):
        filled_found = False
        for row in range(height):
            if field[row][col] == 1:
                filled_found = True
            elif filled_found and field[row][col] == 0:
                empty_spaces += 1

    # Calculate max height
    max_height = 0
    for col in range(width):
        for row in range(height):
            if field[row][col] == 1:
                max_height = max(max_height, height - row)
                break

    # Calculate roughness (difference in column heights)
    heights = []
    for col in range(width):
        col_height = 0
        for row in range(height):
            if field[row][col] == 1:
                col_height = height - row
                break
        heights.append(col_height)
    roughness = sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))

    # Calculate potential for future lines
    potential_lines = 0
    for i in range(height):
        filled_cells = sum(1 for j in range(width) if field[i][j] == 1)
        if filled_cells >= width - 2:  # Ako je linija skoro popunjena
            potential_lines += 1

    # Calculate completely full lines
    lineFull = 0
    for i in range(height):
        if all(field[i][j] == 1 for j in range(width)):
            lineFull += 1

    fitness = (empty_spaces * alpha[0] +
               max_height * alpha[1] +
               roughness * alpha[2] -
               potential_lines * alpha[3] -
               lineFull * alpha[4])
    return fitness

GENS = 30
POPULATION_SIZE = 15
GENOME_SIZE = 5  # Broj težinskih faktora

# Inicijalizacija populacije
population = [Individual(GENOME_SIZE) for _ in range(POPULATION_SIZE)]
bestFitness = 0
bestCode = [0, 0, 0, 0, 0]

for individual in population:
    individual.calcFit(simulate_game)

results = {"generations": [], "best_fitness": []}

# Glavna petlja genetskog algoritma
for generation in range(GENS):
    population.sort(reverse=True)
    new_population = []

    ELITISM_COUNT = 2
    new_population.extend(population[:ELITISM_COUNT])

    while len(new_population) < POPULATION_SIZE:
        parent1 = selection(population)
        parent2 = selection(population)
        child1, child2 = crossover(parent1, parent2)
        mutation(child1, mutation_rate=0.1)
        mutation(child2, mutation_rate=0.1)
        child1.calcFit(simulate_game)
        child2.calcFit(simulate_game)
        new_population.append(child1)
        if len(new_population) < POPULATION_SIZE:
            new_population.append(child2)

    population = new_population

    for i in range(ELITISM_COUNT):
        population[i].calcFit(simulate_game)

    best_individual = max(population, key=lambda ind: ind.fitness)

    if best_individual.fitness > bestFitness:
        bestCode = best_individual.code
        bestFitness = best_individual.fitness

    results["generations"].append(generation + 1)
    results["best_fitness"].append(best_individual.fitness)

    print(f"Generation {generation + 1}: Best fitness = {best_individual.fitness}")

with open("results.json", "w") as f:
    json.dump(results, f)

# Najbolji rezultat nakon evolucije
best_individual = max(population, key=lambda ind: ind.fitness)
if best_individual.fitness > bestFitness:
    bestCode = best_individual.code
    bestFitness = best_individual.fitness

print("Best genome:", best_individual.code)
print("Best in all iterations genome:", bestCode, " fitness: ", bestFitness)