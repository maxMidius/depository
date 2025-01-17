import streamlit as st
import graphviz
from typing import Callable

def create_mindmap(data: dict):
    # Create a new directed graph
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')  # Left to right layout

    # Add project node
    project_id = f"project_{data['projectId']}"
    graph.node(project_id, data['projectName'], 
               style='filled', 
               fillcolor='lightblue')

    # Add deliverable nodes and connect to project
    for deliverable in data['deliverables']:
        deliverable_id = f"deliverable_{deliverable['deliverableId']}"
        graph.node(deliverable_id, deliverable['deliverableName'],
                  style='filled',
                  fillcolor='lightgreen')
        graph.edge(project_id, deliverable_id)

        # Add task nodes and connect to deliverable
        for task in deliverable['tasks']:
            task_id = f"task_{task['taskId']}"
            color = {
                'Completed': 'lightgray',
                'In Progress': 'yellow',
                'Pending': 'orange'
            }.get(task['status'], 'white')

            graph.node(task_id, f"{task['taskName']}\n({task['status']})",
                      style='filled',
                      fillcolor=color)
            graph.edge(deliverable_id, task_id)

    return graph

def main():
    st.title("Project Mindmap")

    # Your data structure
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

    # Create columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create and display the mindmap
        graph = create_mindmap(data)
        st.graphviz_chart(graph)

    with col2:
        st.subheader("Node Selection")
        # Create buttons for each node type

        # Project button
        if st.button(f"Project: {data['projectName']}", key="project"):
            st.write(f"Project Details:")
            st.json({
                "projectId": data['projectId'],
                "projectName": data['projectName']
            })

        # Deliverable buttons
        st.write("---")
        st.write("Deliverables:")
        for deliverable in data['deliverables']:
            if st.button(f"📦 {deliverable['deliverableName']}", 
                        key=f"del_{deliverable['deliverableId']}"):
                st.write(f"Deliverable Details:")
                st.json({
                    "deliverableId": deliverable['deliverableId'],
                    "deliverableName": deliverable['deliverableName']
                })

        # Task buttons
        st.write("---")
        st.write("Tasks:")
        for deliverable in data['deliverables']:
            for task in deliverable['tasks']:
                status_emoji = {
                    'Completed': '✅',
                    'In Progress': '🔄',
                    'Pending': '⏳'
                }.get(task['status'], '❓')

                if st.button(f"{status_emoji} {task['taskName']}", 
                            key=f"task_{task['taskId']}"):
                    st.write(f"Task Details:")
                    st.json({
                        "taskId": task['taskId'],
                        "taskName": task['taskName'],
                        "status": task['status'],
                        "parentDeliverable": deliverable['deliverableName']
                    })

if __name__ == "__main__":
    main()
