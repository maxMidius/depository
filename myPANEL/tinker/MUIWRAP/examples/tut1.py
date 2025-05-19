import panel as pn
import param
import sys
import os

# Add the parent directory to the path so we can use absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.muiWrapLib import ClickableButton, Rating, DiscreteSlider

# Initialize Panel with material template - IMPORTANT: add reacton and material-ui extensions
pn.extension('reacton', 'material-ui', template='material')

# Create a status display - using a reactive pane for better updates
status_text = pn.pane.Markdown("### Status: Waiting for interaction...")

# Define event handlers
def button_clicked(event=None):
    """Handle button click events"""
    # Get the button label from the event's owner (the button component)
    button_label = event.obj.label if event and hasattr(event, 'obj') else "unknown"
    status_text.object = f"### Status: Button '{button_label}' was clicked!"
    print(f"Button clicked! Label: {button_label}")

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

# Use the MUI Button instead of Panel's button
button = ClickableButton(label="Click Me!", variant="contained")
button.param.watch(button_clicked, 'clicked')

rating = Rating(value=3)
slider = DiscreteSlider(value=37)

# Set up the value watchers
slider.param.watch(slider_changed, 'value')
rating.param.watch(rating_changed, 'value')

def doLayout() :
    # Create a demo layout
    app = pn.Row(
        pn.Column(
            pn.pane.Markdown("## Button Component (MUI)"),
            button.controls(['disabled', 'label', 'variant']),
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
    return app

doLayout().servable(title="Button/Slider/Rating Demo")