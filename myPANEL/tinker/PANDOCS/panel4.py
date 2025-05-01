import panel as pn
import reacton.ipywidgets as reacton
import ipywidgets as widgets

pn.extension('ipywidgets')

# Create a Reacton Text widget
text_widget, set_text = reacton.use_state("Hello, Reacton!")

# Create a Panel layout
layout = pn.Column(
    pn.pane.Markdown("## Reacton Text Widget Example"),
    pn.pane.IPyWidget(widgets.Text(value=text_widget, description='Text:', disabled=False), height=100, width=300)
)

# Serve the layout
layout.servable()