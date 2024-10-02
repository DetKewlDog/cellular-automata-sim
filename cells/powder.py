from .cell import Cell, CellUpdate

class Powder(Cell):
  def update(self, neighbors: dict[tuple[int, int], Cell | None]) -> list[CellUpdate | None]:
    if all(list(neighbors.values())):
      return [None]

    is_valid = lambda pos: pos in neighbors and neighbors[pos] == None

    if is_valid((0, 1)):
      return [CellUpdate(self, (0, 1))]
    
    x_positions = [1, -1] if self.dir > 0 else [-1, 1]

    for x in x_positions:
      coord = (x, 1)
      if is_valid(coord):
        self.dir = x
        return [CellUpdate(self, coord)]

    self.dir = 0
    return [None]