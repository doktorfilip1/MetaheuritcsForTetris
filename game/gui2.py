import pygame
import time
import ast
import json
import os

pygame.init()

GRID_W, GRID_H = 10, 20
BLOCK = 30
PADDING = 50

HEADER_H = 100
FIELD_W, FIELD_H = GRID_W * BLOCK, GRID_H * BLOCK

SCREEN_W = PADDING + FIELD_W + 240 + PADDING
SCREEN_H = HEADER_H + PADDING + FIELD_H + PADDING

BG = (28, 31, 38)
GRID_CLR = (75, 80, 92)
FIELD_BR = (66, 133, 244)
PANEL_BG = (36, 41, 51)
PANEL_BR = (58, 65, 78)
TEXT_CLR = (230, 235, 245)
SUBTLE = (180, 190, 205)
ACCENT = (255, 82, 82)
HEADER_BG = (32, 36, 44)

DEFAULT_COLOR = (0, 229, 255)
HILITE_BORDER = (255, 88, 88)


screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("tetris")
font_small = pygame.font.SysFont("segoeui", 20, bold=True)
font_med   = pygame.font.SysFont("segoeui", 26, bold=True)
font_big   = pygame.font.SysFont("segoeui", 34, bold=True)
clock = pygame.time.Clock()


FIELD_ORIGIN_Y = HEADER_H
PANEL_X = PADDING + FIELD_W + 24
PANEL_Y = FIELD_ORIGIN_Y + PADDING
PANEL_W = SCREEN_W - PANEL_X - PADDING
PANEL_H = FIELD_H

BTN_W, BTN_H = 140, 42
STOP_BTN = pygame.Rect(
    PANEL_X + (PANEL_W - BTN_W) // 2,
    PANEL_Y + PANEL_H - BTN_H - 16,
    BTN_W, BTN_H
)

NEXT_BOX = pygame.Rect(PANEL_X + 20, PANEL_Y + 64, PANEL_W - 40, 120)

def parse_placed(line: str):
    if not line.startswith("PLACED:"):
        return None
    try:
        return ast.literal_eval(line[7:].strip())
    except Exception:
        return None

def draw_rounded_rect(surf, rect, color, radius=12, width=0, border_color=None, border_width=2):
    pygame.draw.rect(surf, color, rect, border_radius=radius, width=width)
    if border_color and border_width > 0:
        pygame.draw.rect(surf, border_color, rect, border_radius=radius, width=border_width)

def parse_grid(line: str):
    try:
        grid = ast.literal_eval(line)
        if isinstance(grid, list) and grid and isinstance(grid[0], list):
            return grid
    except Exception:
        pass
    return None

def parse_next(line: str):
    if not line.startswith("NEXT:"):
        return None
    payload = line[5:].strip()
    try:
        mat = ast.literal_eval(payload)
        if isinstance(mat, list) and mat and isinstance(mat[0], list):
            cells = []
            for r, row in enumerate(mat):
                for c, v in enumerate(row):
                    if v:
                        cells.append((c, r))
            return cells
    except Exception:
        return None
    return None

def diff_last_piece(prev_grid, cur_grid):
    if prev_grid is None or cur_grid is None:
        return []
    h, w = len(cur_grid), len(cur_grid[0])
    cells = []
    for y in range(h):
        for x in range(w):
            a = prev_grid[y][x] if (y < len(prev_grid) and x < len(prev_grid[0])) else 0
            b = cur_grid[y][x]
            if a == 0 and b != 0:
                cells.append((x, y))
    return cells

def format_genome(g):
    if not g: return "—"
    return "[" + ", ".join(f"{float(x):.3f}" for x in g) + "]"

def wrap_and_draw_text(text, font, color, x, y, max_width, line_spacing=4):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_width:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    yy = y
    for line in lines:
        surf = font.render(line, True, color)
        screen.blit(surf, (x, yy))
        yy += surf.get_height() + line_spacing

def load_run_meta():
    meta = {"generation": None, "fitness": None, "genome": None, "label": None}
    for path in ("run_meta.json", "best_ever.json", "best_of_last_gen.json"):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "generation" in data: meta["generation"] = data["generation"]
                if "fitness" in data: meta["fitness"] = data["fitness"]
                if "genome" in data and isinstance(data["genome"], list):
                    meta["genome"] = data["genome"]
                if "label" in data: meta["label"] = data["label"]
                break
            except Exception:
                pass
    return meta

RUN_META = load_run_meta()

def draw_header(meta):
    rect = pygame.Rect(0, 0, SCREEN_W, HEADER_H)
    draw_rounded_rect(screen, rect, HEADER_BG, radius=0)

    gen = meta.get("generation")
    fit = meta.get("fitness")
    genome = meta.get("genome")
    label = meta.get("label")

    label_str = f" ({label})" if label else ""
    t1 = font_med.render(f"Generation: {gen if gen is not None else '—'}{label_str}", True, TEXT_CLR)
    t2 = font_med.render(f"Fitness: {fit if fit is not None else '—'}", True, TEXT_CLR)
    screen.blit(t1, (PADDING, 14))
    screen.blit(t2, (PADDING, 14 + t1.get_height() + 8))
    wrap_and_draw_text("Genome: " + format_genome(genome), font_small, TEXT_CLR,
                       PADDING, 14 + t1.get_height() + t2.get_height() + 16, SCREEN_W - 2*PADDING)

def normalize_cells(cells):
    if not cells: return cells
    minx = min(x for x,_ in cells); miny = min(y for _,y in cells)
    return [(x-minx, y-miny) for (x,y) in cells]

def fit_and_draw_cells(box: pygame.Rect, cells, color=(0, 232, 255), outline=(240,240,240)):
    if not cells: return
    norm = normalize_cells(cells)
    maxx = max(x for x,_ in norm)
    maxy = max(y for _,y in norm)
    cell_size = min((box.w - 24)//max(1, maxx+1), (box.h - 24)//max(1, maxy+1))
    offx = box.x + (box.w - cell_size*(maxx+1))//2
    offy = box.y + (box.h - cell_size*(maxy+1))//2
    for (cx, cy) in norm:
        r = pygame.Rect(offx + cx*cell_size, offy + cy*cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, color, r)
        if outline:
            pygame.draw.rect(screen, outline, r, 1)

def draw_field(grid, last_piece_cells):
    screen.fill(BG)
    draw_header(RUN_META)

    field_rect = pygame.Rect(PADDING, FIELD_ORIGIN_Y + PADDING, FIELD_W, FIELD_H)
    pygame.draw.rect(screen, FIELD_BR, field_rect, width=3, border_radius=6)
    for y in range(1, GRID_H):
        pygame.draw.line(screen, GRID_CLR,
                         (PADDING, FIELD_ORIGIN_Y + PADDING + y*BLOCK),
                         (PADDING + FIELD_W, FIELD_ORIGIN_Y + PADDING + y*BLOCK), 1)
    for x in range(1, GRID_W):
        pygame.draw.line(screen, GRID_CLR,
                         (PADDING + x*BLOCK, FIELD_ORIGIN_Y + PADDING),
                         (PADDING + x*BLOCK, FIELD_ORIGIN_Y + PADDING + FIELD_H), 1)

    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if v:
                cell = pygame.Rect(PADDING + x*BLOCK + 1,
                                   FIELD_ORIGIN_Y + PADDING + y*BLOCK + 1,
                                   BLOCK-2, BLOCK-2)
                pygame.draw.rect(screen, DEFAULT_COLOR, cell)
                pygame.draw.rect(screen, (240,240,240), cell, 1)

    for (x, y) in last_piece_cells:
        r = pygame.Rect(PADDING + x*BLOCK,
                        FIELD_ORIGIN_Y + PADDING + y*BLOCK,
                        BLOCK, BLOCK)
        pygame.draw.rect(screen, (0,0,0,0), r)
        pygame.draw.rect(screen, HILITE_BORDER, r, 2)

def draw_button(rect, text, *, bg=(232, 64, 64), hover=(244, 94, 94), fg=(245,245,245)):
    mx, my = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mx, my)
    color = hover if is_hover else bg
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (40,40,40), rect, 2, border_radius=10)
    lbl = font_small.render(text, True, fg)
    screen.blit(lbl, (rect.x + (rect.w - lbl.get_width())//2,
                      rect.y + (rect.h - lbl.get_height())//2))
    return is_hover

def draw_side_panel(score, next_piece_cells):
    draw_rounded_rect(screen, pygame.Rect(PANEL_X, PANEL_Y, PANEL_W, PANEL_H),
                      PANEL_BG, radius=16, border_color=PANEL_BR, border_width=2)

    title = font_med.render("Next piece", True, TEXT_CLR)
    title_x = NEXT_BOX.centerx - title.get_width() // 2
    title_y = NEXT_BOX.y - title.get_height() - 8
    screen.blit(title, (title_x, title_y))

    draw_rounded_rect(screen, NEXT_BOX, (26,29,36), radius=10, border_color=(58,65,78), border_width=2)
    fit_and_draw_cells(NEXT_BOX, next_piece_cells, color=(0, 232, 255))

    score_text = font_big.render(str(score), True, ACCENT)
    score_lbl  = font_small.render("Score", True, SUBTLE)
    lbl_x = PANEL_X + (PANEL_W - score_lbl.get_width()) // 2
    val_x = PANEL_X + (PANEL_W - score_text.get_width()) // 2
    # ispod NEXT box-a
    score_top = NEXT_BOX.bottom + 36
    screen.blit(score_lbl, (lbl_x, score_top))
    screen.blit(score_text, (val_x, score_top + 26))

    draw_button(STOP_BTN, "Stop")

def main():
    with open("sheets.txt", "r", encoding="utf-8") as f:
        data = [line.strip() for line in f if line.strip()]

    grid = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]
    prev_grid = None
    score = 0
    next_piece_cells = []

    draw_field(grid, [])
    draw_side_panel(score, next_piece_cells)
    pygame.display.flip()

    BASE_FPS, STEP_DELAY = 4, 0.12
    running = True

    for line in data:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if STOP_BTN.collidepoint(e.pos):
                    running = False
        if not running:
            break

        if line.startswith("NEXT:"):
            maybe_next = parse_next(line)
            if maybe_next is not None:
                next_piece_cells = maybe_next
            draw_field(grid, [])
            draw_side_panel(score, next_piece_cells)
            pygame.display.flip()
            continue

        new_grid = parse_grid(line)
        if new_grid is not None:
            last_piece = diff_last_piece(prev_grid, new_grid)
            prev_grid = [row[:] for row in new_grid]
            grid = new_grid

            draw_field(grid, last_piece)
            draw_side_panel(score, next_piece_cells)
            pygame.display.flip()
            clock.tick(BASE_FPS); time.sleep(STEP_DELAY)

        elif line.isdigit():
            score = int(line)
            draw_field(grid, [])
            draw_side_panel(score, next_piece_cells)
            pygame.display.flip()
            clock.tick(BASE_FPS); time.sleep(STEP_DELAY)

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if STOP_BTN.collidepoint(e.pos):
                    running = False
        draw_field(grid, [])
        draw_side_panel(score, next_piece_cells)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()