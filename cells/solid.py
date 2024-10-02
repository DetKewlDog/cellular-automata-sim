from .cell import Cell, CellUpdate
from random import random

class Solid(Cell):
  density: float = 0
  
  def update(self, neighbors: dict[tuple[int, int], Cell | None]) -> list[CellUpdate | None]:
    return [None]