# Example adjacency matrix for a graph with 5 nodes
# The value at matrix[i][j] represents the distance from node i to node j
adj_matrix = [
    [0, 1, 2, 3, 4],
    [1, 0, 5, 6, 7],
    [2, 5, 0, 8, 9],
    [3, 6, 8, 0, 10],
    [4, 7, 9, 10, 0]
]


def tsp(adj_matrix, start, end):
    n = len(adj_matrix)
    # memoization table
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1 << start][start] = 0
    # predecessor table
    pred = [[-1] * n for _ in range(1 << n)]

    for mask in range(1, 1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue

            for v in range(n):
                if mask & (1 << v) and adj_matrix[v][u] != -1:
                    if dp[mask][u] > dp[mask ^ (1 << u)][v] + adj_matrix[v][u]:
                        dp[mask][u] = dp[mask ^ (1 << u)][v] + adj_matrix[v][u]
                        pred[mask][u] = v  # store the predecessor of u

    # Reconstruct the path from the predecessor table
    mask = (1 << n) - 1  # All cities have been visited
    u = end
    path = []

    while u != -1:
        path.append(u)
        v = pred[mask][u]
        mask = mask ^ (1 << u)  # remove u from the visited set
        u = v  # move to the predecessor

    path.reverse()  # reverse the path to get the correct order from start to end
    return dp[(1 << n) - 1][end], path  # return the shortest path length and the path itself


# Usage
shortest_path_length, shortest_path = tsp(adj_matrix, 0, 2)  # Assuming start node is 0 and end node is 4
print(f'Shortest path length: {shortest_path_length}')
print(f'Shortest path: {shortest_path}')

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
