import panel as pn

pn.extension()

def get_content_for_route(route_segments):
    """
    Returns Panel content based on the route segments.
    """
    if not route_segments or route_segments == [""]: # Base path or empty path
        return pn.pane.Markdown("# Welcome to AppName\nThis is the main page.")
    elif route_segments == ["r1"]:
        return pn.pane.Markdown("# Route Level 1: r1\nContent for the first level route 'r1'.")
    elif route_segments == ["r1", "r2"]:
        return pn.pane.Markdown("# Route Level 2: r1/r2\nContent for the nested route 'r1/r2'.")
    elif route_segments == ["r3", "r4", "r5"]:
        return pn.pane.Markdown("# Route Level 3: r3/r4/r5\nExample of a deeper nested route.")
    else:
        return pn.pane.Markdown("## 404 - Route Not Found\nInvalid sub-navigation path.")


@pn.depends(pn.state.location.param.pathname)
def app_content(pathname):
    """
    Reactive function to determine content based on the URL pathname.
    """
    # Remove leading slash and split the path into segments
    route_segments = [segment for segment in pathname.strip('/').split('/') if segment]
    return get_content_for_route(route_segments)


# --- Create the Panel App Layout ---
app_layout = pn.Column(
    pn.pane.Markdown("## Panel App with Sub-Navigation Routing"),
    pn.pane.Markdown("Navigate using URLs like:\n\n"
                     "- `/appName` (or `/appName/`)\n"
                     "- `/appName/r1`\n"
                     "- `/appName/r1/r2`\n"
                     "- `/appName/r3/r4/r5`\n"
                     "- `/appName/invalid-route`"), # Example of an invalid route
    pn.layout.Divider(),
    app_content  # Reactive content area
)

app_layout.servable() #  Make it servable with the name "appName"