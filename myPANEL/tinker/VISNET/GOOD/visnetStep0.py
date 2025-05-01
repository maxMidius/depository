import panel as pn
import param
from panel.custom import JSComponent
from rich import print

# Load the vis-network library as an extension
pn.extension(js_files={
    'vis-network': "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"
})

class VisNetComponent(JSComponent):
    object = param.Dict()
    # Add a click event parameter to capture node clicks
    node_click = param.Event(default=None)
    edge_click = param.Event(default=None)

    _esm = """
    export function render({ model, el }) {
        const container = document.createElement('div');
        container.style.width = '100%';
        container.style.height = '400px';
        el.append(container);
        
        // Store full data
        const fullData = model.object.data;
        
        // Use globally available vis object
        const create_network = () => {
            const data = {
                nodes: new vis.DataSet(fullData.nodes),
                edges: new vis.DataSet(fullData.edges)
            };
            
            const network = new vis.Network(container, data, model.object.options);
            
            // Add single click event handler - notify Python
            network.on("click", function(params) {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    
                    // Get the node data
                    const nodeData = fullData.nodes.find(node => node.id === nodeId);

                    console.log("Clicked node ID:", nodeId, nodeData);
                    
                    // Send the node data to Python
                    const jsonData = JSON.stringify(nodeData);
                    model.send_msg(`nodeClick: ${jsonData}`);
                } 
                else if (params.edges.length > 0) {
                    const edgeId = params.edges[0];
                    console.log("Clicked edge ID:", edgeId);
                    
                    // Get the edge data
                    const edgeData = fullData.edges.find(edge => 
                        edge.from === network.getConnectedNodes(edgeId)[0] && 
                        edge.to === network.getConnectedNodes(edgeId)[1]
                    );
                    console.log(edgeData);
                    const jsonData = JSON.stringify(edgeData);
                    model.send_msg(`edgeClick: ${jsonData}`);
                }
            });
            
            return network;
        };
        
        let network = create_network();

        model.on("object", () => {
            network.destroy();
            network = create_network();
        });

        model.on('remove', () => network.destroy());
    }
    """

    # Handler for messages from JavaScript
    def _handle_msg(self, message):
        print(message)

def network_data():
    return {
        "data": {
            "nodes": [
                {"id": 1, "label": "Node 1"},
                {"id": 2, "label": "Node 2"},
                {"id": 3, "label": "Node 3"},
                {"id": 4, "label": "Node 4"},
                {"id": 5, "label": "Node 5"}
            ],
            "edges": [
                {"id": "e1", "from": 1, "to": 2, "label": "Edge 1-2"},
                {"id": "e2", "from": 1, "to": 3, "label": "Edge 1-3"},
                {"id": "e3", "from": 2, "to": 4, "label": "Edge 2-4"},
                {"id": "e4", "from": 2, "to": 5, "label": "Edge 2-5"},
                {"id": "e5", "from": 3, "to": 5, "label": "Edge 3-5"}
            ]
        },
        "options": {
            "physics": {
                "enabled": True,
                "stabilization": {
                    "iterations": 100
                }
            },
            "nodes": {
                "shape": "dot",
                "size": 20, 
                "font": {
                    "size": 14
                }
            },
            "edges": {
                "font": {
                    "size": 12
                },
                "width": 2
            }
        }
    }

# Create the network component
network_component = VisNetComponent(
    object=network_data(), height=400, sizing_mode="stretch_width"
)

# Server display
pn.Column(network_component).servable()