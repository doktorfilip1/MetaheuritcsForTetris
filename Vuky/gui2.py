import pygame
import time
import random

pygame.init()

# Dimenzije ekrana i blokova
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Boje
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)

COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

font_text = pygame.font.SysFont("comicsans", 25)


def draw_grid(grid, score, elapsed_time):
    screen.fill(GRAY)

    # Crtanje okvira table
    pygame.draw.rect(screen, BLUE, (50, 50, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 3)

    for y in range(1, GRID_HEIGHT):
        pygame.draw.line(screen, WHITE, (50, 50 + y * BLOCK_SIZE), (50 + GRID_WIDTH * BLOCK_SIZE, 50 + y * BLOCK_SIZE), 1)
    for x in range(1, GRID_WIDTH):
        pygame.draw.line(screen, WHITE, (50 + x * BLOCK_SIZE, 50), (50 + x * BLOCK_SIZE, 50 + GRID_HEIGHT * BLOCK_SIZE), 1)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[cell - 1], (50 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (50 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    score_text = font_text.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (400, 330))

    pygame.display.update()


def main():
    with open("sheets.txt", "r") as file:
        data = file.readlines()

    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    start_time = time.time()

    for line in data:
        line = line.strip()
        if line.startswith("[["):
            grid = eval(line)
            elapsed_time = int(time.time() - start_time)
            draw_grid(grid, score, elapsed_time)
            time.sleep(0.20)  # Sporije padanje blokova
        elif line.isdigit():
            score = int(line)
            elapsed_time = int(time.time() - start_time)
            draw_grid(grid, score, elapsed_time)
            time.sleep(0.5)  # Duža pauza za prikaz ažuriranja score-a

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()