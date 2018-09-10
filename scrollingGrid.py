"""this program creates a scrolling matrix"""
from random import random

from enum_types import TileTypes, Tile


class Grid:
    def __init__(self, height=16, width=20):
        self.width = width
        self.data = {}

        self.miny = -1
        for r in range(-1, height + 1):
            # Low rows must have no bombs
            if r < height * 0.5:
                self.data[r] = self._gen_row(0.0)
                self.maxy = r
            else:
                self.push_row()


    def push_row(self):
        """Create a new row."""
        mine_frac = min(1, self.maxy / 500) ** 0.5
        row = self._gen_row(mine_frac)
        self.maxy += 1
        self.data[self.maxy] = row
        self._calculate_row(self.maxy - 1)

    def _gen_row(self, mine_frac):
        row = []
        for i in range(self.width):
            if random() < mine_frac:
                row.append(Tile(TileTypes.MINE))
            else:
                row.append(Tile(TileTypes.BLANK))
        return row

    def _calculate_row(self, row_num):
        """Calculate numbers for row row_num."""
        prev_row = self.data[row_num + 1]
        row = self.data[row_num]
        next_row = self.data[row_num - 1]
        for col, tile in enumerate(self.data[row_num]):
            if tile.type == TileTypes.MINE:
                continue
            l = col - 1
            r = col + 2
            neighbours = prev_row[l:r] + row[l:r:2] + next_row[l:r]
            value = sum(c.type is TileTypes.MINE for c in neighbours)
            if value != 0:
                row[col].type = getattr(TileTypes, 'N{}'.format(value))

    def pop_row(self):
        """Delete the bottommost row we are tracking."""
        del self.data[self.miny]
        self.miny += 1

    def next_row(self):
        """Move to the next row."""
        self.push_row()
        self.pop_row()

    def __getitem__(self, pos):
        x, y = pos
        return self.data[y][x]

    def items(self):
        for rownum in range(self.miny, self.maxy + 1):
            row = self.data[rownum]
            for colnum, tile in enumerate(row):
                yield (colnum, rownum), tile
