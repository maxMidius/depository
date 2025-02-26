from dash import html 
import dash
import dash_dangerously_set_inner_html as dsih  # Import for raw HTML

app = dash.Dash(__name__)
with open('myHello.html', 'r') as f:
    html_content = f.read()

app.layout = html.Div([
    dsih.DangerouslySetInnerHTML(html_content)
])

if __name__ == '__main__':
    app.run_server(debug=True)
