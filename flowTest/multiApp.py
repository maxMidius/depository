from dash import html, dcc, Dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from pages import landingPage, gslGallery, gslWorkings, dataExplorer

# Initialize app with correct external stylesheets
app = Dash(__name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        "https://www.w3schools.com/w3css/4/w3.css"
    ]
)

# Layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='sidebar-state', data=True),  # Track sidebar state
    dbc.Row([
        dbc.Col(
            html.Button("☰", id="sidebar-toggle", className="w3-button w3-xlarge"),
            width=1
        ),
        # Update icon with amber background
        dbc.Col(
            html.I(className="fas fa-cubes fa-3x w3-text-white w3-grey w3-round ") ,
            width=1,
        ),
        dbc.Col(
            html.H4("TNT for Surveillance Studio", className="w3-xlarge w3-text-white"),
            width=9
        ),
    ],
    className="w3-blue-grey w3-padding w3-round-large w3-margin-bottom",
    justify="between"),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.A("About", 
                        href="/", 
                        className="w3-bar-item w3-button w3-round-large",
                        id="home-link",
                        style={"color": "black"}),
                    html.A("Gallery", 
                        href="/gallery", 
                        className="w3-bar-item w3-button w3-round-large",
                        id="gallery-link",
                        style={"color": "black"}),
                    html.A("Workings", 
                        href="/workings", 
                        className="w3-bar-item w3-button w3-round-large",
                        id="workings-link",
                        style={"color": "black"}),

                ],
                className="w3-bar-block w3-round-large")
            ],
            id="sidebar",
            className="w3-light-grey w3-round-large",
            style={"padding": "2px"})   # Added custom padding
        ],
        width=2),
        dbc.Col(
            id="page-content", 
            width=10,
            className="w3-round-large"
        )
    ])
])

# Add sidebar toggle callback
@app.callback(
    [Output("sidebar", "style"),
     Output("sidebar-state", "data"),
     Output("page-content", "width")],  # Add width control for content
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar-state", "data")
)
def toggle_sidebar(n_clicks, is_visible):
    if n_clicks is None:
        return {"display": "block"}, True, 10  # Default width with sidebar
    if is_visible:
        return {"display": "none"}, False, 12  # Full width when sidebar hidden
    return {"display": "block"}, True, 10  # Normal width when sidebar shown

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return landingPage.layout()
    elif pathname == "/gallery":
        return gslGallery.layout()
    elif pathname == "/workings":
        return gslWorkings.layout()
    elif pathname == "/explore":
        layout_func, callbacks = dataExplorer.explore_dataset()
        callbacks(app)
        return layout_func()
    return html.Div("404 - Not found", className="p-3 bg-light")

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)