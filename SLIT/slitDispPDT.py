import streamlit as st
import networkx as nx
from pyvis.network import Network

def create_graph(data):
    """Creates a NetworkX graph from the project data."""
    graph = nx.Graph()  # Use nx.DiGraph() for directed graph if needed

    graph.add_node(data['projectId'], label=data['projectName'], level=0, size = 20)

    for deliverable in data['deliverables']:
        graph.add_node(deliverable['deliverableId'], label=deliverable['deliverableName'], level=1, size = 15)
        graph.add_edge(data['projectId'], deliverable['deliverableId'])

        for task in deliverable['tasks']:
            graph.add_node(task['taskId'], label=task['taskName'], level=2, size = 10)
            graph.add_edge(deliverable['deliverableId'], task['taskId'])

    return graph

def display_graph(graph):
    """Displays the graph using pyvis."""
    net = Network(notebook=True, directed=False, cdn_resources='in_line') # Use notebook=True in streamlit
    net.from_nx(graph)

    # Add physics for better layout (optional)
    net.repulsion(node_distance=120, central_gravity=0.2,
                     spring_length=100, spring_strength=0.05,
                     damping=0.9)
    net.show('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as f:
        html_string = f.read()

    st.components.v1.html(html_string, height=600)

def main():
    st.title("Project Structure Visualization")

    data = {
        "projectId": "P1",
        "projectName": "Project A",
        "deliverables": [
            {
                "deliverableId": "D1",
                "deliverableName": "Deliverable A",
                "tasks": [
                    {"taskId": "T1", "taskName": "Task A1", "status": "In Progress"},
                    {"taskId": "T2", "taskName": "Task A2", "status": "Pending"},
                ],
            },
            {
                "deliverableId": "D2",
                "deliverableName": "Deliverable B",
                "tasks": [
                    {"taskId": "T3", "taskName": "Task B1", "status": "Completed"},
                ],
            },
        ],
    }

    graph = create_graph(data)
    display_graph(graph)

if __name__ == "__main__":
    main()
