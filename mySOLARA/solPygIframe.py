import solara
import pandas as pd
import pygwalker as pyg
import base64

@solara.component
def PygWalkerComponent(df: pd.DataFrame):
    # 1. Generate pygWalker HTML
    walker = pyg.walk(df, spec="gw_config.json", debug=False)
    html_content = walker.to_html()

    # 2. Create embeddable content
    encoded_html = base64.b64encode(html_content.encode()).decode()
    iframe_src = f"data:text/html;base64,{encoded_html}"

    # 3. Return iframe with pygWalker content
    return solara.iframe(
        src=iframe_src,
        style={
            "width": "100%",
            "height": "80vh",
            "border": "none",
            "margin": "20px 0"
        }
    )

@solara.component
def Page():
    # Load or create your DataFrame
    df = solara.use_reactive(pd.read_csv("titanic.csv"))  # Replace with your data source

    # Create UI layout
    return solara.Column(
        solara.Markdown("## PygWalker in Solara"),
        PygWalkerComponent(df=df.value),
        style={"padding": "20px"}
    )

# Run with:
# solara run pygwalker_solara.py