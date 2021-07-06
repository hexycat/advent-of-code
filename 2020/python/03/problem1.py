from typing import Tuple, List

class Position():
  def __init__(self, 
               limits: Tuple[int, int] = (None, None), 
               coordinates: Tuple[int, int] = (0, 0)):
    self.coordinates = coordinates
    self.limits = limits

  def move(self, other) -> None:
    x = self.coordinates[0] + other.coordinates[0]
    y = self.coordinates[1] + other.coordinates[1]
    if isinstance(self.limits[0], int) and self.limits[0] > 0:
      x %= self.limits[0]
    if isinstance(self.limits[1], int) and self.limits[1] > 0:
      y %= self.limits[1]
    self.coordinates = (x, y)


def count_trees_on_road(area: List[List[str]], 
                        slope: Tuple[int, int], 
                        position: Tuple[int, int] = (0, 0)) -> int:
  trees = 0
  
  area_height = len(area)
  area_width = len(area[0])
  print(f'Area size: {area_height}, {area_width}')

  slope = Position(coordinates=slope)
  pos = Position(coordinates=position, limits=(None, area_width))

  while pos.coordinates[0] < area_height - 1:
    pos.move(slope)
    try:
      if area[pos.coordinates[0]][pos.coordinates[1]] == '#':
        trees += 1
    except:
      break
  print(f'Trees in total: {trees}')
  return trees

if __name__ == '__main__':
  slope = (1, 3)
  pos = (0, 0)

  with open('input.txt', 'r') as file:
    area = [line.strip() for line in file]

  total_trees = count_trees_on_road(area, slope, pos)