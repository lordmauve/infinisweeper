TILE = 32

TILESW = 20
TILESH = 16

WIDTH = TILESW * TILE
HEIGHT = TILESH * TILE


y = 0


def draw():
    screen.fill('red')
    for x in range(TILESW):
        for y in range(TILESH):
            screen.blit('blank', (x * TILE, y * TILE))


def update(dt):
    global y
    y += TILE * 0.25 * dt


def on_mouse_down(pos, button):

    x, y = pos
    tx = x // TILE
    ty = y // TILE
    print(f"Button {button} pressed at {(tx, ty)}")
