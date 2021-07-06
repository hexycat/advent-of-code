STACK_SIZE = 25

def find_answer(numbers_list, target_number):
  stack = []
  for number in numbers_list:
    number = int(number.strip())
    stack.append(number)
    stack = construct_contiguous_list(stack, target_number)
    if sum(stack) == target_number:
      print(min(stack) + max(stack))
      return
    
def construct_contiguous_list(stack, target_number):
  sum = 0
  sub_stack = []
  for i, number in enumerate(stack[::-1]):
    sum += number
    sub_stack.append(number)
    if i < 2:
      continue
    if sum >= target_number:
      break
  return sub_stack[::-1]

if __name__ == "__main__":
  fh = open('input.txt', 'r')
  find_answer(fh, 1721308972)
  fh.close()