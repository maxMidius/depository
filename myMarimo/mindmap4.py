import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from graphviz_anywidget import GraphvizAnyWidget
    return GraphvizAnyWidget, mo


@app.cell
def _(GraphvizAnyWidget, mo):
    # Create a simple graph
    dot_source = """
    digraph G {
        A -> B;
        B -> C;
        C -> A;
    }
    """
    # Create the GraphvizWidget
    graph_widget = GraphvizAnyWidget(dot_source=dot_source)
    # Display the widget in the marimo notebook
    mo.ui.anywidget(GraphvizAnyWidget(dot_source=dot_source)) 

    return dot_source, graph_widget


if __name__ == "__main__":
    app.run()
