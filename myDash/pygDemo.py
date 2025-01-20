import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pygwalker as pyg
import io
import base64  # Add base64 import

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Container([
        html.H1("PyGWalker Data Visualization", className="text-center my-4"),
        
        # File Upload Component
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        
        # Data Preview
        html.Div(id='output-data-upload'),
        
        # PyGWalker Visualization
        html.Div(id='pygwalker-viz')
    ])
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df
    except Exception as e:
        print(e)
        return None

@app.callback(
    Output('pygwalker-viz', 'children'),
    Input('upload-data', 'contents')
)
def update_output(contents):
    if contents is None:
        return html.Div("Upload a CSV file to begin visualization")
    
    df = parse_contents(contents)
    if df is not None:
        # Generate PyGWalker visualization
        walker = pyg.walk(df)
        viz_html = walker.to_html()
        return html.Iframe(
            srcDoc=viz_html,
            style={'width': '100%', 'height': '800px', 'border': 'none'}
        )
    
    return html.Div("Error processing file")

if __name__ == '__main__':
    app.run_server(debug=True)