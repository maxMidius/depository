from dash import Dash, html, dcc
import dash_cytoscape as cyto
import json

app = Dash(__name__)

# Initial elements
elements = [
    # Nodes
    {'data': {'id': '1', 'label': 'Node 1'}, 'position': {'x': 100, 'y': 100}},
    {'data': {'id': '2', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
    # Edges
    {'data': {'source': '1', 'target': '2', 'label': 'connects to'}}
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='graph',
        elements=elements,
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'label': 'data(label)',
                    'curve-style': 'bezier'
                }
            }
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)