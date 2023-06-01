"""Day 1: Calorie Counting | https://adventofcode.com/2022/day/1"""

import io


def part_one(file: io.TextIOWrapper) -> int:
    """Count maximum calories carried by one elf"""
    max_calories = 0
    elf_calories = 0
    for line in file:
        line = line.strip()
        if line:  # add calories to current elf
            elf_calories += int(line)
            continue
        # check whether it is maximum value
        max_calories = max(max_calories, elf_calories)
        elf_calories = 0  # switch to the next elf
    # take into account the last elf
    return max(max_calories, elf_calories)


def part_two(file: io.TextIOWrapper) -> int:
    """Count total calories carried by top 3 elves"""
    carriers = []
    elf_calories = 0
    for line in file:
        line = line.strip()
        if line:  # add calories to current elf
            elf_calories += int(line)
            continue
        carriers.append(elf_calories)  # save number of calories carried by elf
        elf_calories = 0  # switch to the next elf
    # take into account the last elf
    if elf_calories:
        carriers.append(elf_calories)
    carriers.sort(reverse=True)
    return sum(carriers[:3])



if __name__ == "__main__":
    with open("input", "r", encoding="utf-8") as file:
        print(f"Part one (max calories carried by single elf): {part_one(file)}")
    with open("input", "r", encoding="utf-8") as file:
        print(f"Part two (total calories carried by top 3 elves): {part_two(file)}")
