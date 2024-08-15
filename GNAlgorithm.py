import sys

def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    edges = []
    properties = {}

    for line in lines:
        parts = line.strip().split()
        if line == "\n" or line == "": continue
        if len(parts) == 2:
            user1 = int(parts[0])
            user2 = int(parts[1])
            edges.append((user1, user2))
        else:
            user_id = int(parts[0])
            props = list(map(int, parts[1:]))
            properties[user_id] = props
    
    return edges, properties

def load_data_sprut():
    ulaz = sys.stdin.readlines()
    ulaz = [line.strip() for line in ulaz]
    
    edges = []
    properties = {}

    for line in ulaz:
        if line == "\n" or line == "": continue
    
        parts = line.strip().split()
        if len(parts) == 2:
            user1 = int(parts[0])
            user2 = int(parts[1])
            edges.append((user1, user2))
        else:
            user_id = int(parts[0])
            props = list(map(int, parts[1:]))
            properties[user_id] = props
    
    return edges, properties

def weights(properties, u, v):
    u = properties[u]
    v = properties[v]
    
    same = sum(1 for x, y in zip(u, v) if x == y)
    weight = len(u) + 1 - same
    
    return weight

def create_graph(edges, properties):
    graph = {node: {} for node in properties.keys()}
    
    for u, v in edges:
        weight = weights(properties, u, v)
        graph[u][v] = weight
        graph[v][u] = weight
    
    return graph

def dijkstra(graph, start):
    queue = [(0, start, [start])]
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    shortest_paths = {start: [[start]]}
    while queue:
        current_distance, current_node, path = queue.pop(0)
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_paths[neighbor] = [path + [neighbor]]
                queue.append((distance, neighbor, path + [neighbor]))
            elif distance == distances[neighbor]:
                queue.append((distance, neighbor, path + [neighbor]))
                shortest_paths[neighbor].append(path + [neighbor])
    return distances, shortest_paths

def centrality(graph):
    betweenness = {}
    for s in graph:
        _, paths = dijkstra(graph, s)
        for target in paths:
            if target != s:
                num = len(paths[target])
                for path in paths[target]:
                    for i in range(len(path) - 1):
                        u, v = path[i], path[i + 1]
                        edge = tuple(sorted((u, v)))
                        if edge not in betweenness:
                            betweenness[edge] = 0.0
                        betweenness[edge] += 1 / num
    
    for edge in betweenness:
        betweenness[edge] /= 2.0
        if abs(betweenness[edge]) < 1e-5:
            betweenness[edge] = 0
    return {k: round(v, 4) for k, v in betweenness.items()}

def remove_edge(graph, centralities):
    maksi = max(centralities.values())
    edges_to_remove = sorted((edge for edge, cen in centralities.items() if cen == maksi))
    
    graph1 = {}
    for u, neighbours in graph.items():
        graph1[u] = {}
        for v, weight in neighbours.items():
            if (u, v) not in edges_to_remove and (v, u) not in edges_to_remove:
                graph1[u][v] = weight
    return edges_to_remove, graph1

def components(graph):
    all = {}
    for node in graph:
        _, paths = dijkstra(graph, node)
        all[node] = paths

    seen = set()
    communities = []

    for node in all:
        if node not in seen:
            community = set()
            for path_list in all[node].values():
                for path in path_list:
                    community.update(path)
            communities.append(list(community))
            seen.update(community)
    
    return communities

def calculate_modularity(graph, communities, ks):
    m = 0
    for _, edges in graph.items():
        for edge_weight in edges.values():
            m += edge_weight
    m = sum(ks.values())
    m /= 2
    if m == 0:
        return 0        
    modularity = 0
    sorted_nodes = sorted(graph.keys())
    #print(communities)
    for i in range(len(sorted_nodes)):
        u = sorted_nodes[i]
        for j in range(i, len(sorted_nodes)):
            v = sorted_nodes[j]
            A_uv = graph[u].get(v, 0)
            k_u = ks[u]
            k_v = ks[v]
            delta_uv = 0
            for community in communities:
                if u in community and v in community:
                    delta_uv = 1
                    break
            modularity += (A_uv - (k_u * k_v) / (2 * m)) * delta_uv
            #print(u, v, k_u, k_v, 2 * m, (A_uv - (k_u * k_v) / (2 * m)), delta_uv)
    modularity /= (2 * m)
    if abs(modularity) < 1e-5: return 0
    else: return round(modularity, 4)

def calculate_ks(graph):
    ks = {}
    for node, edges in graph.items():
        ks[node] = sum(edges.values())
    return ks

def girvan_newman_algorithm(edges, properties):
    graph = create_graph(edges, properties)
    all_communities = []
    modularities = []
    ks = calculate_ks(graph)
    while any(len(neighbours) > 0 for neighbours in graph.values()):
        centralities = centrality(graph)
        removed_edges, graph = remove_edge(graph, centralities)
        communities = components(graph)
        communities = sorted(communities, key = lambda x: (len(x), x))
        #print(communities, removed_edges)
        modularity = calculate_modularity(graph, communities, ks)
        all_communities.append((communities, removed_edges))
        modularities.append(modularity)
        #print(modularity, removed_edges)
    best = all_communities[modularities.index(max(modularities))]
    return best, all_communities

#edges, properties = load_data("primjer8.txt")
edges, properties = load_data_sprut()
best, all = girvan_newman_algorithm(edges, properties)
izlaz=""

for communities, removed_edges in all:
    for edge in removed_edges:
        izlaz += str(edge[0]) + " " + str(edge[1]) + "\n"

for community in best[0]:
    community = sorted(community)
    izlaz += "-".join(map(str, community)) + " "

print(izlaz)
