import streamlit as st
from rich.console import Console
from rich.text import Text
from io import StringIO
import base64

def render_ansi(ansi_text):
  console = Console(file=StringIO(), force_terminal=True)
  console.print(Text.from_ansi(ansi_text))
  return console.file.getvalue()

def ansi_to_html(ansi_text):
  rendered = render_ansi(ansi_text)
  return f'<pre style="background-color: black; color: white; padding: 10px; font-family: monospace;">{rendered}</pre>'

def main():
  st.title("ANSI Terminal Simulator")

  # Input area for ANSI text
  user_input = st.text_area("Enter ANSI-formatted text:", 
                            value="\033[31mHello\033[0m \033[32mWorld\033[0m!\n\033[1;33mThis is bold yellow\033[0m")

  # Display the rendered ANSI text
  st.markdown(ansi_to_html(user_input), unsafe_allow_html=True)

  # Example ANSI sequences
  st.sidebar.header("ANSI Sequence Examples")
  examples = {
      "Red Text": r"\033[31mRed Text\033[0m",
      "Green Background": r"\033[42mGreen Background\033[0m",
      "Bold Blue": r"\033[1;34mBold Blue\033[0m",
      "Blinking Text": r"\033[5mBlinking Text\033[0m",
      "Underline": r"\033[4mUnderlined Text\033[0m",
  }

  for name, sequence in examples.items():
      if st.sidebar.button(f"Add {name}"):
          user_input += f"\n{sequence}"
          st.session_state.user_input = user_input

  # Download rendered HTML
  if st.button("Download Rendered HTML"):
      html_content = ansi_to_html(user_input)
      b64 = base64.b64encode(html_content.encode()).decode()
      href = f'<a href="data:text/html;base64,{b64}" download="ansi_rendered.html">Download HTML</a>'
      st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
  main()

# Created/Modified files during execution:
# None
