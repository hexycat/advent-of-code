"""Day 11: https://adventofcode.com/2022/day/11"""

from typing import Callable


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: Callable[[int], int],
        test: Callable[[int], int],
        divisor: int = 1,
    ) -> None:
        self.items = items
        self.operation = operation
        self.test = test
        self.divisor = divisor
        self.worry_level_reduction: Callable[[int], int] = lambda wr: int(wr / 3)
        self.total_inspects = 0

    def inpect_item(self) -> tuple[int | None, int | None]:
        """Inspect next item and return (worry level, next monkey id)"""
        if not self.items:
            return None, None
        item = self.items.pop()
        worry_level = self.worry_level_reduction(self.operation(item))
        monkey_id = self.test(worry_level)
        self.total_inspects += 1
        return worry_level, monkey_id


def parse_starting_items(line: str) -> list[int]:
    """Parse starting items line"""
    items_str = line.split(":")[-1].strip()
    return [int(item) for item in items_str.split(",")]


def parse_operation(line: str) -> Callable[[int], int]:
    """Parse operation line"""
    element = line.split(" ")[-1].strip()
    if element == "old":
        return lambda old: old * old
    if "*" in line:
        return lambda old: old * int(element)
    return lambda old: old + int(element)


def parse_test(lines: list[str]) -> tuple[Callable[[int], int], int]:
    """Parse test line and return test function and divisor"""
    for line in lines:
        number = int(line.split()[-1].strip())
        if "Test" in line:
            divisor = number
            continue
        if "true" in line:
            next_monkey_positive = number
            continue
        if "false" in line:
            next_monkey_negative = number
    return (
        lambda value: next_monkey_positive
        if value % divisor == 0
        else next_monkey_negative
    ), divisor


def load_input(filepath: str) -> list[Monkey]:
    """Load input and return list of monkeys"""
    monkeys = []
    with open(filepath, "r") as file:
        while True:
            line = file.readline()
            if not line:  # EOF case
                break
            if not line.strip() or line.startswith("Monkey"):
                continue
            start_items = parse_starting_items(line)
            operation = parse_operation(file.readline())
            test, divisor = parse_test([file.readline() for _ in range(3)])
            monkeys.append(
                Monkey(
                    items=start_items, operation=operation, test=test, divisor=divisor
                )
            )
    return monkeys


def play_round(monkeys: list[Monkey]) -> None:
    """Play round: all monkeys inspect all items at begining of their turn"""
    for monkey in monkeys:
        item, next_monkey = monkey.inpect_item()
        while item is not None and next_monkey is not None:
            monkeys[next_monkey].items.append(item)
            item, next_monkey = monkey.inpect_item()


def play(monkeys: list[Monkey], n_rounds: int = 1) -> int:
    """Play N rounds and calculate the level of monkey business.
    Round - all monkeys inspect all items that are available at
    the begining of their turn. Monkey business - multiplication
    of total interactions of two monkeys with the most total interactions"""
    for _ in range(n_rounds):
        play_round(monkeys=monkeys)
    inspects = [monkey.total_inspects for monkey in monkeys]
    inspects.sort(reverse=True)
    return inspects[0] * inspects[1]


def part_one(monkeys: list[Monkey]) -> int:
    """Play 20 rounds and calculate the level of monkey business.
    Monkey business - multiplication of total interactions of
    two monkeys with the most total interactions"""
    return play(monkeys=monkeys, n_rounds=20)


def update_worry_level_reduction(
    monkeys: list[Monkey], divisor: int = 1
) -> list[Monkey]:
    """Update worry level reduction for all monkeys to remainder of
    total product of divisors"""
    product = get_divisor_product(monkeys)
    monkeys_updated = []
    for monkey in monkeys:
        monkey.worry_level_reduction = lambda wr: int(wr % product)
        monkeys_updated.append(monkey)
    return monkeys_updated


def get_divisor_product(monkeys: list[Monkey]) -> int:
    """Calculate product of all divisors"""
    product = 1
    for monkey in monkeys:
        product *= monkey.divisor
    return product


def part_two(monkeys: list[Monkey]) -> int:
    """Play 10000 rounds with  updated worry level reduction and calculate
    the level of monkey business. Monkey business - multiplication
    of total interactions of two monkeys with the most total interactions"""
    monkeys = update_worry_level_reduction(monkeys)
    return play(monkeys=monkeys, n_rounds=10000)


if __name__ == "__main__":
    monkeys = load_input("input")
    msg = "Part one: The level of monkey business after 20 rounds:"
    print(f"{msg} {part_one(monkeys)}")

    monkeys = load_input("input")
    print(
        "Part two: The level of monkey business after 10000 rounds "
        + f"and updated worry level reduction: {part_two(monkeys)}"
    )
