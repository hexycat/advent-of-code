with open('input', 'r') as file:
    polymer_source = file.readline().replace('\n', '')
    unique_chars = set(polymer_source.lower())

def collapse(polymer):
    i = 0
    while i < len(polymer) - 1:
        if polymer[i].upper() == polymer[i+1].upper():
            if polymer[i] != polymer[i+1]:
                try:
                    polymer = polymer[:i] + polymer[i+2:]
                except:
                    polymer = polymer[:i]
                i -= 2
                i = max(i, -1)
        i += 1
    return len(polymer)

# part 1
print('Answer: {}'.format(collapse(polymer_source)))

# part 2
min_length = len(polymer_source)
for char in unique_chars:
    polymer = polymer_source.replace(char.upper(), '').replace(char.lower(), '')
    polymer_length = collapse(polymer)
    min_length = min(min_length, polymer_length)
print('Answer 2: {}'.format(min_length))
