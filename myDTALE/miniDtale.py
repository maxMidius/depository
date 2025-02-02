import os
import socket
import pandas as pd
from flask import redirect
from dtale.app import DtaleFlask
import dtale

PORT = 5000
dtale_instance = None

app = DtaleFlask(__name__)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def create_dataset(dataset_type="simple"):
    script_dir = os.path.dirname(__file__)
    if dataset_type.lower() == "simple":
        return pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    elif dataset_type.lower() == "titanic":
        titanic_path = os.path.join(script_dir, 'assets', 'titanic.csv')
        return pd.read_csv(titanic_path)
    return pd.DataFrame()

@app.route('/')
def index():
    global dtale_instance
    if dtale_instance is None:
        df = create_dataset("simple")
        dtale_instance = dtale.show(df, ignore_duplicate=True, open_browser=False, host='0.0.0.0', port=PORT)
    return redirect(dtale_instance._main_url)

if __name__ == '__main__':
    ip = get_ip_address()
    print(f"Starting server at http://{ip}:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)