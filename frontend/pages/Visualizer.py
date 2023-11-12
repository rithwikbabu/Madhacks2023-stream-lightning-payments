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

st.title("Lightning Network Graph Simulator")

# Initialize the graph simulator
simulator = GraphSimulator()
layout_options = simulator.get_pyvis_options("force_atlas")
simulator.import_graph_from_csv('lightning_like_graph_md.csv')

# Use session state variables as default values if they exist
user_address = st.session_state.get('user_address', '')
recipient_address = st.session_state.get('recipient_address', '')
amount = st.session_state.get('amount', 1.0)
threshold = st.session_state.get('threshold', 0.5)
limit = st.session_state.get('limit', 0.2)
aggressiveness = st.session_state.get('aggressiveness', 3)

# Flag to determine if the paths are found
paths_found = False

# If the button is not pressed, show the inputs
if 'button_pressed' not in st.session_state:
    user_address = st.text_input("Your Address", value=user_address)
    recipient_address = st.text_input("Recipient Address", value=recipient_address)
    amount = st.number_input("Transaction Amount", min_value=0.01, max_value=100.0, value=amount)
    threshold = st.slider("Threshold", 0.0, 1.0, threshold, 0.01)
    limit = st.slider("Limit", 0.0, 1.0, limit, 0.01)
    aggressiveness = st.slider("Aggressiveness", 0, 5, aggressiveness)

    # Button to find paths
    if st.button("Find Paths"):
        st.session_state['button_pressed'] = True
else:
    # Define your commodities
    commodities = [{'source': user_address, 'sink': recipient_address, 'amount': amount}]

    success, h, transaction_paths = simulator.multi_commodity_flow_paths(
        commodities, threshold, limit, aggressiveness)

    if not success:
        st.write("No viable paths found or not enough capacity.")
        if st.button("Reset"):
            del st.session_state['button_pressed']
    else:
        graph_data = nx.node_link_data(h)
        
        graph_html = create_network_visualization(
            graph_data, layout_options, transaction_paths)
        
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("Reset"):
                del st.session_state['button_pressed']

        with col2:
            if st.button("Default"):
                graph_html = create_network_visualization(
                    simulator.get_graph_data(), layout_options)

        with col3:
            if st.button("Preprocessing"):
                graph_html = create_network_visualization(
                    graph_data, layout_options)

        with col4:
            if st.button("Routing"):
                graph_html = create_network_visualization(
                    graph_data, layout_options, transaction_paths)

        with col5:
            if st.button("Final"):
                graph_html = create_network_visualization(
                    simulator.get_graph_data(), layout_options, transaction_paths)

        bg = "<style>:root {background-color: #0e1117; margin: 0px; padding: 0px;}</style>"

        st.components.v1.html(bg + graph_html, height=770, width=752)