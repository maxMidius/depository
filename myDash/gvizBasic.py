import dash_interactive_graphviz
from dash import Dash, html, dcc, Input, Output, callback

app = Dash()

dot_source = """
digraph  {
  node[style="filled"]
  a ->b->d
  a->c->d
}
"""

app.layout = html.Div([
    dash_interactive_graphviz.DashInteractiveGraphviz(
        id="graph",
        dot_source=dot_source
    ),
    html.Div(id='output-div')
])


@app.callback(
    Output('output-div', 'children'),
    [Input('graph', 'selected_node')]
)

def change_my_view(selected):
    # Do something with selected
    print(selected)
    if selected:
        return f"Selected node: {selected}"
    else:
        return "No node selected"

if __name__ == '__main__':
    app.run_server(debug=True)