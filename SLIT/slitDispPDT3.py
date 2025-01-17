import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components  # Import at the top
import json
from pprint import  PrettyPrinter
pp=PrettyPrinter(indent=4)

def create_graph(data):
    # ... (same as before)
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

    # Clear the existing graph component before redrawing
    if 'graph_component' in st.session_state:
        st.session_state.pop('graph_component')  # Remove previous component if any

    # Inject JavaScript to handle messages from the graph
    graph_component = components.html(html_string, height=600)
    st.session_state['graph_component'] = graph_component  # Save the component reference

    # Receive messages from JavaScript (node clicks)
    message = components.receive_message()
    return message

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

    pp.pprint(data)
    if 'graph_data' not in st.session_state:
        st.session_state.graph_data = data
        st.session_state.graph = create_graph(st.session_state.graph_data)

    if 'clicked_node' not in st.session_state:
        st.session_state.clicked_node = None


    message = display_graph(st.session_state.graph)
    if message:
        st.session_state.clicked_node = message
        st.experimental_rerun()

    if st.session_state.clicked_node:
        st.write(f"Clicked on node: {st.session_state.clicked_node}")
        # Perform actions based on the clicked node ID
        for deliverable in data['deliverables']:
            if st.session_state.clicked_node == deliverable['deliverableId']:
                st.write(f"Deliverable details: {deliverable}")
            for task in deliverable['tasks']:
                if st.session_state.clicked_node == task['taskId']:
                    st.write(f"Task details: {task}")
        if st.session_state.clicked_node == data['projectId']:
            st.write(f"Project details : {data}")

if __name__ == "__main__":
    main()
