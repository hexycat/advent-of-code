from problem1 import count_trees_on_road

if __name__ == '__main__':
  pos = (0, 0)
  slopes = [
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1)
  ]

  with open('input.txt', 'r') as file:
    area = [line.strip() for line in file]
    
  answer = 1
  for slope in slopes:
    answer *= count_trees_on_road(area, slope, pos)
  print(f'Answer: {answer}')