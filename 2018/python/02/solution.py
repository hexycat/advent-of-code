from collections import Counter
# from functools import reduce
# import numpy as np

boxes = []
with open('input', 'r') as file:
	for box_id in file:
		boxes.append(box_id)
# boxes = [items.replace('\n', '') for items in boxes]


# Puzzle 1
doubles = 0
tripples = 0
for box in boxes:
	bag_of_words = Counter(box)
	if 2 in bag_of_words.values():
		doubles += 1
	if 3 in bag_of_words.values():
		tripples += 1
checksum = doubles * tripples

# print('Puzzle 1')
# print(f'Total doubles: {doubles}')
# print(f'Total tripples: {tripples}')
print(f'Checksum: {checksum}')


#Puzzle 2

# id_length = len(boxes[0])
# splitted_ids = list(zip(*boxes))

# def connect_letters(arr):
# 	return reduce(lambda x, y: x + y, arr)

# for i in range(id_length):
# 	ids_by_letters = np.column_stack(splitted_ids[:i] + splitted_ids[i+1:])
# 	ids = np.apply_along_axis(connect_letters, axis=1, arr=ids_by_letters)
# 	ids_counts = Counter(list(ids))
# 	if 2 in ids_counts.values():
# 		counts2id = {v: k for k, v in ids_counts.items()}
# 		break

found = False
num_of_ids = len(boxes)
id_length = len(boxes[0])
for box_id in range(num_of_ids):
	if found:
		break

	for another_box_id in range(box_id + 1, num_of_ids):
		differences = 0
		last_diff_letter_id = None
		for letter_id in range(id_length):
			if boxes[box_id][letter_id] != boxes[another_box_id][letter_id]:
				differences += 1
				last_diff_letter_id = letter_id
			if differences > 1:
				break

		if differences == 1:
			print(boxes[box_id][:last_diff_letter_id] + 
					boxes[box_id][last_diff_letter_id+1:])
			found = True
			break


# print('\nPuzzle 2')
# print(f'Common letters between the two: {counts2id[2]} (answer)')
# print(f'Common part length: {len(counts2id[2])}')
# print(f'Initial id length: {id_length}')
# print(f'Dropped letter id: {i}')
# print(f'Unique numbers of matches: {list(counts2id.keys())}')
