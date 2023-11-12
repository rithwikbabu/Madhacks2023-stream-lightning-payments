
import streamlit as st
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.simulation.graph_simulator import GraphSimulator



# Set page configuration
st.set_page_config(
    page_title="BitRoute Optimizer",
    page_icon="⚡",
)

# Page Header
st.write("# Welcome to BitRoute Optimizer! ⚡")

# Sidebar
st.sidebar.success("Explore the features on the left.")

# Adding a toggle switch in the sidebar to enable Hedera's testnet
with st.sidebar:
    hedera_testnet = st.checkbox("Enable Hedera Testnet")
    if hedera_testnet:
        with st.spinner('Waiting for Hedera testnet to initialize account...'):
            simulator = GraphSimulator(use_hedera=True)
            st.session_state['hedera'] = True
            time.sleep(5)
            # This will be displayed when the method errors
            st.success('Connected to the Hedera Testnet')

# Introduction Section
st.markdown(
    """
    ## Enhancing Bitcoin Transactions
    Welcome to Bitcoin Transaction Optimizer, a cutting-edge solution designed to enhance and optimize your Bitcoin transactions. Leveraging advanced algorithms, our software aims to streamline and secure your Bitcoin transactions like never before.

    ### Key Features:
    - **Efficient Pathfinding**: 🛣️ Utilize optimized routes for your Bitcoin transactions.
    - **Enhanced Privacy**: 🔒 Improved transaction routing for enhanced privacy.
    - **Cost-Effective**: 💰 Minimize transaction fees with smart path selection.

    **👈 Explore the features from the sidebar** to see how our software can transform your Bitcoin transaction experience!

    ### Hedera Test Network Implementation:
    In our commitment to simulate and improve our algorithms, we are now implementing a test network on Hedera. This allows us to leverage its hashgraph consensus mechanism for high throughput and secure transactions.

    #### Benefits of Hedera Test Network:
    - **High Throughput**: Enjoy faster transaction processing with Hedera's unique consensus mechanism.
    - **Robust Security**: Test and simulate our algorithms on a network built with security in mind.
    - **Real-World Simulation**: Experience how our algorithm performs in an environment that closely mimics the real-world scenario.

    **🌐 Access our Hedera test network simulation** from the sidebar and witness the potential improvements in real-time.

    ### Learn More:
    - Dive into our [Documentation](AI) for technical details.
    - Engage with our custom AI assistant for support and discussions.

    ### Demonstrations:
    - See our software in action [Here](Visualizer).

    ### Get Started:
    Ready to optimize your Bitcoin transactions? [Create a node](Node) to get started or explore the demo versions in the sidebar.
    """
)

# Video or Animation (Placeholder for actual video or animation link)
st.video("frontend/static/demo.mov")

# Footer
st.markdown("---")
st.markdown(
    "© 2023 Bitcoin Transaction Optimizer - Enhancing your Bitcoin experience.")
