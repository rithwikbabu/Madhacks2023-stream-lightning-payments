# backend/simulation/graph_simulator.py

import networkx as nx
import pandas as pd
import random

from hedera import (
    AccountId,
    PrivateKey,
    Client,
    TransferTransaction,
    Hbar
)

class GraphSimulator:
    def __init__(self, use_hedera=False):
        self.graph = nx.Graph()
        self.use_hedera = use_hedera
        random.seed(123)
        self.hedera_accounts = {}

        # Initialize the Hedera client only if Hedera mode is enabled
        if self.use_hedera:
            self.client = Client.forTestnet()
            self.client.setOperator(AccountId(0, 0, 1), PrivateKey.generate())

    def add_node(self, node_id, **attrs):
        # Initialize transactions data for the node
        self.graph.add_node(node_id, **attrs)
        if self.use_hedera:
            hedera_account_id = attrs.get('hedera_account_id', None)
            if hedera_account_id:
                self.hedera_accounts[node_id] = hedera_account_id

    def add_channel(self, sender_id, receiver_id, amount):
        if self.use_hedera:
            # Convert the account strings to AccountId objects
            sender_account_id = AccountId.fromString(sender_id)
            receiver_account_id = AccountId.fromString(receiver_id)
            sender_private_key = PrivateKey.fromString(
                self.graph.nodes[sender_id]['private_key'])

            # Create the transfer transaction
            transfer_transaction = TransferTransaction().addHbarTransfer(sender_account_id,
                                                                         Hbar.fromTinybars(-amount)).addHbarTransfer(receiver_account_id, Hbar.fromTinybars(amount))

            # Freeze the transaction to prepare it for signing
            frozen_transaction = transfer_transaction.freezeWith(self.client)

            # Sign the transaction with the sender's private key
            signed_transaction = frozen_transaction.sign(sender_private_key)

            # Execute the signed transaction
            response = signed_transaction.execute(self.client)

            # Fetch the receipt of the transaction
            receipt = response.getReceipt(self.client)

            status = receipt.status.toString()
        else:
            # Regular network simulation logic
            self.graph.add_edge(sender_id, receiver_id, weight=amount)
            status = "SUCCESS"

        return status

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
                    edges = list(
                        filter(lambda x: h.edges[x]['weight'] < aggressiveness, edges))

                    # Remove a random half of the edges
                    to_remove = random.sample(edges, len(edges)//2)

                    for e in to_remove:
                        h.remove_edge(*e)

        # Remove all marked nodes
        for node in nodes_to_remove:
            h.remove_node(node)

        return h

    def multi_commodity_flow_paths(self, commodities, threshold=.45, limit=.2, aggressiveness=0):
        graph = self.mcfp_preprocess(
            threshold=threshold, limit=limit, aggressiveness=aggressiveness)

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
                # If either the source or sink is not in the graph, no path exists.
                return None

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
                        residual_capacity = edge_data['capacity'] - \
                            edge_data['flow']
                        if residual_capacity > 0:
                            queue.append(
                                (neighbor, path + [(current, neighbor)]))
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
                try:
                    path = find_path(residual_graph, source, sink)
                    if not path:
                        # No more paths available, return with the paths found so far
                        break

                    # Calculate the minimum residual capacity along the path
                    flow_amount = min(amount, min(
                        residual_graph[u][v]['capacity'] - residual_graph[u][v]['flow'] for u, v in path))
                    if flow_amount == 0:
                        # No more flow can be sent along this path
                        break

                    update_residual_graph(residual_graph, path, flow_amount)

                    # Record the path and reduce the amount by the flow amount
                except Exception as e:
                    u, v = path
                    self.graph.nodes[u]['rating'] *= 0.95
                    break
                commodity_paths.append(path)
                amount -= flow_amount

            # If we could not satisfy the commodity, return failure
            if amount > 0:
                return False, "Not all commodities can be satisfied.", []

            self.update_graph_with_paths(commodity_paths)

            all_paths.append(commodity_paths)

        # If we reach this point, all commodities have been satisfied
        return True, ref, all_paths

    # Given a list of paths, update the graph with the transactions
    def update_graph_with_paths(self, paths):
        for path in paths:
            for u, v in path:
                self.graph.nodes[u]['rating'] *= 1.05

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


# graph_sim = GraphSimulator(use_hedera=True)
# graph_sim.add_node('0.0.5872534', private_key="0xb82daf0cc68f29b4be4df0ed2d62f440162d7095db4ab41007e4d7bc9af1da92",
#                    hedera_account_id='0.0.5872534')
# graph_sim.add_node('0.0.5870650', private_key="0xf57021da27b225cabe7b2e73d2f301915e670865be9c530fd80d8c9ed6c214c0",
#                    hedera_account_id='0.0.5870650')
# status = graph_sim.add_channel('0.0.5872534', '0.0.5870650', 10)
# print(status)

# graph_sim_no_hedera = GraphSimulator()
# graph_sim_no_hedera.add_node('node1')
# graph_sim_no_hedera.add_node('node2')
# status_no_hedera = graph_sim_no_hedera.add_channel('node1', 'node2', 100)
# print(status_no_hedera)
