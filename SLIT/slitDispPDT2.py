import streamlit as st
import networkx as nx
from pyvis.network import Network
import json

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
    net = Network(notebook=True, directed=False, cdn_resources='in_line')
    net.from_nx(graph)

    net.repulsion(node_distance=120, central_gravity=0.2,
                     spring_length=100, spring_strength=0.05,
                     damping=0.9)

    # Add onclick event to nodes using JavaScript
    net.options.nodes = {
        'onclick': 'function(nodeId) { sendMessage(nodeId); }'
    }

    net.show('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as f:
        html_string = f.read()

    # Inject JavaScript to handle messages from the graph
    components.html(f"""
    {html_string}
    <script>
        function sendMessage(nodeId) {{
            window.parent.postMessage(nodeId, "*");
        }}

        window.addEventListener('message', function(event) {{
            // Handle messages from Streamlit (if needed later)
        }});
    </script>
    """, height=600)

    # Receive messages from JavaScript (node clicks)
    message = components.receive_message()
    if message:
        st.write(f"Clicked on node: {message}")
        # Perform actions based on the clicked node ID
        for deliverable in data['deliverables']:
            if message == deliverable['deliverableId']:
                st.write(f"Deliverable details: {deliverable}")
            for task in deliverable['tasks']:
                if message == task['taskId']:
                    st.write(f"Task details: {task}")
        if message == data['projectId']:
            st.write(f"Project details : {data}")


def main():
    st.title("Project Structure Visualization with OnClick")
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

# Import components AFTER defining display_graph
import streamlit.components.v1 as components

if __name__ == "__main__":
    main()
