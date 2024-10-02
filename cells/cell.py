
from enum import Enum
from dataclasses import dataclass

class Cell:
  pass

@dataclass(slots=True)
class CellUpdate:
  new_cell: Cell | None
  offset: tuple[int, int]
  destroy_self: bool = True

  def __post_init__(self):
    if self.new_cell:
      self.new_cell.updated = True

class Cell:
  __slots__ = ['dir', 'updated', 'health']

  color: tuple[int, int, int] = (0, 0, 0)
  density: float = 0
  can_burn: bool = False
  can_evaporate: bool = False

  def __init__(self):
    self.dir = 0
    self.updated = False

  def update(self, neighbors: dict[tuple[int, int], Cell | None]) -> list[CellUpdate | None]:
    return [None]
