import panel as pn

pn.extension()

# Create a FileSelector widget
file_selector = pn.widgets.FileSelector('~')

# Read the selected file's contents (assuming it's a text file)
@pn.depends(file_selector.param.value)
def read_file_contents(file_value):
    if file_value:
        try:
            with open(file_value[0], 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return "File not found."
    return ""

# Display the file contents
file_contents = pn.pane.Str(read_file_contents, height=300)
app = pn.Column(file_selector, file_contents)

app.servable()
