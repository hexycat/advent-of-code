from problem1 import DatabaseEntry, extract_info

@property
def is_valid(self):
  lowest_pos = self.policy.frequency.lowest - 1
  highest_pos = self.policy.frequency.highest - 1
  letter = self.policy.letter
  at_lowest = self.password[lowest_pos] == letter
  at_highest = self.password[highest_pos] == letter
  return at_lowest ^ at_highest

DatabaseEntry.is_valid = is_valid

if __name__ == '__main__':
  with open('input.txt', 'r') as file:
    database = file.readlines()

  n_valid = 0
  for raw_entry in database:
    entry = extract_info(raw_entry)
    if entry.is_valid:
      n_valid += 1

  print(f'Answer: {n_valid} valid out of {len(database)}')
