import marimo

__generated_with = "0.10.7"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import graphviz
    from graphviz_anywidget import GraphvizAnyWidget

@app.cell
def setup_inputs():
    # Create input elements
    source = mo.input("Source Node", "A")
    target = mo.input("Target Node", "B")
    add_button = mo.button("Add Edge")
    return source, target, add_button

@app.cell
def create_graph():
    # Initialize the graph
    dot = graphviz.Digraph(comment='Interactive Graph')
    dot.attr(rankdir='LR')  # Left to right layout
    return dot

@app.cell
def update_graph(dot, source, target, add_button):
    # Add nodes and edge when button is clicked
    if add_button.value:
        dot.node(source.value, source.value)
        dot.node(target.value, target.value)
        dot.edge(source.value, target.value)

    # Create widget and display
    widget = GraphvizAnyWidget(dot)
    return widget

@app.cell
def layout():
    # Get input elements
    source, target, add_button = setup_inputs()

    # Create and update graph
    dot = create_graph()
    widget = update_graph(dot, source, target, add_button)

    # Arrange elements in layout
    return mo.hstack([
        mo.vstack([
            mo.md("### Add Nodes and Edges"),
            source,
            target,
            add_button
        ]),
        mo.vstack([
            mo.md("### Graph Visualization"),
            widget
        ])
    ])

if __name__ == "__main__":
    app.run()
