"""Day 13: https://adventofcode.com/2022/day/13"""
import json


def load_input(filepath: str) -> list[list]:
    """Read input file and return list of signal pairs"""
    signals = []
    pair = []
    with open(filepath, mode="r", encoding="utf-8") as file:
        for line in file.readlines():
            if not line.strip():
                signals.append(pair)
                pair = []
                continue
            pair.append(json.loads(line.strip()))
        signals.append(pair)
        return signals


def first_int_is_smaller(first: int, second: int) -> bool | None:
    """Check whether first integer is smaller. Return None if they are equal"""
    if first == second:
        return None
    return first < second


def first_signal_is_smaller(first: list, second: list) -> bool | None:
    """Check whether the first signal is smaller. Return None if they are equal"""
    len_first = len(first)
    len_second = len(second)
    for i in range(min(len_first, len_second)):
        is_smaller = None
        if isinstance(first[i], int) and isinstance(second[i], int):
            is_smaller = first_int_is_smaller(first[i], second[i])
        elif isinstance(first[i], list) and isinstance(second[i], list):
            is_smaller = first_signal_is_smaller(first[i], second[i])
        elif isinstance(first[i], int):
            is_smaller = first_signal_is_smaller([first[i]], second[i])
        else:
            is_smaller = first_signal_is_smaller(first[i], [second[i]])
        if is_smaller is not None:
            return is_smaller
    if len_first == len_second:
        return None
    return len_first < len_second


def part_one(signals: list) -> int:
    """Return sum of signal pair indices that are in the right order.
    Pair is in the right order if the first signal is smaller than the second one.
    Index numeration starts from 1"""
    sum_of_indices = 0
    for position, (first, second) in enumerate(signals, start=1):
        if first_signal_is_smaller(first, second):
            sum_of_indices += position
    return sum_of_indices


def bubble_sort(signals: list) -> list:
    """Sort signals inplace in ascending order using bubble sort"""
    for i in range(len(signals)):
        for j in range(i + 1, len(signals)):
            if first_signal_is_smaller(signals[i], signals[j]) is False:
                signals[i], signals[j] = signals[j], signals[i]
    return signals


def part_two(signal_pairs: list) -> int:
    """Calculate decoder key. Decoder key is multiplication of divider indices
    within signals that are sorted in the right order. Index numeration starts
    from 1"""
    DIVIDER1 = [[2]]
    DIVIDER2 = [[6]]
    # Flatten signal pairs
    signals = [DIVIDER1, DIVIDER2]
    for pair in signal_pairs:
        signals += pair
    bubble_sort(signals)
    return (signals.index(DIVIDER1) + 1) * (signals.index(DIVIDER2) + 1)


if __name__ == "__main__":
    signals = load_input("input")
    p1_answer = part_one(signals)
    print(f"Part one: Sum of pair indices that are in the right order: {p1_answer}")
    print(f"Part two: Decoder key: {part_two(signals)}")
