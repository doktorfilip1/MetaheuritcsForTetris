def _well_sum(field):
    h = len(field); w = len(field[0])
    total = 0
    for c in range(w):
        for r in range(h):
            left  = 1 if c == 0     else field[r][c-1]
            right = 1 if c == w-1   else field[r][c+1]
            if field[r][c] == 0 and left == 1 and right == 1:
                d = 0; rr = r
                while rr < h and field[rr][c] == 0:
                    d += 1; rr += 1
                total += d
    return total

def _column_transitions(field):
    h = len(field); w = len(field[0])
    trans = 0
    for c in range(w):
        prev = 1
        for r in range(h):
            cur = field[r][c]
            if cur != prev:
                trans += 1
            prev = cur
        if prev == 0:
            trans += 1
    return trans

def calculate_fitness(field, alpha):

    height = len(field); width = len(field[0])
    holes = 0
    for c in range(width):
        seen = False
        for r in range(height):
            if field[r][c] == 1:
                seen = True
            elif seen and field[r][c] == 0:
                holes += 1

    max_h = 0
    col_h = []
    for c in range(width):
        h = 0
        for r in range(height):
            if field[r][c] == 1:
                h = height - r
                break
        col_h.append(h)
        if h > max_h:
            max_h = h

    bump = sum(abs(col_h[i] - col_h[i+1]) for i in range(width - 1))

    full_lines = 0
    for r in range(height):
        if all(field[r][c] == 1 for c in range(width)):
            full_lines += 1

    bonus = [0, 1, 3, 5, 8]
    line_bonus = bonus[min(full_lines, 4)]

    wells = _well_sum(field)
    trans = _column_transitions(field)
    H = height; W = width
    holes_n = holes / (H * W)
    max_h_n = max_h / H
    bump_n  = bump / (H * (W - 1)) if W > 1 else 0
    line_n  = line_bonus / 8.0
    wells_cap = H * W / 2
    wells_n = min(wells, wells_cap) / wells_cap
    trans_n = trans / (2 * H * W)

    if len(alpha) < 6:
        return - (holes_n * alpha[0] + max_h_n * alpha[1] + bump_n * alpha[2]) \
               + (line_n * alpha[3])

    return (
        - (holes_n * alpha[0] + max_h_n * alpha[1] + bump_n * alpha[2])
        + (line_n * alpha[3])
        + (wells_n * alpha[4])
        - (trans_n * alpha[5])
    )