import marimo

__generated_with = "0.10.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json

    # Sample data structure
    project_data = {
        "Project A": {
            "Deliverable 1": ["Task 1.1", "Task 1.2", "Task 1.3"],
            "Deliverable 2": ["Task 2.1", "Task 2.2"]
        },
        "Project B": {
            "Deliverable 3": ["Task 3.1", "Task 3.2"],
            "Deliverable 4": ["Task 4.1", "Task 4.2", "Task 4.3"]
        }
    }

    # Convert the data structure to a format suitable for d3.js
    def convert_to_tree(data):
        tree = {
            "name": "Projects",
            "children": []
        }

        for project, deliverables in data.items():
            project_node = {
                "name": project,
                "children": []
            }

            for deliverable, tasks in deliverables.items():
                deliverable_node = {
                    "name": deliverable,
                    "children": [{"name": task} for task in tasks]
                }
                project_node["children"].append(deliverable_node)

            tree["children"].append(project_node)

        return tree

    # Convert data to tree format
    tree_data = convert_to_tree(project_data)

    # Create the HTML/JavaScript code for the mindmap
    html_code = f"""
    <!DOCTYPE html>
    <div id="mindmap"></div>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
    .node circle {{
        fill: #fff;
        stroke: steelblue;
        stroke-width: 3px;
    }}

    .node text {{
        font: 12px sans-serif;
    }}

    .link {{
        fill: none;
        stroke: #ccc;
        stroke-width: 2px;
    }}
    </style>
    <script>
    const treeData = {json.dumps(tree_data)};

    // Set the dimensions and margins of the diagram
    const margin = {{top: 20, right: 90, bottom: 30, left: 90}},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // Create the tree layout
    const treemap = d3.tree().size([height, width]);

    // Assigns parent, children, height, depth
    const root = d3.hierarchy(treeData);
    const nodes = treemap(root);

    // Create the SVG container
    const svg = d3.select("#mindmap")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

    // Adds the links between the nodes
    const link = svg.selectAll(".link")
        .data(nodes.descendants().slice(1))
        .join("path")
            .attr("class", "link")
            .attr("d", d => `
                M ${{d.y}},${{d.x}}
                C ${{(d.y + d.parent.y) / 2}},${{d.x}}
                  ${{(d.y + d.parent.y) / 2}},${{d.parent.x}}
                  ${{d.parent.y}},${{d.parent.x}}
            `);

    // Adds each node as a group
    const node = svg.selectAll(".node")
        .data(nodes.descendants())
        .join("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${{d.y}},${{d.x}})`);

    // Adds the circle to the node
    node.append("circle")
        .attr("r", 10);

    // Adds the text to the node
    node.append("text")
        .attr("dy", ".35em")
        .attr("x", d => d.children ? -13 : 13)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => d.data.name);
    </script>
    """

    # Display the mindmap using Marimo's mo.Html
    mo.Html(html_code)
    return convert_to_tree, html_code, json, mo, project_data, tree_data


if __name__ == "__main__":
    app.run()
