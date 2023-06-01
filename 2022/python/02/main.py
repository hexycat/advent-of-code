"""Day 2: Rock Paper Scissors | https://adventofcode.com/2022/day/2"""

ROCK_OPPONENT = "A"
PAPER_OPPONENT = "B"
SCISSORS_OPPONENT = "C"

# Part one specific constants
ROCK_SELF = "X"
PAPER_SELF = "Y"
SCISSORS_SELF = "Z"
WIN = "W"
DRAW = "D"
LOSE = "L"

# Part two specific constants
ROCK_PLAY = "R"
PAPER_PLAY = "P"
SCISSORS_PLAY = "S"
LOSE_INSTRUCTION = "X"
DRAW_INSTRUCTION = "Y"
WIN_INSTRUCTION = "Z"


def load_input(filepath: str) -> list:
    """Read input data, split lines by space and return it as list of lists"""
    lines = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            lines.append(line.strip().split(" "))
    return lines


def play_game(opponent_play: str, self_play: str) -> str:
    """Return outcome of rock paper scissors game: win, draw or lose"""
    if (
        (opponent_play == ROCK_OPPONENT and self_play == ROCK_SELF)
        or (opponent_play == PAPER_OPPONENT and self_play == PAPER_SELF)
        or (opponent_play == SCISSORS_OPPONENT and self_play == SCISSORS_SELF)
    ):
        return DRAW
    if (
        (opponent_play == ROCK_OPPONENT and self_play == PAPER_SELF)
        or (opponent_play == PAPER_OPPONENT and self_play == SCISSORS_SELF)
        or (opponent_play == SCISSORS_OPPONENT and self_play == ROCK_SELF)
    ):
        return WIN
    return LOSE


def part_one(instructions: list) -> int:
    """Calculates total score of the game in case you follow instructions from
    input file and interpret them as self play"""
    SCORES = {
        ROCK_SELF: 1,
        PAPER_SELF: 2,
        SCISSORS_SELF: 3,
        WIN: 6,
        DRAW: 3,
        LOSE: 0,
    }
    score = 0
    for opponent_play, self_play in instructions:
        outcome = play_game(opponent_play=opponent_play, self_play=self_play)
        score += SCORES.get(outcome, 0) + SCORES.get(self_play, 0)
    return score


def calculate_play(opponent_play: str, outcome: str) -> str:
    """Calculates your play depending on opponent play and desired game outcome"""
    if (
        (outcome == WIN_INSTRUCTION and opponent_play == ROCK_OPPONENT)
        or (outcome == LOSE_INSTRUCTION and opponent_play == SCISSORS_OPPONENT)
        or (outcome == DRAW_INSTRUCTION and opponent_play == PAPER_OPPONENT)
    ):
        return PAPER_PLAY

    if (
        (outcome == WIN_INSTRUCTION and opponent_play == SCISSORS_OPPONENT)
        or (outcome == LOSE_INSTRUCTION and opponent_play == PAPER_OPPONENT)
        or (outcome == DRAW_INSTRUCTION and opponent_play == ROCK_OPPONENT)
    ):
        return ROCK_PLAY
    return SCISSORS_PLAY


def part_two(instructions: list) -> int:
    """Calculates total score of the game in case you follow instructions from
    input file and interpret them as game outcome"""
    SCORES = {
        ROCK_PLAY: 1,
        PAPER_PLAY: 2,
        SCISSORS_PLAY: 3,
        LOSE_INSTRUCTION: 0,
        DRAW_INSTRUCTION: 3,
        WIN_INSTRUCTION: 6,
    }
    score = 0
    for opponent_play, game_outcome in instructions:
        self_play = calculate_play(opponent_play=opponent_play, outcome=game_outcome)
        score += SCORES.get(self_play, 0) + SCORES.get(game_outcome, 0)
    return score


if __name__ == "__main__":
    instrcutions = load_input("input")
    part_one_answer = part_one(instrcutions)
    print(f"Part one: Total score: {part_one_answer}")
    part_two_answer = part_two(instrcutions)
    print(f"Part two: Total score: {part_two_answer}")
