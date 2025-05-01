import panel as pn
from panel.custom import JSComponent

class VisNetApp(JSComponent):
    _stylesheets = []

    _esm = """
    import vis from "https://cdn.jsdelivr.net/npm/vis-network@latest/dist/vis-network.esm.js"

    export function render(model, el) {
      // Create container for the network
      const container = document.createElement("div");
      container.id = "mynetwork";
      container.style.width = "600px";
      container.style.height = "400px";
      container.style.border = "1px solid lightgray";
      el.appendChild(container);

      // Define nodes and edges
      const nodes = new vis.DataSet([
        { id: 1, label: "Node 1" },
        { id: 2, label: "Node 2" },
        { id: 3, label: "Node 3" },
        { id: 4, label: "Node 4" },
        { id: 5, label: "Node 5" },
      ]);
      const edges = new vis.DataSet([
        { from: 1, to: 3 },
        { from: 1, to: 2 },
        { from: 2, to: 4 },
        { from: 2, to: 5 },
        { from: 3, to: 3 },
      ]);

      // Create network
      const data = { nodes: nodes, edges: edges };
      const options = {
        nodes: { shape: "dot", size: 30, font: { size: 14, face: "Tahoma" }, borderWidth: 2, shadow: true },
        edges: { width: 2, shadow: true },
        interaction: { hover: true, tooltipDelay: 200 }
      };
      const network = new vis.Network(container, data, options);

      // Hover event
      network.on("hoverNode", function(params) {
        console.log("Hovering over node: " + nodes.get(params.node).label);
      });
    }
    """

# Create and serve the Panel app
pn.extension()
app = VisNetApp()
pn.Column(app).servable()