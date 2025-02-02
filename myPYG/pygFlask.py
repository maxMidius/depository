from flask import Flask, render_template_string, request
import pandas as pd
import pygwalker as pyg
import contextlib
import io

app = Flask(__name__)

# Function to load dataset from a URL
def load_dataset_from_url(url):
    df = pd.read_csv(url)
    return df

# Route for external data URL
@app.route('/external', methods=['GET'])
def external():
    # Get the external data URL from the query parameter
    data_url = request.args.get('url')
    if not data_url:
        return "Please provide a 'url' query parameter.", 400

    # Load the dataset from the external URL
    df = load_dataset_from_url(data_url)

    # Suppress output while generating PygWalker HTML
    with contextlib.redirect_stdout(io.StringIO()):  # Redirect stdout to suppress output
        walker = pyg.walk(df, spec="./gw_config.json", debug=False)
        html = walker.to_html()

    # Render the HTML in a Flask template
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PygWalker with Flask (External Data)</title>
        </head>
        <body>
            <h1>PygWalker with Flask (External Data)</h1>
            {{ pygwalker_html|safe }}
        </body>
        </html>
    ''', pygwalker_html=html)

if __name__ == '__main__':
    # Run the Flask app on all available interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)