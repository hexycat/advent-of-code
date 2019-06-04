import time


def load_input(filename):
  with open(filename, 'r') as file:
    init_state_str = file.readline().split(' ')[2].replace('\n', '')
    init_state = [i for i in range(len(init_state_str)) if init_state_str[i] == '#']
    file.readline() # skip blank line
    rules = {}
    for line in file.readlines():
      combination_str, result_str = line.replace('\n', '').split(' => ')
      combination = tuple(i for i in range(5) if combination_str[i] == '#')
      result = 1 if (result_str == '#') else 0
      rules[combination] = result
  return init_state, rules


def get_batch(middle_pos):
  return tuple(range(middle_pos - 2, middle_pos + 3))


def encode_batch(batch, data):
  return tuple(i for i in range(5) if batch[i] in data)


def contain_flower(encoded_batch, rules):
  return bool(rules[encoded_batch])


def check_pot(pot, current_generation, rules):
  batch = get_batch(pot)
  encoded_batch = encode_batch(batch, current_generation)
  return contain_flower(encoded_batch, rules)


def check_nearest_pots(pot_with_flower, checked_pots, current_generation, rules):
  pots_with_flowers = []
  for pot in xrange(pot_with_flower - 2, pot_with_flower + 3):
      if pot in checked_pots:
        continue
      pot_will_contain_flower = check_pot(pot, current_generation, rules)
      if pot_will_contain_flower:
        pots_with_flowers.append(pot)
      checked_pots.add(pot)
  return pots_with_flowers, checked_pots


def save_generation(generation_id, current_generation):
  with open('save', 'w') as file:
      file.write('generation id: {}\n'.format(generation_id))
      file.write('pots with flowers: {}\n'.format(current_generation))
      file.write('sum: {}'.format(sum(current_generation)))


start_time = time.time()

n_generations = 1000000
current_generation, rules = load_input('input')
for generation_id in xrange(1, n_generations + 1):
  next_generation = []
  checked_pots = set() # save pots that was already checked
  for pot_with_flower in current_generation:
    pots_with_flowers, checked_pots = check_nearest_pots(pot_with_flower,
                                                        checked_pots,
                                                        current_generation,
                                                        rules)
    next_generation += pots_with_flowers
  current_generation = next_generation[:]

  if generation_id % (n_generations // 10) == 0:
    print('Epoch {} is done!'.format(generation_id))
    save_generation(generation_id, current_generation)

print('Completed in {} seconds'.format(time.time() - start_time))


# part 2 solution explained
# you should do 50 billions generations (50000000000) which is crazy
# every 1000000 generations takes about 100 seconds, so total time is 50000 times larger!
# to figure out the answer save semples of *** to file
# after some time there will be a pattern whithin pots with flowers

# for example, after 1000000 generations *** looks like:
# [999936, 999937, 999939, 999940, 999942, 999943, 999945, 999946, 999951, 999952, 999954, 999955, 999957, 999958, 999960, 999961, 999963, 999964, 999966, 999967, 999969, 999970, 999972, 999973, 999975, 999976, 999981, 999982, 999984, 999985, 999987, 999988, 999990, 999991, 999993, 999994, 999996, 999997, 999999, 1000000, 1000002, 1000003, 1000005, 1000006, 1000011, 1000012, 1000014, 1000015, 1000017, 1000018, 1000023, 1000024, 1000026, 1000027, 1000029, 1000030, 1000032, 1000033, 1000035, 1000036, 1000038, 1000039, 1000044, 1000045, 1000047, 1000048, 1000050, 1000051, 1000053, 1000054, 1000056, 1000057, 1000059, 1000060, 1000062, 1000063, 1000065, 1000066, 1000071, 1000072, 1000074, 1000075, 1000077, 1000078, 1000080, 1000081, 1000083, 1000084, 1000086, 1000087, 1000089, 1000090, 1000092, 1000093, 1000095, 1000096, 1000098, 1000099]

# and after 2000000 generations:
# [1999936, 1999937, 1999939, 1999940, 1999942, 1999943, 1999945, 1999946, 1999951, 1999952, 1999954, 1999955, 1999957, 1999958, 1999960, 1999961, 1999963, 1999964, 1999966, 1999967, 1999969, 1999970, 1999972, 1999973, 1999975, 1999976, 1999981, 1999982, 1999984, 1999985, 1999987, 1999988, 1999990, 1999991, 1999993, 1999994, 1999996, 1999997, 1999999, 2000000, 2000002, 2000003, 2000005, 2000006, 2000011, 2000012, 2000014, 2000015, 2000017, 2000018, 2000023, 2000024, 2000026, 2000027, 2000029, 2000030, 2000032, 2000033, 2000035, 2000036, 2000038, 2000039, 2000044, 2000045, 2000047, 2000048, 2000050, 2000051, 2000053, 2000054, 2000056, 2000057, 2000059, 2000060, 2000062, 2000063, 2000065, 2000066, 2000071, 2000072, 2000074, 2000075, 2000077, 2000078, 2000080, 2000081, 2000083, 2000084, 2000086, 2000087, 2000089, 2000090, 2000092, 2000093, 2000095, 2000096, 2000098, 2000099]

# so take this pattern and manually calculate pots ids with flower after 50000000000 generations
# correct answer is: 4900000001793
# and *** is:
# [49999999936, 49999999937, 49999999939, 49999999940, 49999999942, 49999999943, 49999999945, 49999999946, 49999999951, 49999999952, 49999999954, 49999999955, 49999999957, 49999999958, 49999999960, 49999999961, 49999999963, 49999999964, 49999999966, 49999999967, 49999999969, 49999999970, 49999999972, 49999999973, 49999999975, 49999999976, 49999999981, 49999999982, 49999999984, 49999999985, 49999999987, 49999999988, 49999999990, 49999999991, 49999999993, 49999999994, 49999999996, 49999999997, 49999999999, 50000000000, 50000000002, 50000000003, 50000000005, 50000000006, 50000000011, 50000000012, 50000000014, 50000000015, 50000000017, 50000000018, 50000000023, 50000000024, 50000000026, 50000000027, 50000000029, 50000000030, 50000000032, 50000000033, 50000000035, 50000000036, 50000000038, 50000000039, 50000000044, 50000000045, 50000000047, 50000000048, 50000000050, 50000000051, 50000000053, 50000000054, 50000000056, 50000000057, 50000000059, 50000000060, 50000000062, 50000000063, 50000000065, 50000000066, 50000000071, 50000000072, 50000000074, 50000000075, 50000000077, 50000000078, 50000000080, 50000000081, 50000000083, 50000000084, 50000000086, 50000000087, 50000000089, 50000000090, 50000000092, 50000000093, 50000000095, 50000000096, 50000000098, 50000000099]

