import panel as pn
import base64

pn.extension(
    css_files=[
        "https://www.w3schools.com/w3css/4/w3.css"  # Add w3.css
    ],
    'mermaid'
)

input_data = """
<div class='w3-pale-blue'>
  <b> Some Title </b>
  <div class='w3-row'>
    <div class='w3-col w3-yellow w3-border w3-margin'>
      ```mermaid
      graph TD
          A--> B --> C
      ```
    </div>
    <div class='w3-col w3-orange w3-border w3-margin'>
    <ol>
    <li>Item 1</li>
    <li>Item 2</li>
    </ol>
    <b> Footer here </b>
    </div>
  </div>
</div>
"""

def render_html_mermaid(input_text):
    parts = input_text.split("```mermaid")
    html_content_before_mermaid = parts[0]
    mermaid_part_and_html_after = parts[1] if len(parts) > 1 else ""
    mermaid_parts = mermaid_part_and_html_after.split("```")
    mermaid_script = mermaid_parts[0] if mermaid_parts else ""
    html_content_after_mermaid = mermaid_parts[1] if len(mermaid_parts) > 1 else ""

    # Encode the Mermaid script to base64
    mermaid_encoded = base64.b64encode(mermaid_script.encode('utf-8')).decode('utf-8')

    # Create an IFrame to display the Mermaid diagram
    iframe = f"""
    <iframe src="https://mermaid.ink/img/{mermaid_encoded}" 
            style="width:100%; height:200px; border:none; resize: both; overflow: auto;">
    </iframe>
    """

    html_before = pn.pane.HTML(html_content_before_mermaid)
    html_diagram = pn.pane.HTML(iframe)
    html_after = pn.pane.HTML(html_content_after_mermaid)

    return f"""<div class='w3-pale-blue'>
                <b> Some Title </b>
                <div class='w3-row'>
                    <div class='w3-col w3-yellow w3-border w3-margin'>{html_diagram.object}</div>
                    <div class='w3-col w3-orange w3-border w3-margin'>{html_after.object}</div>
                </div>
            </div>"""

rendered_output = render_html_mermaid(input_data)
pn.pane.HTML(rendered_output).servable()

mermaid_text = """
graph TD
    A[Start] --> B{Is it?};
    B -- Yes --> C[OK];
    B -- No ----> D[KO];
    C --> E[End];
    D --> E;
"""

mermaid_pane = pn.pane.Markdown(f"""
```mermaid
{mermaid_text}
```""")

