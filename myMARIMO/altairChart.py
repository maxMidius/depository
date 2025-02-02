import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo 
    import altair as alt
    import pandas as pd

    return alt, mo, pd


@app.cell
def _(alt, mo, pd):
    # Sample data
    data = {'x': [1, 2, 3, 4, 5], 'y': [2, 5, 3, 1, 4]}
    df1 = pd.DataFrame(data)

    # Create the Altair chart (small and interactive)
    chart = alt.Chart(df1).mark_point().encode(
        x='x',
        y='y'
    ).properties(
        width=200,  # Set a small width
        height=150  # Set a small height
    )

    # Render the chart in Marimo using 'mo.ui.altair_chart'
    clickable_graph = mo.ui.altair_chart(chart)
    clickable_graph
    return chart, clickable_graph, data, df1


if __name__ == "__main__":
    app.run()
