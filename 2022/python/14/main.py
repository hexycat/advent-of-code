"""Day 14: https://adventofcode.com/2022/day/14"""

Point = tuple[int, int]
RockLine = tuple[Point, Point]
Bbox = tuple[int, int, int, int]  # [row_min, col_min, row_max, col_max]

AIR_CHAR = "."
ROCK_CHAR = "#"
SAND_CHAR = "o"

SAND_START_POINT = (0, 500)


def load_input(filepath: str) -> list[RockLine]:
    """Read input file and return list of rock lines to be drawn"""
    rock_lines = []
    with open(filepath, mode="r", encoding="utf-8") as file:
        for line in file.readlines():
            coords = [point.split(",") for point in line.strip().split(" -> ")]
            rock_line = [(int(row), int(col)) for col, row in coords]
            rock_lines.append(rock_line)
    return rock_lines


def get_cave_bbox(rock_lines: list[RockLine], with_floor: bool = False) -> Bbox:
    """Calculate cave size [n_rows, n_cols] from rock lines coordinates"""
    row_min, row_max, col_min, col_max = float("inf"), 0, float("inf"), 0
    for rock_line in rock_lines:
        for row, col in rock_line:
            row_min = min(row, row_min)
            row_max = max(row, row_max)
            col_min = min(col, col_min)
            col_max = max(col, col_max)
    if with_floor:
        row_max += 2
    return 0, int(col_min), row_max, col_max


def create_cave2d(
    bbox: Bbox, rock_lines: list[RockLine], with_floor: bool = False
) -> list[list[str]]:
    """Reconstruct 2D cave from rock lines input"""
    row_min, col_min, row_max, col_max = bbox
    nrows = row_max - row_min + 1
    ncols = col_max - col_min + 1
    cave = [[AIR_CHAR for __ in range(ncols)] for _ in range(nrows)]
    for rock_line in rock_lines:
        for rock_id in range(1, len(rock_line)):
            start = rock_line[rock_id - 1]
            end = rock_line[rock_id]
            row_range = range(min(start[0], end[0]), max(start[0], end[0]) + 1)
            col_range = range(min(start[1], end[1]), max(start[1], end[1]) + 1)
            for row in row_range:
                for col in col_range:
                    cave[row - row_min][col - col_min] = ROCK_CHAR
    if with_floor:
        cave[-1] = [ROCK_CHAR for _ in range(ncols)]
    return cave


def simulate_falling_sand2d(cave: list[list[str]], start: Point) -> int:
    """Simulate falling sand in 2D cave, return number of sand units come to rest"""
    n_rest = 0
    point = start
    while True:
        if point[0] + 1 >= len(cave):
            break
        if cave[point[0] + 1][point[1]] == AIR_CHAR:
            point = (point[0] + 1, point[1])
            continue
        if point[1] - 1 < 0:
            break
        if cave[point[0] + 1][point[1] - 1] == AIR_CHAR:
            point = (point[0] + 1, point[1] - 1)
            continue
        if point[1] + 1 >= len(cave[0]):
            break
        if cave[point[0] + 1][point[1] + 1] == AIR_CHAR:
            point = (point[0] + 1, point[1] + 1)
            continue
        cave[point[0]][point[1]] = SAND_CHAR
        n_rest += 1
        point = start
    return n_rest


def save_cave2d(cave: list[list[str]], filepath: str) -> None:
    """Save 2D cave to the file"""
    with open(filepath, mode="w", encoding="utf-8") as file:
        cave_str = "\n".join([" ".join(row) for row in cave])
        file.writelines(cave_str)


def create_cave_set(rock_lines: list[RockLine]) -> set[Point]:
    """Reconstruct 2D cave by adding rock points to the set"""
    blocks = []
    for rock_line in rock_lines:
        for rock_id in range(1, len(rock_line)):
            start = rock_line[rock_id - 1]
            end = rock_line[rock_id]
            row_range = range(min(start[0], end[0]), max(start[0], end[0]) + 1)
            col_range = range(min(start[1], end[1]), max(start[1], end[1]) + 1)
            for row in row_range:
                for col in col_range:
                    blocks.append((row, col))
    return set(blocks)


def simulate_falling_sand_set(cave: set[Point], start: Point, floor_row: int) -> int:
    """Simulate falling sand in set cave with floor and return number of rest units
    before start is blocked"""
    nrest = 0
    point = start
    while True:
        if point[0] + 1 == floor_row:
            cave.add(point)
            nrest += 1
            point = start
            continue
        new_point = (point[0] + 1, point[1])
        if new_point not in cave:
            point = new_point
            continue
        new_point = (point[0] + 1, point[1] - 1)
        if new_point not in cave:
            point = new_point
            continue
        new_point = (point[0] + 1, point[1] + 1)
        if new_point not in cave:
            point = new_point
            continue
        cave.add(point)
        nrest += 1
        if point == start:
            break
        point = start
    return nrest


def part_one(rock_lines: list[RockLine]) -> int:
    """Calculate number of sand units come to rest before sand
    starts flowing into the abyss"""
    WITH_FLOOR = False
    bbox = get_cave_bbox(rock_lines, with_floor=WITH_FLOOR)
    cave = create_cave2d(bbox=bbox, rock_lines=rock_lines, with_floor=False)
    # save_cave2d(cave=cave, filepath="0.txt")
    sand_start = (SAND_START_POINT[0], SAND_START_POINT[1] - bbox[1])
    nrest = simulate_falling_sand2d(cave=cave, start=sand_start)
    # save_cave2d(cave=cave, filepath=f"{nrest}.txt")
    return nrest


def part_two(rock_lines: list[RockLine]) -> int:
    """Calculate number of sand units come to rest until source of the sand
    becomes blocked"""
    cave = create_cave_set(rock_lines=rock_lines)
    *_, row_max, _ = get_cave_bbox(rock_lines=rock_lines)
    return simulate_falling_sand_set(
        cave=cave, start=SAND_START_POINT, floor_row=row_max + 2
    )


if __name__ == "__main__":
    rock_lines = load_input("input")
    print(f"Part one: Number of sand units rest: {part_one(rock_lines=rock_lines)}")
    print(f"Part two: Number of sand units rest: {part_two(rock_lines=rock_lines)}")
