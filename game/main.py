import random
import pickle
import numpy as np
from copy import deepcopy


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

def roulette_wheel_selection(population):
    total_fitness = sum(individual.fitness for individual in population)
    spin = random.uniform(0, total_fitness)

    cumulative_fitness = 0
    for individual in population:
        cumulative_fitness += individual.fitness
        if cumulative_fitness > spin:
            return individual

    return population[-1]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1.code) - 1)
    child1 = Individual(len(parent1.code))
    child2 = Individual(len(parent1.code))
    child1.code = parent1.code[:point] + parent2.code[point:]
    child2.code = parent2.code[:point] + parent1.code[point:]
    return child1, child2

def mutation(individual, mutation_rate=0.2):
    for i in range(len(individual.code)):
        if random.uniform(0, 1) < mutation_rate:
            individual.code[i] += random.uniform(-0.1, 0.1)
            individual.code[i] = max(0, min(1, individual.code[i]))

# Dummy funkcija koja simulira igru i vraća rezultat na osnovu težinskih faktora
def simulate_game(alpha):
    figures = [
        [[[1, 0, 0], [1, 1, 1]], [[1, 1], [0, 1], [0, 1]], [[1, 1, 1], [0, 0, 1]], [[1, 0], [1, 0], [1, 1]]],
        [[[0, 0, 1], [1, 1, 1]], [[1, 0], [1, 0], [1, 1]], [[1, 1, 1], [1, 0, 0]], [[1, 1], [0, 1], [0, 1]]],
        [[[0, 1, 0], [1, 1, 1]], [[1, 0], [1, 1], [1, 0]], [[1, 1, 1], [0, 1, 0]], [[0, 1], [1, 1], [0, 1]]],
        [[[1, 1], [1, 1]]],
        [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]],
        [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]],
        [[[1, 1, 1, 1]], [[1], [1], [1], [1]]]
    ]
    x = 10
    y = 20

    table = np.zeros((y, x), dtype=int)
    SCORE = 0

    while True:
        next_block_rotations = random.choice(figures)  # Izbor nasumičnog bloka sa svim rotacijama
        best_fitness = float('inf')
        best_field = None

        for rotation in next_block_rotations:
            block = np.array(rotation)
            block_h, block_w = block.shape

            for col in range(x - block_w + 1):
                for row in range(y - block_h, -1, -1):
                    if is_valid_placement(table, block, row, col):
                        new_field = place_block(table, block, row, col)
                        ft = calculate_fitness(new_field, alpha)
                        if ft < best_fitness:
                            best_field = new_field
                            best_fitness = ft

        if best_field is None:
            break

        table = best_field

        # Provera i brisanje popunjenih linija
        full_lines = np.all(table == 1, axis=1)
        if np.any(full_lines):
            SCORE += np.sum(full_lines) * 2
            table = np.delete(table, np.where(full_lines), axis=0)
            table = np.vstack([np.zeros((np.sum(full_lines), x), dtype=int), table])

    return SCORE

def is_valid_placement(field, block, row, col):
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    if row + block_h > field_h or col + block_w > field_w:
        return False  # Blok izlazi izvan okvira

    for i in range(block_h):
        for j in range(block_w):
            if block[i][j] == 1 and field[row + i][col + j] == 1:
                return False  # Preklapa se sa zauzetim mestom

    return True

def can_fall_to_position(field, block, row, col):
    block_h, block_w = len(block), len(block[0])

    # Proverava da li ce blok "lebdeti"
    if row + block_h == len(field):
        return True  # Blok je na dnu

    for i in range(block_h):
        for j in range(block_w):
            if block[i][j] == 1 and field[row + i + 1][col + j] == 1:
                return True  # Blok se oslanja na drugi blok

    return False

def place_block(field, block, row, col):
    field = deepcopy(field)
    block_h, block_w = len(block), len(block[0])

    for i in range(block_h):
        for j in range(block_w):
            if block[i][j] == 1:
                field[row + i][col + j] = 1

    return field

def can_place_next_block(field, block):
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    for col in range(field_w - block_w + 1):
        for row in range(field_h - block_h, -1, -1):  # Krece od dna
            if is_valid_placement(field, block, row, col) and can_fall_to_position(field, block, row, col):
                return True  # Pronadji makar jednu validnu poziciju

    return False  # Nije pronadjena pozcija za blok

def find_all_field_variations_for_block(field, block):
    variations = []
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    for col in range(field_w - block_w + 1):
        for row in range(field_h - block_h, -1, -1):
            if is_valid_placement(field, block, row, col) and can_fall_to_position(field, block, row, col):
                new_field = place_block(field, block, row, col)
                variations.append(new_field)
                break
    return variations

def calculate_fitness(field, alpha):
    height = len(field)
    width = len(field[0])

    # Racuna prazna mesta
    empty_spaces = 0
    for col in range(width):
        filled_found = False
        for row in range(height):
            if field[row][col] == 1:
                filled_found = True
            elif filled_found and field[row][col] == 0:
                empty_spaces += 1

    # racuna maksimalnu visinu
    max_height = 0
    for col in range(width):
        for row in range(height):
            if field[row][col] == 1:
                max_height = max(max_height, height - row)
                break

    # Racuna razliku visina susednih redova
    heights = []
    for col in range(width):
        col_height = 0
        for row in range(height):
            if field[row][col] == 1:
                col_height = height - row
                break
        heights.append(col_height)
    roughness = sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))

    # Racuna mogucnost zatvaranja linije
    lineFull = 0
    for i in range(height):
        is_line_full = True
        for j in range(width):
            if field[i][j] == 0:
                is_line_full = False
        if is_line_full:
            lineFull += width * height

    # Kombinuje predjasnje elemente
    fitness = empty_spaces * alpha[0] + max_height * alpha[1] + roughness * alpha[2] - lineFull * alpha[3]
    return fitness


# Parametri genetskog algoritma
GENS = 20
POPULATION_SIZE = 10
GENOME_SIZE = 4

# Inicijalizacija populacije
population = [Individual(GENOME_SIZE) for _ in range(POPULATION_SIZE)]
bestFitness = 0
bestCode = [0, 0, 0, 0]
fitness_history = []

# Prva evaluacija populacije
for individual in population:
    individual.calcFit(simulate_game)

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
        mutation(child1)
        mutation(child2)
        child1.calcFit(simulate_game)
        child2.calcFit(simulate_game)
        new_population.append(child1)
        if len(new_population) < POPULATION_SIZE:
            new_population.append(child2)

    population = new_population
    for i in range(ELITISM_COUNT):
        population[i].calcFit(simulate_game)

    best_individual = max(population, key=lambda ind: ind.fitness)
    fitness_history.append(best_individual.fitness)
    print(f"Generation {generation + 1}: Best fitness = {best_individual.fitness}")

with open("fitness_data.pkl", "wb") as f:
    pickle.dump(fitness_history, f)

print("Fitness data saved to fitness_data.pkl")