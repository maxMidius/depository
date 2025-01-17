import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import networkx as nx
    import plotly.graph_objects  as go
    return go, mo, nx


@app.cell
def graph_with_click(nx, plt):
    def create_graph():
        """Creates a graph visualization with clickable nodes."""
        def handle_click(node):
            print(f"Clicked node: {node}")

        G = nx.DiGraph()
        G.add_node("A", pos=(0, 0), on_click=lambda : handle_click("A"))
        G.add_node("B", pos=(1, 1), on_click=lambda : handle_click("B"))
        G.add_node("C", pos=(1, -1), on_click=lambda : handle_click("C"))
        G.add_edge("A", "B")
        G.add_edge("A", "C")

        pos = nx.get_node_attributes(G, 'pos')
        on_click_handlers = nx.get_node_attributes(G, 'on_click')

        fig, ax = plt.subplots()
        nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", arrowsize=20, ax=ax)

        def onclick_handler(event):
           if event.inaxes == ax:
              for node, coords in pos.items():
                x,y = ax.transData.transform(coords)
                if abs(event.x - x) < 20 and abs(event.y - y) < 20: # Click within the bounding box
                    on_click_handlers[node]() #execute the corresponding on_click handler
                    break
        fig.canvas.mpl_connect('button_press_event', onclick_handler)
        return fig
    return (create_graph,)


@app.cell
def _(create_graph):
    fig = create_graph()
    fig
    return (fig,)


if __name__ == "__main__":
    app.run()
