import panel as pn
from ipytree import Node, Tree
import pandas as pd

# Initialize Panel extension to support ipywidgets
pn.extension('ipywidgets')

# Load the World Cities dataset
world_cities = pd.read_csv('/home/maximus/GIT/DR/depository/worldcities.csv')

# Limit the dataset to a sample of 100 rows for faster loading
world_cities = world_cities.sample(n=100, random_state=42)

# Debugging: Print dataset head to verify loading
print("Dataset Head:")
print(world_cities.head())

# Define the tree structure dynamically based on the dataset
data_tree = Tree(multiple_selection=False)

# Handle NaN values in the 'city' column by replacing them with a default string
for country, country_data in world_cities.groupby('country'):
    country_node = Node(country)
    for _, city_row in country_data.iterrows():
        city_name = city_row['city'] if not pd.isna(city_row['city']) else "Unknown City"
        city_node = Node(city_name)
        city_node.add_node(Node(f"Population: {city_row['population']}") if not pd.isna(city_row['population']) else Node("Population: N/A"))
        country_node.add_node(city_node)
    data_tree.add_node(country_node)

# Debugging: Print tree structure after creation
print("Tree Structure:")
for node in data_tree.nodes:
    print(f"Country Node: {node.name}, Cities: {[child.name for child in node.nodes]}")

# Define a callback to display node details
def on_node_click(event):
    clicked_node = event['new']
    if clicked_node:
        details_pane.object = f"Clicked Node: {clicked_node.name}"

# Attach the callback to the tree
data_tree.observe(on_node_click, names='selected_nodes')

# Add buttons to expand and collapse all nodes
expand_button = pn.widgets.Button(name='Expand All', button_type='primary')
collapse_button = pn.widgets.Button(name='Collapse All', button_type='danger')

# Define expand and collapse functions
def expand_all(event):
    for node in data_tree.nodes:
        node.opened = True

def collapse_all(event):
    for node in data_tree.nodes:
        node.opened = False

# Attach functions to buttons
expand_button.on_click(expand_all)
collapse_button.on_click(collapse_all)

# Create a Panel layout
details_pane = pn.pane.Markdown("Click a node to see details here.")
layout = pn.Column(pn.Row(expand_button, collapse_button), data_tree, details_pane)

# Serve the app
layout.servable()