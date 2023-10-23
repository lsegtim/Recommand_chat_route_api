import itertools
import networkx as nx

def total_weight(graph, path):
    # Function to calculate the total weight of a path
    weight = 0
    for i in range(len(path) - 1):
        if graph.has_edge(path[i], path[i+1]):
            weight += graph[path[i]][path[i+1]]['weight']
        else:
            # If an edge doesn't exist, return a high weight to discourage this path
            return float('inf')
    return weight

def brute_force_tsp(graph, start, end):
    nodes = list(graph.nodes())
    nodes.remove(start)
    nodes.remove(end)
    shortest_path = None
    shortest_length = float('inf')

    for perm in itertools.permutations(nodes):
        path = [start] + list(perm) + [end]
        length = total_weight(graph, path)
        if length < shortest_length:
            shortest_length = length
            shortest_path = path

    return shortest_path, shortest_length

# Create a graph with your nodes and edges
graph = nx.Graph()
# Assuming nodes are numbered 0 to n-1 and start node is 0, end node is n-1
graph.add_nodes_from(range(5))
graph.add_weighted_edges_from([(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 0, 6), (0, 2, 7), (1, 3, 8), (2, 4, 9)])

# Find the shortest path from start to end visiting all nodes
start_node = 0
end_node = 2
path, length = brute_force_tsp(graph, start_node, end_node)

# Output the result
print(f'Shortest Path: {path}')
print(f'Path Length: {length}')

import matplotlib.pyplot as plt
# plot the graph with weighted edges
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True)
labels = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

plt.show()
