import solara
import pandas as pd
import pygwalker as pyg

@solara.component
def Page():
    # Sample DataFrame
    df = pd.DataFrame({
        'x': [1, 2, 3],
        'y': [4, 5, 6]
    })

    # Generate pygwalker HTML
    walker = pyg.walk(df)
    html_str = walker.to_html()

    # Render the HTML
    return solara.HTML(unsafe_innerHTML=html_str)

# Run the app with solara run filename.py