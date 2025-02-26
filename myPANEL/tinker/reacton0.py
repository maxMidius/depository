import panel as pn
import reacton.ipywidgets as w
import reacton
import markdown

pn.extension('ipywidgets')
pn.extension()

pn.extension(
    css_files=[
        "https://www.w3schools.com/w3css/4/w3.css"  # Add w3.css
    ] ,
    js_files=[
        "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.2.7/mermaid.min.js"
    ]
)

@reacton.component
def ButtonClick():
    # first render, this return 0, after that, the last argument
    # of set_clicks
    clicks, set_clicks = reacton.use_state(0)
    
    def my_click_handler():
        # trigger a new render with a new value for clicks
        set_clicks(clicks+1)

    button = w.Button(description=f"Clicked {clicks} times",
                      on_click=my_click_handler)
    return button

@reacton.component
def Markdown(md: str):
    html = markdown.markdown(md)
    return w.HTML(value=html)

# Mermaid content
mermaid_content = """
graph TD
    A--> B --> C
"""

# Combine Mermaid content and script
html_content = f"""
# Reacton rocks\nSeriously **bold** idea! 

<div class='mermaid'>
    {mermaid_content}
</div>
"""

# Use HTML pane to ensure JavaScript is executed
m1 = pn.pane.HTML(html_content, height=400, width=600)

# JavaScript callback to initialize Mermaid
js_callback = """
console.log('Mermaid initializing!');
mermaid.initialize({ startOnLoad: true });
"""

# Attach the JavaScript callback to the document
pn.state.onload(lambda: pn.state.execute(js_callback))

b1 = ButtonClick()

pn.Column(m1, pn.panel(b1)).servable()