from typing import List

letter2int = {
  'F': 0,
  'B': 1,
  'L': 0,
  'R': 1
}

MAX_ROW_ID = 127
MAX_COL_ID = 7

def binary_search(sequence: str, interval: List[int]) -> int:
  for letter in sequence:
    start, end = interval
    middle = (start + end) // 2
    if not letter2int[letter]: # Take lower half
      interval = [start, middle]
    else: # Take upper half
      interval = [middle + 1, end]
  return interval[0]

def row_search(sequence: str) -> int:
  return binary_search(sequence, [0, MAX_ROW_ID])

def col_search(sequence: str) -> int:
  return binary_search(sequence, [0, MAX_COL_ID])

def get_seat_id(row_id, col_id):
  return row_id * 8 + col_id

def scan_seats(fh):
  seats = []
  for line in fh:
    line = line.strip()
    row_sequence, col_sequence = line[:7], line[7:]
    row_id = row_search(row_sequence)
    col_id = col_search(col_sequence)
    seat_id = get_seat_id(row_id, col_id)
    seats.append(seat_id)
    print(f'{line} -> {seat_id}')
  return seats

if __name__ == "__main__":
  fh = open('input.txt', 'r')
  seats = scan_seats(fh)
  fh.close()
  print(f'Max seat ID: {max(seats)}')
  