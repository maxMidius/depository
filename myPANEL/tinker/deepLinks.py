import panel as pn
import param

pn.extension()

class DeepLinkedApp(param.Parameterized):
    """
    A simple Panel app demonstrating deep linking.
    The state (slider value) is encoded in the URL.
    """
    slider_value = param.Integer(default=5, bounds=(0, 10), label="Slider Value")

    def __init__(self, **params):
        super().__init__(**params)
        self._sync_slider_from_url()  # Initialize slider from URL on app load

    @param.depends("slider_value", watch=True)
    def _update_url(self, *args):
        """Updates the URL query parameters when the slider_value changes."""
        pn.state.location.search = f"?slider_value={self.slider_value}"

    def _sync_slider_from_url(self):
        """Initializes the slider_value from URL query parameters if present."""
        params_from_url = pn.state.location.query_params
        if "slider_value" in params_from_url:
            try:
                url_value = int(params_from_url["slider_value"])
                if self.param.slider_value.bounds[0] <= url_value <= self.param.slider_value.bounds[1]:
                    # Temporarily disable events to avoid recursion
                    with param.discard_events(self):  # FIXED: Pass 'self' as the argument
                        self.slider_value = url_value
                else:
                    print(f"Warning: Slider value from URL '{url_value}' is out of bounds. Using default.")
            except ValueError:
                print(f"Warning: Invalid slider_value in URL '{params_from_url['slider_value']}'. Using default.")

    # ADDED: A reactive function to display the current slider value
    @pn.depends('slider_value')
    def current_value_display(self):
        return pn.pane.Markdown(f"**Current Slider Value:** {self.slider_value}")

    def view(self):
        """Returns the Panel layout for the app."""
        return pn.Column(
            pn.pane.Markdown(f"## Deep Linked Panel App"),
            pn.pane.Markdown("Move the slider below to see the URL update. "
                             "Share the URL or bookmark it to save and restore the app state."),
            self.current_value_display,  # CHANGED: Using the reactive function
            pn.widgets.IntSlider.from_param(self.param.slider_value),
            pn.pane.Markdown("---"),
            pn.pane.Markdown("**Instructions:**\n\n"
                             "1.  Run this app using `panel serve deep_link_demo.py`.\n"
                             "2.  Open the app in your browser.\n"
                             "3.  Move the slider and observe the URL in the address bar changing.\n"
                             "4.  Copy the URL and share it or bookmark it.\n"
                             "5.  Open the copied URL in a new browser tab or share it with someone.\n"
                             "6.  The app should open with the slider at the saved position.\n")
        )


# Instantiate the app
deep_linked_app = DeepLinkedApp()

# Create Panel layout and make it servable
app_layout = deep_linked_app.view()  # Call the view method to get the layout
app_layout.servable(title="Deep Link Demo")


# To run this app:
# 1. Save this code as a Python file (e.g., deep_link_demo.py)
# 2. Run from your terminal:  panel serve deep_link_demo.py
# 3. Open the URL provided in your terminal in your web browser