import re
from problem1 import Scanner, Passport

class ImprovedScanner(Scanner):
  def _height_rule(hgt):
    if hgt.endswith('cm') and (150 <= int(hgt[:-2]) <= 193):
      return True
    elif hgt.endswith('in') and (59 <= int(hgt[:-2]) <= 76):
      return True
    return False

  def _hair_color_rule(color):
    regex = r'^#[a-f0-9]{6}$'
    return re.fullmatch(regex, color) is not None

  def _pid_rule(pid):
    if not len(pid) == 9:
      return False
    try:
      int(pid)
    except:
      return False
    return True

  rules = {
    'byr': lambda year: 1920 <= int(year) <= 2002, # Birth Year
    'iyr': lambda year: 2010 <= int(year) <= 2020, # Issue Year
    'eyr': lambda year: 2020 <= int(year) <= 2030, # Expiration Year
    'hgt': _height_rule, # Height
    'hcl': _hair_color_rule, # Hair Color
    'ecl': lambda color: color in  {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}, # Eye Color
    'pid': _pid_rule, # Passport ID
  }


  def is_strictly_valid(self, passport: Passport):
    if not self.is_valid(passport):
      return False
    for field, check_function in self.rules.items():
      if not check_function(getattr(passport, field)):
        return False
    return True

if __name__ == '__main__':
  scanner = ImprovedScanner()
  queue = open('input.txt', 'r')
  valid_passports = scanner.process_passendgers(queue, validation_function=scanner.is_strictly_valid)
  print(f'{valid_passports=}')