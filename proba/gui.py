import pygame
import time
import ast

def load_data(filename):
    with open(filename, "r") as f:
        raw_data = f.read().strip().split("\n\n")  # Split by empty lines

    game_states = []
    for i, entry in enumerate(raw_data):
        if i > 2:  # Stop after first 3 entries to avoid too much output
            print("... (output hidden) ...")
            break  

        parts = entry.split("\n", 3)  # Expecting 4 parts
        if len(parts) < 4:
            print(f"Skipping incomplete entry at index {i}")
            continue
        
        try:
            next_block = ast.literal_eval(parts[0].strip())
            placed_table = ast.literal_eval(parts[1].strip())
            score = int(parts[2].strip())
            cleared_table = ast.literal_eval(parts[3].strip())
            game_states.append((next_block, placed_table, score, cleared_table))
        except Exception as e:
            print(f"\n❌ ERROR while parsing entry {i} ❌")
            print(f"❌ Error Message: {e}\n")
            break  # Stop immediately on error

    return game_states


def draw_grid(screen, grid, offset_x=0, color=(200, 200, 200)):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect((x + offset_x) * 30, y * 30, 30, 30)
            pygame.draw.rect(screen, (50, 50, 50) if cell == 0 else (0, 255, 255), rect)
            pygame.draw.rect(screen, color, rect, 1)

def visualize_tetris(filename):
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    clock = pygame.time.Clock()
    
    game_states = load_data(filename)
    for i, (next_block, placed_table, score, cleared_table) in enumerate(game_states):
        print(f"Displaying state {i+1} / {len(game_states)}")

        screen.fill((0, 0, 0))
        draw_grid(screen, placed_table)
        pygame.display.flip()
        time.sleep(1)  # Show placed board before animation
        
        # Animate block falling
        max_offset_x = max(0, len(placed_table[0]) - len(next_block[0]))  # Avoid out-of-bounds
        for offset_x in range(max_offset_x + 1):
            screen.fill((0, 0, 0))
            draw_grid(screen, placed_table)
            draw_grid(screen, next_block, offset_x, (255, 0, 0))
            pygame.display.flip()
            time.sleep(0.2)

        time.sleep(1)  # Pause before clearing lines

        # Show cleared board
        screen.fill((0, 0, 0))
        draw_grid(screen, cleared_table)
        pygame.display.flip()
        time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    visualize_tetris("sheets.txt")
