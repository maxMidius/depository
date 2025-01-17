import marimo
import ipycytoscape as cyto
import json

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return mo


@app.cell
def create_graph():
    elements = [
        {"data": {"id": "A", "label": "A"}},
        {"data": {"id": "B", "label": "B"}},
        {"data": {"id": "C", "label": "C"}},
        {"data": {"source": "A", "target": "B", "label": "A->B"}},
        {"data": {"source": "A", "target": "C", "label": "A->C"}},
    ]
    return elements


@app.cell
def _(mo, create_graph):
    selected_element = mo.state(None)
    return selected_element


@app.cell
def display_graph(create_graph, selected_element):
    def handle_click(element):
        if element:
           selected_element.value = element
           print(f'Element selected {json.dumps(element)}')  # logging if needed
           selected_element.batch()

    graph_widget = cyto.CytoscapeWidget()
    graph_widget.graph.add_elements(create_graph())

    graph_widget.on("node", "click", lambda ele: handle_click(ele.data))
    graph_widget.on("edge", "click", lambda ele: handle_click(ele.data))
    return graph_widget


@app.cell
def display_selection(selected_element):
    if selected_element.value:
        return f"Selected element: {selected_element.value}"
    else:
        return "No element selected"

if __name__ == "__main__":
    app.run()
