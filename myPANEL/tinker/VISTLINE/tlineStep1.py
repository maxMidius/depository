import panel as pn
import param
from panel.custom import JSComponent
from rich import print
import json

# Import the timeline data from the separate file
from timelineData import timeline_data

# Load the vis-timeline library AND CSS as an extension
pn.extension(js_files={
    'vis-timeline': "https://unpkg.com/vis-timeline@7.7.0/standalone/umd/vis-timeline-graph2d.min.js",
    'vis-data': "https://unpkg.com/vis-data@7.1.4/standalone/umd/vis-data.min.js"
}, css_files=[
    "https://unpkg.com/vis-timeline@7.7.0/dist/vis-timeline-graph2d.min.css",
    "https://www.w3schools.com/w3css/4/w3.css"  # Add W3.CSS for styling
])

class VisTimelineComponent(JSComponent):
    object = param.Dict()
    # Add parameters for events
    item_click = param.Event(default=None)
    # Add a parameter to store clicked item information
    click_info = param.String(default="No item clicked yet. Click on a timeline item to see details.")

    _esm = """
    export function render({ model, el }) {
        // Create a container for the timeline
        const container = document.createElement('div');
        container.style.width = '100%';
        container.style.height = '400px';
        el.append(container);
        
        // Store full data
        const timelineData = model.object.data;
        
        // Create and configure the timeline
        const create_timeline = () => {
            // Check if vis is available
            if (typeof vis === 'undefined') {
                console.error("vis library not loaded");
                el.innerHTML = "<p>Error: Timeline library not loaded</p>";
                return null;
            }
            
            try {
                // Create DataSets (allows for dynamic data loading/updating)
                const items = new vis.DataSet(timelineData.items);
                const groups = new vis.DataSet(timelineData.groups);
                
                // Configuration for the Timeline
                const options = model.object.options || {};
                
                // Create a Timeline
                const timeline = new vis.Timeline(container, items, options);
                
                // Set groups separately after initialization
                timeline.setGroups(groups);
                
                // Add event handlers
                timeline.on('click', function(properties) {
                    if (properties.item) {
                        const itemId = properties.item;
                        const item = items.get(itemId);
                        console.log("Clicked item:", item);
                        
                        // Send the item data to Python
                        const jsonData = JSON.stringify(item);
                        model.send_msg(`itemClick: ${jsonData}`);
                    }
                });
                
                // Add selection event
                timeline.on('select', function(properties) {
                    const selectedItems = properties.items;
                    if (selectedItems.length > 0) {
                        console.log("Selected items:", selectedItems);
                        
                        // Get detailed data for selected items
                        const selectedData = items.get(selectedItems);
                        const jsonData = JSON.stringify(selectedData);
                        model.send_msg(`itemSelect: ${jsonData}`);
                    }
                });
                
                // Add range change event (when zooming or moving the timeline)
                timeline.on('rangechanged', function(properties) {
                    console.log("Range changed:", properties);
                    const jsonData = JSON.stringify({
                        start: properties.start.toISOString(),
                        end: properties.end.toISOString(),
                        byUser: properties.byUser
                    });
                    model.send_msg(`rangeChanged: ${jsonData}`);
                });
                
                return timeline;
            } catch (error) {
                console.error("Error creating timeline:", error);
                el.innerHTML = "<p>Error: Unable to create timeline</p>";
                return null;
            }
        };
        
        let timeline = create_timeline();

        // Handle updates to the data
        model.on("object", () => {
            if (timeline) {
                timeline.destroy();
            }
            timeline = create_timeline();
        });

        // Clean up when removed
        model.on('remove', () => {
            if (timeline) {
                timeline.destroy();
            }
        });
    }
    """

    # Handler for messages from JavaScript
    def _handle_msg(self, message):
        print(message)  # For debugging
        
        if message.startswith('itemClick:'):
            item_data = json.loads(message.replace('itemClick:', '').strip())
            print(f"Item clicked: {item_data}")
            
            # Format a nice message for display
            html = f"""
            <div class="w3-panel w3-pale-blue w3-leftbar w3-border-blue">
                <h3>Item Details</h3>
                <p><strong>ID:</strong> {item_data['id']}</p>
                <p><strong>Content:</strong> {item_data['content']}</p>
                <p><strong>Start:</strong> {item_data['start']}</p>
                {"<p><strong>End:</strong> " + item_data.get('end', 'N/A') + "</p>" if 'end' in item_data else ""}
                <p><strong>Type:</strong> {item_data.get('type', 'range')}</p>
                <p><strong>Group:</strong> {item_data['group']}</p>
            </div>
            """
            
            # Update the click_info parameter
            self.click_info = html
            
            # Trigger the event for listeners
            self.param.trigger('item_click')
            
        elif message.startswith('itemSelect:'):
            items_data = json.loads(message.replace('itemSelect:', '').strip())
            print(f"Items selected: {items_data}")
        elif message.startswith('rangeChanged:'):
            range_data = json.loads(message.replace('rangeChanged:', '').strip())
            print(f"Range changed: {range_data}")

# Create the timeline component
timeline_component = VisTimelineComponent(
    object=timeline_data(), height=400, sizing_mode="stretch_width"
)

# Add a title
title = pn.pane.HTML("""
<div class="w3-container w3-teal w3-padding">
    <h1>Vis.js Timeline Component</h1>
    <p>Click on timeline items to see details below</p>
</div>
""", sizing_mode="stretch_width")

# Create an info panel to display click events
info_panel = pn.pane.HTML(
    pn.bind(lambda info: info, timeline_component.param.click_info),
    sizing_mode="stretch_width"
)

# Server display
pn.Column(
    title, 
    timeline_component,
    info_panel,
    sizing_mode="stretch_width"
).servable()