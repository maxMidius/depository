import panel as pn
import panel.widgets as pnw

# Initialize Panel extensions
pn.extension()

# --- Column Definitions (similar to your existing code) ---
column1 = pn.Column(
    pn.pane.Markdown("### Column 1 (20%)", margin=(0, 5)),
    pnw.Button(name="Button C1", button_type="primary"),
    sizing_mode='stretch_height',
    styles={
        'padding': '10px',
        'background-color': 'rgba(173, 216, 230, 0.5)',
        'border': '1px dashed blue',
        'flex-basis': '20%', # Initial proportion
        'flex-grow': '2' # Allow it to grow
    },
    # width_policy='max', # Not strictly needed for this flex approach
    # min_width=100
)

column2 = pn.Column(
    pn.pane.Markdown("### Column 2 (60%)", margin=(0, 5)),
    pnw.TextInput(name="Input in Column 2", placeholder="Enter text..."),
    pn.pane.Markdown("This column is wider and can hold more content.", margin=(5, 0)),
    sizing_mode='stretch_height',
    styles={
        'padding': '10px',
        'background-color': 'rgba(144, 238, 144, 0.5)',
        'border': '1px dashed green',
        'border': '1px dashed red',
        'flex-basis': '58%', # Initial proportion
        'flex-grow': '6' # Allow it to grow
    },
    # width_policy='max',
    # min_width=150
)

column3 = pn.Column(
    pn.pane.Markdown("### Column 3 (20%)", margin=(0, 5)),
    pnw.DiscreteSlider(name="Slider C3", options=[0, 1, 2, 3, 4, 5], value=3),
    sizing_mode='stretch_height',
    styles={
        'padding': '10px',
        'background-color': 'rgba(255, 192, 203, 0.5)',
        'border': '1px dashed red',
    },
    # width_policy='max',
    # max_width=200
    # width='20%'
)

# --- Toggle Buttons and Callbacks ---
toggle_left_button = pnw.Button(name="Toggle Left Column", button_type="warning", width=150)
toggle_right_button = pnw.Button(name="Toggle Right Column", button_type="warning", width=150)

def toggle_left_column_visibility(event):
    column1.visible = not column1.visible
    toggle_left_button.name = "Show Left Column" if not column1.visible else "Hide Left Column"

def toggle_right_column_visibility(event):
    column3.visible = not column3.visible
    toggle_right_button.name = "Show Right Column" if not column3.visible else "Hide Right Column"

# Link buttons to callbacks
toggle_left_button.on_click(toggle_left_column_visibility)
toggle_right_button.on_click(toggle_right_column_visibility)

# Set initial button names based on visibility
toggle_left_button.name = "Hide Left Column" if column1.visible else "Show Left Column"
toggle_right_button.name = "Hide Right Column" if column3.visible else "Show Right Column"

# --- Main Layout ---
# Row for the three data columns
data_row = pn.Row(
    column1,
    column2,
    column3,
    sizing_mode='stretch_width', # Keep this for height and general layout policy
    #styles={'background-color': '#fafafa', 'border': '1px solid #ccc', 'padding': '5px'}
    styles={'width': '98vw', 'box-sizing': 'border-box', 'margin': '10px'} # Use viewport width
)

# Overall layout: controls on top, data row below
main_layout = pn.Column(
    pn.Row(toggle_left_button, toggle_right_button, sizing_mode='stretch_width', styles={'margin_bottom': '10px'}),
    data_row,
)

# To display this layout
main_layout.servable()