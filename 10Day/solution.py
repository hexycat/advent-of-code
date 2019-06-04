import numpy as np

with open('input', 'r') as file:
    positions = []
    velocities = []
    for line in file:
        parts = line.replace('\n', '').replace(' ', '').split('>')
        position = parts[0].split('=<')[1].split(',')
        velocity = parts[1].split('=<')[1].split(',')
        velocities.append(velocity)
        positions.append(position)
    positions = np.array(positions, dtype=int)
    velocities = np.array(velocities, dtype=int)


def position_limits(positions):
    x_min = positions[:, 0].min()
    x_max = positions[:, 0].max()

    y_min = positions[:, 1].min()
    y_max = positions[:, 1].max()
    return x_min, x_max, y_min, y_max

def deltas(x_min, x_max, y_min, y_max):
    return x_max - x_min, y_max - y_min

def positions_differences(positions):
    x_min, x_max, y_min, y_max = position_limits(positions)
    x_delta, y_delta = deltas(x_min, x_max, y_min, y_max)
    return x_delta, y_delta

def rewind(positions, velocities, total_seconds, time_delta=1):
    positions += time_delta * velocities
    total_seconds += time_delta * 1
    return positions, total_seconds

def prepare_positions(positions):
    x_min, x_max, y_min, y_max = position_limits(positions)
    # change points coords limits to values in range [0, max]
    if x_min < 0:
        positions[:, 0] += positions[:, 0].min()
    else:
        positions[:, 0] -= positions[:, 0].min()
    if y_min < 0:
        positions[:, 1] += positions[:, 1].min()
    else:
        positions[:, 1] -= positions[:, 1].min()
    return positions

def reflect_on_sky(positions):
    x_min, x_max, y_min, y_max = position_limits(positions)
    sky = np.full((x_max + 1, y_max + 1), ' ')
    for point in range(positions.shape[0]):
        x, y = positions[point, :]
        sky[x, y] = '#'
    return sky


total_seconds = 0
x_delta_old, y_delta_old = positions_differences(positions) # init positions differences

positions, total_seconds = rewind(positions, velocities, total_seconds) # make step further by 1 sec
x_delta, y_delta = positions_differences(positions) # new positions differences

while (x_delta < x_delta_old) and (y_delta < y_delta_old):
    x_delta_old = x_delta
    y_delta_old = y_delta

    positions, total_seconds = rewind(positions, velocities, total_seconds)
    x_delta, y_delta = positions_differences(positions)

# make one step backward because while loop makes extra step further
positions, total_seconds = rewind(positions, velocities, total_seconds, time_delta=-1)
# prepare points positions to reflect on the sky
positions = prepare_positions(positions)
sky = reflect_on_sky(positions)

# Look to the sky and see
print('Message in the sky:')
print(np.flipud(sky)) # flip matrix along axis 0 due to flipped letters; part 1 answer
print('\nTotal seconds: {}'.format(total_seconds)) # part 2 answer
