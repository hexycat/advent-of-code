TARGET_SUM = 2020

with open('input.txt', 'r') as file:
	numbers = file.readlines()

# Convert to set to get O(1) number existence check complexity
# Cons: Uable to find numbers presented twice in numbers list
# for example: 1010 + 1010 for target sum of 2020
numbers = {int(number.strip()) for number in numbers}

for number in numbers:
	term = TARGET_SUM - number
	if (term != number) and (term in numbers):
	  print(f'Sum: {number} + {term} = {TARGET_SUM}')
	  print(f'Answer: {number * term}')
	  break
