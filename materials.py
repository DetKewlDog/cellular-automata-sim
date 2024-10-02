from cells import *

from random import random, randrange

class Sand(Powder):
  color = (255, 200, 0)
  density = 3
  
  def __init__(self):
    super().__init__()
    self.color = (randrange(230, 256), randrange(190, 210), randrange(0, 20))

class Wood(Solid):
  color = (128, 64, 0)
  density = 0
  can_burn = True

  def __init__(self):
    super().__init__()
    self.color = (randrange(115, 125), randrange(55, 65), randrange(0, 10))

class Smoke(Gas):
  color = (64, 64, 64)
  density = 0.333
  
  def __init__(self):
    super().__init__()
    self.color = (randrange(50, 70), randrange(50, 70), randrange(50, 70))

class Ash(Powder):
  color = (64, 64, 64)
  density = 3
  can_burn = True

  def __init__(self):
    super().__init__()
    self.color = (randrange(50, 70), randrange(50, 70), randrange(50, 70))

class Water(Liquid):
  color = (64, 64, 255)
  density = 1
  can_evaporate = True

class Fire(Cell):
  color = (255, 128, 0)
  density = 0

  def __init__(self, on_air: bool = True):
    super().__init__()
    self.on_air = on_air
    self.color = (randrange(200, 256), randrange(100, 200), randrange(0, 20))

  def update(self, neighbors: dict[tuple[int, int], Cell | None]) -> list[CellUpdate | None]:
    will_spread = random() > 0.25

    if will_spread:
      results: list[CellUpdate | None] = []
      for pos, cell in neighbors.items():
        if not cell: continue

        if cell.can_burn:
          results.append(CellUpdate(Fire(False), pos))
        elif cell.can_evaporate:
          results.append(CellUpdate(Smoke(), pos))
      return results

    return [CellUpdate(Ash() if random() > 0.05 and not self.on_air else Smoke(), (0, 0))]

class Lava(Liquid):
  color = (255, 128, 0)
  density = 0

  def __init__(self):
    super().__init__()

  def update(self, neighbors: dict[tuple[int, int], Cell | None]) -> list[CellUpdate | None]:
    will_spread = random() > 0.25

    results: list[CellUpdate | None] = []
    if will_spread:
      for pos, cell in neighbors.items():
        if not cell: continue

        if cell.can_burn:
          results.append(CellUpdate(Fire(False), pos))
        elif cell.can_evaporate:
          results.append(CellUpdate(Smoke(), pos))

    return super().update(neighbors) + results

class Oil(Liquid):
  color = (48, 48, 100)
  density = 3
  can_burn = True

  def __init__(self):
    super().__init__()
    self.color = (randrange(40, 50), randrange(40, 50), randrange(95, 105))

class Acid(Liquid):
  color = (48, 150, 48)
  density = 3
  can_evaporate = True

  def __init__(self):
    super().__init__()
    self.color = (randrange(40, 50), randrange(145, 155), randrange(40, 50))

  def update(self, neighbors: dict[tuple[int, int], Cell | None]) -> list[CellUpdate | None]:
    results = []

    will_dissolve = random() < 0.05

    if will_dissolve:
      for pos, cell in neighbors.items():
        if (cell and
          cell.__class__ != self.__class__
        ):
          results += [CellUpdate(Acid(), pos), CellUpdate(Smoke(), (0, 0))]

    return super().update(neighbors) + results


class Propane(Gas):
  color = (110, 110, 255)
  density = 0.333
  can_burn = True

  def __init__(self):
    super().__init__()
    self.color = (randrange(105, 115), randrange(105, 115), randrange(245, 255))