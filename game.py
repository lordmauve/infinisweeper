from enum import Enum
import random
TILE = 32

TILESW = 20
TILESH = 16

WIDTH = TILESW * TILE
HEIGHT = TILESH * TILE

WINNING = True

viewport_y = 0


class TileTypes(Enum):
    BLANK = 'blank'
    N1 = 'one'
    N2 = 'two'
    N3 = 'three'
    N4 = 'four'
    N5 = 'five'
    N6 = 'six'
    N7 = 'seven'
    N8 = 'eight'
    MINE = 'mine'


types = list(TileTypes)


class State(Enum):
    COVERED = 1
    UNCOVERED = 2
    FLAGGED = 3



class Tile:
    def __init__(self, state=None):
        self.flagged = False
        self.state = state or State.COVERED
        self.type = random.choice(types)

    @property
    def image(self):
        if self.state is State.COVERED:
            return 'cover'
        elif self.state is State.FLAGGED:
            return 'flag'
        else:
            return self.type.value

    def on_uncover(self):
        self.state = State.UNCOVERED

    def on_flag(self):
        if self.state is State.COVERED:
            self.state = State.FLAGGED
        elif self.state is State.FLAGGED:
            self.state = State.COVERED

    def is_dangerous(self):
        if (self.state is State.COVERED and self.type is TileTypes.MINE) or \
           (self.state is State.FLAGGED and self.type is not TileTypes.MINE):
            return True
        return False



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

