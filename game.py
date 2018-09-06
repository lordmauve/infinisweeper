from enum import Enum
import random
TILE = 32

TILESW = 20
TILESH = 16

WIDTH = TILESW * TILE
HEIGHT = TILESH * TILE


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


LINES = [
    [Tile() for _ in range(TILESW)]
    for _ in range(1000)
]


def draw():
    screen.fill('red')
    for y, row in enumerate(LINES):
        for x, tile in enumerate(row):
            screen.blit(tile.image, (x * TILE, HEIGHT - (y + 1) * TILE + viewport_y))


def update(dt):
    global viewport_y
    viewport_y += TILE * 0.25 * dt


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

