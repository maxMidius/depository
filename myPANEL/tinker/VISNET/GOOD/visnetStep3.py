import panel as pn
import param
from panel.custom import JSComponent
from rich import print
import json

# Import the network data from the separate file
from visData.network_data import available_networks

# Load the vis-network library and W3.CSS as extensions
pn.extension(
    js_files={
        'vis-network': "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"
    },
    css_files=[
        "https://www.w3schools.com/w3css/4/w3.css"
    ]
)

class VisNetComponent(JSComponent):
    object = param.Dict()
    # Add a parameter to store click information
    click_info = param.String(default="No clicks yet. Click on nodes or edges to see information here.")

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
        
        // Listen for the fit_view message
        model.on("msg:custom", (msg) => {
            if (msg === "fit_view") {
                console.log("Fitting network to view");
                network.fit({
                    animation: {
                        duration: 800,
                        easingFunction: "easeInOutQuad"
                    }
                });
            }
        });

        model.on("object", () => {
            collapsedNodes.clear();
            network.destroy();
            network = create_network();
        });

        model.on('remove', () => network.destroy());
    }
    """

    # Python callback for messages - update the click_info parameter
    def _handle_msg(self, msg):
        print(msg)  # Keep console logging
        
        # Parse the message
        if msg.startswith('nodeClick:'):
            # Extract the JSON data
            node_data = json.loads(msg.replace('nodeClick:', '').strip())
            # Format a nice message
            self.click_info = f"""
            <div class="w3-panel w3-pale-blue w3-leftbar w3-border-blue">
                <h4>Node Click Event</h4>
                <p><strong>ID:</strong> {node_data['id']}</p>
                <p><strong>Label:</strong> {node_data['label']}</p>
                <p><strong>Level:</strong> {node_data['level']}</p>
                {f"<p><strong>Group:</strong> {node_data['group']}</p>" if 'group' in node_data else ""}
            </div>
            """
        elif msg.startswith('edgeClick:'):
            # Extract the JSON data
            edge_data = json.loads(msg.replace('edgeClick:', '').strip())
            # Format a nice message
            self.click_info = f"""
            <div class="w3-panel w3-pale-green w3-leftbar w3-border-green">
                <h4>Edge Click Event</h4>
                <p><strong>ID:</strong> {edge_data['id']}</p>
                <p><strong>From:</strong> {edge_data['from']}</p>
                <p><strong>To:</strong> {edge_data['to']}</p>
                <p><strong>Label:</strong> {edge_data['label']}</p>
                {f"<p><strong>Width:</strong> {edge_data['width']}</p>" if 'width' in edge_data else ""}
                {f"<p><strong>Dashed:</strong> {'Yes' if edge_data.get('dashes') else 'No'}</p>" if 'dashes' in edge_data else ""}
            </div>
            """
    
    # Add method to fit view
    def fit_view(self, event=None):
        self._send_msg("fit_view")

# Get all available networks
networks = available_networks()
network_names = list(networks.keys())

# Create a selector for the network type
network_selector = pn.widgets.Select(
    name="Select Network Type",
    options=network_names,
    value=network_names[0],
    width=300,
    css_classes=["w3-select", "w3-border", "w3-round"]
)

# Create a reset button
reset_button = pn.widgets.Button(
    name="Reset View",
    button_type="primary",
    icon="refresh",
    css_classes=["w3-button", "w3-teal", "w3-round"],
    width=150
)

# Create a function to get the selected network data
def get_selected_network(network_name):
    return networks[network_name]()

# Create the network component with reactivity to the selector
network_component = VisNetComponent(
    object=pn.bind(get_selected_network, network_selector),
    height=400, 
    sizing_mode="stretch_width"
)

# Link the button to the fit_view method
reset_button.on_click(network_component.fit_view)

# Create a header with W3.CSS badge
header_html = """
<div class="w3-container w3-padding-16 w3-teal">
    <h2>Network Visualization 
        <span class="w3-badge w3-red w3-large">STEP-3</span>
    </h2>
    <p>Interactive network with expand/collapse and multiple data sources</p>
</div>
"""
header = pn.pane.HTML(header_html, sizing_mode="stretch_width")

# Create a container for the selector with a nice title
selector_title = pn.pane.HTML(
    """<div class="w3-container w3-light-grey">
        <h3>Network Data Selection</h3>
    </div>""",
    sizing_mode="stretch_width"
)

selector_container = pn.Column(
    selector_title,
    pn.Row(network_selector, reset_button),  # Add reset button next to selector
    css_classes=["w3-container", "w3-card-2", "w3-round", "w3-margin-bottom"],
    sizing_mode="stretch_width"
)

# Create an info panel to display click events
event_display = pn.pane.HTML(
    pn.bind(lambda info: info, network_component.param.click_info),
    sizing_mode="stretch_both",
    css_classes=["w3-container", "w3-card-2", "w3-round"]
)

# Add a title for the event display
event_title = pn.pane.HTML(
    """<div class="w3-container w3-light-grey">
        <h3>Click Event Information</h3>
    </div>""",
    sizing_mode="stretch_width"
)

# Server display with the header, selector, network and event display
def doLayout() :
    return pn.Column(
        header,
        selector_container,
        network_component,
        event_title,
        event_display,
        css_classes=["w3-container", "w3-light-grey"],
        sizing_mode="stretch_both"
    )

doLayout().servable()