import panel as pn

pn.extension(
    css_files=[
        "https://www.w3schools.com/w3css/4/w3.css"  # Add w3.css
    ]
)


pn.extension()

# Define the HTML content for each column
html_content1 = """
<div class="w3-container w3-pale-blue">
  <h2>Column 1</h2>
  <p>This is some HTML text for column 1.</p>
</div>
"""

html_content2 = """
<div class="w3-container w3-pale-green">
  <h2>Column 2</h2>
  <p>This is some HTML text for column 2.</p>
</div>
"""

html_content3 = """
<div class="w3-container w3-pale-yellow">
  <h2>Column 3</h2>
  <p>This is some HTML text for column 3.</p>
</div>
"""

# Create HTML panes for each column
html_pane1 = pn.pane.HTML(html_content1, height=200, width=300)
html_pane2 = pn.pane.HTML(html_content2, height=200, width=300)
html_pane3 = pn.pane.HTML(html_content3, height=200, width=300)

# Create a row with three columns
row = pn.Row(
    pn.Column(html_pane1),
    pn.Column(html_pane2),
    pn.Column(html_pane3)
)

# Serve the row
row.servable()