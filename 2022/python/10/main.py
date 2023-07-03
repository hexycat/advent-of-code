"""Day 10: https://adventofcode.com/2022/day/10"""
from typing import Callable

Instruction = tuple[str, int]  # (operation, value)
Operation = Callable[[int, int], int]  # (state, value) -> new_state

OPERATIONS: dict[str, Operation] = {
    "noop": lambda x, v: x,
    "addx": lambda x, v: x + v,
}
OPERATIONS_EXECUTION_LENGTH = {
    "noop": 1,
    "addx": 2,
}

INITIAL_REGISTER_VALUE = 1
SPRITE_WIDTH = 3
SPRITE_SHOULDER = int(SPRITE_WIDTH // 2)
SCREEN_WIDTH = 40
SCREEN_HEIGHT = 6
EMPTY_PIXEL_CHAR = "."
NOT_EMPTY_PIXEL_CHAR = "#"


def load_input(filepath: str) -> list[Instruction]:
    """Loads instructions from file and return them as list of tuples
    (operation, value)"""
    instructions = []
    with open(file=filepath, mode="r", encoding="utf-8") as file:
        for row in file.readlines():
            splits = row.strip().split()
            if len(splits) == 1:
                instructions.append((splits[0], 0))
                continue
            instructions.append((splits[0], int(splits[1])))
    return instructions


def execute_instructions(
    instructions: list[Instruction], measure_points: tuple[int] = tuple()
) -> list[int]:
    """Execute instructions and return signal strength measured at measure points"""
    if not measure_points:
        return []
    measure_points_set = set(measure_points)
    register_state = INITIAL_REGISTER_VALUE
    signal_strength = []
    cycle = 0
    for op, val in instructions:
        for op_time in range(OPERATIONS_EXECUTION_LENGTH[op]):
            if op_time == OPERATIONS_EXECUTION_LENGTH[op] - 1:
                register_state = OPERATIONS[op](register_state, val)
            cycle += 1
            if cycle in measure_points_set:
                signal_strength.append(register_state * cycle)
    return signal_strength


def part_one(instructions: list[Instruction]) -> int:
    """Calculate sum of CPU signal strength at 20th, 60th, 100th, 140th,
    180th, and 220th cycles"""
    measure_points = tuple(range(20, 221, 40))
    register_states = execute_instructions(instructions, measure_points)
    return sum(register_states)


def initialize_screen(height: int, width: int) -> list[list[str]]:
    """Initilize empty screen of size [height x width]"""
    return [[EMPTY_PIXEL_CHAR for col in range(width)] for row in range(height)]


def print_screen(screen: list[list[str]]) -> None:
    """Print screen in easy to read format"""
    for row in range(len(screen)):
        print("".join(screen[row]))


def draw(instructions: list[Instruction], screen: list[list[str]]) -> list[list[str]]:
    """Draws image on the screen by executing instructions"""
    sprite_center = INITIAL_REGISTER_VALUE
    instruction_id = 0
    op_time = 1
    for cycle in range(SCREEN_HEIGHT * SCREEN_WIDTH):
        row, col = (int(cycle // SCREEN_WIDTH), int(cycle % SCREEN_WIDTH))
        op, val = instructions[instruction_id]
        if sprite_center - SPRITE_SHOULDER <= col <= sprite_center + SPRITE_SHOULDER:
            screen[row][col] = NOT_EMPTY_PIXEL_CHAR
        if op_time == OPERATIONS_EXECUTION_LENGTH[op]:
            sprite_center = OPERATIONS[op](sprite_center, val)
            instruction_id += 1
            op_time = 1
            continue
        op_time += 1
    return screen


def part_two(instructions: list[Instruction]) -> None:
    """Prints screen state after instructions execution"""
    screen = initialize_screen(SCREEN_HEIGHT, SCREEN_WIDTH)
    screen = draw(instructions, screen)
    print_screen(screen)


if __name__ == "__main__":
    instructions = load_input("input")
    print(f"Part one: Sum of register states: {part_one(instructions)}")
    print("Part two: Screen state:")
    part_two(instructions)
