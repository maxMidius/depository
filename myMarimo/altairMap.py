import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import plotly.graph_objects as go
    import numpy as np
    return go, mo, np


@app.cell
def _(go, marimo):
    # Define the nodes and edges for the mindmap-like structure
    nodes = [
        {'id': 0, 'label': 'Main Topic'},
        {'id': 1, 'label': 'Subtopic 1'},
        {'id': 2, 'label': 'Subtopic 2'},
        {'id': 3, 'label': 'Detail 1a'},
        {'id': 4, 'label': 'Detail 1b'},
        {'id': 5, 'label': 'Detail 2a'},
    ]
    edges = [
        {'source': 0, 'target': 1},
        {'source': 0, 'target': 2},
        {'source': 1, 'target': 3},
        {'source': 1, 'target': 4},
        {'source': 2, 'target': 5},
    ]


    # Create node positions for a basic layout (you might need a more sophisticated algorithm for complex graphs)
    node_positions = {
        0: (0.5, 0.8),
        1: (0.2, 0.5),
        2: (0.8, 0.5),
        3: (0.1, 0.2),
        4: (0.3, 0.2),
        5: (0.9, 0.2)
    }


    # Extract x, y coordinates, and labels for nodes
    x_nodes = [node_positions[node['id']][0] for node in nodes]
    y_nodes = [node_positions[node['id']][1] for node in nodes]
    labels = [node['label'] for node in nodes]


    # Create edge traces
    edge_traces = []
    for edge in edges:
        x0, y0 = node_positions[edge['source']]
        x1, y1 = node_positions[edge['target']]
        edge_trace = go.Scatter(x=[x0, x1],
                               y=[y0, y1],
                               line=dict(width=0.5, color='#888'),
                               hoverinfo='none',
                               mode='lines')
        edge_traces.append(edge_trace)


    # Create node trace
    node_trace = go.Scatter(x=x_nodes,
                            y=y_nodes,
                            mode='markers+text',
                            marker=dict(size=20, color='skyblue'),
                            text=labels,
                            textposition="bottom center",
                            hoverinfo='text',
                            customdata=[node['id'] for node in nodes])

    # Create the figure
    fig = go.Figure(data=edge_traces+[node_trace])
    fig.update_layout(
        showlegend=False,
        width=500,  # Set width to make the graph smaller
        height=400,  # Set height to make the graph smaller
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        clickmode='event')

    # Function to handle clicks
    def handle_click(trace, points, state):
        if points.point_inds:
            clicked_index = points.point_inds[0]
        clicked_node_id = trace.customdata[clicked_index]
        marimo.stop(data=f'Clicked node ID: {clicked_node_id}')
    return (
        edge,
        edge_trace,
        edge_traces,
        edges,
        fig,
        handle_click,
        labels,
        node_positions,
        node_trace,
        nodes,
        x0,
        x1,
        x_nodes,
        y0,
        y1,
        y_nodes,
    )


app._unparsable_cell(
    r"""
    # Use marimo.ui.output to display the plot
    plot=mo.
    .on_click(handle_click)

    fig
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
