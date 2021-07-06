import copy

accumulator = 0
iid = 0
visited_iids = set()

def acc(value):
  global accumulator, iid
  accumulator += value
  iid += 1

def jmp(value):
  global iid
  iid += value

def nop(_):
  global iid
  iid += 1

operations = {
  'acc': acc,
  'jmp': jmp,
  'nop': nop
}

def reset():
  global iid, accumulator, visited_iids
  accumulator = 0
  iid = 0
  visited_iids = set()

def run(instructions):
  termination_iid = len(instructions)
  while True:
    operation, argument = instructions[iid].strip().split()
    if iid in visited_iids:
      print(f'Infinite loop termination status: {accumulator}')
      return 1
    visited_iids.add(iid)
    operations[operation.strip()](int(argument))
    if iid == termination_iid:
      print(f'Normal termination status: {accumulator}')
      return 0
  return 2

def fix_run(instructions):
  fixed_codes = set()
  while True:
    reset()
    instructions_copy = copy.deepcopy(instructions)
    for i, instruction in enumerate(instructions_copy):
      if ('jmp' in instruction) and (i not in fixed_codes):
        instructions_copy[i] = instruction.replace('jmp', 'nop')
        fixed_codes.add(i)
        print(f'Fix code jmp at position {i}')
        break
      elif ('nop' in instruction) and (i not in fixed_codes):
        instructions_copy[i] = instruction.replace('nop', 'jmp')
        fixed_codes.add(i)
        print(f'Fix code nop at position {i}')
        break
    exit_code = run(instructions_copy)
    if not exit_code:
      return

with open('input.txt', 'r') as file:
  instructions = file.readlines()

fix_run(instructions)