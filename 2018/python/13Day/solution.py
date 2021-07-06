import numpy as np
from itertools import count


class Carret():
  __carret_id = count(0)

  SHIFTS = {
    'up': np.array([-1, 0]),
    'down': np.array([1, 0]),
    'left': np.array([0, -1]),
    'right': np.array([0, 1])
  }

  MOVEMENTS = {
    # (route_part, direction): movement
    ('-', 'right'): 'right',
    ('-', 'left'): 'left',
    ('|', 'up'): 'up',
    ('|', 'down'): 'down',
    ('/', 'up'): 'right',
    ('/', 'left'): 'down',
    ('/', 'down'): 'left',
    ('/', 'right'): 'up',
    ('\\', 'right'): 'down',
    ('\\', 'up'): 'left',
    ('\\', 'down'): 'right',
    ('\\', 'left'): 'up',
    ('+', 'up'): 'up',
    ('+', 'left'): 'left',
    ('+', 'right'): 'right',
    ('+', 'down'): 'down',
  }

  def __init__(self, position, direction):
    self.id = next(self.__carret_id)
    self.position = position
    self.direction = direction
    self.intersection_move_id = 0
    self.map = None
    self.route_part = None
    self.destroyed = False

  def set_map(self, input_map):
    self.map = input_map
    self.route_part = self.map[self.position[0], self.position[1]]

  def get_intersection_movement_direction(self):
    # intersection movements order [left, stright, right]
    if self.route_part == '+':
      if self.intersection_move_id == 0:
        if self.direction == 'up':
          return 'left'
        elif self.direction == 'left':
          return 'down'
        elif self.direction == 'right':
          return 'up'
        elif self.direction == 'down':
          return 'right'
      elif self.intersection_move_id == 2:
        if self.direction == 'up':
          return 'right'
        elif self.direction == 'left':
          return 'up'
        elif self.direction == 'right':
          return 'down'
        elif self.direction == 'down':
          return 'left'
      else:
        return self.direction

  def get_next_intersection_move_id(self):
    return int((self.intersection_move_id + 1) % 3)

  def move(self):
    if self.route_part == '+':
      self.direction = self.get_intersection_movement_direction()
      self.intersection_move_id = self.get_next_intersection_move_id()
    else:
      self.direction = self.MOVEMENTS[(self.route_part, self.direction)]
    self.position += self.SHIFTS[self.direction]
    self.route_part = self.map[self.position[0], self.position[1]]


def extract_carrets(input_map):
  INIT_CARRET_DIRECTION = {
    '<': 'left',
    '>': 'right',
    '^': 'up',
    'v': 'down'
  }
  carrets = []
  for i in range(input_map.shape[0]):
    for j in range(input_map.shape[1]):
      char = input_map[i, j]
      if char in ['<', '>', '^', 'v']:
        carret = Carret(np.array([i, j]), INIT_CARRET_DIRECTION[char])
        carrets.append(carret)
  return carrets


def replacement_char(input_map:np.array, pos:tuple):
  i, j = pos
  top, left, right, bottom = '', '', '', ''
  if i >= 1:
    top = input_map[i-1, j].replace(' ', '')
  if j >= 1:
    left = input_map[i, j-1].replace(' ', '')
  if j < input_map.shape[1] - 1:
    right = input_map[i, j+1].replace(' ', '')
  if i < input_map.shape[0] - 1:
    bottom = input_map[i+1, j].replace(' ', '')

  if top in ['|', '/', '+', '\\'] and bottom in ['|', '/', '+', '\\'] and \
     left in ['-', '\\', '+', '/'] and right in ['-', '\\', '+', '/']:
    return '+'
  elif (top == '|' and left == '-') or (bottom == '|' and right == '-'):
    return '/'
  elif (top == '|' and right == '-') or (bottom == '|' and left == '-'):
    return '/'
  elif (left in ['-', '\\', '+', '/']) and (right in ['-', '/', '+', '\\']):
    return '-'
  elif (top in ['|', '/', '+', '\\']) and (bottom in ['|', '/', '+', '\\']):
    return '|'


def collided_with(carret, carrets):
  other_carrets = [c for c in carrets
                    if (not c.destroyed) and (c.id != carret.id)]
  for c in other_carrets:
    if (c.position[0] == carret.position[0]) and (c.position[1] == carret.position[1]):
      return c
  return None


def read_map(filename):
  input_map = None
  with open(filename, 'r') as file:
    for line in file:
      line = line.replace('\n', '')
      if len(line) == 0:
        continue
      if input_map is None:
        input_map = np.full((1, len(line)), ' ')
      input_map = np.vstack((input_map, list(line)))
    input_map = input_map[1:, :]
  return input_map


def restore_map(input_map, positions):
  print('Restoring map....')
  for i, j in positions:
    top, left, right, bottom = ' ', ' ', ' ', ' '
    if i >= 1:
      top = input_map[i-1, j]
    if j >= 1:
      left = input_map[i, j-1]
    if j < input_map.shape[1] - 1:
      right = input_map[i, j+1]
    if i < input_map.shape[0] - 1:
      bottom = input_map[i+1, j]
    input_map[i, j] = replacement_char(input_map, (i, j))
    print(f'Nearest positions (top, left, right, bottom): {top}, {left}, {right}, {bottom}. Replacement (center): {input_map[i, j]}')
  return input_map


def sort_carrets(carrets):
  carrets = sorted(carrets, key=lambda carret: carret.position[1])
  return sorted(carrets, key=lambda carret: carret.position[0])


def run_simulation(carrets):
  answers = ''
  i = 0  # carret serial number to control epochs
  collided = []

  print(f'\nRun simulation....\nThere are total {len(carrets)} carrets')
  while True:
    if i == 0:
      carrets = sort_carrets(carrets)
      if len(carrets) - len(collided) == 1:
        break

    carret = carrets[i]
    if carret.id in collided:
      i = (i + 1) % len(carrets)
      continue

    # print(f'{carret.id}: from {carret.position}, {carret.direction}, {carret.route_part}')
    carret.move()
    # print(f'{carret.id}: to {carret.position}, {carret.direction}, {carret.route_part}')

    collided_carret = collided_with(carret, carrets)
    if collided_carret is not None:
      if collided == []:
        answers += f'\nFirst answer: First collision {carret.id} with {collided_carret.id} at {[carret.position[1], carret.position[0]]}\n'
      collided += [carret.id, collided_carret.id]
      carret.destroyed = True
      collided_carret.destroyed = True
      print(f'Collision {carret.id} with {collided_carret.id} at {carret.position}')

    i = (i + 1) % len(carrets)

  for carret in carrets:
    if not carret.destroyed:
      answers += f'Second answer: Last carret {carret.id} position {[carret.position[1], carret.position[0]]}\n'
      break
  print(answers)



if __name__ == '__main__':
  input_map = read_map('input')
  carrets = extract_carrets(input_map)
  input_map = restore_map(input_map, [c.position for c in carrets])
  for carret in carrets:
    carret.set_map(input_map)
  run_simulation(carrets)
