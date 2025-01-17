import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo
    import json
    import graphviz
    from rich import print

    __generated_with = "0.8.2"
    app = marimo.App(width="medium")
    return __generated_with, app, graphviz, json, marimo, print


@app.cell
def _(graphviz):
    def __():
        import marimo as mo
        dot = graphviz.Digraph(comment='Interactive Graph')

    return


@app.cell
def _(mo, print):
    def __():
        # Create input elements for node names
        node1 = mo.ui.text("Node 1 name", "A")
        node2 = mo.ui.text("Node 2 name", "B")

        # Create a button to add edge
        add_button = mo.ui.button("Add Edge")
        print ("created interfacce")
    return


@app.cell
def _(add_button, dot, node1, node2):
    def update_graph():
        # Add nodes and edge when button is clicked
        if add_button.value:
            dot.node(node1.value)
            dot.node(node2.value)
            dot.edge(node1.value, node2.value)

    return (update_graph,)


@app.cell
def _(add_button, mo, node1, node2, update_graph):

    dot1 = update_graph()
    mo.hstack([
            mo.vstack([node1, node2, add_button]),
            mo.markdown(dot1.source),
            dot1 ]
        )
    return (dot1,)



if __name__ == "__main__":
    app.run()
