import panel as pn

pn.extension()

# Create a SlidesTemplate instance
template = pn.template.SlidesTemplate(title="Nested Slides Example", reveal_theme="solarized")

# Chapter 1 and its vertical slides
chapter1_slides = [
    pn.pane.Markdown("""
        # Chapter 1: Introduction
        (Use UP/DOWN arrows to see sub-slides)
        """, sizing_mode="stretch_width"),
    pn.pane.Markdown("""
        ## Slide 1.1: Overview
        Welcome to the overview of Chapter 1.
        """, sizing_mode="stretch_width"),
    pn.pane.Markdown("""
        ## Slide 1.2: Details
        Here we provide additional details for Chapter 1.
        """, sizing_mode="stretch_width")
]

# Chapter 2 and its vertical slides
chapter2_slides = [
    pn.pane.Markdown("""
        # Chapter 2: Interactive Demo
        (Use UP/DOWN arrows to see interactive examples)
        """, sizing_mode="stretch_width"),
    pn.Column(
        pn.pane.Markdown("""
            ## Slide 2.1: Widget Demo
            Try the slider below:
            """, sizing_mode="stretch_width"),
        pn.widgets.FloatSlider(
            name="Demo Slider", 
            start=0, 
            end=10, 
            value=5, 
            width=300
        )
    ),
    pn.pane.Markdown("""
        ## Slide 2.2: Conclusion
        Thank you for your attention!
        """, sizing_mode="stretch_width")
]

# Add slides to the template
for slide in chapter1_slides:
    template.main.append(slide)
for slide in chapter2_slides:
    template.main.append(slide)

# Serve the template
template.servable()