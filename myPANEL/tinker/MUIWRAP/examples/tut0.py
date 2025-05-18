import panel as pn
import param
import sys
import os

# Add the parent directory to the path so we can use absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.muiWrapLib import Rating, DiscreteSlider

# Initialize Panel with material template
pn.extension(template='material')

# Create a status display - using a reactive pane for better updates
status_text = pn.pane.Markdown("### Status: Waiting for interaction...")

# Define event handlers
def button_clicked(event=None):
    """Handle button click events"""
    status_text.object = f"### Status: Button was clicked!"
    print("Button clicked!")

def slider_changed(event):
    """Handle slider value changes"""
    new_value = event.new
    status_text.object = f"### Status: Slider value changed to {new_value}°C"
    print(f"Slider value changed to: {new_value}")

def rating_changed(event):
    """Handle rating value changes"""
    new_rating = event.new
    status_text.object = f"### Status: Rating changed to {new_rating} stars"
    print(f"Rating changed to: {new_rating}")

# Approach using a standard Panel button instead of MUI
button = pn.widgets.Button(name="Click Me!", button_type="primary")
button.on_click(button_clicked)  # Use Panel's built-in click handling

rating = Rating(value=3)
slider = DiscreteSlider(value=37)

# Set up the value watchers
slider.param.watch(slider_changed, 'value')
rating.param.watch(rating_changed, 'value')  # Add watcher for rating changes

# Create a demo layout
app = pn.Row(
    pn.Column(
        pn.pane.Markdown("## Button Component"),
        button
    ),
    pn.Column(
        pn.pane.Markdown("## Rating Component"),
        rating.controls(['value']), 
        rating
    ),
    pn.Column(
        pn.pane.Markdown("## Slider Component"),
        slider.controls(['value']), 
        slider
    ),
    pn.Column(
        status_text
    )
)

app.servable(title="Material UI Components Demo")