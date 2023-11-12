import streamlit as st
from pathlib import Path
import sys

from backend.simulation.graph_simulator import GraphSimulator

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Set page configuration
st.set_page_config(
    page_title="Node Manager",
    page_icon="🌐",
    layout="wide"
)

# Page Header
st.title("Node Manager for Graph Network 🌐")

# Introduction Section
st.markdown(
    """
    ## Add a New Node to the Network
    Use this page to add new nodes to your graph network. You can also choose to add your node to the public ledger for transparency and data integrity.
    """
)

# Sidebar
st.sidebar.header("Node Manager")
st.sidebar.info("Use the form to add nodes to your graph.")

# Node Addition Form
with st.form("node_addition_form", clear_on_submit=True):
    st.subheader("Add Node Form")
    node_id = st.text_input("Node ID", help="Enter a unique identifier for the node.")
    node_attrs = st.text_area("Node Attributes (JSON Format)", help="Enter the node attributes in JSON format.")
    add_to_public_ledger = st.checkbox("Add to Public Ledger", value=False, help="Check to add this node to the public ledger.")
    submit_button = st.form_submit_button("Add Node")

    if submit_button and node_id:
        simulator = GraphSimulator()
        simulator.add_node(node_id, node_attrs)
        
        # TODO: add public ledger option
        
        st.success(f"Node {node_id} added successfully!")

# Public Ledger Option
if add_to_public_ledger:
    st.markdown(
        """
        ### Public Ledger
        Your node will be added to the public ledger, enhancing the transparency and security of the network.
        """
    )

# Footer
st.markdown("---")
st.caption("© 2023 Node Manager - Manage your graph network efficiently.")
