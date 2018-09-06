from enum import Enum
import random


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
    def __init__(self, type=None):
        self.flagged = False
        self.state = State.COVERED
        self.type = type or random.choice(types)

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
