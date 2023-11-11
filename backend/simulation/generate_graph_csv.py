# generate_graph_csv.py

import pandas as pd
import random
import networkx as nx

def generate_lightning_like_graph_csv(file_path, num_nodes, num_edges_per_node):
    # Create a scale-free network using the Barabási-Albert model
    BA_graph = nx.barabasi_albert_graph(num_nodes, num_edges_per_node)

    # Extract edges and convert them to a DataFrame
    edges = [{'source': f"Node_{u}", 'target': f"Node_{v}"} for u, v in BA_graph.edges()]
    df = pd.DataFrame(edges)

    # Save to CSV
    df.to_csv(file_path, index=False)

# Example usage
generate_lightning_like_graph_csv('lightning_like_graph.csv', num_nodes=100, num_edges_per_node=2)
