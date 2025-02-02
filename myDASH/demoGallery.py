from dash import Dash, html
from dash_bootstrap_components import Carousel, themes

demos = [
    {"id": "demo1", "title": "REST API Demo", "description": "Fetch and display JSON data from SpaceX API", "link": "/rest"},
    {"id": "demo2", "title": "Chart Demo", "description": "Interactive data visualization using Plotly", "link": "/chart"},
    {"id": "demo3", "title": "Form Demo", "description": "Dynamic form handling with validation", "link": "/form"},
    {"id": "demo4", "title": "Data Table", "description": "Interactive table with sorting and filtering", "link": "/table"},
    {"id": "demo5", "title": "Map View", "description": "Geographic data visualization", "link": "/map"},
    {"id": "demo6", "title": "Real-time", "description": "Live data streaming dashboard", "link": "/live"}
]

app = Dash(__name__, external_stylesheets=[themes.DARKLY])

def create_carousel_slide1(demo):
    return {
        "key": demo["id"],
        "header": demo["title"],
        "caption": demo["description"],
        "src": "assets/demo-placeholder.png",
        "img_style": {
            "object-fit": "contain",
            "height": "200px",
            "width": "100px", 
            "margin": "auto"
        }
    }

def create_carousel_slide(demo):
    dbcContent= {
        "key": demo["id"],
        "header": demo["title"],
        "caption": demo['description'],
        "img_style": {
            "object-fit": "contain",
            "height": "390px",
            "width": "100px", 
            "margin": "auto"
        }
    }
    return dbcContent

app.layout = html.Div([
    html.Div([
        Carousel(
            items=[create_carousel_slide(demo) for demo in demos],
            controls=True,
            indicators=True,
            interval=None,
            style={
                "width": "600px",
                "margin": "auto",
                "height": "400px",
                "borderRadius": "4px",
                "backgroundColor": "#505050"
            }
        )
    ], style={
        'backgroundColor': '#606060',
        'borderRadius': '4px',
        'borderColor': 'red',
        'padding': '10px',
        'margin': ' auto',
        'width': '650px'
    })
], style={
    'backgroundColor': '#303030',
    'padding': '20px',
    'margin': 'auto',
    'minHeight': '100vh'
})

if __name__ == '__main__':
    app.run_server(debug=True)