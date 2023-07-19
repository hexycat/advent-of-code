"""Day 12: https://adventofcode.com/2022/day/12"""

import string

grid = list[list[str]]
coord = tuple[int, int]
path = list[coord]

START_CHAR = "S"
END_CHAR = "E"
CHAR2HEIGHT = {char: i for i, char in enumerate(string.ascii_lowercase)}


def load_input(filepath: str) -> grid:
    """Load input from file and return 2d elevation grid"""
    with open(filepath, "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def get_char_positions(elevation_map: grid, char: str = "a") -> list[coord]:
    """Return all (row, col) positions of the char"""
    positions = []
    for row in range(len(elevation_map)):
        for col in range(len(elevation_map[0])):
            if elevation_map[row][col] == char:
                positions.append((row, col))
    return positions


def extract_start_end(elevation_map: grid) -> tuple[coord, coord]:
    """Return coordinates of start and end points and replace them with
    corresponding elevation values"""
    start = get_char_positions(elevation_map, char=START_CHAR)[0]
    end = get_char_positions(elevation_map, char=END_CHAR)[0]
    elevation_map[start[0]][start[1]] = "a"
    elevation_map[end[0]][end[1]] = "z"
    return start, end


def find_path(
    elevation_map: grid,
    end_points: set[coord],
    paths: list[path],
    visited: set = set(),
    reversed_traversal: bool = False,
) -> path:
    paths_updated = []
    nrows, ncols = len(elevation_map), len(elevation_map[0])
    if not paths:
        return []
    for path in paths:
        row, col = path[-1]
        if (row, col) in end_points:
            return path
        height_current = CHAR2HEIGHT[elevation_map[row][col]]
        for delta_row, delta_col in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            row_new, col_new = row + delta_row, col + delta_col
            if row_new in {-1, nrows} or col_new in {-1, ncols}:
                continue
            if (row_new, col_new) in visited:
                continue
            height_new = CHAR2HEIGHT[elevation_map[row_new][col_new]]
            height_difference = height_new - height_current
            if reversed_traversal:
                height_difference = height_current - height_new
            if height_difference > 1:
                continue
            paths_updated.append(path + [(row_new, col_new)])
            visited.add((row_new, col_new))
    return find_path(
        elevation_map,
        end_points=end_points,
        paths=paths_updated,
        visited=visited,
        reversed_traversal=reversed_traversal,
    )


if __name__ == "__main__":
    elevation_map = load_input("input")
    start, end = extract_start_end(elevation_map)

    msg = "Part one: Minimal number of steps to take to travel from S to E:"
    shortest_path = find_path(
        elevation_map,
        end_points={end},
        paths=[[start]],
        visited={start},
        reversed_traversal=False,
    )
    print(f"{msg} {len(shortest_path) - 1}")

    msg = "Part two: Minimal number of steps to take to travel from E to a:"
    shortest_path = find_path(
        elevation_map,
        end_points=set(get_char_positions(elevation_map, char="a")),
        paths=[[end]],
        visited={end},
        reversed_traversal=True,
    )
    print(f"{msg} {len(shortest_path) - 1}")
