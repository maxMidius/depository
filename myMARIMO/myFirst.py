import marimo

__generated_with = "0.10.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from ipyaggrid import Grid
    import pandas as pd
    return Grid, mo, pd


@app.cell
def _():
    # Sample DataFrame
    data1 = {'name': ['John Doe', 'Jane Smith', 'David Lee'], 
            'age': [30, 25, 35], 
            'city': ['New York', 'London', 'Paris']}
    return (data1,)


@app.cell
def _():
    data2 = {
        "projectId": "P1",
        "projectName": "Project A",
        "deliverables": [
            {
                "deliverableId": f"D{i}",
                "deliverableName": f"Deliverable {chr(65+i)}",
                "tasks": [
                    {
                        "taskId": f"T{i}{j}",
                        "taskName": f"Task {chr(65+i)}{j+1}",
                        "status": ["In Progress", "Completed", "Pending"][j % 3],
                    }
                    for j in range(6)
                ],
            }
            for i in range(6)
        ],
    }
    return (data2,)


@app.cell
def _():
    import anywidget
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          let button = document.createElement("button");
          button.innerHTML = `count is ${model.get("value")}`;
          button.addEventListener("click", () => {
            model.set("value", model.get("value") + 1);
            model.save_changes();
          });
          model.on("change:value", () => {
            button.innerHTML = `count is ${model.get("value")}`;
          });
          el.classList.add("counter-widget");
          el.appendChild(button);
        }
        export default { render };
        """
        _css = """
        .counter-widget button { color: white; font-size: 1.75rem; background-color: #ea580c; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; }
        .counter-widget button:hover { background-color: #9a3412; }
        """
        value = traitlets.Int(0).tag(sync=True)

    CounterWidget(value=42)
    return CounterWidget, anywidget, traitlets


@app.cell
def _(mo):
    from jupyter_anywidget_graphviz import GraphvizAnywidgetMagic

    # Define a simple Graphviz diagram
    dot_source = """
    digraph G {
        A -> B;
        B -> C;
        C -> A;
        D -> A;
    }
    """

    # Create a Graphviz widget
    graphviz_widget = GraphvizAnywidgetMagic(dot_source)

    # Display the widget
    mo.Html(graphviz_widget)
    return GraphvizAnywidgetMagic, dot_source, graphviz_widget


@app.cell
def _(mo):
    sl1 = mo.ui.slider(1,10,1)
    sl1
    return (sl1,)


@app.cell
def _(mo, sl1):
    def but1Handler(val) :
        print (f"clicked {val} {sl1.value}")

    sl1.callout(kind='danger')

    but1=mo.ui.button(label="Hello", on_click = but1Handler("JJJ"))
    but1
    return but1, but1Handler


@app.cell
def _(mo, pd):
    #import marimo as mo
    import pygwalker as pyg

    # Create a sample Pandas DataFrame
    data = {'col1': [1, 2, 3, 4, 5], 'col2': ['A', 'B', 'A', 'C', 'B']}
    df = pd.DataFrame(data)

    # Generate the PygWalker visualization
    gwalker = pyg.walk(df)

    # Get the HTML from pygwalker's to_html() method
    html_content = gwalker.to_html()

    # Display the HTML in Marimo using mo.html
    mo.Html(html_content)
    return data, df, gwalker, html_content, pyg


@app.cell
def _():
    #from ipyaggrid import Grid
    import ipywidgets
    from IPython.display import display

    # Sample data
    data5 = [
        {"Name": "Alice", "Age": 25, "City": "New York"},
        {"Name": "Bob", "Age": 30, "City": "San Francisco"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"},
    ]

    # Grid options
    grid_options1 = {
        "columnDefs": [
            {"headerName": "Name", "field": "Name"},
            {"headerName": "Age", "field": "Age"},
            {"headerName": "City", "field": "City"},
        ],
        "rowData": data5,
    }
    button = ipywidgets.Button(description="Click Me")
    display(button)
    # Create and display the grid
    #grid1 = Grid(grid_options=grid_options1)
    #display(grid1)
    return button, data5, display, grid_options1, ipywidgets


@app.cell
def _():
    struct1 = { "a": 10  ,  "b":15}
    return (struct1,)


@app.cell
def _(struct1):
    struct1.update({"b": 10 , "c": 100})
    struct1
    return


if __name__ == "__main__":
    app.run()
