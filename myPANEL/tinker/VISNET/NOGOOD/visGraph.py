import panel as pn
import param

pn.extension()

# Graph data (nodes and edges)
graph_data = {
    "nodes": [
        {"id": 1, "label": "Node 1"},
        {"id": 2, "label": "Node 2"},
        {"id": 3, "label": "Node 3"},
        {"id": 4, "label": "Node 4"}
    ],
    "edges": [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3},
        {"from": 3, "to": 4}
    ]
}

# Define JSComponent for Vis.js
class VisJSNetworkGraph(pn.reactive.ReactiveHTML):
    __javascript__ = [
        "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"
    ]
    __css__ = [
        "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.css"
    ]
    __js_require__ = {
        "paths": {
            "vis": "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min"
        }
    }
    
    # Use param.Dict for reactive data
    data = param.Dict(default=graph_data)

    _template = """
    <div id="network" style="width:100%; height:600px; border:1px solid #ccc;"></div>
    <script>
        const nodes = new vis.DataSet(${data.nodes});
        const edges = new vis.DataSet(${data.edges});
        const container = document.getElementById("network");
        const data = { nodes: nodes, edges: edges };
        const options = {
            nodes: { shape: "dot", size: 20 },
            edges: { arrows: "to" }
        };
        const network = new vis.Network(container, data, options);
    </script>
    """

# Instantiate the component
vis_graph = VisJSNetworkGraph()

# Serve the Panel app
pn.serve(vis_graph)
