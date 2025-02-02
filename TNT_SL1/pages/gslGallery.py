from dash import html, Dash
import dash_bootstrap_components as dbc

def layout():
    return html.Div([
        html.H1("GSL Gallery", className='w3-blue w3-round-large')
    ])

if __name__ == '__main__':
    app = Dash(__name__, 
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.icons.FONT_AWESOME,
            "https://www.w3schools.com/w3css/4/w3.css"
        ]
    )
    app.layout = layout()
    app.run_server(debug=True, port=8051)  # Different port than multiApp