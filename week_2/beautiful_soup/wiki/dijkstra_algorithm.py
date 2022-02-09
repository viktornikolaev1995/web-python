nodes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
distances = {
    'B': {'A': 5, 'D': 1, 'G': 2},
    'A': {'B': 5, 'D': 3, 'E': 12, 'F': 5},
    'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
    'G': {'B': 2, 'D': 1, 'C': 2},
    'C': {'G': 2, 'E': 1, 'F': 16},
    'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
    'F': {'A': 5, 'E': 2, 'C': 16}}

unvisited = {node: None for node in nodes} #using None as +inf
print(unvisited)
visited = {}
current = 'A'
currentDistance = 0
unvisited[current] = currentDistance
print(unvisited)
print(visited)
# elem = {}
while True:
    print("**************************")
    print(current)
    for neighbour, distance in distances[current].items():
        print(neighbour, distance)
        print(f'unvisited in start loop: {unvisited}')
        if neighbour not in unvisited.keys():
            print(True)
            continue
        newDistance = currentDistance + distance

        # if neighbour not in elem.keys():
        #     if current in elem.keys():
        #         elem[neighbour] = []
        #         elem[neighbour].append(elem[current])
        #         elem[neighbour].append(current)
        #     else:
        #         elem[neighbour] = current
        # elif neighbour in elem.keys():
        #     if len(elem[neighbour]) == 1:
        #         elem[neighbour] = set(elem[neighbour])
        #         elem[neighbour].add(current)
        #     else:
        #         elem[neighbour].add(current)

        if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
            # if len(elem[neighbour]) > 1:
                # elem[neighbour].pop()
                # elem[neighbour].append(current)
            unvisited[neighbour] = newDistance
            print(f'unvisited after 2 if: {unvisited}')
            # if len(elem[neighbour]) == 1:
            #     elem[neighbour] = set(elem[neighbour])
            #     elem[neighbour].add(current)
            # elif len(elem[neighbour]) > 1:
            #     elem[neighbour].add(current)
    visited[current] = currentDistance
    print(f'visited after add  current: {visited}')
    del unvisited[current]
    print(f'unvisited after del current: {unvisited}')
    if not unvisited:
        break

    candidates = [node for node in unvisited.items() if node[1]]
    print(f'candidates: {candidates}')
    current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]
    print(f'sorted candidates at 1 idx: {sorted(candidates, key = lambda x: x[1])}')
    print(f'current: {current}\ncurrentDistance: {currentDistance}')
    # print(current, currentDistance)
    # print(elem)
    print("**************************")

