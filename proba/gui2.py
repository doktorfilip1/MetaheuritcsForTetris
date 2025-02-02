import pygame
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Visualization")

# Font for score
font = pygame.font.SysFont("comicsans", 30)

def draw_grid(grid, score):
    screen.fill(BLACK)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[cell - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, (255,0,0))
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
    
    pygame.display.update()

def main():
    with open("sheets.txt", "r") as file:
        data = file.readlines()

    grid = []
    score = 0
    next_block = None

    for line in data:
        line = line.strip()
        if line.startswith("[["):
            if next_block is None:
                next_block = eval(line)
            else:
                grid = eval(line)
                draw_grid(grid, score)
                time.sleep(0.05)  # Slow down the falling blocks
        elif line.isdigit():
            score = int(line)
            draw_grid(grid, score)
            time.sleep(0.4)  # Pause to show the score update

    # Keep the window open until closed by the user
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()