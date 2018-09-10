from enum import Enum
import random

from enum_types import State, TileTypes, types, Tile
from scrollingGrid import Grid

TITLE = "Infinisweeper"
TILE = 32

TILESW = 20
TILESH = 16

WIDTH = TILESW * TILE
HEIGHT = TILESH * TILE

WINNING = True

viewport_y = 0



grid = Grid(height=TILESH, width=TILESW)


def draw():
    screen.fill((80, 80, 80))
    for (x, y), tile in grid.items():
        img = tile.image
        if not WINNING:
            img = tile.type.value
        screen.blit(img, (x * TILE, HEIGHT - (y + 1) * TILE + viewport_y))

    if not WINNING:
        screen.draw.text(
            'Game Over',
            color=(180, 0, 0),
            fontsize=100,
            center=(WIDTH // 2, HEIGHT // 2)
        )


last_check_row = 0


def update(dt):
    global viewport_y, last_check_row, WINNING
    viewport_y += TILE * 0.25 * dt
    check_row = int(viewport_y // TILE)

    if check_row > last_check_row:
        if WINNING:
            last_check_row = check_row
            for x in range(TILESW):
                t = grid[x, check_row]
                if t.is_dangerous():
                    game_over()
                    break
        grid.next_row()


def game_over():
    global WINNING
    WINNING = False
    clock.schedule_unique(restart, 4)


def restart():
    global WINNING, viewport_y
    WINNING = True
    viewport_y = 0
    generate_grid()


def on_mouse_down(pos, button):
    x, y = pos
    tx = x // TILE
    ty = int(HEIGHT - y + viewport_y) // TILE
    print(f"Button {button} pressed at {(tx, ty)}")
    current = grid[tx, ty]
    if button == mouse.LEFT:
        current.on_uncover()
    elif button == mouse.RIGHT:
        current.on_flag()
