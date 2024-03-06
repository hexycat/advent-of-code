from typing import Iterator


def load_input(path: str) -> list[str]:
    """Loads engine schematic from input file."""
    schematic: list[str] = []
    with open(path, "r") as file:
        for line in file.readlines():
            schematic.append(line.strip())
    return schematic


def extract_numbers_positions(string: str) -> Iterator[tuple[int, int]]:
    """Generator that returns start and end positions of the numbers in row."""
    start: int = 0
    end: int = start + 1

    while start < len(string):
        if not string[start].isdigit():
            start += 1
            continue

        end = start + 1
        while end < len(string) and string[end].isdigit():
            end += 1
        yield start, end
        start = end + 1


def has_symbol_around(schematic: list[str], ln: int, start: int, end: int) -> bool:
    """Checks for symbols around the number position.

    Dot is not considered as symbol."""

    left = max(start - 1, 0)
    right = min(end + 1, len(schematic[0]))
    up = max(ln - 1, 0)
    down = min(ln + 2, len(schematic))

    for ln in range(up, down):
        for idx in range(left, right):
            char = schematic[ln][idx]
            if not char.isdigit() and char != ".":
                return True
    return False


def part_one(schematic: list[str]) -> int:
    """Calculates sum of engine parts in schematic.

    Engine part is a integer number that has at least one symbol around it."""

    sum: int = 0

    for ln, line in enumerate(schematic):
        for number_start, number_end in extract_numbers_positions(line):
            if not has_symbol_around(schematic, ln=ln, start=number_start, end=number_end):
                continue
            sum += int(line[number_start:number_end])
    return sum


def restore_gear_number(line: str, start: int) -> tuple[int, int]:
    """Returns start and end positions of the gear number in the line."""

    end = start
    for idx in range(start, len(line)):
        if not line[idx].isdigit():
            break
        end = idx

    for idx in range(start, -1, -1):
        if not line[idx].isdigit():
            break
        start = idx

    return start, end + 1


def get_gear_numbers(schematic: list[str], ln: int, idx: int) -> list[int]:
    """Finds and returns gear numbers around the position."""

    numbers: list[int] = []

    left = max(idx - 1, 0)
    right = min(idx + 2, len(schematic[0]))
    up = max(ln - 1, 0)
    down = min(ln + 2, len(schematic))

    for ln in range(up, down):
        end: int = left
        for idx in range(left, right):
            if idx < end or not schematic[ln][idx].isdigit():
                continue
            start, end = restore_gear_number(line=schematic[ln], start=idx)
            number = int(schematic[ln][start:end])
            numbers.append(number)

    return numbers


def possible_gears_positions_generator(schematic: list[str]) -> Iterator[tuple[int, int]]:
    """Generator that returns positions of the star symbol in schematic.

    Start symbol represents possible gear position."""

    for ln in range(len(schematic)):
        for idx in range(len(schematic[0])):
            if schematic[ln][idx] != "*":
                continue
            yield ln, idx


def part_two(schematic: list[str]) -> int:
    """Calculates sum of all gears ratios in the schematic.

    Gears ratio is multiplication of exactly two numbers adjacent to the gear (star symbols)."""

    sum: int = 0
    for ln, idx in possible_gears_positions_generator(schematic):
        gear_numbers = get_gear_numbers(schematic, ln=ln, idx=idx)
        if len(gear_numbers) < 2:
            continue
        sum += gear_numbers[0] * gear_numbers[1]
    return sum


if __name__ == "__main__":
    schematic = load_input("input")

    part_one_answer = part_one(schematic)
    print(f"Part one: Sum of engine parts: {part_one_answer}")

    part_two_answer = part_two(schematic)
    print(f"Part two: Sum of gears ratios: {part_two_answer}")
