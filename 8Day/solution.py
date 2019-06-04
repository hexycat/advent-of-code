with open('input', 'r') as file:
    data = file.readline().replace('\n', '').split(' ')

data = [int(number) for number in data]

# part 1
def extract_subtree(start_pos, data, metadata):
    childs = data[start_pos]
    metadata_size = data[start_pos + 1]
    i = start_pos + 2
    for child_number in range(childs):
        i, metadata, sub_metadata_size = extract_subtree(i, data, metadata)
    new_metadata = data[i:i+metadata_size]
    return i+metadata_size, metadata + new_metadata, metadata_size

metadata = []
end_pos, metadata, last_metadata_size = extract_subtree(0, data, metadata)
print('Part 1:', sum(metadata))


# part 2
root = 0 # root node is 0 in our notation
node_value = {} # node: node_value

# pos - position in data list
# in out notation: pos = node_id
def get_node_value(pos, data, node_value):
    n_childs = data[pos]
    n_metadata = data[pos + 1]

    if n_childs == 0:
        metadata_pos = pos + 2
        node_value[pos] = sum( data[metadata_pos:metadata_pos+n_metadata] )
        return metadata_pos+n_metadata, node_value

    childs_ids = []
    next_node = pos + 2

    for _ in range(n_childs):
        childs_ids.append(next_node)
        next_node, node_value = get_node_value(next_node, data, node_value)

    current_node_value = 0
    metadata = data[next_node : next_node+n_metadata]
    for value in metadata:
        try:
            node = childs_ids[value - 1]
            current_node_value += node_value.get(node, 0)
        except:
            pass

    node_value[pos] = current_node_value
    return next_node + n_metadata, node_value

_, node_value = get_node_value(0, data, node_value)
print(f'Part 2: {node_value[root]}')
