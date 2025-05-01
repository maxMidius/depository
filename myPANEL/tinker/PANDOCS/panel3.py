import panel as pn
from panel_mermaid import MermaidDiagram

pn.extension(
    css_files=[
        "https://www.w3schools.com/w3css/4/w3.css"  # Add w3.css
    ]
)

pic1= """
graph TD
    A--> B --> C

"""

pic2= """
sequenceDiagram
    participant Alice
    participant Bob

    Alice->John: Hello John, do you want to go to the mall?
    loop Healthcheck
        John->John: Fight against hypochondria
    end
    Note right of John: Rational thoughts<br/>prevail...
    John-->Alice: Yes!
    Alice->Bob: How about you?
    Bob-->Alice: No way!
"""

r0c0 = """
<div class="w3-container w3-pale-blue">
<h2>Column 1</h2>
<p>This is some HTML text for column 1.</p>
</div>

"""
r0c1 = """
<div class="w3-container w3-pale-green">
<h2>Column 2</h2>
<p>This is some HTML text for column 2.</p>
</div>
"""
r0c2 = """
<div class="w3-container w3-pale-yellow">
<h2>Column 3</h2>
<p>This is some HTML text for column 3.</p>
</div>
"""

pn.Row(
    pn.Column(
        pn.pane.HTML(r0c0) ,
        MermaidDiagram(object=pic1 ),
        styles={
        'background': '#f0f8ff',  # AliceBlue
        'padding': '20px',
        'border-radius': '10px',
        'border': '1px solid #ddd',
        'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)'
        },
        sizing_mode='stretch_width'
        ),
    pn.Column(
        pn.pane.HTML(r0c1), 
        MermaidDiagram(object=pic2, width=500, height=200)
        ),
    pn.Column(pn.pane.HTML(r0c2 )), 
).servable()

