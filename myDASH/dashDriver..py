from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Dataset URL Viewer", className="text-center mb-4"),
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
                        dbc.Button("Submit", id="submit-button", color="primary", className="mb-3"),
                        html.Div(id="iframe-container"),
                    ],
                    width=8,
                    className="mx-auto",
                )
            ]
        )
    ],
    fluid=True,
)

# Callback to update the text input when a dropdown option is selected
@app.callback(
    Output("dataset-url", "value"),
    Input("dataset-dropdown", "value"),
    prevent_initial_call=True,
)
def update_text_input(selected_url):
    return selected_url

# Callback to update the iframe with the Flask endpoint
@app.callback(
    Output("iframe-container", "children"),
    Input("submit-button", "n_clicks"),
    State("dataset-url", "value"),
    prevent_initial_call=True,
)
def update_iframe(n_clicks, dataset_url):
    if not dataset_url:
        return html.Div("Please enter or select a valid dataset URL.", className="text-danger")

    # Construct the Flask endpoint URL
    flask_endpoint = f"http://172.25.116.90:5000/external?url={dataset_url}"

    # Return an iframe with the Flask endpoint
    return html.Iframe(
        src=flask_endpoint,
        style={"width": "100%", "height": "600px", "border": "none"},
    )

# Run the Dash app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)