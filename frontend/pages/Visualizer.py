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
                     title=node.get('title', str(round(node['rating']*100, 2)) + "%"), color=node_color)

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

st.title("BitRoute Network Graph Simulator")

# Initialize the graph simulator
simulator = GraphSimulator()
layout_options = simulator.get_pyvis_options("force_atlas")
simulator.import_graph_from_csv('lightning_like_graph_md.csv')

# Simplified input for source, sink, and amount
input_string = st.text_input("Enter source, sink, and amount separated by commas (e.g., source,sink,amount;source,sink,amount)")
split_input = input_string.split(';')

commodities = []
for transaction in split_input:
    parsed_input = transaction.split(',')
    
    if len(parsed_input) == 3:
        source, sink, amount = parsed_input[0].strip(), parsed_input[1].strip(), float(parsed_input[2].strip())
        commodities.append({'source': source, 'sink': sink, 'amount': amount})
    
    # Fixed values for threshold, limit, and aggressiveness for this example
    threshold = 0.45
    limit = 0.2
    aggressiveness = 0
    
# Button to find paths
if st.button("Find Paths"):
    success, h, transaction_paths = simulator.multi_commodity_flow_paths(
        commodities, threshold, limit, aggressiveness)
    
    if not success:
        st.write("No viable paths found or not enough capacity.")
    else:
        graph_data = nx.node_link_data(h)
        graph_html = create_network_visualization(graph_data, layout_options, transaction_paths)
        bg = "<style>:root {background-color: #0e1117; margin: 0px; padding: 0px;}</style>"

        st.components.v1.html(bg + graph_html, height=770, width=752)
else:
    st.write("Please enter the source, sink, and amount correctly.")