"""Day 8: https://adventofcode.com/2022/day/8"""


def load_input(filepath: str) -> list:
    """Loads trees grid from text file as list[list[int]]"""
    trees_grid = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.strip()
            grid_row = [int(number) for number in line]
            trees_grid.append(grid_row)
    return trees_grid


def is_visible(trees_grid: list, tree_row: int, tree_col: int) -> bool:
    """Checks visibility of the tree from 4 directions.
    Tree is visible if all trees at least in one direction are smaller"""
    tree = trees_grid[tree_row][tree_col]
    # Visible from left
    visible = True
    for j in range(tree_col):
        if trees_grid[tree_row][j] >= tree:
            visible = False
            break
    if visible:
        return True
    # Visible from right
    visible = True
    for j in range(tree_col + 1, len(trees_grid[0])):
        if trees_grid[tree_row][j] >= tree:
            visible = False
            break
    if visible:
        return True
    # Visible from top
    visible = True
    for i in range(tree_row):
        if trees_grid[i][tree_col] >= tree:
            visible = False
            break
    if visible:
        return True
    # Visible from bottom
    visible = True
    for i in range(tree_row + 1, len(trees_grid)):
        if trees_grid[i][tree_col] >= tree:
            visible = False
            break
    if visible:
        return True
    return False


def part_one(trees_grid: list) -> int:
    """Counts number of visible trees on the grid"""
    nrows = len(trees_grid)
    ncols = len(trees_grid[0])
    visible = 2 * (nrows + ncols - 2)
    for i in range(1, nrows - 1):
        for j in range(1, ncols - 1):
            if is_visible(trees_grid=trees_grid, tree_row=i, tree_col=j):
                visible += 1
    return visible


def get_scenic_score(trees_grid: list, tree_row: int, tree_col: int) -> int:
    """Calculates scenic score for the tree with given coordinates.
    Score is calculated as multiplication of number of visible trees from given
    position in 4 directions"""
    scenic_score = 1
    tree = trees_grid[tree_row][tree_col]
    # N trees visible to the left
    n_visible = 0
    for j in range(tree_col - 1, -1, -1):
        if trees_grid[tree_row][j] < tree:
            n_visible += 1
            continue
        if trees_grid[tree_row][j] >= tree:
            n_visible += 1
            break
    scenic_score *= n_visible
    # N trees visible to the right
    n_visible = 0
    for j in range(tree_col + 1, len(trees_grid[0])):
        if trees_grid[tree_row][j] < tree:
            n_visible += 1
            continue
        if trees_grid[tree_row][j] >= tree:
            n_visible += 1
            break
    scenic_score *= n_visible
    # N trees visible to the top
    n_visible = 0
    for i in range(tree_row - 1, -1, -1):
        if trees_grid[i][tree_col] < tree:
            n_visible += 1
            continue
        if trees_grid[i][tree_col] >= tree:
            n_visible += 1
            break
    scenic_score *= n_visible
    # N trees visible to the bottom
    n_visible = 0
    for i in range(tree_row + 1, len(trees_grid)):
        if trees_grid[i][tree_col] < tree:
            n_visible += 1
            continue
        if trees_grid[i][tree_col] >= tree:
            n_visible += 1
            break
    scenic_score *= n_visible
    return scenic_score


def part_two(trees_grid: list) -> int:
    """Calculates highest scenic score among all trees on the grid"""
    max_score = 0
    for i in range(1, len(trees_grid) - 1):
        for j in range(1, len(trees_grid[0]) - 1):
            score = get_scenic_score(trees_grid, tree_row=i, tree_col=j)
            max_score = max(score, max_score)
    return max_score


if __name__ == "__main__":
    grid = load_input("input")
    print(f"Part one: Number of visible trees: {part_one(grid)}")
    print(f"Part two: Highest score among all trees: {part_two(grid)}")
