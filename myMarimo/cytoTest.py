import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():

    import dash
    import dash_cytoscape as cyto
    from IPython.display import display

    # Create a basic graph
    elements = [
        {'data': {'id': 'one', 'label': 'Node 1'}},
        {'data': {'id': 'two', 'label': 'Node 2'}},
        {'data': {'source': 'one', 'target': 'two'}}
    ]


    # Create the cytoscape object
    cytoscape_graph = cyto.Cytoscape(
        id='cytoscape-graph',
        elements=elements,
        layout={'name': 'grid'}
    )


    display(cytoscape_graph) 


    return cyto, cytoscape_graph, dash, display, elements


if __name__ == "__main__":
    app.run()
