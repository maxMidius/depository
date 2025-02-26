import panel as pn

# Initialize Panel extension with w3.css
pn.extension(
    css_files=[
        "https://www.w3schools.com/w3css/4/w3.css"
    ]
)

# Define the title
title = pn.pane.HTML("<h3 class='w3-large w3-center'> My Website Title</h3>")

# Define the main content area
main_content = pn.pane.HTML("<h4>Main Content Area</h4><p>This is a placeholder for the main content.</p>")

# Define the callback function to update the main content area
def update_main_content(event):
    main_content.object = f"<h4>{event.new}</h4><p>This is the content for {event.new}.</p>"

# Define the sidebar menu items using Accordion
menu_items = pn.layout.Accordion(
    ('Menu Item 1', pn.widgets.Select(
        name='Sub Menu 1',
        options={'Sub Item 1.1': 'Sub Item 1.1', 'Sub Item 1.2': 'Sub Item 1.2'},
        width=200
    )),
    ('Menu Item 2', pn.widgets.Select(
        name='Sub Menu 2',
        options={'Sub Item 2.1': 'Sub Item 2.1', 'Sub Item 2.2': 'Sub Item 2.2'},
        width=200
    )),
    active_header_background='#f1f1f1'
)

# Attach the callback function to the menu items
menu_items.param.watch(update_main_content, 'active')

# Define the layout
layout = pn.template.MaterialTemplate(
    title='My Website',
    sidebar=[menu_items],
    main=[title, main_content]
)

# Serve the layout
layout.servable()