import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import networkx as nx
    import json

    # Create the graph
    G = nx.Graph()
    G.add_node("Main Topic", color="#F44336", size=20) 
    G.add_node("Subtopic 1", color="#4CAF50", size=15)
    G.add_node("Subtopic 2", color="#FFC107", size=15)
    G.add_node("Subtopic 3", color="#2196F3", size=15)

    G.add_edge("Main Topic", "Subtopic 1")
    G.add_edge("Main Topic", "Subtopic 2")
    G.add_edge("Main Topic", "Subtopic 3")
    return G, json, mo, nx


@app.cell
def _(G, json):
    # Convert graph into data structure suitable for visualization
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
    return (get_mindmap_data,)


@app.cell
def _(get_mindmap_data, mo):
    # Visualization cell
    mindmap_view = mo.md(f"""
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
    return (mindmap_view,)


@app.cell
def _(mindmap_view, mo):
    # Display mindmap and a control panel
    display_interface = mo.hstack([
        mindmap_view,
        mo.vstack([
            mo.md("### Mindmap Controls"),
            mo.md("- Pan or zoom with mouse and scroll wheel<br>- Click on a node to select it<br>- Drag nodes to rearrange them"),
        ])
    ])
    return (display_interface,)


@app.cell
def _(G, mo):
    node_name_input = mo.ui.text("Enter new node name")
    color_input = mo.ui.text("Enter node color (e.g., #E91E63 or red)")
    parent_select = mo.ui.dropdown(list(G.nodes()), label="Select parent for the new node")
    add_node_interface= mo.hstack( [
        # Interface to add new nodes
        node_name_input,
        color_input,
        parent_select,

        ] )
    return add_node_interface, color_input, node_name_input, parent_select


@app.cell
def _(
    G,
    color_input,
    get_mindmap_data,
    mindmap_view,
    mo,
    node_name_input,
    parent_select,
):
    def add_node_action(_):
        node_name = node_name_input.value
        color_val = color_input.value or "#78b1f7"
        parent_node = parent_select.value
        if node_name and parent_node:
            G.add_node(node_name, color=color_val, size=15)
            G.add_edge(parent_node, node_name)
            # Re-render the mindmap
            mindmap_view.value = mo.md(f"""
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
    return (add_node_action,)


@app.cell
def _(add_node_interface, display_interface, mo):
    # Combine all elements
    mo.vstack([
        display_interface,
        mo.md("---"),
        add_node_interface
    ])
    return


if __name__ == "__main__":
    app.run()
