import streamlit as st
import graphviz
from typing import Callable

# Initialize session state for expanded/collapsed states
if 'expanded_deliverables' not in st.session_state:
    st.session_state.expanded_deliverables = set()  # Store expanded deliverable IDs

# Larger dataset
data = {
    "projectId": "P1",
    "projectName": "Project A",
    "deliverables": [
        {
            "deliverableId": f"D{i}",
            "deliverableName": f"Deliverable {chr(65+i)}",
            "tasks": [
                {
                    "taskId": f"T{i}{j}",
                    "taskName": f"Task {chr(65+i)}{j+1}",
                    "status": ["In Progress", "Completed", "Pending"][j % 3]
                } for j in range(6)
            ],
        } for i in range(6)
    ],
}

def toggle_deliverable(deliverable_id: str):
    """Toggle the expanded/collapsed state of a deliverable"""
    if deliverable_id in st.session_state.expanded_deliverables:
        st.session_state.expanded_deliverables.remove(deliverable_id)
    else:
        st.session_state.expanded_deliverables.add(deliverable_id)

def create_mindmap(data: dict):
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')  # Left to right layout

    # Set default node attributes
    graph.attr('node', 
              fontcolor='black',
              fontname='Arial',
              style='filled',
              color='gray')  # default border color

    # Add project node
    project_id = f"project_{data['projectId']}"
    graph.node(project_id, data['projectName'], 
               fillcolor='#ADD8E6',  # light blue
               color='#4682B4')      # border color

    # Add deliverable nodes and connect to project
    for deliverable in data['deliverables']:
        deliverable_id = f"deliverable_{deliverable['deliverableId']}"

        # Add deliverable node
        is_expanded = deliverable_id in st.session_state.expanded_deliverables
        label = f"{deliverable['deliverableName']}\n[{'-' if is_expanded else '+'}]"

        graph.node(deliverable_id, 
                  label,
                  fillcolor='#90EE90',  # light green
                  color='#228B22',      # forest green border
                  fontcolor='black')    # explicit black text

        graph.edge(project_id, deliverable_id)

        # Only show tasks if deliverable is expanded
        if is_expanded:
            for task in deliverable['tasks']:
                task_id = f"task_{task['taskId']}"

                # Task colors with better contrast
                color = {
                    'Completed': '#F0F0F0',    # very light gray
                    'In Progress': '#FFFACD',  # light yellow
                    'Pending': '#FFE4B5'       # light orange
                }.get(task['status'], 'white')

                graph.node(task_id, 
                          f"{task['taskName']}\n({task['status']})",
                          fillcolor=color,
                          color='#696969',     # darker border
                          fontcolor='black')    # explicit black text

                graph.edge(deliverable_id, task_id)

    return graph

def main():
    st.title("Project Mindmap")

    # Create columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create and display the mindmap
        graph = create_mindmap(data)
        st.graphviz_chart(graph)

    with col2:
        st.subheader("Controls")

        # Add expand/collapse all buttons
        col_exp_all, col_col_all = st.columns(2)
        with col_exp_all:
            if st.button("Expand All"):
                st.session_state.expanded_deliverables = {
                    f"deliverable_D{i}" for i in range(len(data['deliverables']))
                }
                st.rerun()

        with col_col_all:
            if st.button("Collapse All"):
                st.session_state.expanded_deliverables.clear()
                st.rerun()

        st.write("---")
        st.write("Deliverables:")
        for deliverable in data['deliverables']:
            deliverable_id = f"deliverable_{deliverable['deliverableId']}"
            is_expanded = deliverable_id in st.session_state.expanded_deliverables

            col_del, col_exp = st.columns([3, 1])

            with col_del:
                if st.button(f"📦 {deliverable['deliverableName']}", 
                            key=f"del_{deliverable['deliverableId']}"):
                    st.write(f"Deliverable Details:")
                    st.json({
                        "deliverableId": deliverable['deliverableId'],
                        "deliverableName": deliverable['deliverableName']
                    })

            with col_exp:
                if st.button("➖" if is_expanded else "➕", 
                            key=f"exp_{deliverable['deliverableId']}"):
                    toggle_deliverable(deliverable_id)
                    st.rerun()

            # Show tasks only if deliverable is expanded
            if is_expanded:
                for task in deliverable['tasks']:
                    status_emoji = {
                        'Completed': '✅',
                        'In Progress': '🔄',
                        'Pending': '⏳'
                    }.get(task['status'], '❓')

                    if st.button(f"  {status_emoji} {task['taskName']}", 
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
