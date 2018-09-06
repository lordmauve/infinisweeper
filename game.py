from enum import Enum
import random

from enum_types import State, TileTypes, types, Tile

TILE = 32

TILESW = 20
TILESH = 16

WIDTH = TILESW * TILE
HEIGHT = TILESH * TILE

WINNING = True

viewport_y = 0



LINES = None


def generate_grid():
    global LINES
    LINES = [
        [Tile() for _ in range(TILESW)]
        for _ in range(1000)
    ]

generate_grid()


def draw():
    screen.fill('red')
    for y, row in enumerate(LINES):
        for x, tile in enumerate(row):
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
    if check_row > last_check_row and WINNING:
        last_check_row = check_row
        for x in range(TILESW):
            t = LINES[check_row][x]
            if t.is_dangerous():
                game_over()
                break



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
    current = LINES[ty][tx]
    if button == mouse.LEFT:
        current.on_uncover()
    elif button == mouse.RIGHT:
        current.on_flag()

