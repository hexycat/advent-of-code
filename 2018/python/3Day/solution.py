import numpy as np

filename = 'input'
with open(filename, 'r') as file:
  data = file.readlines()

N_COLUMNS = 4
n_claims = len(data)

claims_params = np.zeros((n_claims, N_COLUMNS), dtype=int)
for i in range(n_claims):
  row = data[i].replace('\n', '')
  rectungle_params = row.split(' @ ')[1].split(': ')
  indent = np.array(rectungle_params[0].split(','), dtype=int)
  size = np.array(rectungle_params[1].split('x'), dtype=int)
  claims_params[i, 0:2] = indent
  claims_params[i, 2:4] = indent + size

material_width = claims_params[:, 2].max() - 1
material_length = claims_params[:, 3].max() - 1
material = np.zeros((material_length, material_width))

for i in range(n_claims):
  w_from, l_from, w_to, l_to = claims_params[i, :]
  material[l_from:l_to, w_from:w_to] += 1

result = (material > 1).sum()
print(result)

# Puzzle 2
claims_to_skip = {claim_id: [claim_id, ] for claim_id in range(n_claims)}

for claim_id in range(n_claims):
  claim_param = claims_params[claim_id, :]
  intersection = bool(len(claims_to_skip[claim_id]) - 1)

  for another_claim_id in range(claim_id + 1, n_claims):
    if another_claim_id in claims_to_skip[claim_id]:
      continue

    another_claim_param = claims_params[another_claim_id, :]
    width_intersect = (claim_param[0] < another_claim_param[2]) and (another_claim_param[0] < claim_param[2])
    length_intersect = (claim_param[1] < another_claim_param[3]) and (another_claim_param[1] < claim_param[3])
    if width_intersect and length_intersect:
      intersection = True
      claims_to_skip[another_claim_id].append(claim_id)

  if not intersection:
    print(claim_id + 1)
    break
