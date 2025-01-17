import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime, timedelta
import pandas as pd

# Sample data with completion dates
relationships = {
    'projects': ['Project 1', 'Project 2'],
    'deliverables': [
        {'name': 'Deliverable 1', 'completion_date': '2024-03-15'},
        {'name': 'Deliverable 2', 'completion_date': '2024-04-30'},
        {'name': 'Deliverable 3', 'completion_date': '2024-05-15'}
    ],
    'tasks': ['Task 1', 'Task 2', 'Task 3', 'Task 4'],
    'releases': ['Release 1', 'Release 2'],
    'project_deliverable': [
        ('Project 1', 'Deliverable 1'),
        ('Project 1', 'Deliverable 2'),
        ('Project 2', 'Deliverable 3')
    ],
    'deliverable_task': [
        ('Deliverable 1', 'Task 1'),
        ('Deliverable 1', 'Task 2'),
        ('Deliverable 2', 'Task 3'),
        ('Deliverable 3', 'Task 4')
    ],
    'release_deliverable': [
        ('Release 1', 'Deliverable 1'),
        ('Release 1', 'Deliverable 2'),
        ('Release 2', 'Deliverable 3')
    ]
}

st.title("Project-Deliverable-Task-Release Timeline")

# Create tabs for different views
tab1, tab2 = st.tabs(["Network View", "Timeline View"])

with tab1:
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes with different categories
    for project in relationships['projects']:
        G.add_node(project, category='project')
    for deliverable in relationships['deliverables']:
        G.add_node(deliverable['name'], 
                  category='deliverable',
                  completion_date=deliverable['completion_date'])
    for task in relationships['tasks']:
        G.add_node(task, category='task')
    for release in relationships['releases']:
        G.add_node(release, category='release')

    # Add edges
    for edge in relationships['project_deliverable']:
        G.add_edge(edge[0], edge[1])
    for edge in relationships['deliverable_task']:
        G.add_edge(edge[0], edge[1])
    for edge in relationships['release_deliverable']:
        G.add_edge(edge[0], edge[1])

    # Create layout
    pos = nx.multipartite_layout(G, subset_key='category', align='horizontal')

    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node traces for each category
    node_traces = {}
    colors = {'project': '#1f77b4', 'deliverable': '#2ca02c', 
              'task': '#ff7f0e', 'release': '#d62728'}

    for category in ['project', 'deliverable', 'task', 'release']:
        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            if G.nodes[node]['category'] == category:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                if category == 'deliverable':
                    completion_date = G.nodes[node]['completion_date']
                    node_text.append(f"{node}<br>Due: {completion_date}")
                else:
                    node_text.append(node)

        node_traces[category] = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="bottom center",
            name=category.capitalize(),
            marker=dict(
                color=colors[category],
                size=30,
                line_width=2))

    # Create the network figure
    fig_network = go.Figure(data=[edge_trace] + list(node_traces.values()))
    fig_network.update_layout(
        title='Project-Deliverable-Task-Release Relationships',
        showlegend=True,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=1000,
        height=600
    )

    st.plotly_chart(fig_network)

with tab2:
    # Create timeline view
    deliverables_df = pd.DataFrame(relationships['deliverables'])
    deliverables_df['completion_date'] = pd.to_datetime(deliverables_df['completion_date'])

    # Create timeline figure
    fig_timeline = go.Figure()

    # Add deliverables as points
    fig_timeline.add_trace(go.Scatter(
        x=deliverables_df['completion_date'],
        y=deliverables_df['name'],
        mode='markers+text',
        name='Deliverables',
        text=deliverables_df['name'],
        marker=dict(size=20, color='#2ca02c'),
        textposition="bottom center"
    ))

    # Update timeline layout
    fig_timeline.update_layout(
        title='Deliverables Timeline',
        xaxis_title='Completion Date',
        yaxis_title='Deliverables',
        height=400,
        showlegend=False
    )

    st.plotly_chart(fig_timeline)

# Sidebar filters and controls
st.sidebar.header("Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Filter by Completion Date Range",
    value=(
        min(pd.to_datetime(d['completion_date']) for d in relationships['deliverables']),
        max(pd.to_datetime(d['completion_date']) for d in relationships['deliverables'])
    )
)

# Project filter
selected_projects = st.sidebar.multiselect(
    "Select Projects",
    relationships['projects'],
    default=relationships['projects']
)

# Release filter
selected_releases = st.sidebar.multiselect(
    "Select Releases",
    relationships['releases'],
    default=relationships['releases']
)

# Statistics
st.sidebar.header("Statistics")
st.sidebar.write(f"Total Projects: {len(relationships['projects'])}")
st.sidebar.write(f"Total Deliverables: {len(relationships['deliverables'])}")
st.sidebar.write(f"Total Tasks: {len(relationships['tasks'])}")
st.sidebar.write(f"Total Releases: {len(relationships['releases'])}")

# Add explanation
st.markdown("""
### Views:
1. **Network View**: Shows relationships between all components
2. **Timeline View**: Shows deliverables arranged by completion date

### Relationship Types:
- **Project → Deliverable**: One project can have multiple deliverables
- **Deliverable → Task**: One deliverable can have multiple tasks
- **Release → Deliverable**: One release can include multiple deliverables

### Color Legend:
- 🔵 Blue: Projects
- 🟢 Green: Deliverables (with completion dates)
- 🟠 Orange: Tasks
- 🔴 Red: Releases
""")
