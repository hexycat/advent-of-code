from dataclasses import dataclass

@dataclass
class Frequency:
  lowest: int = 0
  highest: int = 0

@dataclass
class PasswordPolicy:
  frequency: Frequency = Frequency()
  letter: str = ''

@dataclass
class DatabaseEntry:
  raw: str = ''
  policy: PasswordPolicy = PasswordPolicy()
  password: str = ''

  @property
  def is_valid(self):
    lowest_count = self.policy.frequency.lowest
    highest_count = self.policy.frequency.highest
    letter_count = self.password.count(self.policy.letter)
    return lowest_count <= letter_count <= highest_count

def extract_info(database_entry: str) -> DatabaseEntry:
  password_policy, password = database_entry.strip().split(':')
  frequency, letter = password_policy.split()
  lowest, highest = frequency.split('-')
  frequency = Frequency(lowest=int(lowest.strip()), 
                        highest=int(highest.strip()))
  policy = PasswordPolicy(frequency=frequency, 
                          letter=letter.strip())
  return DatabaseEntry(raw=database_entry,
                       policy=policy,
                       password=password.strip())

if __name__ == '__main__':
  with open('input.txt', 'r') as file:
    database = file.readlines()

  n_valid = 0
  for raw_entry in database:
    entry = extract_info(raw_entry)
    if entry.is_valid:
      n_valid += 1

  print(f'Answer: {n_valid} valid out of {len(database)}')
