from copy import deepcopy
import numpy as np

X, Y = 10, 20

FIGURES = [
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]],
    [[0,1,0],[1,1,1]],
    [[1,1],[1,1]],
    [[0,1,1],[1,1,0]],
    [[1,1,0],[0,1,1]],
    [[1,1,1,1]],
]

def is_valid(field, block, row, col):
    h, w = len(field), len(field[0])
    b = np.array(block); bh, bw = b.shape
    if row+bh > h or col+bw > w: return False
    for i in range(bh):
        for j in range(bw):
            if b[i,j] == 1 and field[row+i][col+j] == 1:
                return False
    return True

def can_fall(field, block, row, col):
    b = np.array(block); bh, bw = b.shape
    if row + bh == len(field): return True
    for i in range(bh):
        for j in range(bw):
            if b[i,j] == 1 and field[row+i+1][col+j] == 1:
                return True
    return False

def place(field, block, row, col):
    b = np.array(block)
    out = deepcopy(field)
    bh, bw = b.shape
    for i in range(bh):
        for j in range(bw):
            if b[i,j] == 1:
                out[row+i][col+j] = 1
    return out

def can_place(field, block):
    h, w = len(field), len(field[0])
    b = np.array(block); bh, bw = b.shape
    for c in range(w - bw + 1):
        for r in range(h - bh, -1, -1):
            if is_valid(field, b, r, c) and can_fall(field, b, r, c):
                return True
    return False

def variations(field, block):
    res = []
    h, w = len(field), len(field[0])
    b = np.array(block); bh, bw = b.shape
    for c in range(w - bw + 1):
        for r in range(h - bh, -1, -1):
            if is_valid(field, b, r, c) and can_fall(field, b, r, c):
                res.append(place(field, b, r, c))
                break
    return res

def clear_full_lines(table):
    lines_cleared = 0
    new_t = [row[:] for row in table]
    write_ptr = Y - 1
    for r in range(Y - 1, -1, -1):
        if all(new_t[r][c] == 1 for c in range(X)):
            lines_cleared += 1
        else:
            new_t[write_ptr] = new_t[r][:]
            write_ptr -= 1
    for r in range(write_ptr, -1, -1):
        new_t[r] = [0] * X
    return new_t, lines_cleared

