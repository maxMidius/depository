#
#--------------------------------------
# vi: sw=4 ts=4  expandtab
#--------------------------------------
import streamlit as st
import requests

def generate_mermaid_svg(mermaid_code):
    url = 'http://localhost:3000/generate-svg'
    response = requests.post(url, json={'code': mermaid_code})
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error generating SVG: {response.text}")

text = """k
graph TD
A --> B
B --> C
"""

code = """
graph TD
    A --> B
"""

mm2 = """
graph LR
    A --> B --> C
"""

# Title of the Streamlit app
st.title("Mermaid Diagram with Streamlit")

t1, t2 = st.tabs(("D1", "D2"))
with t1:
    svg = generate_mermaid_svg(code)
    st.image(svg, width=50)
with t2:
    svg = generate_mermaid_svg(mm2)
    st.image(svg, width=250)
