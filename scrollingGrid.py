"""this program creates a scrolling matrix"""


from collections import deque
from random import random

from enum_types import TileTypes, Tile


class Grid:
    def __init__(self, height=16, width=20):
        self.width = width
        self.data = deque()
        for _ in range(height):
            self.new_row()

    def new_row(self):
        row = []
        for i in range(self.width):
            if random() < 0.1:
                row.append(Tile(TileTypes.MINE))
            else:
                row.append(Tile(TileTypes.EMPTY))
        self.data.append(row)

    def click(self,x,y):
        cell = self.data[y][x]
        if cell.type is TileTypes.MINE:
            raise ValueError('You Died')
