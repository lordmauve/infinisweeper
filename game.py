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


grid = None


def generate_grid():
    global grid
    grid = Grid(height=TILESH, width=TILESW)
    grid.last_check_row = grid.score = 0

generate_grid()


def draw():
    screen.fill((80, 80, 80))
    for (x, y), tile in grid.items():
        img = tile.image
        if not WINNING:
            img = tile.type.value
        screen.blit(img, (x * TILE, HEIGHT - (y + 1) * TILE + viewport_y))

    screen.draw.filled_rect(
        Rect(0, HEIGHT - TILE, WIDTH, 5),
        'red'
    )

    if not WINNING:
        screen.draw.text(
            'Game Over',
            color=(180, 0, 0),
            shadow=(0.5, 0.5),
            fontsize=100,
            center=(WIDTH // 2, HEIGHT // 2)
        )
    screen.draw.text(
        "Score: {}".format(grid.score),
        color='white',
        owidth=1,
        fontsize=40,
        topright=(WIDTH - 8, 2)
    )


def update(dt):
    global viewport_y, WINNING
    viewport_y += TILE * 0.25 * dt
    check_row = int(viewport_y // TILE)

    if check_row > grid.last_check_row:
        grid.last_check_row = check_row

        if WINNING:
            mistakes = 0
            for x in range(TILESW):
                t = grid[x, check_row]
                mistakes += t.reveal()
            if mistakes:
                game_over()
            else:
                grid.score += 1

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
    current = grid[tx, ty]
    if button == mouse.LEFT:
        current.on_uncover()
        if current.type in (TileTypes.MINE, TileTypes.RED):
            game_over()
        elif current.type is TileTypes.BLANK:
            type = grid.reveal((tx, ty))
    elif button == mouse.RIGHT:
        current.on_flag()
