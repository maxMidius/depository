import panel as pn

class VisNetPane(pn.reactive.ReactiveHTML):

    _template = "<div id='${id}_mynetwork' style='width:600px; height:400px; border:1px solid lightgray'></div>"

    _scripts = {
        'render': """
            console.log("Trying to initialize network");
            
            // Use view.el to get the root element directly from Panel
            // This is more reliable than getElementById
            const vis_container = view.el.querySelector(`#${id}_mynetwork`);
            console.log("container:", vis_container);

            // Wait for both the container and vis library to be ready
            if (typeof vis !== 'undefined' && vis_container) {
                console.log("vis and container are available");
                
                // Create the data
                const nodes = new vis.DataSet([
                    { id: 1, label: "Node 1" },
                    { id: 2, label: "Node 2" },
                    { id: 3, label: "Node 3" },
                    { id: 4, label: "Node 4" },
                    { id: 5, label: "Node 5" }
                ]);
                
                const edges = new vis.DataSet([
                    { from: 1, to: 3 },
                    { from: 1, to: 2 },
                    { from: 2, to: 4 },
                    { from: 2, to: 5 },
                    { from: 3, to: 3 }
                ]);

                const data = { nodes: nodes, edges: edges };
                const options = {
                    nodes: { shape: "dot", size: 30, font: { size: 14, face: "Tahoma" }, borderWidth: 2, shadow: true },
                    edges: { width: 2, shadow: true },
                    interaction: { hover: true, tooltipDelay: 200 }
                };
                
                // Create the network
                try {
                    state.network = new vis.Network(vis_container, data, options);
                    console.log("Network initialized successfully.");
                } catch (e) {
                    console.error("Error initializing network:", e);
                }
            } else {
                console.error("vis or container not available:", { 
                    "vis": typeof vis, 
                    "container": Boolean(vis_container) 
                });
            }
        """
    }

    # Define the required JS module
    _modules = {'vis': 'https://cdn.jsdelivr.net/npm/vis-network@latest/dist/vis-network.min.js'}

    def __init__(self, **params):
        super().__init__(**params)

pn.extension()
app = VisNetPane(sizing_mode="stretch_width")
app.servable()