STACK_SIZE = 25

def find_weakness(numbers_list):
  stack = []
  for i, number in enumerate(numbers_list):
    number = int(number.strip())
    if i < STACK_SIZE:
      stack.append(number)
      continue
    if not is_sum_of_previous(number, stack):
      print(number)
      break
    stack[:-1] = stack[1:]
    stack[-1] = number

def is_sum_of_previous(number, stack):
  for i in range(len(stack)):
    for j in range(i, len(stack)):
      if stack[i] == stack[j]:
        continue
      if stack[i] + stack[j] == number:
        return True
  return False


if __name__ == "__main__":
  fh = open('input.txt', 'r')
  find_weakness(fh)
  fh.close()