# backend/simulation/graph_simulator.py

from copy import deepcopy
import networkx as nx
import pandas as pd
import random
from networkx.algorithms.flow import edmonds_karp
import pulp


class GraphSimulator:
    def __init__(self):
        self.graph = nx.Graph()
        random.seed(123)

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
            self.graph.add_node(row['source'], rating=row.get(
                'rating', random.uniform(0, 1)))
            self.graph.add_node(row['target'], rating=row.get(
                'rating', random.uniform(0, 1)))
            # Assuming the CSV contains a 'capacity' column for edge weights
            self.graph.add_edge(row['source'], row['target'], weight=row.get(
                'capacity', 1))  # Default capacity to 1 if not specified

    def mcfp_preprocess(self, threshold=.45, limit=.2, aggressiveness=0):
        """
        Solve the Multi-Commodity Flow Problem (MCFP) with ratings.
        Returns a dict of paths and the amount to be sent through each path.
        """
        h = self.graph.copy()

        # List of nodes and edges to be removed
        nodes_to_remove = []

        # Loop through each node
        for node in h.nodes():
            rating = h.nodes[node]['rating']
            # If the rating of the node is below the limit, remove it
            if rating < limit:
                # Mark node for removal
                nodes_to_remove.append(node)

            # If the rating of the node is below the threshold, delete a random edge
            if rating < threshold:
                edges = list(h.edges(node))
                if len(edges) > 1:
                    # Sort the edges by weight
                    edges.sort(key=lambda x: h.edges[x]['weight'])
                    
                    # Filter out weights greater than 3
                    edges = list(filter(lambda x: h.edges[x]['weight'] < aggressiveness, edges))
                    
                    # Remove a random half of the edges    
                    to_remove = random.sample(edges, len(edges)//2)

                    for e in to_remove:
                        h.remove_edge(*e)

        # Remove all marked nodes
        for node in nodes_to_remove:
            h.remove_node(node)

        return h
    
    def multi_commodity_flow_paths(self, commodities, threshold=.45, limit=.2, aggressiveness=0):
        graph = self.mcfp_preprocess(threshold=threshold, limit=limit, aggressiveness=aggressiveness)
        
        ref = graph.copy()
        
        residual_graph = nx.Graph()
        for u, v, data in graph.edges(data=True):
            # Add edge with the capacity as the initial residual
            residual_graph.add_edge(u, v, capacity=data['weight'], flow=0)

        # This will store the paths for all commodities
        all_paths = []

        # Path searching function using BFS for shortest path
        def find_path(residual, source, sink):
            if source not in residual or sink not in residual:
                return None  # If either the source or sink is not in the graph, no path exists.

            visited = {source}
            queue = [(source, [])]
            while queue:
                current, path = queue.pop(0)
                if current == sink:
                    return path
                for neighbor in residual.neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        edge_data = residual[current][neighbor]
                        residual_capacity = edge_data['capacity'] - edge_data['flow']
                        if residual_capacity > 0:
                            queue.append((neighbor, path + [(current, neighbor)]))
            return None

        # Function to update the residual graph with the given path and flow amount
        def update_residual_graph(residual, path, flow_amount):
            for u, v in path:
                residual[u][v]['flow'] += flow_amount

        # Main loop for each commodity
        for commodity in commodities:
            source = commodity['source']
            sink = commodity['sink']
            amount = commodity['amount']
            commodity_paths = []

            # While there is a path with flow to send and the required amount has not been met
            while amount > 0:
                path = find_path(residual_graph, source, sink)
                if not path:
                    # No more paths available, return with the paths found so far
                    break

                # Calculate the minimum residual capacity along the path
                flow_amount = min(amount, min(residual_graph[u][v]['capacity'] - residual_graph[u][v]['flow'] for u, v in path))
                if flow_amount == 0:
                    # No more flow can be sent along this path
                    break

                update_residual_graph(residual_graph, path, flow_amount)

                # Record the path and reduce the amount by the flow amount
                commodity_paths.append(path)
                amount -= flow_amount

            # If we could not satisfy the commodity, return failure
            if amount > 0:
                return False, "Not all commodities can be satisfied.", []

            all_paths.append(commodity_paths)

        # If we reach this point, all commodities have been satisfied
        return True, ref, all_paths

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
                """
        }
        # Return empty options as default
        return options.get(layout_type, "{}")
