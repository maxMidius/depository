from dash import html, dcc, Dash, Input, Output, State, callback_context as ctx
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

# Define menu items
menu_items = [
    dbc.NavItem(dbc.NavLink("Home", href="/", id="nav-home")),
    dbc.NavItem(dbc.NavLink("Gallery", href="/gallery", id="nav-gallery")),
    dbc.NavItem(dbc.NavLink("Workings", href="/workings", id="nav-workings"))
]

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='active-menu', storage_type='session'),
    
    # Combined Banner and Menu Row
    dbc.Row([
        # Banner Column - Combined Icon and Title
        dbc.Col([
            html.Div([
                html.I(className="fas fa-cubes fa-3x w3-text-white w3-blue-grey w3-round me-3"),
                html.H2("TNT for Surveillance Studio", 
                       className="w3-blue-grey w3-round d-inline-block mb-0")
            ], className="d-flex align-items-center")
        ], width=6),
        
        # Menu Column
        dbc.Col([
            dbc.Nav(
                menu_items,
                className="w3-bar w3-round-large w3-light-grey"
            )
        ], width=6)
    ], className="mb-4"),
    
    # Content Area
    dbc.Row([
        dbc.Col(
            id="page-content",
            className="w3-round-large"
        )
    ])
])

@app.callback(
    [Output(f"nav-{page}", "className") for page in ["home", "gallery", "workings"]],
    Input("url", "pathname")
)
def update_active_menu(pathname):
    classes = []
    paths = {"/": "home", "/gallery": "gallery", "/workings": "workings"}
    
    for page in ["home", "gallery", "workings"]:
        if pathname == [k for k,v in paths.items() if v == page][0]:
            classes.append("nav-link active w3-blue-grey")
        else:
            classes.append("nav-link")
    return classes

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