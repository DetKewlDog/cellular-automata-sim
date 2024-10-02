import pygame, sys
from pygame.locals import *

from grid import Grid
from materials import *

def main():
  pygame.init()

  BLACK = (0, 0, 0)

  WIDTH  = 160
  HEIGHT = 90
  FPS = 60

  PIXEL_SIZE = 4

  drawing = False
  win = pygame.display.set_mode((WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE), 0, 32)
  screen = pygame.Surface((WIDTH, HEIGHT))
  pygame.display.set_caption("sim")

  grid = Grid(WIDTH, HEIGHT)

  clock = pygame.time.Clock()

  material: Cell = Wood

  is_deleting = False


  while True:
    clock.tick(FPS)

    grid.update_cells()

    screen.fill(BLACK)

    for y, row in enumerate(grid.get_colors()):
      for x, color in enumerate(row):
        screen.set_at((x, y), color)

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEMOTION:
        if drawing:
          pos = pygame.mouse.get_pos()
          pos = (pos[0] // PIXEL_SIZE, pos[1] // PIXEL_SIZE)
          size = 2
          for y in range(-size, size + 1):
            for x in range(-size, size + 1):
              cell = None if is_deleting else material()
              grid.set_cell(cell, (pos[0] + x, pos[1] + y))

      elif event.type == MOUSEBUTTONUP:
        drawing = False
      elif event.type == MOUSEBUTTONDOWN:
        drawing = True
        if event.button == 1: is_deleting = False
        if event.button == 3: is_deleting = True

      elif event.type == KEYDOWN:
        match (event.key):
          case pygame.K_1: material = Wood
          case pygame.K_2: material = Sand
          case pygame.K_3: material = Water
          case pygame.K_4: material = Smoke
          case pygame.K_5: material = Fire
          case pygame.K_6: material = Lava
          case pygame.K_7: material = Oil
          case pygame.K_8: material = Acid
          case pygame.K_9: material = Propane
          case _:          material = Wood

    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
    pygame.display.update()

if __name__ == "__main__":
  main()