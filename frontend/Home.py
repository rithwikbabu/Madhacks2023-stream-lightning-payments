import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


# Set page configuration
st.set_page_config(
    page_title="BitRoute Optimizer",
    page_icon="⚡",
)

# Page Header
st.write("# Welcome to BitRoute Optimizer! ⚡")

# Sidebar
st.sidebar.success("Explore the features on the left.")

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
st.video("https://www.example.com/path_to_video.mp4")

# Footer
st.markdown("---")
st.markdown("© 2023 Bitcoin Transaction Optimizer - Enhancing your Bitcoin experience.")
