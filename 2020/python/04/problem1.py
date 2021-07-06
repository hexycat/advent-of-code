class Passport():
  def __init__(self, **kwargs):
    for attr, value in kwargs.items():
      self.__setattr__(attr, value)

  def presented_fields(self):
    return set([name for name, value in self.get_attributes().items() if value is not None])
    
  def get_attributes(self):
    return {name: value for name, value in self.__dict__.items()
            if not(name.startswith('__') and name.endswith('__'))}

  def __repr__(self):
    return self.get_attributes().__str__()

  
class Scanner():
  @staticmethod
  def read_passports(queue):
    loaded_data = {}
    for line in queue:
      line = line.strip()
      if len(line) == 0:
        yield Passport(**loaded_data)
        loaded_data = {}
        continue
      line_data = {}
      for data in line.split(' '):
        field, value = data.split(':')
        line_data[field] = value
      loaded_data.update(line_data)
  
  def process_passendgers(self, queue, validation_function=None):
    if validation_function is None:
      validation_function = self.is_valid
    valid_passports = 0
    for passport in self.read_passports(queue):
      if validation_function(passport):
        valid_passports += 1
    return valid_passports

  def is_valid(self, passport: Passport) -> bool:
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    if len(required_fields - passport.presented_fields()) > 0:
      return False
    return True

if __name__ == '__main__':
  scanner = Scanner()
  queue = open('input.txt', 'r')
  valid_passports = scanner.process_passendgers(queue)
  print(f'{valid_passports=}')