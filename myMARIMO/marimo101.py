import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import graphviz
    from graphviz_anywidget import graphviz_widget
    import numpy as np
    import wigglystuff
    from IPython.display import SVG, display
    return SVG, display, graphviz, graphviz_widget, mo, np, wigglystuff


@app.cell
def _(graphviz):
    # Create a new directed graph
    dot = graphviz.Digraph(comment='Example Graph')

    # Add two nodes A and B
    dot.node('A', 'A')
    dot.node('B', 'B')

    # Add edge from A to B
    dot.edge('A', 'B')

    # Display the graph - use _repr_svg_() to get the SVG representation
    svg_code = dot.pipe(format='svg').decode('utf-8')
    svg_code
    return dot, svg_code


if __name__ == "__main__":
    app.run()
