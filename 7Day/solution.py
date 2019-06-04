graph = {}
unique_nodes = []

with open('input', 'r') as file:
    for line in file:
        finished = line.split(' ')[1]
        before = line.split(' ')[7]
        if before not in graph:
            graph[before] = []
        graph[before].append(finished)

        unique_nodes.append(before)
        unique_nodes.append(finished)

unique_nodes = set(unique_nodes)
for node in unique_nodes:
    if node not in graph:
        graph[node] = []

graph = [(node, dependencies) for node, dependencies in graph.items()]
graph = sorted(graph, key=lambda x: x[0])
graph_source = [(node, dependencies[:]) for node, dependencies in graph]
answer_length = len(graph)



# part 1
answer1 = []
while len(answer1) != answer_length:
    for node, dependencies in graph:
        if not bool(dependencies):
            answer1 += [node, ]
            break

    graph.remove((node, []))
    for _, dependencies in graph:
        try:
            dependencies.remove(node)
        except:
            pass

print('Answer 1: {}'.format(''.join(answer1)))



# part 2
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
time_per_node = {char: 60 + i + 1 for i, char in enumerate(alphabet)}
timer = dict.fromkeys(alphabet, 0)
workers = 5
graph = [(node, dependencies[:]) for node, dependencies in graph_source]
answer2 = []
processing = []
total_seconds = 0

while len(answer2) != answer_length:
    total_seconds += 1
    completed_nodes = []
    for node, dependencies in graph:
        if (not bool(dependencies)) and (node not in processing):
            if len(processing) < workers:
                processing.append(node)
            else:
                break

    for node in processing:
        timer[node] += 1
        if timer[node] == time_per_node[node]:
            completed_nodes.append(node)

    for node in completed_nodes:
        answer2 += [node, ]
        processing.remove(node)
        graph.remove((node, []))
        for _, dependencies in graph:
            try:
                dependencies.remove(node)
            except:
                pass

print('Answer 2: {}'.format(total_seconds))
print('Part 2 sequence: {}'.format(''.join(answer2)))
