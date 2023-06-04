"""Day 5: https://adventofcode.com/2022/day/5"""


def parse_stack_level_row(row: str) -> list:
    """Parse stack row and extract crate names of one stack level"""
    n_stacks = int(len(row) // 4) + 1
    stack_level = ["" for _ in range(n_stacks)]
    for stack_id, i in enumerate(range(0, len(row), 4)):
        if row[i] == "[":
            stack_level[stack_id] = row[i + 1]
    return stack_level


def parse_instruction_row(row: str) -> tuple:
    """Parse intruction row and return tuple (amount, from, to)"""
    splits = row.split(" ")
    return int(splits[1]), int(splits[3]), int(splits[5])  # (amount, from, to)


def load_input(filepath: str) -> tuple:
    """Loads input data, returns two objects:
    stacks that are represented as list[list[str]], and
    instructions that are represented as list[list[int]]"""
    stacks = []
    instructions = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.rstrip("\n")
            if "from" in line:  # instruction
                entry = parse_instruction_row(line)
                instructions.append(entry)
                continue
            if "[" in line:  # [ indicates row with stack crates
                stack_level = parse_stack_level_row(line)
                if not stacks:
                    stacks = [[] for _ in range(len(stack_level))]
                for stack_id, crate in enumerate(stack_level):
                    if not crate:
                        continue
                    # put crate under the previous crates
                    # due to we read rows from top to bottom
                    # so top crate will always be at the end of the list
                    stacks[stack_id] = [crate] + stacks[stack_id]
    return stacks, instructions


def part_one(stacks: dict, instructions: list) -> str:
    """Apply instructions to stack and return top crate names as string.
    Crates can only be moved one at a time"""
    for amount, stack_from, stack_to in instructions:
        for _ in range(amount):
            crate = stacks[stack_from - 1].pop()
            stacks[stack_to - 1].append(crate)
    top_crates = [crates[-1] for crates in stacks]
    return "".join(top_crates)


def part_two(stacks: dict, instructions: list) -> str:
    """Apply instructions to stack and return top crate names as string.
    Crates are moved together, preserving the order"""
    for amount, stack_from, stack_to in instructions:
        crates = stacks[stack_from - 1][-amount:]
        stacks[stack_from - 1] = stacks[stack_from - 1][:-amount]
        stacks[stack_to - 1] += crates
    top_crates = [crates[-1] for crates in stacks]
    return "".join(top_crates)


if __name__ == "__main__":
    stacks, instructions = load_input("input")
    msg = "Part one: Top crates after applying instructions (one by one): "
    print(msg + part_one(stacks, instructions))

    stacks, instructions = load_input("input")
    msg = "Part two: Top crates after applying instructions (many at a time): "
    print(msg + part_two(stacks, instructions))
