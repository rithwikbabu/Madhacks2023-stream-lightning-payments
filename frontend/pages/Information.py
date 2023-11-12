import streamlit as st

# Set Streamlit page configuration
st.set_page_config(
   page_title="BitRoute Optimizer",
   page_icon="⚡",
   layout="wide",
)

# Main header
st.markdown("# Welcome to BitRoute Optimizer! ⚡")
st.markdown("### Enhancing Bitcoin Transactions")

# Introduction text
st.markdown("""
BitRoute Transaction Optimizer is your advanced tool for optimized Bitcoin transactions. By leveraging the Hedera Hashgraph technology on the test network, we ensure unparalleled efficiency and security.
""")

# Key Features section
st.markdown("#### Key Features:")
st.markdown("""
- **Efficient Pathfinding:** 🛣️ Optimize routes for Bitcoin transactions.
- **Enhanced Privacy:** 🔒 Advanced transaction routing for privacy.
- **Cost-Effective:** 💰 Minimize fees with intelligent path selection.
""")

# Learn More section
st.markdown("#### Learn More:")
st.markdown("""
- **Documentation:** Delve into our documentation for technical details.
- **AI Assistant:** Engage with our AI for support and discussions.
""")

# Algorithm Explanation
st.markdown("---")
st.markdown("## THE ALGORITHM")
st.markdown("""
Our backend, powered by `graph_simulator.py`, employs `networkx` and `hedera` for graph and blockchain interactions respectively.

**Highlights:**
- **Hedera Test Network Integration:** Provides a safe and cost-effective environment for transaction simulations.
- **Graph-Based Simulations:** Facilitates realistic transaction pathfinding using the Hedera cryptocurrency API.

**Caveats:**
- Blockchain operations are dependent on test network availability and may have different performance metrics compared to the mainnet.
""")

# Hedera Implementation
st.markdown("---")
st.markdown("## Hedera Implementation")
st.markdown("""
Our software utilizes the Hedera test network to simulate real-world transactions with the Hedera cryptocurrency API.

**Hedera Test Network Features:**
- Access to a pre-configured environment for development and testing.
- Simulated account creation and HBAR transfers to test transactions without real-world costs.
- Real-time feedback on transaction status and performance for optimization.

**Note:** Transactions on the Hedera test network use test HBARs and have no real-world value, allowing for risk-free testing.
""")

# Verbal Runtime Analysis
st.markdown("---")
st.markdown("## Runtime Analysis")
st.markdown("""
While actual performance metrics are subject to several factors, indicative analysis on the Hedera test network is as follows:

- **Initialization:** Sub-second setup for the Hedera client.
- **Account Creation:** Ranges between 100-200ms on the Hedera test network.
- **Transaction Execution:** Typically takes 500-1000ms, depending on network conditions and transaction complexity.

These metrics are illustrative for the Hedera test network and may vary based on actual network conditions.
""")
