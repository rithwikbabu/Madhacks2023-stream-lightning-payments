# frontend/app.py
import networkx as nx
from backend.simulation.graph_simulator import GraphSimulator
from matplotlib import colormaps as cm
import matplotlib.colors as mcolors
from pyvis.network import Network
import streamlit as st

def create_network_visualization(graph_data, layout_options, transaction_paths=None):
    net = Network(height="750px", width="750px",
                  bgcolor="#0e1117", font_color="white")
    net.toggle_physics(True)

    # Apply the layout options to the Pyvis network
    net.set_options(layout_options)

    # Create a color map from green to red
    green_to_red = cm.get_cmap('RdYlGn_r')  # Reverse Red-Yellow-Green colormap
    red_to_green = cm.get_cmap('RdYlGn')  # Reverse Red-Yellow-Green colormap

    # Find the maximum weight for normalization
    max_weight = max([link.get('weight', 1) for link in graph_data['links']])

    # Add nodes to the network
    for node in graph_data['nodes']:
        node_color = mcolors.to_hex(red_to_green(node['rating']))
        net.add_node(node['id'], label=node.get('label', ''),
                     title=node.get('title', ''), color=node_color)

    # Flatten the transaction paths for easy edge checking
    transaction_paths = transaction_paths or []

    transaction_edges = set()
    for transaction in transaction_paths:
        for path in transaction:
            for edge in path:
                transaction_edges.add(edge)

    print(transaction_edges)

    # Add edges to the network with varying color based on capacity
    for link in graph_data['links']:
        weight = link.get('weight', 1)
        norm_weight = weight / max_weight  # Normalize weight
        # Convert normalized weight to hex color
        hex_color = mcolors.to_hex(green_to_red(norm_weight))

        # Check if the edge is part of the transaction path
        is_in_path = (link['source'], link['target']) in transaction_edges or (
            link['target'], link['source']) in transaction_edges

        width = 15 if is_in_path else 2  # Double the width if part of the transaction path
        # Color transaction path differently
        color = 'pink' if is_in_path else hex_color

        net.add_edge(link['source'], link['target'], color=color, width=width)

    # Return HTML of the network
    network_html = net.generate_html()

    return network_html


def main():
    st.title("Lightning Network Graph Simulator")

    # Initialize the graph simulator
    simulator = GraphSimulator()
    layout_options = simulator.get_pyvis_options("force_atlas")
    simulator.import_graph_from_csv('lightning_like_graph_md.csv')

    # Input fields for source, sink, and transaction amount
    source = st.sidebar.text_input("Source Node", value="Node_1")
    sink = st.sidebar.text_input("Sink Node", value="Node_2")
    amount = st.sidebar.number_input(
        "Transaction Amount", min_value=0.01, max_value=100.0, value=1.0)

    # Get graph data and visualize
    graph_data = simulator.get_graph_data()

    # Button to find paths
    transaction_paths = None
    if st.sidebar.button("Find Optimal Paths"):
        threshold = 0.5
        limit = 0.2
        # Define your commodities
        commodities = [{'source': source, 'sink': sink, 'amount': amount}]

        success, h, transaction_paths = simulator.multi_commodity_flow_paths(
            commodities, threshold, limit, aggresiveness=3)
        graph_data = nx.node_link_data(h)

        if transaction_paths:
            st.write("Optimal Paths:", transaction_paths)
        else:
            st.write("No viable paths found or not enough capacity.")

    graph_html = create_network_visualization(
        graph_data, layout_options, transaction_paths)

    bg = "<style>:root {background-color: #0e1117; margin: 0px; padding: 0px;}</style>"

    st.components.v1.html(bg + graph_html, height=770, width=752)


if __name__ == "__main__":
    main()
