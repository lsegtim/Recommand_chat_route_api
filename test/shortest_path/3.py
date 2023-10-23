def tsp(adj_matrix, start, end):
    n = len(adj_matrix)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1 << start][start] = 0
    pred = [[-1] * n for _ in range(1 << n)]

    for mask in range(1, 1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue

            for v in range(n):
                if mask & (1 << v) and adj_matrix[v][u] != -1:
                    if dp[mask][u] > dp[mask ^ (1 << u)][v] + adj_matrix[v][u]:
                        dp[mask][u] = dp[mask ^ (1 << u)][v] + adj_matrix[v][u]
                        pred[mask][u] = v

    mask = (1 << n) - 1
    u = end
    path = []

    while u != -1:
        path.append(u)
        v = pred[mask][u]
        mask = mask ^ (1 << u)
        u = v

    path.reverse()
    return dp[(1 << n) - 1][end], path


def duplicate_nodes(adj_matrix, copies):
    n = len(adj_matrix)
    new_n = n * copies
    new_matrix = [[0] * new_n for _ in range(new_n)]

    for i in range(new_n):
        for j in range(new_n):
            new_matrix[i][j] = adj_matrix[i % n][j % n]

    return new_matrix


# Original adjacency matrix
adj_matrix = [
    [0, 1, 2, 3, 4],
    [1, 0, 5, 6, 7],
    [2, 5, 0, 8, 9],
    [3, 6, 8, 0, 10],
    [4, 7, 9, 10, 0]
]

# Duplicate each node 2 times
copies = 2
new_adj_matrix = duplicate_nodes(adj_matrix, copies)

# Update start and end nodes indices
start, end = 0, 4
new_start = start * copies
new_end = (end + 1) * copies - 1

# Solve TSP on the new graph
shortest_path_length, shortest_path = tsp(new_adj_matrix, new_start, new_end)

# Adjust the node indices in the path to reflect the original node indices
n = len(adj_matrix)
shortest_path = [node % n for node in shortest_path]

# Output
print(f'Shortest path length: {shortest_path_length}')
print(f'Shortest path: {shortest_path}')  # [0, 3, 3, 0, 2, 2, 1, 1, 4, 4]


# Optimize the answer
def optimize_path(shortest_path):
    i = 0
    while i < len(shortest_path) - 1:
        if shortest_path[i] == shortest_path[i + 1]:
            shortest_path.pop(i)
        else:
            i += 1

    return shortest_path


shortest_path = optimize_path(shortest_path)
print(f'Shortest path: {shortest_path}')  # [0, 3, 0, 2, 1, 4]

# plot the graph with weighted edges
import matplotlib.pyplot as plt
import networkx as nx

graph = nx.Graph()
graph.add_weighted_edges_from(
    [(0, 1, 1), (0, 2, 2), (0, 3, 3), (0, 4, 4), (1, 2, 5), (1, 3, 6), (1, 4, 7), (2, 3, 8), (2, 4, 9), (3, 4, 10)])
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True)
labels = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
plt.show()
