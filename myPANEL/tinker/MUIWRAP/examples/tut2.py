import panel as pn
import param
import sys
import os

# Add the parent directory to the path so we can use absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.muiWrapStepper import Stepper

# Initialize Panel with material template and required extensions
pn.extension('reacton', 'material-ui', template='material', sizing_mode="stretch_width")

# Create a status display
status_text = pn.pane.Markdown("### Status: Ready to start")

# Create step content panes
step_contents = [
    pn.Column(
        pn.pane.Markdown("## Step 1: Select Options"),
        pn.widgets.Select(name="Product", options=["Basic", "Standard", "Premium"], value="Premium"),
        pn.widgets.IntSlider(name="Quantity", start=1, end=10, value=1),
        pn.widgets.Checkbox(name="Add warranty", value=True)
    ),
    pn.Column(
        pn.pane.Markdown("## Step 2: Review Details"),
        pn.pane.Markdown("Please review your selection:"),
        pn.pane.Markdown("- Product: Premium"),
        pn.pane.Markdown("- Quantity: 1"),
        pn.pane.Markdown("- Warranty: Yes"),
        pn.pane.Markdown("- Total: $149.99")
    ),
    pn.Column(
        pn.pane.Markdown("## Step 3: Complete Purchase"),
        pn.pane.Markdown("✅ Your order has been submitted!"),
        pn.pane.Markdown("Order #12345 has been confirmed."),
        pn.pane.Markdown("Thank you for your purchase.")
    )
]

# Create active step indicators for different sections
basic_active_step = pn.Column(step_contents[0])
vertical_active_step = pn.Column(step_contents[0])
advanced_active_step = pn.Column(step_contents[0])

# Create different stepper variants
basic_stepper = Stepper(
    steps=["Select options", "Review details", "Complete purchase"],
    active_step=0,
    alternative_label=True,  # This makes it look more like the screenshot
    completed_steps=[],      # Will be updated as we progress
    connector_type="normal"
)

vertical_stepper = Stepper(
    steps=["Select options", "Review details", "Complete purchase"],
    active_step=0,
    orientation="vertical",
    alternative_label=False,  # Alternative label doesn't work well with vertical
    connector_type="normal"
)

advanced_stepper = Stepper(
    steps=["Select master blaster campaign settings", "Create an ad group", "Create an ad"],
    active_step=0,
    optional_steps=[1],      # Second step is optional
    completed_steps=[0],     # First step is completed
    alternative_label=True,  # Like in the screenshot
    linear=False,            # Allow direct navigation
    dark_theme=True          # Use dark theme to match the example exactly
)

# Define event handlers for basic stepper
next_button = pn.widgets.Button(name="Next", button_type="primary")
back_button = pn.widgets.Button(name="Back", button_type="default")

def on_next_click(event):
    if basic_stepper.active_step < len(basic_stepper.steps) - 1:
        # Add the current step to completed_steps before advancing
        completed = list(basic_stepper.completed_steps)
        if basic_stepper.active_step not in completed:
            completed.append(basic_stepper.active_step)
        basic_stepper.completed_steps = completed
        
        basic_stepper.active_step += 1
        basic_active_step[0] = step_contents[min(basic_stepper.active_step, len(step_contents)-1)]
        status_text.object = f"### Status: Moved to step {basic_stepper.active_step+1} ({basic_stepper.steps[basic_stepper.active_step]})"
        
        # Update button states
        back_button.disabled = False
        if basic_stepper.active_step == len(basic_stepper.steps) - 1:
            next_button.disabled = True

def on_back_click(event):
    if basic_stepper.active_step > 0:
        basic_stepper.active_step -= 1
        basic_active_step[0] = step_contents[basic_stepper.active_step]
        status_text.object = f"### Status: Moved back to step {basic_stepper.active_step+1} ({basic_stepper.steps[basic_stepper.active_step]})"
        
        # Update button states
        next_button.disabled = False
        if basic_stepper.active_step == 0:
            back_button.disabled = True

# Initialize button states
back_button.disabled = True
next_button.on_click(on_next_click)
back_button.on_click(on_back_click)

# Define event handlers for vertical stepper
vertical_next_button = pn.widgets.Button(name="Next Step", button_type="primary")
vertical_back_button = pn.widgets.Button(name="Previous Step", button_type="default")

def on_vertical_next_click(event):
    if vertical_stepper.active_step < len(vertical_stepper.steps) - 1:
        vertical_stepper.active_step += 1
        vertical_active_step[0] = step_contents[min(vertical_stepper.active_step, len(step_contents)-1)]
        status_text.object = f"### Status: Moved to vertical step {vertical_stepper.active_step+1}"
        
        # Update button states
        vertical_back_button.disabled = False
        if vertical_stepper.active_step == len(vertical_stepper.steps) - 1:
            vertical_next_button.disabled = True

def on_vertical_back_click(event):
    if vertical_stepper.active_step > 0:
        vertical_stepper.active_step -= 1
        vertical_active_step[0] = step_contents[vertical_stepper.active_step]
        status_text.object = f"### Status: Moved back to vertical step {vertical_stepper.active_step+1}"
        
        # Update button states
        vertical_next_button.disabled = False
        if vertical_stepper.active_step == 0:
            vertical_back_button.disabled = True

# Initialize vertical button states
vertical_back_button.disabled = True
vertical_next_button.on_click(on_vertical_next_click)
vertical_back_button.on_click(on_vertical_back_click)

# First, add navigation handlers for the advanced stepper
advanced_next_button = pn.widgets.Button(name="Next", button_type="primary")
advanced_back_button = pn.widgets.Button(name="Back", button_type="default")

def on_advanced_next_click(event):
    if advanced_stepper.active_step < len(advanced_stepper.steps) - 1:
        advanced_stepper.active_step += 1
        # Adjust index to avoid out of bounds with our content
        content_idx = min(advanced_stepper.active_step, len(step_contents)-1)
        advanced_active_step[0] = step_contents[content_idx]
        status_text.object = f"### Status: Advanced stepper moved to step {advanced_stepper.active_step+1}"
        
        # Update button states
        advanced_back_button.disabled = False
        if advanced_stepper.active_step == len(advanced_stepper.steps) - 1:
            advanced_next_button.disabled = True

def on_advanced_back_click(event):
    if advanced_stepper.active_step > 0:
        advanced_stepper.active_step -= 1
        advanced_active_step[0] = step_contents[min(advanced_stepper.active_step, len(step_contents)-1)]
        status_text.object = f"### Status: Advanced stepper moved back to step {advanced_stepper.active_step+1}"
        
        # Update button states
        advanced_next_button.disabled = False
        if advanced_stepper.active_step == 0:
            advanced_back_button.disabled = True

# Initialize advanced button states
advanced_back_button.disabled = True
advanced_next_button.on_click(on_advanced_next_click)
advanced_back_button.on_click(on_advanced_back_click)

# Define a function to reset all steppers
def reset_all(event):
    basic_stepper.active_step = 0
    vertical_stepper.active_step = 0
    advanced_stepper.active_step = 0
    
    # Reset content displays
    basic_active_step[0] = step_contents[0]
    vertical_active_step[0] = step_contents[0]
    advanced_active_step[0] = step_contents[0]
    
    # Reset button states
    back_button.disabled = True
    next_button.disabled = False
    vertical_back_button.disabled = True
    vertical_next_button.disabled = False
    advanced_back_button.disabled = True
    advanced_next_button.disabled = False
    
    status_text.object = "### Status: All steppers reset"

reset_button = pn.widgets.Button(name="Reset All", button_type="danger")
reset_button.on_click(reset_all)

# Create the layout
def doLayout():
    app = pn.Column(
        pn.pane.Markdown("# Material UI Stepper Demo"),
        pn.pane.Markdown("This example demonstrates different variants of Material UI's Stepper component."),
        
        # Basic Horizontal Stepper
        pn.pane.Markdown("## Basic Horizontal Stepper"),
        pn.Column(
            pn.pane.HTML("<div style='min-height: 120px;'>", width=800),  # Add space for the stepper
            basic_stepper,
            pn.Spacer(height=20),
            basic_active_step,
            pn.Row(back_button, next_button, align="center"),
            width=800  # Wider to show the stepper properly
        ),
        
        pn.layout.Divider(),
        
        # Vertical Stepper - improved layout to make orientation more obvious
        pn.pane.Markdown("## Vertical Stepper"),
        pn.Row(
            # Give more width to the stepper component to ensure vertical orientation is visible
            pn.Column(vertical_stepper, width=300),
            pn.Column(
                vertical_active_step,
                pn.Row(vertical_back_button, vertical_next_button, align="center")
            )
        ),
        
        pn.layout.Divider(),
        
        # Advanced Stepper with Optional & Error States
        pn.pane.Markdown("## Alternative Label Stepper"),
        pn.pane.Markdown("Labels can be placed below the step icon by setting the `alternative_label` prop on the `Stepper` component."),
        pn.Column(
            advanced_stepper,
            pn.Spacer(height=20),
            advanced_active_step,
            pn.Row(advanced_back_button, advanced_next_button, align="center")
        ),
        
        # Reset button and status
        pn.Row(reset_button),
        pn.Spacer(height=20),
        status_text,
        width=800
    )
    return app

doLayout().servable(title="MUI Stepper Variants Demo")

"""
# Additional MUI Styling Test
test_chip_component = TestChip(label="MUI Test", color="secondary")

pn.Column(
    "# MUI Styling Test",
    test_chip_component
).show()  # Or .servable()
"""