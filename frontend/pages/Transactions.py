import time
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from backend.simulation.graph_simulator import GraphSimulator

st.set_page_config(
    page_title="BitRoute Transact",
    page_icon="⚡",
)

st.title("💸 Make a BitRoute Transaction 💸")

# Initialize session state variables if not already set
if 'user_address' not in st.session_state:
    st.session_state['user_address'] = ""
if 'recipient_address' not in st.session_state:
    st.session_state['recipient_address'] = ""

# Transaction Inputs
user_address = st.text_input("Your Address", value=st.session_state['user_address'])
recipient_address = st.text_input("Recipient Address", value=st.session_state['recipient_address'])
amount = st.number_input("Transaction Amount", min_value=0.01, max_value=100.0, value=1.0)

# Sliders for Threshold, Limit, and Aggressiveness
threshold = st.slider("Threshold", 0.0, 1.0, 0.45, 0.01)
limit = st.slider("Limit", 0.0, 1.0, 0.2, 0.01)
aggressiveness = st.slider("Aggressiveness", 0, 5, 0)

# Process Transaction Button
if st.button("Process Transaction"):
    # Store addresses in session state
    st.session_state['user_address'] = user_address
    st.session_state['recipient_address'] = recipient_address
    
    simulator = GraphSimulator()
    simulator.import_graph_from_csv('lightning_like_graph_md.csv')
    
    commodities = [{'source': user_address, 'sink': recipient_address, 'amount': amount}]
    success, graph, paths = simulator.multi_commodity_flow_paths(commodities, threshold, limit, aggressiveness)
    
    if success:
        placeholder = st.empty()  # Create a placeholder outside the loop
        placeholder.write("Calculating optimal routes...")
        time.sleep(1)  # Delay for a second
        route_string = f"Route: {user_address}"
        placeholder.success(route_string)
        for i, path in enumerate(paths[0][0], start=1):
            route_string += f" → {path[1]}"
            time.sleep(.8)  # Delay for a second
            placeholder.success(route_string)
        time.sleep(2)
        placeholder.success(f"{route_string}  🚀")
        st.balloons()  # Release balloons on successful completion
        
        if st.button("Go to Visualizer"):
            # Update session state with current addresses
            st.session_state['user_address'] = user_address
            st.session_state['recipient_address'] = recipient_address
            st.session_state['amount'] = amount
            st.session_state['threshold'] = threshold
            st.session_state['limit'] = limit
            st.session_state['aggressiveness'] = aggressiveness
            
            
            # Redirect to the visualizer page
            switch_page("Visualizer")
    else:
        st.error(f"Transaction Failed!: No path found between {user_address} and {recipient_address}")