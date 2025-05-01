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

    _esm = """
    export function render({ model, el }) {
        const container = document.createElement('div');
        container.style.width = '100%';
        container.style.height = '400px';
        el.append(container);
        
        // Track collapsed node ids
        let collapsedNodes = new Set();
        
        // Store full data
        const fullData = model.object.data;
        
        // Helper function to get child nodes of a parent node
        const getChildNodeIds = (parentId) => {
            return fullData.edges
                .filter(edge => edge.from === parentId)
                .map(edge => edge.to);
        };
        
        // Check if node is a leaf node (no children)
        const isLeafNode = (nodeId) => {
            return !fullData.edges.some(edge => edge.from === nodeId);
        };
        
        // Get all descendant nodes recursively
        const getAllDescendants = (nodeId, result = new Set()) => {
            const children = getChildNodeIds(nodeId);
            
            children.forEach(childId => {
                result.add(childId);
                if (!isLeafNode(childId)) {
                    getAllDescendants(childId, result);
                }
            });
            
            return result;
        };
        
        // Filter data based on collapsed nodes
        const getFilteredData = () => {
            // Start with all nodes visible
            let visibleNodeIds = new Set(fullData.nodes.map(node => node.id));
            
            // For each collapsed node, remove all its descendants
            collapsedNodes.forEach(nodeId => {
                const descendants = getAllDescendants(nodeId);
                descendants.forEach(descendantId => {
                    visibleNodeIds.delete(descendantId);
                });
            });
            
            // Filter nodes and edges
            const nodes = fullData.nodes.filter(node => visibleNodeIds.has(node.id));
            const edges = fullData.edges.filter(edge => 
                visibleNodeIds.has(edge.from) && visibleNodeIds.has(edge.to)
            );
            
            return { nodes, edges };
        };
        
        // Use globally available vis object
        const create_network = () => {
            const filteredData = getFilteredData();
            const data = {
                nodes: new vis.DataSet(filteredData.nodes),
                edges: new vis.DataSet(filteredData.edges)
            };
            
            const network = new vis.Network(container, data, model.object.options);
            
            // Single click handler - now handles both normal clicks and shift+click
            network.on("click", function(params) {
                const isShiftClick = params.event.srcEvent.shiftKey;
                
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    
                    // Check if this is a shift-click for expand/collapse
                    if (isShiftClick && !isLeafNode(nodeId)) {
                        console.log("Shift+Click on node ID:", nodeId, "- toggling expand/collapse");
                        
                        // Toggle collapsed state
                        if (collapsedNodes.has(nodeId)) {
                            // Expand node
                            collapsedNodes.delete(nodeId);
                        } else {
                            // Collapse node
                            collapsedNodes.add(nodeId);
                        }
                        
                        // Update network with new filtered data
                        const filteredData = getFilteredData();
                        data.nodes.clear();
                        data.nodes.add(filteredData.nodes);
                        data.edges.clear();
                        data.edges.add(filteredData.edges);
                    } 
                    // Regular click (no shift) - just notify Python
                    else {
                        // Get the node data
                        const nodeData = fullData.nodes.find(node => node.id === nodeId);
                        console.log("Clicked node ID:", nodeId, nodeData);
                        
                        // Send the node data to Python
                        const jsonData = JSON.stringify(nodeData);
                        model.send_msg(`nodeClick: ${jsonData}`);
                    }
                } 
                else if (params.edges.length > 0) {
                    const edgeId = params.edges[0];
                    
                    // Get the edge data with all attributes
                    const edgeData = fullData.edges.find(edge => edge.id === edgeId);
                    
                    // Log enhanced edge information
                    console.log("Clicked edge:", {
                        id: edgeData.id,
                        from: edgeData.from,
                        to: edgeData.to,
                        label: edgeData.label
                    });
                    
                    // Send complete edge data to Python
                    const jsonData = JSON.stringify(edgeData);
                    model.send_msg(`edgeClick: ${jsonData}`);
                }
            });
            
            return network;
        };
        
        let network = create_network();

        model.on("object", () => {
            collapsedNodes.clear();
            network.destroy();
            network = create_network();
        });

        model.on('remove', () => network.destroy());
    }
    """

    # Python callback for messages
    def _handle_msg(self, someMsg):
        print(someMsg)

def network_data():
    return {
        "data": {
            "nodes": [
                {"id": 1, "label": "Root", "level": 0},
                
                # Level 1 - Three main branches
                {"id": 2, "label": "Branch 1", "level": 1},
                {"id": 3, "label": "Branch 2", "level": 1},
                {"id": 4, "label": "Branch 3", "level": 1},
                
                # Level 2 - Two children per branch
                {"id": 5, "label": "Node 1.1", "level": 2},
                {"id": 6, "label": "Node 1.2", "level": 2},
                {"id": 7, "label": "Node 2.1", "level": 2},
                {"id": 8, "label": "Node 2.2", "level": 2},
                {"id": 9, "label": "Node 3.1", "level": 2},
                {"id": 10, "label": "Node 3.2", "level": 2},
                
                # Level 3 - Two children per level 2 node
                {"id": 11, "label": "Node 1.1.1", "level": 3},
                {"id": 12, "label": "Node 1.1.2", "level": 3},
                {"id": 13, "label": "Node 1.2.1", "level": 3},
                {"id": 14, "label": "Node 1.2.2", "level": 3},
                {"id": 15, "label": "Node 2.1.1", "level": 3},
                {"id": 16, "label": "Node 2.1.2", "level": 3},
                {"id": 17, "label": "Node 2.2.1", "level": 3},
                {"id": 18, "label": "Node 2.2.2", "level": 3},
                {"id": 19, "label": "Node 3.1.1", "level": 3},
                {"id": 20, "label": "Node 3.1.2", "level": 3},
                {"id": 21, "label": "Node 3.2.1", "level": 3},
                {"id": 22, "label": "Node 3.2.2", "level": 3}
            ],
            "edges": [
                # Root to Level 1
                {"id": "e1-2", "from": 1, "to": 2, "label": "Root→Branch 1"},
                {"id": "e1-3", "from": 1, "to": 3, "label": "Root→Branch 2"},
                {"id": "e1-4", "from": 1, "to": 4, "label": "Root→Branch 3"},
                
                # Branch 1 to Level 2
                {"id": "e2-5", "from": 2, "to": 5, "label": "B1→1.1"},
                {"id": "e2-6", "from": 2, "to": 6, "label": "B1→1.2"},
                
                # Branch 2 to Level 2
                {"id": "e3-7", "from": 3, "to": 7, "label": "B2→2.1"},
                {"id": "e3-8", "from": 3, "to": 8, "label": "B2→2.2"},
                
                # Branch 3 to Level 2
                {"id": "e4-9", "from": 4, "to": 9, "label": "B3→3.1"},
                {"id": "e4-10", "from": 4, "to": 10, "label": "B3→3.2"},
                
                # Level 2 to Level 3 (Branch 1)
                {"id": "e5-11", "from": 5, "to": 11, "label": "1.1→1.1.1"},
                {"id": "e5-12", "from": 5, "to": 12, "label": "1.1→1.1.2"},
                {"id": "e6-13", "from": 6, "to": 13, "label": "1.2→1.2.1"},
                {"id": "e6-14", "from": 6, "to": 14, "label": "1.2→1.2.2"},
                
                # Level 2 to Level 3 (Branch 2)
                {"id": "e7-15", "from": 7, "to": 15, "label": "2.1→2.1.1"},
                {"id": "e7-16", "from": 7, "to": 16, "label": "2.1→2.1.2"},
                {"id": "e8-17", "from": 8, "to": 17, "label": "2.2→2.2.1"},
                {"id": "e8-18", "from": 8, "to": 18, "label": "2.2→2.2.2"},
                
                # Level 2 to Level 3 (Branch 3)
                {"id": "e9-19", "from": 9, "to": 19, "label": "3.1→3.1.1"},
                {"id": "e9-20", "from": 9, "to": 20, "label": "3.1→3.1.2"},
                {"id": "e10-21", "from": 10, "to": 21, "label": "3.2→3.2.1"},
                {"id": "e10-22", "from": 10, "to": 22, "label": "3.2→3.2.2"}
            ]
        },
        "options": {
            "physics": {
                "enabled": True,
                "hierarchicalRepulsion": {
                    "centralGravity": 0.0,
                    "springLength": 100,
                    "springConstant": 0.01,
                    "nodeDistance": 120
                }
            },
            "layout": {
                "hierarchical": {
                    "enabled": True,
                    "direction": "UD",
                    "sortMethod": "directed"
                }
            },
            "nodes": {
                "shape": "dot",
                "size": 16
            },
            "edges": {
                "arrows": "to",
                "font": {
                    "align": "middle"
                }
            }
        }
    }

# Create the network component
network_component = VisNetComponent(
    object=network_data(), height=400, sizing_mode="stretch_width"
)

# Server display
pn.Column(network_component).servable()