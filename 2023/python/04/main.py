from typing import Iterator

CardNumbers = list[int]
Card = tuple[CardNumbers, CardNumbers]


def cards_generator(input: str) -> Iterator[Card]:
    """Loads card content from the file,.

    Card is described by two lists of int numbers - winning numbers and card numbers."""
    with open(input, "r") as file:
        for line in file.readlines():
            winning_numbers_str, card_numbers_str = line.strip().split(": ")[1].split("|")

            winning_numbers: list[int] = []
            for number in winning_numbers_str.split(" "):
                if not number:
                    continue
                winning_numbers.append(int(number))

            card_numbers: list[int] = []
            for number in card_numbers_str.split(" "):
                if not number:
                    continue
                card_numbers.append(int(number))

            yield winning_numbers, card_numbers


def calculate_card_points(winning_numbers: list[int], card_numbers: list[int]) -> int:
    """Calculates winning points of the card."""
    winning = set(winning_numbers)
    points: int = 0
    for number in card_numbers:
        if number not in winning:
            continue
        if not points:
            points += 1
            continue
        points *= 2
    return points


def part_one(cards_generator: Iterator[Card]) -> int:
    """Calculates total number of winning points within all cards."""
    total_points: int = 0
    for winning_numbers, card_numbers in cards_generator:
        total_points += calculate_card_points(winning_numbers, card_numbers)
    return total_points


def number_of_matches(winning_numbers: list[int], card_numbers: list[int]) -> int:
    """Calculates number of matches between card numbers and winning numbers."""
    winning = set(winning_numbers)
    matched: int = 0
    for number in card_numbers:
        if number not in winning:
            continue
        matched += 1
    return matched


def part_two(cards_generator: Iterator[Card]) -> int:
    """Calculates total number of cards after processing all original cards and copies."""
    cards_in_hand: list[int] = [1]

    for card_id, (winning_numbers, card_numbers) in enumerate(cards_generator):
        if card_id >= len(cards_in_hand):
            cards_in_hand.append(1)

        cards_to_get = number_of_matches(winning_numbers, card_numbers)
        for idx in range(1, cards_to_get + 1):
            if card_id + idx >= len(cards_in_hand):
                cards_in_hand.append(1)
            cards_in_hand[card_id + idx] += cards_in_hand[card_id]

    return sum(cards_in_hand[: card_id + 1])


if __name__ == "__main__":
    generator = cards_generator("input")
    part_one_answer = part_one(generator)
    print(f"Part one: Sum of cards points: {part_one_answer}")

    generator = cards_generator("input")
    part_two_answer = part_two(generator)
    print(f"Part two: Total cards in hand: {part_two_answer}")
