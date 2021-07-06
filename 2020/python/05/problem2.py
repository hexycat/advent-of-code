from problem1 import scan_seats

NROWS = 128
NCOLS = 8

def search_for_seat(seats, nrows, ncols):
  seats = set(seats) 
  # range changes from 1 to x - 1 because your seat is not at the front
  # and not the end of the plane
  empty_seats = set(range(1, ncols * nrows - 1)) - set(seats)
  for seat in empty_seats:
    if (seat + 1 in seats) and (seat - 1 in seats):
      return seat
  
if __name__ == "__main__":
  fh = open('input.txt', 'r')
  seats = scan_seats(fh)
  fh.close()
  seat_id = search_for_seat(seats, NROWS, NCOLS)
  if seat_id:
    print(f'Your seat ID: {seat_id}')
  else:
    print(f'Seat is not found!')