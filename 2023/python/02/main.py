from enum import StrEnum
from io import TextIOWrapper
from typing import Iterator


class Colors(StrEnum):
    red = "red"
    green = "green"
    blue = "blue"


Match = dict[Colors, int]
Game = list[Match]

BAG: dict[Colors, int] = {
    Colors.red: 12,
    Colors.green: 13,
    Colors.blue: 14,
}


def games_entries_generator(file: TextIOWrapper) -> Iterator[tuple[int, Game]]:
    """Generates game and game's id from the opened file"""
    for game_id, line in enumerate(file.readlines(), start=1):
        game: Game = []
        matches = line.strip().split(":")[1].split(";")
        for match_results in matches:
            match: Match = {}
            for entry in match_results.strip().split(","):
                quantity, color = entry.strip().split(" ")
                match[color] = int(quantity)  # type: ignore
            game.append(match)
        yield game_id, game


def is_possible_game(game: Game, bag: Match) -> bool:
    """Checks whether game is possible or not using given bag."""
    for match in game:
        for color, quantity in match.items():
            if quantity > bag[color]:
                return False
    return True


def part_one(file: TextIOWrapper) -> int:
    """Reads opened file and returns sum of possible games ids."""
    sum: int = 0
    for game_id, game in games_entries_generator(file=file):
        if is_possible_game(game=game, bag=BAG):
            sum += game_id
    return sum


def get_minimal_possible_bag(game: Game) -> Match:
    """Returns minimal bag with which game is possible."""
    bag: Match = dict.fromkeys([color.value for color in Colors], 0)  # type: ignore
    for match in game:
        for color, quantity in match.items():
            bag[color] = max(quantity, bag[color])
    return bag


def part_two(file: TextIOWrapper) -> int:
    """Reads opened file and returns sum of minimal bags powers.

    Bag power is calculated as multiplication of number of cubes of each color."""
    sum: int = 0
    for _, game in games_entries_generator(file=file):
        bag = get_minimal_possible_bag(game)
        power = 1
        for quantity in bag.values():
            power *= quantity
        sum += power
    return sum


if __name__ == "__main__":
    with open("input", "r") as file:
        part_one_answer = part_one(file=file)
        print(f"Part one: Sum of possible games ids: {part_one_answer}")

    with open("input", "r") as file:
        part_two_answer = part_two(file=file)
        print(f"Part two: Sum of minimal bags powers: {part_two_answer}")
