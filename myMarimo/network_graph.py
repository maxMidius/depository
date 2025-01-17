import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    # Create a cell to store our selected node/edge
    import marimo as mo
    import plotly.graph_objects as go
    import networkx as nx
    return go, mo, nx


@app.cell
def _(go, nx):
    def create_graph():
        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes and edges
        G.add_edges_from([('A', 'B'), ('A', 'C')])

        # Create layout
        pos = nx.spring_layout(G)

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
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines')

        # Create node traces
        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=30,
                color='#1f77b4',
                line_width=2))

        # Create the figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=0,l=0,r=0,t=0),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))

        return fig
    return (create_graph,)


@app.cell
def plot_output(create_graph, selection_state):
    fig = create_graph()

    # Add click event handling
    def handle_click(trace, points, state):
        if points.point_inds:
            idx = points.point_inds[0]
            if trace.mode == 'markers+text':  # Node click
                selection_state.value.selected_element = f"Node: {trace.text[idx]}"
            else:  # Edge click
                selection_state.value.selected_element = f"Edge clicked"

    fig.data[0].on_click(handle_click)  # Edge trace
    fig.data[1].on_click(handle_click)  # Node trace
    fig
    return fig, handle_click


if __name__ == "__main__":
    app.run()
