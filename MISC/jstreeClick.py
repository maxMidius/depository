import panel as pn
import json

pn.extension()

# Define tree data
tree_data = [
    {
        "id": "root",
        "text": "Root",
        "children": [
            {"id": "folder1", "text": "Folder 1", "children": [
                {"id": "file1", "text": "File 1.txt"},
                {"id": "file2", "text": "File 2.txt"},
            ]},
            {"id": "folder2", "text": "Folder 2", "children": [
                {"id": "file3", "text": "File 3.txt"}
            ]}
        ]
    }
]

# Output area for logging
output = pn.pane.Markdown("## Click on nodes to see output here")

def create_node_button(node, level=0):
    """Recursively create clickable buttons for tree nodes"""
    
    def node_clicked(node_id, node_text):
        msg = f"**Node clicked:** {node_text} (ID: {node_id})\n\n"
        print(f"Node clicked: {node_id} - {node_text}")
        output.object = msg + output.object.replace("## Click on nodes to see output here", "").lstrip()
    
    items = []
    
    if node.get('children'):
        # Create an expander for parent nodes
        children_widgets = []
        for child in node['children']:
            children_widgets.append(create_node_button(child, level + 1))
        
        btn = pn.widgets.Button(
            name=f"▶ {node['text']}", 
            button_type='light',
            width=300
        )
        btn.on_click(lambda event: node_clicked(node['id'], node['text']))
        
        items.append(btn)
        items.extend(children_widgets)
    else:
        # Leaf node - just a button
        btn = pn.widgets.Button(
            name=f"• {node['text']}", 
            button_type='light',
            width=300
        )
        btn.on_click(lambda event, nid=node['id'], nt=node['text']: node_clicked(nid, nt))
        items.append(btn)
    
    if level > 0:
        # Indent child nodes
        return pn.Column(*items, margin=(0, 0, 0, level * 20))
    else:
        return pn.Column(*items)

# Build tree
tree_widgets = []
for node in tree_data:
    tree_widgets.append(create_node_button(node))

# Layout
pn.Column(
    pn.pane.Markdown('# Tree Example'),
    pn.Column(*tree_widgets),
    pn.pane.Markdown("---"),
    output,
    height=600
).servable()
