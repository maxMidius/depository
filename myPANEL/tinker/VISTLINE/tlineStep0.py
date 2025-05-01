import panel as pn
import param
from panel.custom import JSComponent
from rich import print
import json

# Load the vis-timeline library AND CSS as an extension
pn.extension(js_files={
    'vis-timeline': "https://unpkg.com/vis-timeline@7.7.0/standalone/umd/vis-timeline-graph2d.min.js",
    'vis-data': "https://unpkg.com/vis-data@7.1.4/standalone/umd/vis-data.min.js"
}, css_files=[
    "https://unpkg.com/vis-timeline@7.7.0/dist/vis-timeline-graph2d.min.css"
])

class VisTimelineComponent(JSComponent):
    object = param.Dict()
    # Add parameters for events
    item_click = param.Event(default=None)

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
            # Trigger the event for listeners
            self.param.trigger('item_click')
        elif message.startswith('itemSelect:'):
            items_data = json.loads(message.replace('itemSelect:', '').strip())
            print(f"Items selected: {items_data}")
        elif message.startswith('rangeChanged:'):
            range_data = json.loads(message.replace('rangeChanged:', '').strip())
            print(f"Range changed: {range_data}")

def timeline_data():
    """Sample timeline data with items and groups"""
    return {
        "data": {
            "items": [
                {"id": 1, "content": "Task 1", "start": "2023-01-01", "end": "2023-01-10", "group": 1},
                {"id": 2, "content": "Task 2", "start": "2023-01-05", "end": "2023-01-15", "group": 1},
                {"id": 3, "content": "Task 3", "start": "2023-01-12", "end": "2023-01-20", "group": 2},
                {"id": 4, "content": "Task 4", "start": "2023-01-18", "end": "2023-02-05", "group": 2},
                {"id": 5, "content": "Milestone", "start": "2023-01-25", "type": "point", "group": 3},
                {"id": 6, "content": "Task 5", "start": "2023-01-28", "end": "2023-02-10", "group": 3},
                {"id": 7, "content": "Task 6", "start": "2023-02-01", "end": "2023-02-15", "group": 4}
            ],
            "groups": [
                {"id": 1, "content": "Project A"},
                {"id": 2, "content": "Project B"},
                {"id": 3, "content": "Project C"},
                {"id": 4, "content": "Project D"}
            ]
        },
        "options": {
            "stack": True,
            "editable": False,
            "margin": {
                "item": 10,
                "axis": 5
            },
            "orientation": "top",
            "showTooltips": True,
            "tooltip": {
                "followMouse": True,
                "overflowMethod": "flip"
            },
            "zoomKey": "ctrlKey",
            "zoomMin": 1000 * 60 * 60 * 24,  # one day in milliseconds
            "zoomMax": 1000 * 60 * 60 * 24 * 31 * 3  # about 3 months in milliseconds
        }
    }

# Create the timeline component
timeline_component = VisTimelineComponent(
    object=timeline_data(), height=400, sizing_mode="stretch_width"
)

# Add a title
title = pn.pane.Markdown("# Vis.js Timeline Component")

# Server display
pn.Column(
    title, 
    timeline_component,
    sizing_mode="stretch_width"
).servable()