import sys

"""
ulaz = []
with open('ulaz.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        ulaz.append(line)
"""
ulaz = sys.stdin.readlines()
ulaz = [line.strip() for line in ulaz]

n, e = ulaz[0].split(" ")
n = int(n)
e = int(e)

black_nodes = []
graph = {}
for i in range(n):
    if int(ulaz[i+1]): black_nodes.append(i)
    graph[i] = []

for i in range(e):
    brid = ulaz[n+1+i].split(" ")
    u = int(brid[0])
    v = int(brid[1])
    graph[u].append(v)
    graph[v].append(u)

"""
for key, value in graph.items():
    print(key, ": ", value)
"""

def black_nodes_bfs(graph, black_nodes, max_depth=10):
    queue = [(node, 0) for node in black_nodes]
    n = len(graph)
    distances = [-1] * n
    depths = [-1] * n

    for node in black_nodes:
        distances[node] = node
        depths[node] = 0

    while queue:
        current_node, depth = queue.pop(0)

        if depth > max_depth:
            continue

        for neighbour in graph[current_node]:
            if depths[neighbour] == -1 or depth + 1 < depths[neighbour]:
                depths[neighbour] = depth + 1
                distances[neighbour] = distances[current_node]
                queue.append((neighbour, depth + 1))
            elif depth + 1 == depths[neighbour]:
                if distances[current_node] < distances[neighbour]:
                    distances[neighbour] = distances[current_node]

    return distances, depths

distances, depths = black_nodes_bfs(graph, black_nodes)

izlaz = ""
for i in range(n):
    if depths[i] == -1:
        izlaz += "-1 -1\n"
    else:
        izlaz += f"{distances[i]} {depths[i]}\n"

print(izlaz.strip())