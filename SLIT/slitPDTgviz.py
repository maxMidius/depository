import streamlit as st
from graphviz import Digraph

# Create a directed graph
dot = Digraph()

# Add nodes
dot.node("P", "Project A")
dot.node("D1", "Deliverable 1")
dot.node("D2", "Deliverable 2")
dot.node("T1", "Task 1")
dot.node("T2", "Task 2")
dot.node("R1", "Release 1")

# Add edges
dot.edges([("P", "D1"), ("P", "D2"), ("D1", "T1"), ("D2", "T2"), ("R1", "T1"), ("R1", "T2")])

# Render the graph in Streamlit
st.graphviz_chart(dot)
