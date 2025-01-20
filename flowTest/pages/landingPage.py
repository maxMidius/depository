from dash import html, Dash
import dash_bootstrap_components as dbc

def layout():
    return html.Div([
        # Banner with larger centered text
        dbc.Row([
            dbc.Col(
                html.H1("Why Surveillance Studio ?", 
                       className='w3-text-blue-grey w3-xxlarge w3-padding w3-center'),
                className='w3-round-large w3-light-grey w3-margin w3-padding'
            )
        ], className='w3-container'),
        
        # Four Column Layout - set equal widths
        dbc.Row([
            # Requirements Column
            dbc.Col([
                html.Div([
                    # Centered icon and header
                    html.Div([
                        html.I(className="fas fa-list-check fa-3x w3-text-blue-grey w3-margin"),
                        html.H3("Requirements", className='w3-text-blue-grey')
                    ], className='w3-center'),
                    # Left aligned bullet points
                    html.Ul([
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Start with basics"
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Refine  iteratively"
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Enable BAs to code"
                        ])
                    ], className='w3-ul w3-small')
                ], className='w3-container text-left')
            ], xs=12, sm=6, md=3, className='w3-round-large w3-light-grey w3-margin-small w3-padding'),
            
            # Data Access Column
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-database fa-3x w3-text-blue-grey w3-margin"),
                        html.H3("Data Access", className='w3-text-blue-grey')
                    ], className='w3-center'),
                    html.Ul([
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Access data easily"
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "DB2, Impala etc ..."
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Interact to explore"  # Removed html.A wrapper
                        ])
                    ], className='w3-ul w3-small')
                ], className='w3-container text-left')
            ], xs=12, sm=6, md=3, className='w3-round-large w3-light-grey w3-margin-small w3-padding'),
            
            # Development Column
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-code fa-3x w3-text-blue-grey w3-margin"),
                        html.H3("Development", className='w3-text-blue-grey')
                    ], className='w3-center'),
                    html.Ul([
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Declarative logic "
                        ]),
                       html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Wire graphically"
                        ]),
                       html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "inspect results"
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Join data sources"
                        ])
                    ], className='w3-ul w3-small')
                ], className='w3-container text-left')
            ], xs=12, sm=6, md=3, className='w3-round-large w3-light-grey w3-margin-small w3-padding'),
            
            # Deploy Column
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-rocket fa-3x w3-text-blue-grey w3-margin"),
                        html.H3("Deploy", className='w3-text-blue-grey')
                    ], className='w3-center'),
                    html.Ul([
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Test locally"
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "in a sandbox"
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Promote code"
                        ]),
                        html.Li([
                            html.I(className="fas fa-check w3-text-blue-grey w3-margin-right"),
                            "Triggers deployment"
                        ])
                    ], className='w3-ul w3-small')
                ], className='w3-container text-left')
            ], xs=12, sm=6, md=3, className='w3-round-large w3-light-grey w3-margin-small w3-padding')
        ], className='w3-container g-0')  # g-0 removes gutters
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
    app.run_server(debug=True, port=8052)