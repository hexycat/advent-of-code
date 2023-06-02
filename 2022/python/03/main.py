"""Day 3: https://adventofcode.com/2022/day/3"""

import string

PRIORITY = {letter: i + 1 for i, letter in enumerate(string.ascii_letters)}


def load_input(filepath: str) -> list:
    """Read input data and return it as list of strings"""
    lines = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            lines.append(line.strip())
    return lines


def part_one(rucksacks: list) -> int:
    """Calculates sum of priority of misplaced items"""
    summ = 0
    for rucksack in rucksacks:
        split_point = len(rucksack) // 2
        first = set(rucksack[:split_point])
        second = set(rucksack[split_point:])
        misplaced_item = list(first.intersection(second))[0]
        summ += PRIORITY.get(misplaced_item, 0)
    return summ


def part_two(rucksacks: list) -> int:
    """Searches common item (badge) within group of 3 and
    calculates sum of priority for all such items"""
    summ = 0
    for i in range(0, len(rucksacks), 3):
        first_group = set(rucksacks[i])
        second_group = set(rucksacks[i + 1])
        third_group = set(rucksacks[i + 2])
        badge = first_group.intersection(second_group).intersection(third_group)
        badge = list(badge)[0]  # extract item id from set
        summ += PRIORITY.get(badge, 0)
    return summ


if __name__ == "__main__":
    backpacks = load_input("input")
    print(f"Part one: Sum of priority of misplaced items: {part_one(backpacks)}")
    print(f"Part two: Sum of priority of badges: {part_two(backpacks)}")
