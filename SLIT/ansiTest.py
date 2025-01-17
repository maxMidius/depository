import streamlit as st
from rich.console import Console
from rich.text import Text
from io import StringIO

# Create a console object
console = Console(file=StringIO(), force_terminal=True)

# Example ANSI escape sequence
ansi_text = "\033[31mThis is red text\033[0m and this is normal text."

# Use Rich to render the ANSI text
console.print(Text.from_ansi(ansi_text))

# Get the rendered output
rendered_output = console.file.getvalue()

# Display the rendered output in Streamlit
st.markdown(f"<pre>{rendered_output}</pre>", unsafe_allow_html=True)
