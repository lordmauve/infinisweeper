"""this program creates a scrolling matric"""


from collections import deque
from random import random
from enum import Enum

class Cell(Enum):
    MINE = 1
    EMPTY = 2

class Grid:
    def __init__(self, width=20):
        self.width = width
        self.data = deque()

    def new_row(self):   
        row = []
        for i in range(self.width):
            if random() < 0.1:
                row.append(Cell.MINE)
            else
                row.append(Cell.EMPTY)
        self.data.append(row)
        
    def click(self,x,y):
        cell = self.data[y][x]
        if cell = Cell.MINE:
            raise ValueError('You Died')

    def neighbours(self,x,y):
        
        


               
        
        
        
        
