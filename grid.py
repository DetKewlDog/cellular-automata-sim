from cells.cell import Cell
from typing_extensions import TypeAlias
from copy import copy

Position: TypeAlias = tuple[int, int]
Neighbors: TypeAlias = dict[Position, Cell | None]
Color: TypeAlias = tuple[int, int, int]


class Grid:
  width: int
  height: int
  grid: list[list[Cell | None]]
  colors: list[list[Color]]
  
  def __init__(self, width: int, height: int):
    self.width = width
    self.height = height
    
    self.grid = [[None for x in range(self.width)] for y in range(self.height)]
    self.colors = []
    
  def is_in_bounds(self, pos: Position) -> bool:
    x, y = pos
    return x >= 0 and y >= 0 and x < self.width and y < self.height

  def get_cell(self, pos: Position) -> Cell | None:
    if not self.is_in_bounds(pos):
      return None
    
    x, y = pos
    return self.grid[y][x]

  def set_cell(self, cell: Cell, pos: Position) -> None:
    if not self.is_in_bounds(pos):
      return

    if self.get_cell(pos) and cell and cell.density > 1:
      return

    x, y = pos
    self.grid[y][x] = cell

  def get_neighbors(self, pos: Position) -> Neighbors:
    res: Neighbors = {}

    for x in range(-1, 2):
      for y in range(-1, 2):
        if x == 0 and y == 0:
          continue

        new_pos = (pos[0] + x, pos[1] + y)
        if not self.is_in_bounds(new_pos):
          continue

        res[(x, y)] = self.get_cell(new_pos)

    return res

  def update_cells(self) -> None:
    self.colors = [
      [
        cell.color if cell
        else (0, 0, 0)
        for cell in row
      ] for row in self.grid
    ]

    for row in self.grid:
      for cell in row:
        if cell:
          cell.updated = False

    for y in range(self.height - 1, 0, -1):
      for x in range(self.width):
        cell = self.grid[y][x]
        if not cell:
          self.colors[y][x] = (0, 0, 0)
          continue

        if cell.updated:
          continue


        neighbors = self.get_neighbors((x, y))

        if (0, -1) in neighbors and neighbors[(0, -1)] and neighbors[(0, -1)].density > cell.density and cell.density:
          temp = copy(cell)
          self.grid[y][x] = cell = copy(neighbors[(0, -1)])
          self.grid[y - 1][x] = neighbors[(0, -1)] = temp
          temp_col = self.colors[y][x]
          self.colors[y][x] = self.colors[y - 1][x]
          self.colors[y - 1][x] = temp_col

        updates = cell.update(neighbors)
        if cell:
          cell.updated = True

        for update in updates:
          if not update:
            continue

          dx, dy = update.offset

          if (update.destroy_self):
            self.grid[y][x] = None
            self.colors[y][x] = (0, 0, 0)

          self.grid[y + dy][x + dx] = update.new_cell
          self.colors[y + dy][x + dx] = update.new_cell.color if update.new_cell else (0, 0, 0)

          if update.new_cell:
            update.new_cell.updated = True

  def get_colors(self) -> list[list[Color]]:
    return self.colors

