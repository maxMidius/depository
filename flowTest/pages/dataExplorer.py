from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_pivottable import PivotTable
from sklearn.datasets import load_iris
import pandas as pd
import plotly.express as px

def get_default_dataset():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    return df

def create_layout(df):
    return html.Div([
        html.H3("Dataset Explorer", className="w3-text-blue-grey w3-padding"),
        dbc.Tabs([
            # Tab 1: Scatter Plot
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("Scatter Plot Controls"),
                        dcc.Dropdown(id='x-axis', 
                                   options=[{'label': col, 'value': col} for col in df.columns], 
                                   value=df.columns[0], className='mb-2'),
                        dcc.Dropdown(id='y-axis',
                                   options=[{'label': col, 'value': col} for col in df.columns],
                                   value=df.columns[1], className='mb-2'),
                        dcc.Dropdown(id='color-by',
                                   options=[{'label': col, 'value': col} for col in df.columns],
                                   value=df.columns[-1], className='mb-2')
                    ], width=3),
                    dbc.Col([dcc.Graph(id='scatter-plot')], width=9)
                ])
            ], label="Scatter Plot"),
            
            # Tab 2: Box Plot
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        html.H4("Box Plot Controls"),
                        dcc.Dropdown(
                            id='box-feature',
                            options=[{'label': col, 'value': col} for col in df.columns if col != 'species'],
                            value=df.columns[0],
                            className='mb-2'
                        )
                    ], width=3),
                    dbc.Col([dcc.Graph(id='box-plot')], width=9)
                ])
            ], label="Box Plot"),
            
            # Tab 3: Data Table
            dbc.Tab([
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    sort_action="native",
                    filter_action="native",
                    page_size=10
                )
            ], label="Data Table"),
            
            # Tab 4: Pivot Table
            dbc.Tab([
                PivotTable(
                    id='pivot-table',
                    data=df.to_dict('records'),
                    cols=['species'],
                    rows=[df.columns[0]],
                    vals=['sepal length (cm)'],
                    aggregatorName='Average',
                    rendererName='Heatmap'
                )
            ], label="Pivot Table")
        ])
    ])

def init_callbacks(app, df):
    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('x-axis', 'value'),
         Input('y-axis', 'value'),
         Input('color-by', 'value')]
    )
    def update_scatter(x_column, y_column, color_column):
        return px.scatter(df, x=x_column, y=y_column, color=color_column)

    @app.callback(
        Output('box-plot', 'figure'),
        [Input('box-feature', 'value')]
    )
    def update_box(feature):
        return px.box(df, x=df.columns[-1], y=feature)

def explore_dataset(dataset=None):
    df = dataset if dataset is not None else get_default_dataset()
    return lambda: create_layout(df), lambda app: init_callbacks(app, df)

if __name__ == '__main__':
    app = Dash(__name__, 
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://www.w3schools.com/w3css/4/w3.css"
        ]
    )
    layout, callbacks = explore_dataset()
    app.layout = layout()
    callbacks(app)
    app.run_server(debug=True, port=8054)