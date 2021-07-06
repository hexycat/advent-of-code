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

def run(instructions):
  while True:
    operation, argument = instructions[iid].strip().split()
    if iid in visited_iids:
      print(accumulator)
      break
    visited_iids.add(iid)
    operations[operation.strip()](int(argument))

with open('input.txt', 'r') as file:
  instructions = file.readlines()

run(instructions)