# frontend/app.py

import streamlit as st
from pyvis.network import Network

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.simulation.graph_simulator import GraphSimulator

def create_network_visualization(graph_data, layout_options, transaction_path=None):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    net.toggle_physics(True)

    # Apply the layout options to the Pyvis network
    net.set_options(layout_options)

    # Add nodes and edges to the network
    for node in graph_data['nodes']:
        node_color = 'green' if transaction_path and node['id'] in transaction_path else 'white'
        net.add_node(node['id'], label=node.get('label', ''), title=node.get('title', ''), color=node_color)

    for link in graph_data['links']:
        if transaction_path and link['source'] in transaction_path and link['target'] in transaction_path:
            # Highlight the path of the transaction
            net.add_edge(link['source'], link['target'], color='green', width=10)
        else:
            net.add_edge(link['source'], link['target'])

    # Return HTML of the network
    return net.generate_html()


def main():
    st.title("Lightning Network Graph Simulator")

    # Initialize the graph simulator
    simulator = GraphSimulator()

    # Add a selector in the sidebar for layout options
    layout_type = st.sidebar.selectbox("Select Layout Type", 
                                       options=["force_atlas", "barnes_hut", "hierarchical, static"], 
                                       index=0)

    # Get the selected layout options from the simulator
    layout_options = simulator.get_pyvis_options(layout_type)
    
    # Add nodes and channels for demonstration
    simulator.import_graph_from_csv('lightning_like_graph.csv')
    simulator.get_pyvis_options('force_atlas')

    # Define a transaction path (e.g., from A to C via B)
    transaction_path = ['Node_1', 'Node_81', 'Node_12', 'Node_41', 'Node_84']

    # Get graph data and visualize
    graph_data = simulator.get_graph_data()
    graph_html = create_network_visualization(graph_data, layout_options, transaction_path)
    st.components.v1.html(graph_html, height=800)

if __name__ == "__main__":
    main()