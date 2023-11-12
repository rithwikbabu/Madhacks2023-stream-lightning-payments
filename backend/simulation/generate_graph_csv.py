# generate_graph_csv.py

import pandas as pd
import random
import networkx as nx
import numpy as np

def generate_lightning_like_graph_csv(file_path, num_nodes, num_edges_per_node):
    # Create a scale-free network using the Barabási-Albert model
    BA_graph = nx.barabasi_albert_graph(num_nodes, num_edges_per_node)

    # Extract edges and convert them to a DataFrame
    edges = []
    for u, v in BA_graph.edges():
        # Generate a capacity (weight) for the edge, skewed towards lower values
        capacity = abs(np.random.exponential(scale=3))  # Using exponential distribution with a scale of 3
        capacity = min(max(capacity, 0.01), 100)  # Ensuring the capacity is between 0.01 and 100
        edges.append({'source': f"Node_{u}", 'target': f"Node_{v}", 'capacity': round(capacity, 4)})

    df = pd.DataFrame(edges)

    # Save to CSV
    df.to_csv(file_path, index=False)

# Example usage
generate_lightning_like_graph_csv('lightning_like_graph_sm.csv', num_nodes=3, num_edges_per_node=2)
