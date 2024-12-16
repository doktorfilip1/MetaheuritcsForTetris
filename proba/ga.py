import numpy as np
from copy import deepcopy

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

# Example usage
field = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0]
]

block = [
    [1, 1, 1],
    [0, 0, 1]
]  # T-shape block

field_variations = find_all_field_variations_for_block(field, block)
for i, variation in enumerate(field_variations):
    print(f"Field Variation {i + 1}:")
    print(np.array(variation))
