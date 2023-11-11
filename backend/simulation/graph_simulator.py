# backend/simulation/graph_simulator.py

import networkx as nx
import pandas as pd

class GraphSimulator:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node_id, **attrs):
        self.graph.add_node(node_id, **attrs)

    def add_channel(self, node1, node2, capacity):
        # Adding the capacity as a weight attribute
        self.graph.add_edge(node1, node2, weight=capacity)

    def get_graph_data(self):
        # Converts the graph to a format suitable for visualization
        # including the edge weights (capacities)
        return nx.node_link_data(self.graph)

    def import_graph_from_csv(self, file_path):
        # Read CSV file
        df = pd.read_csv(file_path)

        # Add nodes and edges from CSV
        for _, row in df.iterrows():
            self.graph.add_node(row['source'])
            self.graph.add_node(row['target'])
            # Assuming the CSV contains a 'capacity' column for edge weights
            self.graph.add_edge(row['source'], row['target'], weight=row.get('capacity', 1))  # Default capacity to 1 if not specified


    def get_pyvis_options(self, layout_type):
        # Return different Pyvis options based on the layout_type
        options = {
            'force_atlas': """
                {
                  "physics": {
                    "forceAtlas2Based": {
                      "gravitationalConstant": -50,
                      "centralGravity": 0.01,
                      "springLength": 100,
                      "springConstant": 0.08
                    },
                    "maxVelocity": 50,
                    "solver": "forceAtlas2Based",
                    "timestep": 0.35,
                    "stabilization": { "iterations": 150 }
                  }
                }
                """,
            'barnes_hut': """
                {
                  "physics": {
                    "barnesHut": {
                      "gravitationalConstant": -8000,
                      "springLength": 200,
                      "springConstant": 0.04,
                      "damping": 0.09
                    }
                  }
                }
                """,
            'hierarchical': """
                {
                  "layout": {
                    "hierarchical": {
                      "enabled": true,
                      "levelSeparation": 150,
                      "nodeSpacing": 100,
                      "treeSpacing": 200
                    }
                  }
                }
                """,
            'static': """
                {
                  "physics": {
                    "enabled": false
                  }
                }
                """
        }
        return options.get(layout_type, "{}")  # Return empty options as default
