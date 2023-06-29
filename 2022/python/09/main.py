"""Day 9: https://adventofcode.com/2022/day/9"""

Instruction = tuple[str, int]  # [direction, n_steps]
Position = tuple[int, int]  # [row, col]

DIRECTIONS: dict[str, Position] = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
    "UR": (1, 1),
    "DR": (1, -1),
    "UL": (-1, 1),
    "DL": (-1, -1),
    "S": (0, 0),  # same position
}


def relative_position(knot: Position, other_knot: Position) -> str:
    """Returns other_knot's position relative to knot"""
    delta_col = knot[0] - other_knot[0]
    delta_row = knot[1] - other_knot[1]
    if delta_col == 0:
        if delta_row > 0:
            return "U"
        if delta_row < 0:
            return "D"
    if delta_row == 0:
        if delta_col > 0:
            return "R"
        if delta_col < 0:
            return "L"
    if delta_col > 0:
        if delta_row > 0:
            return "UR"
        if delta_row < 0:
            return "DR"
    if delta_col < 0:
        if delta_row > 0:
            return "UL"
        if delta_row < 0:
            return "DL"
    return "S"


def move(knot: Position, direction: str) -> Position:
    """Moves knot in direction"""
    delta = DIRECTIONS.get(direction, (0, 0))
    return (knot[0] + delta[0], knot[1] + delta[1])


def load_input(filepath: str) -> list[Instruction]:
    """Loads instructions from file and return them as list of tuples
    (direction, n_steps)"""
    instructions = []
    with open(file=filepath, mode="r", encoding="utf-8") as file:
        for row in file.readlines():
            direction, steps = row.strip().split()
            instructions.append((direction, int(steps)))
    return instructions


def should_move_knot(knot: Position, other_knot: Position) -> bool:
    """Checks whether other_knot should be moved towards knot or not"""
    delta_x = abs(knot[0] - other_knot[0])
    delta_y = abs(knot[1] - other_knot[1])
    return delta_x >= 2 or delta_y >= 2


def part_one(instructions: list[Instruction]) -> int:
    """Returns numbers of unique cells visited by bridge's tail"""
    start = (0, 0)
    unqiue_tail_cells: set[Position] = {start}
    head = start
    tail = start
    for head_direction, n_steps in instructions:
        for _ in range(n_steps):
            head = move(head, head_direction)
            if should_move_knot(head, tail):
                tail_direction = relative_position(head, tail)
                tail = move(tail, tail_direction)
                unqiue_tail_cells.add(tail)
    return len(unqiue_tail_cells)


def part_two(instructions: list[Instruction], bridge_length: int = 10) -> int:
    """Returns numbers of unique cells visited by bridge's tail.
    Length of the bridge might differ"""
    HEAD_ID = 0
    TAIL_ID = bridge_length - 1
    knots: list[Position] = [(0, 0) for _ in range(bridge_length)]
    unqiue_tail_cells: set[Position] = {knots[-1]}
    for head_direction, n_steps in instructions:
        for _ in range(n_steps):
            previous_knot_id = HEAD_ID
            knots[HEAD_ID] = move(knots[HEAD_ID], head_direction)
            for knot_id in range(1, bridge_length):
                if not should_move_knot(knots[previous_knot_id], knots[knot_id]):
                    break
                direction = relative_position(knots[previous_knot_id], knots[knot_id])
                knots[knot_id] = move(knots[knot_id], direction)
                if knot_id == TAIL_ID:
                    unqiue_tail_cells.add(knots[knot_id])
                previous_knot_id = knot_id
    return len(unqiue_tail_cells)


if __name__ == "__main__":
    instructions = load_input("input")
    print(f"Part one: Number of unique cells visited by tail: {part_one(instructions)}")
    part_two_answer = part_two(instructions, bridge_length=10)
    print(f"Part two: Number of unique cells visited by tail: {part_two_answer}")
