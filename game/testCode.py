import random
from copy import deepcopy
from time import sleep

import numpy as np


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


def mutation(individual, mutation_rate=0.2):
    for i in range(len(individual.code)):
        if random.uniform(0, 1) < mutation_rate:
            individual.code[i] += random.uniform(-0.3, 0.3)
            individual.code[i] = max(0, min(1, individual.code[i]))


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
    SCORE = 0

    with open("output.txt", "w") as file:
        while True:
            next_block = random.choice(figures)
            check = any(can_place_next_block(table, np.rot90(next_block, i)) for i in range(4))
            if not check:
                break

            best_fitness = float('inf')
            best_field = None
            for i in range(4):
                rotated_block = np.rot90(next_block, i)
                variations = find_all_field_variations_for_block(table, rotated_block)
                for fld in variations:
                    ft = calculate_fitness(fld, alpha)
                    if ft < best_fitness:
                        best_field = fld
                        best_fitness = ft
            table = best_field

            table, lines_cleared = clear_full_lines(table)
            SCORE += lines_cleared  # Povećaj rezultat na osnovu obrisanih linija

            file.write(f"Next block: {next_block}\n")
            file.write(f"Table:\n{np.array(table)}\n")
            file.write(f"Score: {SCORE}\n\n")

    return SCORE


def clear_full_lines(field):
    new_field = [row for row in field if not all(row)]
    lines_cleared = len(field) - len(new_field)

    while len(new_field) < len(field):
        new_field.insert(0, [0] * len(field[0]))

    return new_field, lines_cleared

def is_valid_placement(field, block, row, col):
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    if row + block_h > field_h or col + block_w > field_w:
        return False  # Block goes out of field bounds

    for i in range(block_h):
        for j in range(block_w):
            if block[i][j] == 1 and field[row + i][col + j] == 1:
                return False  # Overlap with occupied space

    return True


def can_fall_to_position(field, block, row, col):
    block_h, block_w = len(block), len(block[0])

    # Check if the block can stay at the given row without floating
    if row + block_h == len(field):
        return True  # Block is at the bottom

    for i in range(block_h):
        for j in range(block_w):
            if block[i][j] == 1 and field[row + i + 1][col + j] == 1:
                return True  # Block rests on another block

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
        for row in range(field_h - block_h, -1, -1):  # Start from the bottom
            if is_valid_placement(field, block, row, col) and can_fall_to_position(field, block, row, col):
                return True  # Found at least one valid position

    return False  # No valid position found


def find_all_field_variations_for_block(field, block):
    variations = []
    field_h, field_w = len(field), len(field[0])
    block_h, block_w = len(block), len(block[0])

    for col in range(field_w - block_w + 1):
        for row in range(field_h - block_h, -1, -1):  # Start from the bottom
            if is_valid_placement(field, block, row, col) and can_fall_to_position(field, block, row, col):
                new_field = place_block(field, block, row, col)
                variations.append(new_field)
                break  # Only consider the first valid placement for each column

    return variations


def calculate_fitness(field, alpha):
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

    # Calculate lineClose
    lineFull = 0
    for i in range(height):
        lineFull = True
        for j in range(width):
            if field[i][j] == 0:
                lineFull = False
        if lineFull:
            lineFull = width * height

    # Combine metrics into fitness score
    fitness = empty_spaces * alpha[0] + max_height * alpha[1] + roughness * alpha[2] - lineFull * alpha[3]
    return fitness


jedinka = Individual(4)
# jedinka.code = [0.7081688134659031, 0.11014248648423453, 0.13999307043093268, 0.846820491045681]
jedinka.code = [0.9635348759805299, 0.02197870449645889, 0.22959360116973254, 0.20793209342444544]

for i in range(1):
    jedinka.calcFit(simulate_game)
    print(i + 1, "gen, fitness: ", jedinka.fitness)