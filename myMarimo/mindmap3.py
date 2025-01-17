import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import networkx as nx
    import json
    return json, mo, nx


@app.cell
def _(nx):
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
    return G, create_graph


@app.cell
def _(G, json, mo):
    def get_mindmap_data():
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

        return json.dumps({"nodes": nodes_data, "edges": edges_data})

    def visualize_mindmap():
        return mo.Html(f"""
        <div id="mindmap"></div>
        <script>
            var data = {get_mindmap_data()};
            var container = document.getElementById('mindmap');
            var options = {{
                nodes: {{
                    shape: 'dot',
                    size: 15,
                    font: {{
                        size: 12,
                        face: 'Tahoma'
                    }}
                }},
                edges: {{
                    color: '#000000'
                }}
            }};
            var network = new vis.Network(container, data, options);
            network.on('click', function(params) {{
                if (params.nodes.length > 0) {{
                    var clicked_node = params.nodes[0];
                    var output = document.createElement('div');
                    output.innerHTML = '<strong>Selected node: ' + clicked_node + '</strong>';
                    document.body.appendChild(output);
                }}
            }});
        </script>
        """)

    mindmap_view = visualize_mindmap()
    return get_mindmap_data, mindmap_view, visualize_mindmap


@app.cell
def _(mindmap_view, mo):
    def display_interface():
        return mo.hstack([
            mindmap_view,
            mo.vstack([
                mo.md("### Mindmap Controls"),
                mo.md("- Pan or zoom with mouse and scroll wheel<br>- Click on a node to select it<br>- Drag nodes to rearrange them"),
            ])
        ])

    display_interface()
    return (display_interface,)


@app.cell
def _(G, mindmap_view, mo, visualize_mindmap):
    def add_node_interface():
        node_name_input = mo.ui.text("Enter new node name")
        color_input = mo.ui.text("Enter node color (e.g., #E91E63 or red)")
        parent_select = mo.ui.dropdown(list(G.nodes()), label="Select parent for the new node")

        def add_node_action(_):
            node_name = node_name_input.value
            color_val = color_input.value or "#78b1f7"
            parent_node = parent_select.value
            if node_name and parent_node:
                G.add_node(node_name, color=color_val, size=15)
                G.add_edge(parent_node, node_name)
                # Re-render the mindmap
                mindmap_view.value = visualize_mindmap()

        return mo.vstack([
            mo.hstack([node_name_input, color_input]),
            parent_select,
            mo.ui.button(label="Add Node", on_click=add_node_action)
        ])

    add_node_interface()
    return (add_node_interface,)


if __name__ == "__main__":
    app.run()
