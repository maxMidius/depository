from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pygwalker as pyg
import dtale
from flask import Flask, redirect
from dtale.app import build_app
from dtale.views import startup
import threading

# Initialize the Dash app
dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Predefined datasets with human-readable names and URLs
DATASETS = {
    "Titanic Dataset": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
    "Wine Quality Dataset": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    "Diabetes Dataset": "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv",
    "Air Quality Dataset": "https://raw.githubusercontent.com/vaibhavwalvekar/Air-Quality-Prediction/master/AirQualityUCI.csv",
    "California Housing Dataset": "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv",
    "Pokémon Dataset": "https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv",
    "Netflix Movies and TV Shows Dataset": "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv",
    "World Happiness Report Dataset": "https://raw.githubusercontent.com/datasets/world-happiness-report/master/data-2023/WHR2023.csv",
    "COVID-19 Dataset": "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv",
    "IMDB Movies Dataset": "https://raw.githubusercontent.com/datasets/imdb-movie-data/master/movie_metadata.csv",
    "Superstore Sales Dataset": "https://raw.githubusercontent.com/plotly/datasets/master/superstore.csv",
    "New York City Airbnb Dataset": "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-07-02/nyc_airbnb.csv",
    "Global Terrorism Dataset": "https://raw.githubusercontent.com/plotly/datasets/master/global_terrorism.csv",
    "Olympics Dataset": "https://raw.githubusercontent.com/rgriff23/Olympic_history/master/data/athlete_events.csv",
    "Cereal Dataset": "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-01-09/cereal.csv",
}

# Layout of the Dash app
dash_app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Data Visualization", className="text-center mb-4"),
                        dcc.Tabs(
                            id="tabs",
                            value="tab-pygwalker",
                            children=[
                                dcc.Tab(label="PygWalker", value="tab-pygwalker"),
                                dcc.Tab(label="Dtale", value="tab-dtale"),
                            ],
                            className="mb-3",
                        ),
                        html.Div(id="tabs-content"),
                    ],
                    width=10,
                    className="mx-auto",
                )
            ]
        )
    ],
    fluid=True,
)

# Callback to render the content of the selected tab
@dash_app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value"),
)
def render_tab_content(selected_tab):
    if selected_tab == "tab-pygwalker":
        return dbc.Container(
            [
                dbc.Label("Select a predefined dataset:"),
                dcc.Dropdown(
                    id="dataset-dropdown",
                    options=[{"label": name, "value": url} for name, url in DATASETS.items()],
                    placeholder="Select a dataset...",
                    className="mb-3",
                ),
                dbc.Label("Or enter a custom dataset URL:"),
                dbc.Input(
                    id="dataset-url",
                    type="text",
                    placeholder="Enter dataset URL...",
                    className="mb-3",
                ),
                dbc.Button("Visualize", id="visualize-button", color="primary", className="mb-3"),
                dbc.Spinner(html.Div(id="pygwalker-container"), color="primary"),
                html.Div(id="dataset-title", className="mt-3"),
            ]
        )
    elif selected_tab == "tab-dtale":
        # Embed Dtale in an iframe
        return html.Iframe(
            src="http://localhost:8080",  # Dtale runs on port 8080
            style={"width": "100%", "height": "800px", "border": "none"},
        )

# Callback to update the text input when a dropdown option is selected
@dash_app.callback(
    Output("dataset-url", "value"),
    Input("dataset-dropdown", "value"),
    prevent_initial_call=True,
)
def update_text_input(selected_url):
    return selected_url

# Callback to load the dataset and render PygWalker visualization
@dash_app.callback(
    [Output("pygwalker-container", "children"), Output("dataset-title", "children")],
    Input("visualize-button", "n_clicks"),
    [State("dataset-url", "value"), State("dataset-dropdown", "value")],
    prevent_initial_call=True,
)
def render_pygwalker(n_clicks, dataset_url, dropdown_value):
    if not dataset_url:
        return html.Div("Please enter or select a valid dataset URL.", className="text-danger"), ""

    try:
        # Load the dataset from the URL
        df = pd.read_csv(dataset_url)

        # Generate PygWalker HTML
        walker = pyg.walk(df, spec="./gw_config.json", debug=False)
        html_content = walker.to_html()

        # Determine the dataset name
        dataset_name = next((name for name, url in DATASETS.items() if url == dataset_url), "Custom Dataset")

        # Return the PygWalker HTML as an iframe and the dataset title
        return (
            html.Iframe(
                srcDoc=html_content,
                style={"width": "100%", "height": "800px", "border": "none"},
            ),
            html.H3(f"Visualizing: {dataset_name}", className="text-center"),
        )

    except Exception as e:
        return html.Div(f"Error loading dataset: {str(e)}", className="text-danger"), ""

# Function to run the Dtale Flask app
def run_dtale():
    dtale_flask_app = build_app(reaper_on=False)

    @dtale_flask_app.route("/create-df")
    def create_df():
        df = pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))
        instance = startup("", data=df, ignore_duplicate=True)
        return redirect(f"/dtale/main/{instance._data_id}", code=302)

    @dtale_flask_app.route("/")
    def hello_world():
        return 'Hi there, load data using <a href="/create-df">create-df</a>'

    dtale_flask_app.run(host="0.0.0.0", port=8080)

# Run the Dtale Flask app in a separate thread
dtale_thread = threading.Thread(target=run_dtale)
dtale_thread.daemon = True
dtale_thread.start()

# Run the Dash app
if __name__ == "__main__":
    dash_app.run_server(host="0.0.0.0", port=8050, debug=True)