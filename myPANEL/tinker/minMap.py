import panel as pn
import networkx as nx
import param
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, MultiLine, TapTool, HoverTool, ColumnDataSource, LabelSet

# Initialize extensions
pn.extension()

# Create a sample NetworkX graph with more variety
G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D", "E"]) 
G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "E"), ("C", "E")])

# Create the Bokeh figure
plot = figure(width=600, height=400, tools="pan,box_zoom,reset,save", title="Interactive Node Graph")

# Create the output text display
output_text = pn.pane.Markdown("**Click on nodes to select them**")

# Create graph renderer
graph = GraphRenderer()

# Set node properties with colors as a data field for dynamic updating
node_source = ColumnDataSource(data=dict(
    index=list(range(len(G.nodes()))),
    name=list(G.nodes()),
    colors=['red'] * len(G.nodes()),
    border_colors=['black'] * len(G.nodes()),
    border_width=[1] * len(G.nodes()),
    node_sizes=[15] * len(G.nodes())  # Store node radius values
))
graph.node_renderer.data_source = node_source

# Use field mapping for multiple attributes
graph.node_renderer.glyph = Circle(
    radius="node_sizes",
    fill_color="colors",
    line_color="border_colors",
    line_width="border_width"
)
graph.node_renderer.selection_glyph = Circle(radius=15, fill_color="orange")
graph.node_renderer.hover_glyph = Circle(radius=15, fill_color="yellow")
graph.node_renderer.nonselection_glyph = Circle(radius=15, fill_color="gray", fill_alpha=0.5)

# Set edge properties
edges = list(G.edges())
edge_source = ColumnDataSource(data=dict(
    start=[list(G.nodes()).index(start) for start, end in edges],
    end=[list(G.nodes()).index(end) for start, end in edges],
    edge_names=[f"{start}-{end}" for start, end in edges]
))

graph.edge_renderer.data_source = edge_source
graph.edge_renderer.glyph = MultiLine(line_width=2, line_color="gray")

# Set up the layout
layout = nx.spring_layout(G)
graph_layout = {i: (layout[node][0]*200, layout[node][1]*200) for i, node in enumerate(G.nodes())}
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

# Add the graph renderer to the plot
plot.renderers.append(graph)

# Add node labels
x_coords = []
y_coords = []
names = []

for i, node_name in enumerate(G.nodes()):
    x, y = graph_layout[i]
    x_coords.append(x)
    y_coords.append(y)
    names.append(node_name)

# Create a separate source for labels
label_source = ColumnDataSource(data=dict(
    x=x_coords,
    y=y_coords,
    names=names
))

# Add labels with custom styling
labels = LabelSet(
    x='x', y='y', text='names',
    source=label_source, 
    text_font_size='12pt',
    text_color='white',
    x_offset=-5,  # Center horizontally
    y_offset=-5   # Center vertically
)
plot.add_layout(labels)

# Add hover tools for nodes only
node_hover = HoverTool(tooltips=[("Node", "@name")], renderers=[graph.node_renderer])
plot.add_tools(node_hover)

# Add tap tool for selection (using multi behavior to select multiple nodes)
tap_tool = TapTool(behavior="select")
plot.add_tools(tap_tool)

# Create a ParameterizedClass to manage node selection
class GraphExample(param.Parameterized):
    selected_node = param.String(default="Nothing selected")
    new_label = param.String(default="")
    
    def __init__(self, graph, **params):
        super().__init__(**params)
        self.graph = graph
        self.nodes = list(graph.nodes())
        # Store original appearance
        self.original_colors = ['red'] * len(G.nodes())
        self.original_borders = ['black'] * len(G.nodes())
        self.original_widths = [1] * len(G.nodes())
        self.original_sizes = [15] * len(G.nodes())
        
    def make_green(self, event):
        """Turn selected nodes green"""
        indices = node_source.selected.indices
        if indices:
            colors = list(node_source.data['colors'])
            for idx in indices:
                colors[idx] = 'green'
            
            # Update the data source
            node_source.data['colors'] = colors
            self.selected_node = f"Changed {len(indices)} nodes to green"
            
            # Clear selection so we can see the color change
            node_source.selected.indices = []
        else:
            self.selected_node = "No nodes selected to change color"
    
    def make_yellow(self, event):
        """Turn selected nodes yellow"""
        indices = node_source.selected.indices
        if indices:
            colors = list(node_source.data['colors'])
            for idx in indices:
                colors[idx] = 'yellow'
            
            # Update the data source
            node_source.data['colors'] = colors
            self.selected_node = f"Changed {len(indices)} nodes to yellow"
            
            # Clear selection so we can see the color change
            node_source.selected.indices = []
        else:
            self.selected_node = "No nodes selected to change color"
    
    def blue_border(self, event):
        """Make selected nodes have blue border"""
        indices = node_source.selected.indices
        if indices:
            borders = list(node_source.data['border_colors'])
            widths = list(node_source.data['border_width'])
            for idx in indices:
                borders[idx] = 'blue'
                widths[idx] = 3  # Make border thicker
            
            # Update the data source
            node_source.data['border_colors'] = borders
            node_source.data['border_width'] = widths
            self.selected_node = f"Changed {len(indices)} node borders to blue"
            
            # Clear selection
            node_source.selected.indices = []
        else:
            self.selected_node = "No nodes selected to change border"
    
    def increase_size(self, event):
        """Make selected nodes larger"""
        indices = node_source.selected.indices
        if indices:
            sizes = list(node_source.data['node_sizes'])
            for idx in indices:
                # Increase size by 5, up to a maximum of 30
                sizes[idx] = min(sizes[idx] + 5, 30)
            
            # Update the data source
            node_source.data['node_sizes'] = sizes
            self.selected_node = f"Increased size of {len(indices)} nodes"
            
            # Clear selection
            node_source.selected.indices = []
        else:
            self.selected_node = "No nodes selected to resize"
    
    def reset_all(self, event):
        """Reset all properties to original values"""
        node_source.data['colors'] = self.original_colors.copy()
        node_source.data['border_colors'] = self.original_borders.copy()
        node_source.data['border_width'] = self.original_widths.copy()
        node_source.data['node_sizes'] = self.original_sizes.copy()
        self.selected_node = "Reset all node properties"
        
        # Clear selection
        node_source.selected.indices = []
        
    def change_labels(self, event):
        """Change the labels of selected nodes to the text in the input field"""
        indices = node_source.selected.indices
        if indices and self.new_label:
            new_labels = list(label_source.data['names'])
            
            for idx in indices:
                new_labels[idx] = self.new_label
            
            # Update the data source for labels
            label_source.data['names'] = new_labels
            self.selected_node = f"Changed labels for {len(indices)} nodes to '{self.new_label}'"
            
            # Clear selection
            node_source.selected.indices = []
        else:
            if not indices:
                self.selected_node = "No nodes selected to change labels"
            elif not self.new_label:
                self.selected_node = "Please enter a new label"
        
    def view(self):
        # Create output using Markdown pane
        output_text = pn.pane.Markdown(f"**{self.selected_node}**")
        
        # Define a function to update the output text
        def update_output(event):
            output_text.object = f"**{event.new}**"
        
        # Bind the output to the selected_node parameter
        self.param.watch(update_output, 'selected_node')
        
        # Node selection handling
        node_source.selected.on_change('indices', 
            lambda attr, old, new: self._handle_node_selection(new)
        )
        
        # Create action buttons
        green_button = pn.widgets.Button(name="Green Fill", button_type="success")
        green_button.on_click(self.make_green)
        
        yellow_button = pn.widgets.Button(name="Yellow Fill", button_type="warning")
        yellow_button.on_click(self.make_yellow)
        
        border_button = pn.widgets.Button(name="Blue Border", button_type="primary")
        border_button.on_click(self.blue_border)
        
        size_button = pn.widgets.Button(name="Increase Size", button_type="primary")
        size_button.on_click(self.increase_size)
        
        reset_button = pn.widgets.Button(name="Reset All", button_type="danger")
        reset_button.on_click(self.reset_all)
        
        label_button = pn.widgets.Button(name="Change Labels", button_type="primary")
        label_button.on_click(self.change_labels)
        
        label_input = pn.widgets.TextInput(name="New Label", value="")
        label_input.param.watch(lambda event: setattr(self, 'new_label', event.new), 'value')
        
        # Return the layout with two rows of buttons
        return pn.Column(
            pn.pane.Markdown("## Interactive Node Graph"),
            pn.pane.Markdown("Click on nodes to select them (hold Shift for multiple)"),
            pn.pane.Bokeh(plot),
            pn.pane.Markdown("### Node Fill:"),
            pn.Row(green_button, yellow_button),
            pn.pane.Markdown("### Node Properties:"),
            pn.Row(border_button, size_button, label_button, reset_button),
            label_input,
            output_text
        )
        
    def _handle_node_selection(self, indices):
        print(f"Node selection event with indices: {indices}")
        if indices:
            try:
                # Get all selected node names
                selected_names = [self.nodes[idx] for idx in indices if idx < len(self.nodes)]
                
                if selected_names:
                    self.selected_node = f"Selected nodes: {', '.join(selected_names)}"
                else:
                    self.selected_node = f"Unknown node indices: {indices}"
            except Exception as e:
                self.selected_node = f"Node selection error: {str(e)}"
                print(f"Error in node selection: {e}")
        else:
            self.selected_node = "Nothing selected"

# Create the app instance
graph_app = GraphExample(G)

# Get the view and make it servable
app = graph_app.view()
app.servable("Interactive Node Graph")