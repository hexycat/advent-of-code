import io

DIGITS_MAPPING: dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def extract_calibration_value_as_digits(line: str) -> int:
    """Extracts calibration value from the line taking into account only numeric symbols."""
    length = len(line)

    left_digit: int = 0
    for idx in range(length):
        if line[idx].isdigit():
            left_digit = int(line[idx])
            break

    right_digit: int = 0
    for idx in range(length - 1, -1, -1):
        if line[idx].isdigit():
            right_digit = int(line[idx])
            break

    return 10 * left_digit + right_digit


def part_one(file: io.TextIOWrapper) -> int:
    """Reads opened file and calculates sum of calibration values.

    Extraction of calibration values takes into account only numeric symbols.
    """
    sum: int = 0
    for line in file.readlines():
        sum += extract_calibration_value_as_digits(line.strip())
    return sum


def extract_calibration_value_as_digits_and_words(line: str) -> int:
    """Extracts calibration value from the line taking into account numeric symbols
    and word representation."""
    length = len(line)

    left_digit: int = 0
    for idx in range(length):
        if line[idx].isdigit():
            left_digit = int(line[idx])
            break
        if digit := DIGITS_MAPPING.get(line[idx : min(idx + 3, length)]):
            left_digit = digit
            break
        if digit := DIGITS_MAPPING.get(line[idx : min(idx + 4, length)]):
            left_digit = digit
            break
        if digit := DIGITS_MAPPING.get(line[idx : min(idx + 5, length)]):
            left_digit = digit
            break

    right_digit: int = 0
    for idx in range(length - 1, -1, -1):
        if line[idx].isdigit():
            right_digit = int(line[idx])
            break
        if digit := DIGITS_MAPPING.get(line[max(idx - 2, 0) : idx + 1]):
            right_digit = digit
            break
        if digit := DIGITS_MAPPING.get(line[max(idx - 3, 0) : idx + 1]):
            right_digit = digit
            break
        if digit := DIGITS_MAPPING.get(line[max(idx - 4, 0) : idx + 1]):
            right_digit = digit
            break

    return 10 * left_digit + right_digit


def part_two(file: io.TextIOWrapper) -> int:
    """Reads opened file and calculates sum of calibration values.

    Extraction of calibration values takes into account numeric symbols and word representations.
    """
    sum: int = 0
    for line in file.readlines():
        sum += extract_calibration_value_as_digits_and_words(line.strip())
    return sum


if __name__ == "__main__":
    with open("input", "r") as file:
        part_one_answer = part_one(file=file)
    print(f"Part one: Sum of calibration values presented as numeric symbols: {part_one_answer}")

    with open("input", "r") as file:
        part_two_answer = part_two(file=file)
    print(f"Part two: Sum of calibration values presented as numeric symbols and words: {part_two_answer}")
