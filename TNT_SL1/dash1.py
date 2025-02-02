import dash
import dash_cytoscape as cyto
from dash import html, Input, Output

app = dash.Dash(__name__)


nodes = [
    {'data': {'id': 'center', 'label': 'Main Topic'}},
    {'data': {'id': 'sub1', 'label': 'Subtopic 1'}},
    {'data': {'id': 'sub2', 'label': 'Subtopic 2'}},
    {'data': {'id': 'sub1_1', 'label': 'Detail 1.1'}},
    {'data': {'id': 'sub1_2', 'label': 'Detail 1.2'}},
    {'data': {'id': 'sub2_1', 'label': 'Detail 2.1'}},
]
edges = [
    {'data': {'source': 'center', 'target': 'sub1'}},
    {'data': {'source': 'center', 'target': 'sub2'}},
    {'data': {'source': 'sub1', 'target': 'sub1_1'}},
    {'data': {'source': 'sub1', 'target': 'sub1_2'}},
    {'data': {'source': 'sub2', 'target': 'sub2_1'}},
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-mindmap',
        elements=nodes + edges,
        style={'width': '600px', 'height': '400px'},
        layout={'name': 'breadthfirst', 'roots': '[id = "center"]'}
    ),
    html.Div(id='clicked-node')
])

@app.callback(
    Output('clicked-node', 'children'),
    Input('cytoscape-mindmap', 'tapNodeData')
)
def display_clicked_node(data):
    if data:
        return f"You clicked: {data['label']}"
    return "Click a node"

if __name__ == '__main__':
    app.run_server(debug=True)


