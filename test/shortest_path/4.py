import math

import numpy as np
import pandas as pd

# show all columns
pd.set_option('display.max_columns', None)


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

    # # print mappping
    # for i in range(new_n):
    #     print(i, ":", i % n, end="\t")
    return new_matrix

def optimize_path(shortest_path, start_node_index, end_node_index, df):
    print("\nOptimizing path...")
    print(shortest_path)
    print(start_node_index, end_node_index)

    # Step 1: Remove duplicated indices
    i = 0
    while i < len(shortest_path) - 1:
        if shortest_path[i] == shortest_path[i + 1]:
            shortest_path.pop(i)
        else:
            i += 1

    # Step 2: Remove cycles
    node_indices = {}  # Dictionary to keep track of the index at which each node is first encountered
    for i, node in enumerate(shortest_path):
        if node in node_indices:
            # Cycle detected from node_indices[node] to i
            # Remove the cycle by keeping the part of the path before the cycle
            shortest_path = shortest_path[:node_indices[node] + 1] + shortest_path[i + 1:]
            node_indices = {node: index for index, node in enumerate(shortest_path)}  # Update node_indices
        else:
            node_indices[node] = i  # No cycle detected, update node_indices

    # Ensure the optimized path starts and ends with the correct nodes
    if shortest_path[0] != start_node_index:
        shortest_path.insert(0, start_node_index)
    if shortest_path[-1] != end_node_index:
        shortest_path.append(end_node_index)

    return shortest_path


# Optimize the answer
# def optimize_path(shortest_path, start_node_index, end_node_index, df):
#     # print("\nOptimizing path...")
#     # print(shortest_path)
#     # print(start_node_index, end_node_index)
#     # # print(df)
#     #
#     # # Convert node indices to node IDs
#     # shortest_path_ids = [df.iloc[node_index % (len(df))]['_id'] for node_index in shortest_path]
#     #
#     # # Find the first occurrence of the start_node_id and the last occurrence of the end_node_id
#     # start_index = shortest_path_ids.index(df.iloc[start_node_index]['_id'])
#     # end_index = len(shortest_path_ids) - 1 - shortest_path_ids[::-1].index(df.iloc[end_node_index]['_id'])
#     #
#     # # Slice the path to only include nodes between the start and end nodes, inclusive
#     # optimized_path_ids = shortest_path_ids[start_index:end_index + 1]
#     #
#     # return optimized_path_ids
#     i = 0
#     while i < len(shortest_path) - 1:
#         if shortest_path[i] == shortest_path[i + 1]:
#             shortest_path.pop(i)
#         else:
#             i += 1
#
#     # # break the cycle at current location and destination
#     # current_index = shortest_path.index(start_id)
#     # destination_index = shortest_path.index(end_id)
#     # shortest_path = shortest_path[current_index:destination_index + 1]
#
#     return shortest_path

def find_shortest_path(adj_matrix, start_node_id, end_node_id, df):
    start_node_index = df[df['_id'] == start_node_id].index[0]
    end_node_index = df[df['_id'] == end_node_id].index[0]
    print(start_node_index, end_node_index)

    # Duplicate each node 2 times
    copies = 2
    new_adj_matrix = duplicate_nodes(adj_matrix, copies)

    new_start = start_node_index
    new_end = end_node_index + len(adj_matrix)

    print(new_start, new_end)

    # Solve TSP on the new graph
    shortest_path_length, shortest_path = tsp(new_adj_matrix, new_start, new_end)

    print(shortest_path_length, shortest_path)

    # Adjust the node indices in the path to reflect the original node indices
    n = len(adj_matrix)
    shortest_path = [node % n for node in shortest_path]

    shortest_path = optimize_path(shortest_path, start_node_index, end_node_index, df)

    print(df)
    # by dataframe index sort the df
    df = df.reindex(shortest_path)
    df = df.reset_index()
    print(df)

    return shortest_path_length, shortest_path, df


def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371000  # Radius of the Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # kilometers
    return (r * c) / 1000


def create_adjacency_matrix(df):
    num_nodes = len(df)
    adj_matrix = np.zeros((num_nodes, num_nodes))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:  # No need to calculate distance from a node to itself
                adj_matrix[i][j] = haversine_distance(df.iloc[i]['latitude'], df.iloc[i]['longitude'],
                                                      df.iloc[j]['latitude'], df.iloc[j]['longitude'])
            else:
                adj_matrix[i][j] = 0  # Set distance from a node to itself as zero

    return adj_matrix


df = pd.read_csv("test_2.csv")

start_node_id = "652b9d229c8deef2485bf8ea" # Independence Square
end_node_id = "652b9d229c8deef2485bf8e9" # Rideekanda Forest Monastery

# Usage
adj_matrix = create_adjacency_matrix(df)
shortest_path_length, shortest_path, df = find_shortest_path(adj_matrix, start_node_id, end_node_id, df)
print(f'Shortest path: {shortest_path}')  # [0, 3, 0, 2, 1, 4]
print(f'Shortest path length: {shortest_path_length}')
