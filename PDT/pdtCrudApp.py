import streamlit as st
from streamlit_flow import streamlit_flow
# Create a new Flow instance
flow = Flow()

# Define the nodes
project_node = flow.add_node("Project")
deliverable_node = flow.add_node("Deliverable")
task_node = flow.add_node("Task")

# Define the edges
flow.add_edge(project_node, deliverable_node)
flow.add_edge(deliverable_node, task_node)

# Create a Streamlit app
st.title("Project Management App")

# Display the Flow instance
st.write(flow)

# Add interactive buttons to add/delete nodes
if st.button("Add Project"):
    new_project_node = flow.add_node("New Project")
    flow.add_edge(new_project_node, deliverable_node)

if st.button("Add Deliverable"):
    new_deliverable_node = flow.add_node("New Deliverable")
    flow.add_edge(project_node, new_deliverable_node)

if st.button("Add Task"):
    new_task_node = flow.add_node("New Task")
    flow.add_edge(deliverable_node, new_task_node)

if st.button("Delete Node"):
    node_to_delete = st.selectbox("Select node to delete", flow.nodes)
    flow.delete_node(node_to_delete)