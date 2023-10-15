import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from itertools import combinations
from geopy.distance import geodesic

# Load Data
df = pd.read_csv("data/m_locations_sp.csv")


# df = pd.read_csv("data/m_locations.csv")


# Calculate Distances
def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).km


# Generate Graph
def generate_graph(current_location, df):
    # Step 1: Add current location to df
    df = pd.concat([df, pd.DataFrame([[0, 'Current Location', current_location[0], current_location[1]]],
                                     columns=['_id', 'name', 'latitude', 'longitude'])], ignore_index=True)

    # Step 3: Generate Graph
    G = nx.Graph()

    # Add nodes
    for _, row in df.iterrows():
        G.add_node(row['_id'], name=row['name'], latitude=row['latitude'], longitude=row['longitude'])

    # Add edges (fully connected)
    locations = list(df['_id'])
    for node1, node2 in combinations(locations, 2):
        lat1, lon1 = G.nodes[node1]['latitude'], G.nodes[node1]['longitude']
        lat2, lon2 = G.nodes[node2]['latitude'], G.nodes[node2]['longitude']
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        G.add_edge(node1, node2, weight=distance)

    hamiltonian_cycle = nx.approximation.traveling_salesman_problem(G, cycle=True)

    # # Find the indices of the current location and destination
    # current_index = hamiltonian_cycle.index(0)
    # destination_index = hamiltonian_cycle.index(destination_id)

    # if neibouring nodes are same remove one
    hamiltonian_cycle = [x for x, y in zip(hamiltonian_cycle, hamiltonian_cycle[1:] + hamiltonian_cycle[:1]) if x != y]

    # break the cycle at current location and destination
    # hamiltonian_cycle_between_current_and_destination = hamiltonian_cycle[current_index:destination_index+1]
    # print(hamiltonian_cycle[current_index:])
    # print(hamiltonian_cycle[:current_index+1])

    # Reorder the Hamiltonian cycle starting from current location and ending at destination
    # hamiltonian_cycle = hamiltonian_cycle[current_index:] + hamiltonian_cycle[:current_index+1]

    # remove duplicate nodes in the cycle
    # hamiltonian_cycle = list(dict.fromkeys(hamiltonian_cycle))
    # remove last node if it is already in the cycle
    if hamiltonian_cycle[-1] == hamiltonian_cycle[0]:
        hamiltonian_cycle.pop()

    # print(hamiltonian_cycle)

    return G, hamiltonian_cycle


def plot_hamiltonian_cycle(G, hamiltonian_cycle):
    # Create a subgraph with only the nodes and edges in the Hamiltonian cycle
    hamiltonian_subgraph = nx.Graph()
    hamiltonian_subgraph.add_nodes_from(hamiltonian_cycle)
    hamiltonian_edges = [(hamiltonian_cycle[i], hamiltonian_cycle[i + 1]) for i in range(len(hamiltonian_cycle) - 1)]
    hamiltonian_edges.append((hamiltonian_cycle[-1], hamiltonian_cycle[0]))  # Complete the cycle
    hamiltonian_subgraph.add_edges_from(hamiltonian_edges)

    # Draw the original graph
    pos = nx.spring_layout(G)  # You can use a different layout if you prefer
    nx.draw(G, pos, with_labels=True, font_weight='bold')

    # Draw the Hamiltonian cycle
    nx.draw(hamiltonian_subgraph, pos, edge_color='r', width=2, node_color='r', node_size=500)

    # # Add labels for the Hamiltonian cycle edges
    # labels = {(u, v): G[u][v]['weight'] for u, v in hamiltonian_edges}
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Show the plot
    plt.show()


# current_location = (6.9271, 79.8612)
# # destination_id = 17  # Replace with the actual ID from df
# G, hamiltonian_cycle = generate_graph(current_location, df)
# # plot_hamiltonian_cycle(G, hamiltonian_cycle)
#
# print(hamiltonian_cycle)
