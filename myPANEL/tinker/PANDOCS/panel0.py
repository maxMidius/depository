import panel as pn

pn.extension()

pn.panel("Hello World").servable()



text = """A wind turbine is a renewable energy device that converts the kinetic energy from wind into electricity. It typically consists of a tall tower with large blades attached to a rotor. As the wind blows, it causes the rotor to spin, which in turn rotates a generator to produce electricity. Wind turbines are designed to harness the natural power of the wind and are used to generate clean, sustainable energy. They come in various sizes, from small residential turbines to massive commercial installations, and play a crucial role in reducing greenhouse gas emissions and meeting renewable energy goals."""

pn.panel(text, width=300).servable()