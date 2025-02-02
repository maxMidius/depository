import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


# Cell 1: Setup - import necessary libraries
@app.cell
def _() :
    import marimo as mo
    import networkx as nx
    import json

# Cell 2: Create the graph
@app.cell
def _():
    def create_graph():
        G = nx.Graph()
        # Add initial nodes
        G.add_node("Main Topic", color="#F44336", size=20) 
        G.add_node("Subtopic 1", color="#4CAF50", size=15)
        G.add_node("Subtopic 2", color="#FFC107", size=15)
        G.add_node("Subtopic 3", color="#2196F3", size=15)

        # Add edges
        G.add_edge("Main Topic", "Subtopic 1")
        G.add_edge("Main Topic", "Subtopic 2")
        G.add_edge("Main Topic", "Subtopic 3")
        return G

    G = create_graph()

# Cell 3: Visualization cell
@app.cell
def _() :
    def visualize_mindmap():
        # Convert graph into data structure suitable for marimo.vis.network
        nodes_data = []
        for node in G.nodes(data=True):
            node_id = node[0]
            attrs = node[1]
            nodes_data.append({
                "id": node_id,
                "label": node_id,
                "color": attrs.get("color", "#758bfd"),
                "size": attrs.get("size", 10)
            })

        edges_data = []
        for edge in G.edges():
            edges_data.append({"from": edge[0], "to": edge[1]})

        # Callback for node clicks
        def on_click(params):
            if params and "nodes" in params and params["nodes"]:
                clicked_node = params["nodes"][0]
                return mo.md(f"**Selected node: {clicked_node}**")

        return mo.vis.network({
            "nodes": nodes_data,
            "edges": edges_data
        }, height="400px", events={"click": on_click})

    mindmap_view = visualize_mindmap()

# Cell 4: Display mindmap and a control panel
@app.cell
def _() :
    def display_interface():
        return mo.hstack([
            mindmap_view,
            mo.vstack([
                mo.md("### Mindmap Controls"),
                mo.md("- Pan or zoom with mouse and scroll wheel<br>- Click on a node to select it<br>- Drag nodes to rearrange them"),
            ])
        ])

    display_interface()

# Cell 5: Interface to add new nodes
@app.cell
def _() :
    def add_node_interface():
        node_name_input = mo.input("Enter new node name")
        color_input = mo.input("Enter node color (e.g., #E91E63 or red)")
        parent_select = mo.select(list(G.nodes()), label="Select parent for the new node")

        def add_node_action(_):
            node_name = node_name_input.value
            color_val = color_input.value or "#78b1f7"
            parent_node = parent_select.value
            if node_name and parent_node:
                G.add_node(node_name, color=color_val, size=15)
                G.add_edge(parent_node, node_name)
                # Re-render the mindmap
                return visualize_mindmap()

        return mo.vstack([
            mo.hstack([node_name_input, color_input]),
            parent_select,
            mo.button("Add Node", on_click=add_node_action)
        ])

    add_node_interface()
