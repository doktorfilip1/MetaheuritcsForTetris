import random
import json
import numpy as np
from typing import List, Optional, Dict, Any
from .board import X, Y, FIGURES, can_place, variations, clear_full_lines
from .fitness import calculate_fitness

def simulate_game(
    alpha: List[float],
    write_frames: bool = False,
    max_steps: Optional[int] = None,      # None = bez limita
    capture: bool = False,
    piece_sequence: Optional[List[List[List[int]]]] = None,
) -> Any:
    table = [[0 for _ in range(X)] for _ in range(Y)]
    score = 0
    writer = open("sheets.txt", "w", encoding="utf-8") if write_frames else None

    seq_idx = 0
    used_pieces: List[List[List[int]]] = []

    def next_rand_piece():
        return random.choice(FIGURES)

    if piece_sequence and len(piece_sequence) > 0:
        current_block = piece_sequence[0]
        next_block = piece_sequence[1] if len(piece_sequence) > 1 else next_rand_piece()
        seq_idx = 2
    else:
        current_block = next_rand_piece()
        next_block = next_rand_piece()

    steps = 0
    while True:
        if max_steps is not None and steps >= max_steps:
            break
        steps += 1

        if writer:
            writer.write("NEXT:" + json.dumps(next_block) + "\n")

        rots = []
        b = np.array(current_block)
        for k in range(4):
            bb = np.rot90(b, k)
            if can_place(table, bb):
                rots.append(bb)
        if not rots:
            break

        best_field = None
        best_val = float("-inf")
        for bb in rots:
            for fld in variations(table, bb):
                val = calculate_fitness(fld, alpha)
                if val > best_val:
                    best_val = val
                    best_field = fld

        table = best_field
        table, lines = clear_full_lines(table)

        if lines == 1:
            score += 1
        elif lines == 2:
            score += 3
        elif lines == 3:
            score += 5
        elif lines == 4:
            score += 8

        if writer:
            writer.write(str(table) + "\n")
            writer.write(str(score) + "\n")

        if capture:
            used_pieces.append(current_block)

        if piece_sequence and seq_idx < len(piece_sequence):
            current_block = next_block
            next_block = piece_sequence[seq_idx]
            seq_idx += 1
        else:
            current_block = next_block
            next_block = next_rand_piece()

    if writer:
        placed = []
        for y in range(Y):
            for x in range(X):
                if table[y][x] == 0 and best_field[y][x] != 0:
                    placed.append((x, y))
        writer.write("PLACED:" + str(placed) + "\n")

    if capture:
        return {"pieces_used": used_pieces, "score": score}
    return score