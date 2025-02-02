import random
from copy import deepcopy
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





# Dummy funkcija koja simulira igru i vraća rezultat na osnovu težinskih faktora
def simulate_game(alpha):
    f = open("sheets.txt", 'w')
    
    
    figures = [
        [[1, 0, 0], [1, 1, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[0, 1, 0], [1, 1, 1]],
        [[1, 1], [1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[1, 1, 1, 1]],
    ]
    x = 10
    y = 20

    table = [[0 for _ in range(x)] for _ in range(y)]
    SCORE = 0

    while True:
        next_block = random.choice(figures)  # Izbor nasumičnog bloka
        check = 0

        if can_place_next_block(table, next_block):
            field_variations1 = find_all_field_variations_for_block(table, next_block)
            check = 1
        if can_place_next_block(table, np.rot90(next_block)):
            field_variations2 = find_all_field_variations_for_block(table, np.rot90(next_block))
            check = 1
        if can_place_next_block(table, np.rot90(np.rot90(next_block))):
            field_variations3 = find_all_field_variations_for_block(table, np.rot90(np.rot90(next_block)))
            check = 1
        if can_place_next_block(table, np.rot90(np.rot90(np.rot90(next_block)))):
            field_variations4 = find_all_field_variations_for_block(table, np.rot90(np.rot90(np.rot90(next_block))))
            check = 1
        if check == 0:
            break
        else:
            best_fitness = float('inf')
            best_field = None
            for fld in field_variations1:
                ft = calculate_fitness(fld, alpha)
                if ft < best_fitness:
                    best_field = fld
                    best_fitness = ft
            table = best_field
            
            for fld in field_variations2:
                ft = calculate_fitness(fld, alpha)
                if ft < best_fitness:
                    best_field = fld
                    best_fitness = ft
            table = best_field
            
            for fld in field_variations3:
                ft = calculate_fitness(fld, alpha)
                if ft < best_fitness:
                    best_field = fld
                    best_fitness = ft
            table = best_field
            
            for fld in field_variations4:
                ft = calculate_fitness(fld, alpha)
                if ft < best_fitness:
                    best_field = fld
                    best_fitness = ft
            table = best_field
            f.write(str(next_block) + '\n' + str(table)+ '\n' + str(SCORE) + '\n')
            
            for i in range(y):
                lineFull = True
                for j in range(x):
                    if table[i][j] == 0:
                        lineFull = False
                if lineFull:
                    SCORE += 2
                    for m in range(i,0,-1):
                        for k in range(x):
                            table[m][k] = table[m-1][k]
                    for m in range(x):
                        table[0][m] = 0
            f.write(str(table) + '\n')
                            
                    

    
    
    return SCORE


def is_valid_placement(field, block, row, col):
    """Check if placing the block at (row, col) is valid."""
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
    """Check if the block can rest at the given position."""
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
        for row in range(field_h - block_h, -1, -1):  # Start from the bottom
            if is_valid_placement(field, block, row, col) and can_fall_to_position(field, block, row, col):
                return True  # Found at least one valid position

    return False  # No valid position found

def find_all_field_variations_for_block(field, block):
    """Find all possible field variations with the block placed in its current orientation."""
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


def calculate_fitness(field,alpha):
    """Calculate the fitness of the field based on empty spaces, max height, and roughness."""
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
            lineFull = width*height
            
    
    # Combine metrics into fitness score
    fitness = empty_spaces*alpha[0] + max_height*alpha[1] + roughness*alpha[2] - lineFull*alpha[3]
    return fitness
    
    #izmena test


jedinka = Individual(4)
jedinka.code = [1, 0.09113101904215162, 0.18042873323415054, 0.34171898623702524]
for i in range(1):
    jedinka.calcFit(simulate_game)
    print(i+1, "gen, fitness: ", jedinka.fitness)