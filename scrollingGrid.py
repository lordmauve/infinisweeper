"""this program creates a scrolling matrix"""
from random import random

from enum_types import TileTypes, Tile, State


class Grid:
    # Number of rows ahead to generate. More rows reduces the chance that we
    # flood-fill back into view (creating an unexpected pop) when new rows are
    # generated.
    LOOKAHEAD = 5

    def __init__(self, height=16, width=20):
        self.width = width
        self.data = {}
        self.next_adj = set()

        self.miny = 0
        for r in range(height + self.LOOKAHEAD):
            # Low rows must have no bombs
            if r < height * 0.5:
                self.data[r] = self._gen_row(0.0)
                self.maxy = r
            else:
                self.push_row()
        self.reveal((0, self.miny))

    def push_row(self):
        """Create a new row."""
        mine_frac = 1.0 - 0.9 * 1.001 ** -self.maxy
        row = self._gen_row(mine_frac)
        self.maxy += 1
        self.data[self.maxy] = row
        self._calculate_row(self.maxy - 1)

        adj = [(x, self.maxy - 1) for x in self.next_adj]
        self.next_adj.clear()
        self._flood_uncover(adj)

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
            l = max(col - 1, 0)
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
        try:
            return self.data[y][x]
        except (KeyError, IndexError):
            raise KeyError("Invalid coordinate {!r}".format(pos)) from None

    def items(self):
        for rownum in range(self.miny, self.maxy + 1):
            row = self.data[rownum]
            for colnum, tile in enumerate(row):
                yield (colnum, rownum), tile

    def reveal(self, pos):
        """Uncover the tile at pos.

        Return the tile type uncovered.

        """
        self._flood_uncover({pos})

    def _flood_uncover(self, adj):
        adj = set(adj)
        visited = set()

        while adj:
            p = adj.pop()
            visited.add(p)
            x, y = p
            if not (0 <= x < self.width):
                continue
            if y == self.maxy:
                self.next_adj.add(x)
                continue
            elif y < self.miny:
                continue
            tile = self[p]
            tile.state = State.UNCOVERED
            if tile.type == TileTypes.BLANK:
                neighbours = {
                    (x - 1, y - 1),
                    (x, y - 1),
                    (x + 1, y - 1),
                    (x - 1, y),
                    (x + 1, y),
                    (x - 1, y + 1),
                    (x, y + 1),
                    (x + 1, y + 1),
                }
                adj.update(neighbours - visited)
