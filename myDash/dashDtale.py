import pandas as pd
import dash
from dash import html
import dtale
import threading
import time
import socket

# Function to get the host's LAN IP address
def get_host_ip():
    """Returns the LAN IP address of the host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This doesn't need to be reachable
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'  # Fallback to localhost
    finally:
        s.close()
    return ip

# Get the host IP
host_ip = get_host_ip()

# Create sample data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'London', 'Paris', 'Tokyo']
})

# Function to run Dtale server
def run_dtale():
    """Starts the Dtale server."""
    # Start Dtale without blocking the main thread
    dtale.show(df, host=host_ip, port=4001, subprocess=False)

# Start Dtale in a separate thread
dtale_thread = threading.Thread(target=run_dtale, daemon=True)
dtale_thread.start()

# Give Dtale some time to start
time.sleep(2)

# Dtale URL using the determined host IP
dtale_url = f"http://{host_ip}:4001/#/detailed/sample_data"

# Create Dash app
app = dash.Dash(__name__)

# Define Dash app layout
app.layout = html.Div([
    html.H1("Dash App with Dtale Visualization", style={"textAlign": "center", "color": "#ffffff"}),
    html.Iframe(
        src=dtale_url,
        style={
            "width": "100%",
            "height": "800px",
            "border": "none"
        }
    )
], style={
    "backgroundColor": "#303030",
    "padding": "20px",
    "minHeight": "100vh",
    "color": "#ffffff"
})

if __name__ == "__main__":
    # Run Dash app on the determined host IP and default port 8050
    app.run_server(debug=True, host=host_ip)