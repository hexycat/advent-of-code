import numpy as np
import time

with open('input', 'r') as file:
    serial_number = int(file.readline().replace('\n', ''))

def power_level(X, Y, serial_number):
    rack_ID = X + 10
    power = int((rack_ID * Y + serial_number) * rack_ID / 100)
    power = int(str(power)[-1])
    return power - 5

def create_power_grid(grid_shape):
    grid = np.zeros(grid_shape)
    for x in range(1, grid_shape[0] + 1):
        for y in range(1, grid_shape[1] + 1):
            grid[x - 1, y - 1] = power_level(x, y, serial_number)
    return grid

def create_blocks_power_grid(grid, filer_shape):
    shape = (grid.shape[0] - filter_shape[0] + 1,
             grid.shape[1] - filter_shape[1] + 1)
    blocks_grid = np.zeros(shape)
    for x in range(shape[0]):
        for y in range(shape[1]):
            blocks_grid[x, y] = grid[x:(x + filter_shape[0]),
                                     y:(y + filter_shape[1])].sum()
    return blocks_grid

def find_max(blocks_grid):
    max_power = int(blocks_grid.max())
    index = np.unravel_index(blocks_grid.argmax(), blocks_grid.shape)
    return (index[0] + 1, index[1] + 1), max_power


# test cases:
# serial_number = 18 # Part 1: 33,45 with power 29; Part 2: 90,269,16 with power 113
# serial_number = 42 # Part 1: 21,61 with power 30; Part 2: 232,251,12 with power 119

dim_size = 300
power_grid_shape = (dim_size, dim_size)
power_grid = create_power_grid(power_grid_shape)


# Part 1
start_part_1 = time.time()

filter_shape = (3, 3)
blocks_power_grid = create_blocks_power_grid(power_grid, filter_shape)
index, max_power = find_max(blocks_power_grid)

end_part_1 = time.time()
print(f'Part 1: {index} with power {max_power}')
print(f'Solve Part 1 in about {end_part_1 - start_part_1} seconds\n')


# Part 2
start_part_2 = time.time()

block_stats = tuple() # save answer here
absolute_max_power = 0 # max power among all filters
for filter_size in range(1, dim_size + 1):
    filter_shape = (filter_size, filter_size)
    blocks_power_grid = create_blocks_power_grid(power_grid, filter_shape)
    index, max_power = find_max(blocks_power_grid)
    if max_power > absolute_max_power:
        # modify index to satisfy answer format (add filter size)
        block_stats = index + (filter_size, )
        absolute_max_power = max_power

end_part_2 = time.time()
print(f'Part 2: {block_stats} with power {absolute_max_power}')
print(f'Solve Part 2 in about {end_part_2 - start_part_2} seconds')



