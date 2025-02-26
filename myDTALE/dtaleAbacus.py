from flask import Flask, redirect
import pandas as pd
import dtale
from dtale.app import build_app  # Import build_app explicitly
from dtale.views import startup, cleanup_datasets
import socket
import os

# Initialize the Flask app
app = build_app(reaper_on=False)  # Use build_app to create the Flask app

# Function to get the actual host IP address
def get_host_ip():
    try:
        # Create a socket connection to a remote server to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "127.0.0.1"  # Fallback to localhost if unable to determine IP

# Default external dataset URL
DEFAULT_EXTERNAL_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Default local file path (update this to a valid path on your system)
DEFAULT_LOCAL_FILE = "static/titanic.csv"  # Replace with a valid local file path

""" # Ensure the default local file exists
if not os.path.exists(DEFAULT_LOCAL_FILE):
    # Create a sample CSV file if it doesn't exist
    sample_data = pd.DataFrame({"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]})
    sample_data.to_csv(DEFAULT_LOCAL_FILE, index=False)
 """
# Route to load data from an external URL
@app.route("/external/<path:url>")
def load_external_data(url=DEFAULT_EXTERNAL_URL):
    try:
        # Clean up Dtale instance "1" if it exists
        cleanup_datasets("1")

        # Load data from the external URL
        df = pd.read_csv(url)

        # Start Dtale instance "1" with the loaded data
        instance = startup("1", data=df, ignore_duplicate=True)

        # Redirect to the Dtale instance
        return redirect(f"/dtale/main/{instance._data_id}", code=302)
    except Exception as e:
        return f"Error loading external data: {str(e)}", 500

# Route to load data from a local file
@app.route("/internal/<path:file_location>")
@app.route("/internal", defaults={"file_location": DEFAULT_LOCAL_FILE})
def load_local_data(file_location):
    try:
        # Clean up Dtale instance "1" if it exists
        cleanup_datasets("1")

        # Load data from the local file
        df = pd.read_csv(file_location)

        # Start Dtale instance "1" with the loaded data
        instance = startup("1", data=df, ignore_duplicate=True)

        # Redirect to the Dtale instance
        return redirect(f"/dtale/main/{instance._data_id}", code=302)
    except Exception as e:
        return f"Error loading local data: {str(e)}", 500

# Default route
@app.route("/")
def home():
    return f"""
    <h1>Dtale Data Loader</h1>
    <p>Use the following routes to load data:</p>
    <ul>
        <li><strong>External URL:</strong> <code>/external/&lt;url&gt;</code></li>
        <li><strong>Default External Dataset:</strong> <a href="/external">{DEFAULT_EXTERNAL_URL}</a></li>
        <li><strong>Local File:</strong> <code>/internal/&lt;file_location&gt;</code></li>
        <li><strong>Default Local File:</strong> <a href="/internal">{DEFAULT_LOCAL_FILE}</a></li>
    </ul>
    """

# Run the Flask app
if __name__ == "__main__":
    host_ip = get_host_ip()  # Get the actual host IP address
    app.run(host=host_ip, port=8080)