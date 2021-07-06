# Try to approach this problem in the same way as previous one
# When we get first term, it means that this term also consists of two components
# So search for that components

# Create function from problem 1 code

def find_terms(numbers, target_sum):
  for number in numbers:
    term = target_sum - number
    if (term in numbers) and (term != number):
      return number, term
  return None, None

TARGET_SUM  = 2020

with open('input.txt', 'r') as file:
  numbers = file.readlines()

# Convert to set to get O(1) number existence check complexity
numbers = {int(number.strip()) for number in numbers}

for number in numbers:
  term1, term2 = find_terms(numbers, TARGET_SUM - number)
  if term1 and term2:
    print(f'Target sum: {TARGET_SUM}')
    print(f'{number} + {term1} + {term2} = {number + term1 + term2}')
    print(f'Answer: {number * term1 * term2}')
    break
