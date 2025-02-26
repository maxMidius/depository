import solara
import pandas as pd
import dtale
import threading
import numpy as np
from IPython.display import HTML

# Initialize DTale in background
dtale_thread = None
dtale_url = solara.reactive("")

def start_dtale(df):
    global dtale_url
    instance = dtale.show(df, subprocess=False, open_browser=False)
    dtale_url.value = f"http://localhost:{instance.port}"
    instance.kill_without_confirm = False

@solara.component
def Page():
    global dtale_thread

    # Load sample data
    df = pd.DataFrame({
        'Date': pd.date_range('2023-01-01', periods=365),
        'Sales': np.random.randint(100, 5000, 365),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 365)
    })

    # Start DTale on first load
    if not dtale_thread:
        dtale_thread = threading.Thread(target=start_dtale, args=(df,), daemon=True)
        dtale_thread.start()

    return solara.Column(
        solara.Markdown("## DTale Integration"),
        solara.HTML(
            tag="iframe",
            attributes={
                "src": dtale_url.value,
                "style": "width: 100%; height: 80vh; border: none",
                "allow": "clipboard-read; clipboard-write"
            }
        ),
        style={"padding": "20px"}
    )