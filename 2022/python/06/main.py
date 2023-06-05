"""Day 6: https://adventofcode.com/2022/day/6"""


def load_input(filepath: str) -> str:
    """Reads file and returns datastream buffer as a string"""
    with open(filepath, "r", encoding="utf-8") as file:
        buffer = file.readline()
    return buffer.strip()


def get_subroutine_start(subroutine: str) -> int:
    """Returns start index of new start-of-packet inside subroutine
    If index is 0, then entire subroutine is packet"""
    start = 0
    for i in range(len(subroutine) - 1, -1, -1):
        for j in range(i):
            if subroutine[i] == subroutine[j]:
                start = max(start, j + 1)
    return start


def part_one(buffer: str) -> int:
    """Returns number of processed elements at moment
    of occurrence start-of-packet"""
    SUBROUTINE_LENGTH = 4
    start = 0
    while True:
        subroutine = buffer[start : start + SUBROUTINE_LENGTH]
        step = get_subroutine_start(subroutine)
        if step == 0:
            return start + SUBROUTINE_LENGTH
        start += step


def part_two(buffer: str) -> int:
    """Returns number of processed elements at moment
    of occurrence start-of-message"""
    SUBROUTINE_LENGTH = 14
    start = 0
    while True:
        subroutine = buffer[start : start + SUBROUTINE_LENGTH]
        step = get_subroutine_start(subroutine)
        if step == 0:
            return start + SUBROUTINE_LENGTH
        start += step


if __name__ == "__main__":
    datastream = load_input("input")
    msg = "Part one: Number of processed elements at moment of start-of-packet: "
    print(msg + str(part_one(datastream)))
    msg = "Part two: Number of processed elements at moment of start-of-message: "
    print(msg + str(part_two(datastream)))
