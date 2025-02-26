import panel as pn
import param

pn.extension()

class DeepLinkedMenuApp(param.Parameterized):
    """
    A Panel app demonstrating deep linking with multiple selectors.
    The currently selected fruit or vegetable is encoded in the URL.
    """
    # Parameters for selections
    fruit = param.Selector(default="Apples", objects=["Apples", "Mangos", "Bananas"])
    veggie = param.Selector(default="Broccoli", objects=["Broccoli", "Potato", "Tomato"])
    
    # Track which category was last selected
    active_category = param.String(default="fruit")
    
    def __init__(self, **params):
        super().__init__(**params)
        self._sync_from_url()  # Initialize selections from URL on app load

    @param.depends("fruit", watch=True)
    def _update_on_fruit_change(self, *args):
        """Update active category and URL when fruit changes"""
        self.active_category = "fruit"
        self._update_url()
        
    @param.depends("veggie", watch=True)
    def _update_on_veggie_change(self, *args):
        """Update active category and URL when veggie changes"""
        self.active_category = "veggie"
        self._update_url()

    def _update_url(self):
        """Updates the URL query parameters based on the active selection"""
        if self.active_category == "fruit":
            pn.state.location.search = f"?category=fruit&item={self.fruit}"
        else:
            pn.state.location.search = f"?category=veggie&item={self.veggie}"

    def _sync_from_url(self):
        """Initialize selections from URL query parameters if present."""
        params_from_url = pn.state.location.query_params
        if "category" in params_from_url and "item" in params_from_url:
            category = params_from_url["category"]
            item = params_from_url["item"]
            
            if category == "fruit" and item in self.param.fruit.objects:
                with param.discard_events(self):
                    self.fruit = item
                    self.active_category = "fruit"
            elif category == "veggie" and item in self.param.veggie.objects:
                with param.discard_events(self):
                    self.veggie = item
                    self.active_category = "veggie"

    @pn.depends('active_category', 'fruit', 'veggie')
    def item_display(self):
        """Display the currently selected item."""
        if self.active_category == "fruit":
            item = self.fruit
            category = "Fruit"
        else:
            item = self.veggie
            category = "Vegetable"
            
        return pn.Column(
            pn.pane.Markdown(f"## Selected {category}: {item}"),
            pn.pane.PNG(f"https://source.unsplash.com/300x300/?{item}", height=300, width=300)
        )

    def view(self):
        """Returns the main Panel layout for the app."""
        return pn.Column(
            pn.pane.Markdown("# Deep Linked Selector Demo"),
            
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("## Fruits"),
                    pn.widgets.Select.from_param(self.param.fruit, name="Select Fruit")
                ),
                pn.Column(
                    pn.pane.Markdown("## Vegetables"),
                    pn.widgets.Select.from_param(self.param.veggie, name="Select Vegetable")
                )
            ),
            
            pn.pane.Markdown("---"),
            self.item_display,
            pn.pane.Markdown("---"),
            pn.pane.Markdown("**Instructions:**\n\n"
                            "1. Select a fruit or vegetable from either dropdown\n"
                            "2. Notice the URL updates with your selection\n"
                            "3. Copy the URL and open it in a new tab - your selection will be preserved\n")
        )

# Instantiate the app
app = DeepLinkedMenuApp()

# Create Panel layout and make it servable
app_layout = app.view()
app_layout.servable(title="Deep Linked Selector Demo")

# To run this app:
# panel serve deepLinks2.py