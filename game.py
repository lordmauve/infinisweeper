TILE = 32

TILESW = 20
TILESH = 16

WIDTH = TILESW * TILE
HEIGHT = TILESH * TILE


viewport_y = 0

LINES = [
    ['cover'] * TILESW
    for _ in range(1000)
]


def draw():
    screen.fill('red')
    for y, row in enumerate(LINES):
        for x, val in enumerate(row):
            screen.blit(val, (x * TILE, HEIGHT - (y + 1) * TILE + viewport_y))


def update(dt):
    global viewport_y
    viewport_y += TILE * 0.25 * dt


def on_mouse_down(pos, button):
    x, y = pos
    tx = x // TILE
    ty = int(HEIGHT - y + viewport_y) // TILE
    print(f"Button {button} pressed at {(tx, ty)}")
    LINES[ty][tx] = 'blank'

