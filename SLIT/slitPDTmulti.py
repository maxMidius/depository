import streamlit as st
import plotly.graph_objects as go
import networkx as nx

# Install required packages:
# pip install streamlit plotly networkx

st.title("Project-Deliverable-Task-Release Visualization")

# Sample data
relationships = {
    'projects': ['Project 1', 'Project 2'],
    'deliverables': ['Deliverable 1', 'Deliverable 2', 'Deliverable 3'],
    'tasks': ['Task 1', 'Task 2', 'Task 3', 'Task 4'],
    'releases': ['Release 1', 'Release 2'],
    # Define relationships
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

# Create a directed graph
G = nx.DiGraph()

# Add nodes with different categories
for project in relationships['projects']:
    G.add_node(project, category='project')
for deliverable in relationships['deliverables']:
    G.add_node(deliverable, category='deliverable')
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

# Create the figure
fig = go.Figure(data=[edge_trace] + list(node_traces.values()))

# Update layout
fig.update_layout(
    title='Project-Deliverable-Task-Release Relationships',
    showlegend=True,
    hovermode='closest',
    margin=dict(b=20,l=5,r=5,t=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    width=1000,
    height=600
)

# Display the plot
st.plotly_chart(fig)

# Add interactive filters
st.sidebar.header("Filters")

# Filter by project
selected_projects = st.sidebar.multiselect(
    "Select Projects",
    relationships['projects'],
    default=relationships['projects']
)

# Filter by release
selected_releases = st.sidebar.multiselect(
    "Select Releases",
    relationships['releases'],
    default=relationships['releases']
)

# Add some statistics
st.sidebar.header("Statistics")
st.sidebar.write(f"Total Projects: {len(relationships['projects'])}")
st.sidebar.write(f"Total Deliverables: {len(relationships['deliverables'])}")
st.sidebar.write(f"Total Tasks: {len(relationships['tasks'])}")
st.sidebar.write(f"Total Releases: {len(relationships['releases'])}")

# Add explanation
st.markdown("""
### Relationship Types:
- **Project → Deliverable**: One project can have multiple deliverables
- **Deliverable → Task**: One deliverable can have multiple tasks
- **Release → Deliverable**: One release can include multiple deliverables

### Color Legend:
- 🔵 Blue: Projects
- 🟢 Green: Deliverables
- 🟠 Orange: Tasks
- 🔴 Red: Releases
""")
