with open('input', 'r') as f:
	series = f.readlines()

# Puzzle 1
series = [int(value) for value in series]
series_len = len(series)
print(f'Sum of the series: {sum(series)}')

# Puzzle 2
frequencies = {0, }
summ = 0
i = 0

while True:
	summ += series[i]
	if summ in frequencies:
		print(f'First repeat is: {summ}')
		break
	else:
		frequencies.add(summ)

	i += 1
	if i == series_len:
		i = 0

print(f'Number of unique frequencies: {len(frequencies)}')