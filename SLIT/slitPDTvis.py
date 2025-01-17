import streamlit as st
from pyvis.network import Network

# Create a Pyvis network
net = Network(height="750px", width="100%", directed=True)

# Add nodes and edges
net.add_node("Project A", label="Project A", color="#007BFF")
net.add_node("Deliverable 1", label="Deliverable 1", color="#28A745")
net.add_node("Deliverable 2", label="Deliverable 2", color="#28A745")
net.add_node("Task 1", label="Task 1", color="#FFC107")
net.add_node("Task 2", label="Task 2", color="#FFC107")
net.add_node("Release 1", label="Release 1", color="#DC3545")

# Define relationships
net.add_edge("Project A", "Deliverable 1")
net.add_edge("Project A", "Deliverable 2")
net.add_edge("Deliverable 1", "Task 1")
net.add_edge("Deliverable 2", "Task 2")
net.add_edge("Release 1", "Task 1")
net.add_edge("Release 1", "Task 2")

# Save and display the network
net.save_graph("network.html")
st.components.v1.html(open("network.html", "r").read(), height=750)
