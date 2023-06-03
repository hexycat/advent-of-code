"""Day 4: https://adventofcode.com/2022/day/4"""


def load_input(filepath: str) -> list:
    """Read input data, split by "," and "-", return it as list[list[int]]"""
    assignment_pairs = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            first, second = line.strip().split(",")
            first = [int(number) for number in first.split("-")]
            second = [int(number) for number in second.split("-")]
            assignment_pairs.append([first, second])
    return assignment_pairs


def part_one(assignment_pairs: list) -> int:
    """Calculates number of fully intersected segments to clean"""
    total = 0
    for first, second in assignment_pairs:
        if (first[0] <= second[0] and first[1] >= second[1]) or (
            second[0] <= first[0] and second[1] >= first[1]
        ):
            total += 1
    return total


def part_two(assignment_pairs: list) -> int:
    """Calculates total number of overlapping segments to clean"""
    total = 0
    for first, second in assignment_pairs:
        if (first[0] <= second[0] and first[1] >= second[0]) or (
            second[0] <= first[0] and second[1] >= first[0]
        ):
            total += 1
    return total


if __name__ == "__main__":
    sections = load_input("input")
    print(f"Part one: Number of fully intersected segments: {part_one(sections)}")
    print(f"Part two: Number of overlapping segments: {part_two(sections)}")
