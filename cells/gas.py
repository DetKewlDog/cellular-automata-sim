from .cell import Cell, CellUpdate
from random import random

class Gas(Cell):
  def __init__(self):
    super().__init__()
    self.time = 0

  def update(self, neighbors: dict[tuple[int, int], Cell | None]) -> list[CellUpdate | None]:
    self.time += 0.0001

    if random() < self.time * self.time:
      return [CellUpdate(None, (0, 0))]

    if all(list(neighbors.values())):
      return [None]

    is_valid = lambda pos: pos in neighbors and neighbors[pos] == None

    if is_valid((0, -1)):
      return [CellUpdate(self, (0, -1))]
    
    x_positions = [1, -1] if self.dir > 0 else [-1, 1]
    y_positions = [-1, 0]

    for y in y_positions:
      for x in x_positions:
        coord = (x, y)
        if is_valid(coord):
          self.dir = x
          return [CellUpdate(self, coord)]

        
    return [None]