import numpy as np

with open('input', 'r') as file:
    coords = []
    for line in file:
        coords.append(line.replace('\n', '').split(', '))

coords = np.array(coords, dtype=int)


def manh(self, other):
    return np.abs(self - other).sum()


# part 1
def part1(coords):
    matrix = np.zeros(coords.max(axis=0), dtype=int)
    n = coords.shape[0]

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):

            point = np.array([i + 1, j + 1], dtype=int)
            distances = np.zeros(n)
            for k in range(1, n + 1):
                coord = coords[k - 1, :]
                if (coord == point).all():
                    matrix[i, j] = k
                    break
                distances[k - 1] = manh(coord, point)
            else:
                min_ids = np.where(distances == distances.min())[0]
                if min_ids.size == 1:
                    matrix[i, j] = min_ids[0] + 1

    matrix_borders = np.concatenate((matrix[0, :],
                                     matrix[-1, :],
                                     matrix[:, 0],
                                     matrix[:, -1]), axis=None)
    exclude = np.unique(matrix_borders)
    unique, counts = np.unique(matrix, return_counts=True)
    index = []
    if 0 not in exclude:
        index.append(0)
    for excluded_coord_id in exclude:
        index += list(np.where(unique == excluded_coord_id)[0])
    unique = np.delete(unique, index)
    counts = np.delete(counts, index)

    return counts.max()


# part 2
def part2(coords):
    max_distance = 10000
    matrix = np.zeros(coords.max(axis=0), dtype=int)
    n = coords.shape[0]

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):

            point = np.array([i + 1, j + 1], dtype=int)
            distances = np.zeros(n)
            for k in range(1, n + 1):
                coord = coords[k - 1, :]
                distances[k - 1] = manh(coord, point)

            dist = distances.sum()
            if dist < max_distance:
                matrix[i, j] = 1

    return matrix.sum()

ans1 = part1(coords)
ans2 = part2(coords)

print('Part1: {}'.format(ans1))
print('Part2: {}'.format(ans2))
